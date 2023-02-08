# playing_cards.py

import enum 

ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
class Suit(enum.Enum):
    SPADES = chr(9824)
    HEARTS = chr(9829)
    DIAMONDS = chr(9830)
    CLUBS = chr(9827)


class Card:

    """
    Card represents a single playing card
    """

    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        return f'{self.rank} of {self.suit}'

def create_deck():
    return [Card(rank, suit.value) for rank in ranks for suit in Suit]

# class CardVal:
#     def __init__(self, value: int, suit: str):
#         self.value = value
#         self.suit = suit

#     def __repr__(self) -> str:
#         match self.value:
#             case 1 | 14:
#                 rank = "A"
#             case 11:
#                 rank = "J"
#             case 12:
#                 rank = "Q"
#             case 13:
#                 rank = "K"
#             case _:
#                 rank = self.value
#         match self.suit:
#             case "spades":
#                 suit = chr(9824) # Character 9824 is '♠'.
#             case "clubs":
#                 suit = chr(9827) # Character 9827 is '♣'.
#             case "hearts":
#                 suit = chr(9829) # Character 9829 is '♥'.
#             case "diamonds":
#                 suit = chr(9830) # Character 9830 is '♦'.
#         return f'{rank} of {suit}'
