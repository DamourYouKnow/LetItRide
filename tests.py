import unittest
from core import Deck, Card

class TestMethods(unittest.TestCase):
    def test_create_deck(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52, "Deck does not equal 52 cards")


if __name__ == '__main__':
    unittest.main()