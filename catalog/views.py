from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, BasePermission, AllowAny
from .models import Author, Category, Book
from .serializers import AuthorSerializer, CategorySerializer, BookSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, response

# Create your views here.
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
        
    def get_queryset(self):
        qs = Book.objects.prefetch_related()
        

        author_id = self.request.query_params.get("author")
        category_id = self.request.query_params.get("category")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        search = self.request.query_params.get("search")
        ordering = self.request.query_params.get("ordering")  

        if author_id:
            qs = qs.filter(author_id=author_id)

        if category_id:
            qs = qs.filter(category_id=category_id)

        if min_price and max_price:
            qs = qs.filter(price__gte=min_price, price__lte=max_price)
        elif min_price:
            qs = qs.filter(price__gte=min_price)
        elif max_price:
            qs = qs.filter(price__lte=max_price)

        if start_date and end_date:
            qs = qs.filter(pub_date__range=[start_date, end_date])
        elif start_date:
            qs = qs.filter(pub_date__gte=start_date)
        elif end_date:
            qs = qs.filter(pub_date__lte=end_date)

        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(author__name__icontains=search) |
                Q(category__name__icontains=search)
            )

        allowed = {"title", "-title", "price", "-price", "pub_date", "-pub_date"}
        if ordering in allowed:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by("title")
        
        return qs
