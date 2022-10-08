import pygame
import pygame_menu
from time import time
from pygame.locals import *
from random import randint
from pygame_menu.locals import *
game = False

class Timer():
    def __init__(self):
        self.time = 0
    def aktualni(self):
        return time() * 1000
    def __bool__(self):
        return (self.aktualni() <= self.time)
    def set(self, delay):
        self.time = self.aktualni() + delay

class Lukas():
    def __init__(self, x, y):
        self.falling = False
        self.border = y
        self.x = x
        self.y = y
        self.velocity = 0
        self.timer_animation = Timer()
        self.timer_move = Timer()
        self.animation_delay = 200
        self.move_delay = 10
        self.timer_animation.set(self.animation_delay)
        self.pozice = 0
        self.change = 1
        self.jump_velocity = -20
        img1 = pygame.image.load("sprites/lukas_tycka01.png")
        img2 = pygame.image.load("sprites/lukas_tycka02.png")
        self.animations = [pygame.transform.scale(img1, (img1.get_width()*3, img1.get_height()*3)), pygame.transform.scale(img2, (img2.get_width()*3, img2.get_height()*3))]

    def animation(self):
        if not(self.timer_animation):
            if (not self.falling): self.pozice = (self.pozice + 1)%2
            self.timer_animation.set(self.animation_delay)

    def move(self):
        if not(self.timer_move):
            self.velocity += self.change
            if (self.y + self.velocity > self.border):
                self.y = self.border
                self.velocity = 0
                self.falling = False
            else:
                self.y += self.velocity
            self.timer_move.set(self.move_delay)

    def print(self):
        self.animation()
        screen.blit(self.animations[self.pozice], (self.x, self.y))

    def jump(self):
        if (not self.falling):
            self.velocity = self.jump_velocity
            self.falling = True

class Obstacle():
    def __init__(self, x):
        self.x = x
    def move(self):
        pass
def play_menu_music():
    pygame.mixer.music.load(f"""sprites/menu_theme{"2" if (randint(0, 2) == 0) else ""}.mp3""")
    pygame.mixer.music.play(-1)

def start_the_game():
    global game
    game = True
    play_battle_music()
    pygame.display.update()

def play_battle_music():
    pygame.mixer.music.load("sprites/overworld_theme.mp3")
    pygame.mixer.music.play(-1)

def gameLoop():
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    lukas.move()
    lukas.print()

icon = pygame.image.load("sprites/lukas_hlava.png")
pygame.display.set_icon(icon)
lukas = Lukas(100, 370)
pygame.init()
running = True
screen = pygame.display.set_mode((800, 800))
background = pygame.image.load("sprites/background_hogwarts03.png").convert()
pygame.display.set_caption("#knotakjede")
mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0), # transparent background
                title_background_color=(120, 47, 126),
                title_font_shadow=True,
                widget_padding=25,
                widget_font=pygame_menu.font.FONT_8BIT,
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE
                )
menu = pygame_menu.Menu("", 800, 800, theme=mytheme)
menu.add.text_input('', default='Luk64')
menu.add.button('Play', start_the_game)
menu.add.button('leave', pygame_menu.events.EXIT)
play_menu_music()
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE):
                if not(lukas.falling):
                    lukas.jump()

    if not game:
        menu.draw(screen)
        if(menu.update(events)):
            pygame.display.update()
            menu.draw(screen)
            screen.fill((0, 0, 0))
    else:
        gameLoop()
    pygame.display.update()

