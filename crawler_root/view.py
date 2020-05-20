import os
from tabulate import tabulate
from .controller import Controller
from time import sleep


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
        print('1. Start Crawling (without stopping)')
        # print('2. start_crawling_in_layers')
        print('2. See Database')
        print('3. Show Analytics')
        print('------------------------------------------------------------')
        print('9. Exit\n')

    def show_analytic_options(self):
        print('Use the number to specify which command you want to execute.')
        print('============================================================')
        print('1. Last Hour')
        print('2. Last Day')
        print('3. Last 30 Days')
        print('------------------------------------------------------------')
        print('9. Go back\n')

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
            elif command_number == '3':
                self.show_analytics()
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

    def show_analytics(self):
        self.show_analytic_options()
        headers = ["NUMBER"]
        servers_list = []
        command_number = input('>  ')
        os.system('clear')

        if command_number == '1':
            analytics = self.controller.get_analytics(hour=True)
        elif command_number == '2':
            analytics = self.controller.get_analytics(day=True)
        elif command_number == '3':
            analytics = self.controller.get_analytics(month=True)
        else:
            print('============================================================')
            print('Unrecognized command. Going back to Main Menu.')
            print('============================================================')
            return

        servers_list.append((len(analytics),))
        print(tabulate(servers_list, headers=headers, tablefmt="grid"))
        print('============================================================')
        save_file = input('Do you want to save this into a file? < y / n > ')
        print('============================================================')
        if save_file == 'y':
            # Do something ...
            print('Analytics saved to ...')
        elif save_file == 'n':
            print('Analytics were not saved.')
        else:
            print('Unrecognized command. Going back to Main Menu.')
        print('============================================================')
        sleep(1)
        os.system('clear')
