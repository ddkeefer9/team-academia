from django.test import TestCase
import pytest
# Create your tests here.
class BasicTests(TestCase):
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