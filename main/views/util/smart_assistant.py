
from AcademicAssessmentAssistant.settings import BASE_DIR
import re
import nltk
import json
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

class Degree_Object():
    def __init__(self, degree):
        self.degree_name = degree.name
        self.keywords = SmartAssistantHelper.keywords[self.degree_name]
        self.keys = SmartAssistantHelper.keys_from_keywords(self.keywords)
        self.level = degree.level

class SmartAssistantHelper():
    f = open('main/views/util/degree_keywords.json', 'r')
    keywords = json.loads(f.read())
    en_stop = set(nltk.corpus.stopwords.words('english'))
    Blooms_Abbrev = dict()
    Blooms_Abbrev['EV'] = "Evaluation"
    Blooms_Abbrev['SN'] = "Synthesis"
    Blooms_Abbrev['AN'] = "Analysis"
    Blooms_Abbrev['AP'] = "Application"
    Blooms_Abbrev['CO'] = "Comprehension"
    Blooms_Abbrev['KN'] = "Knowledge"
    Blooms_Score = dict()
    Blooms_Score['Evaluation'] = 6
    Blooms_Score['Synthesis'] = 5
    Blooms_Score['Analysis'] = 4
    Blooms_Score['Application'] = 3
    Blooms_Score['Comprehension'] = 2
    Blooms_Score['Knowledge'] = 1
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
        feedback = ""
        tokens = SmartAssistantHelper.prepare_text_for_lda(SLO.goal_text)
        count = 0
        for token in tokens:
            if token in SLO.degree.keys:
                count = count + 1
        
        if count >= 1:
            feedback += "SLO contains discipline specific content. It contains "+ str(count) + (" mentions " if count > 1 else " mention ") + "to relevant keyword synonyms for " + SLO.degree.degree_name + " in WordNet. "
        else:
            feedback += "SLO is generic and does not contain discipline specific content for relevant keyword synonyms for " + SLO.degree.degree_name + " in WordNet. "
            feedback += "Consider updating the SLO to contain objectives more relevant to the discipline. "

        feedback += "SLO reaches Bloom's Taxonomy level of " + SLO.bloom_taxonomy + ". A degree of LEVEL must contain atleast one SLO with a Bloom's Taxonomy level of atleast " + SmartAssistantHelper.Blooms_Abbrev['AP'] + ". "
        if SmartAssistantHelper.Blooms_Score[SLO.bloom_taxonomy] >= 3:
            bloom_num = SmartAssistantHelper.Blooms_Score[SLO.bloom_taxonomy] - SmartAssistantHelper.Blooms_Score[SmartAssistantHelper.Blooms_Abbrev['AP']]
            feedback += "This degree is " + str(bloom_num) + (" levels " if bloom_num > 1 or bloom_num == 0 else " level ") + " ahead of the required minimum. "
        else:
            bloom_num = SmartAssistantHelper.Blooms_Score[SmartAssistantHelper.Blooms_Abbrev['AP']] - SmartAssistantHelper.Blooms_Score[SLO.bloom_taxonomy]
            feedback += "This degree is " + str(bloom_num) + (" level " if bloom_num >1 or bloom_num ==0 else " level ") + " behind the required minimum. "
        return feedback


    def keys_from_keywords(keywords):
        key_syms = set()
        for key in keywords:
            synsets = wn.synsets(key)
            for synset in synsets:
                lemmas = synset.lemmas()
                for lemma in lemmas:
                    key_syms.add(lemma.name())
        return key_syms

    def prepare_text_for_lda(text):
        tokens = SmartAssistantHelper.tokenize(text)
        tokens = nltk.pos_tag(tokens)
        tokens = [(token.lower(),tag) for (token,tag) in tokens if len(token) > 4]
        tokens = [(token,tag) for (token,tag) in tokens if token not in SmartAssistantHelper.en_stop]
        tokens = [SmartAssistantHelper.get_lemma2(token,tag) for (token,tag) in tokens]
        return tokens

    def get_lemma2(word,tag):
        tagFlag = False
        #Lemmatize Verbs/Adjectives by their type (gets rid of ly,ing endings)
        if tag[0] == 'V':
            nvatag = 'v'
            tagFlag = True
        elif tag[0] == 'J':
            nvatag = 'a'
            tagFlag = True
        return WordNetLemmatizer().lemmatize(word , nvatag) if tagFlag else WordNetLemmatizer().lemmatize(word)

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

