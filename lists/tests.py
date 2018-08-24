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

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New list item')

    def test_should_only_save_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_should_redirect_after_POST_request(self):
        response = self.client.post('/', data={'item_text': 'New list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_should_show_all_list_items(self):
        Item.objects.create(text='firstly, an item')
        Item.objects.create(text='secondly, another item')

        response = self.client.get('/')

        self.assertIn('firstly, an item', response.content.decode())
        self.assertIn('secondly, another item', response.content.decode())

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
