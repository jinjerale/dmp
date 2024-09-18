from data_server.models import Patient

def getPatients():
    objs = Patient.objects.all()
    return objs