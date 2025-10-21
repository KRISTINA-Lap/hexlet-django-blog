from django.shortcuts import render, redirect  # добавляем redirect
from django.urls import reverse  # добавляем reverse
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

    def get(self, request, *args, **kwargs):
        # Перенаправляем с главной страницы на /articles/python/42
        return redirect(reverse('article', kwargs={'tags': 'python', 'article_id': 42}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["who"] = "World"
        return context
