from flask import Flask, request, send_file
import youtube_dl
import os

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url')
    format_type = request.json.get('format')
    
    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'mp3' else 'best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format_type == 'mp3' else [],
        'outtmpl': '/tmp/download.%(ext)s',
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return send_file('/tmp/download.mp3' if format_type == 'mp3' else '/tmp/download.mp4')

if __name__ == '__main__':
    app.run()
