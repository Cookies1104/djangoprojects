# Generated by Django 4.0 on 2022-01-16 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conveyor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('capacity', models.FloatField(verbose_name='Производительность в т/ч')),
                ('number_of_conveyor', models.IntegerField(verbose_name='Количество конвейеров в шт')),
                ('material', models.CharField(max_length=10)),
                ('material_size', models.FloatField(verbose_name='Размер кусков материала в мм')),
                ('ascent_or_descent', models.BooleanField(verbose_name='Конвейер работает на спуск')),
                ('length_conveyor', models.FloatField(verbose_name='Длина горизонтальной проекции конвейера в мм')),
                ('height_conveyor', models.FloatField(verbose_name='Высота вертикальной проекции конвейера в мм')),
                ('drop_height', models.FloatField(verbose_name='Высота падения груза на ленту в мм')),
                ('point_speed', models.BooleanField(verbose_name='Скорость  и направление движения груза и ленты в месте загрузки совпадают')),
                ('point_precipitation', models.BooleanField(verbose_name='Воздействие атмосферных осадков или грузов с высокой влажностью')),
                ('point_conditions', models.BooleanField(verbose_name='Условия технического обслуживания затруднительные')),
                ('lining', models.BooleanField(verbose_name='Наличие футеровки на приводном барабане')),
                ('drum_girth_angle', models.IntegerField(verbose_name='Угол обхвата барабана лентой')),
                ('KPD', models.FloatField(verbose_name='КПД двигателя')),
            ],
            options={
                'verbose_name': 'Конвейер',
                'verbose_name_plural': 'Конвейеры',
            },
        ),
    ]
