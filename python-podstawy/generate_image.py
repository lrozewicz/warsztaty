import requests

r = requests.post('https://clipdrop-api.co/text-to-image/v1',
  files = {
      'prompt': (None, "an obese American woman goes jogging", 'text/plain')
  },
  headers = { 'x-api-key': '1c6d11617efcc8d147481d93fbeed98ba26ef6b7eba0f8a6aeedb696b124c68b5aef96e53e92640ba4775ef1c64adb7a'}
)
if (r.ok):
  # r.content contains the bytes of the returned image
  with open('output_image.jpg', 'wb') as f:
    f.write(r.content)
    print("Image saved as output_image.jpg.")
else:
  r.raise_for_status()