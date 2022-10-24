from django.views.generic import TemplateView
from os import environ

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['environment'] = environ.get("ENVIRONMENT", "unknown")
        return context