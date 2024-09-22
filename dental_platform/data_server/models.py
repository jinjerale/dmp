from django.db import models
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

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

class Day(models.IntegerChoices):
    MON = 0, 'Monday'
    TUE = 1, 'Tuesday'
    WED = 2, 'Wednesday'
    THU = 3, 'Thursday'
    FRI = 4, 'Friday'
    SAT = 5, 'Saturday'
    SUN = 6, 'Sunday'

    def __str__(self) -> str:
        return self.name

### Entities ##

class Doctor(models.Model):
    npi = models.CharField(max_length=10) # National Provider Identifier
    name = models.CharField(max_length=MAX_LENGTH)
    email = models.EmailField()
    phone = models.CharField(max_length=MAX_LENGTH)
    # specialties is a list of enums
    specialties = ArrayField(models.CharField(max_length=2, choices=ProcedureType.choices))

    # schedule

    def clean(self):
        # each entry in specialties must be unique
        if len(self.specialties) != len(set(self.specialties)):
            raise ValidationError('Specialties must be unique')

    def __str__(self) -> str:
        return self.name

class Clinic(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    phone = models.CharField(max_length=MAX_LENGTH)
    email = models.EmailField()
    city = models.CharField(max_length=MAX_LENGTH)
    state = models.CharField(max_length=MAX_LENGTH)
    address = models.CharField(max_length=MAX_LENGTH)
    affliated_doctors = models.ManyToManyField(Doctor, through='ClinicDoctor', blank=True)

    def __str__(self) -> str:
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    phone = models.CharField(max_length=MAX_LENGTH)
    address = models.CharField(max_length=MAX_LENGTH)
    birth_date = models.DateField()
    ssn = models.CharField(max_length=9)
    gender = models.CharField(max_length=1, choices=Gender.choices)

    affliated_clinics = models.ManyToManyField(Clinic, blank=True)
    afflicated_doctors = models.ManyToManyField(Doctor, blank=True)

    def __str__(self) -> str:
        return self.name


### Relationships ###

# affliation
class ClinicDoctor(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    office = models.CharField(max_length=MAX_LENGTH)
    # schedule
    def __str__(self) -> str:
        return f"{self.clinic.name} - {self.doctor.name}"
    # make clinic and doctor unique together
    class Meta:
        unique_together = ['clinic', 'doctor']

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    procedures = ArrayField(models.CharField(max_length=2, choices=ProcedureType.choices))
    note = models.TextField()
    # status

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    date_booked = models.DateField(auto_now_add=True)
    procedure = models.CharField(max_length=2, choices=ProcedureType.choices)

    def clean(self) -> None:
        # start_time must be before end_time
        if self.start_time >= self.end_time:
            raise ValidationError('Start time must be before end time')

## Form object

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'phone', 'address', 'email', 'city', 'state']

class DoctorDetail(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['id', 'npi', 'name', 'email', 'phone', 'specialties']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'phone', 'address', 'birth_date', 'ssn', 'gender']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['clinic', 'doctor', 'date', 'start_time', 'end_time', 'procedures', 'note']
        # display doctor name and clinic name instead of object id
        widgets = {
            'clinic': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class WorkingSchedule(models.Model):
    affliation = models.ForeignKey(ClinicDoctor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=Day.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self) -> str:
        return f'{self.get_day_display()}: {self.start_time} - {self.end_time}'

    def __repr__(self) -> str:
        return self.__str__()

    def clean(self) -> None:
        # start_time must be before end_time
        if self.start_time >= self.end_time:
            raise ValidationError('Start time must be before end time')

        # check that the shedule won't overlap with other schedules
        # for schedule in WorkingSchedule.objects.filter(day=self.day):
        #     if schedule.affliation.doctor == self.affliation.doctor:
        #         if schedule.start_time < self.end_time and self.start_time < schedule.end_time:
        #             raise ValidationError('Schedule overlaps with existing schedule')


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self) -> str:
        return f'{self.day.lookup_name}: {self.start_time} - {self.end_time}'

    def __repr__(self) -> str:
        return self.__str__()

    def clean(self) -> None:
        # start_time must be before end_time
        if self.start_time >= self.end_time:
            raise ValidationError('Start time must be before end time')

        for schedule in WorkingSchedule.objects.filter(doctor=self.doctor, date=self.date):
            if schedule.start_time < self.end_time and self.start_time < schedule.end_time:
                raise ValidationError('Schedule overlaps with existing schedule')

# clinic is already specified in the affliation
class ClinicDoctorForm(forms.ModelForm):
    class Meta:
        model = ClinicDoctor
        fields = ['doctor', 'office']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'office': forms.TextInput(attrs={'class': 'form-control'})
        }

class WorkingScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkingSchedule
        # affliation is specified in the parent form
        fields = ['day', 'start_time', 'end_time']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

WorkingScheduleFormSet = inlineformset_factory(
    ClinicDoctor, # parent model
    WorkingSchedule, # model to use
    form=WorkingScheduleForm, # form to use
    extra=1, # number of forms to display
    can_delete=True # allow deletion of forms
)

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        # patient is already specified
        fields = ['procedure', 'clinic', 'doctor', 'date', 'start_time', 'end_time']
        widgets = {
            'procedure': forms.Select(attrs={'class': 'form-control'}),
            'clinic': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clinic'].queryset = Clinic.objects.none() # only after you choose a procedure
        self.fields['doctor'].queryset = Doctor.objects.none() # only after you choose a clinic