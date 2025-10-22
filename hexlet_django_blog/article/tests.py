from django.test import TestCase
from django.urls import reverse
from .models import Article


class ArticleTest(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.article1 = Article.objects.create(
            name="Тестовая статья 1",
            body="Содержание первой тестовой статьи"
        )
        self.article2 = Article.objects.create(
            name="Тестовая статья 2", 
            body="Содержание второй тестовой статьи"
        )

    def test_article_detail_with_parameters_status_code(self):
        """Тест проверяет что страница статьи с параметрами возвращает статус 200"""
        response = self.client.get(reverse('article', kwargs={'tags': 'python', 'article_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_article_detail_with_parameters_content(self):
        """Тест проверяет содержание страницы статьи с параметрами"""
        response = self.client.get(reverse('article', kwargs={'tags': 'django', 'article_id': 42}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Статья номер 42")
        self.assertContains(response, "Тег django")

    def test_article_detail_different_parameters(self):
        """Тест проверяет отображение статьи с разными параметрами"""
        response = self.client.get(reverse('article', kwargs={'tags': 'python', 'article_id': 100}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Статья номер 100")
        self.assertContains(response, "Тег python")

    def test_articles_list_without_parameters_status_code(self):
        """Тест проверяет что страница списка статей возвращает статус 200"""
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)

    def test_articles_list_without_parameters_template(self):
        """Тест проверяет что для списка статей используется правильный шаблон"""
        response = self.client.get('/articles/')
        self.assertTemplateUsed(response, 'articles/index.html')

    def test_articles_list_without_parameters_content(self):
        """Тест проверяет содержание страницы списка статей"""
        response = self.client.get('/articles/')
        self.assertContains(response, "Articles App")
        self.assertContains(response, "Приложение для управления статьями блога")

    def test_articles_list_context_data(self):
        """Тест проверяет что в контекст передаются правильные данные"""
        response = self.client.get('/articles/')
        self.assertIn('app_name', response.context)
        self.assertIn('articles', response.context)
        self.assertEqual(response.context['app_name'], 'Articles App')
        self.assertEqual(len(response.context['articles']), 3)  # 3 тестовые статьи из view

    def test_home_page_redirect(self):
        """Тест проверяет что главная страница перенаправляет на статью"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # 302 - redirect
        self.assertRedirects(
            response, 
            reverse('article', kwargs={'tags': 'python', 'article_id': 42})
        )


class ArticleModelTest(TestCase):
    def test_article_creation(self):
        """Тест создания статьи в базе данных"""
        article = Article.objects.create(
            name="Тест создания статьи",
            body="Тестовое содержание статьи"
        )
        self.assertEqual(article.name, "Тест создания статьи")
        self.assertEqual(article.body, "Тестовое содержание статьи")
        self.assertIsNotNone(article.created_at)
        self.assertIsNotNone(article.updated_at)

    def test_article_str_method(self):
        """Тест метода __str__ модели Article"""
        article = Article.objects.create(
            name="Тестовая статья",
            body="Содержание"
        )
        self.assertEqual(str(article), "Тестовая статья")


class ArticleWithFixturesTest(TestCase):
    fixtures = ['articles.json']

    def test_articles_loaded_from_fixture(self):
        """Тест проверяет загрузку данных из фикстуры"""
        articles = Article.objects.all()
        self.assertTrue(articles.count() > 0)
        print(f"Загружено статей из фикстуры: {articles.count()}")
        
        # Проверяем конкретные статьи
        article1 = Article.objects.get(pk=1)
        self.assertEqual(article1.name, "Введение в Django")
        
        article2 = Article.objects.get(pk=2) 
        self.assertEqual(article2.name, "Основы моделей в Django")
