from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from main.models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
from AcademicAssessmentAssistant.settings import BASE_DIR
from .util.pdf_generation import PDFGenHelpers as pg
from .util.smart_assistant import SmartAssistantHelper as sa
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
		context = dict()      
		context['showDepartments'] = departments
		context['showDegrees'] = degreePrograms
		print(request)
		if request.method == "POST" and context["start_department"] in request.POST and context["start_degree_program"] in request.POST:
			start_department = MakereportsDepartment.objects.filter(id=int(request.POST['department']))[0]
			start_degree_program = MakereportsDegreeprogram.objects.filter(name=request.POST['degree-program'])[0]
			dprqs, sirqs, sirsqs = pg.historicalPdfGenQuery(request.POST['degree-program'])
			slo_texts = sa.SLOList_goaltext(sirqs)
			print(slo_texts)
			slos = [(element, "FEEDBACK_PLACEHOLDER") for element in slo_texts]
			context['showSLOs'] = slos    
			context['start_department'] = start_department
			if start_degree_program:
				context['start_degree_program'] = start_degree_program

		return render(
			request, 
			'smart_assistant/smart_assistant.html',
			context
		)