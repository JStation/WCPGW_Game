from goon import GoonGroup
from narrative import Narrative
from traits import Trait, TraitList


class FailedCriticalObjective(Exception):
    pass


class NotEnoughMoney(Exception):
    pass


class DoesNotOwnAsset(Exception):
    pass


class AssetQuantityTooLittle(Exception):
    pass


class Player(object):
    """
    Place to store player's assets and money
    """

    def __init__(self):
        self._money = 100000  # Start with 100, maybe read from some sort of setting file instead?
        self._assets = []
    
    @property
    def money(self):
        return self._money

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


class MissionAttempt(object):
    def __init__(self, mission):
        self._mission = mission
        self._squads = []
        self._goons = GoonGroup()
        self._traits = set()
        self._narrative = Narrative()
        self._reward = mission.get_reward()
        self._objective_results = {}
        self._failed_objectives = set()

        for objective in mission.objectives:
            self._squads.append(MissionObjectiveSquad(objective, self._narrative, self))

    @property
    def goons(self):
        return self._goons

    @property
    def reward(self):
        return self._reward

    def get_squad_for_objective(self, objective_id, create=True):
        objective = self._mission.get_objective(objective_id)
        for squad in self._squads:
            if squad.objective == objective:
                return squad

        if create:
            return MissionObjectiveSquad(objective, self._narrative, self)

    def add_goon_to_objective(self, objective_id, goon):
        if goon not in self._goons:
            self._goons.add(goon)
        squad = self.get_squad_for_objective(objective_id)
        squad.add_goon(goon)

    def attempt(self):
        for objective_squad in self._squads:
            self._narrative.add('_____________________________________________________________________________________')
            skip = False
            for obj in objective_squad.objective.objectives_required:
                if obj in self._failed_objectives:
                    self._narrative.add('Cannot attempt objective: [%s], failed required objective(s)' % objective_squad.objective.name)
                    skip = True
                    break

            if skip:
                continue

            self._narrative.add('Attempting objective: [%s]' % objective_squad.objective.name)
            if objective_squad.attempt_objective():
                self._narrative.add('The team succeeded [%s]!' % objective_squad.objective.name)
                self._objective_results[objective_squad.objective.id] = True
                reward = objective_squad.objective.get_reward()
                if reward:
                    self._narrative.add('$%s was obtained!' % reward)
                    self._reward += reward
            else:
                self._narrative.add('The team failed [%s].' % objective_squad.objective.name)
                self._objective_results[objective_squad.objective.id] = False
                self._failed_objectives.add(objective_squad.objective.id)


class MissionObjectiveSquad(object):
    def __init__(self, objective, narrative, mission):
        self._goons = GoonGroup()
        self._objective = objective
        self._narrative = narrative
        self._mission = mission

    @property
    def objective(self):
        return self._objective

    def add_goon(self, goon):
        self._goons.add(goon)

    def attempt_objective(self):
        for solution in self._objective.solutions:
            self._narrative.add('- The team has started [%s].' % solution.name)
            if self.attempt_solution(solution):
                self._narrative.add('-- The team succeeded [%s]!' % solution.name)
                return True
            else:
                self._narrative.add('-- The team failed [%s].' % solution.name)

        if not self._objective.can_fail:
            raise FailedCriticalObjective
        return False

    def attempt_solution(self, solution):
        if solution.type == 'assigned':
            goon_traits = self._goons.traits
        else:
            goon_traits = self._mission.goons.traits

        for trait in solution.traits:
            squad_trait = goon_traits.get(trait.trait)
            if squad_trait is None:
                return False

            if squad_trait.value < trait.roll():
                return False

        return True
