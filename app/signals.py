import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Vaccine
from dateutil.relativedelta import relativedelta


@receiver(post_save, sender=Vaccine)
def schedule_next_vaccine(sender, instance, created, **kwargs):
    if instance.status == "Done" and instance.schedule_next:
        interval = instance.type.months_interval
        next_vaccine_date = instance.date + relativedelta(months=interval)
        Vaccine.objects.get_or_create(type=instance.type, dog=instance.dog, date=next_vaccine_date,
                                      vet_name=instance.vet_name, schedule_next=True)
