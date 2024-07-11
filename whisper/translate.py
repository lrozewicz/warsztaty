from openai import OpenAI
import os

# Ustawienie klucza API
os.environ['OPENAI_API_KEY'] = ''

client = OpenAI()

# Funkcja do odczytu pliku SRT
def read_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Funkcja do zapisu przetłumaczonego tekstu do pliku SRT
def write_srt(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Odczyt oryginalnych napisów
original_subtitles = read_srt('napisy.srt')

# Tłumaczenie napisów
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "Jesteś profesjonalnym tłumaczem. Przetłumacz poniższe napisy zachowując format SRT."
        },
        {
            "role": "user",
            "content": f"Przetłumacz te napisy na polski:\n\n{original_subtitles}"
        }
    ],
    temperature=0.3,
    max_tokens=4000,
    top_p=1
)

# Pobranie przetłumaczonego tekstu
translated_subtitles = response.choices[0].message.content

# Zapis przetłumaczonych napisów
write_srt('napisy_pl.srt', translated_subtitles)

print("Tłumaczenie zakończone. Przetłumaczone napisy zapisano w pliku 'napisy_pl.srt'.")