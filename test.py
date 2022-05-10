import json
import math


def get_capacity_calculate(capacity: float, number_of_conveyor: int) -> int:
    """Возвращает расчётную производительность"""
    capacity_calculate = math.ceil(
            capacity * cof['k_n'] / (cof['k_v'] * (cof['k_g'] ** number_of_conveyor))
        )
    return capacity_calculate


def get_material_params(material: int, ascent_or_descent: bool) -> dict:
    """Возвращает физические характеристики материала с учётом работы конвейера (1 - спуск или 2 - подъём)"""
    density = float(cof['material'][material]['density'])
    angle_phi = int(cof['material'][material]['angle_phi'])
    angle_conveyor_max = int(cof['material'][material]['angle_conveyor_max'])
    abrasiveness = int(cof['material'][material]['abrasiveness'])
    
    if ascent_or_descent:
        angle_conveyor_max -= 8
        ascent_or_descent = 1
        angle_phi -= 8
    else:
        ascent_or_descent = 0
    
    material_params = {'density': density, 
                       'angle_phi': angle_phi, 
                       'angle_conveyor_max': angle_conveyor_max,
                       'abrasiveness': abrasiveness,
                       'ascent_or_descent': ascent_or_descent,
                       }
    return material_params
    

def get_angle_conveyor(height_conveyor: float, length_conveyor: float, angle_conveyor_max: int):
    """Возвращает угол наклона, длина и высота конвейера в мм."""
    angle_conveyor = round(float(180 / math.pi * height_conveyor / length_conveyor), 1)
    if angle_conveyor <= angle_conveyor_max:
        return angle_conveyor
    else:
        return ValueError


def get_min_belt_width_for_material_size(material_size: int, index_belt_width: int):
    """Возвращает минимальную ширину ленты конвейера для материала выбранного диаметра и индекс ленты.
    Размер материала и ленты в мм."""
    if material_size > 900:
        return ValueError
    else:
        belt_width_calculate = material_size * cof['k_b'] + 200
        while belt_width_calculate > cof['belt_width_list'][index_belt_width]:
            index_belt_width += 1
        belt_width_calculate = cof['belt_width_list'][index_belt_width]
        return belt_width_calculate, index_belt_width


def get_max_speed_for_belt_width(belt_width: int, size_material: int) -> float:
    """Возвращает максимальную скорость конвейера для размера кусков материала и ширины ленты. Ширина ленты в мм.
    Размер материала в мм. Скорость в м/с"""
    x = 0
    while belt_width != cof['belt_width_list'][x]:
        x += 1
    index_width_belt_1 = x
    x = 0
    while size_material >= cof['material_size_list'][x]:
        x += 1
    index_width_belt_2 = x
    max_speed = cof['rate_speed_max'][index_width_belt_2][index_width_belt_1]
    return max_speed


def get_area_cof(params_material: dict, conveyor_angle: float) -> int:
    """Возвращает коэффициент в зависимости от угла наклона конвейера и угла естественного откоса материала"""
    if params_material['angle_phi'] in range(0, 31):
        area_cof1 = 1
    elif params_material['angle_phi'] in range(31, 36):
        area_cof1 = 2
    elif params_material['angle_phi'] in range(36, 41):
        area_cof1 = 3
    else:
        area_cof1 = 4
    if conveyor_angle in range(0, 11):
        area_cof2 = 1
    elif conveyor_angle in range(11, 16):
        area_cof2 = 2
    elif conveyor_angle in range(16, 19):
        area_cof2 = 3
    else:
        area_cof2 = 4
    area_cof = cof['area_cof'][area_cof1 * area_cof2 - 1]
    return area_cof

def get_speed_and_belt_width_conveyor(params_material: dict,
                        conveyor_angle: float,
                        calculate_capacity: float,
                        material_size: int) -> dict:
    """Возвращает необходимую для расчётной производительности скорость, ширину ленты конвейера. Скорость в м/с.
    Угол конвейера в градусах. Размер материала в мм. Ширина ленты в мм."""
    min_belt_width_for_material_size, index_belt_width = get_min_belt_width_for_material_size(material_size,
                                                                                              index_belt_width=0)
    if params_material['ascent_or_descent']:
        max_speed = 1.6
    else:
        max_speed = get_max_speed_for_belt_width(min_belt_width_for_material_size, material_size)
    area_cof = get_area_cof(params_material, conveyor_angle)
    while True:
        calculate_speed = round(
            calculate_capacity /
                (min_belt_width_for_material_size ** 2 * area_cof * params_material['density']) * 1000 * 1000, 2
        )
        if calculate_speed <= max_speed:
            break
        else:
            index_belt_width += 1
            min_belt_width_for_material_size, index_belt_width = get_min_belt_width_for_material_size(material_size,
                                                                                                      index_belt_width)
    belt_width = min_belt_width_for_material_size
    x = 0
    while calculate_speed > cof['speed_list'][x]:
        x += 1
    speed = cof['speed_list'][x]
    conveyor_params = {'speed': speed,
                       'belt_width': belt_width,
                       'min_belt_width_for_material_size': min_belt_width_for_material_size,
                       'max_speed': max_speed,
                       }
    return conveyor_params


def get_capacity(params_material: dict,
                 angle_conveyor: float,
                 calculate_capacity: float,
                 material_size: int,
                 ) -> dict:
    """Возвращает производительность конвейера"""
    area_cof = get_area_cof(params_material, angle_conveyor)
    conveyor_params = get_speed_and_belt_width_conveyor(
        params_material, angle_conveyor, calculate_capacity, material_size
    )
    capacity = round(
        (conveyor_params['belt_width'] / 1000) ** 2 * area_cof * conveyor_params['speed'] * params_material['density'], 2
    )
    conveyor_params['capacity'] = capacity
    return conveyor_params


with open('cof.json', 'r') as cf:
    cof = json.load(cf)
    

capacity = 100
number_of_conveyor = 2
material = 1
ascent_or_descent = True
height_conveyor = 10000
length_conveyor = 100000
material_size = 50 # max material size 900 mm

capacity_calculate = get_capacity_calculate(capacity, number_of_conveyor)
material_params = get_material_params(material, ascent_or_descent)

try:
    angle_conveyor = get_angle_conveyor(height_conveyor, length_conveyor, material_params['angle_conveyor_max'])
except ValueError:
    print('Угол конвейера превышает максимально допустимый для данного материала')

capacity = get_capacity(params_material=material_params,
                        angle_conveyor=angle_conveyor,
                        calculate_capacity=capacity_calculate,
                        material_size=material_size,
                        )





