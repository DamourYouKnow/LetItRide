from abc import ABC, abstractmethod
from pygame import Surface, Color, Rect
from pygame.event import Event
from pygame.font import Font
import pygame
import string
from core import *
from enum import Enum
from typing import Tuple

class Colors:
    light_gray = Color(200, 200, 200, 1)
    gray = Color(150, 150, 150, 1)
    white = Color(255, 255, 255, 1)
    black = Color(0, 0, 0, 1)
    green = Color(0, 128, 100, 1)


class Screen(ABC):

    @abstractmethod
    def handle(self, event: Event):
        pass
    
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, canvas: Surface):
        pass
    
    @abstractmethod
    def next(self):
        return self

class GameScreen(Screen):
    def __init__(self):
        self._action = Button(300, 500, width=128, height=50, text="Make $1 Bet", color=Colors.light_gray, down_color=Colors.gray,
            action=(self.action))
        self._pull = None
        self._winning = None
        self._game = Game()
        self.game.deal()
        self._cards = []
        self._background = pygame.image.load("./assets/felt.png")
        self._stage = 0
        self._bankroll = Button(100, 500, height=50, text="Bankroll: ", color=Colors.white, down_color=Colors.white, padding=5, border_color=Colors.black)
        payoffTexts = ["%s: %d" % (str(k), v) for k,v in Hand.payouts.items() if k not in [HandType.high, HandType.pair]]
        self._display = [Button(900, 50+30*i, width=200, height=30, text=x, color=Colors.white, border_color=None) for i, x in enumerate(payoffTexts)]
		
        payoffSideTexts = ["%s: %d" % (str(z), x) for z,x in Hand.sidePayouts.items() if z not in [HandType.high, HandType.pair]]
        self._displaySide = [Button(900, 400+30*i, width=200, height=30, text=x, color=Colors.white, border_color=None) for i, x in enumerate(payoffSideTexts)]
		
        self._deck = CardObject(700, 50, Card(1, Suit.clubs), False)
        self._bet_labels = [
            Button(210, 400, "$", width=80, height=30),
            Button(310, 400, "2", width=80, height=30),
            Button(410, 400, "1", width=80, height=30)
        ]
        self._bets = [
            Button(210, 430, None, width=80, height=30),
            Button(310, 430, None, width=80, height=30),
            Button(410, 430, None, width=80, height=30)
        ]
		

    def action(self, pull=False):
        if (self._stage == 0):
            self._game.deal()
            self._game.player.bet(1)
            for bet in self._bets:
                bet.text = "$" + str(1)
            self._cards = [CardObject(700, 50, c, False) for c in self.game.player.hand]

            x = 100
            for card in self._cards:
                card.deal(x, 200)
                x += 100

            [self._cards[i].flip() for i in range(3)]

            self._stage = 1
            self._pull = Button(500, 500, width=128, height=50, text="Pull Bet 1", color=Colors.gray, down_color=Colors.gray,
            action=(lambda: self.action(True)))
            self._action.text = "Let it ride"
            self._winning = None
            print(Statistics.expectedValue(self.game.player.hand.cards[0:3]))
        elif (self._stage == 1):
            self._stage = 2
            self._cards[3].flip()    
            if (pull):
                self._game.player.pull()
                self._bets[2].text = ""
            self._pull = Button(500, 500, width=128, height=50, text="Pull Bet 2", color=Colors.gray, down_color=Colors.gray,
                action=(lambda: self.action(True)))
            print(Statistics.expectedValue(self.game.player.hand.cards[0:4]))
        elif (self._stage == 2):
            self._stage = 0
            if (pull):
                self._game.player.pull()
                self._bets[1].text = ""
            self._cards[4].flip()
            self._pull = Button(500, 500, width=128, height=50, text="Clear Bet", color=Colors.gray, down_color=Colors.gray,
                action=(lambda: self.clear()))
            self._game.player.payout()
            payout = self._game.player.hand.payout(self._game.player.full_bet)
            winText = str(self.game.player.hand.type) + " - Win $" + str(payout)
            self._winning = Button(250, 25, width=228, height=50, text=winText, color=Colors.white, 
                    down_color=Colors.white, padding=5, border_color=Colors.black)
            self._action._text = "Repeat Bet"
            print(Statistics.expectedValue(self.game.player.hand.cards))

    def clear(self):
        if (self._stage == 0):
            self._pull = None
            self._action._text = "Make 1$ Bet"
            self._cards = []
            self._winning = None
            for bet in self._bets:
                bet.text = None

    @property
    def game(self) -> Game:
        return self._game

    @property
    def cards(self):
        return self._cards

    def handle(self, event: Event):
        self._action.handle(event)
        if (self._pull != None):
            self._pull.handle(event)

    def update(self):
        self._bankroll.text = "Bankroll: " + str(self.game.player.money)

    def draw(self, canvas: Surface):
        canvas.fill(Colors.white)
        canvas.blit(self._background, (0,0))
        self._action.draw(canvas)
        self._bankroll.draw(canvas)
        self._deck.draw(canvas)
        [x.draw(canvas) for x in self._display]
        [x.draw(canvas) for x in self._displaySide]
        if self._pull:
            self._pull.draw(canvas)
        if self._winning:
            self._winning.draw(canvas)
        [card.draw(canvas) for card in self.cards]
        [bet.draw(canvas) for bet in self._bet_labels]
        [bet.draw(canvas) for bet in self._bets if bet.text]

    def next(self):
        return self


