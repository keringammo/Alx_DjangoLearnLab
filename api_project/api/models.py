# api/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)   # Book title
    author = models.CharField(max_length=100)  # Author name

    def __str__(self):
        return f"{self.title} by {self.author}"
