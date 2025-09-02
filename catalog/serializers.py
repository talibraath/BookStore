from rest_framework import serializers
from .models import Author, Category, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    author_id = serializers.CharField(source='author.id', read_only=True)

    category_id = serializers.CharField(source='category.id', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)


    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'stock','author_name', 'author_id','category_name','category_id',  'pub_date', 'description']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value
