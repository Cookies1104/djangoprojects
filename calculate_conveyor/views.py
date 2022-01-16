from django.shortcuts import render, redirect
from .models import Conveyor
from .services import Calculate
from .forms import ConveyorForm, ResultForm


# Create your views here.
def calculate(request):
    """Рендерит страницу ввода данных для расчёта конвейера"""
    return render(request, './index.html', {
        'form': ConveyorForm()
    })


def result(request):
    """Если POST - рендерит страницу результата расчёта с формой предложения сохранить
    результат расчёта.
        Если no POST - возвращает на страницу ввода данных для расчёта"""
    if request.POST:
        if 'ascent_or_descent' in request.POST:
            ascent_or_descent = True
        else:
            ascent_or_descent = False
        if 'point_speed' in request.POST:
            point_speed = True
        else:
            point_speed = False
        if 'point_precipitation' in request.POST:
            point_precipitation = True
        else:
            point_precipitation = False
        if 'point_conditions' in request.POST:
            point_conditions = True
        else:
            point_conditions = False
        if 'lining' in request.POST:
            lining = True
        else:
            lining = False

        first_conveyor = Calculate(
            name_conveyor=request.POST['name'],
            capacity=request.POST['capacity'],
            number_of_conveyor=request.POST['number_of_conveyor'],
            material=request.POST['material'],
            material_size=request.POST['material_size'],
            ascent_or_descent=ascent_or_descent,
            length_conveyor=request.POST['length_conveyor'],
            height_conveyor=request.POST['height_conveyor'],
            drop_height=request.POST['drop_height'],
            point_speed=point_speed,
            point_precipitation=point_precipitation,
            point_conditions=point_conditions,
            lining=lining,
            drum_girth_angle=request.POST['drum_girth_angle'],
            KPD=request.POST['KPD']
        )
        result_dict = first_conveyor.calculate()
        result_dict['save'] = ResultForm

        element = Conveyor(
            name_conveyor=request.POST['name'],
            capacity=request.POST['capacity'],
            number_of_conveyor=request.POST['number_of_conveyor'],
            material=request.POST['material'],
            material_size=request.POST['material_size'],
            ascent_or_descent=ascent_or_descent,
            length_conveyor=request.POST['length_conveyor'],
            height_conveyor=request.POST['height_conveyor'],
            drop_height=request.POST['drop_height'],
            point_speed=point_speed,
            point_precipitation=point_precipitation,
            point_conditions=point_conditions,
            lining=lining,
            drum_girth_angle=request.POST['drum_girth_angle'],
            KPD=request.POST['KPD']
        )
        element.save()
        return render(request, './result.html', result_dict)
    else:
        return redirect('calculate', permanent=True)


def save(request):
    """Если POST рендерит страницу успешного сохранения и присваивает значение True в бд.
        Если no POST возвращает на страницу ввода данных для расчёта."""
    if request.POST:
        # storage = {'name': request.POST['name']}
        # print(storage)
        # print(request.POST)
        # capacity = request.POST['capacity']
        # number_of_conveyor = request.POST['number_of_conveyor']
        # capacity_calc = request.POST['capacity_calc']
        # element = Conveyor(name=name, capacity=capacity, number_of_conveyor=number_of_conveyor)
        # element.save()
        return render(request, './save.html')
    else:
        return redirect('calculate', permanent=True)
