Instalacja zależności:
pip install -r requirements.txt

download.py <- pobiera plik mp3 na podstawie URLa do filmu na youtube. Czasem rzuca błędy (zabezpieczenia youtube) i trzeba plik uruchomić kilka razy

transcription.py <- generuje transkrypcję z pliku audio.mp3.
Może być przebna zmiana języka
result = pipe("audio.mp3", generate_kwargs={"language": "ja"})
lub spróbowanie aby sam wykrył (nie zawsze to działa)
result = pipe("audio.mp3")

translate.py <- tłumaczy plik napisy.srt na język polski i zapisuje jako napisy_pl.srt

youtube_downloader.py <- pobiera wskazny film youtube w najwyższej możliwej jakości i zapisuje jako mp4