from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pytest
# Create your tests here.
pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class BasicTests(TestCase):
	pytestmark = pytest.mark.django_db

	def test_example(self):
		assert 1 == 1

	def test_view_url_exists_at_desired_location(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_url_does_not_exist(self):
		response = self.client.get('/fake_site')
		self.assertEqual(response.status_code, 404)

	def test_url_admin(self):
		response = self.client.get('/admin')
		self.assertEqual(response.status_code, 301)


	def testButtonSmartFeedback(self):
		selenium = webdriver.Chrome('C:/bin/chromedriver.exe')
		#Choose your url to visit
		selenium.get('http://127.0.0.1:8000/')
		#find the elements you need to submit form
		# Obtain button by link text and click.
		selenium.find_element_by_xpath("//a[@type='button' and @value='Smart']").click()
		#check result; page source looks at entire html document
		currentURL = selenium.current_url
		self.assertEqual(currentURL,"http://127.0.0.1:8000/smartAssistant")
		selenium.quit()

	def testButtonHistoricalData(self):
		selenium = webdriver.Chrome('C:/bin/chromedriver.exe')
		#Choose your url to visit
		selenium.get('http://127.0.0.1:8000/')
		#find the elements you need to submit form
		# Obtain button by link text and click.
		selenium.find_element_by_xpath("//a[@type='button' and @value='Hist']").click()
		#check result; page source looks at entire html document
		currentURL = selenium.current_url
		self.assertEqual(currentURL,"http://127.0.0.1:8000/historical")
		selenium.quit()

