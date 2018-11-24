import random
from enum import Enum
from typing import List
    
class Suite(Enum):
    """
    Enum describing all possible card suites.
    """
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

        return strings[self]

    def to_char(self) -> str:
        chars = {
            Suite.diamonds: 'D',
            Suite.clubs: 'C',
            Suite.hearts: 'H',
            Suite.spades: 'S'
        }

        return chars[self]


class HandType(Enum):
    """
    Enum describing all possible hand types.
    """
    royal_flush = 1
    straight_flush = 2
    four_of_kind = 3
    full_house = 4
    flush = 5
    straight = 6
    three_of_kind = 7
    two_pair = 8
    high_pair = 9
    pair = 10
    high = 11

    def __str__(self) -> str:
        strings = {
            HandType.royal_flush: "royal flush",
            HandType.straight_flush: "straight flush",
            HandType.four_of_kind: "four of a kind",
            HandType.full_house: "full house",
            HandType.flush: "flush",
            HandType.straight: "straight",
            HandType.three_of_kind: "three of a kind",
            HandType.two_pair: "two pair",
            HandType.high_pair: "high pair",
            HandType.pair: "pair",
            HandType.high: "high"
        }

        return strings[self]


class Card:
    """
    Class representing a playing card.
    """
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

    @property
    def filename(self):
        return "./assets/" + str(self.rank) + self.suite.to_char() 

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
    """
    Class representing the hand of a player or banker.
    """
    def __init__(self, cards: List[Card]=[]):
        self._cards = cards

    @property
    def cards(self) -> List[Card]:
        return self._cards

    def __len__(self):
        return len(self._cards)

    @property
    def type(self) -> HandType:
        hand = self._cards.copy()
        hand.sort()
        size = len(hand)

        royals = [1, 10, 11, 12, 13]
        ranks = [card.rank for card in hand]
        is_royal = all([c.rank in royals for c in hand])
        is_straight = ranks == list(range(ranks[0], ranks[-1] + 1)) or is_royal
        is_flush = len([c for c in hand if c.suite == hand[0].suite]) == size

        if is_royal and is_flush:
            return HandType.royal_flush
        if is_straight and is_flush:
            return HandType.straight_flush
        if is_straight:
            return HandType.straight
        if is_flush:
            return HandType.flush

        count_map = {
            c.rank: len([c2 for c2 in hand if c2.rank == c.rank]) for c in hand
        }
        counts = list(count_map.values())

        if counts.count(4) == 1:
            return HandType.four_of_kind
        if counts.count(3) == 1 and counts.count(2) == 1:
            return HandType.full_house
        if counts.count(3) == 1:
            return HandType.three_of_kind
        if counts.count(2) == 2:
            return HandType.two_pair
        if counts.count(2) == 1:
            if [c for c in hand if c.rank in royals and count_map[c.rank] == 2]:
                return HandType.high_pair
            else:
                return HandType.pair

        return HandType.high


class Deck:
    """
    Class representing a deck of cards.
    """
    def __init__(self, count: int=1):
        self._cards = Deck._create_deck(count)

    @property
    def cards(self) -> List[Card]:
        return self._cards

    def draw(self) -> Card:
        return self._cards.pop()

    def shuffle(self):
        random.shuffle(self._cards)

    def __len__(self):
        return len(self._cards)

    @staticmethod
    def _create_deck(count: int=1) -> List[Card]:
        deck = []
        for _ in range(0, count):
            for i in range(1, 14):
                deck.append(Card(i, Suite.clubs))
                deck.append(Card(i, Suite.diamonds))
                deck.append(Card(i, Suite.hearts))
                deck.append(Card(i, Suite.spades))
        return deck


class Game:
    """
    Class representing a blackjack game.
    """
    def __init__(self):
        self._deck = Deck(2)
        self._player = None

    @property
    def deck(self) -> Deck:
        return self._deck
    
    @property
    def player(self) -> 'Player':
        return self._player

    
class Player:
    """
    Class representing a player.
    """
    def __init__(self, game: Game, name: str="Player"):
        self._game = game
        self._name = name
        self._money = 0
        self._current_bet = 0
        self._hand = Hand()

    @property
    def name(self) -> str:
        return self._name

    @property 
    def money(self) -> int:
        return self._money

    @property
    def hand(self) -> Hand:
        return self._hand

    def draw(self, count: int=1):
        for _ in range(0, count):
            self._hand.cards.append(self._game.deck.draw())

