from django.db import models
from django.contrib.postgres.fields import ArrayField

MAX_LENGTH = 100

### Enums ###

class ProcedureType(models.TextChoices):
    CLEANING = 'CL', 'Cleaning'
    CROWN = 'CR', 'Crown'
    FILLING = 'FI', 'Filling'
    ROOT_CANAL = 'RC', 'Root Canal'
    WHITENING = 'WH', 'Whitening'

### Entities ##

class Doctor(models.Model):
    npi = models.CharField(max_length=10) # National Provider Identifier
    name = models.CharField(max_length=MAX_LENGTH)
    # specialities is a list of enums
    specialities = ArrayField(models.CharField(max_length=2, choices=ProcedureType.choices))

    # schedule

class Clinic(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    phone = models.CharField(max_length=MAX_LENGTH)
    city = models.CharField(max_length=MAX_LENGTH)
    state = models.CharField(max_length=MAX_LENGTH)
    affliated_doctors = models.ManyToManyField(Doctor, through='ClinicDoctor', blank=True)


class Patient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    phone = models.CharField(max_length=MAX_LENGTH)
    email = models.EmailField()
    address = models.CharField(max_length=MAX_LENGTH)
    birth_date = models.DateField()
    ssn = models.CharField(max_length=9)

    affliated_clinics = models.ManyToManyField(Clinic, blank=True)
    afflicated_doctors = models.ManyToManyField(Doctor, blank=True)
    # address

### Relationships ###

# affliation
class ClinicDoctor(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    office = models.CharField(max_length=MAX_LENGTH)
    # schedule

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    procedures = models.CharField(max_length=2, choices=ProcedureType.choices)
    note = models.TextField()
    # status

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    procedure = models.CharField(max_length=2, choices=ProcedureType.choices)
    # status