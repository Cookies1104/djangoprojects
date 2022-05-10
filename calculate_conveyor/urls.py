from django.urls import path
from .views import data_entry_page_for_conveyor_calculation, save_page_complete


urlpatterns = [
    path('', data_entry_page_for_conveyor_calculation, name='calculate'),
    # path('result/', conveyor_calculation_results_page, name='result'),
    path('save/', save_page_complete, name='save'),
]
