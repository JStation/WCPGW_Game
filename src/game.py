import cmd
from goon import Goon


assets = []

def get_asset(asset_id):
    for asset in assets:
        if asset_id == asset.asset_id:
            return asset


class game_cmd(cmd.Cmd, object):

    def do_newgoon(self, s):
        g = Goon()
        print("Name: %s\nType: %s" % (g.name, g.type))

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
