import yt_dlp
import os

def download_youtube_video(url, output_path="."):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Pobieranie wideo...")
            ydl.download([url])

        print(f"Pobieranie zakończone. Plik zapisany w: {output_path}")

    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")

# URL wideo do pobrania
video_url = "https://www.youtube.com/watch?v=uV-gAMV6J-Y"

# Ścieżka, gdzie ma być zapisane wideo (domyślnie bieżący katalog)
output_directory = "."

# Wywołanie funkcji do pobrania wideo
download_youtube_video(video_url, output_directory)