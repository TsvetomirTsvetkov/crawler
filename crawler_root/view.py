import os
from tabulate import tabulate
from .controller import Controller


class View:
    def __init__(self):
        self.controller = Controller()
        self.welcome()

    def welcome(self):
        os.system('clear')
        print('Welcome to Crawler')
        print('============================================================')
        self.execute_command()

    def show_commands(self):
        print('Use the number to specify which command you want to execute.')
        print('============================================================')
        print('1. Start crawling (without stopping)')
        # print('2. start_crawling_in_layers')
        print('2. See database')
        print('------------------------------------------------------------')
        print('9. Exit\n')

    def execute_command(self):
        self.show_commands()
        command_number = input('>  ')
        os.system('clear')

        while command_number != '9':
            if command_number == '1':
                self.start_crawling_without_stopping()
            # elif command_number == '2':
            #     self.start_crawling_in_layers()
            elif command_number == '2':
                self.see_db()
            else:
                print('============================================================')
                print('Unrecognized command. Try again.')
                print('============================================================')

            self.show_commands()
            command_number = input('>  ')
            os.system('clear')

    def start_crawling_in_layers(self):
        print('start_crawling_in_layers()')

    def start_crawling_without_stopping(self):
        print('===================Starting Crawler=========================')
        self.controller.start_crawling_without_stopping()
        print('=========================END================================')

    def see_db(self):
        servers = self.controller.see_db()
        headers = ["ID", "NAME", "NUMBER, ADDED"]

        servers_list = []

        if servers:
            for server in servers:
                servers_list.append((server.server_id, server.name, server.number, server.added))

            print(tabulate(servers_list, headers=headers, tablefmt="grid"))
            input('Press Enter...')
            os.system('clear')
        else:
            print('============================================================')
            print('No servers in the database.')

        print('============================================================')
