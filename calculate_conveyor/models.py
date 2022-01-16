from django.db import models


# Create your models here.
class Conveyor(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    name = models.TextField(max_length=10, db_index=True, verbose_name='Название конвейера (код)')
    capacity = models.FloatField(verbose_name='Производительность в т/ч')
    number_of_conveyor = models.IntegerField(verbose_name='Количество конвейеров в шт')
    capacity_calc = models.FloatField(verbose_name='Расчётная производительность в т/ч')
    material = models.CharField(max_length=10)
    material_size = models.FloatField(verbose_name='Размер кусков материала в мм')
    ascent_or_descent = models.BooleanField(verbose_name='Конвейер работает на спуск')
    length_conveyor = models.FloatField(verbose_name='Длина горизонтальной проекции конвейера в мм')
    height_conveyor = models.FloatField(verbose_name='Высота вертикальной проекции конвейера в мм')
    drop_height = models.FloatField(verbose_name='Высота падения груза на ленту в мм')
    point_speed = models.BooleanField(verbose_name=
                                      'Скорость  и направление движения груза и ленты в месте загрузки совпадают')
    point_precipitation = models.BooleanField(verbose_name=
                                              'Воздействие атмосферных осадков или грузов с высокой влажностью')
    point_conditions = models.BooleanField(verbose_name='Условия технического обслуживания затруднительные')
    lining = models.BooleanField(verbose_name='Наличие футеровки на приводном барабане')
    drum_girth_angle = models.IntegerField(verbose_name='Угол обхвата барабана лентой')
    KPD = models.FloatField(verbose_name='КПД двигателя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '"Конвейер"'
        verbose_name_plural = 'Конвейеры'


class ResultCalculate(models.Model):
    name = models.ForeignKey(Conveyor, on_delete=models.PROTECT, unique=True)
    capacity = models.FloatField(verbose_name='Полученная производительность, т/ч')
    speed = models.FloatField(verbose_name='Скорость конвейера, м/с')
    speed_max = models.FloatField(verbose_name='Максимальная скорость конвейера, м/с')
    angle_conveyor = models.FloatField(verbose_name='Угол конвейера в градусах')
    angle_conveyor_max = models.FloatField(verbose_name='Допустимый угол ковнейера в градусах')
    angle_phi = models.FloatField(verbose_name='Угол естественного откоса материала в градусах')
    width_frame = models.IntegerField(verbose_name='Ширина рамы в мм')
    belt_width = models.IntegerField(verbose_name='Ширина ленты в мм')
    count_gasket = models.IntegerField(verbose_name='Количество тяговых прокладок, шт')
    k_p = models.IntegerField(verbose_name='Прочность тяговых прокладок')
    distance_idlers = models.FloatField(verbose_name='Расстояние между верхними роликоопорами в м')
    distance_idlers_down = models.FloatField(verbose_name='Расстояние между нижними роликоопорами в м')
    diameter_rollers = models.IntegerField(verbose_name='Диаметр роликов в мм')
    drive_drum_diameter = models.IntegerField(verbose_name='Диаметр приводного барабана в мм')
    driven_drum = models.IntegerField(verbose_name='Диаметр натяжного/ведомого барабана в мм')
    revolving_drum = models.IntegerField(verbose_name='Диаметр обводящего барабана в мм')
    deflecting_drum = models.IntegerField(verbose_name='Диаметр отклоняющего барабана в мм')
    shaft_drive_drum = models.IntegerField(verbose_name='Диаметр вала приводного барабана в мм')
    motor_power_calc = models.IntegerField(verbose_name='Мощность мотор-редуктора в кВт')
    brake = models.IntegerField(verbose_name='Крутящий момент на выходном валу мотор-редуктора в Нм')
    tension_length = models.IntegerField(verbose_name='Частота вращения выходного вала редуктора в об/мин')
    torque = models.CharField(max_length=50, verbose_name='Тормоз')
    rotation_speed_drive_drum = models.IntegerField(verbose_name='Ход натяжного устройства в мм')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
