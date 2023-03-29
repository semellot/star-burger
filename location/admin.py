from django.contrib import admin

from .models import Location

from location.geocode import fetch_coordinates

from environs import Env

env = Env()
env.read_env()


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    def response_change(self, request, obj):
        if not obj.latitude:
            apikey = env.str('YANDEX_APIKEY')
            try:
                lat, lon = fetch_coordinates(apikey, obj.address)
                obj.latitude = lat
                obj.longitude = lon
                obj.save()
            except:
                pass
        return super().response_change(request, obj)
