from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
        "body_preview",  # добавляем кастомное поле
    )
    search_fields = ["name", "body"]
    list_filter = (
        ("created_at", DateFieldListFilter),
    )
    fieldsets = (
        (None, {
            'fields': ('name', 'body')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    # Кастомный метод для отображения превью тела статьи
    def body_preview(self, obj):
        return obj.body[:50] + "..." if len(obj.body) > 50 else obj.body
    body_preview.short_description = 'Превью содержания'
