from enum import Enum


# Mapping for Spanish translations outside the enum class
SPANISH_NAMES = {
    1: "Carta Alta",
    2: "Par",
    3: "Doble Par",
    4: "Trío",
    5: "Escalera",
    6: "Color",
    7: "Full House",
    8: "Póker",
    9: "Escalera de Color",
    10: "Escalera Real",
}


class HandRanks(Enum):
    HIGH_CARD = 1  # High card
    PAIR = 2  # One pair
    TWO_PAIR = 3  # Two pair
    THREE_OF_A_KIND = 4  # Three of a kind
    STRAIGHT = 5  # Straight
    FLUSH = 6  # Flush
    FULL_HOUSE = 7  # Full house
    FOUR_OF_A_KIND = 8  # Four of a kind
    STRAIGHT_FLUSH = 9  # Straight flush
    ROYAL_FLUSH = 10  # Royal flush

    @classmethod
    def get_name(cls, rank):
        """
        Get the name of the poker hand in Spanish.
        Assumes `rank` can be either an integer or an instance of HandRanks.
        """
        # Ensure rank is an integer value (from enum instance or raw value)
        rank_value = rank.value if isinstance(rank, cls) else rank

        # Access SPANISH_NAMES dictionary directly
        return SPANISH_NAMES.get(rank_value, "Rango de Mano Desconocido")
