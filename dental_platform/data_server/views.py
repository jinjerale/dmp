from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def clinics(request):
    template = loader.get_template('clinics.html')
    context = {
        'clinics': [] #TODO
    }
    return HttpResponse(template.render(context, request))

def doctors(request):
    template = loader.get_template('doctors.html')
    context = {
        'doctors': [] #TODO
    }
    return HttpResponse(template.render(context, request))

def patients(request):
    template = loader.get_template('patients.html')
    context = {
        'patients': [] #TODO
    }
    return HttpResponse(template.render(context, request))