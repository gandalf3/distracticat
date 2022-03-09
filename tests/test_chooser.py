#!/usr/bin/env python3

import pytest
from distracticat import chooser


def test_simple():
    choices, feedback = chooser.parse_choices("this or that?")
    assert choices == ["this", "that"]
    assert feedback is None

def test_surrounding_whitespace():
    choices, feedback = chooser.parse_choices("  this  or that ?   ? ")
    assert choices == ["this", "that"]
    assert feedback is None

def test_single_or():
    choices, feedback = chooser.parse_choices("or")
    assert choices is None
    assert feedback is not None

def test_two_or():
    choices, feedback = chooser.parse_choices("or or")
    assert choices is None
    assert feedback is not None

def test_three_or():
    choices, feedback = chooser.parse_choices("or or or")
    assert choices == ["or"]
    assert feedback is not None

def test_four_or():
    choices, feedback = chooser.parse_choices("or or or or")
    assert choices == ["or", "or", ""]
    assert feedback is not None

def test_five_or():
    choices, feedback = chooser.parse_choices("or or or or or")
    assert choices == ["or"]
    assert feedback is not None

def test_weird_or():
    choices, feedback = chooser.parse_choices("or thing or")
    assert choices == ["thing", ""]
    assert feedback is None

def test_weird_or2():
    choices, feedback = chooser.parse_choices("or or thing or")
    assert choices == ["thing", ""]
    assert feedback is None

def test_weird_or3():
    choices, feedback = chooser.parse_choices("or or or thing or")
    assert choices == ["thing", ""]
    assert feedback is None

def test_weird_or4():
    choices, feedback = chooser.parse_choices("or thing or or or")
    assert choices == ["thing", ""]
    assert feedback is None

def test_only_question():
    choices, feedback = chooser.parse_choices("? or ?")
    assert choices == ["?", "?"]
    assert feedback is None

def test_leading_question():
    choices, feedback = chooser.parse_choices("?ok??? or ?")
    assert choices == ["?ok???", "?"]
    assert feedback is None

def test_spaced_question():
    choices, feedback = chooser.parse_choices("ok? ?")
    assert choices == ["ok"]
    assert feedback is None

def test_internal_question():
    choices, feedback = chooser.parse_choices("o?k? ?")
    assert choices == ["o?k? ?"]
    assert feedback is None

def test_multi_question():
    choices, feedback = chooser.parse_choices("??? or ??")
    assert choices == ["???", "??"]
    assert feedback is None

def test_single_question():
    choices, feedback = chooser.parse_choices("?")
    assert choices == ["?"]
    assert feedback is None

def test_internal_space():
    choices, feedback = chooser.parse_choices("meow meow? or pie")
    assert choices == ["meow meow", "pie"]
    assert feedback is None



if __name__ == '__main__':
    pytest.main()

