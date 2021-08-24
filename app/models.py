from django.db import models
from django.contrib.auth.models import User


class VaccineType(models.Model):
    name = models.CharField(max_length=50)
    months_interval = models.IntegerField(default=3)

    def __str__(self):
        return self.name


class Dog(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    birth_date = models.DateField()
    owners = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Vaccine(models.Model):
    type = models.ForeignKey(VaccineType, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    time = models.DateTimeField()
    vet_name = models.CharField(max_length=50, blank=True, null=True)
    schedule_next = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=(("Todo", "Todo"), ("Done", "Done")), default="Todo")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type.name}-{self.time.strftime('%B')}"