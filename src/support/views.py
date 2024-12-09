from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from support.models import ChatSupportMessage, ChatSupportSession


class SupportPageView(LoginRequiredMixin, TemplateView):
    template_name = 'support/support_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            session_id = self.kwargs.get('session_id')
            session = get_object_or_404(ChatSupportSession, id=session_id)
        else:
            session = ChatSupportSession.objects.filter(user=self.request.user).first()
        context["session"] = session
        context["messages"] = session.messages.order_by("timestamp") if session else []
        return context


class SendMessageView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            content = request.data.get('content')
            sender = "Модератор" if request.user.is_staff else request.user.first_name.title()
            if request.user.is_staff:
                session_id = request.data.get('session_id')
                if not session_id:
                    return JsonResponse({"error": "Не указан ID сессии."}, status=400)
                session = ChatSupportSession.objects.filter(id=session_id).first()
            else:
                session, created = ChatSupportSession.objects.get_or_create(user=request.user)

            message = ChatSupportMessage.objects.create(
                session=session,
                sender=sender,
                content=content,
            )

            # Перенаправление обратно на страницу чата
            return redirect('support:support_page')
        except ChatSupportSession.DoesNotExist:
            return JsonResponse({"error": "Сессия не найдена."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class ModeratorDashboardView(TemplateView):
    template_name = 'support/support_page_for_moderator.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        sessions = ChatSupportSession.objects.all().order_by("created_at")
        context["sessions"] = sessions
        return context
