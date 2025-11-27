from django.db import models

class Author(models.Model):
    # Stores the author's name
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    # Book title
    title = models.CharField(max_length=255)
    # Year the book was published
    publication_year = models.IntegerField()
    # Links each book to an author (one-to-many)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return self.title
