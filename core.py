import random
from enum import Enum
from typing import List
import itertools
import math
    
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
    three_of_kind_side= 13
    flush_side=14
    straight_flush_side=15
    straight_side = 16
    pair_side = 17
    high_side = 18
    
    
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
            HandType.mini_royal: "Mini Royal",
            HandType.three_of_kind_side: "Three of a Kind",
            HandType.straight_flush_side: "Straight Flush",
            HandType.flush_side: "Flush",
            HandType.straight_side: "Straight",
            HandType.pair_side: "Pair",
            HandType.high_side: "Nothing"
        }
        return strings[self]

class Card:
    """
    Class representing a playing card.
    """
    def __init__(self, rank: int, Suit: Suit):
        """
        Create an instance of a card.
        
        Arguments:
            rank {int} -- Rank of card (A=1,J=11,Q=12,K=13)
            Suit {Suit} -- Suit of card.
        """
        self._rank = rank
        self._Suit = Suit

    @property
    def rank(self) -> int:
        """
        Returns:
            int -- Rank of card.
        """
        return self._rank

    @property
    def Suit(self) -> Suit:
        """ 
        Returns:
            Suit -- Suit of card.
        """

        return self._Suit

    @property
    def filename(self) -> str:
        """
        Returns:
            [str] -- Filepath of card image.
        """

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
        HandType.straight_flush_side: 40,
        HandType.three_of_kind_side: 30,
        HandType.straight_side: 6,
        HandType.flush_side: 3,
        HandType.pair_side: 1
        }

    def __init__(self, cards: List[Card]=[]):
        self._cards = cards

    @property
    def cards(self) -> List[Card]:
        """
        Returns:
            List[Card] -- Cards in hand.
        """

        return self._cards

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        for card in self._cards:
            yield card

    def payout(self, bet: int) -> int:
        """
        Computes the payout of a hand for a specified bet.
        
        Arguments:
            bet {int} -- Bet amount.
        
        Returns:
            int -- Payout of bet.
        """
        if self.type in Hand.payouts:
            # +1 for returning initial bet
            return (Hand.payouts[self.type]+1) * bet
        return 0

    @property
    def type(self) -> HandType:
        """
        Determines the type of a hand (Two pair, straight, flush, ...).
        
        Returns:
            HandType -- Type of hand.
        """
        hand = self._cards.copy()
        hand.sort()
        size = len(hand)
            
        royals = [1, 10, 11, 12, 13]
        ranks = [card.rank for card in hand]
        is_royal = ranks == royals
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

    @property
    def type_side(self) -> HandType:
        """
        Determines the type of a side bet hand.

        Returns:
            HandType -- Hand type.
        """
        hand = self._cards.copy()[:3]
        hand.sort()
        size=3

        royals = [11, 12, 13]
        ranks = [card.rank for card in hand]
        high = ranks == [1, 12, 13]
        is_royal = ranks == royals
        is_straight = ranks == list(range(ranks[0], ranks[-1] + 1)) or high
        is_flush = len([c for c in hand if c.Suit == hand[0].Suit]) == size

        if is_royal and is_flush:
            return HandType.mini_royal
        if is_straight and is_flush:
            return HandType.straight_flush_side
        if is_straight:
            return HandType.straight_side
        if is_flush:
            return HandType.flush_side

        count_map = {
            c.rank: len([c2 for c2 in hand if c2.rank == c.rank]) for c in hand
        }
        counts = list(count_map.values())

        if counts.count(3) == 1:
            return HandType.three_of_kind_side
  
        if counts.count(2) == 1:
            return HandType.pair_side

        return HandType.high_side
        

