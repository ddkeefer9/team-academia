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
    year_dropdown = []
    for r in range(2015, (datetime.datetime.now().year+1)):
        year_dropdown.append((r,r))
    date_start = year = forms.ChoiceField(choices=year_dropdown)
    date_end = forms.ChoiceField(choices=year_dropdown, initial=datetime.datetime.now().year)