from colorama import Fore
from cards import Deck
from utils.output_formatter import OutputFormatter
from utils.hand_analyzer import HandAnalyzer

# from exceptions import *

PLAYER = 1
COMPUTER = 0


class Match(object):
    """
    Class that represents a Poker match

    Attributes:
        deck (Deck): An instance of the Deck class representing the deck of cards.
        players (List[Player]): A list of Player objects participating in the match.
        flop (List[Card]): A list containing the three community cards on the table (flop).
        turn (Card): A single community card dealt after the flop.
        river (Card): A single community card dealt after the turn.
    """

    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.flop = []
        self.turn = None
        self.river = None
        self.deck.shuffle()

    def draw_n_cards(self, num=1):
        """Draws n number of cards from the deck"""
        cards = []
        for _ in range(num):
            card = self.deck.deal()
            if not card:
                break
            cards.append(card)
        return cards

    def draw_single_card(self, stage="turn"):
        """
        Draws a single card for the turn or river.
        The stage variable defaults to 'turn'
        """
        card = self.deck.deal()
        if not card:
            return False
        if stage == "turn":
            self.turn = card
        elif stage == "river":
            self.river = card
        else:
            raise ValueError("Stage no valido, debe ser ser 'turn' o 'river'.")
        return True

    def draw_hole_cards(self):
        """Draws two cards for each player"""
        # Ensure there are enough cards in the deck
        total_cards_needed = len(self.players) * 2
        if len(self.deck.cards) < total_cards_needed:
            raise ValueError("No hay suficientes cartas en la baraja")
        for player in self.players:
            cards = self.draw_n_cards(2)
            if not cards:  # If no cards are drawn, handle the situation
                raise ValueError(
                    f"No se ha podido entregar cartas privadas a {player.name}."
                )
            for card in cards:
                player.hand.append(card)

    # Draws three cards and assigns them to the flop set
    def draw_flop(self):
        """Draws 3 cards for the flop"""
        cards = self.draw_n_cards(3)
        if not cards:
            return False
        self.flop.extend(cards)
        return True

    def draw_turn(self):
        """Draws a card for the turn"""
        return self.draw_single_card("turn")

    def draw_river(self):
        """Draws a card for the river"""
        return self.draw_single_card("river")

    def get_community_cards(self):
        """Returns a list containing the community cards"""
        community_cards = []
        community_cards.extend(self.flop)
        if self.turn:
            community_cards.append(self.turn)
        if self.river:
            community_cards.append(self.river)
        return community_cards

    def await_option(self):
        """Asks the user if he/she wants to continue or quit the game"""
        community_cards = self.get_community_cards()
        # In the context of this game, the player will always be initialized on the position 1
        # Position 0 of the player's list belongs to the computer
        player = self.players[PLAYER]
        OutputFormatter.print_community_cards(community_cards)
        computer = self.players[COMPUTER]
        OutputFormatter.print_player_hand(player)
        OutputFormatter.print_player_hand(computer)
        while True:
            command = str(input("Deseas continuar? (s|n) ")).strip().lower()
            if command not in ("s", "n"):
                print(Fore.RED + "Por favor ingresa una opcion valida")
                continue
            break
        return command == "s"

    def get_full_hand(self, index):
        """Returns a list with the community cards and the hole cards"""
        player_hand = self.players[index].hand[:]
        player_hand.extend(self.get_community_cards())
        return player_hand

    def get_best_hand_and_rank(self, player_index):
        """Helper method to get the best hand and rank for a player."""
        full_hand = self.get_full_hand(player_index)
        best_hand, hand_rank = HandAnalyzer.best_hand(full_hand)
        return best_hand, hand_rank

    def showdown(self):
        """Chooses a winner or verifies if there is a tie."""
        # Get player's best hand and rank
        player_best_hand, player_rank = self.get_best_hand_and_rank(PLAYER)
        # Get computer's best hand and rank
        computer_best_hand, computer_rank = self.get_best_hand_and_rank(COMPUTER)

        # Print best hands
        OutputFormatter.print_best_hand(self.players[PLAYER].name, player_rank)
        OutputFormatter.print_best_hand(self.players[COMPUTER].name, computer_rank)

        # Compare hand ranks
        if player_rank.value > computer_rank.value:
            return True  # Player wins
        elif player_rank.value < computer_rank.value:
            return False  # Computer wins
        else:
            # If ranks are the same, compare card values
            player_sorted = sorted((card.value for card in player_best_hand), reverse=True)
            computer_sorted = sorted((card.value for card in computer_best_hand), reverse=True)

            # Compare each card in order
            for player_card, computer_card in zip(player_sorted, computer_sorted):
                if player_card > computer_card:
                    return True  # Player wins
                elif player_card < computer_card:
                    return False  # Computer wins

            # If all cards are equal, it's a tie
            return None

    def start(self, players):
        """Fills the player's list"""
        self.players.extend(players)
