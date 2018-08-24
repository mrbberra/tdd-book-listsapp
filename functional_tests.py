from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_should_start_list_and_retreive_it_later(self):
        # JJ accesses the new To-Do list website
        self.browser.get('http://localhost:8000')
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
        input_box.send_keys('Go to home depot')
        input_box.send_keys(Keys.ENTER)
        # The page updates and JJ now sees a new list with her first to-do
        time.sleep(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Go to home depot', [row.text for row in rows])
        # JJ can still add more items
        self.fail('TODO: Finish Test')
        # JJ adds a second item to her list
        # JJ doesn't know how to access the list again from her other computer
        ### She sees a new URL has been generated, and the site explains it
        # JJ accesses the unique URL from her second computer and sees her items

if __name__ == '__main__':
    unittest.main(warnings='ignore')
