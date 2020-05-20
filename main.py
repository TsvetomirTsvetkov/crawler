import sys
from db import Database
from view import View


class Application:
    @classmethod
    def build(self):
        Database.build()

    @classmethod
    def start(self):
        return View()


def main():
    if len(sys.argv) == 2:
        parameter = sys.argv[1]

        if parameter == 'build':
            Application.build()

        elif parameter == 'start':
            Application.start()

        else:
            print('Unrecognized command.\nCommands are: build | start')
    else:
        print('You need to specify a command after "main.py"\nCommands are: build | start')


if __name__ == '__main__':
    main()
