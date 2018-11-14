import unittest
from core import Deck, Card, Hand, Suite, Game, Player

class TestMethods(unittest.TestCase):
    def test_create_deck(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52, "Deck does not equal 52 cards")
        deck = Deck(2)
        self.assertEqual(len(deck.cards), 104, "Deck does not equal 104 cards")

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

    def test_draw(self):
        deck = Deck()
        deck_size = len(deck)
        card = deck.draw()

        self.assertEqual(len(deck), deck_size - 1, "Card not removed from deck")
        self.assertIsInstance(card, Card, "Draw does not return card")

    def test_hit(self):
        game = Game()
        player = Player(game)
        deck_size = len(game.deck)
        player.hit()

        self.assertEqual(
                len(game.deck), deck_size - 1, "Card not removed from deck") 

        self.assertEqual(len(player.hand), 1, "Card not added to player hand")

if __name__ == '__main__':
    unittest.main()