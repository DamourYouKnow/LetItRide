import random
from enum import Enum
from typing import List
    
class Suite(Enum):
    diamonds = 1
    clubs = 2
    hearts = 3
    spades = 4

    def __str__(self) -> str:
        strings = {
            Suite.diamonds: "diamonds",
            Suite.clubs: "clubs",
            Suite.hearts: "hearts",
            Suite.spades: "spades"
        }

        return strings[self.value]


class Card:
    rank_strings = {
        1: "ace",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "jack",
        12: "queen",
        13: "king"
    }

    def __init__(self, rank: int, suite: Suite):
        self._rank = rank
        self._suite = suite

    @property
    def rank(self):
        return self._rank

    @property
    def suite(self):
        return self._suite

    def __eq__(self, other: 'Card') -> bool:
        return self.rank == other.rank and self.suite == other.suite

    def __ne__(self, other: 'Card') -> bool:
        return not self == other

    def __gt__(self, other: 'Card') -> bool:
        return self.rank > other.rank

    def __ge__(self, other: 'Card') -> bool:
        return self.rank >= other.rank

    def __lt__(self, other: 'Card') -> bool:
        return self.rank < other.rank

    def __le__(self, other: 'Card') -> bool:
        return self.rank <= other.rank

    def __str__(self) -> str:
        return self._rank_str().title() + " of " + str(self._suite).title()
   
    def _rank_str(self) -> str:
        return Card.rank_strings[self._rank]


class Hand:
    def __init__(self):
        self._cards = []

    @property
    def values(self):
        vals = [0]
        for card in self._cards:
            if card.rank >= 2 and card.rank <= 10:
                vals = [val + card.rank for val in vals]
            elif card.rank >= 11 and card.rank <= 13:
                vals = [val + 10 for val in vals]
            elif card.rank == 1:
                vals = [val + 11 for val in vals] + [val + 1 for val in vals]
        return sorted(vals)


class Deck:
    def __init__(self):
        self._cards = Deck._create_deck()

    @property
    def cards(self) -> List[Card]:
        return self._cards

    def draw(self) -> Card:
        return self._cards.pop()

    def shuffle(self):
        random.shuffle(self._cards)

    @staticmethod
    def _create_deck() -> List[Card]:
        deck = []
        for i in range(1, 14):
            deck.append(Card(i, Suite.clubs))
            deck.append(Card(i, Suite.diamonds))
            deck.append(Card(i, Suite.hearts))
            deck.append(Card(i, Suite.spades))
        return deck
