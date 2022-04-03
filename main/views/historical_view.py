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
class HistoricalPage():
    """
    Historical View
    """
    def display_historical(request):
                departments = MakereportsDepartment.objects.all()
                degreePrograms = MakereportsDegreeprogram.objects.all()
                return render(
                    request, 
                    'reports/historical_report.html',
                    {'showDepartments':departments,
                        'showDegrees':degreePrograms}
            )