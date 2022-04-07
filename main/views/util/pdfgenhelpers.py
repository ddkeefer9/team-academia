import re
from django.db.models import Q
import numpy as np
from ...models import (
    MakereportsAssessmentdata, MakereportsAssessmentversion, MakereportsReport, MakereportsSloinreport, 
    MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, MakereportsAssessmentversion
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from AcademicAssessmentAssistant.settings import BASE_DIR

def cleanhtml(raw_html):
    return re.sub(re.compile('<.*?>'), '', raw_html)

class PDFGenHelpers:

    def pdfGenQuery(degreeprogram_name, request):
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
        dprqs = MakereportsReport.objects.filter(
            Q(degreeprogram=mrdpqs[0]) &
            Q(year__lte=request.POST['date_end']) &
            Q(year__gte=request.POST['date_start'])
        )
        # print(dprqs)
        if len(dprqs) < 1:  # Degree program does not have a report associated with it.
            return (None,None,None)
        # SLOs in report queryset.
        sirqs = MakereportsSloinreport.objects.filter(report__in=dprqs)

        # SLOs in report status queryset. 
        sirsqs = MakereportsSlostatus.objects.filter(sloir__in=sirqs)
        # Assessment version in report query set.
        avirqs = MakereportsAssessmentversion.objects.filter(slo__in=sirqs)
        return dprqs, sirqs, sirsqs

    def pdfGenPlotting(dprqs, sirqs, sirsqs):
        """
        Helper for plotting the resulting QuerySet from pdfGenQuery for our default report

        Returns:
            - plot: The plot utilizing the data.
        """
        possible_statuses = ['Met', 'Partially Met', 'Not Met', 'Unknown']
        degree_program = dprqs[0].degreeprogram.name
        slos_by_report = list()
        dp_df = pd.DataFrame()
        for report in dprqs:
            statuses = list()
            SLO_nums = list()
            slo_dict = dict()
            report_slos = MakereportsSloinreport.objects.filter(report=report)
            report_slo_statuses = MakereportsSlostatus.objects.filter(sloir__in=report_slos)
            for status in report_slo_statuses:
                statuses.append(status.status)
            for slo in report_slos:
                SLO_nums.append(slo.number)
            for i in range(len(statuses)):
                slo_dict[SLO_nums[i]] = statuses[i]
            report_series = pd.Series(data=slo_dict, name=str(report))   
            dp_df = dp_df.append(report_series)
        slomet_freq = dp_df.apply(pd.Series.value_counts, axis=1).T.reindex(possible_statuses, fill_value=np.nan)
        
        fig, ax = plt.subplots(slomet_freq.iloc[0].size, 1)
        for i in range(slomet_freq.iloc[0].size):
            plot = sns.countplot(y=slomet_freq.iloc[:,i], ax=ax[i], hue=slomet_freq.index)
            ax[i].get_legend().remove()
        fig.tight_layout()
        handles, labels = plt.gca().get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right')
        plt.savefig(str(BASE_DIR) + "/main/static/testfig.png")
        
    def pdfDegreeGenQuery(degreeprogram_name):
        """
        Helper for querying the database to generate our default report.

        Queries from the MakereportsReport table -> MakereportsSloinreport table -> MakereportsSlostatus table.

        Returns:
        A 3-tuple of the form: (dpqs, sirqs, sirsqs) where:
                - dpqs: is the Degree program queryset.
                - sirqs: is the SLOinreport queryset.
                - sirsqs: is the SLOinreportstatus queryset.
        """
        mrdpqs = MakereportsDegreeprogram.objects.filter(name=degreeprogram_name)
        if len(mrdpqs) < 1:
            return (None, None)
                # Degree program report queryset.
        dprqs = MakereportsReport.objects.filter(degreeprogram=mrdpqs[0])
        if len(dprqs) < 1:  # Degree program does not have a report associated with it.
            return (None,None)
        
        reportsAssessmentVersionQS = MakereportsAssessmentversion.objects.filter(report__in=dprqs)
        
        assessmentDataQS = MakereportsAssessmentdata.objects.filter(assessmentversion__in=reportsAssessmentVersionQS)
        return dprqs, assessmentDataQS

    def pdfDegreeGenPlotting(degree_program, degree_program2):
        """
        Helper for plotting the resulting QuerySet from pdfGenQuery for our default report

        Returns:
            - plot: The plot utilizing the data.
        """
        degree_programs = []
        overallProficiency = []
        
        dprqs, assessmentDataQS = PDFGenHelpers.pdfDegreeGenQuery(degree_program)
        dprqs2, assessmentDataQS2 = PDFGenHelpers.pdfDegreeGenQuery(degree_program2)
        print(degree_program)
        print(degree_program2)
        if assessmentDataQS is not None and len(assessmentDataQS) > 0 :
            degree_programs.append(dprqs[0].degreeprogram.name)
            overallProficiency.append(assessmentDataQS[0].overallproficient)
        if assessmentDataQS2 is not None and len(assessmentDataQS2) > 0 :
            degree_programs.append(dprqs2[0].degreeprogram.name)
            overallProficiency.append(assessmentDataQS2[0].overallproficient)

        df = pd.DataFrame(data = {
            'Programs' : degree_programs,
            'Overall Proficiency' : overallProficiency,
        })

        if (len(degree_programs) > 0):
            plot = sns.catplot(x="Programs", y="Overall Proficiency",  kind="bar", data=df)
            plot.set(ylim=(50,100))
            
            #Start putting numbers above bar plots*******************************
            # extract the matplotlib axes_subplot objects from the FacetGrid
            ax = plot.facet_axis(0, 0)

            # iterate through the axes containers
            for c in ax.containers:
                labels = [f'{(v.get_height())}%' for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            #End putting numbers above bar plots*********************************

            plt.savefig(str(BASE_DIR) + "/main/static/degreetestfig.png")
        else:
            plot = sns.catplot(x="Programs", y="Overall Proficiency",  kind="bar", data=df, order=[degree_program, degree_program2])
            plt.savefig(str(BASE_DIR) + "/main/static/degreetestfig.png")
