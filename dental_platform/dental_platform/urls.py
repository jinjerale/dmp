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
from django.urls import path
from data_server import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('clinics/', views.clinics, name='clinics'),
    path('doctors/', views.doctors, name='doctors'),
    path('patients/', views.patients, name='patients'),
    path('clinics/<int:clinic_id>/', views.clinic, name='clinic'),
    path('doctors/<int:doctor_id>/', views.doctor, name='doctor'),
    path('patients/<int:patient_id>/', views.patient, name='patient'),
    path('clinics/<int:clinic_id>/edit/', views.edit_clinic, name='edit_clinic'),
    path('doctors/<int:doctor_id>/edit/', views.edit_doctor, name='edit_doctor'),
    path('patients/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('clinics/<int:clinic_id>/info/', views.get_clinic_info, name='get_clinic_info'),
]
