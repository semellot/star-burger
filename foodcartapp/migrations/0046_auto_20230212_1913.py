# Generated by Django 3.2.15 on 2023-02-12 19:13

from django.db import migrations


def add_price_to_order_item(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    for order_item in OrderItem.objects.all():
        order_item.price = order_item.product.price * order_item.quantity
        order_item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0045_orderitem_quantity'),
    ]

    operations = [
        migrations.RunPython(add_price_to_order_item),
    ]
