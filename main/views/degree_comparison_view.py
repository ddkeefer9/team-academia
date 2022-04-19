from django.shortcuts import render
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from main.models import \
        MakereportsCollege, MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
from AcademicAssessmentAssistant.settings import BASE_DIR
from .reports_view import PDFPage
from ..forms import PdfForm
# Report Gen Imports
from django.http import FileResponse
from .util.pdf_generation import PDFGenHelpers as pg
import io
# Create your views here.
class DegreeCompPage():
    """
    Degree Comparison View
    """
    def display_degree_comp(request):
        """
        Display Degree Comparison view
            Notes:
                This view handles POST requests as well as GET requests for the historical data page. 
                The view will either generate the PDF if the request is a POST and not from the homepage.
                Or it will persist some data from the homepage from a POST request.
                Or it will simply render the page (only possible by manually typing URL).
        """
        if request.method == "POST" and "comparisons_woptions" not in request.POST:
            return PDFPage.display_degree_pdfGen(request)
        
        departments = MakereportsDepartment.objects.all()
        degreePrograms = MakereportsDegreeprogram.objects.all()
        colleges = MakereportsCollege.objects.all()
        
        form = PdfForm()

        if request.method == "POST" and "department" in request.POST and "degree-program" in request.POST:
            start_department = MakereportsDepartment.objects.filter(id=int(request.POST['department']))[0]
            start_degree_program = MakereportsDegreeprogram.objects.filter(name=request.POST['degree-program'])[0]
            return render(
                request,
                'reports/degree_program_comparison.html',
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
            'reports/degree_program_comparison.html',
            {
                'showDepartments':departments,
                'showDegrees':degreePrograms,
                'showColleges':colleges,
                'pdfForm':form
            }
        )