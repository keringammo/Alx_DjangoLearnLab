from rest_framework import permissions
from rest_framework import viewsets, generics
from .models import Book
from .serializers import BookSerializer


# Existing ListAPIView (optional if you still want it)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# New ViewSet for full CRUD
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
