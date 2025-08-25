from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, BasePermission, AllowAny
from .models import Author, Category, Book
from .serializers import AuthorSerializer, CategorySerializer, BookSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Book.objects.all()

        author = self.request.query_params.get("author")
        category = self.request.query_params.get("category")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        start_date = self.request.query_params.get("start_date")  
        end_date = self.request.query_params.get("end_date")
        search = self.request.query_params.get("search")

        if author:
            queryset = queryset.filter(author__name__iexact=author)

        if category:
            queryset = queryset.filter(category__name__isexact=category)

        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        elif min_price:
            queryset = queryset.filter(price__gte=min_price)

        elif max_price:
            queryset = queryset.filter(price__lte=max_price)

        if start_date and end_date:
            queryset = queryset.filter(publication_date__range=[start_date, end_date])

        elif start_date:
            queryset = queryset.filter(publication_date__gte=start_date)

        elif end_date:
            queryset = queryset.filter(publication_date__lte=end_date)

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(author__name__icontains=search))

        return queryset
