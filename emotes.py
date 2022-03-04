import random

class kaomoji:
    categories = {}

    with open("kaomoji.txt") as f:
        for line in f:
            category, sep, kaomoji = line.partition(":")
            try:
                categories[category].append(kaomoji)
            except KeyError:
                categories[category] = [kaomoji]

    @classmethod
    def confident(cls):
        return random.choice(cls.categories["confident"])
