from abc import ABC, abstractmethod
from pygame import Surface, Color, Rect
from pygame.event import Event
from pygame.font import Font
import pygame
import string
from core import *
from typing import Tuple

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
        self._action = Button(300, 500, width=128, height=50, text="Make $1 Bet", color=Color(200,200,200,1), downColor=Color(150,150,150,1),
            action=(self.action))
        self._pull = None
        self._winning = None
        self._game = Game()
        self.game.deal()
        self._cards = []
        self._background = pygame.image.load("./assets/felt.png")
        self._stage = 0
        self._bankroll = Button(100, 500, height=50, text="Bankroll: ", color=Color(255,255,255,1), downColor=Color(255,255,255,1), padding=5, borderColor=Color(0,0,0,1))
        payoffTexts = ["%s: %d" % (str(x), Hand.payouts[x] if x in Hand.payouts else 0) for x in HandType if x != HandType.high and x != HandType.pair]
        self._display = [Button(900, 50+30*i, width=200, height=30, text=x, color=Color(255,255,255,1), borderColor=None) for i, x in enumerate(payoffTexts)]
        self._deck = CardObject(700, 50, Card(1, Suite.clubs), False)
        self._bet_labels = [Button(210, 400, "$", width=80, height=30, color=Color(199,199,199,1), borderColor=None),
            Button(310, 400, "2", width=80, height=30, color=Color(199,199,199,1), borderColor=None),
            Button(410, 400, "1", width=80, height=30, color=Color(199,199,199,1), borderColor=None)]
        self._bets = [Button(210, 430, None, width=80, height=30, color=Color(199,199,199,1), borderColor = None),
            Button(310, 430, None, width=80, height=30, color=Color(199,199,199,1), borderColor = None),
            Button(410, 430, None, width=80, height=30, color=Color(199,199,199,1), borderColor = None)]

    def action(self, pull=False):
        if (self._stage == 0):
            self._game.player.bet(1)
            for bet in self._bets:
                bet.setText("$" + str(1))
            self._cards = [CardObject(700, 50, c, False) for c in self.game.player.hand]
            self._cards[0].deal(100, 200)
            self._cards[1].deal(200, 200)
            self._cards[2].deal(300, 200)
            self._cards[3].deal(400, 200)
            self._cards[4].deal(500, 200)
            self._cards[0].flip()
            self._cards[1].flip()
            self._cards[2].flip()
            self._stage = 1
            self._pull = Button(500, 500, width=128, height=50, text="Pull Bet 1", color=Color(200,200,200,1), downColor=Color(150,150,150,1),
            action=(lambda: self.action(True)))
            self._action._text = "Let it ride"
            self._winning = None
        elif (self._stage == 1):
            self._stage = 2
            self._cards[3].flip()    
            if (pull):
                self._game.player.pull()
                self._bets[2].setText("")
            self._pull = Button(500, 500, width=128, height=50, text="Pull Bet 2", color=Color(200,200,200,1), downColor=Color(150,150,150,1),
                action=(lambda: self.action(True)))
        elif (self._stage == 2):
            self._stage = 0
            if (pull):
                self._game.player.pull()
                self._bets[1].setText("")
            self._cards[4].flip()
            self._pull = Button(500, 500, width=128, height=50, text="Clear Bet", color=Color(200,200,200,1), downColor=Color(150,150,150,1),
                action=(lambda: self.clear()))
            payout = self._game.player.hand.payout(self._game.player.full_bet)
            winText = str(self.game.player.hand.type) + " - Win $" + str(payout)
            self._winning = Button(250, 25, width=228, height=50, text=winText, color=Color(255,255,255,1), 
                    downColor=Color(255,255,255,1), padding=5, borderColor=Color(0,0,0,1))
            self._action._text = "Repeat Bet"
            self._game.deal()

    def clear(self):
        if (self._stage == 0):
            self._pull = None
            self._action._text = "Make 1$ Bet"
            self._cards = []
            self._winning = None
            for bet in self._bets:
                bet.setText(None)

    @property
    def game(self) -> Game:
        return self._game

    @property
    def cards(self):
        return self._cards

    def handle(self, event: Event):
        self._action.handle_click(event)
        if (self._pull != None):
            self._pull.handle_click(event)

    def update(self):
        self._bankroll.setText("Bankroll: " + str(self.game.player.money))

    def draw(self, canvas: Surface):
        canvas.fill(Color(255, 255, 255, 1))
        canvas.blit(self._background, (0,0))
        self._action.draw(canvas)
        self._bankroll.draw(canvas)
        self._deck.draw(canvas)
        for x in self._display:
            x.draw(canvas) 
        if (self._pull != None):
            self._pull.draw(canvas)
        if (self._winning != None):
            self._winning.draw(canvas)
        for card in self.cards:
            card.draw(canvas)
        for bet in self._bet_labels:
            bet.draw(canvas)
        for bet in self._bets:
            if (bet.text != None):
                bet.draw(canvas)

    def next(self):
        return self


