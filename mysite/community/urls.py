from django.urls import path
from . import views


app_name = 'community'

urlpatterns = [
    path('community_create/', views.community_create, name='community_create'),
]