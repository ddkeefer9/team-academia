from asyncio.windows_events import NULL
from fileinput import filename
from operator import contains
from unicodedata import name
from django.test import TestCase
from django.test import LiveServerTestCase
from numpy import equal, number
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .models import MakereportsDepartment, MakereportsAnnouncement, MakereportsReport
from main.views.util.smart_assistant import SLO_Object, SmartAssistantHelper

from main.views.util.queries import CollegeQueries, DegreeQueries
from .models import MakereportsDepartment, MakereportsAnnouncement, MakereportsAssessment, DjangoSummernoteAttachment
from main.views.util.pdf_generation import AssessmentStatisticsPage, PDFGenHelpers as pg, SLOStatusPage
import time


import pytest
# Create your tests here.
pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class BasicTests(TestCase):
	pytestmark = pytest.mark.django_db

	def test_view_url_exists_at_desired_location(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_url_does_not_exist(self):
		response = self.client.get('/fake_site')
		self.assertEqual(response.status_code, 404)

	def test_url_admin(self):
		response = self.client.get('/admin')
		self.assertEqual(response.status_code, 301)

	def testButtonSmartFeedback_home(self):
		selenium = webdriver.Chrome('C:/bin/chromedriver.exe')
		#Choose your url to visit
		selenium.get('http://127.0.0.1:8000/')
		#find the elements you need to submit form
		# Obtain button by link text and click.
		selenium.find_element_by_xpath("//a[@type='submit' and @value='Feedback Smart Assistant']").click()
		#check result; page source looks at entire html document
		currentURL = selenium.current_url
		self.assertEqual(currentURL,"http://127.0.0.1:8000/smart_assistant")
		selenium.quit()

	def testButtonHistoricalData_home(self):
		selenium = webdriver.Chrome('C:/bin/chromedriver.exe')
		#Choose your url to visit
		selenium.get('http://127.0.0.1:8000/')
		#find the elements you need to submit form
		# Obtain button by link text and click.
		selenium.find_element_by_xpath("//a[@type='submit' and @value='View Historical Data']").click()
		#check result; page source looks at entire html document
		currentURL = selenium.current_url
		self.assertEqual(currentURL,"http://127.0.0.1:8000/historical")
		selenium.quit()

	def testButtonDegreeComparisons_home(self):
		selenium = webdriver.Chrome('C:/bin/chromedriver.exe')
		#Choose your url to visit
		selenium.get('http://127.0.0.1:8000/')
		#find the elements you need to submit form
		# Obtain button by link text and click.
		selenium.find_element_by_xpath("//a[@type='submit' and @value='View Degree Program Comparisons']").click()
		#check result; page source looks at entire html document
		currentURL = selenium.current_url
		self.assertEqual(currentURL,"http://127.0.0.1:8000/degree_comparison")
		selenium.quit()

	def testGeneratesPDF(self):
				selenium = webdriver.Chrome('C:/bin/chromedriver.exe')
				#Choose your url to visit
				selenium.get('http://127.0.0.1:8000/')
				selenium.find_element_by_link_text("View Historical Data").click()
				selenium.get('http://127.0.0.1:8000/historical')
				selenium.find_element_by_id("id_department").click()
				Select(selenium.find_element_by_id("id_department")).select_by_visible_text("Computer Science")
				time.sleep(1)
				selenium.find_element_by_id("id_degree-program").click()
				Select(selenium.find_element_by_id("id_degree-program")).select_by_visible_text("Computer Science")
				selenium.find_element_by_name("gen_pdf").click()
				selenium.get('file:///C:/~/Downloads/Computer%20Science-Computer%20ScienceHistoricalReport%20.pdf')
				currentURL = selenium.current_url
				self.assertTrue(currentURL.__contains__(".pdf"))
				selenium.quit()

	def testFeedbackAssistantTableNotEmpty(self):
			selenium = webdriver.Chrome('C:/bin/chromedriver.exe')
			selenium.get("http://127.0.0.1:8000/")
			selenium.find_element_by_link_text("Feedback Smart Assistant").click()
			selenium.get("http://127.0.0.1:8000/smart_assistant")
			selenium.find_element_by_id("id_department").click()
			Select(selenium.find_element_by_id("id_department")).select_by_visible_text("Computer Science")
			time.sleep(1)
			selenium.find_element_by_id("id_degree-program").click()
			Select(selenium.find_element_by_id("id_degree-program")).select_by_visible_text("Computer Science")
			selenium.find_element_by_name("smart_woptions").click()
			MakereportsReport.objects.filter()
			self.assertTrue(MakereportsReport.numberofslos != 0)
			#response = self.client.post('/smart_assistant/')
			#self.assertTrue(True if 'showSLOs' in response.context else False)
			selenium.quit()

	def testFeedbackAssistantTableEmpty(self):
			selenium = webdriver.Chrome('C:/bin/chromedriver.exe')
			selenium.get("http://127.0.0.1:8000/")
			selenium.find_element_by_link_text("Feedback Smart Assistant").click()
			selenium.get("http://127.0.0.1:8000/smart_assistant")
			selenium.find_element_by_id("id_department").click()
			Select(selenium.find_element_by_id("id_department")).select_by_visible_text("Psychology")
			time.sleep(1)
			selenium.find_element_by_id("id_degree-program").click()
			Select(selenium.find_element_by_id("id_degree-program")).select_by_visible_text("BA Psychology")
			selenium.find_element_by_name("smart_woptions").click()
			MakereportsReport.objects.filter()
			response = self.client.post('/smart_assistant/')
			self.assertTrue(True if 'showSLOs' not in response.context else False)
			selenium.quit()
	
    

class UnitTests(TestCase):

	def test_department_length(self):
		assert len(MakereportsDepartment.objects.all()) == 26

	def test_announcement_length(self):
		assert len(MakereportsAnnouncement.objects.all()) == 0

	def test_SLOStatus(self):
		page = SLOStatusPage(0 , 4)
		assert page.description == "SLO Status"
	
	def test_SLO_dprqs(self):
		page = SLOStatusPage(0 , 4)
		assert page.dprqs == 0
	
	def test_SLO_plots_per_page(self):
		page = SLOStatusPage(0 , 4)
		assert page.plots_per_page == 4

	def test_AssessmentStats(self):
		page = AssessmentStatisticsPage(0,4,0)
		assert page.description == "Assessment Statistics"
	
	def test_AssessmentStats_dprqs(self):
		page = SLOStatusPage(0 , 4)
		assert page.dprqs == 0
	
	def test_AssessmentStats_plots_per_page(self):
		page = SLOStatusPage(0 , 4)
		assert page.plots_per_page == 4

@pytest.mark.django_db
class DegreeComparisonQueriesTests(TestCase):
	pytestmark = pytest.mark.django_db

	def test_getCollegeQSFromID(self):
		collegeQS =CollegeQueries.getCollegeQSFromID(1)
		assert len(collegeQS) == 1
	
	def test_getDegreesFromCollegeQS(self):
		collegeQS = CollegeQueries.getCollegeQSFromID(1)
		degreeProgramQS = CollegeQueries.getDegreesFromCollegeQS(collegeQS)
		assert len(degreeProgramQS) > 0
	
	def test_pdfDegreeAssessmentQuery(self):
		assessmentDataQS = DegreeQueries.pdfDegreeAssessmentQuery(1)
		assert len(assessmentDataQS) > 0
	
	def test_pdfDegreeReportQuery(self):
		makeReportQS = DegreeQueries.pdfDegreeReportQuery(1)
		assert len(makeReportQS) > 0
	
	def test_pdfDegreeBloomQuery(self):
		sloBloomQS = DegreeQueries.pdfDegreeBloomQuery(1)
		assert len(sloBloomQS) > 0
