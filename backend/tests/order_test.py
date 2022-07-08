import unittest

def addTwoNumbers(a, b):
    return a + b


class TestAddTwoNumbers(unittest.TestCase):
    def test_add_two_numbers(self):
        self.assertEqual(addTwoNumbers(1, 2), 3)
        self.assertEqual(addTwoNumbers(2, 2), 4)
        self.assertEqual(addTwoNumbers(3, 2), 5)