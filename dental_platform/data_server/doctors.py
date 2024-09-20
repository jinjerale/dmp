from data_server.models import Doctor, ProcedureType, DoctorDetail

def getDoctors():
    objs = Doctor.objects.all()

    for doctor in objs:
        doctor.specialties = [ProcedureType(s).label for s in doctor.specialties]
        doctor.clinic_count = doctor.clinic_set.count()
        doctor.patient_count = doctor.patient_set.count()
    return objs

def getDoctorDetail(doctor_id):
    obj = Doctor.objects.get(id=doctor_id)
    if obj is None:
        return None, None, None

    formobj = DoctorDetail(instance=obj)

    # get affliated clinics
    clinics = obj.clinic_set.all()

    # get affliated patients
    patients = obj.patient_set.all()

    return formobj, clinics, patients

def updateDotorDetail(doctor_id, data):
    obj = Doctor.objects.get(id=doctor_id)
    if obj is None:
        return False

    formobj = DoctorDetail(data, instance=obj)
    if formobj.is_valid():
        formobj.save()
        return True
    return False

def addDoctor(data):
    print(data)
    formobj = DoctorDetail(data)
    if formobj.is_valid():
        formobj.save()
        return True, "Doctor added successfully"
    return False, formobj.errors.as_text()