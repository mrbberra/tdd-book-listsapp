from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 5

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_table(self,row_text_expected):
        end_time = time.time() + MAX_WAIT
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text_expected, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() > end_time:
                    raise e
                time.sleep(.25)

    def test_should_start_list_and_retreive_it_later(self):
        # JJ accesses the new To-Do list website
        self.browser.get(self.live_server_url)
        # JJ sees the homepage, and confirms it's the site she wanted
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        # JJ can enter a new to-do item straight from the main homepage
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # JJ creates a new to-do item
        input_box.send_keys('Measure bed dimensions')
        input_box.send_keys(Keys.ENTER)
        # The page updates and JJ now sees a new list with her first to-do
        self.wait_for_row_in_table('1: Measure bed dimensions')
        # JJ can still add more items. She adds a second item to her list
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Go to home depot')
        input_box.send_keys(Keys.ENTER)
        # The second item appears once the page updates, and the first remains
        self.wait_for_row_in_table('1: Measure bed dimensions')
        self.wait_for_row_in_table('2: Go to home depot')
        # JJ doesn't know how to access the list again from her other computer
        # She sees a new URL has been generated, and the site explains it
        self.fail('TODO: Finish Test')
        # JJ accesses the unique URL from her second computer and sees her items
