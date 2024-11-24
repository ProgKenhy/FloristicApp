import openai
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.generic.base import TemplateView

from .tasks import generate_image


class IndexView(TemplateView):
    template_name = 'products/index.html'
    title = 'FloriAI'

    def post(self, request, *args, **kwargs):
        prompt = request.POST.get('chatboxImageGen', '')

        if not prompt:
            return JsonResponse({'error': "Пожалуйста, введите запрос для генерации изображения."})

        # Запуск задачи для генерации изображения
        task = generate_image.delay(prompt)
        if task.id is None:
            return JsonResponse({'error': "Не удалось запустить задачу генерации изображения."})

        context = {
            'task_id': task.id,
            'message': "Запрос на генерацию изображения отправлен. Проверьте статус позже.",
            'image_url': task.get()  # Это будет передано в шаблон
        }

        # Вернемся на тот же шаблон с обновленным контекстом
        return self.render_to_response(context)


class TranslaterView(TemplateView):
    template_name = 'products/translate.html'
    title = 'FloriAI - Translater'

    def post(self, request, *args, **kwargs):
        if request.FILES.get('file'):
            file = request.FILES['file']
            file_path = default_storage.save(f"temp/{file.name}", file)

            try:
                openai.api_key = settings.API_KEY_OPENAI

                with open(file_path, 'rb') as img:
                    response = openai.Image.create_edit(
                        image=img,
                        prompt="Определите цветы на букете и их значения",
                        n=1,
                        size="1024x1024"
                    )

                default_storage.delete(file_path)

                if response and 'data' in response:
                    return JsonResponse({'status': 'success', 'data': response['data']})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Ошибка анализа изображения'}, status=500)
            except openai.error.OpenAIError as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        return JsonResponse({'status': 'error', 'message': 'Неверный запрос'}, status=400)


class ContactView(TemplateView):
    template_name = 'products/contact.html'
    title = 'FloriAI - Contact'
