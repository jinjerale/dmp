from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from data_server.clinics import *
from data_server.doctors import *
from data_server.patients import *

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
@api_view(['GET', 'POST', 'PUT'])
def clinic(request, clinic_id):
    if request.method == 'POST':
        # create new clinic
        pass
    elif request.method == 'PUT':
        # update clinic
        pass
    # get
    template = loader.get_template('clinic_detail.html')
    context = {
        'clinic': {
            'id' : clinic_id,
        } #TODO
    }
    return HttpResponse(template.render(context, request))

@api_view(['GET', 'POST', 'PUT'])
def doctor(request, doctor_id):
    if request.method == 'POST':
        # create new doctor
        pass
    elif request.method == 'PUT':
        # update doctor
        pass
    # get
    template = loader.get_template('doctor_detail.html')
    context = {
        'doctor': {
            'id' : doctor_id,
        } #TODO
    }
    return HttpResponse(template.render(context, request))

@api_view(['GET', 'POST', 'PUT'])
def patient(request, patient_id):
    if request.method == 'POST':
        # create new patient
        pass
    elif request.method == 'PUT':
        # update patient
        pass
    # get
    template = loader.get_template('patient_detail.html')
    context = {
        'patient': {
            'id' : patient_id,
        } #TODO
    }
    return HttpResponse(template.render(context, request))