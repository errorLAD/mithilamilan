from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomeView(TemplateView):
    template_name = 'static_pages/home.html'

class AboutView(TemplateView):
    template_name = 'static_pages/about.html'

class TermsView(TemplateView):
    template_name = 'static_pages/terms.html'

class PrivacyView(TemplateView):
    template_name = 'static_pages/privacy.html'
