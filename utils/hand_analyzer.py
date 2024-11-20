from itertools import combinations
from collections import Counter
from utils.hand_rankings import HandRanks
from treys import Deck, Evaluator
import random

class HandAnalyzer(object):
    """
    Utility class to verify which hand was formed 
    which the hole cards given to the player 
    and the community cards
    """

    @staticmethod
    def is_flush(cards):
        """Check if all cards have the same suit."""
        suits = [card.suit for card in cards]
        return len(set(suits)) == 1

    @staticmethod
    def is_straight(cards):
        """Check if cards form a straight."""
        values = sorted(card.value for card in cards)
        for i in range(len(values) - 1):
            if values[i] + 1 != values[i + 1]:
                return False
        return True

    @staticmethod
    def hand_rank(cards):
        """Evaluate the hand rank and return a HandRank enum."""
        values = sorted([card.value for card in cards], reverse=True)
        counts = Counter(values)
        most_common = counts.most_common()

        match True:
            case _ if HandAnalyzer.is_flush(cards) and HandAnalyzer.is_straight(cards):
                if values == [10, 11, 12, 13, 14]:
                    return HandRanks.ROYAL_FLUSH
                return HandRanks.STRAIGHT_FLUSH

            case _ if most_common[0][1] == 4:
                return HandRanks.FOUR_OF_A_KIND

            case _ if most_common[0][1] == 3 and most_common[1][1] == 2:
                return HandRanks.FULL_HOUSE

            case _ if HandAnalyzer.is_flush(cards):
                return HandRanks.FLUSH

            case _ if HandAnalyzer.is_straight(cards):
                return HandRanks.STRAIGHT

            case _ if most_common[0][1] == 3:
                return HandRanks.THREE_OF_A_KIND

            case _ if most_common[0][1] == 2 and most_common[1][1] == 2:
                return HandRanks.TWO_PAIR

            case _ if most_common[0][1] == 2:
                return HandRanks.PAIR

            case _:
                return HandRanks.HIGH_CARD

    @staticmethod
    def best_hand(cards):
        """Find the best 5-card hand from the 7 available cards."""
        best = max(combinations(cards, 5), key=lambda hand: HandAnalyzer.hand_rank(hand).value)
        return best, HandAnalyzer.hand_rank(best)

    @staticmethod
    def calculate_hand_probabilities(num_simulations=1000000):
        """Calculate the probabilities of each hand type by simulating poker hands."""
        hand_counts = Counter()
        evaluator = Evaluator()

        for _ in range(num_simulations):
            deck = Deck()
            deck.shuffle()
            cards = [deck.draw(1) for _ in range(7)]
            hand_rank = evaluator.evaluate(cards[:2], cards[2:])
            hand_counts[hand_rank] += 1

        probabilities = {hand: (count / num_simulations) * 100 for hand, count in hand_counts.items()}
        return probabilities

# Example usage
if __name__ == "__main__":
    probabilities = HandAnalyzer.calculate_hand_probabilities()
    for hand, probability in probabilities.items():
        print(f"{hand}: {probability:.2f}%")