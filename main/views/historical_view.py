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
        """
        Display Historical view
            Notes:
                This view handles POST requests as well as GET requests for the historical data page. 
                The view will either generate the PDF if the request is a POST and not from the homepage.
                Or it will persist some data from the homepage from a POST request.
                Or it will simply render the page (only possible by manually typing URL).
        """
        if request.method == "POST" and "historical_woptions" not in request.POST:
            return PDFPage.display_pdfGen(request)
        
        departments = MakereportsDepartment.objects.all()
        degreePrograms = MakereportsDegreeprogram.objects.all()
        form = PdfForm()
        context = dict()      
        context['showDepartments'] = departments
        context['showDegrees'] = degreePrograms
        context['pdfForm'] = form      
        if request.method == "POST" and "department" in request.POST and "degree-program" in request.POST:
            start_department = MakereportsDepartment.objects.filter(id=int(request.POST['department']))
            start_degree_program = MakereportsDegreeprogram.objects.filter(name=request.POST['degree-program'])
            context['start_department'] = start_department[0]
            if start_degree_program:
                context['start_degree_program'] = start_degree_program[0]
            return render(
                request,
                'reports/historical_report.html',
                context
            )
        return render(
            request, 
            'reports/historical_report.html',
            context
        )