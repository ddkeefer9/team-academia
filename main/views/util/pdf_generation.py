from pickle import NONE
import re
from django.db.models import Q
import numpy as np
from ...models import (
    MakereportsAssessment, MakereportsAssessmentdata, MakereportsAssessmentversion, MakereportsCollege, MakereportsReport, MakereportsSloinreport, 
    MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, MakereportsAssessmentversion, MakereportsAssessmentaggregate
)
from reportlab.lib.pagesizes import letter
import matplotlib
matplotlib.use('Agg')
import pandas as pd, io, seaborn as sns, matplotlib.pyplot as plt
from PIL import Image
from AcademicAssessmentAssistant.settings import BASE_DIR

class SLOStatusPage:
        """
        Class to describe the SLO Status PDF Page.
        """

        def __init__(self, dprqs, plots_per_page):
            """
            Constructor
            """
            self.dprqs = dprqs
            self.plots_per_page = plots_per_page
            self.description = "SLO Status"

        def __str__(self):
            """
            toString
            """
            return self.description
    
        def get_report_descriptions(self, SLOdata_bool_mask):
            descriptions = list()
            for report in self.dprqs:
                descriptions.append([report.__str__(), "Heading2"])
            for i in range(len(SLOdata_bool_mask)):
                if SLOdata_bool_mask[i]:
                    descriptions[i][0] += " (No SLO Status Data)"
            return descriptions
                
        def slos_met_by_report_plotting(self):
            """
            Main plotting function that creates up to plots_per_page number of plots for a page describing data from the dprqs (Degree Program Report) QuerySet.

            Returns: A PIL object with the plots split into plots_per_page number of subplots. Or returns a string saying:

            This page for (degree_program) contained no data regarding SLO status.

            """
            possible_statuses = ['Met', 'Partially Met', 'Not Met', 'Unknown']
            degree_program = self.dprqs[0].degreeprogram.name
            dp_df = pd.DataFrame()
            SLOdata_bool_mask = []
            for report in self.dprqs:
                statuses = list()
                SLO_nums = list()
                slo_dict = dict()
                report_slos = MakereportsSloinreport.objects.filter(report=report)
                report_slo_statuses = MakereportsSlostatus.objects.filter(sloir__in=report_slos)
                if len(report_slo_statuses) < 1:
                    SLOdata_bool_mask.append(True)
                    continue
                else:
                    SLOdata_bool_mask.append(False)
                for status in report_slo_statuses:
                    statuses.append(status.status)
                for slo in report_slos:
                    SLO_nums.append(slo.number)
                for i in range(len(statuses)):
                    slo_dict[SLO_nums[i]] = statuses[i]
                report_series = pd.Series(data=slo_dict, name=str(report))   
                dp_df = dp_df.append(report_series)
            slomet_freq = dp_df.apply(pd.Series.value_counts, axis=1).T.reindex(possible_statuses, fill_value=np.nan)
            n_plots = slomet_freq.iloc[0].size
            report_descriptions = self.get_report_descriptions(SLOdata_bool_mask)
            if n_plots > 0:
                fig, ax = plt.subplots(self.plots_per_page, 1, sharex=True, sharey=True)
                for i in range(self.plots_per_page):
                    if i in range(n_plots):
                        plot = sns.barplot(y=slomet_freq.index, x=slomet_freq.iloc[:,i], ax=ax[i])
                    else:
                        ax[i].set_visible(False)
                fig.set_size_inches(8.5, 9, forward=True)
                fig.tight_layout()
                img_buf = io.BytesIO()
                plt.savefig(img_buf)
                plt_img = Image.open(img_buf)
                return (plt_img, report_descriptions)
            else:
                return (f"This page for {degree_program} contained no data regarding SLO status.", report_descriptions)

class AssessmentStatisticsPage:
    """
    Class to describe the Assessment Statistics PDF Page.
    """

    def __init__(self, dprqs, sirqs, avirqs, plots_per_page):
        """
        Constructor
        """
        self.dprqs = dprqs
        self.sirqs = sirqs
        self.avirqs = avirqs
        self.plots_per_page = plots_per_page
        self.description = "Assessment Statistics"

    def __str__(self):
        """
        toString
        """
        return self.description

    def assessment_stats_for_each_slo(self):
        for report in self.dprqs:
            slos = MakereportsSloinreport.objects.filter(report=report)
            for slo in slos:
                assessments = MakereportsAssessmentversion.objects.filter(slo=slo)
                for assessment in assessments:
                    aggregates = MakereportsAssessmentaggregate.objects.filter(assessmentversion=assessment)
                    for aggregate in aggregates:
                        description = ( f"Report {report} with SLO {slo} and an assessment with an aggregate of {aggregate.aggregate_proficiency} percent proficient and a target of {assessment.target} percent,"
                                        f" marked as {'met' if aggregate.met else 'unmet'}."
                        )
                        fig = plt.plot([1, 2, 3], [3, 2, 1])  
                        img_buf = io.BytesIO()
                        plt.savefig(img_buf)
                        plt_img = Image.open(img_buf)
                        return (plt_img, [[description, "Normal"]])                    

