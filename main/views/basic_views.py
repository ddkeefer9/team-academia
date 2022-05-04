from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from main.models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
from AcademicAssessmentAssistant.settings import BASE_DIR
# Report Gen Imports
from django.http import FileResponse
from main.views.degree_comparison_view import DegreeCompPage
from main.views.historical_view import HistoricalPage
import io

from main.views.smart_view import SmartAssistantPage
# Create your views here.
class HomePage():
    def display_index(request):
        """
        Display Index view
            Notes:
                This view handles passing data to be displayed on the homepage.
        """
        departments = MakereportsDepartment.objects.all()
        degreePrograms = MakereportsDegreeprogram.objects.all()
        return render(
            request, 
            'home/home_page.html',
            {'showDepartments':departments,
            'showDegrees':degreePrograms},
        )

    def display_sendDegrees(request):
        """
        Display Send Degrees
            Notes:
                This view handles passing data that is filtered by department to be shown in the degree programs drop down.
        """
        degreePrograms = MakereportsDegreeprogram.objects.filter(department=request.GET.get("department"))
        return render(
            request,
            'home/degreeDropdown.html',
            {'degrees':degreePrograms},
        )
    def display_sendDegreesWithoutAllDegreesOption(request):
        """
        Display Send Degrees
            Notes:
                This view handles passing data that is filtered by department to be shown in the degree programs drop down.
        """
        degreePrograms = MakereportsDegreeprogram.objects.filter(department=request.GET.get("department"))
        return render(
            request,
            'home/degreeDropdownWithoutAllPrograms.html',
            {'degrees':degreePrograms},
        )
    
    def page_traversal(request):
        """
        Page traversal view
            Notes:
                The page traversal view is a view with a use of handling POST requests from the homepage and subsequent pages.
                If somehow the /assistant URL is accessed without a POST (i.e., manually typing URL), then the home page is returned.
        """
        if "historical_woptions" in request.POST:
            return HistoricalPage.display_historical(request)
        elif "smart_woptions" in request.POST:
            return SmartAssistantPage.display_smartAssistant(request)
        elif "comparisons_woptions" in request.POST:
            return DegreeCompPage.display_degree_comp(request)
        else:
            return HomePage.display_index(request)

