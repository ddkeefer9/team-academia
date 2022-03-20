from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from .models import \
        MakereportsReport, MakereportsSloinreport, MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus, \
        MakereportsSlostatus 
from AcademicAssessmentAssistant.settings import BASE_DIR
# Report Gen Imports
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.pagesizes import letter
from .util.pdfgenhelpers import PDFGenHelpers as pg
# Create your views here.

def index(request):
        departments = MakereportsDepartment.objects.all()
        degreePrograms = MakereportsDegreeprogram.objects.all()
        return render(
                request, 
                'home/home_page.html',
                {'showDepartments':departments,
                'showDegrees':degreePrograms},
        )
def smartAssistant(request):
        return render(
                request, 
                'smart_assistant/smart_assistant.html',
        )

def pdfGen(request):
        ## DB query to retrieve usable info for this generated PDF
        dprqs, sirqs, sirsqs = pg.pdfGenQuery(1)

        ## Generate the plot
        if any((dprqs, sirqs, sirsqs)):
                plot = pg.pdfGenPlotting(dprqs, sirqs, sirsqs)

        ## PDF generation nonsense
        PAGE_WIDTH, PAGE_HEIGHT = letter
        buf = io.BytesIO()
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
def sendDegrees(request):
        degreePrograms = MakereportsDegreeprogram.objects.filter(department=request.GET.get("department"))
        print(degreePrograms)
        return render(
                request,
                'home/degreeDropdown.html',
                {'degrees':degreePrograms},
        )