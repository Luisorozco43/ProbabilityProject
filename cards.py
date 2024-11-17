import random
from itertools import combinations

class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    # Implementing build in methods so that you can print a card object
    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()
        
    def show(self):
        if self.value == 1:
            val = "Ace"
        elif self.value == 11:
            val = "Jack"
        elif self.value == 12:
            val = "Queen"
        elif self.value == 13:
            val = "King"
        else:
            val = self.value

        return "{} of {}".format(val, self.suit)


class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    # Display all cards in the deck
    def show(self):
        for card in self.cards:
            print(card.show())

    # Generate 52 cards
    def build(self):
        self.cards = []
        for suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
            for val in range(1,14):
                self.cards.append(Card(suit, val))

    # Shuffle the deck
    def shuffle(self, num=1):
        length = len(self.cards)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.cards[i], self.cards[randi] = self.cards[randi], self.cards[i]
            # You can also use the build in shuffle method
            # random.shuffle(self.cards)

    # Return the top card
    def deal(self):
        return self.cards.pop()


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []

    def sayHello(self):
        print("Hi! My name is {}".format(self.name))
        return self

    # Draw n number of cards from a deck
    # Returns true in n cards are drawn, false if less then that
    def draw(self, deck, num=1):
        for _ in range(num):
            card = deck.deal()
            if card:
                self.hand.append(card)
            else: 
                return False
        return True

    # Display all the cards in the players hand
    def show_hand(self):
        print("{}'s hand: {}".format(self.name, self.hand))
        return self

    def discard(self):
        return self.hand.pop()

# Sample Space Generator for Card Games:
# Simulate a deck of cards and generate the sample space of all possible outcomes when drawing one or more cards.
# Show all possible combinations and their probability of occurrence.


def generate_sample_space(deck, num_cards):
    sample_space = list(combinations(deck.cards, num_cards))
    total_outcomes = len(sample_space)
    probability = 1 / total_outcomes if total_outcomes > 0 else 0

    print(f"Total possible outcomes when drawing {num_cards} card(s): {total_outcomes}")
    print(f"Probability of each outcome: {probability:.6f}")

    for outcome in sample_space:
        print(", ".join(str(card) for card in outcome))

#get the input from the user and generate the sample space based on the input on the console

def main():
    deck = Deck()
    deck.shuffle()

    while True:
        try:
            num_cards = int(input("Enter the number of cards to draw: "))
            if num_cards < 1:
                print("Please enter a number greater than 0.")
                continue
            generate_sample_space(deck, num_cards)
            break
        except ValueError:
            print("Please enter a valid number.")
        

if __name__ == '__main__':
    main()
