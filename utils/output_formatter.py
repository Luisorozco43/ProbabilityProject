from colorama import Fore
from utils.hand_rankings import HandRanks


class OutputFormatter:
    """
    Utility class that formats the output with colors
    for information on various stages of the poker game.
    """

    @staticmethod
    def print_community_cards(community_cards):
        """
        Prints the community cards in a formatted and colored output.

        Parameters:
            community_cards (List[Card]): A list of `Card` objects representing the community cards.

        Returns:
            None: This method prints the community cards to the console and does not return any value.
        """
        default_color = Fore.GREEN
        print(default_color + "===CARTAS COMUNITARIAS===")
        for card in community_cards:
            print(default_color + f"{card}")
        print(default_color + "=" * 25)

    @staticmethod
    def print_player_hand(player):
        """
        Prints the player's hand in a formatted and colored output.

        Parameters:
            player (Player): An instance of the `Player` class containing the player's name and hand of cards.

        Returns:
            None: This method prints the player's hand to the console and does not return any value.
        """
        default_color = Fore.CYAN
        print(default_color + f"===CARTAS DE {player.name.upper()}===")
        for card in player.hand:
            print(default_color + f"{card}")
        print(default_color + "=" * 30)

    @staticmethod
    def print_best_hand(player_name, ranking):
        """
        Prints the best hand ranking in a formatted and colored output.

        Parameters:
            player_name (str): The name of the player who owns the hand
            ranking (HandRanks): An instance of `HandRanks` representing the hand's rank (e.g., 'Pair', 'Straight').

        Returns:
            None: This method prints the best hand ranking to the console and does not return any value.
        """
        default_color = Fore.GREEN
        rank = HandRanks.get_name(ranking)
        print(default_color + f"Mejor mano de {player_name}: {rank}")

    @staticmethod
    def print_winner(winner):
        """
        Prints the winner of the game in a formatted and colored output.

        Parameters:
            winner (str): A string indicating the winner of the game.
                          Can be one of 'player', 'computer', or 'tie'.

        Returns:
            None: This method prints the outcome of the game to the console and does not return any value.

        Raises:
            ValueError: If the `winner` is not one of 'player', 'computer', or 'tie'.
        """
        if winner == "player":
            print(Fore.GREEN + "Tu ganas!")
        elif winner == "computer":
            print(Fore.RED + "La computadora gana!")
        elif winner == "tie":
            print(Fore.YELLOW + "Es un empate!")
        else:
            raise ValueError("El ganador solo puede ser la computadora o tu.")
