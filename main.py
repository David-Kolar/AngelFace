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

    def is_safe(self):
        for obstacle in obstacles.obstacles:
            # print(lukas.y, lukas.y + lukas.height, obstacle.y, obstacle.y+obstacle.height)
            if not (check_interval(self.x, self.x + self.width, obstacle.x,
                                   obstacle.x + obstacle.width) or check_interval(self.y, self.y + self.height,
                                                                                  obstacle.y,
                                                                                  obstacle.y + obstacle.height)):
                return False
        return True
    def animation(self, standart_control=True):
        right = keyboard.d
        if (standart_control): right = keyboard.right
        if not(self.timer_animation):
            if (not self.falling): self.pozice = (self.pozice + 1)%2
            self.animation_delay = self.default_animation_delays[1]
            if (right):
                self.animation_delay = self.default_animation_delays[2]
            self.timer_animation.set(self.animation_delay)

    def move(self, standart_control=True):
        right = keyboard.d
        left = keyboard.a
        if (standart_control):
            right = keyboard.right
            left = keyboard.left
        if not(self.timer_move):
            self.velocity += self.change
            if (left) and (self.x > 0):
                self.x -= self.x_velocity
            if (right and self.x <= 750):
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
        screen.blit(self.animations[self.pozice], (self.x, self.y))

    def jump(self):
        if (not self.falling):
            zvuky.play(zvuky.skok)
            self.velocity = self.jump_velocity
            self.falling = True

    def set_skin_princezna(self):
        img1 = pygame.image.load("sprites/grafika/lukas_princezna01.png")
        img2 = pygame.image.load("sprites/grafika/lukas_princezna02.png")
        self.animations = [pygame.transform.scale(img1, (img1.get_width() * 3, img1.get_height() * 3)),
                           pygame.transform.scale(img2, (img2.get_width() * 3, img2.get_height() * 3))]
    def set_skin_lukasenko(self):
        img1 = pygame.image.load("sprites/grafika/lukasenko01.png")
        img2 = pygame.image.load("sprites/grafika/lukasenko02.png")
        self.animations = [pygame.transform.scale(img1, (img1.get_width() * 3, img1.get_height() * 3)),
                           pygame.transform.scale(img2, (img2.get_width() * 3, img2.get_height() * 3))]
    def set_skin_dino(self):
        img1 = pygame.image.load("sprites/grafika/dino01.png")
        img2 = pygame.image.load("sprites/grafika/dino02.png")
        self.animations = [img1, img2]

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
    pygame.mixer.music.load(f"""sprites/hudba/menu_theme{"2" if (randint(0, 40) == 0) else ""}.mp3""")
    pygame.mixer.music.play(-1)

def start_the_game():
    global game_state, lukas, obstacles, start_time, score, level, highscore, predchozi_score, singleplayer
    zvuky.play(zvuky.select)
    singleplayer = True
    predchozi_score = 0
    level = 0
    start_time = time()*10
    highscore = load_highscore()
    lukas = Lukas(100, y_border)
    if (namebox_single_player.get_value()=="angelface"):
        lukas.set_skin_princezna()
    if (namebox_single_player.get_value()=="dino"):
        lukas.set_skin_dino()
    if (namebox_single_player.get_value()=="lukasenko"):
        lukas.set_skin_lukasenko()
    obstacles = Obstacles()
    for i in range(5): obstacles.add_random()
    zvuky.play(zvuky.lets_go)
    game_state = 1
    play_battle_music()
    pygame.display.update()

def start_the_multiplayer():
    global game_state, lukas, obstacles, start_time, score, level, highscore, predchozi_score, princezna, singleplayer, name1, name2, title1, title2
    name1 = namebox1.get_value().upper()
    name2 = namebox2.get_value().upper()
    color = (0, 55, 55)
    title1 = name_font.render(name1, True, color)
    title2 = name_font.render(name2, True, color)
    singleplayer = False
    zvuky.play(zvuky.select)
    predchozi_score = 0
    level = 0
    start_time = time() * 10
    highscore = load_highscore()
    lukas = Lukas(100, y_border)
    princezna = Lukas(100, y_border)
    princezna.set_skin_princezna()
    obstacles = Obstacles()
    for i in range(5): obstacles.add_random()
    zvuky.play(zvuky.lets_go)
    game_state = 2
    play_battle_music()
    pygame.display.update()

def empty_loop(time):
    timer = Timer()
    timer.set(time)
    while(timer):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

def load_knotstar():
    image = pygame.image.load("sprites/grafika/knotstar_games.png")
    sound = pygame.mixer.Sound("sprites/zvuky/knotstar_sound.mp3")
    sound.set_volume(0.5)
    pygame.mixer.Sound.play(sound)
    screen.blit(image, (0, 0))
    pygame.display.update()
    empty_loop(13000)

def load_company_intro():
    screen.fill((255, 255, 255))
    image = pygame.image.load("sprites/grafika/knot_foundation.png")
    sound = pygame.mixer.Sound("sprites/zvuky/company_sound.mp3")
    pygame.mixer.Sound.play(sound)
    screen.blit(image, (0, 0))
    pygame.display.update()
    empty_loop(11000)

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

class Keyboard():
    def __init__(self):
        for i in ("space", "up", "left", "right", "w", "a", "d"):
            exec(f"self.{i} = False")

