from django.shortcuts import render
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from main.models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
from AcademicAssessmentAssistant.settings import BASE_DIR
from .reports_view import PDFPage
from ..forms import PdfForm
# Report Gen Imports
from django.http import FileResponse
from .util.pdfgenhelpers import PDFGenHelpers as pg
import io
# Create your views here.
class HistoricalPage():
    """
    Historical View
    """
    def display_historical(request):
        print(request.POST)
        if request.method == "POST" and "historical_woptions" not in request.POST:
            return PDFPage.display_pdfGen(request)
        
        departments = MakereportsDepartment.objects.all()
        degreePrograms = MakereportsDegreeprogram.objects.all()
        form = PdfForm()

        if request.method == "POST" and "department" in request.POST and "degree-program" in request.POST:
            start_department = MakereportsDepartment.objects.filter(id=int(request.POST['department']))[0]
            start_degree_program = MakereportsDegreeprogram.objects.filter(name=request.POST['degree-program'])[0]
            return render(
                request,
                'reports/historical_report.html',
                {
                    'showDepartments':departments,
                    'showDegrees':degreePrograms,
                    'pdfForm':form,
                    'start_department': start_department,
                    'start_degree_program': start_degree_program
                }
            )
        return render(
            request, 
            'reports/historical_report.html',
            {
                'showDepartments':departments,
                'showDegrees':degreePrograms,
                'pdfForm':form
            }
        )