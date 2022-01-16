from django.urls import path
from .views import calculate, result, save

urlpatterns = [
    path('', calculate, name='calculate'),
    path('result/', result, name='result'),
    path('save/', save, name='save'),
]
