import unittest
from core import Deck, Card, Hand, Suite, Game, Player

class TestMethods(unittest.TestCase):
    def test_create_deck(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52, "Deck does not equal 52 cards")
        deck = Deck(2)
        self.assertEqual(len(deck.cards), 104, "Deck does not equal 104 cards")

    def test_draw(self):
        deck = Deck()
        deck_size = len(deck)
        card = deck.draw()

        self.assertEqual(len(deck), deck_size - 1, "Card not removed from deck")
        self.assertIsInstance(card, Card, "Draw does not return card")


if __name__ == '__main__':
    unittest.main()