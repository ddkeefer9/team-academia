import re
from django.db.models import Q
import numpy as np
from ...models import (
    MakereportsAssessmentdata, MakereportsAssessmentversion, MakereportsCollege, MakereportsReport, MakereportsSloinreport, 
    MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, MakereportsAssessmentversion
)
import matplotlib
matplotlib.use('Agg')
import pandas as pd, io, seaborn as sns, matplotlib.pyplot as plt
from PIL import Image
from AcademicAssessmentAssistant.settings import BASE_DIR

def cleanhtml(raw_html):
    return re.sub(re.compile('<.*?>'), '', raw_html)

class PDFGenHelpers:

    class SLOStatusPage:

        def __init__(self, dprqs):
            self.dprqs = dprqs
            self.description = "SLO Status"

        def __str__(self):
            return self.description

        def slos_met_by_report_plotting(self):
            possible_statuses = ['Met', 'Partially Met', 'Not Met', 'Unknown']
            degree_program = self.dprqs[0].degreeprogram.name
            dp_df = pd.DataFrame()
            for report in self.dprqs:
                statuses = list()
                SLO_nums = list()
                slo_dict = dict()
                report_slos = MakereportsSloinreport.objects.filter(report=report)
                report_slo_statuses = MakereportsSlostatus.objects.filter(sloir__in=report_slos)
                if len(report_slo_statuses) < 1:
                    continue
                for status in report_slo_statuses:
                    statuses.append(status.status)
                for slo in report_slos:
                    SLO_nums.append(slo.number)
                for i in range(len(statuses)):
                    slo_dict[SLO_nums[i]] = statuses[i]
                report_series = pd.Series(data=slo_dict, name=str(report))   
                dp_df = dp_df.append(report_series)
            slomet_freq = dp_df.apply(pd.Series.value_counts, axis=1).T.reindex(possible_statuses, fill_value=np.nan)
            if slomet_freq.iloc[0].size > 0:
                fig, ax = plt.subplots(slomet_freq.iloc[0].size, 1)
                if slomet_freq.iloc[0].size > 1:
                    for i in range(slomet_freq.iloc[0].size):
                        plot = sns.barplot(y=slomet_freq.index, x=slomet_freq.iloc[:,i], ax=ax[i])
                else:
                    plot = sns.barplot(y=slomet_freq.index, x=slomet_freq.iloc[:,0])
                fig.tight_layout()
                img_buf = io.BytesIO()
                plt.savefig(img_buf)
                plt_img = Image.open(img_buf)
                return plt_img
            else:
                return f"{degree_program} contained no data regarding SLO status."

    def historicalPdfGenPlotting(dprqs, sirqs, sirsqs, request):
        """
        Helper for plotting the resulting QuerySet from pdfGenQuery for our historical report

        Returns:
            - plot: The plot utilizing the data.
        """
        plots = list()
        slo_page = PDFGenHelpers.SLOStatusPage(dprqs=dprqs)
        slostatus_by_report = slo_page.slos_met_by_report_plotting()
        if slostatus_by_report:
            plots.append(slostatus_by_report)
        
        if 'assessmentStats' in request.POST:
            PDFGenHelpers.assessment_stats_for_each_slo(dprqs)
        if 'numbOfSLOsMet' in request.POST:
            n_slos_met = PDFGenHelpers.number_of_slos_met(dprqs)
            if n_slos_met:
                plots.append(n_slos_met)
        return plots


    def assessment_stats_for_each_slo(dprqs):
        pass

    def number_of_slos_met(dprqs):
        pass

    def historicalPdfGenQuery(degreeprogram_name, request):
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
        if len(dprqs) < 1:  # Degree program does not have a report associated with it.
            return (None,None,None)
        # SLOs in report queryset.
        sirqs = MakereportsSloinreport.objects.filter(report__in=dprqs)

        # SLOs in report status queryset. 
        sirsqs = MakereportsSlostatus.objects.filter(sloir__in=sirqs)
        # Assessment version in report query set.
        avirqs = MakereportsAssessmentversion.objects.filter(slo__in=sirqs)
        return dprqs, sirqs, sirsqs

    def pdfDegreeGenQuery(degree_id):
        """
        Helper for querying the database to generate our default report.

        Queries from the MakereportsReport table -> MakereportsSloinreport table -> MakereportsSlostatus table.

        Returns:
        A 3-tuple of the form: (dpqs, sirqs, sirsqs) where:
                - dpqs: is the Degree program queryset.
                - sirqs: is the SLOinreport queryset.
                - sirsqs: is the SLOinreportstatus queryset.
        """
        # collegeQS = MakereportsCollege.objects.filter(name=college_name)
        # if len(collegeQS) < 1:
        #     return (None, None)
        
        # departmentQS = MakereportsDepartment.objects.filter(college__in=collegeQS)

        # degreeProgramQS = MakereportsDegreeprogram.objects.filter(department__in=departmentQS)

        makeReportQS = MakereportsReport.objects.filter(degreeprogram=degree_id)
        if len(makeReportQS) < 1:  # Degree program does not have a report associated with it.
            return (None,None)
        
        reportsAssessmentVersionQS = MakereportsAssessmentversion.objects.filter(report__in=makeReportQS)
        
        assessmentDataQS = MakereportsAssessmentdata.objects.filter(assessmentversion__in=reportsAssessmentVersionQS)
        return makeReportQS, assessmentDataQS

    def pdfCollegeComparisonsPlotting(college_name):
        """
        Plots the college comparisons graphs for a given college name.

        Returns:
            - plot: The plot utilizing the data.
        """
        collegeQS = MakereportsCollege.objects.filter(name=college_name)
        if len(collegeQS) < 1:
            return (None, None)
        
        departmentQS = MakereportsDepartment.objects.filter(college__in=collegeQS)

        degreeProgramQS = MakereportsDegreeprogram.objects.filter(department__in=departmentQS)

        degree_programs = []
        overallProficiency = []

        for degree in degreeProgramQS:
            dprqs, assessmentDataQS = PDFGenHelpers.pdfDegreeGenQuery(degree)
            if assessmentDataQS is not None and len(assessmentDataQS) > 0 :
                degree_programs.append(degree.name)
                overallProficiency.append(assessmentDataQS[0].overallproficient)
                print("loop")
        
        # if assessmentDataQS is not None and len(assessmentDataQS) > 0 :
        #     degree_programs.append(dprqs.degreeprogram.name)
        #     overallProficiency.append(assessmentDataQS.overallproficient)

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
            plot = sns.catplot(x="Programs", y="Overall Proficiency",  kind="bar", data=df, order=degreeProgramQS.all)
            plt.savefig(str(BASE_DIR) + "/main/static/degreetestfig.png")
