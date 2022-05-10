from django.shortcuts import render

from .forms import CrossSectionForm


# Create your views here.
def calculate(request):
    """Рендерит страницу ввода данных для расчёта короба конвейера"""
    return render(request, './calculate_box_height.html', {
        'form': CrossSectionForm()
    })
