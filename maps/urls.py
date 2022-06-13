from django.urls import path
from . import views


app_name = 'maps'

urlpatterns = [
    path('maps/', views.maps, name = 'maps'),
]