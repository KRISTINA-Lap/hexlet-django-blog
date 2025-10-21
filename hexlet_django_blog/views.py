from django.shortcuts import render
from django.views.generic.base import TemplateView

# Старая функция about остается пока как функция
def about(request):
    tags = ["обучение", "программирование", "python", "oop", "django", "hexlet"]
    return render(
        request,
        "about.html",
        context={"tags": tags},
    )

# Новая классовая view для главной страницы
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["who"] = "World"
        return context
