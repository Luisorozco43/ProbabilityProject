import random
import matplotlib.pyplot as plt
from utils.hand_analyzer import HandAnalyzer
from utils.hand_rankings import HandRanks

class ProbabilityCalculator:
    """
    Utility class for calculating the probability of getting a specific poker hand.
    Optimized for better performance by sampling a subset of possibilities.
    """

    SAMPLE_SIZE = 100000  # Define a fixed number of samples for simulation

    @staticmethod
    def calculate_probability(match, player_index, target_hand_rank):
        """
        Calculate the probability of getting a specific hand rank.

        Args:
            match (Match): The current Match instance.
            player_index (int): Index of the player for whom the probability is calculated.
            target_hand_rank (HandRanks): The desired hand rank to calculate probability for.

        Returns:
            float: Probability (as a percentage) of achieving the target hand rank.
        """
        deck = match.deck  # Use the existing deck from the match
        known_cards = match.get_full_hand(player_index)  # Player's hand + community cards
        remaining_deck = [card for card in deck.cards if card not in known_cards]

        community_cards = match.get_community_cards()
        needed_cards = 5 - len(community_cards)  # Number of community cards yet to be dealt
        target_hands_count = 0
        total_samples = 0

        if needed_cards <= 0:
            # No cards needed, evaluate the current hand directly
            _, hand_rank = HandAnalyzer.best_hand(known_cards)
            return 100.0 if hand_rank == target_hand_rank else 0.0

        # Sample combinations randomly
        for _ in range(ProbabilityCalculator.SAMPLE_SIZE):
            sampled_cards = random.sample(remaining_deck, needed_cards)
            full_hand = known_cards + sampled_cards

            _, hand_rank = HandAnalyzer.best_hand(full_hand)
            total_samples += 1
            if hand_rank == target_hand_rank:
                target_hands_count += 1

        # Calculate probability
        probability = (
            (target_hands_count / total_samples) * 100 if total_samples > 0 else 0
        )
        return probability

    @staticmethod
    def plot_probability_tree(probabilities):
        """
        Dibuja un diagrama de árbol con las probabilidades condicionales.
        """
        stages = ['Inicio', 'Flop', 'Turn', 'River']  # Etapas del juego
        plt.figure(figsize=(10, 6))

        for i, prob in enumerate(probabilities):
            plt.plot([i, i], [0, prob], label=f'{stages[i]}', marker='o')

        plt.xlabel('Etapas del Juego')
        plt.ylabel('Probabilidad (%)')
        plt.title('Diagrama de Probabilidad Condicional')
        plt.grid(True)
        plt.legend()
        plt.show()

    @staticmethod
    def menu(match, player_index):
        """
        Display a menu for selecting a target hand rank and calculate its probability.

        Args:
            match (Match): The current Match instance.
            player_index (int): Index of the player for whom the probability is calculated.
        """
        print("\n--- Calcular Probabilidades ---")
        for rank in HandRanks:
            print(f"{rank.value}. {HandRanks.get_name(rank)}")

        while True:
            try:
                choice = int(input("\nSelecciona el rango de mano deseado (1-10): "))
                target_hand_rank = HandRanks(choice)
                break
            except (ValueError, KeyError):
                print("Por favor ingresa una opción válida.")

        # Calcular la probabilidad
        probability = ProbabilityCalculator.calculate_probability(
            match, player_index, target_hand_rank
        )
        print(
            f"\nProbabilidad de obtener {HandRanks.get_name(target_hand_rank)}: {probability:.2f}%"
        )

        # Registrar las probabilidades en cada etapa
        probabilities = [probability]  # Inicializamos con la probabilidad antes del flop

        # Después de cada etapa, recalculamos las probabilidades
        #match.draw_flop()
        probabilities.append(ProbabilityCalculator.calculate_probability(match, player_index, target_hand_rank))

        #match.draw_turn()
        probabilities.append(ProbabilityCalculator.calculate_probability(match, player_index, target_hand_rank))

        #match.draw_river()
        probabilities.append(ProbabilityCalculator.calculate_probability(match, player_index, target_hand_rank))

        # Mostrar el diagrama de probabilidad
        ProbabilityCalculator.plot_probability_tree(probabilities)
