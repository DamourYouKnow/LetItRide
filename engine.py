from abc import ABC, abstractmethod
from typing import Tuple

import pygame
from pygame import Surface, Color, Rect
from pygame.event import Event


class Colors:
    light_gray = Color(200, 200, 200, 1)
    gray = Color(150, 150, 150, 1)
    white = Color(255, 255, 255, 1)
    black = Color(0, 0, 0, 1)
    green = Color(0, 128, 100, 1)


class GameComponent(ABC):
    def __init__(self):
        self._object = None 

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def handle(self, event: Event):
        pass

    @abstractmethod
    def draw(self, canvas: Surface):
        pass

    @abstractmethod
    def on_attach(self):
        pass


class GameObject(ABC):
    def __init__(self, x: int, y: int, width: int, height: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._components = []

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

    def add_component(self, component: GameComponent):
        component._object = self
        component.on_attach()
        self._components.append(component)

    def get_component(self, component_type: type):
        return next(
                c for c in self._components if isinstance(c, component_type))

    def update(self):
        [c.update() for c in self._components]

    def handle(self, event: Event):
        [c.handle(event) for c in self._components]

    def draw(self, canvas: Surface):
        [c.draw(canvas) for c in self._components]


class Click(GameComponent):
    def __init__(self, action):
        self._action = action
        GameComponent.__init__(self)
    
    def handle(self, event: Event):
        if not self._action:
            return
        if not self._object.rect.collidepoint(pygame.mouse.get_pos()):
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._action()


class TextBox(GameComponent):
    def __init__(
            self,
            text: str=None, placeholder_text: str="", placeholder_color: Color=Colors.gray,
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

    @text.setter
    def text(self, value):
        self._label.text = value

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


class TextureManager:
    textures = dict()

    @staticmethod
    def save(path, img):
        TextureManager.textures[path] = img

    @staticmethod
    def load(path: str) -> Surface:
        if (path in TextureManager.textures):
            return TextureManager.textures.get(path)
        else:
            img = pygame.image.load(path)
            TextureManager.textures[path] = img
            return img


class Sprite(GameComponent):
    def __init__(self, sprite: str, scale: float=1):
        self.sprite = sprite
        self._scale = scale
        GameComponent.__init__(self)

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

    def draw(self, canvas: Surface):
        canvas.blit(self.sprite, (self._object.x, self._object.y))

    def on_attach(self):
        self._object.size = self.sprite.get_rect.size()

