from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from main.models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
from AcademicAssessmentAssistant.settings import BASE_DIR
# Report Gen Imports
from django.http import FileResponse
from main.views.historical_view import HistoricalPage
import io

from main.views.smart_view import SmartAssistantPage
# Create your views here.
class HomePage():
    def display_index(request):
        departments = MakereportsDepartment.objects.all()
        degreePrograms = MakereportsDegreeprogram.objects.all()
        return render(
            request, 
            'home/home_page.html',
            {'showDepartments':departments,
            'showDegrees':degreePrograms},
        )

    def display_sendDegrees(request):
        degreePrograms = MakereportsDegreeprogram.objects.filter(department=request.GET.get("department"))
        return render(
            request,
            'home/degreeDropdown.html',
            {'degrees':degreePrograms},
        )
    
    def page_traversal(request):
        print(request.POST)
        if "historical_woptions" in request.POST:
            return HistoricalPage.display_historical(request)
        elif "smart_woptions" in request.POST:
            return SmartAssistantPage.display_smartAssistant(request)
        departments = MakereportsDepartment.objects.all()
        degreePrograms = MakereportsDegreeprogram.objects.all()
        return render(
            request, 
            'home/home_page.html',
            {'showDepartments':departments,
            'showDegrees':degreePrograms},
        )

