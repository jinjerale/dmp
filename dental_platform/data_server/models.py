from django.db import models
from django import forms
from django.contrib.postgres.fields import ArrayField

MAX_LENGTH = 100

### Enums ###

class ProcedureType(models.TextChoices):
    CLEANING = 'CL', 'Cleaning'
    CROWN = 'CR', 'Crown'
    FILLING = 'FI', 'Filling'
    ROOT_CANAL = 'RC', 'Root Canal'
    WHITENING = 'WH', 'Whitening'

class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMAILE = 'F', 'Female'

### Entities ##

class Doctor(models.Model):
    npi = models.CharField(max_length=10) # National Provider Identifier
    name = models.CharField(max_length=MAX_LENGTH)
    email = models.EmailField()
    phone = models.CharField(max_length=MAX_LENGTH)
    # specialties is a list of enums
    specialities = ArrayField(models.CharField(max_length=2, choices=ProcedureType.choices))

    # schedule

class Clinic(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    phone = models.CharField(max_length=MAX_LENGTH)
    city = models.CharField(max_length=MAX_LENGTH)
    state = models.CharField(max_length=MAX_LENGTH)
    address = models.CharField(max_length=MAX_LENGTH)
    affliated_doctors = models.ManyToManyField(Doctor, through='ClinicDoctor', blank=True)


class Patient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    phone = models.CharField(max_length=MAX_LENGTH)
    email = models.EmailField()
    address = models.CharField(max_length=MAX_LENGTH)
    birth_date = models.DateField()
    ssn = models.CharField(max_length=9)
    gender = models.CharField(max_length=1, choices=Gender.choices)

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

## Frontend Object
class DoctorDetail(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['id', 'npi', 'name', 'email', 'phone', 'specialities']
        # widgets = {
        #     'specialities': forms.CheckboxSelectMultiple(
        #         choices=ProcedureType.choices,
        #     )
        # }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'phone', 'email', 'address', 'birth_date', 'ssn', 'gender']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
