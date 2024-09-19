from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from data_server.clinics import *
from data_server.doctors import *
from data_server.patients import *
from django.shortcuts import redirect

@api_view(['GET'])
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
def clinics(request):
    template = loader.get_template('clinics.html')
    clinics = getClinics()
    context = {
        'clinics': clinics
    }
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
def doctors(request):
    template = loader.get_template('doctors.html')
    context = {
        'doctors': getDoctors()
    }
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
def patients(request):
    template = loader.get_template('patients.html')
    context = {
        'patients': getPatients()
    }
    return HttpResponse(template.render(context, request))

# get clinic details
@api_view(['GET', 'POST'])
def clinic(request, clinic_id):
    if request.method == 'POST':
        # create new clinic
        pass
    # get
    template = loader.get_template('clinic_detail.html')
    clinic, affliated_doctors = getClinicDetail(clinic_id)
    # show not found page if clinic is not found
    if clinic is None:
        template = loader.get_template('not_found.html')
        context = {}
    context = {
        'clinic': clinic,
        'doctors': affliated_doctors
    }
    return HttpResponse(template.render(context, request))

@api_view(['GET', 'POST'])
def doctor(request, doctor_id):
    if request.method == 'POST':
        # create new doctor
        pass
    # get
    template = loader.get_template('doctor_detail.html')
    doctor, affliated_clinics, affliated_patients = getDoctorDetail(doctor_id)
    # show not found page if doctor is not found
    if doctor is None:
        template = loader.get_template('not_found.html')
        context = {}

    context = {
        'doctor': doctor,
        'clinics': affliated_clinics,
        'patients': affliated_patients,
    }
    return HttpResponse(template.render(context, request))

@api_view(['GET', 'POST'])
def patient(request, patient_id):
    if request.method == 'POST':
        # create new patient
        pass
    # get
    template = loader.get_template('patient_detail.html')
    patient, visits, appointment = getPatientDetail(patient_id)
    # show not found page if patient is not found
    if patient is None:
        template = loader.get_template('not_found.html')
        context = {}
    context = {
        'patient': patient,
        'visits': visits,
        'next_appointment': appointment
    }
    return HttpResponse(template.render(context, request))

@api_view(['POST'])
def edit_doctor(request, doctor_id):
    if request.method == 'POST':
        updateDotorDetail(doctor_id, request.POST)
    return redirect('doctor', doctor_id=doctor_id)

@api_view(['POST'])
def edit_clinic(request, clinic_id):
    if request.method == 'POST':
        updateClinicDetail(clinic_id, request.POST)
    return redirect('clinic', clinic_id=clinic_id)

@api_view(['POST'])
def edit_patient(request, patient_id):
    if request.method == 'POST':
        updatePatientDetail(patient_id, request.POST)
    return redirect('patient', patient_id=patient_id)