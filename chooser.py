from typing import Optional
from distracticat.emotes import kaomoji
import re

# Taken from https://stackoverflow.com/a/32640407
def int_to_en(num):
    """Given an int32 number, print it in English."""

    d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'nineteen', 20 : 'twenty',
          30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
          70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    assert(0 <= num)

    if (num < 20):
        return d[num]

    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] + ' ' + d[num % 10]

    if (num < k):
        if num % 100 == 0: return d[num // 100] + ' hundred'
        else: return d[num // 100] + ' hundred and ' + int_to_en(num % 100)

    if (num < m):
        if num % k == 0: return int_to_en(num // k) + ' thousand'
        else: return int_to_en(num // k) + ' thousand, ' + int_to_en(num % k)

    if (num < b):
        if (num % m) == 0: return int_to_en(num // m) + ' million'
        else: return int_to_en(num // m) + ' million, ' + int_to_en(num % m)

    if (num < t):
        if (num % b) == 0: return int_to_en(num // b) + ' billion'
        else: return int_to_en(num // b) + ' billion, ' + int_to_en(num % b)

    if (num % t == 0): return int_to_en(num // t) + ' trillion'
    else: return int_to_en(num // t) + ' trillion, ' + int_to_en(num % t)

    # raise AssertionError('num is too large: %s' % str(num))
    return str(num)


def parse_choices(choices_str: str) -> tuple[Optional[list], Optional[str]]:
    feedback = None

    choices = [ choice.strip() for choice in choices_str.split("or") ]

    if choices == ['', '']:
        feedback = "Or? Or what u silly??"
        choices = None

    elif choices == ['', '', '']:
        feedback = "Or or? Spit it out already!!"
        choices = None

    # only ors
    elif all(map(lambda x: x == '', choices)):
        num_ors = len(choices)-1

        facts = f"you said or {int_to_en(num_ors)} times and hrm... that means"

        if num_ors%2:
            facts += " the only real choice is just or!!"
            choices = ["or"]
        else:
            num_choosable_ors = (num_ors+1)//2
            perc_chance = "{:.0%}".format(1/(num_choosable_ors+1))
            facts += f" the only real choices are or and nothing! ..with a {perc_chance} chance of picking nothing hehe"
            choices = ["or"]*num_choosable_ors + ['']

        feedback = f"h..hey you aren't trying to confuse me are you ??? w..well it wont work!!! I know {facts} {kaomoji.confident()}"

    # only or and ?
    elif all(map(lambda x: re.match(r"^[\s\?]*$", x), choices)):
        # TODO add extra feedback
        pass

    # or and ? and other things
    else:
        # remove all empty entries and remove all-but-one empty entries after
        # the last non-empty
        should_add_empty = choices[-1] == ''
        choices = [ choice for choice in choices if choice != '']
        if (should_add_empty):
            choices += ['']

        # rstrip questions marks and whitespace from each choice only if there
        # are no question marks before the last non-whitespace-questionmark
        # character
        choices = list(map(
            lambda c: re.sub(r"[\s\?]+$", "", c)
            if re.match(r"^[^\?]+[\s\?]*$", c)
            else c, choices
        ))

    return choices, feedback

