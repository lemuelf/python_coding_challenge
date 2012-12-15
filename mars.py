#!/usr/bin/env python

import json
import os


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


if __name__ == "__main__":
    mars = Mars()

    try:
        mars.send("")
    except Exception as e:
        # also asserts that an exception is raised
        assert type(e) is Exception, \
            "send() with a non-dict argument did not raise an Exception"

    assert mars.send({"name": "marvin", "mission": "probe someone"}) == 1, \
        "successful send did not return 1"
    assert os.path.isfile(mars.filename), "file not created"

    assert type(mars.receive()) is dict, "receive() return value is not dict"

    os.unlink(mars.filename)
    assert os.path.exists(mars.filename) is False
    try:
        mars.receive()
    except Exception as e:
        # asserts that an exception is raised if the file doesn't exist
        assert type(e) is Exception, "exception type is not "

    fname = "./a_different_file.txt"
    mars = Mars(fname)
    mars.send({})
    assert os.path.isfile(fname), "file supplied in __init__ not created"
