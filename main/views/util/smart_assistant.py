
from AcademicAssessmentAssistant.settings import BASE_DIR
import re
from .pdf_generation import PDFGenHelpers as pg
from ...models import \
        MakereportsAssessmentdata, MakereportsAssessmentversion, MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus


class SLO_Object():
    def __init__(self, slo_object):
        self.slo_object = slo_object
        self.goal_text = SmartAssistantHelper.SLO_goaltext(self.slo_object)
        self.bloom_taxonomy = SmartAssistantHelper.SLO_Blooms(self.slo_object)

class SmartAssistantHelper():
    Blooms_Abbrev = dict()
    Blooms_Abbrev['EV'] = "Evaluation"
    Blooms_Abbrev['SN'] = "Synthesis"
    Blooms_Abbrev['AN'] = "Analysis"
    Blooms_Abbrev['AP'] = "Application"
    Blooms_Abbrev['CO'] = "Comprehension"
    Blooms_Abbrev['KN'] = "Knowledge"
    """
            A 3-tuple of the form: (dpqs, sirqs, sirsqs) where:
                - dpqs: is the Degree program queryset.
                - sirqs: is the SLOinreport queryset.
                - sirsqs: is the SLOinreportstatus queryset.
    """
    def SLOList_goaltext(slo_list):
        slo_texts = []
        for i in range(len(slo_list)):
            slo_texts.append(SmartAssistantHelper.SLO_goaltext(slo_list[i]))
        return slo_texts

    def SLO_goaltext(slo_object):
        first_report_goal_text = ""
        if slo_object is not None:
            first_report_goal_text = SmartAssistantHelper.cleanhtml(slo_object.goaltext)
        return first_report_goal_text

    def SLOList_bloomText(slo_list):
        slo_texts = []
        for i in range(len(slo_list)):
            slo_texts.append(SmartAssistantHelper.SLO_Blooms(slo_list[i]))
        return slo_texts


    def SLO_Blooms(slo_object):
        if slo_object is not None:
            slo_make_report = slo_object.slo
            bloom_abbrev = SmartAssistantHelper.cleanhtml(slo_make_report.blooms)
            return SmartAssistantHelper.Blooms_Abbrev[bloom_abbrev]
        return ""



    def cleanhtml(raw_html):
        return re.sub(re.compile('<.*?>'), '', raw_html)

    

    def sloQuerySet(degreeprogram_name):
        """
        Helper for querying the database to generate our default report.
        Queries from the MakereportsReport table -> MakereportsSloinreport table -> MakereportsSlostatus table.
        Returns:
        A 3-tuple of the form: (dpqs, sirqs, sirsqs) where:
                - dpqs: is the Degree program queryset.
                - sirqs: is the SLOinreport queryset.
                - sirsqs: is the SLOinreportstatus queryset.
        """

        # Degree program report queryset.
        mrdpqs = MakereportsDegreeprogram.objects.filter(name=degreeprogram_name)
        if len(mrdpqs) < 1:
            return (None, None, None)
        dprqs = MakereportsReport.objects.filter(degreeprogram=mrdpqs[0])
        #print(dprqs)
        if len(dprqs) < 1:  # Degree program does not have a report associated with it.
            return (None,None,None)
        # SLOs in report queryset.
        sirqs = MakereportsSloinreport.objects.filter(report__in=dprqs)
        # SLOs in report status queryset. 
        sirsqs = MakereportsSlostatus.objects.filter(sloir__in=sirqs)
        return dprqs, sirqs, sirsqs

