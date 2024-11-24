# import json
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
#
# @csrf_exempt  # Чтобы отключить CSRF-защиту, так как мы используем fetch (только для отладки, лучше включить CSRF токен)
# def generate_image(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         prompt = data.get("text", "")
#
#         # Если текст не предоставлен, возвращаем ошибку
#         if not prompt:
#             return JsonResponse({"error": "Empty prompt provided."}, status=400)
#
#         # Получаем API ключи из настроек
#         API_URL = "https://api-key.fusionbrain.ai/"  # Замените на реальный URL
#         API_KEY = settings.API_KEY_KANDINSKY
#         SECRET_KEY = settings.SECRET_KEY_KANDINSKY
#
#         # Заголовки для авторизации
#         headers = {
#             'X-Key': f'Key {API_KEY}',
#             'X-Secret': f'Secret {SECRET_KEY}',
#         }
#
#         # Запрос к API
#         model_id = "ID_вашей_модели"  # Укажите ID модели, если это не меняется динамически
#         payload = {
#             "model_id": model_id,
#             "params": {
#                 "type": "GENERATE",
#                 "numImages": 1,
#                 "width": 1024,
#                 "height": 1024,
#                 "generateParams": {
#                     "query": prompt
#                 }
#             }
#         }
#
#         try:
#             # Генерация изображения
#             response = requests.post(f"{API_URL}/key/api/v1/text2image/generated", headers=headers, json=payload)
#             response.raise_for_status()
#             response_data = response.json()
#
#             # Проверка статуса генерации изображения
#             request_id = response_data.get("uuid")
#             status_response = requests.get(f"{API_URL}/key/api/v1/text2image/status/{request_id}", headers=headers)
#
#             if status_response.ok and status_response.json().get("status") == "DONE":
#                 images = status_response.json().get("images", [])
#                 if images:
#                     return JsonResponse({"image_url": images[0]}, status=200)
#
#             # В случае, если изображения нет
#             return JsonResponse({"error": "Image generation failed."}, status=500)
#
#         except requests.RequestException as e:
#             return JsonResponse({"error": f"Request error: {e}"}, status=500)
#
#     # Ответ для любых других методов
#     return JsonResponse({"error": "Only POST method is allowed."}, status=405)
