from rest_framework.generics import ListCreateAPIView
from .models import Book
from .serializers import BookSerializer

class BookListCreateAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
