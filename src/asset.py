
class Asset(object):
    """
    Assets that a player can purchase, like vehicles, weapons or mission requirement items like "Mega Torch 3000" to
    cut through vault doors!
    """

    def __init__(self, asset_id, name, description):
        self._asset_id = asset_id
        self._name = name
        self._description = description
