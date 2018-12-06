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
    def __init__(self, settings: Settings):
        self._action = Button(300, 500, width=128, height=50, text="Make $1 Bet", color=Colors.light_gray, down_color=Colors.gray,
            action=(self.action))
        self._pull = None
        self._winning = None
        self._autoplay_button = Button(700, 250, width=128, height=40, text="Autoplay On", color=Colors.light_gray, down_color=Colors.gray,
            action=(self.autoplay))
        self._main_menu = Button(50, 50, width=100, height=50, text="Main Menu", color=Colors.light_gray, down_color=Colors.gray, 
            action=(lambda: self.home(settings)))
        self._game = Game(settings.game_decks, settings.player_name, settings.player_bankroll)
        self.game.deal()
        self._cards = []
        self._background = pygame.image.load("./assets/felt.png")
        self._stage = 0
        self._bankroll = Button(100, 500, height=50, text="Bankroll: ", color=Colors.white, down_color=Colors.white, padding=5, border_color=Colors.black)
        payoffTexts = ["Payouts", "-------"] + ["%s: %d" % (str(k), v) for k,v in Hand.payouts.items() if k not in [HandType.high, HandType.pair]]
        self._payoffs = TextArea(900, 50, payoffTexts, width=200, background_color=Color(255, 255, 255, 255))
        payoffSideTexts = ["Sidebet Payouts", "---------------"] + ["%s: %d" % (str(z), x) for z,x in Hand.sidePayouts.items() if z not in [HandType.high, HandType.pair]]
        self._payoffs_side = TextArea(900, 320, width=200, texts=payoffSideTexts, background_color=Color(255, 255, 255, 255))
        self._statistics = None
        self._autoplay = False
        self._next_screen = self

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
            self._pull = Button(500, 500, width=128, height=50, text="Pull Bet 1", color=Colors.light_gray, down_color=Colors.gray,
            action=(lambda: self.action(True)))
            self._action.text = "Let it ride"
            self._winning = None
            self.update_statistics()
        elif (self._stage == 1):
            self._stage = 2
            self._cards[3].flip()    
            if (pull):
                self._game.player.pull()
                self._bets[2].text = ""
            self._pull = Button(500, 500, width=128, height=50, text="Pull Bet 2", color=Colors.light_gray, down_color=Colors.gray,
                action=(lambda: self.action(True)))
            self.update_statistics()
        elif (self._stage == 2):
            self._stage = 0
            if (pull):
                self._game.player.pull()
                self._bets[1].text = ""
            self._cards[4].flip()
            self.update_statistics()
            self._pull = Button(500, 500, width=128, height=50, text="Clear Bet", color=Colors.light_gray, down_color=Colors.gray,
                action=(lambda: self.clear()))
            self._game.player.payout()
            payout = self._game.player.hand.payout(self._game.player.full_bet)
            winText = str(self.game.player.hand.type) + " - Win $" + str(payout)
            self._winning = Button(250, 25, width=228, height=50, text=winText, color=Colors.white, 
                    down_color=Colors.white, padding=5, border_color=Colors.black)
            self._action.text = "Repeat Bet"

    def home(self, settings):
        self._next_screen = MainMenu(settings)

    def autoplay(self):
        if (self._autoplay):
            self._autoplay = False
            self._autoplay_button.text = "Autoplay On"
        else:
            self._autoplay = True
            self._autoplay_button.text = "Autoplay Off"

    def update_statistics(self):
        if (self._stage == 1 or self._stage == 2):
            cards = self.game.player.hand.cards[0:self._stage + 2]
        else:
            cards = self.game.player.hand.cards
        probabilities = Statistics.probabilityDistribution(cards)
        self._probabilityWin = sum([v for k,v in probabilities.items() if k in Hand.payouts])/Statistics.choose(52-2-self._stage, 3-self._stage)
        self._expectedValue = Statistics.expectedValue(cards, probabilities)
        self._shouldRide = Statistics.shouldRide(cards, self._expectedValue)
        self._statistics = TextArea(900, 500, [
            "Should Ride: " + str(self._shouldRide),
            "Expected Value: " + ("%.3f" % self._expectedValue),
            "Probability Win: " + ("%.3f" % self._probabilityWin)
        ], width=200, background_color=Color(255, 255, 255, 255))

    def clear(self):
        if (self._stage == 0):
            self._pull = None
            self._action._text = "Make 1$ Bet"
            self._cards = []
            self._winning = None
            self._statistics = None
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
        self._autoplay_button.handle(event)
        self._main_menu.handle(event)
        if (self._pull != None):
            self._pull.handle(event)

    def update(self):
        self._bankroll.text = "Bankroll: " + str(self.game.player.money)
        if (self._autoplay and len([card for card in self.cards if card._deal or card._flipping]) == 0):
            if (self._stage == 1 or self._stage == 2):
                self.action(not(self._shouldRide))
            else:
                self.action()

    def draw(self, canvas: Surface):
        canvas.fill(Colors.white)
        canvas.blit(self._background, (0,0))
        self._action.draw(canvas)
        self._bankroll.draw(canvas)
        self._deck.draw(canvas)
        self._payoffs.draw(canvas)
        self._payoffs_side.draw(canvas)
        self._autoplay_button.draw(canvas)
        self._main_menu.draw(canvas)
        if (self._statistics):
            self._statistics.draw(canvas)
        if self._pull:
            self._pull.draw(canvas)
        if self._winning:
            self._winning.draw(canvas)
        [card.draw(canvas) for card in self.cards]
        [bet.draw(canvas) for bet in self._bet_labels]
        [bet.draw(canvas) for bet in self._bets if bet.text]

    def next(self):
        return self._next_screen


