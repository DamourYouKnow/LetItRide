from abc import ABC, abstractmethod
from pygame import Surface, Color, Rect
from pygame.event import Event
from pygame.font import Font
import pygame
import string
import math
from core import *
from enum import Enum
from typing import Tuple

class Colors:
    light_gray = Color(200, 200, 200, 1)
    gray = Color(150, 150, 150, 1)
    white = Color(255, 255, 255, 1)
    black = Color(0, 0, 0, 1)
    green = Color(0, 128, 100, 1)
    blue_gray = Color(180, 180, 200, 1)
    dark_blue_gray = Color(120, 120, 140, 1)


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
        CardObject.CARD_BACK = settings.card
        self._action = Button(290, 500, width=148, height=50, text="Make $0 Bet", color=Colors.light_gray, down_color=Colors.gray,
            action=(self.action))
        
        self._pull = Button(480, 500, width=148, height=50, text="Reset Bet", color=Colors.light_gray, down_color=Colors.gray,
            action=self.clear)
        self._winning = None
        self._winning_side = None
        self._autoplay_button = Button(1036, 500, width=128, height=40, text="Autoplay On", color=Colors.blue_gray, down_color=Colors.dark_blue_gray,
            action=(self.autoplay))
        self._card_selector_button = Button(1036, 550, width=128, height=40, text="Card Selector", color=Colors.blue_gray, down_color=Colors.dark_blue_gray,
            action=(self.cardselector))
        self._statistics_button = Button(1036, 600, width=128, height=40, text="Show Statistics", color=Colors.blue_gray, down_color=Colors.dark_blue_gray,
            action=(self.show_statistics))
        self._show_statistics = False
        self._main_menu = Button(10, 10, width=100, height=50, text="Main Menu", color=Colors.light_gray, down_color=Colors.gray, 
            action=(lambda: self.home(settings)))
        self._game = Game(settings.game_decks, settings.player_name, settings.player_bankroll)
        self.game.deal()
        self._cards = []
        self._background = TextureManager.load(settings.background)
        self._stage = 0
        self._bankroll = Button(100, 500, height=50, width=148, text="Bankroll: ", color=Colors.white, down_color=Colors.white, padding=5, border_color=Colors.black)
        self._side = Button(690, 500, width=148, height=50, text="Side Bet:OFF", color=Colors.light_gray, down_color=Colors.gray,
            action=(self.side))
        self._side_state=False
        
        payoffTexts = ["Payouts", "-------"] + ["%s: %d" % (str(k), v) for k,v in Hand.payouts.items() if k not in [HandType.high, HandType.pair]]
        self._payoffs = TextArea(1000, 5, payoffTexts, width=200, background_color=Colors.light_gray)
        payoffSideTexts = ["Sidebet Payouts", "---------------"] + ["%s: %d" % (str(z), x) for z,x in Hand.sidePayouts.items() if z not in [HandType.high, HandType.pair]]
        self._payoffs_side = TextArea(1000, 275, width=200, texts=payoffSideTexts, background_color=Colors.light_gray)
        self._statistics = None
        self._autoplay = False
        self._next_screen = self

        self._bet_pool = 0
        self._bet_buttons = [
            SpriteObject(139, 575, "./assets/chip-1.png", scale=0.8, action=(lambda: self.add_bet(1))),
            SpriteObject(214, 575, "./assets/chip-5.png", scale=0.8, action=(lambda: self.add_bet(5))),
            SpriteObject(289, 575, "./assets/chip-10.png", scale=0.8, action=(lambda: self.add_bet(10))),
            SpriteObject(364, 575, "./assets/chip-20.png", scale=0.8, action=(lambda: self.add_bet(20))),
            SpriteObject(439, 575, "./assets/chip-50.png", scale=0.8, action=(lambda: self.add_bet(50))),
            SpriteObject(514, 575, "./assets/chip-100.png", scale=0.8, action=(lambda: self.add_bet(100)))
        ]

        self._deck = CardObject(700, 50, Card(1, Suit.clubs), False)
        self._bet_labels = [
            Button(224, 400, "$", width=80, height=30),
            Button(324, 400, "2", width=80, height=30),
            Button(424, 400, "1", width=80, height=30)
        ]
        self._bets = [
            Button(224, 430, None, width=80, height=30),
            Button(324, 430, None, width=80, height=30),
            Button(424, 430, None, width=80, height=30)
        ]

    def add_bet(self, amount):
        if self._stage == 0 and self.game.player.money >= self._bet_pool*3 + (amount* 3):
            self._bet_pool += amount
            self._action.text = "Make $" + str(self._bet_pool * 3) + " Bet"

    def side(self):
        if (self._side_state ==False):
            self._side_state = True
            self._side.text="Side Bet: ON"
        else:
            self._side_state = False
            self._side.text="Side Bet: OFF"
        
    def action(self, pull=False):
        if (self._stage == 0):
            if self._bet_pool == 0:
                return
        
            self._game.deal()
            self._game.player.bet(self._bet_pool)
            for bet in self._bets:
                bet.text = "$" + str(self._bet_pool)
            self._cards = [CardObject(700, 50, c, False) for c in self.game.player.hand]

            x = 100
            for card in self._cards:
                card.deal(x, 160)
                x += 100

            [self._cards[i].flip() for i in range(3)]
            
            if (self._side_state==True):
                #self._game.player.payout()
                #payout = self._game.player.hand.payout(self._game.player.full_bet)
                winText_side = str(self.game.player.hand.type_side) + " - Win $"   #+ str(payout)
                self._winning_side = Button(250, 80, width=228, height=50, text=winText_side, color=Colors.white, 
                    down_color=Colors.white, padding=5, border_color=Colors.black)
            
            
            self._stage = 1
            self._pull = Button(480, 500, width=148, height=50, text="Pull Bet 1", color=Colors.light_gray, down_color=Colors.gray,
            action=(lambda: self.action(True)))
            self._action.text = "Let it ride"
            self._winning = None
            if (self._show_statistics):
                self.update_statistics()
        elif (self._stage == 1):
            self._stage = 2
            self._cards[3].flip()    
            if (pull):
                self._game.player.pull()
                self._bets[2].text = ""
            self._pull = Button(480, 500, width=148, height=50, text="Pull Bet 2", color=Colors.light_gray, down_color=Colors.gray,
                action=(lambda: self.action(True)))
            if (self._show_statistics):
                self.update_statistics()
        elif (self._stage == 2):
            self._stage = 0
            if (pull):
                self._game.player.pull()
                self._bets[1].text = ""
            self._cards[4].flip()
            if (self._show_statistics):
                self.update_statistics()
            self._pull = Button(480, 500, width=148, height=50, text="Clear Bet", color=Colors.light_gray, down_color=Colors.gray,
                action=(lambda: self.clear()))
            self._game.player.payout()
            payout = self._game.player.hand.payout(self._game.player.full_bet)
            winText = str(self.game.player.hand.type) + " - Win $" + str(payout)
            self._winning = Button(250, 25, width=228, height=50, text=winText, color=Colors.white, 
                    down_color=Colors.white, padding=5, border_color=Colors.black)
            self._action.text = "Repeat Bet"

    def home(self, settings):
        settings.player_bankroll = self._game.player.money
        self._next_screen = MainMenu(settings)

    def autoplay(self):
        if (self._autoplay):
            self._autoplay = False
            self._autoplay_button.text = "Autoplay On"
        else:
            self._autoplay = True
            self._autoplay_button.text = "Autoplay Off"

    def show_statistics(self):
        self._show_statistics = not self._show_statistics
        if (self._show_statistics):
            self._statistics_button.text = "Hide Statistics"
            self.update_statistics()
        else:
            self._statistics_button.text = "Show Statistics"
            self._statistics = None

    def cardselector(self):
        self._next_screen = CardSelectorScreen(self)

    def update_statistics(self):
        if (self._stage == 1 or self._stage == 2):
            cards = self.game.player.hand.cards[0:self._stage + 2]
        else:
            cards = self.game.player.hand.cards
        probabilities = Statistics.probabilityDistribution(cards)
        self._probabilityWin = sum([v for k,v in probabilities.items() if k in Hand.payouts])/Statistics.choose(52-2-self._stage, 3-self._stage)
        self._expectedValue = Statistics.expectedValue(cards, probabilities)
        self._shouldRide = Statistics.shouldRide(cards, self._expectedValue)
        self._statistics = TextArea(664, 585, [
            "Should Ride: " + str(self._shouldRide),
            "Expected Value: " + ("%.3f" % self._expectedValue),
            "Probability Win: " + ("%.3f" % self._probabilityWin)
        ], width=200, background_color=None,color=Colors.white)

    def clear(self):
        if (self._stage == 0):
            self._pull = Button(480, 500, width=148, height=50, text="Reset Bet", color=Colors.light_gray, down_color=Colors.gray,
                action=self.clear)
            self._action.text = "Make $0 Bet"
            self._cards = []
            self._winning = None
            self._winning_side = None
            self._statistics = None
            self._bet_pool = 0
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
        self._statistics_button.handle(event)
        self._side.handle(event)
        if (self._stage == 0):
            self._card_selector_button.handle(event)
            [chip.handle(event) for chip in self._bet_buttons]
        self._main_menu.handle(event)
        if (self._pull != None):
            self._pull.handle(event)

    def update(self):
        self._bankroll.text = "Bankroll: " + str(self.game.player.money)
        if (self._autoplay and len([card for card in self.cards if card._dealing or card._flipping]) == 0):
            if (self._stage == 1 or self._stage == 2):
                self.update_statistics()
                self.action(not(self._shouldRide))
            else:
                self.action()

    def draw(self, canvas: Surface):
        canvas.fill(Colors.white)
        canvas.blit(self._background, (0,0))
        pygame.draw.rect(canvas, Colors.light_gray, Rect(1000, 0, 200, 800))
        pygame.draw.rect(canvas, Colors.gray, Rect(995, 0, 5, 800))
        pygame.draw.rect(canvas, Colors.gray, Rect(1000, 265, 200, 5))
        pygame.draw.rect(canvas, Colors.gray, Rect(1000, 470, 200, 5))
        pygame.draw.rect(canvas, Colors.gray, Rect(0, 470, 995, 5))
        panel = pygame.Surface((995, 200))
        panel.set_alpha(80)
        panel.fill((0,0,0))
        canvas.blit(panel, (0, 475))
        self._action.draw(canvas)
        self._bankroll.draw(canvas)
        self._side.draw(canvas)
        self._deck.draw(canvas)
        self._payoffs.draw(canvas)
        self._payoffs_side.draw(canvas)
        self._autoplay_button.draw(canvas)
        self._statistics_button.draw(canvas)
        self._main_menu.draw(canvas)
        if (self._stage == 0):
            self._card_selector_button.draw(canvas)
        if (self._show_statistics):
            self._statistics.draw(canvas)
        if self._pull:
            self._pull.draw(canvas)
        if self._winning:
            self._winning.draw(canvas)
        if self._winning_side:
            self._winning_side.draw(canvas)
        [chip.draw(canvas) for chip in self._bet_buttons]
        [card.draw(canvas) for card in self.cards]
        [bet.draw(canvas) for bet in self._bet_labels]
        [bet.draw(canvas) for bet in self._bets if bet.text]

    def next(self):
        return self._next_screen

