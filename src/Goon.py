import random

class Goon(object):
    """
    Name, skills, etc.
    """
    first_names = ["Grim", "Savvy", "Henry", "Granny"]
    last_names = ["Hudson", "Midnight", "Samson", "Pendleton"]
    archetypes = ["Con Artist", "Hitman", "Technician", "Burglar"]

    def __init__(self, name=None):
        if name:
            self.name = name
        else:
            self.name = self.generateName()

        self.type = self.generateType()

        self.skills = {
            "tech":1,
            "force":1,
            "charm":4,
            "stealth":3,
        }


    def generateName(self):
        first = random.choice(self.first_names)
        last = random.choice(self.last_names)
        name = "%s %s" % (first.title(), last.title())
        return name

    def generateType(self):
        return random.choice(self.archetypes)

    def __repr__(self):
        return self.name