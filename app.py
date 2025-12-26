import os
import cv2
import img2pdf
import yt_dlp
from flask import Flask, render_template, request, send_file, jsonify
import uuid
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp_downloads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max payload (not strictly relevant for URL input but good practice)

# Ensure temp directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def download_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]/best[ext=mp4]/best', # Prioritize video-only or best mp4
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def extract_frames(video_path, interval):
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise Exception("Could not open video file")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)
    
    current_frame = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if current_frame % frame_interval == 0:
            # Convert to RGB (OpenCV uses BGR)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Encode to JPEG in memory
            _, buffer = cv2.imencode('.jpg', frame_rgb, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            frames.append(buffer.tobytes())
            
        current_frame += 1
        
    cap.release()
    return frames

@app.route('/')
def index():
    return render_template('index.html')

import io

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.json
    url = data.get('url')
    interval = float(data.get('interval', 5.0))
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    session_id = str(uuid.uuid4())
    session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(session_dir)
    
    video_path = os.path.join(session_dir, 'video.mp4')
    
    try:
        # 1. Download Video
        download_video(url, video_path)
        
        # 2. Extract Frames
        frames = extract_frames(video_path, interval)
        
        if not frames:
            return jsonify({'error': 'No frames extracted. Check video or interval.'}), 400

        # 3. Create PDF in memory
        pdf_bytes = img2pdf.convert(frames)
        
        # Cleanup immediately before sending response
        try:
            shutil.rmtree(session_dir)
        except Exception as e:
            print(f"Error cleaning up: {e}")

        return send_file(
            io.BytesIO(pdf_bytes),
            as_attachment=True,
            download_name='frames.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        # Cleanup on error
        if os.path.exists(session_dir):
            try:
                shutil.rmtree(session_dir)
            except Exception as cleanup_error:
                print(f"Error cleaning up after failure: {cleanup_error}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
