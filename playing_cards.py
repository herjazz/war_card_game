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

    Attributes:
        rank (str): rank of card
        suit (str): suit of card
    """

    def __init__(self, rank: str, suit: str):
        """
        Initializes class attributes

        Args:
           rank (str): rank of card
           suit (str): suit of card
        """

        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        """ Represents an instance of Card with rank then suit """
        return f'{self.rank} of {self.suit}'

def create_deck() -> list[Card]:
    """ Creates an unshuffled standard deck of cards as a list """
    return [Card(rank, suit.value) for rank in ranks for suit in Suit]
