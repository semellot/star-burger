import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.templatetags.static import static

from .models import Product
from .models import Order
from .models import OrderItem

from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
    try:
        for key in {'firstname', 'lastname', 'phonenumber', 'address'}:
            if key not in request.data:
                raise ValueError(f'{key}: Обязательное поле')
            elif not request.data[key]:
                raise ValueError(f'{key}: Это поле не может быть пустым')
            elif not isinstance(request.data[key], str):
                raise ValueError(f'{key}: Ожидается str')

        phone_number = PhoneNumber.from_string(request.data['phonenumber'])
        if not phone_number.is_valid():
            raise ValueError('phonenumber: Введен некорректный номер телефона')

        if 'products' not in request.data:
            raise ValueError('products: Обязательное поле')
        elif not request.data['products']:
            raise ValueError('products: Этот список не может быть пустым')
        elif not isinstance(request.data['products'], list):
            raise ValueError('products: Ожидался list со значениями')
        else:
            order = Order.objects.create(
                address=request.data['address'],
                first_name=request.data['firstname'],
                last_name=request.data['lastname'],
                phone_number=PhoneNumber.from_string(request.data['phonenumber'])
            )
        
            for item in request.data['products']:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=Product.objects.get(id=item['product']),
                    count=item['quantity']
                )
            
        return Response({},status=status.HTTP_200_OK)
    except ValueError as error:
        return Response(
            {'error': error.args[0]},
            status=status.HTTP_200_OK
        )
    except Product.DoesNotExist:
        return Response(
            {'error': 'products: Недопустимый первичный ключ'},
            status=status.HTTP_200_OK
        )
    except NumberParseException.INVALID_COUNTRY_CODE:
        return Response(
            {'error': 'phonenumber: Введен некорректный номер телефона'},
            status=status.HTTP_200_OK
        )

