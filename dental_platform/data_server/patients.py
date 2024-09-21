from data_server.models import Patient, Visit, Appointment, PatientForm, ProcedureType, VisitForm
from django.shortcuts import get_object_or_404
from django.db import transaction

def getPatients():
    objs = Patient.objects.all()
    for obj in objs:
        last_visit = Visit.objects.filter(patient=obj).order_by('-date').first()
        next_appointment = Appointment.objects.filter(patient=obj).order_by('date').first()
        if last_visit:
            obj.last_visit_date = last_visit.date
            obj.last_visit_doctor = last_visit.doctor.name
            obj.last_visit_procedures = [ProcedureType(s).label for s in last_visit.procedures]
        if next_appointment:
            obj.next_appointment_date = next_appointment.date
            obj.next_appointment_doctor = next_appointment.doctor.name
            obj.next_appointment_procedure = next_appointment.procedure

    return objs

def getPatientDetail(patient_id):
    obj = Patient.objects.get(id=patient_id)
    if obj is None:
        return None, None, None

    obj.ssn = obj.ssn[-4:]
    form = PatientForm(instance=obj)

    # get visits
    visits = Visit.objects.filter(patient=obj)

    # get next appointment
    next_appointment = Appointment.objects.filter(patient=obj).order_by('date').first()

    return form, visits, next_appointment

def updatePatientDetail(patient_id, data):
    obj = Patient.objects.get(id=patient_id)
    if obj is None:
        return False

    form = PatientForm(data, instance=obj)
    if form.is_valid():
        form.save()
        return True
    print(form.errors)
    return False

def addPatient(data):
    form = PatientForm(data)
    if form.is_valid():
        form.save()
        return True, "Patient added successfully"
    print(form.errors)
    return False, form.errors.as_text()

# create affliation
@transaction.atomic
def addVisit(patient_id, data):
    patient = get_object_or_404(Patient, id=patient_id)
    form = VisitForm(data)
    if form.is_valid():
        visit = form.save(commit=False)
        visit.patient = patient
        visit.save()
        # create affliation to clinic and doctor
        patient.affliated_clinics.add(visit.clinic)
        patient.afflicated_doctors.add(visit.doctor)
        patient.save()

        return True
    print(form.errors)
    return False