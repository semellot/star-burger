# Generated by Django 4.1.6 on 2023-02-09 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_orderitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Элемент заказа', 'verbose_name_plural': 'Элементы заказа'},
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='foodcartapp.product', verbose_name='Товар'),
        ),
    ]
