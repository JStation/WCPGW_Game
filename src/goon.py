import random


class Goon(object):
    """
    Name, skills, etc.
    """


    def __init__(self):
        # class data set by get_goon_data in Game class
        self.first_names = self.goon_data["first_names"]
        self.last_names = self.goon_data["last_names"]
        self.archetypes = self.goon_data["archetypes"]
        self.goon_traits = self.goon_data["goon_traits"]


        # generate unique attributes for goon instance
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
