from selenium import webdriver
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
        assert 'To-Do' in self.browser.title

        # JJ can enter a new to-do item straight from the main homepage
        # JJ creates a new to-do item
        # The page updates and JJ now sees a new list with her first to-do
        # JJ can still add more items
        # JJ adds a second item to her list
        # JJ doesn't know how to access the list again from her other computer
        ### She sees a new URL has been generated, and the site explains it
        # JJ accesses the unique URL from her second computer and sees her items

if __name__ == '__main__':
    unittest.main(warnings='ignore')
