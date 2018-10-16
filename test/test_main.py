#!/usr/bin/env python3 -O

import unittest

import main

class TestMain(unittest.TestCase):
    def test_something(self):
        self.assertEqual(main.return_something(), "something")
