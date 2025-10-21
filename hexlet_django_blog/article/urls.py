from django.urls import path
from hexlet_django_blog.article.views import IndexView  # изменяем импорт

urlpatterns = [
    path("", IndexView.as_view()),  # используем классовую view
]
