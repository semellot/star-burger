from django.db import models

import requests
from environs import Env

env = Env()
env.read_env()


def fetch_coordinates(apikey, address):
    print(f'Address: {address}')
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    print(f'longitude: {lon}')
    print(f'latitude: {lat}')
    return lat, lon


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
