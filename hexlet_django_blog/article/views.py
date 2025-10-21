from django.http import HttpResponse
from django.views import View
from datetime import datetime
from django.shortcuts import render

class IndexView(View):
    def get(self, request, *args, **kwargs):
        # Проверяем, переданы ли параметры tags и article_id
        tags = kwargs.get('tags', None)
        article_id = kwargs.get('article_id', None)
        
        # Если параметры переданы - выводим информацию о статье
        if tags and article_id is not None:
            return HttpResponse(f"Статья номер {article_id}. Тег {tags}")
        
        # Иначе выводим старую страницу со списком статей
        context = {
            "app_name": "Articles App",
            "description": "Приложение для управления статьями блога",
            "article_count": 3,
            "created_date": datetime.now().strftime("%d.%m.%Y"),
            "tags": ["Django", "Python", "Web", "Блог", "Хекслет"],
            "articles": [
                {
                    "title": "Первая статья в блоге",
                    "content": "Это содержание первой статьи, написанной для демонстрации работы шаблонов Django.",
                    "author": "Администратор"
                },
                {
                    "title": "Изучение Django",
                    "content": "Django - это мощный фреймворк для веб-разработки на Python.",
                    "author": "Автор"
                },
                {
                    "title": "Шаблоны в Django",
                    "content": "Шаблоны позволяют отделить логику представления от разметки HTML.",
                    "author": "Разработчик"
                }
            ]
        }
        return render(request, "articles/index.html", context=context)
