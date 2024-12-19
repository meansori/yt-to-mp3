from flask import Flask, request, jsonify, send_file, render_template
from utils import extract_youtube_audio
import os

app = Flask(__name__, 
            static_folder='static', 
            template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_link():
    url = request.json.get('url', '')
    quality = request.json.get('quality', '192')
    audio_format = request.json.get('format', 'mp3')
    
    try:
        # Untuk YouTube, gunakan fungsi extract_youtube_audio
        if 'youtube.com' in url or 'youtu.be' in url:
            audio_path = extract_youtube_audio(
                url, 
                quality=quality, 
                audio_format=audio_format
            )
            return jsonify({
                'status': 'success',
                'audio_url': f'/download/{os.path.basename(audio_path)}'
            })
        
        # Untuk platform lain (placeholder)
        return jsonify({
            'status': 'error',
            'message': 'Platform selain YouTube belum didukung'
        }), 400
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/download/<filename>')
def download_audio(filename):
    return send_file(f'audio/{filename}', as_attachment=True)

if __name__ == '__main__':
    os.makedirs('audio', exist_ok=True)
    app.run(debug=True)