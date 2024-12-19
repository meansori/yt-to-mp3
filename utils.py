import yt_dlp
import os
import time
import logging

# Konfigurasi folder temporary untuk menyimpan file
TEMP_DIR = "/tmp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Konfigurasi logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def cleanup_old_files():
    """Membersihkan file yang lebih dari 1 jam"""
    current_time = time.time()
    for filename in os.listdir(TEMP_DIR):
        filepath = os.path.join(TEMP_DIR, filename)
        if os.path.getmtime(filepath) < (current_time - 3600):
            try:
                os.remove(filepath)
                logger.info(f"Deleted old file: {filepath}")
            except Exception as e:
                logger.error(f"Error cleaning up file {filepath}: {str(e)}")

def extract_youtube_audio(url, output_path=TEMP_DIR, quality='192', audio_format='mp3'):
    """
    Mengunduh audio dari YouTube dengan pilihan kualitas dan format
    
    Args:
        url (str): URL video YouTube
        output_path (str): Direktori untuk menyimpan audio
        quality (str): Kualitas audio ('128', '192', '256', '320')
        audio_format (str): Format audio ('mp3', 'wav', 'aac', 'm4a')
    
    Returns:
        str: Path file audio yang dihasilkan
    """
    # Validasi input
    valid_qualities = ['128', '192', '256', '320']
    valid_formats = ['mp3', 'wav', 'aac', 'm4a']
    
    if quality not in valid_qualities:
        quality = '192'  # Default
    
    if audio_format not in valid_formats:
        audio_format = 'mp3'  # Default
    
    # Konfigurasi yt-dlp untuk ekstraksi audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': quality,
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ekstrak informasi video
            info_dict = ydl.extract_info(url, download=True)
            
            # Dapatkan nama file audio
            audio_filename = ydl.prepare_filename(info_dict)
            audio_filename = audio_filename.rsplit('.', 1)[0] + f'.{audio_format}'
            
            return audio_filename
    
    except Exception as e:
        raise ValueError(f"Gagal mengunduh audio: {str(e)}")

# Contoh penggunaan
if __name__ == "__main__":
    try:
        # Bersihkan file lama sebelum mengunduh
        cleanup_old_files()
        
        # Unduh audio dari YouTube
        youtube_url = "https://www.youtube.com/watch?v=example"
        audio_file = extract_youtube_audio(youtube_url)
        logger.info(f"Audio berhasil diunduh: {audio_file}")
    except Exception as e:
        logger.error(f"Terjadi kesalahan: {str(e)}")
