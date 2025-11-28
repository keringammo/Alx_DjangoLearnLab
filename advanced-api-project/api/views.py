# api/views.py

from rest_framework import generics, filters
from django_filters import rest_framework as django_filters  # <-- required import
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Add filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields you can filter by
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Fields you can search by
    search_fields = ['title', 'author__name']

    # Fields you can order by
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering
