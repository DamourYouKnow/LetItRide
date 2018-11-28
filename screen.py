from abc import ABC, abstractmethod
from pygame import Surface, Color, Rect
from pygame.event import Event
from pygame.font import Font
import pygame
import string
from core import *

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
        self._ride_button = Button(
                0, 0, "Let it Ride", Color(100, 100, 100, 1), action=(lambda: self.cards[3].flip())) 
        self._game = Game()
        self.game.deal()
        self._cards = [
            CardComponent(100, 300, self.game.player.hand.playerCards()[0]),
            CardComponent(300, 300, self.game.player.hand.playerCards()[1]),
            CardComponent(500, 300, self.game.player.hand.playerCards()[2]),
            CardComponent(200, 100, self.game.player.hand.firstBet(), False),
            CardComponent(400, 100, self.game.player.hand.secondBet(), False),
        ]
        
    @property
    def game(self) -> Game:
        return self._game

    @property
    def cards(self):
        return self._cards

    def handle(self, event: Event):
        if event.type == pygame.MOUSEBUTTONUP:
            self._ride_button.handleClick(event)

    def update(self):
        pass

    def draw(self, canvas: Surface):
        canvas.fill(Color(255, 255, 255, 1))
        self._ride_button.draw(canvas)
        for card in self.cards:
            card.draw(canvas)

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
            button.handleClick(event)

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

class Label:
    def __init__(self, x: int, y: int, text: string, color: Color = Color(0,0,0,1), fontSize: int = 20,
        fontName: string = "Times"):
        self._x = x
        self._y = y
        self._text = text
        self._color = color
        self._font = pygame.font.SysFont(fontName, fontSize)
    
    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

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

class CardComponent:
    def __init__(self, x: int, y: int, card: Card, flipped: bool = True):
        self._x = x
        self._y = y
        self._card = card
        self._flipped = flipped
        self._cardImg = pygame.image.load(self.card.filename)
        self._cardBack = pygame.image.load("./assets/card_back.png")
    
    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y
    
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

    def flip(self):
        self._flipped = not (self._flipped)

    def draw(self, canvas):
        if self.flipped:
            canvas.blit(self.cardImg, (self.x, self.y))
        else:
            canvas.blit(self.cardBack, (self.x, self.y))


class Button:

    def __init__(self, x: int, y: int, text: string, color: Color, downColor: Color = Color(0,0,0,1),
                 borderWidth: int = 2, borderColor: Color = Color(0,0,0,1), 
                 fontSize: int = 20, fontName: string = "Times", padding: int = 4, 
                 width: int = (-1), height: int = (-1), action = None):
        self._x = x
        self._y = y
        self._padding = padding
        self._text = text
        self._color = color
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self._font = pygame.font.SysFont(fontName, fontSize)
        self._action = action
        self._downColor = downColor
        self._isDown = False
        if height < 0:
            self._height = fontSize + 2 * self.padding
        else:
            self._height = height
        if width < 0:
            self._width = self.font.render(self.text, False, (0,0,0)).get_width() + 2 * self.padding
        else:
            self._width = width
        self._rect = Rect(self.x, self.y, self.width, self.height)
    
    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def padding(self) -> int:
        return self._padding

    @property
    def text(self) -> string:
        return self._text

    @property
    def rect(self) -> Rect:
        return self._rect

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
    
    @property
    def isDown(self):
        return self._isDown
    
    def setDown(self, isDown):
        self._isDown = isDown

    def getColor(self):
        if (self.isDown):
            return self.downColor
        else:
            return self.color
    
    def draw(self, canvas: Surface):
        pygame.draw.rect(canvas, self._borderColor, self.rect)
        pygame.draw.rect(canvas, self.getColor(), 
            Rect(self.x+self.borderWidth,
                 self.y+self.borderWidth,
                 self.width - 2*self.borderWidth,
                 self.height - 2*self.borderWidth))
        textSurface = self.font.render(self.text, False, (0,0,0))
        canvas.blit(textSurface, (self.x + self.padding, self.y + self.padding))
    
    def handleClick(self, event: Event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONUP and not (self.action == None):
                self.action()
                self.setDown(False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.setDown(True)
            else:
                self.setDown(False)
        else:
            self.setDown(False)