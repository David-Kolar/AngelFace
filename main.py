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
import toml
from os.path import abspath

def load_config():
    return toml.load("config.toml")
config = load_config()
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

def load_highscore():
    with open("data") as file:
        cislo = int(file.read())
    return cislo

def set_highscore():
    highscore = load_highscore()
    if (score > highscore):
        with open("data", "w") as file:
            file.write(str(score))

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
        img1 = pygame.image.load("sprites/grafika/lukas_tycka01.png")
        img2 = pygame.image.load("sprites/grafika/lukas_tycka02.png")
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
            zvuky.play(zvuky.skok)
            self.velocity = self.jump_velocity
            self.falling = True

class Obstacles():
    def __init__(self):
        self.obstacles = []
        self.timer = Timer()
        self.delay = 10
        self.image = pygame.image.load("sprites/grafika/cactus_scaled.png")
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
    pygame.mixer.music.load(f"""sprites/hudba/menu_theme{"2" if (randint(0, 20) == 0) else ""}.mp3""")
    pygame.mixer.music.play(-1)

def start_the_game():
    global game_state, lukas, obstacles, start_time, score, level, highscore, predchozi_score
    zvuky.play(zvuky.select)
    predchozi_score = 0
    level = 0
    start_time = time()*10
    highscore = load_highscore()
    lukas = Lukas(100, y_border)
    obstacles = Obstacles()
    for i in range(5): obstacles.add_random()
    zvuky.play(zvuky.lets_go)
    game_state = 1
    play_battle_music()
    pygame.display.update()

def load_company_intro():
    image = pygame.image.load("sprites/grafika/knot_foundation.png")
    sound = pygame.mixer.Sound("sprites/zvuky/company_sound.mp3")
    pygame.mixer.Sound.play(sound)
    screen.blit(image, (0, 0))
    pygame.display.update()
    pygame.time.wait(11000)

def load_cia_warning():
    image = pygame.image.load("sprites/grafika/cia.png")
    screen.blit(image, (0, 0))
    pygame.display.update()
    pygame.time.wait(4000)

def play_battle_music():
    pygame.mixer.music.load("sprites/hudba/overworld_theme.mp3")
    pygame.mixer.music.play(-1)

def set_one_player_menu():
    global game_state, active_menu
    zvuky.play(zvuky.select)
    active_menu = one_player
    pygame.display.update()

def set_two_players_menu():
    global game_state, active_menu
    zvuky.play(zvuky.select)
    active_menu = two_players
    pygame.display.update()

def set_menu():
    global game_state, active_menu
    if (not beggining): zvuky.play(zvuky.select)
    active_menu = menu
    pygame.display.update()
    if (game_state != 0): play_menu_music()
    game_state = 0

class Zvuky():
    def __init__(self, audio):
        self.audio = audio
        self.skok = pygame.mixer.Sound("sprites/zvuky/Mario Jump - Gaming Sound Effect (HD)20150625.mp3")
        self.skok.set_volume(0.04)
        self.smrt = pygame.mixer.Sound("sprites/zvuky/death.mp3")
        self.lets_go = pygame.mixer.Sound("sprites/zvuky/Lets go.mp3")
        self.wow = pygame.mixer.Sound("sprites/zvuky/Wow.mp3")
        self.amazing = pygame.mixer.Sound("sprites/zvuky/Amazing.mp3")
        self.sheesh = pygame.mixer.Sound("sprites/zvuky/Sheesh.mp3")
        self.select = pygame.mixer.Sound("sprites/zvuky/menu_select_sound.mp3")
        self.styl_styl = pygame.mixer.Sound("sprites/zvuky/styl styl 2.mp3")
        self.jezisku = pygame.mixer.Sound("sprites/zvuky/ježíšku na křížku 2.mp3")
        self.krajta = pygame.mixer.Sound("sprites/zvuky/aj ta krajta 2.mp3")
    def play(self, zvuk):
        if (self.audio): pygame.mixer.Sound.play(zvuk)
    def nahodny_zvuk_smrti(self):
        self.play(choice([self.smrt, self.jezisku, self.krajta]))

pygame.init()
game_state = 0
highscore = 0
zvuky = Zvuky(config["audio"])
beggining = True

