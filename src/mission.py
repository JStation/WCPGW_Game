import random
from traits import TraitRequirement


class Mission(object):
    """
    Mission requirements, objectives, etc.
    """
    def __init__(self, mission_id, name, description, category, reward_min, reward_max):
        self._id = mission_id
        self._name = name
        self._description = description
        self._category = category
        self._reward_min = reward_min
        self._reward_max = reward_max

        self._objectives = []
        self._complications = set()

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name

    @property
    def objectives(self):
        return self._objectives

    def get_reward(self):
        return random.randint(self._reward_min, self._reward_max)

    def add_objective(self, objective):
        self._objectives.append(objective)

    def get_objective(self, objective_id):
        for objective in self._objectives:
            if objective.id == objective_id:
                return objective

        return None

    def add_complication(self, complication):
        self._complications.add(complication)

    @classmethod
    def from_json(cls, json_data):
        mission = cls(
            mission_id=json_data['id'],
            name=json_data['name'],
            description=json_data['description'],
            category=json_data['category'],
            reward_min=json_data.get('reward_min', 0),
            reward_max=json_data.get('reward_max', 0)
        )

        for objective in json_data['objectives']:
            mission.add_objective(MissionObjective.from_json(objective))

        for complication in json_data['complications']:
            mission.add_complication(MissionComplication.from_json(complication))

        return mission


class MissionObjective(object):
    def __init__(self, objective_id, name, can_fail, objectives_required, reward_min=0, reward_max=0):
        self._id = objective_id
        self._name = name
        self._can_fail = can_fail
        self._objectives_required = objectives_required
        self._reward_min = reward_min
        self._reward_max = reward_max
        self._solutions = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def can_fail(self):
        return self._can_fail

    @property
    def objectives_required(self):
        return self._objectives_required

    @property
    def solutions(self):
        return self._solutions

    def get_reward(self):
        return random.randint(self._reward_min, self._reward_max)

    def add_solution(self, solution):
        self._solutions.append(solution)

    @classmethod
    def from_json(cls, json_data):
        objective = cls(
            objective_id=json_data['id'],
            name=json_data['name'],
            can_fail=json_data.get('can_fail', True),
            objectives_required=json_data.get('objectives_required', []),
            reward_min=json_data.get('reward_min', 0),
            reward_max=json_data.get('reward_max', 0),
        )

        for solution in json_data['solutions']:
            objective.add_solution(MissionObjectiveSolution.from_json(solution))

        return objective


class MissionObjectiveSolution(object):
    def __init__(self, solution_id, name, type, traits=None):
        self._id = solution_id
        self._name = name
        self._type = type
        self._traits = []

        if traits is not None:
            self._traits += traits

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def traits(self):
        return self._traits

    @classmethod
    def from_json(cls, json_data):
        traits = TraitRequirement.list_from_json(json_data['traits'])

        solution = cls(
            solution_id=json_data['id'],
            name=json_data['name'],
            type=json_data['type'],
            traits=traits
        )

        return solution


class MissionComplication(object):
    def __init__(self, complication_id, name, description, objectives, chance, traits=None):
        self._id = complication_id
        self._name = name
        self._description = description
        self._objectives = []

        if isinstance(objectives, str):
            self._objectives.append(objectives)
        else:
            self._objectives += objectives

        self._chance = chance
        self._traits = []

        if traits is not None:
            self._traits += traits

    @classmethod
    def from_json(cls, json_data):
        traits = TraitRequirement.list_from_json(json_data['traits'])

        complication = cls(
            complication_id=json_data['id'],
            name=json_data['name'],
            description=json_data['description'],
            objectives=json_data['objectives'],
            chance=json_data['chance'],
            traits=traits
        )

        return complication
