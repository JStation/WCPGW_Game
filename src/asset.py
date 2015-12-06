
class DuplicateAssetTrait(Exception):
    pass


class Asset(object):
    """
    Assets that a player can purchase, like vehicles, weapons or mission requirement items like "Mega Torch 3000" to
    cut through vault doors!
    """

    def __init__(self, asset_id, name, description, category, price):
        self._asset_id = asset_id
        self._name = name
        self._description = description
        self._category = category
        self._price = price
        self._traits = {}

    def add_trait(self, trait, value):
        if trait in self._traits:
            raise DuplicateAssetTrait
        self._traits[trait] = value

    @classmethod
    def from_json(cls, json_data):
        asset = cls(
            asset_id=json_data['id'],
            name=json_data['name'],
            description=json_data['description'],
            category=json_data['category'],
            price=json_data['price']
        )

        for trait, value in json_data['traits'].items():
            asset.add_trait(trait, value)

        return asset
