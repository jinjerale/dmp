from data_server.models import Clinic

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

    # get affliated doctors
    doctors = obj.affliated_doctors.all()

    return obj, doctors