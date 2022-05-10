import math


def calculate_cross_section(
    belt_width: int,
    idlers_angle: int,
    material_slope_angle: int,
    density: float,
    required_capacity: float,
    speed: float
) -> dict:
    """Выполняет расчёт короба конвейера."""
    result = {}
    # Расчитываем горизонтальный участок ленты
    horizontal_section_belt = (0.371 * belt_width + 6.35) / belt_width
    inclined_section_belt = (1-horizontal_section_belt) / 2

    # Расчитываем потребное поперечное сечение материала и записываем в результаты
    calculate_required_capacity = required_cross_section(density, required_capacity, speed)
    result['calculate_required_capacity'] = calculate_required_capacity

    return result


def required_cross_section(density: float, required_capacity: float, speed: float) -> float:
    """Выполняет расчёт потребного сечения материала в м^2"""
    calculate_required_capacity = (required_capacity / (speed * density * 3600))
    return calculate_required_capacity


def fun_horizontal_section_belt(belt_width: int, idlers_angle: int, material_slope_angle: int) -> float:
    """Выполняет расчёт соотношений ленты конвейера к остальным параметрам. См. рис. 4.10 стр. 67 CEMA"""
    b_c = (0.371 * belt_width + 6.35) / belt_width
    b_we = (0.055 * belt_width + 22.9) / belt_width
    b_w = (1 - b_c) / 2
    r_sch = abs((b_c / 2) + (math.cos(idlers_angle) * b_w / math.sin(material_slope_angle))
    return horizontal_section_belt
