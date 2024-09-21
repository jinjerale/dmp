from django.contrib import admin
from data_server.models import *
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Clinic)
admin.site.register(Patient)
admin.site.register(ClinicDoctor)
admin.site.register(Visit)
admin.site.register(Appointment)
admin.site.register(WorkingSchedule)
admin.site.register(DoctorSchedule)
