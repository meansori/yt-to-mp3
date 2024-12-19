import yt_dlp
import os

def extract_youtube_audio(url, output_path='audio', quality='192', audio_format='mp3'):
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
    # Buat direktori audio jika belum ada
    os.makedirs(output_path, exist_ok=True)
    
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
        'outtmpl': os.path.join(output_path, '%(title)s_%(height)s.%(ext)s'),
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