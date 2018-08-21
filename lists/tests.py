from django.test import TestCase

class SmokeTest(TestCase):

    def test_should_fail_bad_math(self):
        self.assertEqual(1 + 1, 3)