class CardSelectorScreen(Screen):
    
    def __init__(self, game: GameScreen):
        self._title = Label(460, 40, "Select Card 1", font_size=50, color=Colors.white)
        self._back = Button(40, 40, "Back", height=50, width=200, action=self.back)
        deck = Deck().cards
        deck.sort(key=(lambda x: (x.Suit.value, x.rank)))
        self._cards = [CardObject(5+91*(i%13),100+130*(i//13),card,scale=0.7,action=(lambda x: self.action(x))) for i, card in enumerate(deck)]
        self._selected = []
        self._next_screen = self
        self._game_screen = game
        self._background = game._background

    def action(self, card):
        if (card in self._selected):
            self._selected.remove(card)
        elif (len(self._selected) < 5):
            self._selected.append(card)
        if (len(self._selected) >= 5):
           self._title.text = "Click Save Cards"
        else:
           self._title.text = "Select Card " + str(len(self._selected) + 1)
        if (len(self._selected) == 0):
            self._back.text = "Back"
        else:
            self._back.text = "Save cards"

    def back(self):
        if len(self._selected) > 0:
            self._game_deal = self._game_screen.game.deal
            self._game_screen.game.deal = self.deal
        self._game_screen._next_screen = self._game_screen
        self._next_screen = self._game_screen 

    def deal(self):
        self._game_screen.game.deal = self._game_deal
        self._game_screen.game._deck = Deck(self._game_screen.game._deck_count) # We may want to change this logic.
        self._game_screen.game._deck.shuffle()
        [self._game_screen.game._deck._cards.remove(card) for card in self._selected]
        self._game_screen.game.player.hand = Hand(self._selected + [self._game_screen.game.deck.draw() for _ in range(5-len(self._selected))])


    def update(self):
        pass

    def handle(self, event):
        self._back.handle(event)
        [card.handle(event) for card in self._cards]

    def draw(self, canvas):
        canvas.fill(Colors.white)
        canvas.blit(self._background, (0,0))
        for card in self._cards:
            card.draw(canvas)
            if card.card in self._selected:
                pygame.draw.rect(canvas, Color(100, 200, 255, 2), Rect(card.x-1, card.y-1, card.width+2, card.height+2), 4)
        self._title.draw(canvas)
        self._back.draw(canvas)

    def next(self):
        return self._next_screen

class MainMenu(Screen):

    LOADED = False

    def __init__(self, settings=Settings()):
        CardObject.CARD_BACK = settings.card
        self._next_screen = self
        self._settings = settings
        self._background = TextureManager.load(settings.background)
        self._buttons = [
		    Button(400, 250, "Play", Colors.light_gray, down_color=Colors.gray, width=400, height=80, action=self._to_game),
		    Button(400, 350, "Info", Colors.light_gray, down_color=Colors.gray, width=400, height=80, action=self._to_info),
            Button(400, 450, "Settings", Colors.light_gray, down_color=Colors.gray, width=400, height=80, action=self._to_settings)
        ]
        self._labels = [
		    Label(340, 70, "Let It Ride Poker", font_size = 80, font_name="IMPACT", color=Colors.white),
            Label(361, 650, "Created by Bailey D'Amour, Joey Miller and Michael Cardy", color=Colors.white)
		]
        if not MainMenu.LOADED:
            [TextureManager.load("./assets/card_back" + str(i) + ".png") for i in range(1,6)]
            [TextureManager.load(card.filename) for card in Deck().cards]
            MainMenu.LOADED=True

    def _to_game(self):
        self._next_screen = GameScreen(self._settings)
		
    def _to_settings(self):
        self._next_screen = SettingsScreen(self._settings)
    
    def _to_info(self):
        self._next_screen = InfoScreen(self._settings)

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
        canvas.blit(self._background, (0,0))
        card_back = TextureManager.load(CardObject.CARD_BACK)
        canvas.blit(card_back, (800, 45))
        canvas.blit(pygame.transform.rotate(card_back, -20), (800, 55))
        canvas.blit(pygame.transform.rotate(card_back, -40), (800, 80))
        back = Surface((540, 100))
        back.set_alpha(120)
        back.fill(Colors.black)
        canvas.blit(back, (330, 70))
        [item.draw(canvas) for item in self.buttons + self.labels]
    
    def next(self):
        return self._next_screen

class InfoScreen(Screen):

    def __init__(self, settings: Settings):
        self._next_screen = self
        self._background = TextureManager.load(settings.background)
        self._buttons = [Button(10, 10, width=100, height=50, text="Main Menu", color=Colors.light_gray, down_color=Colors.gray, 
            action=(lambda: self.home(settings)))]

    def handle(self, event: Event):
        for button in self.buttons:
            button.handle(event)

    def home(self, settings):
        self._next_screen = MainMenu(settings)

    @property
    def buttons(self):
        return self._buttons

    def update(self):
        pass

    def draw(self, canvas: Surface):
        canvas.fill(Colors.white)
        canvas.blit(self._background, (0,0))
        [item.draw(canvas) for item in self.buttons]
    
    def next(self):
        return self._next_screen

class SettingsScreen(Screen):

    def __init__(self, settings: Settings=Settings()):
        CardObject.CARD_BACK = settings.card
        self._player_name = TextBox(350, 150, 600, 40, text=settings.player_name, placeholder_text="Name...", font_size=30)
        self._player_money = TextBox(350, 210, 600, 40, text=str(settings.player_bankroll), placeholder_text="Money...", font_size=30)
        self._game_decks = TextBox(350, 270, 600, 40, text=str(settings.game_decks), placeholder_text="Decks...", font_size=30)
        self._warning = Button(380, 600, width=440, color=Color(220, 100, 100, 1), text=None)
        self._backgrounds = []
        for i in range(0,5):
            background = "./assets/felt" + str(i+1) + ".png"
            sprite = SpriteObject(400 + i*100, 350, background, scale=0.08, action=(lambda s: self.set_background(s.background)))
            sprite.background = background
            self._backgrounds.append(sprite)
        self._cards = []
        for i in range(0,5):
            card = "./assets/card_back" + str(i+1) + ".png"
            sprite = SpriteObject(405 + i*100, 450, card, scale=0.7, action=(lambda s: self.set_card(s.card)))
            sprite.card = card
            self._cards.append(sprite)
        self._components = [
            Label(480, 20, "Settings", font_size=64, font_name="Impact"),
            Label(200, 150, "Player: ", font_size=36),
            self._player_name,
            Label(200, 210, "Bankroll: ", font_size=36),
            self._player_money,
            Label(200, 270, "Decks: ", font_size=36),
            self._game_decks,
            Button(480, 600, width=240, color=Colors.white, text="Back", action=(lambda: self.gather_settings())),
            Label(200, 350, "Background: ", font_size=36),
            Label(200, 450, "Card Back:", font_size=36)
        ] + self._backgrounds + self._cards
        self.set_background(settings.background)
        self._card = settings.card
        self._next_screen = self

    def set_background(self, background):
        self._selected_background = background
        self._background = TextureManager.load(self._selected_background)

    def set_card(self, card):
        self._card = card

    def gather_settings(self):
        if (self._warning.text == None):
            self._next_screen = MainMenu(Settings(self._player_name.text, int(self._player_money.text), int(self._game_decks.text), self._selected_background, self._card))

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
        for cardSprite in self._cards:
            if (cardSprite.card == self._card):
                border = 4
                pygame.draw.rect(canvas, Color(100, 200, 255, 0), 
                    Rect(cardSprite.x-border, cardSprite.y-border, cardSprite.width+2*border, cardSprite.height+2*border), border)
                break
        if (self._warning.text != None):
            self._warning.draw(canvas)

    def next(self):
        return self._next_screen

class TextureManager:
    textures = dict()

    def save(path, img):
        TextureManager.textures[path] = img

    def load(path: str) -> Surface:
        if (path in TextureManager.textures):
            return TextureManager.textures.get(path)
        else:
            img = pygame.image.load(path)
            TextureManager.textures[path] = img
            return img

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

class SpriteObject(GameObject):
    def __init__(self, x: int, y: int, sprite: str, scale: float=1, action=None):
        self._scale = scale
        self._action = action
        self.sprite = sprite
        w,h= self.sprite.get_rect().size
        GameObject.__init__(self, x, y, w, h)
    
    @property
    def scale(self) -> float:
        return self._scale

    @property
    def sprite(self) -> Surface:
        return self._sprite
    
    @sprite.setter
    def sprite(self, sprite: str):
        sprite = TextureManager.load(sprite)
        if (self.scale != 1):
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * self.scale), int(sprite.get_height()*self.scale)))
        self._sprite = sprite

    @property
    def action(self):
        return self._action
        
    def draw(self, canvas: Surface):
        canvas.blit(self.sprite, (self.x, self.y))
    
    def handle(self, event):
        if (self.action != None and event.type == pygame.MOUSEBUTTONDOWN and 
                Rect(self.x, self.y, self.width, self.height).collidepoint(pygame.mouse.get_pos())):
            try:
                self.action(self)
            except:
                self.action()

