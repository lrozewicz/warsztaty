from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

completion = client.chat.completions.create(
  model="nvidia/nemotron-4-340b-instruct",
  messages=[{"role":"user","content":"Napisz w stylu młodzieżowym streszczenie Pana Tadeusza."}],
  temperature=0.2,
  top_p=0.7,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")