def check_namebox(namebox):
    val = namebox.get_value()
    if (len(val) > name_limit):
        namebox.set_default_value(val[0:name_limit])

def check_nameboxes(nameboxes):
    for namebox in nameboxes: check_namebox(namebox)

name_limit = 12
keyboard = Keyboard()
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
################### Game Over Multiplayer Menu ################################################
game_over_background_image_multiplayer = pygame.image.load("sprites/grafika/game_over_3.png")
game_over_multiplayer = pygame_menu.Menu("", 800, 800, theme=mytheme)
game_over_multiplayer.add.button("Play", start_the_multiplayer)
game_over_multiplayer.add.button("Back to menu", set_menu)

###################################################################################
################### One players menu ##############################################
one_player = pygame_menu.Menu("", 800, 800, theme=mytheme)
namebox_single_player = one_player.add.text_input('', default=config["name"])
one_player.add.button('play', start_the_game)
one_player.add.button('back', set_menu)
################### Two players menu ##############################################
two_players = pygame_menu.Menu("", 800, 800, theme=mytheme)
namebox1 = two_players.add.text_input('', default="Levy hrac")
namebox2 = two_players.add.text_input('', default="Pravy hrac")
two_players.add.button('play', start_the_multiplayer)
two_players.add.button('back', set_menu)
###################################################################################
active_menu = menu
font = pygame.font.Font(abspath("sprites/pismo/pixel_font.ttf"), 32)
game_over_font = pygame.font.Font(abspath("sprites/pismo/pixel_font.ttf"),45)
name_font = pygame.font.Font(abspath("sprites/pismo/pixel_font.ttf"), 14)
levels = [100, 200, 300, 400, 500, float("inf")]
predchozi_score = 0
if (config["cia"]):
    load_cia_warning()
if (config["company_intro"]):
    load_company_intro()
    load_knotstar()
play_menu_music()
set_menu()
score = 0
singleplayer = True
while True:
    clock.tick(50)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            pressed = True
        if event.type == pygame.KEYUP:
            pressed = False
        if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
            if (event.key == pygame.K_UP):
                keyboard.up = pressed
            if (event.key == pygame.K_LEFT):
                keyboard.left = pressed
            if (event.key == pygame.K_RIGHT):
                keyboard.right = pressed
            if (event.key == pygame.K_w):
                keyboard.w = pressed
            if (event.key == pygame.K_a):
                keyboard.a = pressed
            if (event.key == pygame.K_d):
                keyboard.d = pressed


    if game_state==0:
        check_nameboxes([namebox1, namebox2, namebox_single_player])
        screen.fill((0, 0, 0))
        screen.blit(background_menu, (0, 0))
        active_menu.draw(screen)
        if(active_menu.update(events)):
            pygame.display.update()
            active_menu.draw(screen)
        pygame.display.update()
    elif (game_state==1):
        if (keyboard.up):
            lukas.jump()
        lukas.move()
        obstacles.move()
        if (not lukas.is_safe()):
            game_state=3
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
        lukas.animation()
        lukas.print()
        obstacles.print()
        pygame.display.update()

    elif(game_state==2):
        if (keyboard.up):
            lukas.jump()
        if (keyboard.w):
            princezna.jump()
        lukas.move()
        princezna.move(False)
        obstacles.move()
        if (not princezna.is_safe() or not lukas.is_safe()):
            message = name1
            if (not princezna.is_safe()):
                message = name2
            game_state=3
            pygame.mixer.music.stop()
            zvuky.nahodny_zvuk_smrti()
            set_highscore()
            continue
        screen.blit(background, (0, 0))
        score = int((time() * 10 - start_time))
        if ((score) % 100 == 0 and score != predchozi_score):
            zvuk = [zvuky.wow, zvuky.amazing, zvuky.sheesh, zvuky.styl_styl]
            zvuky.play(zvuk[(score//100)%len(zvuk)])
            predchozi_score = score
        text = font.render("{:0>5d}".format(score), True, (255, 255, 255))
        h_text = font.render("{:0>5d}".format(highscore), True, (255, 255, 255))
        set_level()
        text = font.render("{:0>5d}".format(score), True, (255, 255, 255))
        h_text = font.render("{:0>5d}".format(highscore), True, (255, 255, 255))
        screen.blit(text, (20, 20))
        screen.blit(h_text, (20, 54))
        lukas.print()
        lukas.animation()
        princezna.animation(False)
        princezna.print()
        screen.blit(title1, (princezna.x, princezna.y - 10))
        screen.blit(title2, (lukas.x, lukas.y - 15))
        obstacles.print()
        pygame.display.update()
    else:
        game_over_menu = game_over_multiplayer
        screen.blit(game_over_background_image_multiplayer, (0, 0))
        if (singleplayer):
            game_over_menu = game_over
            screen.blit(game_over_background_image, (0, 0))
        else:
            text = game_over_font.render(f"{message} won!".upper(), True, (50, 50, 50))
            screen.blit(text, (50, 130))
        game_over_menu.draw(screen)
        if (game_over_menu.update(events)):
            pygame.display.update()
            game_over_menu.draw(screen)
        for i, s in enumerate(medaile_score):
            if (score > s):
                screen.blit(medaile[i], (200 + i*(medaile[i].get_width() + 20), 520))
        pygame.display.update()
    beggining = False
