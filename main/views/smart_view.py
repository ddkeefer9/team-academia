from xml.dom.minidom import Element
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from main.models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
from nltk.corpus import wordnet
from AcademicAssessmentAssistant.settings import BASE_DIR
from .util.pdf_generation import PDFGenHelpers as pg
from .util.smart_assistant import SmartAssistantHelper as sa
from .util.smart_assistant import SLO_Object
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
		if request.method == "POST" and "department" in request.POST and "degree-program" in request.POST:
			start_department = MakereportsDepartment.objects.filter(id=int(request.POST['department']))[0]
			start_degree_program = MakereportsDegreeprogram.objects.filter(name=request.POST['degree-program'])[0]
			context['start_department'] = start_department
			if start_degree_program:
				context['start_degree_program'] = start_degree_program
			dprqs, sirqs, sirsqs = sa.sloQuerySet(request.POST['degree-program'])
			slo_list = []
			for slo_ in sirqs:
				slo_list.append(SLO_Object(slo_, start_degree_program))
			context['showSLOs'] = slo_list    

		return render(
			request, 
			'smart_assistant/smart_assistant.html',
			context
		)