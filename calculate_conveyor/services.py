import json as js
import math


def fun_rate_calculate(variable, matrix, row_result):
    while True:
        x = 0
        while variable > matrix[0][x]:
            x += 1
        x = matrix[row_result][x]
        break
    return x


def fun_closest_value(value, iterable) -> float:
    random_list = []
    for i in iterable:
        random_list.append((abs(value - i), i))
    result = min(random_list)
    return result[1]


def get_data_from_request(request):
    """Конвертирует тело запроса в словарь, а также добавлняет значения при необходимости."""
    try:
        data = dict()
        for key, item in request.POST.items():
            data[key] = item

        if 'csrfmiddlewaretoken' in data.keys():
            data.pop('csrfmiddlewaretoken')
        if 'name_conveyor' in data.keys():
            data.pop('name_conveyor')

        if 'ascent_or_descent' in request.POST:
            data['ascent_or_descent'] = True
        else:
            data['ascent_or_descent'] = False
        if 'point_speed' in request.POST:
            data['point_speed'] = True
        else:
            data['point_speed'] = False
        if 'point_precipitation' in request.POST:
            data['point_precipitation'] = True
        else:
            data['point_precipitation'] = False
        if 'point_conditions' in request.POST:
            data['point_conditions'] = True
        else:
            data['point_conditions'] = False
        if 'lining' in request.POST:
            data['lining'] = True
        else:
            data['lining'] = False

        return data

    except:
        return None


material_choices = [('1', 'Щебень'), ('2', 'Глина')]


