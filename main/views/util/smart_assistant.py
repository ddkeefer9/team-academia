
from AcademicAssessmentAssistant.settings import BASE_DIR
import re
from .pdf_generation import PDFGenHelpers as pg
from ...models import \
        MakereportsAssessmentdata, MakereportsAssessmentversion, MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus

class SmartAssistantHelper():

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


    def cleanhtml(raw_html):
        return re.sub(re.compile('<.*?>'), '', raw_html)

