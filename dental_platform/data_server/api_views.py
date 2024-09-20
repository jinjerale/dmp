from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Clinic, Doctor, Patient
from .serializers import ClinicSerializer, DoctorSerializer, PatientSerializer

# POST api/clinics need to be authenticated
class ClinicCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ClinicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# POST api/doctors
class DoctorCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# POST api/patients
class PatientCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET api/clinics/:clinic_id
class ClinicDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clinic_id):
        try:
            clinic = Clinic.objects.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClinicSerializer(clinic)
        return Response(serializer.data)
