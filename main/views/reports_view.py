from operator import contains
from django.shortcuts import redirect
from django.http import FileResponse
from django.contrib import messages
from main.models import MakereportsDegreeprogram, MakereportsDepartment, MakereportsSlostatus

from AcademicAssessmentAssistant.settings import BASE_DIR
# Report Gen Imports
from django.http import FileResponse

from main.views.util.queries import CollegeQueries
from .util.pdf_generation import DegreeComparisonPlotting, PDFGenHelpers as pg
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
        """
        A helper function for the 'draw_historical_report_body' function that finishes a page and resets the input parameters.
        
        Returns
            - A cleared ReportLab 'story'.
        """
        f.addFromList(story, c)
        f._reset()
        c.showPage()
        story.clear()
        return story

    def draw_historical_report_body(story, canvas, frame, pages):
        """
        A helper function for the 'display_historical_pdfGen' function that handles the ReportLab logic for formatting the body of the requested pages.
        """
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
        """
        The main function for handling a POST request to create a historical PDF for a given department or departments.

        Returns
            - A FileResponse with the generated PDF, OR
            - A redirect to the page with a warning if no data is available.
        """
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
                dprqs, sirqs = pg.historicalPdfGenQuery(degree, request)
                ## Generate the plot
                if any((dprqs, sirqs)):
                    pages = pg.historicalPdfGenPlotting(dprqs, request)

                # Instead of warning display, just continue to next degree program.   
                if not any((dprqs, sirqs)):
                    nodata_degree_bool_mask.append(True)
                    continue
                else:
                    nodata_degree_bool_mask.append(False)

                c.setTitle(f"{department[0]}HistoricalReport")
                PDFPage.draw_historical_report_body(story, c, f, pages)
        else:
            dprqs, sirqs = pg.historicalPdfGenQuery(request.POST['degree-program'], request)

            ## Generate the plot
            if any((dprqs, sirqs)):
                pages = pg.historicalPdfGenPlotting(dprqs, request) 

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
        collegeID = request.POST['college']
        collegeQS = CollegeQueries.getCollegeQSFromID(collegeID)
        collegeName = collegeQS[0].name
        ## Generate the plot
        plot1HasData = True
        plot1 = DegreeComparisonPlotting.pdfCollegeComparisonsAssessmentPlotting(collegeQS)
        if plot1 is None:
            plot1HasData = False
        plot2HasData = True
        plot2 = DegreeComparisonPlotting.pdfCollegeComparisonsSLOPlotting(collegeQS)
        if plot2 is None:
            plot2HasData = False
        plot3HasData = True
        plot3 = DegreeComparisonPlotting.pdfCollegeComparisonsBloomPlotting(collegeQS)
        if plot3 == None:
            plot3HasData = False
        plot4HasData = True
        plot4 = DegreeComparisonPlotting.pdfCollegeComparisonsCosineSimilarityPlotting(collegeQS)
        if plot4 == None:
            plot4HasData = False
        PAGE_WIDTH, PAGE_HEIGHT = letter
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.setTitle(f"{collegeName} Comparison")
        styles = getSampleStyleSheet()
        # inch = 1
        f = Frame(inch, inch, 7*inch, 9*inch, showBoundary=0)
        styleN = styles['Normal']
        styleH1 = styles['Heading1']
        styleH2 = styles['Heading2']
        story = []
        story.append(Paragraph(f"{collegeName} Comparison", styleH2))
        f.addFromList(story, c)
        # c.showPage()
        story.clear()
        # toc = TableOfContents()
        # story.append(toc)
        f.addFromList(story, c)
        # c.showPage()
        # story.clear()
        # story.append(Paragraph(f"Comparison of :  ", styleH1))
        if plot1HasData is True:
            textobject = c.beginText()
            textobject.setFont('Times-Roman', 15)
            textobject.setTextOrigin(inch, inch+243)

            textobject.textLine(text = "Overall Proficiency For A Program:")
            c.drawText(textobject)
            c.drawImage(str(BASE_DIR) + "/main/static/assessmentcomparisonfig.png", inch, inch-60, width=300, height=300, preserveAspectRatio=True)
        else:
            textobject = c.beginText()
            textobject.setFont('Times-Roman', 12)
            textobject.setTextOrigin(inch, inch+150)

            textobject.textLine(text = 'No Data For Assessment Comparison Graph')
            c.drawText(textobject)
            # story.append((f"No Data For Assessment Comparison", styleH2))
        if plot2HasData is True:
            textobject = c.beginText()
            textobject.setFont('Times-Roman', 15)
            textobject.setTextOrigin(inch, inch+565)

            textobject.textLine(text = "Number Of SLOs For A Program:")
            c.drawText(textobject)
            c.drawImage(str(BASE_DIR) + "/main/static/slocomparisonfig.png", inch, inch+260, width=300, height=300, preserveAspectRatio=True)
        else:
            textobject = c.beginText()
            textobject.setFont('Times-Roman', 12)
            textobject.setTextOrigin(inch, inch+450)

            textobject.textLine(text = 'No Data For Number of SLOs Comparison Graph')
            c.drawText(textobject)
        c.showPage()
        if plot3HasData:
            textobject = c.beginText()
            textobject.setFont('Times-Roman', 15)
            textobject.setTextOrigin(inch, inch+600)

            textobject.textLine(text = "Bloom Taxonomies Used For A Program:")
            c.drawText(textobject)
            c.drawImage(str(BASE_DIR) + "/main/static/slobloomcomparisonfig.png", inch, inch+250, width=400, preserveAspectRatio=True)
        else:
            textobject = c.beginText()
            textobject.setFont('Times-Roman', 12)
            textobject.setTextOrigin(inch, inch+600)

            textobject.textLine(text = 'No Data For Blooms Taxonomy Comparison Graph')
            c.drawText(textobject)
        if plot4HasData:
            textobject = c.beginText()
            textobject.setFont('Times-Roman', 15)
            textobject.setTextOrigin(inch, inch+330)

            textobject.textLine(text = "SLO Text Similarity When Programs X SLO(s) Are Compared to Programs Y SLO(s):")
            c.drawText(textobject)
            c.drawImage(str(BASE_DIR) + "/main/static/similaritycomparisonfig.png", inch, inch-90, height=415, width=520)
        else:
            textobject = c.beginText()
            textobject.setFont('Times-Roman', 12)
            textobject.setTextOrigin(inch, inch+300)

            textobject.textLine(text = 'No Data For SLO Similarity Comparison Graph')
            c.drawText(textobject)
        f.addFromList(story, c)
        c.save()
        buf.seek(0)

        # Return file to download to the user.
        return FileResponse(buf, as_attachment=True, filename=f"{collegeName} Comparison.pdf")
        
