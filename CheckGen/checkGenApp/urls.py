from django.urls import path, include
from . import views
#from rest_framework.routers import DefaultRouter

app_name = 'checkGenApp'

urlpatterns = [
    path('create_check/', views.create_check, name='create_check'),
    path('unprinted_check/', views.unprinted_check, name='unprinted_check'),
    path('printed_check/', views.printed_check, name='printed_check'),
]
