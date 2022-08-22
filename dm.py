"""Basketball Team Stats Tool Module."""
import os
import pprint
import string
import sys
import unittest

# Initialize a global private variable for balanced teams since
# it's used in multiple functions.
_balanced_teams = {}


def calculate_avg_height(players_list):
    """
    Calculate the average height of all players in a team.

    This function creates a 'height' list then sums the values and
    returns the rounded average.
    """
    # In case during development I messed with values in the data file
    # the total height could be 0, so I'm including a check for that.
    try:
        height = [player["height"] for player in players_list]
        return round(sum(height) / len(height), 2)
    except ZeroDivisionError:
        print("\nPlayer heights data error.\n")
        return 0


def create_string_from_list_of_lists(list_of_lists):
    """
    Create a string of comma separated values from a list of lists.

    Example: create_string_from_list_of_lists([[1, 2, 3], [4, 5, 6]])
    Returns: "1, 2, 3, 4, 5, 6"
    """
    return ", ".join([", ".join(item) for item in list_of_lists])


def clean_players(data):
    """Clean the data for use in the program.

    Data to be cleaned:
    Height: Should be saved as an integer.
    Experience: Should be a boolean value (True or False).
    Guardians: Should be a List of strings for each player with 'and' removed.

    Returns a List with nested Dictionaries
    """
    cleaned = []

    for item in data:
        fixed = {
            "name": item["name"],
            "guardians": item["guardians"].split(" and "),
            "height": int(item["height"].split(" ")[0]),
            # Using 'tupled ternary technique' to convert experience to boolean
            # https://book.pythontips.com/en/latest/ternary_operators.html
            "experience": (False, True)[item["experience"] == "YES"]}

        cleaned.append(fixed)

    return cleaned


def balance_teams(teams, cleaned_players):
    """Ensure each team has an equal number of players.

    Split players into experienced and inexperienced players.
    Check each list has the same number of players.
    Add equal number of each type of player to each team.

    Save the team analysis data points to the team's data structure
    - number of inexperienced players on that team
    - number of experienced players on that team
    - the average height of the team
    """
    # Initialize balanced_teams dictionary with each teams name.
    # For each team, initialize object keys to hold analysis data.
    for team in teams:
        _balanced_teams[team] = {
            "average_player_height" : 0,
            "number_of_experienced_players" : 0,
            "number_of_inexperienced_players" : 0,
            "players" : []
        }


    # Create a list of experienced and inexperienced players.
    players_trained = [
        player for player in cleaned_players if player["experience"]]
    players_untrained = [
        player for player in cleaned_players if not player["experience"]
    ]

    # TODO: Organize Players by Height
    # When printing the players to the console, print them out from the shortest to the tallest player.

    # Sanity check to ensure data includes an equal number of
    # experienced and inexperienced players.
    if not len(players_trained) == len(players_untrained):
        print(
            "\nERROR: Number of players trained and untrained are not equal."
            f"\n Experienced players: ({len(players_trained)})"
            f"\n Inexperienced players: ({len(players_untrained)})"
            "\n Please check the data and try again.\n")
        sys.exit("Program exited successfully.")

    # Loop through the lists of experienced and inexperienced players
    # and add them to each team. Popping them off the list each time
    # it's added to a team reduces the lists till they're both empty.
    while players_trained and players_untrained:
        for team in teams:
            _balanced_teams[team]["players"].append(players_trained.pop())
            _balanced_teams[team]["players"].append(players_untrained.pop())

    # Save number of experienced/inexperienced players and average height of the team.
    for team in teams:
        players_trained = [player for player in _balanced_teams[team]["players"] if player["experience"]]
        players_untrained = [player for player in _balanced_teams[team]["players"] if not player["experience"]]
        _balanced_teams[team]["average_player_height"] = calculate_avg_height(_balanced_teams[team]["players"])
        _balanced_teams[team]["number_of_experienced_players"] = len(players_trained)
        _balanced_teams[team]["number_of_inexperienced_players"] = len(players_untrained)

    return _balanced_teams


def show_menu_options(options):
    """Show a list of options.

    Args:
        # options (list): List of options to show in menu format.
    """
    menu_dict = dict(zip(string.ascii_uppercase, options))
    for key, value in menu_dict.items():
        print(f" {key}) {value}")