class MainMenu(Screen):
    def __init__(self, settings=Settings()):
        self._next_screen = self
        self._settings = settings
        self._buttons2 = [
            #Button(25, 25, "Setting", Colors.green, action=self._to_settings)
        ]
        self._buttons = [
		    Button(100, 200, "Play", Colors.green,width=150, height=100, action=self._to_game),
            Button(100, 300, "Settings", Colors.green, action=self._to_settings)
        ]
        self._labels = [
		    Label(50, 50, "Let It Ride Poker", font_size = 64),
		]

    def _to_game(self):
        self._next_screen = GameScreen(self._settings)
		
    def _to_settings(self):
        self._next_screen = SettingsScreen(self._settings)
    
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

class SettingsScreen(Screen):

    def __init__(self, settings: Settings=Settings()):
        self._player_name = TextBox(350, 150, 600, 40, text=settings.player_name, placeholder_text="Name...", font_size=30)
        self._player_money = TextBox(350, 210, 600, 40, text=str(settings.player_bankroll), placeholder_text="Money...", font_size=30)
        self._game_decks = TextBox(350, 270, 600, 40, text=str(settings.game_decks), placeholder_text="Decks...", font_size=30)
        self._warning = Button(380, 600, width=440, color=Color(220, 100, 100, 1), text=None)
        self._components = [
            Label(480, 20, "Settings", font_size=64, font_name="Impact"),
            Label(200, 150, "Player: ", font_size=36),
            self._player_name,
            Label(200, 210, "Bankroll: ", font_size=36),
            self._player_money,
            Label(200, 270, "Decks: ", font_size=36),
            self._game_decks,
            Button(480, 600, width=240, color=Colors.white, text="Back", action=(lambda: self.gather_settings()))
        ]
        self._next_screen = self
        self._background = pygame.image.load("./assets/felt.png")

    def gather_settings(self):
        if (self._warning.text == None):
            self._next_screen = MainMenu(Settings(self._player_name.text, int(self._player_money.text), int(self._game_decks.text)))

    def handle(self, event: Event):
        [component.handle(event) for component in self._components]

    def update(self):
        if (not self._player_money.text.isdigit()):
            self._warning.text = "Player money must be a number"
        elif (not self._game_decks.text.isdigit()):
            self._warning.text = "Game decks must be a number"
        else:
            self._warning.text = None

    def draw(self, canvas: Surface):
        canvas.fill(Colors.white)
        canvas.blit(self._background, (0,0))
        pygame.draw.rect(canvas, Color(180, 180, 180, 0), Rect(150, 0, 900, 675))
        [component.draw(canvas) for component in self._components]
        if (self._warning.text != None):
            self._warning.draw(canvas)

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

