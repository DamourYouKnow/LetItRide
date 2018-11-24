import unittest
from core import Deck, Card, Hand, Suite, Game, Player, HandType

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

    def test_royal_flush(self):
        cards = [
            Card(1, Suite.clubs),
            Card(10, Suite.clubs),
            Card(11, Suite.clubs),
            Card(12, Suite.clubs),
            Card(13, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.royal_flush)

    def test_straight_flush(self):
        cards = [
            Card(4, Suite.clubs),
            Card(5, Suite.clubs),
            Card(6, Suite.clubs),
            Card(7, Suite.clubs),
            Card(8, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.straight_flush)

    def test_four_of_kind(self):
        cards = [
            Card(4, Suite.clubs),
            Card(4, Suite.hearts),
            Card(4, Suite.diamonds),
            Card(4, Suite.spades),
            Card(8, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.four_of_kind)

    def test_full_house(self):
        cards = [
            Card(4, Suite.clubs),
            Card(4, Suite.hearts),
            Card(4, Suite.diamonds),
            Card(8, Suite.spades),
            Card(8, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.full_house)

    def test_flush(self):
        cards = [
            Card(2, Suite.clubs),
            Card(4, Suite.clubs),
            Card(6, Suite.clubs),
            Card(8, Suite.clubs),
            Card(10, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.flush)

    def test_straight(self):
        cards = [
            Card(1, Suite.hearts),
            Card(2, Suite.clubs),
            Card(3, Suite.clubs),
            Card(4, Suite.clubs),
            Card(5, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.straight)

        cards = [
            Card(1, Suite.hearts),
            Card(10, Suite.clubs),
            Card(11, Suite.clubs),
            Card(12, Suite.clubs),
            Card(13, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.straight)

    def test_three_of_kind(self):
        cards = [
            Card(1, Suite.hearts),
            Card(1, Suite.clubs),
            Card(1, Suite.diamonds),
            Card(2, Suite.clubs),
            Card(3, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.three_of_kind)

    def test_two_pair(self):
        cards = [
            Card(1, Suite.hearts),
            Card(1, Suite.clubs),
            Card(2, Suite.diamonds),
            Card(2, Suite.clubs),
            Card(3, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.two_pair)

    def test_high_pair(self):
        cards = [
            Card(1, Suite.hearts),
            Card(1, Suite.clubs),
            Card(2, Suite.diamonds),
            Card(3, Suite.clubs),
            Card(4, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.high_pair)

    def test_pair(self):
        cards = [
            Card(1, Suite.hearts),
            Card(2, Suite.clubs),
            Card(2, Suite.diamonds),
            Card(3, Suite.clubs),
            Card(4, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.pair)

    def test_high(self):
        cards = [
            Card(3, Suite.hearts),
            Card(5, Suite.clubs),
            Card(6, Suite.diamonds),
            Card(7, Suite.clubs),
            Card(8, Suite.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.high)

if __name__ == '__main__':
    unittest.main()