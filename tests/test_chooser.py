#!/usr/bin/env python3

import pytest
from distracticat import chooser


def test_simple():
    choices = chooser.parse_choices("this or that?")
    assert choices is ["this", "that"]

def test_surrounding_whitespace():
    choices = chooser.parse_choices("  this  or that ?   ? ")
    assert choices is ["this", "that"]

def test_single_or():
    choices = chooser.parse_choices("or")
    assert choices is ["or"]

def test_two_or():
    choices = chooser.parse_choices("or or")
    assert choices is ["or", ""]

def test_three_or():
    choices = chooser.parse_choices("or or or")
    assert choices is ["or", "or"]

def test_four_or():
    choices = chooser.parse_choices("or or or or")
    assert choices is ["or", "or", ""]

def test_five_or():
    choices = chooser.parse_choices("or or or or or")
    assert choices is ["or", "or", "or"]

def test_only_question():
    choices = chooser.parse_choices("? or ?")
    assert choices is ["?", "?"]

def test_leading_question():
    choices = chooser.parse_choices("?ok??? or ?")
    assert choices is ["?ok???", "?"]


if __name__ == '__main__':
    pytest.main()

