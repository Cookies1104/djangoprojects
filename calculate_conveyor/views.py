from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView

from .models import ConveyorModel
from .services import BeltConveyor, get_data_from_request
from .forms import ConveyorForm



class Index(DetailView):
    model = BeltConveyor



@require_http_methods(['GET', 'POST'])
def data_entry_page_for_conveyor_calculation(request):
    """Рендерит страницу ввода данных для расчёта конвейера"""
    print(request.method)
    if request.method == 'POST':
        request_data = get_data_from_request(request)
        if request_data is None:
            return redirect('calculate', permanent=True)

        calculate_data = BeltConveyor(**request_data).calculate()
        request.session['data'] = request_data
        return render(request, './result.html', calculate_data)
    else:
        return render(request, './index.html', {
            'form': ConveyorForm()
        })


# def conveyor_calculation_results_page(request):
#     """Если POST - рендерит страницу результата расчёта с формой предложения сохранить
#     результат расчёта.
#     Иначе - возвращает на страницу ввода данных для расчёта.
#     Передаёт введёныне пользователем данные, а также результаты расчёта в сессию"""
#     if request.POST:
#         request_data = get_data_from_request(request)
#         if request_data is None:
#             return redirect('calculate', permanent=True)
#
#         calculate_data = BeltConveyor(**request_data).calculate()
#         request.session['data'] = request_data
#         return render(request, './result.html', calculate_data)
#     else:
#         return redirect('calculate', permanent=True)


def save_page_complete(request):
    """Если POST сохраняет в бд экземпляр конвейера.
        Иначе - возвращает на страницу ввода данных для расчёта."""
    if request.POST:
        data = get_data_from_request(request) | request.session['data']
        name_conveyor = request.POST.get('name_conveyor', None)

        ConveyorModel(name=name_conveyor, data=data)#.save()

        return render(request, './save.html', {'name': name_conveyor})
    else:
        return redirect('calculate', permanent=True)
