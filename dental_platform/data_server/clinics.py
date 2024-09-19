from data_server.models import Clinic

def getClinics():
    objs = Clinic.objects.all()
    for clinic in objs:
        clinic.doctor_count = clinic.affliated_doctors.count()
        clinic.patient_count = clinic.patient_set.count()
    return objs