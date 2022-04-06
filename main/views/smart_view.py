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
        departments = MakereportsDepartment.objects.all()
        degreePrograms = MakereportsDegreeprogram.objects.all()

        if request.method == "POST" and "department" in request.POST and "degree-program" in request.POST:
            start_department = MakereportsDepartment.objects.filter(id=int(request.POST['department']))[0]
            start_degree_program = MakereportsDegreeprogram.objects.filter(name=request.POST['degree-program'])[0]
            return render(
                request, 
                'smart_assistant/smart_assistant.html',
                {
                        'showDepartments':departments,
                        'showDegrees':degreePrograms,
                        'start_department': start_department,
                        'start_degree_program': start_degree_program
                }       
            )

        return render(
        request, 
        'smart_assistant/smart_assistant.html',
			{
				'showDepartments':departments,
				'showDegrees':degreePrograms,
			}       
        )