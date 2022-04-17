
from AcademicAssessmentAssistant.settings import BASE_DIR
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from .pdf_generation import PDFGenHelpers as pg
from ...models import \
        MakereportsAssessmentdata, MakereportsAssessmentversion, MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus


class SLO_Object():
    def __init__(self, slo_object, degree):
        self.degree = degree
        self.slo_object = slo_object
        self.goal_text = SmartAssistantHelper.SLO_goaltext(self.slo_object)
        self.bloom_taxonomy = SmartAssistantHelper.SLO_Blooms(self.slo_object)
        self.feedback = SmartAssistantHelper.feedback(self)


class SmartAssistantHelper():
    #nltk.download('stopwords')
    en_stop = set(nltk.corpus.stopwords.words('english'))
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
    def SLO_goaltext(slo_object):
        first_report_goal_text = ""
        if slo_object is not None:
            first_report_goal_text = SmartAssistantHelper.cleanhtml(slo_object.goaltext)
        return first_report_goal_text

    def SLO_Blooms(slo_object):
        if slo_object is not None:
            slo_make_report = slo_object.slo
            bloom_abbrev = SmartAssistantHelper.cleanhtml(slo_make_report.blooms)
            return SmartAssistantHelper.Blooms_Abbrev[bloom_abbrev]
        return ""

    def cleanhtml(raw_html):
        return re.sub(re.compile('<.*?>'), '', raw_html)

    def feedback(SLO):
        return SmartAssistantHelper.prepare_text_for_lda(SLO.goal_text)

    def prepare_text_for_lda(text):
        tokens = SmartAssistantHelper.tokenize(text)
        tokens = [token for token in tokens if len(token) > 4]
        tokens = [token for token in tokens if token not in SmartAssistantHelper.en_stop]
        tokens = [SmartAssistantHelper.get_lemma(token) for token in tokens]
        return tokens

    def get_lemma2(word):
        return WordNetLemmatizer().lemmatize(word)

    def get_lemma(word):
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma

    def tokenize(text):
        tokens = word_tokenize(text)
        return tokens


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

