import cmd
import random
import os
import json
from asset import Asset
from mission import Mission
from goon import Goon
from player import Player, MissionAttempt, FailedCriticalObjective


class Game(object):
    PATH_ASSETS = 'data/assets/'
    PATH_MISSIONS = 'data/missions/'
    PATH_GOON_DATA = 'data/goons/'

    def __init__(self):
        self._assets = set()
        self._missions = set()
        self._player = Player()

        self.load_assets()
        self.load_missions()
        self.load_goon_data()

    @property
    def player(self):
        return self._player

    def load_assets(self):
        for asset in Game.load_json_objects(self.PATH_ASSETS):
            self._assets.add(Asset.from_json(asset))

    def get_asset(self, asset_id):
        for asset in self._assets:
            if asset_id == asset.asset_id:
                return asset
        return None

    def load_missions(self):
        for mission in Game.load_json_objects(self.PATH_MISSIONS):
            self._missions.add(Mission.from_json(mission))

    def get_mission(self, mission_id):
        for mission in self._missions:
            if mission.id == mission_id:
                return mission

        return None

    def random_mission(self):
        return random.choice(tuple(self._missions))

    def load_goon_data(self):
        goon_data = {}
        for json_file in Game.load_json_objects(self.PATH_GOON_DATA):
            for category in json_file:
                goon_data[category] = json_file[category]
        Goon.goon_data = goon_data

    @staticmethod
    def load_json_objects(json_path):
        objects = []
        json_files = [json_file for json_file in os.listdir(json_path) if json_file.endswith('.json')]
        for json_file in json_files:
            with open(os.path.join(json_path, json_file)) as json_file_object:
                objects.append(json.load(json_file_object))
        return objects

game = Game()


class game_cmd(cmd.Cmd, object):

    def do_newgoon(self, s):
        g = Goon()
        print("Name: %s\nType: %s" % (g.name, g.type))
        print(g.generateTraits())

    def do_testmission(self, s=None):
        mission = None
        if s is not None:
            mission = game.get_mission(s)

        if mission is None:
            mission = game.random_mission()

        attempt = MissionAttempt(mission)
        goon_count = 0
        for objective in mission.objectives:
            for i in range(0, random.randint(2,4)):
                goon_count += 1
                goon = Goon()
                goon.generateTraits()
                attempt.add_goon_to_objective(objective.id, goon)

        print "The team is prepared to start %s" % mission.name
        game.player.remove_money(goon_count*200)
        print 'Spent %s on hiring goons.' % (goon_count*200)

        try:
            attempt.attempt()
            print '****************************************************************************************************'
            print 'The team has returned with the loot!'
            reward = attempt.reward
            game.player.add_money(reward)
            print '$%s is safe and sound back at the base!' % reward
            print 'You now have $%s!' % game.player.money
            print '****************************************************************************************************'
        except FailedCriticalObjective:
            print '####################################################################################################'
            print 'The team has failed the objective'
            print '####################################################################################################'

    # example to create a command in interpreter
    # anything with a do_ prefix is a command
    def do_echosomething(self, s):
        # all commands require an s (string) input even if you ignore it
        if s!= '':
            print('You wanted me to echo %s' % s)
        else:
            print("I'll say this instead")


    # gracefully handle exits
    def do_exit(self, s):
        return True

    def help_exit(self):
        print("Exit the interpreter.")
        print("You can also use the Ctrl-D shortcut.")

    do_EOF = do_exit
    help_EOF = help_exit


def main():
    game_interpreter = game_cmd()
    game_interpreter.cmdloop()

if __name__ == '__main__':
    main()
