from django.contrib import admin
from django.urls import path
from hexlet_django_blog import views  # добавляем импорт

urlpatterns = [
    path("", views.index),  # главная страница
    path("about/", views.about),  # страница "О блоге"
    path("admin/", admin.site.urls),
]
