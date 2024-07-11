import torch # Importuje bibliotekę PyTorch, która jest frameworkiem do głębokiego uczenia.
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline # Importuje klasy z biblioteki Hugging Face Transformers, służące do ładowania modeli i przetwarzania danych.
from datasets import load_dataset
import datetime


device = "cuda:0" if torch.cuda.is_available() else "cpu" #O kreśla, czy korzystać z GPU (cuda:0), jeśli jest dostępny, lub z CPU (cpu).
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32 #  Ustawia precyzję obliczeń na float16 dla GPU (jeśli dostępne, dla lepszej wydajności) lub float32 dla CPU.

model_id = "openai/whisper-large-v3" #  Identyfikator modelu do użycia, w tym przypadku "openai/whisper-large-v3" z repozytorium Hugging Face.

model = AutoModelForSpeechSeq2Seq.from_pretrained( # Ładuje model seq2seq (sekwencja do sekwencji) do rozpoznawania mowy z repozytorium Hugging Face, z określonymi parametrami.
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device) # Przenosi model na GPU (jeśli jest dostępne) lub pozostawia na CPU.

processor = AutoProcessor.from_pretrained(model_id) # konfigurują użycie pamięci, typu danych oraz SafeTensors (optymalizacja pamięci).

pipe = pipeline( # worzy potok do automatycznego rozpoznawania mowy.
# Parametry w pipeline definiują model, tokenizator, ekstraktor cech, maksymalną długość tokenów, długość fragmentów audio, wielkość partii, czy zwracać znaczniki czasowe, typ danych i urządzenie.
    "automatic-speech-recognition", # Określa typ potoku, który ma być utworzony. W tym przypadku jest to potok do automatycznego rozpoznawania mowy.
    model=model, # Przekazuje wcześniej załadowany model (w tym przypadku AutoModelForSpeechSeq2Seq dla "openai/whisper-large-v3") do potoku. Model ten jest używany do przetwarzania audio i generowania tekstu.
    tokenizer=processor.tokenizer, # Określa tokenizator, który jest częścią procesora (AutoProcessor). Tokenizator jest używany do przekształcania wygenerowanego tekstu na tokeny, które są zrozumiałe dla modelu.
    feature_extractor=processor.feature_extractor, # Określa ekstraktor cech, który również jest częścią procesora. Jest używany do przekształcania surowych danych audio w cechy, które mogą być przetwarzane przez model.
    #max_new_tokens=448, # Określa maksymalną liczbę nowych tokenów, które mogą być wygenerowane w każdej próbie predykcji. W kontekście ASR, ogranicza to długość generowanego tekstu.
    #chunk_length_s=30, # Określa długość fragmentu audio (w sekundach), który będzie przetwarzany w jednym kroku. Tutaj każdy fragment audio jest ograniczony do 30 sekund.
    batch_size=16, # Ustawia wielkość partii (batch size) przetwarzania. Oznacza to, że 16 fragmentów audio będzie przetwarzanych równocześnie, co może poprawić wydajność, ale wymaga więcej pamięci.
    return_timestamps="word", # Włącza zwracanie znaczników czasowych dla wygenerowanego tekstu. Dzięki temu można wiedzieć, kiedy dokładnie w pliku audio pojawia się dany fragment tekstu.
    torch_dtype=torch_dtype, # Określa typ danych tensorów PyTorch, których używa potok. W Twoim przypadku jest to torch.float16 na GPU lub torch.float32 na CPU, co wpływa na wydajność i dokładność.
    device=device, # Określa urządzenie, na którym potok będzie wykonywany (GPU lub CPU). Pozwala to na optymalizację wydajności potoku w zależności od dostępnego sprzętu.
    chunk_length_s=30,  # Ustawienie długości fragmentu na 30 sekund
    stride_length_s=5,  # Dodanie nakładania się fragmentów
)

dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation") # Ładuje zbiór danych "librispeech_long" z repozytorium "distil-whisper", używany do walidacji.
sample = dataset[0]["audio"] # Wybiera pierwszy przykład audio z wczytanego zestawu danych.

# result = pipe(sample)
# result = pipe("audio.mp3", generate_kwargs={"language": "polish"}) # Wywołuje potok ASR na pliku "wywiad.mp3", określając język na "polski".
result = pipe("audio.mp3", generate_kwargs={"language": "ja"})
#result = pipe("audio.mp3")
# print(result["text"]) # Wyświetla tekst wygenerowany przez model na podstawie przetworzonego pliku audio.
print(result["chunks"])

with open("transkrypcja.txt", "w", encoding="utf-8") as file:
    file.write(result["text"])

def format_timestamp(seconds):
    """Konwertuje sekundy na format timestamp używany w SRT."""
    return str(datetime.timedelta(seconds=seconds)).replace('.', ',')[:12]

# Funkcja do grupowania słów w linie
def group_words_into_lines(words, max_chars=40):
    lines = []
    current_line = []
    current_line_chars = 0

    for word in words:
        if current_line_chars + len(word['text']) + 1 > max_chars and current_line:
            lines.append(current_line)
            current_line = []
            current_line_chars = 0

        current_line.append(word)
        current_line_chars += len(word['text']) + 1

    if current_line:
        lines.append(current_line)

    return lines

# Zapisywanie transkrypcji w formacie SRT
with open("napisy.srt", "w", encoding="utf-8") as file:
    if "chunks" in result:
        words = result["chunks"]
        lines = group_words_into_lines(words)

        for i, line in enumerate(lines, start=1):
            start_time = line[0]["timestamp"][0]
            end_time = line[-1]["timestamp"][1]
            text = " ".join(word["text"] for word in line)

            file.write(f"{i}\n")
            file.write(f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n")
            file.write(f"{text}\n\n")
    else:
        # Jeśli nie ma znaczników czasowych, zapisz cały tekst jako jeden napis
        file.write("1\n")
        file.write("00:00:00,000 --> 99:59:59,999\n")
        file.write(result["text"])

print("Napisy zostały zapisane w pliku 'napisy.srt'")


