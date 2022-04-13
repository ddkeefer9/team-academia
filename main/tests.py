from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .models import MakereportsDepartment, MakereportsAnnouncement

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

class UnitTests(TestCase):

	def test_department_length(self):
		assert len(MakereportsDepartment.objects.all()) == 26

	def test_announcement_length(self):
		assert len(MakereportsAnnouncement.objects.all()) == 0