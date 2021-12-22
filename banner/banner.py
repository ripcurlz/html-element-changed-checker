from datetime import datetime
from banner.colors import Colors

class Banner:

    # https://manytools.org/hacker-tools/ascii-banner/ used for creating the banner in "DOS Rebel"-style

    def __init__(self):
        self.colors = Colors()

    def print_banner(self):

        print('-' * 50)
        print('''
    █████   █████ ██████████   █████████    █████████ 
    ░░███   ░░███ ░░███░░░░░█  ███░░░░░███  ███░░░░░███
     ░███    ░███  ░███  █ ░  ███     ░░░  ███     ░░░ 
     ░███████████  ░██████   ░███         ░███         
     ░███░░░░░███  ░███░░█   ░███         ░███         
     ░███    ░███  ░███ ░   █░░███     ███░░███     ███
     █████   █████ ██████████ ░░█████████  ░░█████████ 
    ░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░░░░░    ░░░░░░░░░                                                       
                                                       
                                                       ''')
        print('-' * 50)

