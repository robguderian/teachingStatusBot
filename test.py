import unittest
from userStatusBot import checkIsPersonTeaching, checkWhenIsPersonTeaching

class TestRegex(unittest.TestCase):
    # does a lower(), so all test have to check the lower-casing

    def setUp(self):
        f = open("teaching_status_config.json.unittest")
        self.config = json.load(f)

    def test_isTeaching(self):
        name = checkIsPersonTeaching("Is Robert teaching")
        self.assertEqual(name, "robert")
        name = checkIsPersonTeaching("Is Robert teaching?")
        self.assertEqual(name, "robert")

        name = checkIsPersonTeaching("Is Robert G teaching?")
        self.assertEqual(name, "robert g")


        # consideration for future releases
        name = checkIsPersonTeaching("do you think that Robert teaching?")
        self.assertIsNone(name)

    def test_whenTeaching(self):
        name = checkIsPersonTeaching("When Is Robert teaching")
        self.assertEqual(name, "robert")
        name = checkIsPersonTeaching("When Is Robert teaching?")
        self.assertEqual(name, "robert")
        name = checkIsPersonTeaching("When Is Robert g teaching?")
        self.assertEqual(name, "robert g")



if __name__ == '__main__':
    unittest.main()

