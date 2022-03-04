#!/usr/bin/env python3

import unittest
import chooser

class TestChoiceParser(unittest.TestCase):

    def test_simple(self):
        choices = chooser.parse_choices("this or that?")
        self.assertIs(choices, ["this", "that"])

    def test_surrounding_whitespace(self):
        choices = chooser.parse_choices("  this  or that ?   ? ")
        self.assertIs(choices, ["this", "that"])

    def test_single_or(self):
        choices = chooser.parse_choices("or")
        self.assertIs(choices, ["or"])

    def test_two_or(self):
        choices = chooser.parse_choices("or or")
        self.assertIs(choices, ["or", ""])

    def test_three_or(self):
        choices = chooser.parse_choices("or or or")
        self.assertIs(choices, ["or", "or"])

    def test_four_or(self):
        choices = chooser.parse_choices("or or or or")
        self.assertIs(choices, ["or", "or", ""])

    def test_five_or(self):
        choices = chooser.parse_choices("or or or or or")
        self.assertIs(choices, ["or", "or", "or"])

    def test_only_question(self):
        choices = chooser.parse_choices("? or ?")
        self.assertIs(choices, ["?", "?"])

    def test_leading_question(self):
        choices = chooser.parse_choices("?ok??? or ?")
        self.assertIs(choices, ["?ok???", "?"])


if __name__ == '__main__':
    unittest.main()

