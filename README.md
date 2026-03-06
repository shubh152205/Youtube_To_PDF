# YouTube to PDF Converter

A powerful Flask-based web application that allows users to download YouTube videos, extract frames at specified intervals, and compile them into a high-quality PDF document.

## 🚀 Features

- **YouTube Downloader**: Seamlessly downloads videos using `yt-dlp`.
- **Frame Extraction**: Uses OpenCV to capture frames at a user-defined interval (e.g., every 5 seconds).
- **PDF Generation**: Automatically converts extracted frames into a single PDF file using `img2pdf`.
- **In-Memory Processing**: Efficiently handles PDF creation without storing large intermediate files.
- **Modern Clean Interface**: Simple and intuitive web dashboard.

## 🛠️ Tech Stack

- **Backend**: Python (Flask)
- **Video Processing**: [yt-dlp](https://github.com/yt-dlp/yt-dlp), [OpenCV](https://opencv.org/)
- **PDF Conversion**: [img2pdf](https://github.com/josch/img2pdf)
- **Frontend**: HTML/CSS/JavaScript
- **Server**: Gunicorn (for deployment)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shubh152205/youtube_to_pdf.git
   cd youtube_to_pdf
   ```

2. **Set up a virtual environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000`.

## 🌐 Deployment

This project is configured for deployment on **Heroku** or similar platforms using the included `Procfile`.

1. Ensure all dependencies are in `requirements.txt`.
2. Connect your repository to Heroku.
3. Deploy!

## 📄 License

This project is open-source and for educational purposes.
