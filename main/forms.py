from django import forms
import datetime


class PdfForm(forms.Form):
    """
    PdfForm
        - department : The department to generate a report for.
        - degree_program : The degree program to generate a report for.
        - date_start : The start of the range of dates.
        - date_end : The end of the range of dates.
        - slo_and_assessment_stats : Include SLO and Assessment stats in the report.
        - num_slos_met : Number of SLOs met in a degree program.
        - targets_met : Number of targets met by each degree program. (*)
    Notes:
        - The targets met is only enabled when the degree program selected is "All Programs"
    """
    department = forms.ChoiceField()
    degree_program = forms.ChoiceField()
    YEAR_CHOICES = []
    for r in range(2015, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))
    date_start = forms.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    date_end = forms.IntegerField()
    SLO_and_Assessment_statistics = forms.BooleanField()
    number_of_SLOs_met = forms.BooleanField()
    targets_met = forms.BooleanField()