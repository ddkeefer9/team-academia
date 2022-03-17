from django.shortcuts import render
from django.http import HttpResponse
from .models import MakereportsSloinreport
from .models import MakereportsDegreeprogram
from .models import MakereportsDepartment
# Create your views here.

def index(request):
        # 
        departments = MakereportsDepartment.objects.all()
        degreePrograms = MakereportsDegreeprogram.objects.all()
        return render(
                request, 
                'home/home_page.html',
                {'showDepartments':departments,
                'showDegrees':degreePrograms},
        )
def smartAssistant(request):
        return render(
                request, 
                'smart_assistant/smart_assistant.html',
        )        
