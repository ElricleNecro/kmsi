#!/usr/bin/env python
# encoding: utf-8

""".. module:: exception
    Contain all the error handling stuff.
"""

class SendError(Exception):
    def __init__(self, error, ret, config):
        self.message = error
        self.value = ret
        self.config = config

    def __str__(self):
        return "Error (" + repr(self.value) + ") while sending request:" + self.message + "\n" + repr(self.config)
