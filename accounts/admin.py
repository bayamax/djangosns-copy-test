from django.contrib import admin

from django.contrib.auth import get_user_model

from .models import Connection

from django.contrib.gis import admin as geoadmin

from testmap.models import Border

admin.site.register(Border, geoadmin.OSMGeoAdmin)

admin.site.register(get_user_model())

admin.site.register(Connection)
