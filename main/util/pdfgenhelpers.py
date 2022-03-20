from ..models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
        
def pdfGenHelper(degreeprogram_id):
        # Degree program queryset.
        dpqs = MakereportsReport.objects.filter(degreeprogram=degreeprogram_id)
        # SLOs in report queryset.
        sirqs = MakereportsSloinreport.objects.filter(report__in=dpqs)
        # SLOs in report status queryset. 
        sirsqs = MakereportsSlostatus.objects.filter(sloir__in=sirqs)
        return dpqs, sirqs, sirsqs