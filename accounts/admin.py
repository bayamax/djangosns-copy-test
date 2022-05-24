from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Connection
from django.contrib.gis import admin as geoadmin
from testmap.models import Border
from leaflet.admin import LeafletGeoAdmin

class BorderAdmin(LeafletGeoAdmin):
  search_fields = ['n03_001','n03_003','n03_004']
  list_filter = ('n03_003')

admin.site.register(Border, geoadmin.OSMGeoAdmin)
admin.site.register(get_user_model())
admin.site.register(Connection)
