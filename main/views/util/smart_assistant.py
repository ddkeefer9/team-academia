
from AcademicAssessmentAssistant.settings import BASE_DIR
import re
import nltk
import json
from nltk.tokenize import word_tokenize
from django.utils.html import format_html
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from ...models import \
        MakereportsAssessmentdata, MakereportsAssessmentversion, MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus


class SLO_Object():
    """
    An initializable class that maintains fields relevant to an SLO object, takes in an slo query object and a degree object
    Contains:
        degree: The degree object that contains this SLO
        slo_object: The slo query object from the database
        goal_text: The text of the SLO in plain english
        bloom_taxonomy: The text of the Bloom's taxonomy level
        bloom_score: The score associated with the Bloom's taxonomy level
        count: The number of relevant mentions to the degree program
        feedback: The feedback text to display for this SLO
        score: The score associated with the colored scoring for this SLO.
    """
    def __init__(self, slo_object, degree):
        self.degree = degree
        self.slo_object = slo_object
        self.goal_text = SmartAssistantHelper.SLO_goaltext(self.slo_object)
        self.bloom_taxonomy = SmartAssistantHelper.SLO_Blooms(self.slo_object)
        self.bloom_score = SmartAssistantHelper.Blooms_Score[self.bloom_taxonomy]
        self.count = SmartAssistantHelper.discipline_count(self)
        self.feedback = SmartAssistantHelper.feedback(self)
        self.score = SmartAssistantHelper.scoreSLO(self)

class Degree_Object():
    """
    An initializable class that maintains fields relevant to a degree object, takes in a degree query object
    Contains:
        degree_name: The given name of the degree
        keywords: The list of keywords relevant to the degree found in the utility file
        keys: The keys generated from keywords for any relevant words to the degree
        level: Undergraduate or Graduate marked as 'UG' or 'G'
        leveltext: Undegraduate or Graduate makred in plain text
        bloom_level: Minimum reuqired bloom's taxonomy numerically represented
        bloom_level_text: Minimum required bloom's taxonomy in text
    """
    def __init__(self, degree):
        self.degree_name = degree.name
        self.keywords = SmartAssistantHelper.keywords[self.degree_name]
        self.keys = SmartAssistantHelper.keys_from_keywords(self.keywords)
        self.level = degree.level
        self.levelText = "undergraduate" if degree.level == "UG" else "graduate"
        self.bloom_level = 2 if degree.level == "UG" else 4
        self.bloom_level_text = "Application" if degree.level == "UG" else "Synthesis"


