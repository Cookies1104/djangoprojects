from django import forms
from .services import material_choices


class ConveyorForm(forms.Form):
    name = forms.CharField(label='Название конвейера (КОД)', max_length=10, help_text=' например NMK2-BC1;')
    capacity = forms.FloatField(label='Производительность', min_value=0.1, help_text='т/ч;')
    number_of_conveyor = forms.IntegerField(label='Количество конвейеров в линии', min_value=1, help_text='шт.;')
    material = forms.ChoiceField(label='Материал', choices=material_choices)
    material_size = forms.FloatField(label='Размер кусков материала', min_value=0.01, help_text='мм;',
                                     max_value=900)
    ascent_or_descent = forms.BooleanField(label='Конвейер рабоатет на спуск', required=False)
    length_conveyor = forms.FloatField(label='Длина горизонтальной проекции конвейера', min_value=1,
                                       help_text=' мм;')
    height_conveyor = forms.FloatField(label='Высота вертикальной проекции конвейера', min_value=0,
                                       help_text=' мм;')
    drop_height = forms.FloatField(label='Высота падения груза на ленту', min_value=0,
                                   help_text=' мм;')
    point_speed = forms.BooleanField(label='Скорость и направление движения груза и ленты в месте загрузки близки',
                                     required=False)
    point_precipitation = forms.BooleanField(label='Воздействие атмосферных осадкой или грузов с высокой влажностью',
                                             required=False)
    point_conditions = forms.BooleanField(label='Условия технического обслуживания затруднительные',
                                          required=False)
    lining = forms.BooleanField(label='Наличие футеровки на приводном барабане', required=False, initial=True)
    drum_girth_angle = forms.IntegerField(label='Угол обхвата барабана лентой', min_value=180, max_value=240,
                                          help_text='180-240 градусов', initial=180)
    KPD = forms.FloatField(label='КПД двигателя', min_value=0.86, max_value=0.92, initial=0.86,
                           help_text='0.86-0.92 %')


class ResultForm(forms.Form):
    name = forms.CharField(max_length=10)
