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
        
        if request.method == "POST":
            messages.error(request, 'Not enough data.')
            messages.get_messages(request).used = True
            return PDFPage.display_pdfGen(request)
        departments = MakereportsDepartment.objects.all()
        degreePrograms = MakereportsDegreeprogram.objects.all()
        form = PdfForm()
        return render(
            request, 
            'reports/historical_report.html',
            {
                'showDepartments':departments,
                'showDegrees':degreePrograms,
                'pdfForm':form
            }
        )