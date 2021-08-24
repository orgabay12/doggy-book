from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from app.models import Vaccine
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import Group, User

from app.utils import send_event


@receiver(post_save, sender=Vaccine)
def schedule_next_vaccine(sender, instance, created, **kwargs):
    if instance.status == "Done" and instance.schedule_next:
        interval = instance.type.months_interval
        next_vaccine_date = instance.date + relativedelta(months=interval)
        Vaccine.objects.get_or_create(type=instance.type, dog=instance.dog, date=next_vaccine_date,
                                      vet_name=instance.vet_name, schedule_next=True)
    if created:
        login_address = "doggybookapp@gmail.com"
        password = "Yeswecan2015"
        attendees = instance.dog.owners
        sender_name = "doggybook"
        subject = f"{instance.type} vaccine for {instance.dog}"
        start_datetime = instance.date
        send_event(login_address, password, attendees, sender_name, subject, start_datetime)


@receiver(pre_save, sender=User)
def set_stuff(sender, instance, created=False, **kwargs):
    if not instance.pk:
        instance.is_staff = True


@receiver(post_save, sender=User)
def set_stuff(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='Owners'))