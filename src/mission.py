

class Mission(object):
    """
    Mission requirements, objectives, etc.
    """
    def __init__(self, mission_id, name, description, category, reward_min, reward_max):
        self._mission_id = mission_id
        self._name = name
        self._description = description
        self._category = category
        self._reward_min = reward_min
        self._reward_max = reward_max

        self._objectives = []
        self._complications = []

    def add_objective(self, objective):
        self._objectives.append(objective)

    def add_complication(self, complication):
        self._complications.append(complication)

    @classmethod
    def from_json(cls, json_data):
        mission = cls(
            mission_id=json_data['id'],
            name=json_data['name'],
            description=json_data['description'],
            category=json_data['category'],
            reward_min=json_data['reward_min'],
            reward_max=json_data['reward_max']
        )

        for objective in json_data['objectives']:
            mission.add_objective(MissionObjective.from_json(objective))

        for complication in json_data['complications']:
            mission.add_complication(MissionComplication.from_json(complication))

        return mission


class MissionObjective(object):
    def __init__(self, objective_id, name, reward_min=0, reward_max=0):
        self._id = objective_id
        self._name = name
        self._reward_min = reward_min
        self._reward_max = reward_max
        self._solutions = []

    def add_solution(self, solution):
        self._solutions.append(solution)

    @classmethod
    def from_json(cls, json_data):
        objective = cls(
            objective_id=json_data['id'],
            name=json_data['name'],
            reward_min=getattr(json_data, 'reward_min', 0),
            reward_max=getattr(json_data, 'reward_max', 0)
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
