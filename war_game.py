# TODO: when down to 2 players the game often doesn't seem to finish
import random
import sys
import playing_cards as pc

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
    "A": 14
}


class Player:
    
    def __init__(self, name, deck=None):
        self.name = name
        if not deck:
            self.deck = []
        else:
            self.deck = deck
        self.discarded = []

    def play_hand(self):
        played_card = self.deck.pop()
        self.discarded.append(played_card)
        print(f"{self.name}'s card is {played_card}.")
        return played_card
    
    def add_cards(self, cards):
        self.deck = cards + self.deck

    def __str__(self):
        return f'{self.name} has {len(self.deck)} card(s) left.'

    def __repr__(self):
        return f'Player({self.name}, {self.deck})'


def choose_num_players() -> int:
    attempts = 0
    while attempts < 5:
        num_players = input("How many players? (Choose 2, 3, or 4): ")
        if num_players in ("2", "3", "4"):
            print(f"You have chosen {num_players} players.")
            return int(num_players)
        attempts += 1
        print("Invalid input, try again.")
    sys.exit("Too many failed attempts. Exiting.")


def create_players(deck, num_players: int) -> list[Player]:
    """ Create a list of players with decks """
    random.shuffle(deck)
    deck_size: int = len(deck) // num_players
    decks = (deck[i:i + deck_size] for i in range(0, len(deck), deck_size))
    return [Player(f'Player {n + 1}', next(decks)) for n in range(num_players)]


def num_winners(scores: list[int], top_score: int) -> int:
    return sum(1 for v in scores.values() if v == top_score)


def check_winner(scores_dict: dict[Player, int], war: bool = False) -> None:
    winnings: list[pc.Card] = []
    winner: Player = max(scores_dict, key=scores_dict.get)
    print(f"{winner.name} wins the hand!")
    for player in scores_dict.keys():
        if war:
            winnings += player.discarded
            player.discarded = []
        else:
            winnings.append(player.discarded.pop())
    winner.add_cards(winnings)


def main():
    players: list[Player] = create_players(pc.create_deck(), choose_num_players())
    round_scores: dict[Player, int] = {}

    while True:
        for player in players:
            card = player.play_hand()
            round_scores[player] = war_scores[card.rank]
        max_score = max(round_scores.values())
        war_play: bool = False
        # Play war
        while num_winners(round_scores, max_score) > 1:
            war_play = True
            print("WAR!")
            remaining_players = []
            for pl, score in round_scores.items():
                if score == max_score:
                    remaining_players.append(pl)
                else:
                    # To ensure "loser" doesn't have highest score if war cards end up lower
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
        survivors = []
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


if __name__ == "__main__":
    main()
