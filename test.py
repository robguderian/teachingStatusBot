import unittest
from userStatusBot import checkIsPersonTeaching, checkWhenIsPersonTeaching

class TestRegex(unittest.TestCase):

    def test_isTeaching(self):
        name = checkIsPersonTeaching("Is Robert teaching")
        # does a lower(), so...
        self.assertEqual(name, "robert")

    def test_whenTeaching(self):
        name = checkIsPersonTeaching("When Is Robert teaching")
        # does a lower(), so...
        self.assertEqual(name, "robert")

if __name__ == '__main__':
    unittest.main()