class PDFGenHelpers:

    def historicalPdfGenPlotting(dprqs, sirqs, sirsqs, avirqs, request, plots_per_page = 4):
        """
        Helper for plotting the resulting QuerySet from pdfGenQuery for our historical report.

        Notes:
            - Function builds out the PDF into individual pages stored as tuples like (plot, title) to pass back to the view for creating the PDF file response.

        Returns:
            - plot: The plot utilizing the data.
        """
        pages = list()
        degree_program = dprqs[0].degreeprogram.name
        for i in range(len(dprqs)//plots_per_page+1):
            slo_page = SLOStatusPage(dprqs=dprqs[i*plots_per_page:(i+1)*plots_per_page], plots_per_page=plots_per_page)
            slostatus_by_report = slo_page.slos_met_by_report_plotting()
            if slostatus_by_report:
                # slostatus_by_report = (slostatus_by_report, )
                pages.append((slostatus_by_report, f"SLO Status Breakdown by Report for {degree_program}"))
    
        if 'assessmentStats' in request.POST:
            assess_stats_page = AssessmentStatisticsPage(dprqs, sirqs, avirqs, plots_per_page=plots_per_page)
            assess_stats_by_report = assess_stats_page.assessment_stats_for_each_slo()
            if assess_stats_by_report:
                pages.append((assess_stats_by_report, f"Assessment Statistics by Report for {degree_program}"))
        return pages

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
            return (None, None, None, None)
        dprqs = MakereportsReport.objects.filter(
            Q(degreeprogram=mrdpqs[0]) &
            Q(year__lte=request.POST['date_end']) &
            Q(year__gte=request.POST['date_start'])
        )
        if len(dprqs) < 1:  # Degree program does not have a report associated with it.
            return (None,None,None,None)
        # SLOs in report queryset.
        sirqs = MakereportsSloinreport.objects.filter(report__in=dprqs)

        # SLOs in report status queryset. 
        sirsqs = MakereportsSlostatus.objects.filter(sloir__in=sirqs)
        # Assessment version in report query set.
        avirqs = MakereportsAssessmentversion.objects.filter(slo__in=sirqs)
        return dprqs, sirqs, sirsqs, avirqs

    def pdfDegreeAssessmentQuery(degree_id):
        """
        Queries to help with College Comparison Assessment Proficiency

        Queries from the MakereportsReport table -> MakereportsAssessmentversion table -> MakereportsAssessmentdata table.

        Returns:
            assessmentDataQS - The assessment data for the given degree_id
        """

        makeReportQS = MakereportsReport.objects.filter(degreeprogram=degree_id)
        if len(makeReportQS) < 1:  # Degree program does not have a report associated with it.
            return None
        
        reportsAssessmentVersionQS = MakereportsAssessmentversion.objects.filter(report__in=makeReportQS)
        
        assessmentDataQS = MakereportsAssessmentdata.objects.filter(assessmentversion__in=reportsAssessmentVersionQS)
        return assessmentDataQS

    def pdfCollegeComparisonsAssessmentPlotting(college_name):
        """
        Plots the college comparisons graphs for a given college name.

        Returns:
            - plot: The plot utilizing the data.
        """
        collegeQS = MakereportsCollege.objects.filter(name=college_name)
        if len(collegeQS) < 1:
            return None
        
        departmentQS = MakereportsDepartment.objects.filter(college__in=collegeQS)

        degreeProgramQS = MakereportsDegreeprogram.objects.filter(department__in=departmentQS)

        degree_programs = []
        overallProficiency = []

        for degree in degreeProgramQS:
            assessmentDataQS = PDFGenHelpers.pdfDegreeAssessmentQuery(degree)
            if assessmentDataQS is not None and len(assessmentDataQS) > 0 :
                degree_programs.append(degree.name)
                overallProficiency.append(assessmentDataQS[0].overallproficient)
                print("loop")
        
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

            return plt.savefig(str(BASE_DIR) + "/main/static/assessmentcomparisonfig.png")
        else:
            return None

    def pdfDegreeReportQuery(degree_id):
        """
        Queries to help with College Number of SLOs Comparison

        Queries from the MakereportsReport table.

        Returns:
            numOfSLOsDataQS - The number of SLOs for the given degree_id
        """
        makeReportQS = MakereportsReport.objects.filter(degreeprogram=degree_id)
        return makeReportQS
        
    def pdfCollegeComparisonsSLOPlotting(college_name):
        """
        Plots the college comparisons graphs for a given college name.

        Returns:
            - plot: The plot utilizing the data.
        """
        degree_programs = []
        numOfSLOs = []
        largestSLO = 0

        collegeQS = MakereportsCollege.objects.filter(name=college_name)
        if len(collegeQS) < 1:
            return None
        
        departmentQS = MakereportsDepartment.objects.filter(college__in=collegeQS)

        degreeProgramQS = MakereportsDegreeprogram.objects.filter(department__in=departmentQS)

        for degree in degreeProgramQS:
            reportDataQS = PDFGenHelpers.pdfDegreeReportQuery(degree)
            if reportDataQS is not None and len(reportDataQS) > 0 :
                degree_programs.append(degree.name)
                numOfSLOs.append(reportDataQS[0].numberofslos)
                if (largestSLO < reportDataQS[0].numberofslos):
                    largestSLO = reportDataQS[0].numberofslos
        
        df = pd.DataFrame(data = {
            'Programs' : degree_programs,
            'Number of SLOs' : numOfSLOs,
        })

        if (len(degree_programs) > 0):
            plot = sns.catplot(y="Programs", x="Number of SLOs",  kind="bar", data=df)
            plot.set(xlim=(0,largestSLO))
            
            #Start putting numbers above bar plots*******************************
            # extract the matplotlib axes_subplot objects from the FacetGrid
            ax = plot.facet_axis(0, 0)

            # iterate through the axes containers
            for c in ax.containers:
                labels = [f'{(v.get_width()):.0f}' for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            #End putting numbers above bar plots*********************************

            return plt.savefig(str(BASE_DIR) + "/main/static/slocomparisonfig.png")
        else:
            return None
