from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class HomePageTest(TestCase):

    def test_should_resolve_root_url_to_home_page_view(self):
        found_homepage = resolve('/')
        self.assertEqual(found_homepage.func, home_page)

    def test_should_use_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_should_save_POST_request(self):
        response = self.client.post('/', data={'item_text': 'New list item'})
        self.assertIn('New list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
