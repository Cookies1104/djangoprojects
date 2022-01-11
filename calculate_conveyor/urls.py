from django.urls import path
from .views import calculate, result

urlpatterns = [
    path('', calculate, name='calculate'),
    path('result/', result, name='result'),
]
