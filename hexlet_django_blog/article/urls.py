from django.urls import path
from hexlet_django_blog.article.views import IndexView

urlpatterns = [
    path("<str:tags>/<int:article_id>/", IndexView.as_view(), name="article"),
    path("", IndexView.as_view(), name="articles"),  # добавляем name для списка
]
