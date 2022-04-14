from django.shortcuts import redirect
from django.http import FileResponse
from django.contrib import messages
from main.models import MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus

from AcademicAssessmentAssistant.settings import BASE_DIR
# Report Gen Imports
from django.http import FileResponse
from .util.pdf_generation import PDFGenHelpers as pg
import io
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.pagesizes import letter


class PDFPage():
    """
    PDF Generation View
    """

    def finish_page(story, c, f):
        f.addFromList(story, c)
        f._reset()
        c.showPage()
        story.clear()
        return story

    def draw_historical_report_body(story, canvas, frame, pages):
        styles = getSampleStyleSheet()
        styleH1 = styles['Heading1']
        styleH3 = styles['Heading3']
        for (page_plot, page_descriptions), page_title in pages:
            story.append(Paragraph(page_title, styleH1))
            for description, style in page_descriptions:
                if isinstance(description, list):
                    for i in range(len(description)):
                        story.append(Paragraph(description[i], style=styles[style[i]]))
                        story.append(Spacer(7*inch, 0.2*inch))
                else:
                    story.append(Paragraph(description, styles[style]))
            if isinstance(page_plot, str):
                # Then the "plot" is actually a string saying that the degree program has no status data.
                story.append(Paragraph(page_plot, styleH3))
                story = PDFPage.finish_page(story, canvas, frame)
                continue
            width, height = page_plot.size
            canvas.drawInlineImage(page_plot, inch, inch, width=0.5*width, height=0.5*height)
            page_plot.close()
            story = PDFPage.finish_page(story, canvas, frame)

    def display_historical_pdfGen(request):
        ## DB query to retrieve usable info for this generated PDF
        department = MakereportsDepartment.objects.filter(id=request.POST['department'])
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        styles = getSampleStyleSheet()
        styleTitle = styles['Title']
        story = []
        f = Frame(inch, inch, 7*inch, 9*inch, showBoundary=0)

        degree_program = request.POST['degree-program']
        year_start = request.POST['date_start']
        year_end = request.POST['date_end']
        # For all programs option, if all True then the entire department does not contain data, triggering a warning later on in this function.
        nodata_degree_bool_mask = []

        if request.POST['degree-program'] == "All Programs":
            degree_programs = MakereportsDegreeprogram.objects.filter(department__in=department)
            story.append(Paragraph(f"Historical Data Report from {year_start} to {year_end} for All Programs in the {department[0]} Department", styleTitle))
            PDFPage.finish_page(story, c, f)
            for degree in degree_programs:
                dprqs, sirqs, sirsqs, avirqs = pg.historicalPdfGenQuery(degree, request)
                ## Generate the plot
                if any((dprqs, sirqs)):
                    pages = pg.historicalPdfGenPlotting(dprqs, sirqs, sirsqs, avirqs, request)

                # Instead of warning display, just continue to next degree program.   
                if not any((dprqs, sirqs)):
                    nodata_degree_bool_mask.append(True)
                    continue
                else:
                    nodata_degree_bool_mask.append(False)

                c.setTitle(f"{department[0]}HistoricalReport")
                PDFPage.draw_historical_report_body(story, c, f, pages)
        else:
            dprqs, sirqs, sirsqs, avirqs = pg.historicalPdfGenQuery(request.POST['degree-program'], request)

            ## Generate the plot
            if any((dprqs, sirqs)):
                pages = pg.historicalPdfGenPlotting(dprqs, sirqs, sirsqs, avirqs, request) 

            if not any((dprqs, sirqs)):
                buf.seek(0)
                messages.warning(request, message=f'No data found for {degree_program} in years between {year_start} and {year_end}')
                return redirect('historical')

            c.setTitle(f"{department[0]}-{degree_program}HistoricalReport")
            story.append(Paragraph(f"Historical Data Report from {year_start} to {year_end} for {degree_program}", styleTitle))
            story = PDFPage.finish_page(story, c, f)

            PDFPage.draw_historical_report_body(story, c, f, pages)

        if nodata_degree_bool_mask and all(nodata_degree_bool_mask):
            buf.seek(0)
            messages.warning(request, message=f'No data found for All Programs in years between {year_start} and {year_end}')
            return redirect('historical')
        c.save()
        buf.seek(0)

        # Return file to download to the user.
        return FileResponse(buf, as_attachment=True, filename=f"{department[0]}-{degree_program}HistoricalReport.pdf")

    def display_degree_pdfGen(request):
        degree_program = request.POST['degree-program']
        degree_program2 = request.POST['degree-program2']
        ## Generate the plot
        plot1HasData = True
        plot1 = pg.pdfCollegeComparisonsAssessmentPlotting("IS&T - College of Information Science & Technology")
        if plot1 == None:
            plot1 = False
        plot2HasData = True
        plot2 = pg.pdfCollegeComparisonsSLOPlotting("IS&T - College of Information Science & Technology")
        if plot2 == None:
            plot2 = False
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
        
