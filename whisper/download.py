import yt_dlp
import os

def download_audio(url, output_path='./', custom_filename=None):
    if custom_filename:
        # Usuń rozszerzenie .mp3, jeśli zostało podane
        custom_filename = os.path.splitext(custom_filename)[0]
        output_template = os.path.join(output_path, f"{custom_filename}.%(ext)s")
    else:
        output_template = os.path.join(output_path, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_template,
        'overwrites': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

        # Znajdź oryginalny plik (przed konwersją)
        original_file = filename
        if os.path.exists(original_file):
            os.remove(original_file)

        # Określ nazwę pliku MP3
        mp3_filename = os.path.splitext(filename)[0] + '.mp3'

    return mp3_filename

# Przykładowe użycie
url = "https://www.youtube.com/watch?v=uV-gAMV6J-Y"

# Bez własnej nazwy pliku
output_file = download_audio(url)
print(f"Plik audio został pobrany i zapisany jako: {output_file}")

# Z własną nazwą pliku
custom_name = "audio.mp3"
output_file = download_audio(url, custom_filename=custom_name)
print(f"Plik audio został pobrany i zapisany jako: {output_file}")