from django.db import models


# Create your models here.
class Conveyor(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    name = models.TextField(max_length=10, verbose_name='Название конвейера (код)')
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
