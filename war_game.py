# TODO: when down to 2 players the game often doesn't seem to finish
# TODO: Break down main() into functions OR make a WarGame class
import random
import sys
import playing_cards as pc

# Card points - Aces high
war_scores = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class WarPlayer(pc.CardPlayer):
    """
    Represents a card player of game of war

    Attributes:
        name (str): name of player
        deck (list[pc.Card]): deck of cards -> class Card from playing_cards
        discarded (list[pc.Card]): empty list for discarded cards
    """

    def __init__(self, name: str, deck: list[pc.Card] = None):
        """
        Initializes class attributes

        Args:
           name (str): name of player
           deck (list[pc.Card]): deck of cards
           discarded (list[pc.Card]): empty list for discarded cards
        """

        super().__init__(name, deck)
        self.discarded: list[pc.Card] = []

    def play_hand(self) -> pc.Card:
        """
        Represents a turn by a player of game of war.
        one card is popped from self.deck and added to
        self.discarded,

        Returns:
            played_card (pc.Card)
        """

        played_card = self.deck.pop()
        self.discarded.append(played_card)
        print(f"{self.name}'s card is {played_card}.")
        return played_card

    def add_cards(self, cards: list[pc.Card]) -> None:
        """
        Adds cards to "bottom" of deck

        Args:
            cards (list[pc.Card]): list of cards to add
        """

        self.deck = cards + self.deck

    def __str__(self) -> str:
        """Prints number of cards left in self.deck"""
        return f"{self.name} has {len(self.deck)} card(s) left."


def choose_num_players() -> int:
    """Function to choose number of players; exits after 5 failed attempts"""
    attempts: int = 0
    while attempts < 5:
        num_players = input("How many players? (Choose 2, 3, or 4): ")
        if num_players in ("2", "3", "4"):
            print(f"You have chosen {num_players} players.")
            return int(num_players)
        attempts += 1
        print("Invalid input, try again.")
    sys.exit("Too many failed attempts. Exiting.")


def create_players(deck: list[pc.Card], num_players: int) -> list[WarPlayer]:
    """Create a list of players with decks"""
    random.shuffle(deck)
    deck_size: int = len(deck) // num_players
    decks = (deck[i : i + deck_size] for i in range(0, len(deck), deck_size))
    return [WarPlayer(f"Player {n + 1}", next(decks)) for n in range(num_players)]


def num_winners(scores: list[int], top_score: int) -> int:
    """Return the number of values that match a top score"""
    return sum(1 for v in scores.values() if v == top_score)


def check_winner(scores_dict: dict[WarPlayer, int], war: bool = False) -> None:
    """Print name of winner and update their deck with won cards"""
    winnings: list[pc.Card] = []
    for player in scores_dict.keys():
        if war:
            winnings += player.discarded
            player.discarded = []
        else:
            winnings.append(player.discarded.pop())
    winner: WarPlayer = max(scores_dict, key=scores_dict.get)
    print(f"{winner.name} wins the hand!")
    winner.add_cards(winnings)


def main():
    players: list[WarPlayer] = create_players(pc.create_deck(), choose_num_players())
    round_scores: dict[WarPlayer, int] = {}
    num_rounds: int = 0

    while num_rounds < 10:
        for player in players:
            card: pc.Card = player.play_hand()
            round_scores[player] = war_scores[card.rank]
        max_score: int = max(round_scores.values())
        war_play: bool = False
        # Play war
        while num_winners(round_scores, max_score) > 1:
            war_play = True
            print("WAR!")
            remaining_players: list[WarPlayer] = []
            for pl, score in round_scores.items():
                if score == max_score:
                    remaining_players.append(pl)
                else:
                    # Reset non-playing player's score
                    round_scores[pl] = 0
            for player in remaining_players:
                if len(player.deck) == 1:
                    card = player.deck.pop()
                else:
                    player.discarded.append(player.deck.pop())
                    card = player.play_hand()
                round_scores[player] = war_scores[card.rank]
        if war_play:
            check_winner(round_scores, war=True)
        else:
            check_winner(round_scores)
        survivors: list[WarPlayer] = []
        for player in players:
            if player.deck:
                survivors.append(player)
                print(player)
            else:
                # Remove any players whose decks are empty
                print(f"Goodbye to {player.name}")
                del round_scores[player]
        if len(survivors) == 1:
            print("GAME OVER!")
            print(f"{survivors[0].name} is the winner!")
            sys.exit()
        else:
            players = survivors
            input("press any key to proceed")
        num_rounds += 1

    # Find player with largest deck
    largest_deck_size: int = max([len(pl.deck) for pl in players])
    biggest_decks: list[WarPlayer] = [
        pl for pl in players if len(pl.deck) == largest_deck_size
    ]
    print("Maximum number of rounds exceeded!")
    print("The winner will be the player with the most cards.")
    if len(biggest_decks) == 1:
        print(f"{biggest_decks[0].name} has the most cards - they are the winner!")
    else:
        # Tiebreak
        # TODO: deal with a 3-way tiebreak
        print(
            f"TIEBREAK!!! between {biggest_decks[0].name} and {biggest_decks[1].name}!"
        )
        cards: list[int] = []
        for pl in biggest_decks:
            card = pl.play_hand()
            cards.append(war_scores[card.rank])
        if len(set(cards)) == 1:
            # TODO: Add code to deal with same cards
            print("Try again")
        else:
            winner: int = cards.index(max(cards))
            print(f"{biggest_decks[winner].name} wins via tiebreak!")


if __name__ == "__main__":
    main()
