from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from main.models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
from AcademicAssessmentAssistant.settings import BASE_DIR
# Report Gen Imports
from django.http import FileResponse
from ..util.pdfgenhelpers import PDFGenHelpers as pg
import io
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
                print(degreePrograms)
                return render(
                        request,
                        'home/degreeDropdown.html',
                        {'degrees':degreePrograms},
                )