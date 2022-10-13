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
            if (left_pressed) and (self.x > 0):
                self.x -= self.x_velocity
            if (right_pressed and self.x <= 750):
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
            pygame.mixer.Sound.play(jump_zvuk)
            self.velocity = self.jump_velocity
            self.falling = True

class Obstacles():
    def __init__(self):
        self.obstacles = []
        self.timer = Timer()
        self.delay = 10
        self.image = pygame.image.load("sprites/cactus_scaled.png")
        self.velocities = [-5, -7, -8, -10, -12, -14]
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
                obstacle.x += self.velocities[level]
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


def set_level():
    global level
    if (score >= levels[level]):
        level += 1

def play_menu_music():
    pygame.mixer.music.load(f"""sprites/menu_theme{"2" if (randint(0, 8) == 0) else ""}.mp3""")
    pygame.mixer.music.play(-1)

def start_the_game():
    global game_state, lukas, obstacles, start_time, score, level
    level = 0
    start_time = time()*10
    lukas = Lukas(100, y_border)
    obstacles = Obstacles()
    for i in range(5): obstacles.add_random()
    game_state = 1
    play_battle_music()
    pygame.display.update()

def play_battle_music():
    pygame.mixer.music.load("sprites/overworld_theme.mp3")
    pygame.mixer.music.play(-1)

def set_menu():
    global game_state
    screen.fill((0, 0, 0))
    pygame.display.update()
    play_menu_music()
    game_state = 0

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 1024)
game_state = 0
jump_zvuk = pygame.mixer.Sound("sprites/Mario Jump - Gaming Sound Effect (HD)20150625.mp3")
jump_zvuk.set_volume(0.04)
screen = pygame.display.set_mode((800, 800))
icon = pygame.image.load("sprites/lukas_hlava.png")
pygame.display.set_icon(icon)
y_border = 370
running = True
space_pressed = False
left_pressed = False
right_pressed = False
background = pygame.image.load("sprites/background_hogwarts05.png")
pygame.display.set_caption("#knotakjede")
clock = pygame.time.Clock()
###################### Herni menu #################################################
background_menu = pygame.image.load("sprites/menu_background.png")
mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0), # transparent background
                title_font_shadow=True,
                widget_padding=25,
                widget_font=pygame_menu.font.FONT_8BIT,
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE
                )
menu = pygame_menu.Menu("", 800, 800, theme=mytheme)
menu.add.text_input('', default='Luk64')
menu.add.button('Play', start_the_game)
menu.add.button('leave', pygame_menu.events.EXIT)
###################################################################################
################### Game Over Menu ################################################
game_over_background_image = pygame.image.load("sprites/game_over.png")
game_over = pygame_menu.Menu("", 800, 800, theme=mytheme)
game_over.add.button("Play", start_the_game)
game_over.add.button("Back to menu", set_menu)

###################################################################################
font = pygame.font.Font('freesansbold.ttf', 42)
levels = [100, 200, 400, 500, 600, 100000]
set_menu()
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


    if game_state==0:
        screen.fill((0, 0, 0))
        screen.blit(background_menu, (0, 0))
        menu.draw(screen)
        if(menu.update(events)):
            pygame.display.update()
            menu.draw(screen)
        pygame.display.update()
    elif (game_state==1):
        lukas.move()
        obstacles.move()
        if (not is_lukas_safe()):
            game_state=2
            pygame.mixer.music.stop()
            continue
        screen.blit(background, (0, 0))
        score = int((time()*10 - start_time))
        text = font.render("{:0>5d}".format(score), True, (255, 255, 255))
        set_level()
        screen.blit(text, (50, 50))
        lukas.print()
        obstacles.print()
        pygame.display.update()
    else:
        screen.blit(game_over_background_image, (0, 0))
        game_over.draw(screen)
        if (game_over.update(events)):
            pygame.display.update()
            game_over.draw(screen)
        pygame.display.update()

