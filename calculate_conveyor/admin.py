from django.contrib import admin
from .models import Conveyor


# Register your models here.
# class CalculateAdmin(admin.ModelAdmin):
#     list_display = ()
admin.site.register(Conveyor)
