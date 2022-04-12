
from msilib.schema import Error
from django.shortcuts import render
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.messages import ERROR 
from main.models import \
    MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
    MakereportsSlostatus 
from AcademicAssessmentAssistant.settings import BASE_DIR
# Report Gen Imports
from django.http import FileResponse
from .util.pdfgenhelpers import PDFGenHelpers as pg
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
import io
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.pagesizes import letter


class PDFPage():
    """
    PDF Generation View
    """
    def display_pdfGen(request):
        ## DB query to retrieve usable info for this generated PDF
        dprqs, sirqs, sirsqs = pg.pdfGenQuery(request.POST['degree-program'], request)
        degree_program = request.POST['degree-program']
        department = MakereportsDepartment.objects.filter(id=request.POST['department'])[0]
        year_start = request.POST['date_start']
        year_end = request.POST['date_end']
        ## Generate the plot
        if any((dprqs, sirqs, sirsqs)):
            pg.pdfGenPlotting(dprqs, sirqs, sirsqs, request)
            

        ## PDF generation nonsense
        PAGE_WIDTH, PAGE_HEIGHT = letter
        buf = io.BytesIO()
        if not any((dprqs, sirqs, sirsqs)):
            print('here')
            buf.seek(0)
            return FileResponse(buf, as_attachment=True, filename=f"{department}-{degree_program}HistoricalReport.pdf")
        c = canvas.Canvas(buf, pagesize=letter)
        c.setTitle("{department}-{degree_program}HistoricalReport")
        styles = getSampleStyleSheet()
        f = Frame(inch, inch, 7*inch, 9*inch, showBoundary=0)
        styleN = styles['Normal']
        styleH1 = styles['Heading1']
        styleH2 = styles['Heading2']
        story = []
        story.append(Paragraph(f"Historical Data Report from {year_start} to {year_end} for {degree_program}", styleH2))
        f.addFromList(story, c)
        c.showPage()
        story.clear()
        toc = TableOfContents()
        story.append(toc)
        f.addFromList(story, c)
        c.showPage()
        story.clear()
        story.append(Paragraph(f"Percentage of Targets the {degree_program} Degree Program Meets", styleH1))
        c.drawInlineImage(str(BASE_DIR) + "/main/static/slo_status_by_reporting_year_fig.png", inch, inch, width=400, height=300)
        f.addFromList(story, c)
        c.save()
        buf.seek(0)

        # Return file to download to the user.
        return FileResponse(buf, as_attachment=True, filename=f"{department}-{degree_program}HistoricalReport.pdf")

    def display_degree_pdfGen(request):
        degree_program = request.POST['degree-program']
        degree_program2 = request.POST['degree-program2']
        
        # print("In display_degree_pdfGen")

        ## Generate the plot
        plot1HasData = True
        plot1 = pg.pdfCollegeComparisonsAssessmentPlotting("IS&T - College of Information Science & Technology")
        if plot1 == None:
            plot1 = False
        plot2HasData = True
        plot2 = pg.pdfCollegeComparisonsSLOPlotting("IS&T - College of Information Science & Technology")
        if plot2 == None:
            plot2 = False
        ## PDF generation nonsense
        PAGE_WIDTH, PAGE_HEIGHT = letter
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.setTitle(f"{degree_program} and {degree_program2} Comparison")
        styles = getSampleStyleSheet()
        # inch = 1
        f = Frame(inch, inch, 7*inch, 9*inch, showBoundary=0)
        styleN = styles['Normal']
        styleH1 = styles['Heading1']
        styleH2 = styles['Heading2']
        story = []
        story.append(Paragraph("College Comparison", styleH2))
        f.addFromList(story, c)
        # c.showPage()
        story.clear()
        # toc = TableOfContents()
        # story.append(toc)
        f.addFromList(story, c)
        # c.showPage()
        # story.clear()
        # story.append(Paragraph(f"Comparison of :  ", styleH1))
        if plot1HasData:
            c.drawImage(str(BASE_DIR) + "/main/static/assessmentcomparisonfig.png", inch, inch, width=300, height=300)
        if plot2HasData:
            c.drawImage(str(BASE_DIR) + "/main/static/slocomparisonfig.png", inch, inch+300, width=300, height=300)
        f.addFromList(story, c)
        c.save()
        buf.seek(0)

        # Return file to download to the user.
        return FileResponse(buf, as_attachment=True, filename=f"Comparison.pdf")
        