medaile = [pygame.image.load(f"sprites/grafika/medaile_{val}.png") for val in ["bronz", "stribro", "zlato", "modra", "diamond"]]
for i in range(len(medaile)):
    medaile[i] = pygame.transform.scale(medaile[i], (medaile[i].get_width()/3, medaile[i].get_height()/3))
medaile_score = [100, 300, 600, 1000, 1500]
screen = pygame.display.set_mode((800, 800))
icon = pygame.image.load("sprites/grafika/lukas_hlava.png")
pygame.display.set_icon(icon)
y_border = 370
running = True
space_pressed = False
left_pressed = False
right_pressed = False
background = pygame.image.load("sprites/grafika/background_hogwarts05.png")
pygame.display.set_caption("#knotakjede")
clock = pygame.time.Clock()
###################### Herni menu #################################################
background_menu = pygame.image.load("sprites/grafika/background_hogwarts_new.png")
mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0), # transparent background
                title_font_shadow=True,
                widget_padding=25,
                widget_font=pygame_menu.font.FONT_8BIT,
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE
                )
menu = pygame_menu.Menu("", 800, 800, theme=mytheme)
#menu.add.text_input('', default=config["name"])
menu.add.button('one player', set_one_player_menu)
menu.add.button('two players', set_two_players_menu)
menu.add.button('leave', pygame_menu.events.EXIT)
###################################################################################
################### Game Over Menu ################################################
game_over_background_image = pygame.image.load("sprites/grafika/game_over_2.png")
game_over = pygame_menu.Menu("", 800, 800, theme=mytheme)
game_over.add.button("Play", start_the_game)
game_over.add.button("Back to menu", set_menu)

###################################################################################
################### One players menu ##############################################
one_player = pygame_menu.Menu("", 800, 800, theme=mytheme)
one_player.add.text_input('', default=config["name"])
one_player.add.button('play', start_the_game)
one_player.add.button('back', set_menu)
################### Two players menu ##############################################
two_players = pygame_menu.Menu("", 800, 800, theme=mytheme)
two_players.add.text_input('', default=config["name"])
two_players.add.text_input('', default=config["name2"])
two_players.add.button('play', start_the_game)
two_players.add.button('back', set_menu)
###################################################################################
active_menu = menu
font = pygame.font.Font(abspath("sprites/pismo/pixel_font.ttf"), 32)
levels = [100, 200, 300, 400, 500, float("inf")]
predchozi_score = 0
if (config["cia"]):
    load_cia_warning()
if (config["company_intro"]):
    load_company_intro()
play_menu_music()
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

    if game_state==0:
        screen.fill((0, 0, 0))
        screen.blit(background_menu, (0, 0))
        active_menu.draw(screen)
        if(active_menu.update(events)):
            pygame.display.update()
            active_menu.draw(screen)
        pygame.display.update()
    elif (game_state==1):
        if (space_pressed):
            lukas.jump()
        lukas.move()
        obstacles.move()
        if (not is_lukas_safe()):
            game_state=2
            pygame.mixer.music.stop()
            zvuky.nahodny_zvuk_smrti()
            set_highscore()
            continue
        screen.blit(background, (0, 0))
        score = int((time()*10 - start_time))
        if ((score) % 100 == 0 and score != predchozi_score):
            zvuk = [zvuky.wow, zvuky.amazing, zvuky.sheesh, zvuky.styl_styl]
            zvuky.play(zvuk[(score//100)%len(zvuk)])
            predchozi_score = score
        text = font.render("{:0>5d}".format(score), True, (255, 255, 255))
        h_text = font.render("{:0>5d}".format(highscore), True, (255, 255, 255))
        set_level()
        screen.blit(text, (20, 20))
        screen.blit(h_text, (20, 54))
        lukas.print()
        obstacles.print()
        pygame.display.update()
    else:
        screen.blit(game_over_background_image, (0, 0))
        game_over.draw(screen)
        if (game_over.update(events)):
            pygame.display.update()
            game_over.draw(screen)
        for i, s in enumerate(medaile_score):
            if (score > s):
                screen.blit(medaile[i], (200 + i*(medaile[i].get_width() + 20), 520))
        pygame.display.update()
    beggining = False

