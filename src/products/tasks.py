from celery import shared_task
from .kandinsky import Text2ImageAPI
from django.conf import settings
import base64


@shared_task
def generate_image(prompt):
    api = Text2ImageAPI(
        url='https://api-key.fusionbrain.ai/',
        api_key=settings.API_KEY_KANDINSKY,
        secret_key=settings.SECRET_KEY_KANDINSKY,
    )

    model_id = api.get_model()
    if not model_id:
        raise Exception("Не удалось получить модель для генерации.")

    uuid = api.generate(prompt, model_id)
    if not uuid:
        raise Exception("Произошла ошибка при генерации изображения.")

    images = api.check_generation(uuid)
    if not images:
        raise Exception("Изображение еще не готово")
    image_data = base64.b64decode(images[0])
    image_url = "data:image/png;base64," + base64.b64encode(image_data).decode('utf-8')
    return image_url

