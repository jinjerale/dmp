from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view

@api_view(['GET'])
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
def clinics(request):
    template = loader.get_template('clinics.html')
    context = {
        'clinics': [] #TODO
    }
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
def doctors(request):
    template = loader.get_template('doctors.html')
    context = {
        'doctors': [] #TODO
    }
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
def patients(request):
    template = loader.get_template('patients.html')
    context = {
        'patients': [] #TODO
    }
    return HttpResponse(template.render(context, request))