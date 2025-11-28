from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")
        self.book1 = Book.objects.create(title="Python Basics", publication_year=2020, author=self.author1)
        self.book2 = Book.objects.create(title="Advanced Python", publication_year=2021, author=self.author2)
        self.client = APIClient()

    # List & Retrieve
    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    # Create
    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book-create')
        data = {"title": "New Book", "publication_year": 2023, "author": self.author1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {"title": "Unauthorized Book", "publication_year": 2023, "author": self.author1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Update
    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book-update', args=[self.book1.id])
        data = {"title": "Updated Title", "publication_year": 2020, "author": self.author1.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_update_book_unauthenticated(self):
        url = reverse('book-update', args=[self.book1.id])
        data = {"title": "Fail Update", "publication_year": 2020, "author": self.author1.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Delete
    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        url = reverse('book-delete', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Filtering, Searching, Ordering
    def test_filter_books_by_author(self):
        url = reverse('book-list') + f'?author__name={self.author1.name}'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Python Basics")

    def test_search_books(self):
        url = reverse('book-list') + '?search=Advanced'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Advanced Python")

    def test_order_books_by_publication_year_desc(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.data[0]['publication_year'], 2021)
