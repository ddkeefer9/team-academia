
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
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
    def display_historical_pdfGen(request):
        ## DB query to retrieve usable info for this generated PDF
        dprqs, sirqs, sirsqs = pg.historicalPdfGenQuery(request.POST['degree-program'], request)
        degree_program = request.POST['degree-program']
        department = MakereportsDepartment.objects.filter(id=request.POST['department'])[0]
        year_start = request.POST['date_start']
        year_end = request.POST['date_end']
        ## Generate the plot
        if any((dprqs, sirqs, sirsqs)):
            plots = pg.historicalPdfGenPlotting(dprqs, sirqs, sirsqs, request)
            

        ## PDF generation nonsense
        PAGE_WIDTH, PAGE_HEIGHT = letter
        buf = io.BytesIO()
        if not any((dprqs, sirqs, sirsqs)):
            buf.seek(0)
            messages.warning(request, message=f'No data found for {degree_program}')
            return redirect('historical')
        c = canvas.Canvas(buf, pagesize=letter)
        c.setTitle(f"{department}-{degree_program}HistoricalReport")
        styles = getSampleStyleSheet()
        f = Frame(inch, inch, 7*inch, 9*inch, showBoundary=0)
        styleN = styles['Normal']
        styleH1 = styles['Heading1']
        styleH2 = styles['Heading2']
        styleH3 = styles['Heading3']
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
        story.append(Paragraph(f"SLO Status Breakdown by Report for {degree_program}", styleH1))
        for plot in plots:
            if isinstance(plot, str):
                # Then the "plot" is actually a string saying that the degree program has no status data.
                story.append(Paragraph(plot, styleH3))
                continue
            c.drawInlineImage(plot, inch, inch, width=400, height=300)
            plot.close()
        f.addFromList(story, c)
        c.save()
        buf.seek(0)

        # Return file to download to the user.
        return FileResponse(buf, as_attachment=True, filename=f"{department}-{degree_program}HistoricalReport.pdf")

    def display_degree_pdfGen(request):
        degree_program = request.POST['degree-program']
        degree_program2 = request.POST['degree-program2']

        ## Generate the plot
        plot = pg.pdfCollegeComparisonsPlotting(degree_program, degree_program2)

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
        