def menu_teams(msg=None):
    """Show a list of teams and prompt user for input.

    Convert a letter returned as 'selected_option' into an integer to use
    as an index for accessing the selected team in the teams list before
    displaying the team's stats.
    """
    # To print the data structure uncomment the following line.
    # devtime(_balanced_teams)
    team_keys = tuple(_balanced_teams.keys())
    print()
    show_menu_options(team_keys)
    print([msg, ''][msg is None])
    selected_option = input("Enter an option: ")

    # Test if selected_option is an alpha character within range
    # NOTE: The selected_option is converted to an integer using ord() to use
    # as an index indicating which team in the team_index to show stats for.
    # ord() conversion example:
    # If team is 'a', the index will be 0 (97 - 97 = 0)
    # If team is 'b', the index will be 1 (98 - 97 = 1)
    # REF: https://docs.python.org/3/library/functions.html#ord
    # REF: https://en.wikipedia.org/wiki/List_of_Unicode_characters#Basic_Latin
    # Notice decimal value for 'Latin Small Letter A' is 97.
    if selected_option.isalpha() and (ord(selected_option.lower()) - 97) in range(len(team_keys)):
        show_team_stats(team_keys[ord(selected_option.lower()) - 97])
        input("\nPress ENTER to continue...")
        menu_main()
    else:
        menu_teams(f"\n'{selected_option}' is invalid. Enter a menu option.")


def menu_main(msg=None):
    """Show a list of options and prompt user for input."""
    # Clear screen each time main menu is shown
    os.system('cls' if os.name == 'nt' else 'clear')
    print("BASKETBALL TEAM STATS TOOL")
    print("\n---- MENU----")
    print("\nHere are your choices:")

    # NOTE: I'm packing a Tuple to store _main_menu_options because the order
    # matters. If this were a List or Set, the order would be random since
    # they're mutable.
    show_menu_options(("Display Team Stats", "Quit"))
    print([msg, ''][msg is None])
    selected_option = input("Enter an option: ")

    if selected_option.lower() == "a":
        menu_teams()
    elif selected_option.lower() == "b":
        os.system("clear")
        print("\nBye :)\n")
        sys.exit("Program exited successfully.")
    else:
        menu_main(
            f"\n'{selected_option}' is invalid. Enter a menu option.")


def show_team_stats(team_key):
    """Show stats for a team.

    Args:
        team_key (str): Key value of the team in the _balanced_teams dictionary
    """
    team = _balanced_teams[team_key]
    players_guardians = [player["guardians"] for player in team["players"]]

    print(f"\nTeam: {team_key} Stats")
    print("-"*79)
    print(f"Total players: {len(team['players'])}")
    print(f"Total experienced: {team['number_of_experienced_players']}")
    print(f"Total inexperienced: {team['number_of_inexperienced_players']}")
    print(f"Average height: {team['average_player_height']}")
    print("-"*79)
    # Print players list based on height in a table format.
    print("Players List (shortest to tallest):")
    print("Name                 | Height | Experience".upper())
    print("-"*48)
    # NOTE: The lambda (a custom anonymous function) returns the height value
    # to use as the key for sorting.
    # It's equivalent to writing something like this:
    # def get_height_value(player):
    #     return player["height"]
    # REF: https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions
    for player in sorted(team["players"], key=lambda p: p["height"]):
        # Pad the values with spaces to align the other columns.
        player_name = f"{player['name']:<20}"
        player_height = f"{player['height']:>6}"
        player_experience = "Inexperienced"
        if player['experience'] is True:
            player_experience = "Experienced"
        txt = "{} | {} | {}"
        print(txt.format(player_name, player_height, player_experience))
    print("-"*79)
    print(
        f"Guardians:\n {create_string_from_list_of_lists(players_guardians)}")

    # Show the lists of experienced/inexperienced player dictionaries if needed
    # print("\nExperienced Players:")
    # print(*players_trained, sep=',\n')
    # print("\nInexperienced Players:")
    # print(*players_untrained, sep=',\n')


def main(players, teams):
    """Start the application.

    Args:
        PLAYERS (list): List of player objects.
        TEAMS (list): List of team data.
    """
    _balanced_teams = balance_teams(teams, clean_players(players))
    menu_main()


