"""
URL configuration for dental_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from data_server import views
from rest_framework.authtoken.views import obtain_auth_token
from data_server.api_views import ClinicCreateView, DoctorCreateView, PatientCreateView, ClinicDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('clinics/', views.clinics, name='clinics'),
    path('doctors/', views.doctors, name='doctors'),
    path('patients/', views.patients, name='patients'),
    path('clinics/<int:clinic_id>/', views.clinic, name='clinic'),
    path('doctors/<int:doctor_id>/', views.doctor, name='doctor'),
    path('patients/<int:patient_id>/', views.patient, name='patient'),
    path('clinics/<int:clinic_id>/edit/', views.edit_clinic, name='edit_clinic'),
    path('doctors/<int:doctor_id>/edit/', views.edit_doctor, name='edit_doctor'),
    path('patients/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('patients/<int:patient_id>/visits/', views.patient_visit, name='patient_visit'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/clinics/', ClinicCreateView.as_view(), name='create_clinic'),
    path('api/doctors/', DoctorCreateView.as_view(), name='create_doctor'),
    path('api/patients/', PatientCreateView.as_view(), name='create_patient'),
    path('api/clinics/<int:clinic_id>/', ClinicDetailView.as_view(), name='clinic_detail'),
    path('clinics/<int:clinic_id>/affliations/', views.add_affliation, name='add_affliation'),
    path('patients/<int:patient_id>/add_appointment/', views.new_appointment, name='new_appointment'),
    path('ajax/clinics/', views.load_clinics, name='load_clinics'),
    path('ajax/doctors/', views.load_doctors, name='load_doctors'),
    path('ajax/patients/<int:patient_id>/appointments', views.add_appointment, name='add_appointment'),
]
