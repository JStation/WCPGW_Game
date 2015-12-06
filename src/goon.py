import random


class Goon(object):
    """
    Name, skills, etc.
    """

    # todo: pull this data from goon.JSON
    first_names = ["Grim", "Savvy", "Henry", "Granny"]
    last_names = ["Hudson", "Midnight", "Samson", "Pendleton"]
    archetypes = {
        "Technician":"tech",
        "Hitman":"force",
        "Con Artist":"charm",
        "Burglar":"stealth"
    }
    goon_traits = ["tech", "stealth", "force", "charm"]

    def __init__(self, name=None):
        if name:
            self.name = name
        else:
            self.name = self.generateName()

        self.type = self.generateType()

        self.traits = self.generateTraits()


    def generateName(self):
        first = random.choice(self.first_names)
        last = random.choice(self.last_names)
        name = "%s %s" % (first.title(), last.title())
        return name

    def generateType(self):
        return random.choice(self.archetypes.keys())

    def generateTraits(self):
        primary_trait = self.archetypes[self.type]
        traits = set()
        traits.add(primary_trait)
        results = {}
        while (random.random() < .5):
            traits.add(random.choice(self.goon_traits))
        for t in traits:
            results[t] = random.randint(1,6)
        return results


    def __repr__(self):
        return self.name
