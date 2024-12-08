from support.views import (SupportPageView, SendMessageView, ModeratorDashboardView)
from django.urls import path


app_name = 'support'

urlpatterns = [
    path('', SupportPageView.as_view(), name='support_page'),
    path('<int:session_id>/', SupportPageView.as_view(), name='session'),
    path('send-message/', SendMessageView.as_view(), name='send_message'),
    path('moderator-dashboard/', ModeratorDashboardView.as_view(), name='moderator_dashboard'),
]