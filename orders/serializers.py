from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Order, OrderItem
from catalog.models import Book


class OrderItemSerializer(ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_id = serializers.CharField(source='book.id', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'book_title','book_id', 'book','quantity', 'price']
        read_only_fields = ['price'] 


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'total_amount', 'items']
        read_only_fields = ['user', 'created_at', 'status', 'total_amount']
    
    def validate(self, data):
        items_data = data.get('items', [])
    
        if not items_data:
            raise serializers.ValidationError("Order must contain at least one item.")
        
        for item_data in items_data:
            book = item_data['book']   
            quantity = item_data['quantity']

            if book.stock < quantity:
                raise serializers.ValidationError(f"This book does not have enough stock.")
            
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        user = self.context['request'].user

        order = Order.objects.create(user=user, **validated_data)
        total_amount = 0

        for item_data in items_data:
            book = item_data['book']   
            quantity = item_data['quantity']

            if book.stock < quantity:
                raise serializers.ValidationError(
                    f"THis book does not have enough stock."
                )

            book.stock -= quantity
            book.save()

            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=quantity,
                price=book.price
            )

            total_amount += book.price * quantity

        order.total_amount = total_amount
        order.save(update_fields=['total_amount'])

        return order
