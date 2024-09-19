from data_server.models import Clinic, ClinicForm

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
        return True
    print(formobj.errors)
    return False