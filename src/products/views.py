import openai
from celery.result import AsyncResult
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from openai import OpenAIError

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

        return JsonResponse({
            'task_id': task.id,
            'message': "Запрос на генерацию изображения отправлен. Проверьте статус позже.",
        })


def task_status(request, task_id):
    result = AsyncResult(task_id)

    if result.state == 'PENDING':
        return JsonResponse({'status': 'pending'})

    if result.state == 'SUCCESS':
        return JsonResponse({'status': 'success', 'image_url': result.result})

    if result.state == 'FAILURE':
        return JsonResponse({'status': 'failure', 'error': str(result.result)})

    return JsonResponse({'status': result.state})


class TranslaterView(TemplateView):
    template_name = 'products/translate.html'
    title = 'FloriAI - Translater'

    def post(self, request, *args, **kwargs):
        context = {}
        if request.FILES.get('file'):
            file = request.FILES['file']
            file_name = default_storage.save(f"temp/{file.name}", file)
            file_path = default_storage.path(file_name)

            try:
                openai.api_key = settings.API_KEY_OPENAI

                with open(file_path, 'rb') as img:
                    response = openai.Image.create_edit(
                        image=img,
                        prompt="Определите цветы на букете и их значения",
                        n=1,
                        size="1024x1024"
                    )

                if response and 'data' in response:
                    context['result'] = response['data']
                else:
                    context['error'] = 'Ошибка анализа изображения'

            except OpenAIError as e:
                context['error'] = f"Ошибка OpenAI: {str(e)}"
            finally:
                default_storage.delete(file_path)

            return self.render_to_response(context)

        context['error'] = 'Пожалуйста, загрузите файл'
        return self.render_to_response(context)


class ContactView(TemplateView):
    template_name = 'products/contact.html'
    title = 'FloriAI - Contact'
