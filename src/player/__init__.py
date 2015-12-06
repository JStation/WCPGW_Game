from .asset import PlayerAsset


class NotEnoughMoney(Exception):
    pass


class DoesNotOwnAsset(Exception):
    pass


class Player(object):
    """
    Place to store player's assets and money
    """

    def __init__(self):
        self._money = 100  # Start with 100, maybe read from some sort of setting file instead?
        self._assets = []

    def get_asset(self, asset_id):
        for a in self._assets:
            if asset_id == a.asset.asset_id:
                return a

        return None

    def add_asset(self, asset_id, quantity=1):
        player_asset = self.get_asset(asset_id)

        if player_asset is None:
            player_asset = PlayerAsset(asset_id, 0)
            self._assets.append(player_asset)

        player_asset += quantity

    def subtract_asset(self, asset_id, quantity=1):
        player_asset = self.get_asset(asset_id)
        player_asset -= quantity
        if player_asset.quantity == 0:
            self._assets.remove(player_asset)

    def add_money(self, change):
        self._money += change

    def remove_money(self, change):
        if self._money < change:
            raise NotEnoughMoney
        self._money -= change
