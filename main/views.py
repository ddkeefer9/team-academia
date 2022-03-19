from django.shortcuts import render
from django.http import HttpResponse
from .models import MakereportsSloinreport
from .models import MakereportsDegreeprogram
from .models import MakereportsDepartment
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
        # Constants for width and height to refer to later.
        PAGE_WIDTH, PAGE_HEIGHT = letter
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.setTitle("DefaultReport")
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading2']
        story = []

        # add some flowables
        story.append(Paragraph("Historical Data Report from YEAR to YEAR for PROGRAM", styleH))
        f = Frame(inch, inch, 7*inch, 9*inch, showBoundary=0)
        f.addFromList(story, c)
        c.showPage()
        story.clear()
        toc = TableOfContents()
        PS = ParagraphStyle
        toc.levelStyles = [
                PS(fontName='Helvetica', fontSize=14, name='TOCHeading1',
                leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=16),
                PS(fontSize=12, name='TOCHeading2',
                leftIndent=40, firstLineIndent=-20, spaceBefore=0, leading=12),
                PS(fontSize=10, name='TOCHeading3',
                leftIndent=60, firstLineIndent=-20, spaceBefore=0, leading=12),
                PS(fontSize=10, name='TOCHeading4',
                leftIndent=100, firstLineIndent=-20, spaceBefore=0, leading=12),
        ]
        # toc.addEntry(1, "Testing for the use of the table of contents", 1)
        toc.addEntry(0, "Test", 1, toc.levelStyles[0])
        print(toc._entries)
        story.append(toc)
        f = Frame(inch, inch, 7*inch, 9*inch, showBoundary=0)
        f.addFromList(story, c)
        c.save()
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename="DefaultReport.pdf")

