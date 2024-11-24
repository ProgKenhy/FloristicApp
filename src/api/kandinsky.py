# import json
# import time
# import requests
# from django.conf import settings
#
#
# class Text2ImageAPI:
#     BASE_PATH = 'key/api/v1'
#     GENERATE_PATH = BASE_PATH + 'text2image/generated'
#     STATUS_PATH = BASE_PATH + 'text2image/status'
#
#     def __init__(self, url: str, api_key: str, secret_key: str):
#         self.URL = url
#         self.AUTH_HEADERS = {
#             'X-Key': f'Key {api_key}',
#             'X-Secret': f'Secret {secret_key}',
#         }
#
#     def get_model(self) -> str:
#         try:
#             response = requests.get(self.URL + self.BASE_PATH + 'models', headers=self.AUTH_HEADERS)
#             response.raise_for_status()  # Проверка на успешность запроса
#             data = response.json()
#             if data and 'id' in data[0]:
#                 return data[0]['id']
#             raise ValueError("Model ID not found in response data.")
#         except requests.exceptions.RequestException as e:
#             print(f'Error fetching model ID: {e}')
#             return ""
#
#     def generate(self, prompt: str, model: str, images: int = 1, width: int = 1024, height: int = 1024) -> str:
#         params = {
#             "type": "GENERATE",
#             "numImages": images,
#             "width": width,
#             "height": height,
#             "generateParams": {
#                 "query": prompt
#             }
#         }
#
#         data = {
#             'model_id': (None, model),
#             'params': (None, json.dumps(params), 'application/json')
#         }
#
#         try:
#             response = requests.post(self.URL + self.GENERATE_PATH, headers=self.AUTH_HEADERS, files=data)
#             response.raise_for_status()
#             data = response.json()
#             return data.get('uuid', "")
#         except requests.exceptions.RequestException as e:
#             print(f"Error during generation request: {e}")
#             return ""
#
#     def check_generation(self, request_id: str, attempts: int = 10, delay: int = 10) -> list:
#         for _ in range(attempts):
#             try:
#                 response = requests.get(self.URL + self.STATUS_PATH + request_id, headers=self.AUTH_HEADERS)
#                 response.raise_for_status()
#                 data = response.json()
#
#                 if data.get('status') == 'DONE':
#                     return data.get('images', [])
#             except requests.exceptions.RequestException as e:
#                 print(f"Error checking generations status: {e}")
#                 return []
#
#             time.sleep(delay)
#         print("Generation did not complete within the given attempts.")
#         return []
#
#
# if __name__ == '__main__':
#     API_KEY_KANDINSKY = settings.API_KEY_KANDINSKY
#     SECRET_KEY_KANDINSKY = settings.SECRET_KEY_KANDINSKY
#     api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY_KANDINSKY, SECRET_KEY_KANDINSKY)
#     model_id = api.get_model()
#     if model_id:
#         uuid = api.generate("Sun in sky", model_id)
#         if uuid:
#             images = api.check_generation(uuid)
#             print(images)
