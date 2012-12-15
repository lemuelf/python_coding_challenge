#!/usr/bin/env python

import json
import os
import sys
import unittest


class Mars:
    def __init__(self, filename="./martian_spaceship.json"):
        self.filename = filename

    def send(self, martians):
        if type(martians) is not dict:
            # TypeError would probably be more appropriate
            raise Exception("martians not dict, is: %s" % type(martians))

        try:
            with open(self.filename, 'w') as f:
                json.dump(martians, f)
        except Exception as e:
            # wrap whatever specific Exception in a (general) Exception
            # because that's what the instruction said.
            raise Exception("%s: %s" % (type(e), e.args))
        else:
            return 1

    def receive(self):
        try:
            with open(self.filename) as f:
                return json.load(f)
        except Exception as e:
            # wrap whatever specific Exception in a (general) Exception
            # because that's what the instruction said.
            raise Exception("%s: %s" % (type(e), e.args))


class TestMars(unittest.TestCase):
    def setUp(self):
        self.mars = Mars()

    def tearDown(self):
        if os.path.isfile(self.mars.filename):
            os.unlink(self.mars.filename)

    def test_file_passed_in_init_is_the_file_being_worked_on(self):
        fname = "./a_different_file.txt"
        mars = Mars(fname)
        mars.send({})
        self.assertTrue(os.path.isfile(fname),
                        "file supplied in __init__ not created")

    def test_send_raises_an_exception_if_passed_with_non_dict(self):
        self.assertRaises(Exception, self.mars.send, "")

    def test_send_returns_1_on_success(self):
        self.assertEqual(
            1, self.mars.send({"name": "marvin", "mission": "probe someone"}),
            "successful send did not return 1"
        )

    def test_send_writes_a_json_file(self):
        self.mars.send({})
        self.assertTrue(os.path.isfile(self.mars.filename), "file not created")

    def test_receive_raises_an_exception_if_json_file_doesnt_exist(self):
        self.assertRaises(Exception, self.mars.receive)

    def test_receive_returns_a_dict(self):
        self.mars.send({})
        if sys.version_info >= (2, 7):
            self.assertIs(type(self.mars.receive()), dict,
                          "receive() return value is not dict")
        else:
            self.assertTrue(type(self.mars.receive()) is dict,
                            "receive() return value is not dict")


if __name__ == "__main__":
    if sys.version_info >= (2, 7):
        unittest.main(exit=False)
    else:
        try:
            unittest.main()
        except SystemExit:
            pass

    mars = Mars()
    mars.send({"name": "Marvin", "mission": "probe someone"})
    with open(mars.filename) as f:
        print f.readlines()

    for key, value in mars.receive().iteritems():
        print "%s: %s" % (key, value)
