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
        if isinstance(trait, TraitList):
            for t in trait:
                # Pass a new trait into self.add, we don't want to reference existing trait
                if isinstance(t, TraitRange):
                    self.add(TraitRange(t.trait,t.min,t.max))
                else:
                    self.add(t.trait, t.value)
        else:
            if isinstance(trait, str) or isinstance(trait, unicode):
                trait = Trait(trait, value)

            if trait in self:
                existing_trait = self.get(trait.trait)
                existing_trait += trait
            else:
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

    def __repr__(self):
        return ', '.join(['%s: %s' % (trait.trait, trait.value) for trait in self._traits])


    @classmethod
    def list_from_json(cls, json_data):
        traits = cls()

        for t,r in json_data.items():
            if isinstance(r, int):
                trait = Trait(t, r, 0)
            else:
                trait = TraitRange(t, *r.split('-'))
            traits.add(trait)

        return traits


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

    def __repr__(self):
        return '%s: %s' % (self._trait, self._value)

    def __add__(self, other):
        if isinstance(other, Trait):
            self._value += other.value
        else:
            self._value += other

    def __eq__(self, other):
        if isinstance(other, str) or isinstance(other, unicode):
            return self.trait == other
        return self.trait == other.trait


class TraitRange(object):
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

    @property
    def value(self):
        return self.roll()

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    def roll(self):
        if self._max == 0:
            return self._min
        else:
            return random.randint(self._min, self._max)

    def __repr__(self):
        return '%s: %s-%s' % (self._trait, self._min, self._max)

    def __add__(self, other):
        if isinstance(other, Trait) or isinstance(other, TraitRange):
            self._min += other.value
            self._max += other.value
        else:
            self._min += other
            self._max += other

    def __eq__(self, other):
        if isinstance(other, str) or isinstance(other, unicode):
            return self.trait == other
        return self.trait == other.trait
