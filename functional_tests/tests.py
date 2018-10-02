from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 5

class NewVisitorTest(StaticLiveServerTestCase):

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

    def test_should_allow_multiple_users_with_different_urls(self):
        # JJ starts a new to-do lists
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Measure bed dimensions')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Measure bed dimensions')
        # JJ sees that her new list has a unique url
        jj_list_url = self.browser.current_url
        self.assertRegex(jj_list_url, '/lists/.+')
        # Now Benji opens the site from his computer
        self.browser.quit()
        self.browser = webdriver.Firefox()
        # Benji arrives at the home page and sees none of JJ's items
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Measure bed dimensions', page_text)
        # Benji starts a list of his own by adding an item from the home page
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Find tailoring patterns')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Find tailoring patterns')
        # Benji gets his own unique url
        benji_list_url = self.browser.current_url
        self.assertRegex(benji_list_url, '/lists/.+')
        self.assertNotEqual(jj_list_url, benji_list_url)
        # On Benji's list's url, none of JJ's items show up
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Measure bed dimensions', page_text)
        self.assertIn('Find tailoring patterns', page_text)

    def test_should_load_layout_and_styling(self):
        # JJ navigates to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        # She sees the input box is centered
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