class MainMenu(Screen):
    def __init__(self):
        self._next_screen = self
        self._buttons2 = [
            #Button(25, 25, "Setting", Colors.green, action=self._to_settings)
        ]
        self._buttons = [
		    Button(100, 200, "Play", Colors.green,width=150, height=100, action=self._to_game),
            #Button(100, 300, "Settings", Colors.green, action=self._to_settings)
        ]
        self._labels = [
		    Label(50, 50, "Let It Ride Poker", font_size = 64),
		    Label(600, 200, "Settings", font_size = 24)
		]

    def _to_game(self):
        self._next_screen = GameScreen()
		
    def _to_settings(self):
        self._next_screen = GameScreen()
    
    @property
    def buttons(self):
        return self._buttons
    @property
    def labels(self):
        return self._labels

    def handle(self, event: Event):
        for button in self.buttons:
            button.handle(event)

    def update(self):
        pass

    def draw(self, canvas: Surface):
        canvas.fill(Colors.white)
        [item.draw(canvas) for item in self.buttons + self.labels]
    
    def next(self):
        return self._next_screen


class GameObject(ABC):
    def __init__(self, x: int, y: int, width: int, height: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def pos(self) -> Tuple[int, int]:
        return (self._x, self._y)

    @pos.setter
    def pos(self, value: Tuple[int, int]):
        self._x, self._y = value

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def size(self) -> Tuple[int, int]:
        return (self._width, self._height)

    @size.setter
    def size(self, value: Tuple[int, int]):
        self._width, self._height = value

    @property
    def rect(self) -> Rect:
        return Rect(self._x, self._y, self._width, self._height)

    def move(self, x: int, y: int):
        self.pos = (x, y)

    def handle(self, event: Event):
        pass

    @abstractmethod
    def draw(self, canvas: Surface):
        raise NotImplementedError()

    
class Label(GameObject):
    def __init__(
            self, x: int, y: int, text: str, 
            color: Color=Colors.black, 
            font_size: int=20, font_name: str="Times"):
        self._text = text
        self._color = color
        self._font = pygame.font.SysFont(font_name, font_size)    
        w, h = self.font.render(self.text, False, (0,0,0)).get_rect().size
        GameObject.__init__(self, x, y, w, h)
    
    @property
    def text(self) -> string:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self.size = self.font.render(self.text, False, (0,0,0)).get_rect().size

    @property
    def color(self) -> Color:
        return self._color

    @property
    def font(self) -> Font:
        return self._font

    def draw(self, canvas: Surface):
        textSurface = self.font.render(self.text, False, self.color)
        canvas.blit(textSurface, (self.x, self.y))


# TODO: Create SpriteObject class.
class CardObject(GameObject):
    def __init__(self, x: int, y: int, card: Card, flipped: bool=True):
        self._card = card
        self._flipped = flipped
        self._cardImg = pygame.image.load(self.card.filename)
        self._cardBack = pygame.image.load("./assets/card_back.png")
        self._flipping = False
        self._shouldFlip = False
        self._flipX = 0
        self._deal = False
        w, h = self._cardImg.get_rect().size
        GameObject.__init__(self, x, y, w, h)
    
    @property
    def card(self) -> int:
        return self._card
    
    @property
    def cardImg(self):
        return self._cardImg
    
    @property
    def cardBack(self):
        return self._cardBack

    @property
    def flipped(self) -> bool:
        return self._flipped

    @property
    def flipping(self) -> bool:
        return self._flipping
    
    @property
    def flipX(self) -> int:
        return self._flipX

    def flip(self):
        self._flipping = True
        self._flipX = 0
    
    def deal(self, targetX, targetY):
        self._deal = True
        self._targetX = targetX
        self._targetY = targetY
        self._dealX = self.x
        self._dealY = self.y

    def draw(self, canvas):
        if self._deal:
            if (self._dealX == self._targetX and self._dealY == self._targetY):
                self._deal = False
                self._x = self._targetX
                self._y = self._targetY
            else:
                self._dealX += (self._targetX-self._x)/10
                self._dealY += (self._targetY-self._y)/10
                canvas.blit(self.cardBack, (self._dealX, self._dealY))
                return
        if self.flipping:
            if (self.flipX >= self.cardImg.get_width()):
                self._flipped = not(self._flipped)
                self._flipX = 0
                self._flipping = False
            elif (2*self.flipX >= self.cardImg.get_width()):
                img = self.cardBack if self.flipped else self.cardImg
                img = pygame.transform.scale(img, (img.get_width()-2*(img.get_width() - self.flipX), img.get_height()))
                canvas.blit(img, (self.x + (self.cardImg.get_width() - self.flipX), self.y))
                self._flipX = self.flipX + 10
                return
            else:
                img = self.cardImg if self.flipped else self.cardBack
                img = pygame.transform.scale(img, (img.get_width()-2*self.flipX, img.get_height()))
                canvas.blit(img, (self.x + self.flipX, self.y))
                self._flipX = self.flipX + 10
                return
        if self.flipped:
            canvas.blit(self.cardImg, (self.x, self.y))
        else:
            canvas.blit(self.cardBack, (self.x, self.y))


class Button(GameObject):
    def __init__(
            self, x: int, y: int, text: str, 
            color: Color=Colors.light_gray, down_color: Color=Colors.gray,
            border_width: int=2, border_color: Color=Colors.black, 
            padding: int = 4, width: int=(-1), height: int=(-1), 
            action=None):
        GameObject.__init__(self, x, y, width, height)
        self._default_width = width
        self._default_height = height
        self._padding = padding
        self._color = color
        self._border_color = border_color
        self._border_width = border_width if self.border_color != None else 0
        self._action = action
        self._down_color = down_color
        self._down = False
        self._label = Label(x + padding, y + padding, text)
        self._adjust_label()
    
    @property
    def text(self) -> string:
        return self._label.text

    @text.setter
    def text(self, value: str):
        self._label.text = value
        self._adjust_label()

    @property
    def padding(self) -> int:
        return self._padding

    @property
    def border_width(self) -> int:
        return self._border_width

    @property
    def border_color(self) -> Color:
        return self._border_color
 
    @property
    def action(self):
        return self._action

    @property
    def down_color(self):
        return self._down_color
      
    @property
    def color(self):
        if self._down:
            return self._down_color
        return self._color
    
    def draw(self, canvas: Surface):
        if self.color:
            pygame.draw.rect(
                    canvas, self.color, 
                    Rect(self.x, self.y, self.width, self.height))
        if self._border_color:
            pygame.draw.rect(canvas, self._border_color, self.rect, self.border_width)
        self._label.draw(canvas)
    
    def handle(self, event: Event):
        self._down = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONUP and self._action:
                self._action()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._down = True

    def _adjust_label(self):
        self._width = max(
                self._default_width, self._label.width + 2 * self._padding)
        self._height = max(
                self._default_height, self._label.height + 2 * self._padding)
        
        padding_x, padding_y = self._padding, self._padding
        if self._label.width < self._width * self._padding:
            padding_x = (self._width - self._label.width) / 2
        if self._label.height < self._height * self._height:
            padding_y = (self._height - self._label.height) / 2
        self._label.pos = (self._x + padding_x, self._y + padding_y)

