import unittest
from userStatusBot import checkIsPersonTeaching, checkWhenIsPersonTeaching

class TestRegex(unittest.TestCase):
    # does a lower(), so all test have to check the lower-casing

    def test_isTeaching(self):
        name = checkIsPersonTeaching("Is Robert teaching")
        self.assertEqual(name, "robert")
        name = checkIsPersonTeaching("Is Robert teaching?")
        self.assertEqual(name, "robert")

        # consideration for future releases
        name = checkIsPersonTeaching("do you think that Robert teaching?")
        self.assertIsNone(name)

    def test_whenTeaching(self):
        name = checkIsPersonTeaching("When Is Robert teaching")
        self.assertEqual(name, "robert")
        name = checkIsPersonTeaching("When Is Robert teaching?")
        self.assertEqual(name, "robert")


if __name__ == '__main__':
    unittest.main()

