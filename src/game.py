import cmd
import os
import json
from asset import Asset
from goon import Goon
from player import Player


class Game(object):
    PATH_ASSETS = 'data/assets/'

    def __init__(self):
        self._assets = []
        self._player = Player()

        self.load_assets()

    def load_assets(self):
        for asset in Game.load_json_objects(self.PATH_ASSETS):
            self._assets.append(Asset.from_json(asset))

    def get_asset(self, asset_id):
        for asset in self._assets:
            if asset_id == asset.asset_id:
                return asset

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

        if s!=None:
            print(g.generateTraits())
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
