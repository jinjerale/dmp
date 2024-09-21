from data_server.models import Clinic, ClinicForm, ClinicDoctor, WorkingSchedule, ClinicDoctorForm, WorkingScheduleFormSet, Doctor
from django.db import transaction

def getClinics():
    objs = Clinic.objects.all()
    for clinic in objs:
        clinic.doctor_count = clinic.affliated_doctors.count()
        clinic.patient_count = clinic.patient_set.count()
    return objs

def getClinicDetail(clinic_id):
    obj = Clinic.objects.get(id=clinic_id)
    if obj is None:
        return None, None, None

    formobj = ClinicForm(instance=obj)

    # get affliated doctors
    doctors = obj.affliated_doctors.all()
    # get schedule for office address and working schedule
    for doctor in doctors:
        affliation = ClinicDoctor.objects.get(clinic=obj, doctor=doctor)
        office_address = affliation.office
        # get schedule given doctor and affliaion
        working_schedule = WorkingSchedule.objects.filter(affliation=affliation)
        doctor.office_address = office_address
        doctor.working_schedule = working_schedule

    return formobj, doctors

def updateClinicDetail(clinic_id, data):
    obj = Clinic.objects.get(id=clinic_id)
    if obj is None:
        return False

    formobj = ClinicForm(data, instance=obj)
    if formobj.is_valid():
        print('valid')
        formobj.save()
        return True
    print('invalid')
    print(formobj.errors)
    return False

def addClinic(data):
    formobj = ClinicForm(data)
    if formobj.is_valid():
        formobj.save()
        return True, "Clinic added successfully"
    print(formobj.errors)
    return False, formobj.errors.as_text()

def getClinicInfo(clinic_id):
    try:
        obj = Clinic.objects.get(id=clinic_id)
    except Clinic.DoesNotExist:
        return None
    return obj

@transaction.atomic
def addAffliation(clinic_id, data):
    clinic = Clinic.objects.get(id=clinic_id)
    doctor = Doctor.objects.get(id=data['doctor'])
    clinic_doctor_form = ClinicDoctorForm(data)
    working_schedule_formset = WorkingScheduleFormSet(data)

    if clinic_doctor_form.is_valid() and working_schedule_formset.is_valid():
        try:
            with transaction.atomic():
                clinic_doctor = clinic_doctor_form.save(commit=False)
                clinic_doctor.clinic = clinic
                clinic_doctor.doctor = doctor
                clinic_doctor.save()
                for schedule in working_schedule_formset:
                    form = schedule.save(commit=False)
                    form.affliation = clinic_doctor
                    form.save()

            return True, f"{len(working_schedule_formset)} affliations added successfully"
        except Exception as e:
            return False, str(e)

    # DEBUG
    print(clinic_doctor_form.errors)
    print(working_schedule_formset.errors)

    err = clinic_doctor_form.errors.as_text()
    for e in working_schedule_formset.errors:
        err += e.as_text()

    return False, err