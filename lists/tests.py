from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):

    def test_should_use_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListAndItemModelsTest(TestCase):

    def test_should_save_and_retrieve_items(self):
        item_list = List()
        item_list.save()

        first_item = Item()
        first_item.text = 'Here\'s the first one!'
        first_item.list = item_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Strike two'
        second_item.list = item_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, item_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Here\'s the first one!')
        self.assertEqual(first_saved_item.list, item_list)
        self.assertEqual(second_saved_item.text, 'Strike two')
        self.assertEqual(second_saved_item.list, item_list)

class ListViewTest(TestCase):

    def test_should_use_list_template(self):
        response = self.client.get('/lists/only-list-that-exists/')
        self.assertTemplateUsed(response, 'list.html')

    def test_should_display_all_items(self):
        item_list = List.objects.create()
        Item.objects.create(text="First item", list=item_list)
        Item.objects.create(text="Second item", list=item_list)

        response = self.client.get('/lists/only-list-that-exists/')

        self.assertContains(response, "First item")
        self.assertContains(response, "Second item")

class NewListTest(TestCase):

    def test_should_save_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_should_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'New list item'})
        self.assertRedirects(response, '/lists/only-list-that-exists/')
