from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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

# show form to add new appointment
@api_view(['GET'])
@login_required
def new_appointment(request, patient_id):
    template = loader.get_template('new_appointment.html')
    error_message = request.GET.get('message')
    context = {
        'patient_id': patient_id,
        'new_appointment': AppointmentForm(),
        'message': error_message
    }
    return HttpResponse(template.render(context, request))

# find clinics that provides the given procedure
# GET /api/clinics/?procedure=<procedure>
@api_view(['GET'])
@login_required
def load_clinics(request):
    procedure = request.GET.get('procedure')
    print(procedure, type(procedure))
    # only show clinics that have at least one doctor providing the procedure
    # find doctors where their specialites contain the procedure
    avaliable_doctors = Doctor.objects.filter(specialties__contains=[procedure])
    # find clinics where the doctor is affliated, only return unique clinics
    clinics = Clinic.objects.filter(clinicdoctor__doctor__in=avaliable_doctors).distinct()
    print(clinics)
    return HttpResponse(render(request, 'hr/clinic_dropdown.html', context={'clinics': clinics}))

# find doctors that provides the given procedure in the clinic
@api_view(['GET'])
@login_required
def load_doctors(request):
    clinic_id = request.GET.get('clinic_id')
    procedure = request.GET.get('procedure')
    print(clinic_id, procedure)
    # find doctors that are affliated with the clinic and provide the procedure
    doctors = Doctor.objects.filter(clinicdoctor__clinic_id=clinic_id, specialties__contains=[procedure])
    print(doctors)
    return HttpResponse(render(request, 'hr/doctor_dropdown.html', context={'doctors': doctors}))

@api_view(['POST'])
@login_required
def add_appointment(request, patient_id):
    success = False
    message = "not completed"
    if request.method == 'POST':
        success, message = addAppointment(patient_id, request.POST)
        if success:
            return redirect('patient', patient_id=patient_id)
    # put message as url get parameter
    url = reverse('new_appointment', args=[patient_id])
    if message:
        url = f'{url}?message={message}'
    return redirect(url)

