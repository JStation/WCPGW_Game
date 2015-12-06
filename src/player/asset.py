
class AssetQuantityTooLittle(Exception):
    pass


class PlayerAsset(object):
    def __init__(self, asset_id, quantity):
        self._asset_id = asset_id
        self._quantity = quantity

    def __add__(self, quantity):
        self.add(quantity)

    def __sub__(self, quantity):
        self.subtract(quantity)

    def add(self, quantity=1):
        self._quantity += quantity

    def subtract(self, quantity=1):
        if self._quantity < quantity:
            raise AssetQuantityTooLittle
        self._quantity -= quantity

    @property
    def asset_id(self):
        return self._asset_id

    @property
    def quantity(self):
        return self._quantity
