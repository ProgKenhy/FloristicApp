from support.views import (SupportPageView, SendMessageView, ModeratorDashboardView)
from django.urls import path


app_name = 'support'

urlpatterns = [
    path('', SupportPageView.as_view(), name='support_page'),
    path('send-message/', SendMessageView.as_view(), name='send_message'),
    path('moderator-dashboard/', ModeratorDashboardView.as_view(), name='moderator_dashboard'),
    path('session/<int:session_id>/', SupportPageView.as_view(), name='session'),
]