"""
Program: Spaghetti code hra s Lukášem bez komentářů.
Autor: David Kolář
Email: kolard@jirovcovka.net
"""
import pygame
import pygame_menu
from time import time
from collections import deque
from pygame.locals import *
from random import choice, randint
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

def check_interval(a0, a1, b0, b1):
    return (a1 <= b0)or(b1 <= a0)

def is_lukas_safe():
    for obstacle in obstacles.obstacles:
       #print(lukas.y, lukas.y + lukas.height, obstacle.y, obstacle.y+obstacle.height)
       if not (check_interval(lukas.x, lukas.x + lukas.width, obstacle.x, obstacle.x+obstacle.width) or check_interval(lukas.y, lukas.y + lukas.height, obstacle.y, obstacle.y+obstacle.height)):
            return False
    return True

class Lukas():
    def __init__(self, x, y):
        self.falling = False
        self.border = y
        self.x = x
        self.y = y
        self.width = 22*3
        self.height = 38*3
        self.velocity = 0
        self.x_velocity = 10
        self.timer_animation = Timer()
        self.timer_move = Timer()
        self.default_animation_delays = [400, 200, 10]
        self.animation_delay = self.default_animation_delays[1]
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
            self.animation_delay = self.default_animation_delays[1]
            if (right_pressed):
                self.animation_delay = self.default_animation_delays[2]
            self.timer_animation.set(self.animation_delay)

    def move(self):
        if not(self.timer_move):
            self.velocity += self.change
            if (left_pressed):
                self.x -= self.x_velocity
            if (right_pressed):
                self.x += self.x_velocity
            if (self.y + self.velocity > self.border):
                self.y = self.border
                self.velocity = 0
                self.falling = False
            else:
                self.y += self.velocity
            self.timer_move.set(self.move_delay)
            return True
        return False

    def print(self):
        self.animation()
        screen.blit(self.animations[self.pozice], (self.x, self.y))

    def jump(self):
        if (not self.falling):
            self.velocity = self.jump_velocity
            self.falling = True

class Obstacles():
    def __init__(self):
        self.obstacles = []
        self.timer = Timer()
        self.delay = 10
        self.image = pygame.image.load("sprites/cactus_scaled.png")
        self.velocity = -5
        self.timer.set(self.delay)

    def add_random(self):
        y = 425
        if (not len(self.obstacles)):
            x = 800
        else:
            x = self.obstacles[-1].x + choice([300, 400, 600])
        self.obstacles.append(Obstacle(x, y, self.image))

    def move(self):
        if not(self.timer):
            for i, obstacle in enumerate(self.obstacles):
                obstacle.x += self.velocity
                if (obstacle.x + obstacle.image.get_width() < 0):
                    del self.obstacles[i]
                    self.add_random()
            self.timer.set(self.delay)
            return True
        return False

    def print(self):
        for obstacle in self.obstacles:
            screen.blit(obstacle.image, (obstacle.x, obstacle.y))

class Obstacle():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.image = img


def play_menu_music():
    pygame.mixer.music.load(f"""sprites/menu_theme{"2" if (randint(0, 2) == 0) else ""}.mp3""")
    pygame.mixer.music.play(-1)

def start_the_game():
    global game, lukas, obstacles
    lukas = Lukas(100, y_border)
    obstacles = Obstacles()
    for i in range(5): obstacles.add_random()
    game = True
    play_battle_music()
    pygame.display.update()

def play_battle_music():
    pygame.mixer.music.load("sprites/overworld_theme.mp3")
    pygame.mixer.music.play(-1)

pygame.init()
screen = pygame.display.set_mode((800, 800))
background_menu = pygame_menu.baseimage.BaseImage("sprites/angel_face_logo.png")
icon = pygame.image.load("sprites/lukas_hlava.png")
pygame.display.set_icon(icon)
y_border = 370
running = True
space_pressed = False
left_pressed = False
right_pressed = False
background = pygame.image.load("sprites/background_hogwarts03.png")
pygame.display.set_caption("#knotakjede")
clock = pygame.time.Clock()
mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0), # transparent background
                title_background_color=(120, 47, 126),
                title_font_shadow=True,
                widget_padding=25,
                widget_font=pygame_menu.font.FONT_8BIT,
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE
                )
menu = pygame_menu.Menu("", 800, 800, theme=mytheme)
menu.add.image(background_menu)
menu.add.text_input('', default='Luk64')
menu.add.button('Play', start_the_game)
menu.add.button('leave', pygame_menu.events.EXIT)

play_menu_music()
while True:
    clock.tick(50)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE):
                space_pressed = True
            if (event.key == pygame.K_LEFT):
                left_pressed = True
            if (event.key == pygame.K_RIGHT):
                right_pressed = True
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_SPACE):
                space_pressed = False
            if (event.key == pygame.K_LEFT):
                left_pressed = False
            if (event.key == pygame.K_RIGHT):
                right_pressed = False
    if (space_pressed):
        lukas.jump()




    if not game:
        menu.draw(screen)
        if(menu.update(events)):
            pygame.display.update()
            menu.draw(screen)
            screen.fill((0, 0, 0))
        pygame.display.update()
    else:
        lukas.move()
        obstacles.move()
        if (not is_lukas_safe()):
            game=False
            screen.fill((0, 0, 0))
            play_menu_music()
            continue
        screen.blit(background, (0, 0))
        lukas.print()
        obstacles.print()
        pygame.display.update()

