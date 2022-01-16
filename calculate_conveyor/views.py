from django.shortcuts import render, redirect
from .models import Conveyor, ResultCalculate
from .services import Calculate
from .forms import ConveyorForm


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

        element = Conveyor(
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
        print(request.POST)
        element = ResultCalculate(
            name=request.POST['name_conveyor'],
            capacity=request.POST['capacity_calc'],
            speed=request.POST['speed'],
            speed_max=request.POST['speed_max'],
            angle_conveyor=request.POST['angle_conveyor'],
            angle_conveyor_max=request.POST['angle_conveyor_max'],
            angle_phi=request.POST['angle_phi'],
            width_frame=request.POST['width_frame'],
            belt_width=request.POST['belt_width'],
            count_gasket=request.POST['count_gasket'],
            k_p=request.POST['k_p'],
            distance_idlers=request.POST['distance_idlers'],
            distance_idlers_down=request.POST['distance_idlers_down'],
            diameter_rollers=request.POST['diameter_rollers'],
            drive_drum_diameter=request.POST['drive_drum_diameter'],
            driven_drum=request.POST['driven_drum'],
            revolving_drum=request.POST['revolving_drum'],
            deflecting_drum=request.POST['deflecting_drum'],
            shaft_drive_drum=request.POST['shaft_drive_drum'],
            motor_power_calc=request.POST['motor_power_calc'],
            brake=request.POST['brake'],
            tension_length=request.POST['tension_length'],
            torque=request.POST['torque'],
            rotation_speed_drive_drum=request.POST['rotation_speed_drive_drum'],
        )
        element.save()
        return render(request, './save.html')
    else:
        return redirect('calculate', permanent=True)
