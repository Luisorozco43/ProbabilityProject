import colorama
from colorama import Fore
from match import Match
from cards import Player
from utils.output_formatter import OutputFormatter
from utils.probability_calculator import ProbabilityCalculator

colorama.init(autoreset=True)
ABORT_MATCH_MESSAGE = "La partida ha terminado"


# Start the match
def main():
    """
    Entry point of the game
    """
    name = str(input("Cual es tu nombre (por defecto 'Jugador')=> "))
    match = Match()
    computer = Player("Computadora")
    player = Player(name if name else "Jugador")
    players = [computer, player]
    match.start(players)

    # Hole cards
    match.draw_hole_cards()
    
    ProbabilityCalculator.menu(match, 1)

    # Flop
    match.draw_flop()
    if match.await_option() is False:
        print(Fore.RED + ABORT_MATCH_MESSAGE)
        return

    ProbabilityCalculator.menu(match, 1)

    # Turn
    match.draw_turn()
    if match.await_option() is False:
        print(Fore.RED + ABORT_MATCH_MESSAGE)
        return

    ProbabilityCalculator.menu(match, 1)

    # River
    match.draw_river()
    if match.await_option() is False:
        print(Fore.RED + ABORT_MATCH_MESSAGE)
        return

    # Showdown
    winner = match.showdown()
    if winner:
        OutputFormatter.print_winner("player")
    elif not winner:
        OutputFormatter.print_winner("computer")
    else:
        OutputFormatter("tie")


if __name__ == "__main__":
    main()