class CardObject(SpriteObject):
    CARD_BACK = "./assets/card_back.png"

    def __init__(self, x: int, y: int, card: Card, flipped: bool=True, scale: float=1, action=None):
        self._card = card
        self._flipped = flipped
        self._flipping = False
        self._dealing = False
        sprite = card.filename if flipped else CardObject.CARD_BACK
        SpriteObject.__init__(self, x, y, sprite, scale, action)
    
    @property
    def card(self):
        return self._card

    @property
    def action(self):
        return (lambda s: s._action(s._card))

    def flip(self):
        self._flipping = True
        self._flipX = 0
    
    def deal(self, targetX, targetY):
        self._dealing = True
        self._targetX = targetX
        self._targetY = targetY
        self._dealX = self.x
        self._dealY = self.y
    
    def draw(self, canvas: Surface):
        if self._dealing:
            if (self._dealX == self._targetX and self._dealY == self._targetY):
                self._dealing = False
                self._x = self._targetX
                self._y = self._targetY
            else:
                self._dealX += (self._targetX-self._x)/10
                self._dealY += (self._targetY-self._y)/10
                canvas.blit(self.sprite, (self._dealX, self._dealY))
        elif self._flipping:
            if (self._flipX >= self.width):
                self._flipped = not(self._flipped)
                self._flipX = 0
                self._flipping = False
                canvas.blit(self.sprite, (self.x, self.y))
            elif (2*self._flipX >= self.width):
                img = pygame.transform.scale(self.sprite, (self.width-2*(self.width - self._flipX), self.height))
                canvas.blit(img, (self.x + (self.width - self._flipX), self.y))
                self._flipX = self._flipX + 10
            else:
                img = pygame.transform.scale(self.sprite, (self.width-2*self._flipX, self.height))
                canvas.blit(img, (self.x + self._flipX, self.y))
                self._flipX = self._flipX + 10
                if (2*self._flipX >= self.width):
                    self.sprite = CardObject.CARD_BACK if self._flipped else self.card.filename
        else:
            canvas.blit(self.sprite, (self.x, self.y))

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

