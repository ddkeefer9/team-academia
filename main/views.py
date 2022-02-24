from django.shortcuts import render
from django.http import HttpResponse
from .models import MakereportsAssessment
# Create your views here.

def index(response):
        # MakereportsSloinreport.objects.all()
        return HttpResponse("Hello World! Patrik was here (x)")

def table_home_view(response):
        return HttpResponse("changed view...")
