from django.contrib import admin
from django.urls import path, include
from hexlet_django_blog.views import about, IndexView  # изменяем импорт

urlpatterns = [
    path("", IndexView.as_view()),  # используем классовую view
    path("about/", about),
    path("articles/", include("hexlet_django_blog.article.urls")),
    path("admin/", admin.site.urls),
]
