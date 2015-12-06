
class Goon(object):
    """
    Name, skills, etc.
    """
    def __init__(self):
        self.name = "Another Goon"
        self.type = "Con Artist"
        self.skills = {
            "tech":1,
            "force":1,
            "charm":4,
            "stealth":3,
        }


    def __repr__(self):
        return self.name