from openai import OpenAI
import os
os.environ['OPENAI_API_KEY'] = ''

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": "Przedstaw zalety i wady pracy zdalnej."
    }
  ],
  temperature=0.5, #1 - kreatywny, 0 - bardziej dokładny
  max_tokens=500,
  top_p=1
)

print(response.choices[0].message.content)