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
		print(request.method)
		if request.method == "POST":
			dprqs, sirqs, sirsqs = pg.historicalPdfGenQuery(request.POST['degree-program'])
			slo_texts = sa.SLOList_goaltext(sirqs)
			print(slo_texts)
			slos = [(element, "FEEDBACK_PLACEHOLDER") for element in slo_texts]
			context['showSLOs'] = slos    

		return render(
			request, 
			'smart_assistant/smart_assistant.html',
			context
		)