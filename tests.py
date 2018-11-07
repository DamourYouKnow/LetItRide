import unittest
from core import Deck, Card, Hand, Suite

class TestMethods(unittest.TestCase):
    def test_create_deck(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52, "Deck does not equal 52 cards")

    def test_hand_value(self):
        hand = Hand()
        hand._cards = [
            Card(11, Suite.clubs),
            Card(1, Suite.clubs),
            Card(1, Suite.clubs),
            Card(2, Suite.clubs)        
        ]

        values = hand.values
        
        self.assertEqual(len(values), 3)
        self.assertEqual(values[0], 14)
        self.assertEqual(values[1], 24)
        self.assertEqual(values[2], 34)


if __name__ == '__main__':
    unittest.main()