from rest_framework import serializers

from data_server.models import Clinic

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        exclude = ['affliated_doctors']
