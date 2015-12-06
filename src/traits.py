import random


class Trait(object):
    def __init__(self, trait, value):
        self._trait = trait
        self._value = value

    @property
    def trait(self):
        return self._trait

    @property
    def value(self):
        return self._value

    def __add__(self, other):
        if isinstance(other, Trait):
            self._value += other.value
        else:
            self._value += other

    def __eq__(self, other):
        return self.trait == other.trait


class TraitRequirement(object):
    """
    Max can be 0, in which case we always return min
    This allows us to have flat requirements on some things
    """

    def __init__(self, trait, min, max):
        self._trait = trait
        self._min = int(min)
        self._max = int(max)

    def roll(self):
        if self._max == 0:
            return self._min
        else:
            return random.randint(self._min, self._max)

    @classmethod
    def list_from_json(cls, json_data):
        traits = []

        for t,r in json_data.items():
            if isinstance(r, int):
                trait = cls(t, r, 0)
            else:
                trait = cls(t, *r.split('-'))
            traits.append(trait)

        return traits
