from django.shortcuts import render
from django.http import HttpResponse
from .models import MakereportsSloinreport
# Create your views here.

def index(request):
        # 
        slo_report = MakereportsSloinreport.objects.all()
        slo_report = slo_report[0:10]
        return render(
                request, 
                'home/home_page.html',
                {'slosInReport':slo_report},
        )
def smartAssistant(request):
        return render(
                request, 
                'smart_assistant/smart_assistant.html',
        )