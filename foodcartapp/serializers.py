from rest_framework import serializers

from .models import Order
from .models import OrderItem

from phonenumber_field.serializerfields import PhoneNumberField


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class PhoneNumberSerializer(serializers.Serializer):
    phonenumber = PhoneNumberField(region="CA")

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    products = OrderItemSerializer(many=True, allow_empty=False, write_only=True)
    address=serializers.CharField(max_length=100)
    firstname=serializers.CharField(max_length=50)
    lastname=serializers.CharField(max_length=50)
    phonenumber=PhoneNumberField()

    def create(self, validated_data):
        order = Order.objects.create(
            address=validated_data['address'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber']
        )
        products_fields = validated_data['products']
        products = [OrderItem(order=order, price=fields['product'].price, **fields) for fields in products_fields]
        OrderItem.objects.bulk_create(products)
        return order

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']
