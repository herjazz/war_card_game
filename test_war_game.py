import unittest
import playing_cards as pc
from war_game import WarPlayer


class TestWarPlayer(unittest.TestCase):
    """Tests for the class WarPlayer"""

    def setUp(self):
        """Create common items for test methods"""
        deck = pc.create_deck()
        self.cards = deck[5:10]
        self.player = WarPlayer("Test Player", deck)

    def test_play_hand_card(self):
        """Check card popped is 'top card' in deck"""
        top_card = self.player.deck[-1]
        card = self.player.play_hand()
        self.assertEqual(card, top_card)

    def test_play_hand_discarded(self):
        """Check card gets added to discard pile"""
        card = self.player.play_hand()
        self.assertEqual(card, self.player.discarded[-1])

    def test_add_cards(self):
        """Check card gets added to discard pile"""
        self.player.add_cards(self.cards)
        self.assertEqual(self.cards, self.player.deck[:5])

    def test_add_cards_empty(self):
        """Check card gets added to discard pile"""
        previous_length = len(self.player.deck)
        self.player.add_cards([])
        self.assertEqual(previous_length, len(self.player.deck))


if __name__ == "__main__":
    unittest.main()
