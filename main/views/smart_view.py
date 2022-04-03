from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from main.models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
from AcademicAssessmentAssistant.settings import BASE_DIR
# Report Gen Imports
from django.http import FileResponse
import io
# Create your views here.
class SmartAssistantPage():
    """
    Smart Assistant View
    """
    def display_smartAssistant(request):
            return render(
                    request, 
                    'smart_assistant/smart_assistant.html',
            )