from django.test.testcases import TestCase
from ..utils import camelcase_to_separated_lowercase

class UtilsTestCase(TestCase):
    def test_camelcase_to_separated_lowercase(self):
        self.assertEqual(camelcase_to_separated_lowercase('SomeCameCasedString', '-'), 'some-came-cased-string')
