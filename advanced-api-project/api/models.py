from django.db import models

class Author(models.Model):
    # Stores the author's name
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    # Title of the book
    title = models.CharField(max_length=255)
    # Year the book was published
    publication_year = models.IntegerField()
    # ForeignKey linking each book to one author (one-to-many relationship)
    # related_name='books' allows us to access all books of an author via author.books.all()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return self.title

