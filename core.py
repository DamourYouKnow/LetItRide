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
            Suite.diamonds: "D",
            Suite.clubs: "C",
            Suite.hearts: "H",
            Suite.spades: "S"

        }
        return strings[self]


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
            HandType.royal_flush: "Royal Flush",
            HandType.straight_flush: "Straight Flush",
            HandType.four_of_kind: "Four of a Kind",
            HandType.full_house: "Full House",
            HandType.flush: "Flush",
            HandType.straight: "Straight",
            HandType.three_of_kind: "Three of a Kind",
            HandType.two_pair: "Two Pair",
            HandType.high_pair: "10s or Better",
            HandType.pair: "Nothing",
            HandType.high: "Nothing"
        }
        return strings[self]


class Card:
    """
    Class representing a playing card.
    """
    def __init__(self, rank: int, suite: Suite):
        self._rank = rank
        self._suite = suite

    @property
    def rank(self):
        return self._rank

    @property
    def suite(self):
        return self._suite

    def __str__(self):
        return str(self.rank) + str(self.suite)

    @property
    def filename(self):
        return "./assets/" + str(self.rank) + str(self.suite) + ".png"

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
        rank_str = str(self._rank)
        if self._rank == 1 or self._rank >= 11:
            rank_str = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}[self._rank]
        return rank_str + str(self._suite)


class Hand:
    """
    Class representing the hand of a player or banker.
    """
    main_payouts = {
        HandType.royal_flush: 1000,
        HandType.straight_flush: 200,
        HandType.four_of_kind: 50,
        HandType.full_house: 11,
        HandType.flush: 8,
        HandType.straight: 5,
        HandType.three_of_kind: 3,
        HandType.two_pair: 2,
        HandType.high_pair: 1
    }

    def __init__(self, cards: List[Card]=[]):
        self._cards = cards

    @property
    def cards(self) -> List[Card]:
        return self._cards

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        for card in self._cards:
            yield card

    @property
    def payout(self) -> int:
        if self.type in Hand.main_payouts:
            return Hand.main_payouts[self.type]
        return 0

    def playerCards(self) -> List[Card]:
        return self.cards[0:3]

    def firstBet(self) -> Card:
        return self.cards[3]
    
    def secondBet(self) -> Card:
        return self.cards[4]

    @property
    def type(self) -> HandType:
        hand = self._cards.copy()
        hand.sort()
        size = len(hand)

        royals = [1, 10, 11, 12, 13]
        ranks = [card.rank for card in hand]
        is_royal = all([r in ranks for r in royals])
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

    def drawHand(self, num: int = 5) -> Card:
        hand = []
        for i in range(0,num):
            hand.append(self.draw())
        return hand

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
    def __init__(self, decks: int = 1, name: str="Player", money: int = 1000):
        self._deck_count = decks
        self._deck = Deck(decks)
        self._player = Player(self, name, money)
        self._current_bet_0 = 0
        self._current_bet_1 = 0
        self._current_bet_2 = 0
        self.deck.shuffle()

    @property
    def deck(self) -> Deck:
        return self._deck
    
    @property
    def player(self) -> 'Player':
        return self._player
    
    def deal(self):
        self.player.setHand(Hand(self.deck.drawHand()))

    def payout(self) -> int:
        payout = (self.player.hand.payout+1)*(self._current_bet_0 + self._current_bet_1 + self._current_bet_2) if self.player.hand.payout != 0 else 0
        self.player._money = self.player.money + payout
        return payout


    def firstBet(self, pull: bool):
        if (pull):
            self.player._money = self.player.money + self._current_bet_1
            self._current_bet_1 = 0
    
    def secondBet(self, pull: bool):
        if (pull):
            self.player._money = self.player.money + self._current_bet_2
            self._current_bet_2 = 0

    def bet(self, bet: int):
        self.player._money = self.player._money - 3*bet
        self._current_bet_0 = bet
        self._current_bet_1 = bet
        self._current_bet_2 = bet
        self._deck = Deck(self._deck_count)
        self.deck.shuffle()
        self.deal()
    
class Player:
    """
    Class representing a player.
    """
    def __init__(self, game: Game, name: str, money: int):
        self._game = game
        self._name = name
        self._money = money
        self._hand = None

    @property
    def name(self) -> str:
        return self._name

    @property 
    def money(self) -> int:
        return self._money

    @property
    def hand(self) -> Hand:
        return self._hand

    def setHand(self, hand):
        self._hand = hand

    def draw(self, count: int=1):
        for _ in range(0, count):
            self._hand.cards.append(self._game.deck.draw())

