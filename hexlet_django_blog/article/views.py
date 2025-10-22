from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from hexlet_django_blog.article.models import Article


class IndexView(View):
    def get(self, request, *args, **kwargs):
        # Проверяем, переданы ли параметры tags и article_id
        tags = kwargs.get('tags', None)
        article_id = kwargs.get('article_id', None)
        
        # Если параметры переданы - выводим информацию о статье
        if tags and article_id is not None:
            return HttpResponse(f"Статья номер {article_id}. Тег {tags}")
        
        # Иначе выводим список статей
        articles = Article.objects.all()[:15]
        return render(
            request,
            "articles/index.html",
            context={
                "articles": articles,
            },
        )
