import json
import time
import requests
import base64
from django.conf import settings



class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    def save_image(self, image_base64, filename):
        image_data = base64.b64decode(image_base64)
        with open(filename, "wb") as image_file:
            image_file.write(image_data)


if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', settings.API_KEY_KANDINSKY, settings.SECRET_KEY_KANDINSKY)
    model_id = api.get_model()
    uuid = api.generate(
        "Картинка на рабочий стол для программиста без людей в наивысшем качестве",
        model_id)
    images = api.check_generation(uuid)

    # Save the first image as a file if the generation succeeded
    if images:
        api.save_image(images[0], "generated_image.jpg")
        print("Image saved as 'generated_image.jpg'")
    else:
        print("Image generation failed or timed out.")
