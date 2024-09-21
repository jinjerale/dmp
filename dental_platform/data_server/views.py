from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from data_server.clinics import *
from data_server.doctors import *
from data_server.patients import *
from data_server.serializers import *
from data_server.api_views import *
from .models import *

@login_required(redirect_field_name='login')
@api_view(['GET'])
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
@api_view(['GET', 'POST'])
def clinics(request):
    if request.method == 'POST':
        # create new clinic
        try:
            success, message = addClinic(request.data)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

        return JsonResponse({'success': success, 'message': message})

    # get
    template = loader.get_template('clinics.html')
    clinics = getClinics()
    context = {
        'clinics': clinics,
        'new_clinic': ClinicForm(),
    }
    return HttpResponse(template.render(context, request))

@login_required
@api_view(['GET', 'POST'])
def doctors(request):
    if request.method == 'POST':
        # create new doctor
        try:
            success, message = addDoctor(request.data)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        return JsonResponse({'success': success, 'message': message})
    # get
    template = loader.get_template('doctors.html')
    context = {
        'doctors': getDoctors(),
        'new_doctor': DoctorDetail(),
    }
    return HttpResponse(template.render(context, request))

@login_required
@api_view(['GET', 'POST'])
def patients(request):
    if request.method == 'POST':
        # create new patient
        try:
            success, message = addPatient(request.data)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        return JsonResponse({'success': success, 'message': message})
    # get
    template = loader.get_template('patients.html')
    context = {
        'patients': getPatients(),
        'new_patient': PatientForm(),
    }
    return HttpResponse(template.render(context, request))

# get clinic details
@login_required
@api_view(['GET'])
def clinic(request, clinic_id):
    template = loader.get_template('clinic_detail.html')
    clinic, affliated_doctors = getClinicDetail(clinic_id)
    # show not found page if clinic is not found
    if clinic is None:
        template = loader.get_template('not_found.html')
        context = {}
    context = {
        'clinic': clinic,
        'doctors': affliated_doctors,
        'clinic_doctor_form': ClinicDoctorForm(),
        'working_schedule_formset': WorkingScheduleFormSet()
    }
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
@login_required
def doctor(request, doctor_id):
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

@api_view(['GET'])
@login_required
def patient(request, patient_id):
    template = loader.get_template('patient_detail.html')
    patient, visits, appointment = getPatientDetail(patient_id)
    # show not found page if patient is not found
    if patient is None:
        template = loader.get_template('not_found.html')
        context = {}
    context = {
        'patient': patient,
        'visits': visits,
        'visit': VisitForm(),
        'next_appointment': appointment
    }
    return HttpResponse(template.render(context, request))

@api_view(['POST'])
@login_required
def edit_doctor(request, doctor_id):
    if request.method == 'POST':
        updateDotorDetail(doctor_id, request.POST)
    return redirect('doctor', doctor_id=doctor_id)

@api_view(['POST'])
@login_required
def edit_clinic(request, clinic_id):
    if request.method == 'POST':
        updateClinicDetail(clinic_id, request.POST)
    return redirect('clinic', clinic_id=clinic_id)

@api_view(['POST'])
@login_required
def edit_patient(request, patient_id):
    if request.method == 'POST':
        updatePatientDetail(patient_id, request.POST)
    return redirect('patient', patient_id=patient_id)

@api_view(['POST'])
@login_required
def patient_visit(request, patient_id):
    if request.method == 'POST':
        success = addVisit(patient_id, request.POST)
        if success:
            return redirect('patient', patient_id=patient_id)
    return redirect('patient', patient_id=patient_id)

@api_view(['POST'])
@login_required
def add_affliation(request, clinic_id):
    message = "unknow error"
    if request.method == 'POST':
        success, message = addAffliation(clinic_id, request.POST)
        if success:
            return redirect('clinic', clinic_id=clinic_id)
    return JsonResponse({'success': success, 'message': message}, status=400)