import random


class Kaomoji:
    categories = {}

    with open("data/kaomoji.txt") as f:
        for line in f:
            category, sep, kaomoji = line.partition(":")
            try:
                categories[category].append(kaomoji)
            except KeyError:
                categories[category] = [kaomoji]

    @classmethod
    def confident(cls):
        return random.choice(cls.categories["confident"])


class Reactions:
    reactions = []
    noises = []

    with open("data/reactions.txt") as f:
        reactions = f.read().splitlines()

    with open("data/noises.txt") as f:
        noises = f.read().splitlines()

    @classmethod
    def reaction(cls):
        noise = random.choice(cls.noises)
        return random.choice(cls.reactions).replace("<noise>", noise)
