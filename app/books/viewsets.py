from .models import Book
from rest_framework import viewsets
from.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Book instances.
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all()
