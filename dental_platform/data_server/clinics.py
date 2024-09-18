from data_server.models import Clinic

def getClinics():
    objs = Clinic.objects.all()
    return objs