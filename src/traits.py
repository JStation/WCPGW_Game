import random


class TraitList(object):
    def __init__(self):
        self._traits = set()

    @property
    def traits(self):
        return self._traits

    def reset(self):
        self._traits = set()

    def add(self, trait, value=None):
        if isinstance(trait, str):
            trait = Trait(trait, value)
        self._traits.add(trait)

    def remove(self, trait):
        """
        You can pass trait string or object into this method
        """
        self._traits.remove(trait)

    def get(self, trait):
        for t in self._traits:
            if t == trait:
                return t

    def __len__(self):
        return len(self._traits)

    def __iter__(self):
        return iter(self._traits)


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
        if isinstance(other, str) or isinstance(other, unicode):
            return self.trait == other
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

    @property
    def trait(self):
        return self._trait

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
