from django.urls import path

from products.views import TranslaterView

app_name = 'translater'

urlpatterns = [
    path('', TranslaterView.as_view(), name='index'),
]
