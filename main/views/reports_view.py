
from django.shortcuts import render
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
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
        dprqs, sirqs, sirsqs = pg.pdfGenQuery(request.POST['degree-program'])
        ## Generate the plot
        if any((dprqs, sirqs, sirsqs)):
            plot = pg.pdfGenPlotting(dprqs, sirqs, sirsqs)
            

        ## PDF generation nonsense
        PAGE_WIDTH, PAGE_HEIGHT = letter
        buf = io.BytesIO()
        if not any((dprqs, sirqs, sirsqs)):
            buf.seek(0)
            return FileResponse(buf, as_attachment=True, filename="DefaultReport.pdf")
        c = canvas.Canvas(buf, pagesize=letter)
        c.setTitle("DefaultReport")
        styles = getSampleStyleSheet()
        f = Frame(inch, inch, 7*inch, 9*inch, showBoundary=0)
        styleN = styles['Normal']
        styleH1 = styles['Heading1']
        styleH2 = styles['Heading2']
        story = []
        story.append(Paragraph("Historical Data Report from YEAR to YEAR for PROGRAM", styleH2))
        f.addFromList(story, c)
        c.showPage()
        story.clear()
        toc = TableOfContents()
        story.append(toc)
        f.addFromList(story, c)
        c.showPage()
        story.clear()
        story.append(Paragraph(f"Percentage of Targets the {dprqs[0].degreeprogram.name} Degree Program Meets", styleH1))
        c.drawInlineImage(str(BASE_DIR) + "/main/static/testfig.png", inch, inch, width=400, height=300)
        f.addFromList(story, c)
        c.save()
        buf.seek(0)

        # Return file to download to the user.
        return FileResponse(buf, as_attachment=True, filename="DefaultReport.pdf")

    def display_degree_pdfGen(request):
        degree_program = request.POST['degree-program']
        degree_program2 = request.POST['degree-program2']

        ## Generate the plot
        plot = pg.pdfDegreeGenPlotting(degree_program, degree_program2)

        ## PDF generation nonsense
        PAGE_WIDTH, PAGE_HEIGHT = letter
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.setTitle(f"{degree_program} and {degree_program2} Comparison")
        styles = getSampleStyleSheet()
        f = Frame(inch, inch, 7*inch, 9*inch, showBoundary=0)
        styleN = styles['Normal']
        styleH1 = styles['Heading1']
        styleH2 = styles['Heading2']
        story = []
        story.append(Paragraph("Program Comparison", styleH2))
        f.addFromList(story, c)
        c.showPage()
        story.clear()
        toc = TableOfContents()
        story.append(toc)
        f.addFromList(story, c)
        c.showPage()
        story.clear()
        story.append(Paragraph(f"Comparison of Proficiency between {degree_program} and {degree_program2}", styleH1))
        c.drawInlineImage(str(BASE_DIR) + "/main/static/degreetestfig.png", inch, inch, width=400, height=300)
        f.addFromList(story, c)
        c.save()
        buf.seek(0)

        # Return file to download to the user.
        return FileResponse(buf, as_attachment=True, filename=f"{degree_program} and {degree_program2} Comparison.pdf")
        
