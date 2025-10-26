from django.urls import path
from hexlet_django_blog.article.views import IndexView, ArticleView

urlpatterns = [
    path("<str:tags>/<int:article_id>/", IndexView.as_view(), name="article"),
    path("<int:id>/", ArticleView.as_view(), name="article_detail"),
    path("", IndexView.as_view(), name="articles"),
]
