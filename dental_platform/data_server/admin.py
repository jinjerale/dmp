from django.contrib import admin
from data_server.models import Doctor, Clinic, Patient, ClinicDoctor, Visit, Appointment
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Clinic)
admin.site.register(Patient)
admin.site.register(ClinicDoctor)
admin.site.register(Visit)
admin.site.register(Appointment)
