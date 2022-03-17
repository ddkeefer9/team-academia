from django.shortcuts import render
from django.http import HttpResponse
from .models import MakereportsSloinreport
from .models import MakereportsDegreeprogram
# Create your views here.

def index(request):
        # 
        degreePrograms = MakereportsDegreeprogram.objects.all()
        return render(
                request, 
                'home/home_page.html',
                {'showdegrees':degreePrograms},
        )