class SmartAssistantHelper():
    """
    A static class that maintains Bloom's Taxonomy Lookup tables, a set of NTLK necessary downloads and imports, and utility files.
        Contains:
            Blooms_Abbrev: A Dicrionary mapping Bloom's Abbreviationst to Full words
            Blooms_Score: A dictionary mapping BLoom's levels to scores 0-5
            en_stop: A set of stopwords in NTLK
            keywords: A set of keywords relevant to each degree
            Helper Fucntions: To provide utility for degree and SLO objects
    """
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
    Blooms_Score['Evaluation'] = 5
    Blooms_Score['Synthesis'] = 4
    Blooms_Score['Analysis'] = 3
    Blooms_Score['Application'] = 2
    Blooms_Score['Comprehension'] = 1
    Blooms_Score['Knowledge'] = 0
    def SLO_goaltext(slo_object):
        """
        Helper function to grab and clean the SLO goal text found in the database
        Returns:
            A string representing the SLO goal text cleaned from any formatting
        """
        first_report_goal_text = ""
        if slo_object is not None:
            first_report_goal_text = SmartAssistantHelper.cleanhtml(slo_object.goaltext)
        return first_report_goal_text

    def SLO_Blooms(slo_object):
        """
        Helper function to find the correct level of Blooms Taxxonomy from the abbreviation found in the databased. 
        Makes use of the Smart Assistant Helper tables for Bloom Abbreviations
        Returns:
            The SLO Blooms Level
            Or a blank string if none is found
        """
        if slo_object is not None:
            slo_make_report = slo_object.slo
            bloom_abbrev = SmartAssistantHelper.cleanhtml(slo_make_report.blooms)
            return SmartAssistantHelper.Blooms_Abbrev[bloom_abbrev]
        return ""

    def cleanhtml(raw_html):
        """
        Helper function to remove html tagging text found in a html string
        Returns:
            A string with any tagging found removed
        """
        return re.sub(re.compile('<.*?>'), '', raw_html)

    def feedback(SLO):
        """
        Function to generate the feedback text of an SLO based on the SLO object fields already calculated
        Returns:
            A string representing in plain english the relevancy of the SLo to the degree as well as the SLO Bloom Level relation to the minimum degree requirements
        """
        feedback = ""
        if SLO.count >= 1:
            feedback += "SLO contains discipline specific content. It contains "+ str(SLO.count) + (" mentions " if SLO.count > 1 else " mention ") + "to relevant keyword synonyms for " + SLO.degree.degree_name + " in WordNet. "
        else:
            feedback += "SLO is generic and does not contain discipline specific content for relevant keyword synonyms for " + SLO.degree.degree_name + " in WordNet. "
            feedback += "Consider updating the SLO to contain objectives more relevant to the discipline. "

        feedback += "SLO reaches Bloom's Taxonomy level of " + SLO.bloom_taxonomy + ". "
        if SmartAssistantHelper.Blooms_Score[SLO.bloom_taxonomy] >= 3:
            bloom_num = SmartAssistantHelper.Blooms_Score[SLO.bloom_taxonomy] - SmartAssistantHelper.Blooms_Score[SmartAssistantHelper.Blooms_Abbrev['AP']]
            feedback += "This SLO is " + str(bloom_num) + (" levels " if bloom_num > 1 or bloom_num == 0 else " level ") + " ahead of the required minimum. "
        else:
            bloom_num = SmartAssistantHelper.Blooms_Score[SmartAssistantHelper.Blooms_Abbrev['AP']] - SmartAssistantHelper.Blooms_Score[SLO.bloom_taxonomy]
            feedback += "This SLO is " + str(bloom_num) + (" levels " if bloom_num >1 or bloom_num ==0 else " level ") + " behind the required minimum. "
        return feedback

    def scoreSLO(SLO):
        """
        Function to score an SLO based on the combined Blooms and Relevancy to degree characteristics
        Returns:
            A Number defining the overall SLO score where:  
             0- Did not meet Bloom's Minimum Criteria or Degree Relevancy (Red)
             1 - Met either Bloom's Minimum Criteria or Degree Relevancy (Yellow)
             2 - Met both Bloom's Minimum Criteria and Degree Relevancy (Green)
        """
        score = 0 
        if(SLO.bloom_score >= SLO.degree.bloom_level):
            score += 1
        if(SLO.count > 0):
            score += 1
        return score
            


    def discipline_count(SLO):
        """
        Function to count the number of relevant words found in tokenized SLO text
        Returns:
            Integer representing number of relevant keyword mentions found in an SLO text
        """
        tokens = SmartAssistantHelper.prepare_text_for_lda(SLO.goal_text)
        count = 0
        for token in tokens:
            if token in SLO.degree.keys:
                count = count + 1
        return count


    def aggregateFeedbackMetrics(SLOList):
        """
        Helper function to provide the metrics necessary for creating the feedback text for a degree programm
        Returns:
            A 3-tuple of the form (numSLO, bloom_count, bloom_list) where:
                numSLO is a counter for the number of SLO's that are considered degree relevant
                bloom_count is a counter for the number of SLO's that meet Bloom's taxonomy needs for this degree program
                bloom_lust is an array with 6 elements corresponding to the number of SLO's in each category of Bloom's taxonomy
        """
        #Each index is a level of Bloom's Taxonomy
        degree = SLOList[0].degree
        numSLO = 0
        bloom_count = 0
        bloom_list = [0,0,0,0,0,0]
        for idx,SLO in enumerate(SLOList):
            if SLO.bloom_score >= degree.bloom_level:
                bloom_count += 1
            if SLO.count > 0:
                numSLO += 1
            if SLO.bloom_score is not None:
                bloom_list[SLO.bloom_score] += 1
        return (numSLO, bloom_count, reversed(bloom_list))
            
            
    def aggregateFeedbackText(SLOList):
        """
        Provides the textfeedback for an entire degree, overviewing its Bloom's taxonomy level and SLO relevancy
        Returns:
            A string formated with html tagging to display the BLooms Distribution, SLO relevancy, and minimum requirements
        """
        degree = SLOList[0].degree
        (numSLO, bloom_count, bloom_list) = SmartAssistantHelper.aggregateFeedbackMetrics(SLOList)
        score = 0
        if numSLO > len(SLOList) / 2:
            score += 1
        if bloom_count > 1:
            score += 1
        bloom_levels = list(SmartAssistantHelper.Blooms_Abbrev.values())
        feedback = ""
        feedback = "A " + degree.levelText +" degree must contain atleast one SLO with a Bloom's Taxonomy level of atleast " +  degree.bloom_level_text + " status. " 
        feedback += "This degree program contains " + str(bloom_count) + " SLO's that match or exceed the minimum requirement. "
        feedback += " A degree should consist of atleast half (" + str(int(len(SLOList)/2)) + ") of the SLO's considered discipline specific. "
        feedback += "This degree contains " + str(numSLO) + (" SLO " if numSLO == 1 else " SLOs ") + " considered discipline specific. "
        feedback += " The following is the distribution of SLO's which match each Bloom's Taxonomy Level.<br><br>Bloom Distribution:<br>"
        for idx,element in enumerate(bloom_list):
            feedback += bloom_levels[idx] + ": " + str(element) + "<br>"

        feedback = format_html("<p>"+ feedback +"</p>")
        return (feedback, score)


    def cosine_similarity_degrees(degree1, degree2):
        """
        Comoutes the cosine text similarity average across all SLO's in one degree to another degree. 
        This is found by taking each SLO in a degree, and finding the most similar SLO in a second degree, then computing its text similarity score.
        Each of these scores are averaged across a degree. A degree mapped to itself will return 1. Degrees mapped to each other will not return the same value.
        Returns:
            A number representing the average SLO similarity max mapping from one degree to another degree
        """
        (_,sloList1,_) = SmartAssistantHelper.sloQuerySet(degree1)
        (_,sloList2,_) = SmartAssistantHelper.sloQuerySet(degree2)
        if (sloList1 is None or len(sloList1) == 0):
            return 1
        if (sloList2 is None or len(sloList2) == 0):
            return 0
        cosine_slo_list_list = []
        for slo1 in sloList1:
            cosine_slo_list = []
            for slo2 in sloList2:
                cosine_slo_list.append(SmartAssistantHelper.cosine_similarity_slo(slo1,slo2))

            cosine_slo_list_list.append(cosine_slo_list)

        list2 = list(map(max, cosine_slo_list_list))
        return sum(list2)/len(list2)



    def cosine_similarity_slo(slo1,slo2):
        """
        Helper function to determine the direct text similarity between two slo's
        Returns:
            The text similarity value between SLO's
        """
        #Extract Goal Text From SLOs
        X = SmartAssistantHelper.SLO_goaltext(slo1)
        Y = SmartAssistantHelper.SLO_goaltext(slo2)
        #Extract Stop Words from Helper
        stops = SmartAssistantHelper.en_stop

        # tokenization of SLO text
        X_list = SmartAssistantHelper.tokenize(X) 
        Y_list = SmartAssistantHelper.tokenize(Y)
        
        # empty lists for unionization
        l1 =[];l2 =[]
        
        # remove stop words fron SLO text
        X_set = {w for w in X_list if not w in stops} 
        Y_set = {w for w in Y_list if not w in stops}
        
        # form a set containing keywords of both strings 
        rvector = X_set.union(Y_set) 
        for w in rvector:
            if w in X_set: l1.append(1) #vector 1
            else: l1.append(0)
            if w in Y_set: l2.append(1) #vector 2
            else: l2.append(0)
        c = 0
        
        # cosine formula 
        for i in range(len(rvector)):
                c+= l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)
        return cosine


    def keys_from_keywords(keywords):
        """
        Helper function to find a list of synonyms from a keyword. Utilizes the Wordnet database
        Returns:
            List of synonyms related to the keyword
        """
        key_syms = set()
        for key in keywords:
            synsets = wn.synsets(key)
            for synset in synsets:
                lemmas = synset.lemmas()
                for lemma in lemmas:
                    key_syms.add(lemma.name())
        return key_syms

    def prepare_text_for_lda(text):
        """
        Helper function to prepate text for analysis by tokenizing, lemmatizing, and removing stop words
        Returns:
            A List of tokens from the original text post-processing
        """
        tokens = SmartAssistantHelper.tokenize(text)
        tokens = nltk.pos_tag(tokens)
        tokens = [(token.lower(),tag) for (token,tag) in tokens if len(token) > 4]
        tokens = [(token,tag) for (token,tag) in tokens if token not in SmartAssistantHelper.en_stop]
        tokens = [SmartAssistantHelper.get_lemma2(token,tag) for (token,tag) in tokens]
        return tokens

    def get_lemma2(word,tag): 
        """
        Helper function to lemmatize a word pased on its Part of Speech Tag. Helps reduce ing/ly endings
        Returns:
            The Lemmatized word, passed to Wordnet by its part of speech tag if relevant
        
        """
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
        """
        Helper function to return a lemma from a given word
        Returns:
            Original word if there is no attached lemma
            The lemma symbolizing the word if it exists in the WordNet database
        """
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma

    def tokenize(text):
        """
        Helper function to tokenize a given pure text element
        Returns:
            A List of tokens
        """
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

