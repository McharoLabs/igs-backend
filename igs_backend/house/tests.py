from django.test import TestCase

class SimpleTestCase(TestCase):
    def test_basic_addition(self):
        """
        Test that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_string_concatenation(self):
        """
        Test that concatenating 'Hello' and ' World' results in 'Hello World'.
        """
        self.assertEqual('Hello' + ' World', 'Hello World')

    def test_list_length(self):
        """
        Test that the length of the list [1, 2, 3] is 3.
        """
        self.assertEqual(len([1, 2, 3]), 3)