class TextBox(GameObject):
    def __init__(
            self, x: int, y: int, width: int, height: int, text: str=None, placeholder_text: str="", placeholder_color: Color=Colors.gray,
            font_color: Color=Colors.black, background_color: Color=Colors.white, halo_color: Color=Color(0, 180, 210, 1),
            font_size: int=20, font_name: str="Times"):
        self._default_text = placeholder_text
        self._font_color = font_color
        self._placeholder_color = placeholder_color
        self._background_color = background_color
        self._halo_color = halo_color
        self._font = pygame.font.SysFont(font_name, font_size)
        self._selected = False
        self._empty = (text == None)
        if not self._empty:
            self._label = Label(x+4, y+(height-font_size)/2-1, text, color=font_color, font_size=font_size, font_name=font_name)
        else:
            self._label = Label(x+4, y+(height-font_size)/2-1, placeholder_text, color=placeholder_color, font_size = font_size, font_name = font_name)
        GameObject.__init__(self, x, y, width, height)

    @property
    def text(self):
        return self._label.text if not self._empty else "" 

    def handle(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self._selected = True
            else:
                self._selected = False
        if self._selected and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if (not self._empty):
                    self._label.text = self._label.text[:-1]
                    if (self._label.text == ""):
                        self._empty = True
                        self._label._color = self._placeholder_color
                        self._label.text = self._default_text
            elif event.unicode != "" and ord(event.unicode)>=32 and ord(event.unicode)<= 126 and self._label.width < self.width-10:
                if (self._empty):
                    self._label.text = "" + event.unicode
                    self._label._color = self._font_color
                    self._empty = False
                else:
                    self._label.text = self._label.text + event.unicode

    def draw(self, canvas: Surface):
        padding = 2
        pygame.draw.rect(
                canvas, self._background_color, 
                Rect(self.x, self.y, self.width, self.height))
        if (self._selected):
            pygame.draw.rect(canvas, self._halo_color, self.rect, 1)
        else:
            pygame.draw.rect(canvas, Colors.black, self.rect, 1)
        self._label.draw(canvas)

class TextArea(GameObject):
    def __init__(
            self, x: int, y: int, texts: List[str], width: int=0, height: int=0, 
            color: Color=Colors.black, background_color: Color=None,
            font_size: int=20, font_name: str="Times", bold: int=0, italic: int=0, padding=1, centered=True):
        self._color = color
        self._background_color = background_color
        self._padding = padding
        self._default_width = width
        self._default_height = height
        self._centered = centered
        self._font = pygame.font.SysFont(font_name, font_size, bold=bold, italic=italic)   
        GameObject.__init__(self, x, y, width, height)
        self.texts = texts
    
    @property
    def texts(self) -> List[str]:
        return self._texts

    @texts.setter
    def texts(self, value: List[str]):
        self._texts = value
        rects = [self.font.render(text, False, (0,0,0)).get_rect() for text in self._texts]
        if (self._default_width <= 0):
            width = max([rect.width for rect in rects])+2*self._padding
        else:
            width = self._default_width
        if (self._default_height <= 0):
            height = sum([rect.height for rect in rects])+2*self._padding
        else:
            height = self._default_height
        self.size = (width,height)

    @property
    def color(self) -> Color:
        return self._color

    @property
    def font(self) -> Font:
        return self._font

    def draw(self, canvas: Surface):
        textSurfaces = [self.font.render(text, False, self.color) for text in self.texts]
        if (self._background_color != None):
            pygame.draw.rect(canvas, self._background_color, Rect(self.x, self.y, self.width, self.height))
        [canvas.blit(textSurface, 
            (self.x+self._padding + ((self.width-textSurface.get_width())/2 if self._centered else 0),
                self.y + self._padding + (i*self.font.get_height()))) 
            for i, textSurface in enumerate(textSurfaces)]

class Label(GameObject):
    def __init__(
            self, x: int, y: int, text: str, 
            color: Color=Colors.black, 
            font_size: int=20, font_name: str="Times", bold: int=0, italic: int=0):
        self._text = text
        self._color = color
        self._font = pygame.font.SysFont(font_name, font_size, bold=bold, italic=italic)    
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

