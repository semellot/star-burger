from django.db import models


class Location(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=100,
        unique=True,
    )
    latitude = models.DecimalField(
        'Широта',
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        'Долгота',
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.address
