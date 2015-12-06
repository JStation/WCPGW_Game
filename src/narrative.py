
class Narrative(object):
    def __init__(self):
        self._narrative = []

    def add(self, narrative):
        self._narrative.append(narrative)
        print narrative
