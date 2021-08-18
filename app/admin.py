from django.contrib import admin

from app.models import VaccineType, Dog, Vaccine


@admin.register(VaccineType)
class VaccineTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'months_interval')


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed')
    readonly_fields = ('owners', )

    def get_queryset(self, request):
        qs = super(DogAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owners=request.user)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        new_object = obj.id == None
        obj.save()
        if new_object:
            obj.owners.add(request.user)
            obj.save()


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dog', 'date', 'status')

    def get_queryset(self, request):
        qs = super(VaccineAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(dog__owners=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "dog":
            kwargs["queryset"] = Dog.objects.filter(owners=request.user)
        return super(VaccineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)