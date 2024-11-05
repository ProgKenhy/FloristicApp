from django.shortcuts import render
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'products/index.html'
    title = 'FloriAI'


class TranslaterView(TemplateView):
    template_name = 'products/translate.html'
    title = 'FloriAI - Translater'


class ContactView(TemplateView):
    template_name = 'products/contact.html'
    title = 'FloriAI - Contact'
