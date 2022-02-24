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
                'table_home_page.html',
                {'slosInReport':slo_report},
        )