class BeltConveyor:
    """Расчёт конвейера после ввода данных"""
    material_choices = [('1', 'Щебень'), ('2', 'Глина')]

    def __init__(self, capacity, number_of_conveyor, material, material_size,
                 ascent_or_descent, length_conveyor, height_conveyor, drop_height, point_speed,
                 point_precipitation, point_conditions, lining, drum_girth_angle, KPD):
        """Инициализация атрибутов"""
        self.capacity = float(capacity)
        self.number_of_conveyor = int(number_of_conveyor)
        self.material = material
        self.material_size = float(material_size)
        self.ascent_or_descent = bool(ascent_or_descent)
        self.length_conveyor = float(length_conveyor)
        self.height_conveyor = float(height_conveyor)
        self.drop_height = float(drop_height)
        self.point_speed = bool(point_speed)
        self.point_precipitation = bool(point_precipitation)
        self.point_conditions = bool(point_conditions)
        self.lining = bool(lining)
        self.drum_girth_angle = int(drum_girth_angle)
        self.KPD = float(KPD)

    def calculate(self) -> dict:
        """Выполняет расчёт конвейера по полученным данным"""
        # Раздел 2 пособия. Определения основных параметров конвейеров.
        with open('cof.json', 'r') as cf:
            cof = js.load(cf)

        capacity_calc = math.ceil(
            self.capacity * cof['k_n'] / (cof['k_v'] * (cof['k_g'] ** self.number_of_conveyor))
        )

        # Выбор скорости и ширины ленты.
        density = float(cof['material'][self.material]['density'])
        angle_phi = int(cof['material'][self.material]['angle_phi'])
        angle_conveyor_max = int(cof['material'][self.material]['angle_conveyor_max'])
        abrasiveness = int(cof['material'][self.material]['abrasiveness'])

        if self.ascent_or_descent:
            angle_conveyor_max -= 8
            ascent_or_descent = 1
            angle_phi -= 8
        else:
            ascent_or_descent = 0

        angle_conveyor = round(float(180 / math.pi * self.height_conveyor / self.length_conveyor), 1)
        """Необходимо добавить исключение, когда угол конвейера больше максимального угла конвейера"""

        belt_width_calc = self.material_size * cof['k_b'] + 200

        speed_max = 1.6  # constant
        speed_calc = 100  # constant
        index_belt_width = 0  # constant
        while speed_calc > speed_max:
            while belt_width_calc > cof['belt_width_list'][index_belt_width]:
                index_belt_width += 1
            belt_width = cof['belt_width_list'][index_belt_width]

            if ascent_or_descent == 0:
                x = 0
                while belt_width != cof['belt_width_list'][x]:
                    x += 1
                index_width_belt_1 = x
                x = 0
                while self.material_size >= cof['material_size_list'][x]:
                    x += 1
                index_width_belt_2 = x
                speed_max = cof['rate_speed_max'][index_width_belt_2][index_width_belt_1]

            if angle_phi in range(0, 31):
                area_cof1 = 1
            elif angle_phi in range(31, 36):
                area_cof1 = 2
            elif angle_phi in range(36, 41):
                area_cof1 = 3
            else:
                area_cof1 = 4
            if int(angle_conveyor) in range(0, 11):
                area_cof2 = 1
            elif int(angle_conveyor) in range(11, 16):
                area_cof2 = 2
            elif int(angle_conveyor) in range(16, 19):
                area_cof2 = 3
            else:
                area_cof2 = 4
            area_cof = cof['area_cof'][area_cof1 * area_cof2 - 1]
            speed_calc = round(capacity_calc / (belt_width ** 2 * area_cof * density) * 1000 * 1000, 2)
            index_belt_width += 1

        x = 0
        while speed_calc > cof['speed_list'][x]:
            x += 1
        speed = cof['speed_list'][x]

        capacity = round((belt_width / 1000) ** 2 * area_cof * speed * density, 2)

        # Раздел 3 пособия. Тяговый расчёт. Приближённый метод.
        if self.material_size <= 80:
            point_material_size = 0
        elif self.material_size <= 150:
            point_material_size = 8
        elif self.material_size <= 350:
            point_material_size = 18
        else:
            point_material_size = 25
        point_abrasiveness = cof['abrasiveness'][abrasiveness - 1]
        point_density = point_material_size * fun_rate_calculate(density, cof['density'], 1)
        """Необходимо добавить исключение, когда point_w > 100 ленточный конвейер использовать не допускается"""
        point_drop_height = fun_rate_calculate(self.drop_height, cof['drop_height'], 1)
        if self.point_speed == True:
            point_speed = 0
        else:
            point_speed = 0.4
        point_speed = point_speed * point_abrasiveness
        if self.point_precipitation == True:
            point_precipitation = 10
        else:
            point_precipitation = 0
        if self.point_conditions == True:
            point_conditions = 20
        else:
            point_conditions = 0
        point_w = (
                point_material_size + point_abrasiveness + point_density + point_drop_height + point_speed
                + 10 + point_precipitation + point_conditions
        )
        if (self.length_conveyor ** 2 + self.height_conveyor ** 2) ** (1 / 2) <= 100000:
            w = fun_rate_calculate(point_w, cof['w'], 1)
        else:
            w = fun_rate_calculate(point_w, cof['w'], 2)

        k_d = 10.396 * (((self.length_conveyor ** 2 + self.height_conveyor ** 2) ** (1 / 2) / 1000) ** (-0.383))
        load_material = capacity * cof['g'] / (36 * speed)
        load_belt = cof['load'][str(belt_width)][0]
        load_idlers_up = cof['load'][str(belt_width)][1]
        load_idlers_down = cof['load'][str(belt_width)][2]

        if ascent_or_descent == 0:
            force_on_drum = (
                (k_d * self.length_conveyor * w * (
                        load_material + load_idlers_up + load_idlers_down + 2 * load_belt
                ) + load_material * self.height_conveyor) / 1000
            )
        else:
            force_on_drum = (
                math.fabs((k_d * self.length_conveyor * w * (
                        load_material + load_idlers_up + load_idlers_down + 2 * load_belt
                ) + load_material * self.height_conveyor)) / 1000
            )

        if self.lining == True:
            friction = fun_rate_calculate(point_w, cof["friction"], 1)
        else:
            friction = fun_rate_calculate(point_w, cof["friction"], 2)

        traction_factor1 = 0
        while friction != cof["friction_list"][traction_factor1]:
            traction_factor1 += 1
        if traction_factor1 == 6:
            traction_factor1 = 5
        traction_factor2 = 0
        while self.drum_girth_angle >= cof['drum_girth_angle'][traction_factor2]:
            traction_factor2 += 1
        traction_factor = cof["traction_factor"][traction_factor1][traction_factor2]

        load_incoming = force_on_drum * traction_factor
        load_escaping = load_incoming - force_on_drum

        # Определение мощности привода.
        motor_power = force_on_drum * speed / 100
        if motor_power > 50:
            k = 1.2
        else:
            k = 1.1
        motor_power_calc = motor_power * k / self.KPD

        # Раздел 4 пособия. Выбор основного оборудования.
        k_p = 0
        count_gasket = 7
        while count_gasket > 6:
            k_p += 100
            factor_safety = 9
            count_gasket = math.ceil(load_incoming * factor_safety / (belt_width * k_p * 0.1))
            if count_gasket > 5 and angle_conveyor >= 10:
                new_factor_safety = 10
                count_gasket = math.ceil(count_gasket * new_factor_safety / factor_safety)
            elif count_gasket > 5 and angle_conveyor < 10:
                new_factor_safety = 9
                count_gasket = math.ceil(count_gasket * new_factor_safety / factor_safety)
            elif count_gasket < 5 and angle_conveyor >= 10:
                new_factor_safety = 9
                count_gasket = math.ceil(count_gasket * new_factor_safety / factor_safety)
            # elif count_gasket < 5 and angle_conveyor < 10:
            else:
                new_factor_safety = 8
                count_gasket = math.ceil(count_gasket * new_factor_safety / factor_safety)
            if count_gasket < 3:
                count_gasket = 3

        x = 0
        while density >= cof['density_list'][x]:
            x += 1
        distance_idlers = cof['distance_idlers'][str(belt_width)][x]
        if self.material_size >= 350:
            distance_idlers = round(distance_idlers * 0.9, 2)

        x = 2.5  # constant
        distance_idlers_down = x * distance_idlers
        while distance_idlers_down > 3.5:
            x -= 0.05
            distance_idlers_down = x * distance_idlers
        while load_escaping < (8 * load_belt * distance_idlers_down * math.cos(math.radians(angle_conveyor))):
            x -= 0.05
            distance_idlers_down = x * distance_idlers

        if belt_width in (400, 500, 650) and density < 1.6 and speed < 2:
            d_rollers = 89
        elif belt_width in (400, 500, 650) and density < 2 and speed < 2.5:
            d_rollers = 108
        elif belt_width == 800 and density < 1.6 and speed < 1.6:
            d_rollers = 89
        elif belt_width in (800, 1000, 1200) and density < 1.6 and speed < 2.5:
            d_rollers = 108
        elif belt_width in (800, 1000, 1200) and density < 2 and speed < 2.5:
            d_rollers = 127
        elif belt_width in (800, 1000, 1200) and density < 3.15 and speed < 4:
            d_rollers = 159
        elif belt_width in (1400, 1600, 2000) and density < 3.15 and speed < 3.1:
            d_rollers = 194
        elif belt_width == 1400 and density < 3.15 and speed < 4:
            d_rollers = 194
        elif belt_width in (1600, 2000) and density < 3.15 and speed < 6.3:
            d_rollers = 194

        # Определение диаметра барабанов и валов.
        if angle_conveyor <= 10:
            breaking_force = k_p * belt_width * 0.1 * count_gasket / new_factor_safety
        else:
            breaking_force = k_p * belt_width * 0.1 * count_gasket / new_factor_safety

        k_s = round(load_incoming / breaking_force)
        x = 0
        while k_s * 100 > cof['k_drum'][0][x]:
            x += 1
        k_drum_drive = cof['k_drum'][1][x]  # table 24
        k_drum_driven = cof['k_drum'][2][x]  # table 24
        k_drum_revolving = cof['k_drum'][3][x]  # table 24
        k_drum_deflecting = cof['k_drum'][4][x]  # table 24

        drive_drum_diameter = fun_closest_value(
            cof['k_z'][str(k_p)] * k_drum_drive * count_gasket, cof['drum_diameter'])
        driven_drum = fun_closest_value(
            cof['k_z'][str(k_p)] * k_drum_driven * count_gasket, cof['drum_diameter'])
        revolving_drum = fun_closest_value(
            cof['k_z'][str(k_p)] * k_drum_revolving * count_gasket, cof['drum_diameter'])
        deflecting_drum = fun_closest_value(
            cof['k_z'][str(k_p)] * k_drum_deflecting * count_gasket, cof['drum_diameter'])

        rate_ph = cof['rate_ph'][traction_factor1][traction_factor2]
        pressure_drum = 0.3  # constant
        while pressure_drum > 0.2:
            pressure_drum = (
                3600 * load_incoming * (rate_ph + 1) / (
                    self.drum_girth_angle * math.pi * belt_width * drive_drum_diameter * rate_ph
                )
            )
            if pressure_drum > 0.2:
                x = cof['drum_diameter'].index(drive_drum_diameter)
                drive_drum_diameter = cof['drum_diameter'][x + 1]
        torque = round(0.5 * force_on_drum * drive_drum_diameter, 2)
        length_drive_drum = cof['length_drum_dictionary'][str(belt_width)]
        width_frame = cof['width_conveyor'][str(belt_width)]
        shaft_drive_drum = (
            ((((load_incoming + load_escaping) * 10) / 2) * (
                (width_frame - length_drive_drum) * 0.001) / (65 * 1000000)) ** (1 / 3) * 1000
        )
        shafts = []
        for i in cof['shafts']:
            shafts.append(i)
        random_list = []
        for i in cof['shafts'].keys():
            random_list.append((abs(shaft_drive_drum - int(i)), int(i)))
        result = min(random_list)
        if result[1] < shaft_drive_drum:
            index_result = shafts.index(result[1])
            index_result += 1
            shaft_drive_drum = shafts[index_result]
        else:
            shaft_drive_drum = result[1]
        rotation_speed_drive_drum = round(60 / (math.pi * drive_drum_diameter / 1000 / speed))

        # Определение тормозного момента и необходимости установки тормоза.
        k_i = 0.55  # constant
        braking_torque = (
            0.5 * (load_material * self.height_conveyor) - k_i * (
                force_on_drum - load_material * self.height_conveyor
            ) * drive_drum_diameter * self.KPD
        )
        if load_material * self.height_conveyor <= force_on_drum:
            brake = 'Необходима установка тормоза'
        else:
            brake = 'Необходимости установки тормоза нет'

        # Определение параметров натяжного устройства.
        k_c = 0.3
        tension_length_inst = k_c * belt_width
        if angle_conveyor <= 10:
            k_y = 0.85
        else:
            k_y = 0.65
        e_o = 0.015
        tension_length_work = k_y * k_s * e_o * self.length_conveyor
        tension_length = round(tension_length_inst + tension_length_work)

        # Вывод данных.
        data = dict()
        data['capacity_calc'] = capacity
        data['speed'] = speed
        data['speed_max'] = speed_max
        data["angle_conveyor"] = angle_conveyor
        data['angle_conveyor_max'] = angle_conveyor_max
        data['angle_phi'] = angle_phi
        data['width_frame'] = width_frame
        data['belt_width'] = belt_width
        data["count_gasket"] = count_gasket
        data["k_p"] = k_p
        data["distance_idlers"] = distance_idlers
        data['distance_idlers_down'] = round(distance_idlers_down, 2)
        data['d_rollers'] = d_rollers
        data['drive_drum_diameter'] = drive_drum_diameter
        data['driven_drum'] = driven_drum
        data['revolving_drum'] = revolving_drum
        data['deflecting_drum'] = deflecting_drum
        data['shaft_drive_drum'] = shaft_drive_drum
        data['motor_power_calc'] = math.ceil(motor_power_calc)
        data['brake'] = brake
        data['tension_length'] = tension_length
        data['torque'] = torque
        data['rotation_speed_drive_drum'] = rotation_speed_drive_drum
        return data
