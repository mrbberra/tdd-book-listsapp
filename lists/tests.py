from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

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

class ItemModelTest(TestCase):

    def test_should_save_and_retrieve_items(self):
        first_item = Item()
        first_item.text = 'Here\'s the first one!'
        first_item.save()

        second_item = Item()
        second_item.text = 'Strike two'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Here\'s the first one!')
        self.assertEqual(second_saved_item.text, 'Strike two')
