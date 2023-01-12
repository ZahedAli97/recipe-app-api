"""
Sample tests
"""

from django.test import SimpleTestCase
from app import calc


class calcTests(SimpleTestCase):
    """Test the calc module"""

    def test_add_numbers(self):  # always start with test
        """Test adding numbers together"""
        res = calc.add(2, 3)

        self.assertEqual(res, 5)

    def test_subtract_numbers(self):
        """Test subtracting numbers"""
        res = calc.subtract(10, 15)

        self.assertEqual(res, 5)
