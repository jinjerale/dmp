from data_server.models import Doctor, ProcedureType

def getDoctors():
    objs = Doctor.objects.all()

    for doctor in objs:
        doctor.specialities = [ProcedureType(s).label for s in doctor.specialities]
    return objs