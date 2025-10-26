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
        self.assertContains(response, "Список статей")
        self.assertContains(response, "Тестовая статья 1")
        self.assertContains(response, "Тестовая статья 2")
        self.assertContains(response, "Всего статей: 2")

    def test_articles_list_context_data(self):
        """Тест проверяет что в контекст передаются правильные данные"""
        response = self.client.get('/articles/')
        self.assertIn('articles', response.context)
        articles = response.context['articles']
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].name, "Тестовая статья 1")
        self.assertEqual(articles[1].name, "Тестовая статья 2")

    def test_articles_list_shows_articles_from_db(self):
        """Тест проверяет что список статей показывает статьи из базы данных"""
        response = self.client.get('/articles/')
        self.assertContains(response, "Тестовая статья 1")
        self.assertContains(response, "Тестовая статья 2")

    def test_home_page_redirect(self):
        """Тест проверяет что главная страница перенаправляет на статью"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, 
            reverse('article', kwargs={'tags': 'python', 'article_id': 42})
        )

    def test_article_detail_page(self):
        """Тест проверяет страницу просмотра конкретной статьи"""
        response = self.client.get(reverse('article_detail', kwargs={'id': self.article1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article1.name)
        self.assertContains(response, self.article1.body)
        self.assertTemplateUsed(response, 'articles/show.html')

    def test_article_detail_nonexistent(self):
        """Тест проверяет 404 для несуществующей статьи"""
        response = self.client.get(reverse('article_detail', kwargs={'id': 999}))
        self.assertEqual(response.status_code, 404)

    def test_article_list_links_to_detail(self):
        """Тест проверяет что в списке статей есть ссылки на детальный просмотр"""
        response = self.client.get('/articles/')
        self.assertContains(response, f'href="/articles/{self.article1.id}/"')
        self.assertContains(response, f'href="/articles/{self.article2.id}/"')

    def test_article_create_form_page(self):
        """Тест проверяет страницу формы создания статьи"""
        response = self.client.get(reverse('articles_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/create.html')
        self.assertContains(response, 'Создание новой статьи')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="body"')

    def test_article_create_success(self):
        """Тест проверяет успешное создание статьи"""
        articles_count_before = Article.objects.count()
        form_data = {
            'name': 'Новая тестовая статья',
            'body': 'Содержание новой тестовой статьи'
        }
        response = self.client.post(reverse('articles_create'), form_data)
    
        self.assertRedirects(response, reverse('articles'))
    
        # Проверяем что статья добавилась в базу
        self.assertEqual(Article.objects.count(), articles_count_before + 1)
    
        # Проверяем флеш-сообщение
        response = self.client.get(reverse('articles'))
        self.assertContains(response, 'Новая тестовая статья')

    def test_article_create_validation(self):
        """Тест проверяет валидацию формы"""
        form_data = {
            'name': '',  # Пустое название
            'body': 'Содержание'
        }
        response = self.client.post(reverse('articles_create'), form_data)
    
        # Проверяем что остаемся на странице формы с ошибками
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/create.html')
        self.assertContains(response, 'Пожалуйста, исправьте ошибки')

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
        
        article1 = Article.objects.get(pk=1)
        self.assertEqual(article1.name, "Введение в Django")
        
        article2 = Article.objects.get(pk=2) 
        self.assertEqual(article2.name, "Основы моделей в Django")
