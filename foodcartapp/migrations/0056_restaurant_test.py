# Generated by Django 3.2.15 on 2023-06-02 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0055_auto_20230329_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='test',
            field=models.CharField(blank=True, max_length=50, verbose_name='Тестовое поле'),
        ),
    ]
