from django.http import HttpResponse
from django.views import View
from datetime import datetime

# Новая классовая view для статей
class IndexView(View):
    def get(self, request, *args, **kwargs):
        # Данные для передачи в шаблон через контекст
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
        
        # Используем render для отображения шаблона
        from django.shortcuts import render
        return render(request, "articles/index.html", context=context)
