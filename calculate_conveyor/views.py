from django.shortcuts import render
from .models import Conveyor
from .services import Calculate
from .forms import ConveyorForm, ResultForm


# Create your views here.
def calculate(request):
    form = ConveyorForm()
    return render(request, './index.html', {
        'form': form
    })


def result(request):
    if 'ascent_or_descent' in request.GET:
        ascent_or_descent = True
    else:
        ascent_or_descent = False
    if 'point_speed' in request.GET:
        point_speed = True
    else:
        point_speed = False
    if 'point_precipitation' in request.GET:
        point_precipitation = True
    else:
        point_precipitation = False
    if 'point_conditions' in request.GET:
        point_conditions = True
    else:
        point_conditions = False
    if 'lining' in request.GET:
        lining = True
    else:
        lining = False

    first_conveyor = Calculate(
        name_conveyor=request.GET['name'],
        capacity=request.GET['capacity'],
        number_of_conveyor=request.GET['number_of_conveyor'],
        material=request.GET['material'],
        material_size=request.GET['material_size'],
        ascent_or_descent=ascent_or_descent,
        length_conveyor=request.GET['length_conveyor'],
        height_conveyor=request.GET['height_conveyor'],
        drop_height=request.GET['drop_height'],
        point_speed=point_speed,
        point_precipitation=point_precipitation,
        point_conditions=point_conditions,
        lining=lining,
        drum_girth_angle=request.GET['drum_girth_angle'],
        KPD=request.GET['KPD']
    )
    result_dict = first_conveyor.calculate()
    print(result_dict)

    # capacity_calc = result_dict['capacity_calc']
    # print(result_dict)

    # element = Calculate(
    #     name_conveyor=request.GET['name'],
    #     capacity=request.GET['capacity'],
    #     number_of_conveyor=request.GET['number_of_conveyor'],
    #     material=request.GET['material'],
    #     material_size=request.GET['material_size'],
    #     ascent_or_descent=ascent_or_descent,
    #     length_conveyor=request.GET['length_conveyor'],
    #     height_conveyor=request.GET['height_conveyor'],
    #     drop_height=request.GET['drop_height'],
    #     point_speed=point_speed,
    #     point_precipitation=point_precipitation,
    #     point_conditions=point_conditions,
    #     lining=lining,
    #     drum_girth_angle=request.GET['drum_girth_angle'],
    #     KPD=request.GET['KPD']
    # )
    # element = Conveyor(name=name, capacity=capacity, number_of_conveyor=number_of_conveyor,
    #                    capacity_calc=capacity_calc, material=material, material_size=material_size)
    # element.save()
    return render(request, './result.html', result_dict)


# def save(request):
#     storage = {'name': request.GET['name']}
#     print(storage)
#     print(request.GET)
#     # capacity = request.GET['capacity']
#     # number_of_conveyor = request.GET['number_of_conveyor']
#     # capacity_calc = request.GET['capacity_calc']
#     # element = Conveyor(name=name, capacity=capacity, number_of_conveyor=number_of_conveyor)
#     # element.save()
#     return render(request, './save.html', storage)