class MainMenu(Screen):
    def __init__(self):
        self._next_screen = self
        self._buttons = [
            Button(20, 20, "Hello!", Color(0,128,100,1), fontSize=30, action=self._to_game)
        ]
        self._labels = [Label(50, 50, "Let It Ride Poker", fontSize = 50)]

    def _to_game(self):
        self._next_screen = GameScreen()
    
    @property
    def buttons(self):
        return self._buttons
    @property
    def labels(self):
        return self._labels

    def handle(self, event: Event):
        for button in self.buttons:
            button.handle_click(event)

    def update(self):
        pass

    def draw(self, canvas: Surface):
        canvas.fill(Color(255, 255, 255, 1))
        for button in self.buttons:
            button.draw(canvas)
        for label in self.labels:
            label.draw(canvas)
    
    def next(self):
        return self._next_screen


class GameObject(ABC):
    def __init__(self, x: int, y: int, width: int, height: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._rect = Rect(x, y, width, height)

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
        self._rect = Rect(value[0], value[1], self._width, self._height)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def rect(self) -> Rect:
        return self._rect

    def move(self, x: int, y: int):
        self.pos = (x, y)

    @abstractmethod
    def draw(self):
        raise NotImplementedError()

    
class Label(GameObject):
    def __init__(
            self, x: int, y: int, text: str, 
            color: Color=Color(0,0,0,1), 
            fontSize: int=20, fontName: str="Times"):

        GameObject.__init__(self, x, y, 0, 0) # TODO: Find way to get label height.
        self._text = text
        self._color = color
        self._font = pygame.font.SysFont(fontName, fontSize)
    
    @property
    def text(self) -> string:
        return self._text

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
    def __init__(self, x: int, y: int, text: string, color: Color, downColor: Color = Color(0,0,0,1), fontColor: Color = Color(0,0,0,1),
                 borderWidth: int = 2, borderColor: Color = Color(0,0,0,1), 
                 fontSize: int = 20, fontName: string = "Times", padding: int = 4, 
                 width: int=(-1), height: int=(-1), action=None):
        GameObject.__init__(self, x, y, width, height)
        self._defaultWidth = width
        self._defaultHeight = height
        self._padding = padding
        self._color = color
        self._borderColor = borderColor
        self._borderWidth = borderWidth if self.borderColor != None else 0
        self._fontName = fontName
        self._fontSize = fontSize
        self._font = pygame.font.SysFont(fontName, fontSize)
        self._fontColor = fontColor
        self._action = action
        self._downColor = downColor
        self._down = False
        self.setText(text)
    
    def setText(self, text: str):
        self._text = text
        if self._defaultHeight < 0:
            self._height = self._fontSize + 2 * self.padding
        else:
            self._height = self._defaultHeight
        if self._defaultWidth < 0:
            self._width = self.font.render(self.text, False, (0,0,0)).get_width() + 2 * self.padding
        else:
            self._width = self._defaultWidth
        self._rect = Rect(self.x, self.y, self.width, self.height)

    @property
    def padding(self) -> int:
        return self._padding

    @property
    def text(self) -> string:
        return self._text

    @property
    def color(self) -> Color:
        return self._color

    @property
    def borderWidth(self) -> int:
        return self._borderWidth

    @property
    def borderColor(self) -> Color:
        return self._borderColor

    @property
    def font(self) -> Font:
        return self._font
    
    @property
    def action(self):
        return self._action

    @property
    def downColor(self):
        return self._downColor
      
    def getColor(self):
        if self._down:
            return self.downColor
        return self.color
    
    def draw(self, canvas: Surface):
        if (self._borderColor != None):
            pygame.draw.rect(canvas, self._borderColor, self.rect)
        if (self.getColor() != None):
            pygame.draw.rect(canvas, self.getColor(), 
                Rect(self.x,
                     self.y,
                     self.width,
                     self.height))
        if (self._fontColor != None):
            textSurface = self.font.render(self.text, False, self._fontColor)
            paddingX = self.padding
            paddingY = self.padding
            if (textSurface.get_width() < self.width-2*self.padding):
                paddingX = (self.width-textSurface.get_width())/2
            if (textSurface.get_height() < self.height-2*self.padding):
                paddingY = (self.height-textSurface.get_height())/2
            canvas.blit(textSurface, (self.x + paddingX, self.y + paddingY))
    
    def handle_click(self, event: Event):
        self._down = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONUP and self._action:
                self._action()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._down = True