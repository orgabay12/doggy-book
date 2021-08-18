from django.contrib import admin

from app.models import VaccineType, Dog, Vaccine


@admin.register(VaccineType)
class VaccineTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'months_interval')


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed')


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ('type', 'dog', 'date')