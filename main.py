from colorama import Fore, init
from match import Match
from cards import Player
from utils.output_formatter import OutputFormatter
from utils.probability_calculator import ProbabilityCalculator

# Initialize colorama
init(autoreset=True)

DEFAULT_PLAYER_NAME = "Jugador"
ABORT_MATCH_MESSAGE = "El juego ha sido abortado."

def get_player_name():
    """Prompt the user for their name and return it."""
    name = input("Cual es tu nombre (por defecto 'Jugador') => ").strip()
    return name if name else DEFAULT_PLAYER_NAME

def setup_match():
    """Set up the match with players and return the match object."""
    match = Match()
    computer = Player("Computadora")
    player = Player(get_player_name())
    players = [computer, player]
    match.start(players)
    return match

def play_round(match):
    """Play a round of the game, including drawing cards and calculating probabilities."""
    # Hole cards
    match.draw_hole_cards()
    ProbabilityCalculator.menu(match, 1)  # Calculate player's probability

    # Flop
    match.draw_flop()
    if not match.await_option():
        print(Fore.RED + ABORT_MATCH_MESSAGE)
        return False
    ProbabilityCalculator.menu(match, 1)

    # Turn
    match.draw_turn()
    if not match.await_option():
        print(Fore.RED + ABORT_MATCH_MESSAGE)
        return False
    ProbabilityCalculator.menu(match, 1)

    # River
    match.draw_river()
    if not match.await_option():
        print(Fore.RED + ABORT_MATCH_MESSAGE)
        return False
    ProbabilityCalculator.menu(match, 1)

    return True

def main():
    """Entry point of the game."""
    match = setup_match()
    if play_round(match):
        # Showdown
        result = match.showdown()
        if result is True:
            OutputFormatter.print_winner("player")
        elif result is False:
            OutputFormatter.print_winner("computer")
        else:
            OutputFormatter.print_winner("tie")

if __name__ == "__main__":
    main()
