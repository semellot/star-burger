import json
import io

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.templatetags.static import static

from phonenumber_field.phonenumber import PhoneNumber

from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Order
from .models import OrderItem
from .models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']


class OrderDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    phonenumber = serializers.CharField()
    address = serializers.CharField()


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    order = Order.objects.create(
        address=serializer.validated_data['address'],
        firstname=serializer.validated_data['firstname'],
        lastname=serializer.validated_data['lastname'],
        phonenumber=PhoneNumber.from_string(serializer.validated_data['phonenumber'])
    )

    products_fields = serializer.validated_data['products']
    products = [OrderItem(order=order, **fields) for fields in products_fields]
    OrderItem.objects.bulk_create(products)

    order_serializer = OrderDataSerializer(order)
    content = JSONRenderer().render(order_serializer.data)
    stream = io.BytesIO(content)
    data = JSONParser().parse(stream)

    return Response(data)
