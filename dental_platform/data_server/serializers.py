from rest_framework import serializers
from data_server.models import Clinic, Doctor, Patient

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        exclude = ['affliated_doctors']
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'npi', 'name', 'email', 'phone', 'specialties']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'phone', 'address', 'birth_date', 'ssn', 'gender']

