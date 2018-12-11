import random
from enum import Enum
from typing import List
import itertools
    
class Suit(Enum):
    """
    Enum describing all possible card Suits.
    """
    diamonds = 1
    clubs = 2
    hearts = 3
    spades = 4

    def __str__(self) -> str:
        strings = {
            Suit.diamonds: "D",
            Suit.clubs: "C",
            Suit.hearts: "H",
            Suit.spades: "S"

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
	
	
	#leave this here for now 
    mini_royal= 12

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
            HandType.high: "Nothing",
			
			
			#sidebet strings 
            HandType.mini_royal: "Mini Royal"
            
			
        }
        return strings[self]


class Card:
    """
    Class representing a playing card.
    """
    def __init__(self, rank: int, Suit: Suit):
        self._rank = rank
        self._Suit = Suit

    @property
    def rank(self):
        return self._rank

    @property
    def Suit(self):
        return self._Suit

    @property
    def filename(self):
        return "./assets/" + str(self.rank) + str(self.Suit) + ".png"

    def __eq__(self, other: 'Card') -> bool:
        return self.rank == other.rank and self.Suit == other.Suit

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
        return rank_str + str(self._Suit)


class Hand:
    """
    Class representing the hand of a player or banker.
    """
    payouts = {
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
    sidePayouts = {
        HandType.mini_royal: 50,
        HandType.straight_flush: 40,
        HandType.three_of_kind: 30,
        HandType.straight: 6,
        HandType.flush: 3,
        HandType.pair: 1
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

    def payout(self, bet: int) -> int:
        if self.type in Hand.payouts:
            # +1 for returning initial bet
            return (Hand.payouts[self.type]+1) * bet
        return 0

    @property
    def type(self) -> HandType:
        hand = self._cards.copy()
        hand.sort()
        size = len(hand)

        royals = [1, 10, 11, 12, 13]
        ranks = [card.rank for card in hand]
        is_royal = all([r in ranks for r in royals])
        is_straight = ranks == list(range(ranks[0], ranks[-1] + 1)) or is_royal
        is_flush = len([c for c in hand if c.Suit == hand[0].Suit]) == size

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
        Suits = [Suit.clubs, Suit.diamonds, Suit.hearts, Suit.spades]
        for _ in range(0, count):
            for i in range(1, 14):
                deck += [Card(i, s) for s in Suits]
        return deck


class Game:
    """
    Class representing a blackjack game.
    """
    def __init__(self, decks: int = 1, name: str="Player", money: int = 1000):
        self._deck_count = decks
        self._deck = Deck(decks)
        self._player = Player(self, name, money)
        self.deck.shuffle()

    @property
    def deck(self) -> Deck:
        return self._deck
    
    @property
    def player(self) -> 'Player':
        return self._player
    
    def deal(self):
        self._deck = Deck(self._deck_count) # We may want to change this logic.
        self._deck.shuffle()
        self.player.hand = Hand([self._deck.draw() for _ in range(5)])

class Settings:
    def __init__(self, player_name: str="Player", player_bankroll: int=1000, game_decks: int=1, background: str="./assets/felt5.png", card: str="./assets/card_back1.png"):
        self._player_name = player_name
        self._player_bankroll = player_bankroll
        self._game_decks = game_decks
        self._background = background
        self._card = card
    
    @property
    def player_name(self):
        return self._player_name

    @property
    def player_bankroll(self):
        return self._player_bankroll

    @property
    def game_decks(self):
        return self._game_decks

    @property
    def background(self):
        return self._background

    @property
    def card(self):
        return self._card
    
class Player:
    """
    Class representing a player.
    """
    def __init__(self, game: Game, name: str, money: int):
        self._game = game
        self._name = name
        self._money = money
        self._full_bet = 0
        self._portion_bet = 0
        self._hand = None

    @property
    def name(self) -> str:
        return self._name

    @property 
    def money(self) -> int:
        return self._money

    @money.setter
    def money(self, value: int):
        self._money = value

    @property
    def full_bet(self) -> int:
        return self._full_bet

    @property
    def portion_bet(self) -> int:
        return self._portion_bet

    @property
    def hand(self) -> Hand:
        return self._hand

    @hand.setter
    def hand(self, value: Hand):
        self._hand = value

    def draw(self, count: int=1):
        for _ in range(0, count):
            self._hand.cards.append(self._game.deck.draw())

    def bet(self, bet: int):
        self._money -= bet * 3
        self._full_bet = bet * 3
        self._portion_bet = bet

    def pull(self):
        if self._full_bet <= self._portion_bet:
            raise Exception("Cannot full 1st bet")
        self._full_bet -= self._portion_bet
        self._money += self._portion_bet

    def payout(self):
        self._money += self._hand.payout(self._full_bet)

class Statistics:

    def shouldRide(cards, expectedValue = None):
        ev = expectedValue if expectedValue != None else Statistics.expectedValue(cards)
        return expectedValue >= 0

    def expectedValue(cards, probabilityDistribution = None):
        choose = 5-len(cards)
        results = probabilityDistribution if probabilityDistribution != None else Statistics.probabilityDistribution(cards)
        possibilities = Statistics.choose(52-5+choose, choose)
        ev = 0
        for k,v in results.items():
            if k in Hand.payouts:
                ev += Hand.payouts[k] * v/possibilities
            else:
                ev -= v/possibilities
        return ev

    def probabilityDistribution(cards):
        choose = 5-len(cards)
        results = dict()
        for t in HandType:
            results[t] = 0
        if (choose <= 0):
            results[Hand(cards).type] = 1
            return results
        deck = Deck(1).cards
        for card in cards:
            deck.remove(card)
        for n in itertools.combinations(deck, choose):
            hand = Hand(cards + list(n))
            results[hand.type] += 1
        return results

    def choose(n,k):
        if k<0 or n<k:
            return 0
        nk = 1
        kk = 1
        for i in range(1, min(n-k, k) + 1):
            nk = nk*n
            kk = kk*i
            n = n - 1
        return nk//kk
            
