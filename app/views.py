from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app.models import Vaccine
from app.utils import send_event
from server import settings


@staff_member_required
def send_vaccine_invite(request, vaccine_id):
    vaccine = Vaccine.objects.get(id=vaccine_id)
    login_address = settings.EMAIL
    password = settings.EMAIL_PASSWORD
    attendees = [v.username for v in vaccine.dog.owners.all()]
    sender_name = "doggybook"
    subject = f"{vaccine.type} vaccine for {vaccine.dog}"
    start_datetime = vaccine.time
    send_event(login_address, password, attendees, sender_name, subject, start_datetime)
    return render(request, 'admin/app/vaccine/send_invite.html')