def devtime(data):
    """
    Pretty print data to check for anomalies. For use only during development.

    Example: devtime(_balanced_teams)
    """
    pp = pprint.PrettyPrinter(indent=1, compact=True, width=160)
    print("=" * 79)
    pp.pprint(data)
    print("=" * 79)


# pylint: disable=missing-class-docstring
class Tests(unittest.TestCase):
    # pylint: disable=missing-function-docstring

    def setUp(self):
        # Set up test data
        self.teams = ["Team C", "Team D", "Team A", "Team B"]
        self.players = [
            {
                'name': 'Karl Saygan',
                'guardians': 'Heather Bledsoe',
                'experience': 'YES',
                'height': '42 inches'
            },
            {
                'name': 'Matt Gill',
                'guardians': 'Charles Gill and Sylvia Gill',
                'experience': 'NO',
                'height': '40 inches'
            },
            {
                'name': 'Sammy Adams',
                'guardians': 'Jeff Adams and Gary Adams',
                'experience': 'NO',
                'height': '45 inches'
            },
            {
                'name': 'Chloe Alaska',
                'guardians': 'David Alaska and Jamie Alaska',
                'experience': 'NO',
                'height': '47 inches'
            },
            {
                'name': 'Bill Bon',
                'guardians': 'Sara Bon and Jenny Bon',
                'experience': 'YES',
                'height': '43 inches'
            },
            {
                'name': 'Joe Kavalier',
                'guardians': 'Sam Kavalier and Elaine Kavalier',
                'experience': 'YES',
                'height': '39 inches'
            },
            {
                'name': 'Phillip Helm',
                'guardians': 'Thomas Helm and Eva Jones',
                'experience': 'NO',
                'height': '44 inches'
            },
            {
                'name': 'Les Clay',
                'guardians': 'Wynonna Brown',
                'experience': 'YES',
                'height': '42 inches'
            }
        ]

    def test_create_string_from_list_of_lists(self):
        string_to_test = create_string_from_list_of_lists(
            [['item 1', 'item 2'], ['item 3', 'item 4']])
        self.assertIs(type(string_to_test), str)
        self.assertEqual(string_to_test, "item 1, item 2, item 3, item 4")

    def test_cleaned_players(self):
        cleaned = clean_players(self.players)
        self.assertIs(type(cleaned), list)
        self.assertEqual(len(cleaned), 8)
        self.assertEqual(cleaned[0]['name'], 'Karl Saygan')
        self.assertEqual(cleaned[0]['guardians'], ['Heather Bledsoe'])
        self.assertTrue(cleaned[0]['experience'])
        self.assertEqual(cleaned[0]['height'], 42)

    def test_calculate_avg_height(self):
        players = clean_players(self.players)
        average_height = calculate_avg_height(*players)
        self.assertIs(type(average_height), float)
        self.assertEqual(average_height, 42.75)

    def test_balance_teams(self):
        cleaned_players = clean_players(self.players)
        balanced_teams = balance_teams(self.teams, cleaned_players)
        self.assertIs(type(balanced_teams), dict)
        self.assertEqual(len(balanced_teams), 4)
        # devtime(balanced_teams)
        self.assertEqual(balanced_teams['Team A'][0]['name'], 'Bill Bon')
        self.assertEqual(balanced_teams['Team A'][1]['name'], 'Sammy Adams')
        self.assertEqual(balanced_teams['Team D'][0]['name'], 'Joe Kavalier')
        self.assertEqual(balanced_teams['Team D'][1]['name'], 'Chloe Alaska')


class ToDoTests(unittest.TestCase):
    # Grouping these separately so they can be run separately and appear in the
    # command line output after running the other tests.
    # pylint: disable=missing-function-docstring

    @unittest.skip("TODO: When there's more time, test this")
    def test_show_menu_options(self):
        self.assertEqual(show_menu_options(_main_menu_options), 'a')

    @unittest.skip("TODO: When there's more time, test this")
    def test_show_team_stats(self):
        self.assertEqual(show_team_stats('A'), None)
        self.assertEqual(show_team_stats('B'), None)


# Prevent automatic execution of the script when imported or called directly
if __name__ == "__main__":
    unittest.main()