class Deck:
    """
    Class representing a deck of cards.
    """
    def __init__(self, count: int=1):
        """
        Create a deck of cards with a specified deck size.
        
        Keyword Arguments:
            count {int} -- Size of deck (default: {1})
        """
        if (count < 100):
            self._cards = Deck._create_deck(count)
            self._infinite = False
        else:
            self._cards = Deck._create_deck(1)
            self._infinite = True

    @property
    def cards(self) -> List[Card]:
        """
        Returns:
            List[Card] -- List of cards in deck.
        """
        return self._cards

    def draw(self) -> Card:
        """
        Draws a card from the top of a deck.
        
        Returns:
            Card -- Drawn card.
        """
        if (self._infinite):
            return random.choice(self._cards)
        else:
            return self._cards.pop()

    def shuffle(self):
        """
        Shuffles the deck.
        """
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
    Class representing a Let it Ride game.
    """
    def __init__(self, decks: int = 1, name: str="Player", money: int = 1000):
        """
        Creates an instance of a game.
        
        Keyword Arguments:
            decks {int} -- Number of card decks to use. (default: {1})
            name {str} -- Name of player (default: {"Player"})
            money {int} -- Starting bankroll of player. (default: {1000})
        """
        self._deck_count = decks
        self._deck = Deck(decks)
        self._player = Player(self, name, money)
        self.deck.shuffle()

    @property
    def deck(self) -> Deck:
        """
        Returns:
            Deck -- Game deck.
        """
        return self._deck
    
    @property
    def player(self) -> 'Player':
        """
        Returns:
            [Player] -- Game player.
        """
        return self._player
    
    def deal(self):
        """
        Deal 5 cards into the player's hand.
        """
        self._deck = Deck(self._deck_count) # We may want to change this logic.
        self._deck.shuffle()
        self.player.hand = Hand([self._deck.draw() for _ in range(5)])


class Settings:
    """
    Initializes settings for the game
    """
    def __init__(
            self, 
            player_name: str="Player", player_bankroll: int=1000, 
            game_decks: int=1, 
            background: str="./assets/felt5.png", 
            card: str="./assets/card_back1.png"):
        self._player_name = player_name
        self._player_bankroll = player_bankroll
        self._game_decks = game_decks
        self._background = background
        self._card = card
    
    """
    Gets the name of the player
    """
    @property
    def player_name(self):
        return self._player_name

    """
    Gets the player bankroll
    """
    @property
    def player_bankroll(self):
        return self._player_bankroll

    """
    Setter for player bankroll
    """
    @player_bankroll.setter
    def player_bankroll(self, value: int):
        self._player_bankroll = value
        
    """
    Gets the number of decks used in the game
    """
    @property
    def game_decks(self):
        return self._game_decks

    """
    Gets the configurable background image
    """
    @property
    def background(self):
        return self._background

    """
    Gets the configurable card back
    """
    @property
    def card(self):
        return self._card
    

class Player:
    """
    Class representing a player.
    """
    def __init__(self, game: Game, name: str, money: int):
        """
        Creates and instance of a player.
        
        Arguments:
            game {Game} -- Game player is participating in.
            name {str} -- Name of player.
            money {int} -- Starting bankroll of player.
        """
        self._game = game
        self._name = name
        self._money = money
        self._full_bet = 0
        self._portion_bet = 0
        self._hand = None
        

    @property
    def name(self) -> str:
        """
        Returns:
            str -- Name of player.
        """
        return self._name

    @property 
    def money(self) -> int:
        """
        Returns:
            int -- Bankroll of player.
        """
        return self._money

    @money.setter
    def money(self, value: int):
        """
        Arguments:
            value {int} -- Bankroll of player.
        """

        self._money = value

    @property
    def full_bet(self) -> int:
        """
        Returns:
            int -- Combined bet of player.
        """
        return self._full_bet

    @property
    def portion_bet(self) -> int:
        """
        Returns:
            int -- Individual unit bet of player.
        """
        return self._portion_bet

    @property
    def hand(self) -> Hand:
        """
        Returns:
            Hand -- Hand of player.
        """
        return self._hand

    @hand.setter
    def hand(self, value: Hand):
        """
        Arguments:
            value {Hand} -- Hand of player.
        """
        self._hand = value

    def draw(self, count: int=1):
        """
        Draw a specified number of cards from the game deck into this player's 
        hand.

        Keyword Arguments:
            count {int} -- Number of cards to draw. (default: {1})
        """
        for _ in range(0, count):
            self._hand.cards.append(self._game.deck.draw())

    def bet(self, bet: int):
        """
        Places a bet for a player.

        Remarks:
            The full bet is 3 times this amount.
        
        Arguments:
            bet {int} -- Indivivual bet amount.
        """
        self._money -= bet * 3
        self._full_bet = bet * 3
        self._portion_bet = bet

    def pull(self):
        """
        Pull a portion of a player's bet.
        
        Raises:
            Exception -- Raised if the last bet is pulled.
        """
        if self._full_bet <= self._portion_bet:
            raise Exception("Cannot full 1st bet")
        self._full_bet -= self._portion_bet
        self._money += self._portion_bet

    def payout(self):
        """
        Adds the payout of a player's hand to their bankroll.
        """
        self._money += self._hand.payout(self._full_bet)


class Statistics:
    """
    Returns whether or not a hand should be ridden. Uses expected value
    If no expected value is given, one will be generated with deck size 1
    """
    @staticmethod
    def shouldRide(cards, expectedValue: float = None) -> bool:
        if not expectedValue:
            expectedValue = Statistics.expectedValue(cards)
        return expectedValue >= 0

    """
    Returns the expected value of a hand given a hand distribution
    If no hand distribution is given, a deck of size 1 is used to generate
    """
    @staticmethod
    def expectedValue(cards, handDistribution: dict = None) -> float:
        if not handDistribution:
            handDistribution = Statistics.handDistribution(cards, 1)
        possibilities = sum(handDistribution.values())
        ev = 0
        for k,v in handDistribution.items():
            if k in Hand.payouts:
                ev += Hand.payouts[k] * v/possibilities
            else:
                ev -= v/possibilities
        return ev

    """
    Generates the hand distribution for a given set of cards
    with a certain number of decks. Defaults to 1 deck
    """
    @staticmethod
    def handDistribution(cards, numDecks: int=1) -> dict:
        choose = 5-len(cards)
        results = dict()
        for t in HandType:
            results[t] = 0
        if (choose <= 0):
            results[Hand(cards).type] = 1
            return results
        deck = Deck(numDecks).cards
        if (numDecks != math.inf):
            for card in cards:
                deck.remove(card)
        for n in itertools.combinations(deck, choose):
            hand = Hand(cards + list(n))
            results[hand.type] += 1
        return results
            
