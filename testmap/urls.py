from django.urls import path
from . import views


app_name = 'testmap'

urlpatterns = [
    path('testmap/', views.index, name='testmap'),
]