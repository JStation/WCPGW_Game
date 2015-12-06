
class NotEnoughMoney(Exception):
    pass


class Player(object):
    """
    Place to store player's assets and money
    """

    def __init__(self):
        self._money = 100  # Start with 100, maybe read from some sort of setting file instead?
        self._assets = []

    def add_asset(self, asset):
        self._assets.append(asset)

    def remove_asset(self, asset):
        self._assets.remove(asset)

    def add_money(self, change):
        self._money += change

    def remove_money(self, change):
        if self._money < change:
            raise NotEnoughMoney
        self._money -= change
