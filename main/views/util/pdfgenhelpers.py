from ...models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from AcademicAssessmentAssistant.settings import BASE_DIR

class PDFGenHelpers:

    def pdfGenQuery(degreeprogram_name):
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
        # print(dprqs)
        if len(dprqs) < 1:  # Degree program does not have a report associated with it.
            return (None,None,None)
        # SLOs in report queryset.
        sirqs = MakereportsSloinreport.objects.filter(report__in=dprqs)
        # SLOs in report status queryset. 
        sirsqs = MakereportsSlostatus.objects.filter(sloir__in=sirqs)
        return dprqs, sirqs, sirsqs

    def pdfGenPlotting(dprqs, sirqs, sirsqs):
        """
        Helper for plotting the resulting QuerySet from pdfGenQuery for our default report

        Returns:
            - plot: The plot utilizing the data.
        """
        possible_statuses = ['Met', 'Partially Met', 'Not Met', 'Unknown']
        degree_program = dprqs[0].degreeprogram.name
        statuses = [status.status for status in sirsqs]
        # pd.concat([df.col1.value_counts().reindex(possible_statuses[::-1], fill_value=0)
        df = pd.DataFrame(data = {
            'degree_program' : degree_program,
            'percent_total' : pd.Series(statuses).value_counts().reindex(possible_statuses, fill_value=0).divide(len(statuses)),
            'status' : possible_statuses
        })
        plot = sns.catplot(x="degree_program", y="percent_total", hue="status", kind="bar", data=df)
        plt.savefig(str(BASE_DIR) + "/main/static/testfig.png")
        