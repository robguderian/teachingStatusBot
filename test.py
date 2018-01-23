import unittest
from userStatusBot import *

class TestRegex(unittest.TestCase):
    # does a lower(), so all test have to check the lower-casing

    def setUp(self):
        f = open("teaching_status_config.json.unittest")
        self.config = json.load(f)
        f = open("database.json.unittest")
        self.database = json.load(f)

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

    def test_isPersonTeaching(self):
        name = checkDoesPersonTeachToday("does Robert teach today")
        self.assertEquals(name, 'robert')

    def test_WhenDoesPersonTeach(self):
        name = checkWhenDoesPersonTeach("when does Robert teach")
        self.assertEquals(name, 'robert')


class TestUserMatching(unittest.TestCase):
    def setUp(self):
        f = open("teaching_status_config.json.unittest")
        self.config = json.load(f)
        f = open("database.json.unittest")
        self.database = json.load(f)

    def test_name_matching(self):
        # 2 roberts in test file
        names = nameMatch("robert", self.database)
        self.assertEquals( len(names), 2)
        names = nameMatch("robert guderian", self.database)
        self.assertEquals( len(names), 1)

        # 1 franklin, check values
        names = nameMatch("franklin", self.database)
        self.assertEquals( len(names), 1)
        self.assertEquals(names[0]['firstname'], "Franklin")
        self.assertEquals(names[0]['lastname'], "Bristow")


    def test_no_match(self):
        names = nameMatch("robertdddddd", self.database)
        self.assertIsNone(names)



if __name__ == '__main__':
    unittest.main()

