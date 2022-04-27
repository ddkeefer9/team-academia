from xml.dom.minidom import Element
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from main.models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
from nltk.corpus import wordnet
from django.contrib import messages
from django.shortcuts import redirect
from AcademicAssessmentAssistant.settings import BASE_DIR
from .util.pdf_generation import PDFGenHelpers as pg
from .util.smart_assistant import SmartAssistantHelper as sa
from .util.smart_assistant import SLO_Object, Degree_Object
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
			degreeProgram = Degree_Object(start_degree_program)
			if sirqs is not None and len(sirqs) > 0:
				for slo_ in sirqs:
					slo_list.append(SLO_Object(slo_, degreeProgram))
			else:
				messages.warning(request, message=f'No SLO data found for {start_degree_program}')
				return redirect('smartAssistant')
			context['showSLOs'] = slo_list
			(aggregateText, aggregateColor) = sa.aggregateFeedbackText(slo_list)
			context['showAggregate'] = aggregateText
			context['aggregateColor'] = aggregateColor

		return render(
			request, 
			'smart_assistant/smart_assistant.html',
			context
		)