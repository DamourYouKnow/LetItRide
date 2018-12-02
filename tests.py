import unittest
from core import Deck, Card, Hand, Suit, Game, Player, HandType, Statistics

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
            Card(1, Suit.clubs),
            Card(10, Suit.clubs),
            Card(11, Suit.clubs),
            Card(12, Suit.clubs),
            Card(13, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.royal_flush)

    def test_straight_flush(self):
        cards = [
            Card(4, Suit.clubs),
            Card(5, Suit.clubs),
            Card(6, Suit.clubs),
            Card(7, Suit.clubs),
            Card(8, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.straight_flush)

    def test_four_of_kind(self):
        cards = [
            Card(4, Suit.clubs),
            Card(4, Suit.hearts),
            Card(4, Suit.diamonds),
            Card(4, Suit.spades),
            Card(8, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.four_of_kind)

    def test_full_house(self):
        cards = [
            Card(4, Suit.clubs),
            Card(4, Suit.hearts),
            Card(4, Suit.diamonds),
            Card(8, Suit.spades),
            Card(8, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.full_house)

    def test_flush(self):
        cards = [
            Card(2, Suit.clubs),
            Card(4, Suit.clubs),
            Card(6, Suit.clubs),
            Card(8, Suit.clubs),
            Card(10, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.flush)

    def test_straight(self):
        cards = [
            Card(1, Suit.hearts),
            Card(2, Suit.clubs),
            Card(3, Suit.clubs),
            Card(4, Suit.clubs),
            Card(5, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.straight)

        cards = [
            Card(1, Suit.hearts),
            Card(10, Suit.clubs),
            Card(11, Suit.clubs),
            Card(12, Suit.clubs),
            Card(13, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.straight)

    def test_three_of_kind(self):
        cards = [
            Card(1, Suit.hearts),
            Card(1, Suit.clubs),
            Card(1, Suit.diamonds),
            Card(2, Suit.clubs),
            Card(3, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.three_of_kind)

    def test_two_pair(self):
        cards = [
            Card(1, Suit.hearts),
            Card(1, Suit.clubs),
            Card(2, Suit.diamonds),
            Card(2, Suit.clubs),
            Card(3, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.two_pair)

    def test_high_pair(self):
        cards = [
            Card(1, Suit.hearts),
            Card(1, Suit.clubs),
            Card(2, Suit.diamonds),
            Card(3, Suit.clubs),
            Card(4, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.high_pair)

    def test_pair(self):
        cards = [
            Card(1, Suit.hearts),
            Card(2, Suit.clubs),
            Card(2, Suit.diamonds),
            Card(3, Suit.clubs),
            Card(4, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.pair)

    def test_high(self):
        cards = [
            Card(3, Suit.hearts),
            Card(5, Suit.clubs),
            Card(6, Suit.diamonds),
            Card(7, Suit.clubs),
            Card(8, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).type, HandType.high)

    def test_payout(self):
        cards = [
            Card(3, Suit.hearts),
            Card(5, Suit.clubs),
            Card(6, Suit.diamonds),
            Card(7, Suit.clubs),
            Card(8, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).payout(1), 0)

        cards = [
            Card(1, Suit.hearts),
            Card(1, Suit.clubs),
            Card(1, Suit.diamonds),
            Card(2, Suit.clubs),
            Card(3, Suit.clubs)
        ]
        self.assertEqual(Hand(cards).payout(1), 3 + 1)

    def test_card_str(self):
        self.assertEqual(str(Card(1, Suit.clubs)), "AC")
        self.assertEqual(str(Card(2, Suit.diamonds)), "2D")
        self.assertEqual(str(Card(11, Suit.hearts)), "JH")
        
    def test_expected_val(self):
        hand = [Card(3, Suit.clubs), Card(3, Suit.spades), Card(10, Suit.clubs)]
        probabilityDistribution = Statistics.probabilityDistribution(hand)
        expectedDistribution = dict()
        expectedDistribution[HandType.pair] = 880
        expectedDistribution[HandType.two_pair] = 198
        expectedDistribution[HandType.three_of_kind] = 88
        expectedDistribution[HandType.full_house] = 9
        expectedDistribution[HandType.four_of_kind] = 1
        for k,v in probabilityDistribution.items():
            if k in expectedDistribution:
                self.assertEqual(v, expectedDistribution[k])
            else:
                self.assertEqual(v, 0)
        self.assertEqual(sum(probabilityDistribution.values()), 1176)

    def test_expected_pull(self):
        hand = [Card(3, Suit.clubs), Card(3, Suit.spades), Card(10, Suit.clubs)]
        self.assertEqual(Statistics.shouldRide(hand), False)
    
    def test_expected_ride(self):
        hand = [
            Card(11, Suit.clubs), 
            Card(11, Suit.spades), 
            Card(12, Suit.clubs)
        ]
        self.assertEqual(Statistics.shouldRide(hand), True)

if __name__ == '__main__':
    unittest.main()