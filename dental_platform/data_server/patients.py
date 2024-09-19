from data_server.models import Patient, Visit, Appointment, PatientForm

def getPatients():
    objs = Patient.objects.all()
    # TODO: visits, appointments
    return objs

def getPatientDetail(patient_id):
    obj = Patient.objects.get(id=patient_id)
    if obj is None:
        return None, None, None

    obj.ssn = obj.ssn[-4:]
    form = PatientForm(instance=obj)

    # get visits
    visits = Visit.objects.filter(patient=obj)

    # get appointments
    appointments = Appointment.objects.filter(patient=obj)

    return form, visits, appointments

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
        return True
    print(form.errors)
    return False