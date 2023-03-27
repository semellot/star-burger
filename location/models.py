from django.db import models

from environs import Env

env = Env()
env.read_env()


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
        return {self.address}

    def save(self, *args, **kwargs):
        if not self.pk:
            apikey = env.str('YANDEX_APIKEY')
            fetch_coordinates(apikey, self.address)
        super().save(*args, **kwargs)
