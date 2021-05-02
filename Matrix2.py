import pygame as pg
from random import randrange, choice
import sys
import ctypes


class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green_katakana)
        self.interval = randrange(5,30)


    def draw(self, color):
        frames = pg.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_katakana if color == 'green' else lightgreen_katakana )
        self.y = self.y + self.speed  if self.y < HEIGHT  else -FONT_SIZE
        screen.blit(self.value, (self.x, self.y))


class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(8,18)
        self.speed = randrange(3,6)
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

    def draw(self):
        [symbol.draw('green') if i else symbol.draw('lightgreen') for i, symbol in enumerate(self.symbols) ]


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
#katakana = [chr(int('0x0531', 16) + i) for i in range(38)]
katakana = katakana + ['*', '+', '>','<']

RES = WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
FONT_SIZE = 20
alpha_value = 0

pg.init()
surface= pg.display.set_mode(RES, pg.FULLSCREEN)
screen = pg.Surface(RES)
screen.set_alpha(alpha_value)
fps = 60

clock = pg.time.Clock()

pg.display.set_caption('THE MATRIX')
#font = pg.font.Font('armfont.ttf', FONT_SIZE)
font = pg.font.Font('MS Mincho.ttf', FONT_SIZE)
font.set_bold(True)

green_katakana = [ font.render(char, True, (40, randrange(80,255), 40) ) for char in katakana ]
lightgreen_katakana = [ font.render(char, True, pg.Color('lightgreen') ) for char in katakana ]

symbol_columns = [ SymbolColumn(x,randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE) ]


while True:
    surface.blit(screen, (0,0))
    screen.fill(pg.Color('black'))

    if not pg.time.get_ticks() % 20 and alpha_value < 170:
        alpha_value += 3
        screen.set_alpha(alpha_value)


    [ symbol_column.draw() for symbol_column in symbol_columns ]

    [ sys.exit() for i in pg.event.get() if i.type == pg.KEYDOWN ]
    pg.display.flip()
    clock.tick(fps)

