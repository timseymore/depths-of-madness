# -*- coding: utf-8 -*-
"""
The Depths Of Madness
 ver. 1.00.1

 - Tim Seymore  2018
"""

import pygame
import sys

from src.ui.tools.colors import Color
from src.ui.tools.gameOver import GameOver
from src.ui.tools.winGame import WinGame
from src.ui.tools.titleScreen import TitleScreen
from src.ui.tools.mousePointer import MousePointer
from src.models.players.male import Male
from src.models.players.female import Female
from src.models.enemies.demon import Demon
from src.models.enemies.insect import Insect
from src.models.enemies.zombie import Zombie
from src.models.enemies.spike import Spike
from src.models.enviroment.block import Block
from src.models.enviroment.platform import Platform
from src.models.enviroment.door import Door
from src.models.enviroment.doorLeft import DoorLeft
from src.models.powerups.extraLife import ExtraLife
from src.models.powerups.coin import Coin


# ===============
# ---CONSTANTS---

VERSION = "ver. 1.00.1"
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
BLOCK = 25
FPS = 60
GRAVITY = 47


# ====================
# -----Functions------

def main(screen):
    """
    Start game with main(display_screen)
    """
    clock = pygame.time.Clock()
    menu = TitleScreen(200, 100)
    end = GameOver(200, 100)
    win = WinGame(200, 100)

    # ---Main Game Loop---
    running = True
    while running:
        # clock ticks inside each inner loop
        # ---Control Flow---
        # main menu
        main_menu(menu, screen, clock, FPS, WIDTH, HEIGHT, BLOCK)
        # Create player object
        player = character_selection(screen, clock, FPS, WIDTH, HEIGHT, BLOCK)
        # Start game levels
        level_1(player, WIDTH, HEIGHT, BLOCK, GRAVITY, screen, clock, FPS, end, win)
        level_2(player, WIDTH, HEIGHT, BLOCK, GRAVITY, screen, clock, FPS, end, win)
        level_3(player, WIDTH, HEIGHT, BLOCK, GRAVITY, screen, clock, FPS, end, win)
    # Exit Game
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


# ---Menu Screens---

def main_menu(img, disp, time, fps, width, height, block):
    """
    Title screen for the game.
    :param img: event box img
    :param disp: display screen
    :param time: game clock
    :param fps: frames per second
    :param width: screen width
    :param height: screen height
    :param block: block size
    """
    menu_border = pygame.Surface([400, 150])
    menu_border.fill(Color.Eigengrau)
    menu_box = pygame.Surface([390, 140])
    menu_box.fill(Color.Blood)
    font = pygame.font.SysFont("Comic Sans MS", 30)
    text_surface = font.render("Enter: Start Game", False, Color.RedBrown)
    text_surface_1 = font.render("Tab: Controls", False, Color.RedBrown)
    text_surface_2 = font.render("Esc: Quit", False, Color.RedBrown)
    background = r'sounds\menu_background.wav'
    pygame.mixer.music.load(background)
    pygame.mixer.music.play(-1)

    menu = True
    while menu:
        time.tick(fps)
        for event in pygame.event.get():
            if_quit(event, True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    menu = False
                if event.key == pygame.K_TAB:
                    controls_menu(disp, time, fps, width, height, block)
        fill_background(disp, width, height, block)
        disp.blit(img.image, (200, 20))
        disp.blit(menu_border, (200, 430))
        disp.blit(menu_box, (205, 435))
        disp.blit(text_surface, (250, 430))
        disp.blit(text_surface_1, (250, 480))
        disp.blit(text_surface_2, (250, 530))
        pygame.display.flip()
    pygame.mixer.music.stop()


def controls_menu(disp, time, fps, width, height, block):
    """
    Runs the menu showing controls for the game.
    :param disp: display screen
    :param time: game clock
    :param fps: frames per second
    :param width: screen width
    :param height: screen height
    :param block: block size
    """
    menu_border = pygame.Surface([700, 500])
    menu_border.fill(Color.Eigengrau)
    menu_box = pygame.Surface([650, 450])
    menu_box.fill(Color.Blood)
    font = pygame.font.SysFont("Times Roman", 35)
    text_surface = font.render("Player Controls: ", False, Color.RedBrown, Color.Black)
    text_surface_1 = font.render("Arrow keys or 'a'/'d': Move Left/ Right", False, Color.RedBrown)
    text_surface_2 = font.render("Space Bar: Jump", False, Color.RedBrown)
    text_surface_3 = font.render("Mouse Pointer: Aim", False, Color.Blood)
    text_surface_4 = font.render("Left Mouse Button: Ability 1", False, Color.Blood)
    text_surface_5 = font.render("Right Mouse Button: Ability 2", False, Color.Blood)
    text_surface_6 = font.render("Tab: Toggle Menu", False, Color.RedBrown)
    text_surface_7 = font.render("Esc: Quit Game", False, Color.RedBrown)

    menu = True
    while menu:
        time.tick(fps)
        for event in pygame.event.get():
            if_quit(event, True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    menu = False
        fill_background(disp, width, height, block)
        disp.blit(menu_border, (50, 50))
        disp.blit(menu_box, (75, 75))
        disp.blit(text_surface, (100, 100))
        disp.blit(text_surface_1, (100, 150))
        disp.blit(text_surface_2, (100, 200))
        disp.blit(text_surface_3, (100, 250))
        disp.blit(text_surface_4, (100, 300))
        disp.blit(text_surface_5, (100, 350))
        disp.blit(text_surface_6, (100, 400))
        disp.blit(text_surface_7, (100, 450))
        pygame.display.flip()


def character_selection(disp, time, fps, width, height, block):
    """
    Runs the character selection screen.
    :param disp: display screen
    :param time: game clock
    :param fps: frames per second
    :param width: screen width
    :param height: screen height
    :param block: block size
    """
    img_1 = pygame.image.load("graphics/male_right.png")
    img_2 = pygame.image.load("graphics/female_left.png")
    menu_border = pygame.Surface([600, 400])
    menu_border.fill(Color.Eigengrau)
    menu_box = pygame.Surface([550, 350])
    menu_box.fill(Color.Blood)
    font = pygame.font.SysFont("Comic Sans MS", 60)
    font_1 = pygame.font.SysFont("Comic Sans MS", 15)
    text_surface = font.render("Choose your character", False, Color.RedBrown)
    text_surface_1 = font_1.render("1. Male", False, Color.RedBrown)
    text_surface_2 = font_1.render("2. Female", False, Color.RedBrown)
    background = r'sounds\level_background2.wav'
    pygame.mixer.music.load(background)
    pygame.mixer.music.play(-1)

    while True:
        time.tick(fps)
        for event in pygame.event.get():
            if_quit(event, True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    return Male(block + 10, 40)
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    return Female(block + 10, 40)
        fill_background(disp, width, height, block)
        disp.blit(menu_border, (100, 130))
        disp.blit(menu_box, (125, 155))
        disp.blit(img_1, (200, 220))
        disp.blit(img_2, (300, 220))
        disp.blit(text_surface, (75, 25))
        disp.blit(text_surface_1, (190, 255))
        disp.blit(text_surface_2, (290, 255))
        pygame.display.flip()


# ---Game Levels---


def level_1(player, width, height, block, gravity, disp, clock, fps, end, win):
    """
    Create playable Level 1
    :param player: player object
    :param width: screen width
    :param height: screen height
    :param block: block size
    :param gravity: constant for gravity
    :param disp: display screen
    :param clock: game clock
    :param fps: frames per second
    :param end: end text
    :param win: level clear text
    """
    # Delta time
    dt = clock.tick(fps)

    # Create Sprites Lists
    sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    extra_lives = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    doors = pygame.sprite.Group()
    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # ---BUILD THE MAP--
    add_border(width, height, block, walls, sprites)

    # Top right side ledge
    add_ledge(690, 790, 80, block, walls, sprites)

    # Left side ledge
    add_ledge(block, 200 + block, 300, block, walls, sprites)

    # Stationary platform, right side
    add_ledge(500 - block, 690, 225, block, walls, sprites)
    add_ledge(550 + block, width - block, 300, block, walls, sprites)
    add_column(550 + block, 225, 300, block, walls, sprites)

    # Columns on floor
    add_column(200, (height - block) - 60,  height - block, block, walls, sprites)
    add_column(width - 200, (height - block) - 60, height - block, block, walls, sprites)

    # Floating platform
    add_platform(420, 80, .2 * dt, 0, platforms, walls, sprites)

    # Power Ups
    add_power_up(ExtraLife, 625, 275, extra_lives, sprites)
    add_power_up(Coin, 40, height - 60, coins, sprites)

    # Door
    add_door(width - (block * 2), height - (block + 75), block, doors, sprites)

    # ---Player---
    player.add_player_start(players, sprites)

    # ---Enemies---
    spider = add_enemy(Insect, width//2, (height - block) - 35, -4, walls, players, enemies, sprites)
    bug = add_enemy(Insect, 60, (height - block) - 35, 4, walls, players, enemies, sprites)
    spike = add_enemy(Spike, width - 225, height - 50, 0, walls, players, enemies, sprites)
    spike_1 = add_enemy(Spike, 225, height - 50, 0, walls, players, enemies, sprites)

    # Update player lists
    player.update_lists(walls, enemies, extra_lives, coins, doors, platforms)

    # Set background music
    background = r'sounds\level_background1.wav'
    pygame.mixer.music.load(background)
    pygame.mixer.music.play(-1)

    while not player.dead and not player.clear:
        clock.tick(fps)

        # ---Event Processing

        # ---Game Logic
        print(player.get_state())

        # ---Drawing Code
        stone_background(disp)

        # Sprites
        sprites.update(round(dt / 1000, 2), gravity)
        disp.blit(spike.image, (spike.rect.x, spike.rect.y))
        disp.blit(spike_1.image, (spike_1.rect.x, spike_1.rect.y))
        disp.blit(spider.image, (spider.rect.x, spider.rect.y))
        disp.blit(bug.image, (bug.rect.x, bug.rect.y))
        disp.blit(player.image, (player.rect.x, player.rect.y))
        sprites.draw(disp)

        # HUD
        player.show_hud(disp)

        # Mouse Pointer
        pointer = MousePointer()
        disp.blit(pointer.image, pointer.get_pos())

        pygame.display.flip()

    pygame.mixer.music.stop()
    player.if_clear(win, disp, clock, fps)
    player.if_dead(end, disp, clock, fps)


def level_2(player, width, height, block, gravity, disp, clock, fps, end, win):
    """
    Create playable Level 2
    :param player: player object
    :param width: screen width
    :param height: screen height
    :param block: block size
    :param gravity: constant for gravity
    :param disp: display screen
    :param clock: game clock
    :param fps: frames per second
    :param end: end text
    :param win: level clear text
    """
    # Delta time
    dt = clock.tick(fps)

    # Create Sprites Lists
    sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    extra_lives = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    doors = pygame.sprite.Group()
    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # ---BUILD THE MAP---

    # Main Border
    add_border(width, height, block, walls, sprites)

    # Top right side ledge
    add_ledge(690, 790, 80, block, walls, sprites)

    # Second from top, left side ledge
    add_ledge(block, 200 + block, 225, block, walls, sprites)

    # Second from top, right side ledge
    add_ledge(600 + block, width - block, 300, block, walls, sprites)

    # Stationary platform, right side
    add_ledge(495 - block, 690, 225, block, walls, sprites)

    # Top left side ledge
    add_ledge(block, 210 + block, 200, block, walls, sprites)

    # Floor
    for i in range(5):
        add_ledge(block, 470, height - ((i + 1) * block), block, walls, sprites)

    # Column to platform, right side
    add_column(600 + block, 225, 300, block, walls, sprites)

    # Column on floor left
    add_column(470, height - 180, height, block, walls, sprites)

    # Create the platform objects
    platform = add_platform(300, 80, 0, -3, platforms, walls, sprites,)
    platform.change_bounds(block, width - block, block, height - 10*block)

    # ---ADD OBJECTS---

    # Add the Power Up objects
    add_power_up(ExtraLife, 40, 400, extra_lives, sprites)
    add_power_up(Coin, 660, 265, coins, sprites)

    # Add the door
    add_door(width - (block + 5), height - (block + 75), block, doors, sprites)

    # Add player
    player.add_player_next(players, sprites)

    # Create the enemy objects.
    zombie = add_enemy(Zombie, 60, (height - 5*block) - 37, 1, walls, players, enemies, sprites)
    demon = add_enemy(Demon, 150, (height - 5*block) - 46, -2, walls, players, enemies, sprites)
    spike = add_enemy(Spike, width - 255, height - 50, 0, walls, players, enemies, sprites)
    spike_1 = add_enemy(Spike, width - 280, height - 50, 0, walls, players, enemies, sprites)
    spike_2 = add_enemy(Spike, width - 305, height - 50, 0, walls, players, enemies, sprites)

    # Update player lists
    player.update_lists(walls, enemies, extra_lives, coins, doors, platforms)

    # Set background music
    background = r'sounds\level_background2.wav'
    pygame.mixer.music.load(background)
    pygame.mixer.music.play(-1)

    # ---MAIN LOOP---
    while not player.dead and not player.clear:
        clock.tick(fps)

        # ---Event Processing

        # ---Game Logic
        print(player.get_state())

        # ---Drawing Code
        stone_background(disp)

        # Sprites
        sprites.update(round(dt / 1000, 2), gravity)
        disp.blit(spike.image, (spike.rect.x, spike.rect.y))
        disp.blit(spike_1.image, (spike_1.rect.x, spike_1.rect.y))
        disp.blit(spike_2.image, (spike_2.rect.x, spike_2.rect.y))
        disp.blit(zombie.image, (zombie.rect.x, zombie.rect.y))
        disp.blit(demon.image, (demon.rect.x, demon.rect.y))
        disp.blit(player.image, (player.rect.x, player.rect.y))
        sprites.draw(disp)

        # HUD
        player.show_hud(disp)

        # Mouse Pointer
        pointer = MousePointer()
        disp.blit(pointer.image, pointer.get_pos())

        # --Flip Display--
        pygame.display.flip()

    pygame.mixer.music.stop()
    player.if_clear(win, disp, clock, fps)
    player.if_dead(end, disp, clock, fps)


def level_3(player, width, height, block, gravity, disp, clock, fps, end, win):
    """
    Create playable Level 3
    :param player: player object
    :param width: screen width
    :param height: screen height
    :param block: block size
    :param gravity: constant for gravity
    :param disp: display screen
    :param clock: game clock
    :param fps: frames per second
    :param end: end text
    :param win: level clear text
    """
    # Delta time
    dt = clock.tick(fps)

    # Create Sprites Lists
    sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    extra_lives = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    doors = pygame.sprite.Group()
    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # ---BUILD THE MAP---
    # --Main Border--
    add_border(width, height, block, walls, sprites)

    # Mid level floor
    add_ledge(block, 300, 300, block, walls, sprites)
    add_ledge(400, width - block, 300, block, walls, sprites)

    # Add the door
    add_door(5, height - (block + 75), block, doors, sprites, True)

    # ---ADD OBJECTS---

    # Add the Power Up objects
    add_power_up(Coin, 725, height - 60, coins, sprites)
    add_power_up(ExtraLife, 325, 200, extra_lives, sprites)

    # Add player
    player.add_player_next(players, sprites)

    # Create the enemy objects.
    zombie = add_enemy(Zombie, 60, (height - block) - 37, 1, walls, players, enemies, sprites)
    demon = add_enemy(Demon, 150, (height - block) - 46, -2, walls, players, enemies, sprites)

    # Add spikes to mid level
    spike = add_enemy(Spike, 25, 300 - block, 0, walls, players, enemies, sprites)
    spike_1 = add_enemy(Spike, 50, 300 - block, 0, walls, players, enemies, sprites)
    spike_2 = add_enemy(Spike, 75, 300 - block, 0, walls, players, enemies, sprites)
    spike_3 = add_enemy(Spike, 100, 300 - block, 0, walls, players, enemies, sprites)
    spike_4 = add_enemy(Spike, 125, 300 - block, 0, walls, players, enemies, sprites)
    spike_5 = add_enemy(Spike, 150, 300 - block, 0, walls, players, enemies, sprites)
    spike_6 = add_enemy(Spike, 175, 300 - block, 0, walls, players, enemies, sprites)
    spike_7 = add_enemy(Spike, 200, 300 - block, 0, walls, players, enemies, sprites)
    spike_8 = add_enemy(Spike, 225, 300 - block, 0, walls, players, enemies, sprites)
    spike_9 = add_enemy(Spike, 250, 300 - block, 0, walls, players, enemies, sprites)
    spike_10 = add_enemy(Spike, 275, 300 - block, 0, walls, players, enemies, sprites)

    # TODO Add mario style tunnel leading to lower level
    # Tunnel to lower level

    # Continue mid level spikes
    spike_12 = add_enemy(Spike, 400, 300 - block, 0, walls, players, enemies, sprites)
    spike_13 = add_enemy(Spike, 425, 300 - block, 0, walls, players, enemies, sprites)
    spike_14 = add_enemy(Spike, 450, 300 - block, 0, walls, players, enemies, sprites)
    spike_15 = add_enemy(Spike, 475, 300 - block, 0, walls, players, enemies, sprites)
    spike_16 = add_enemy(Spike, 500, 300 - block, 0, walls, players, enemies, sprites)
    spike_17 = add_enemy(Spike, 525, 300 - block, 0, walls, players, enemies, sprites)
    spike_18 = add_enemy(Spike, 550, 300 - block, 0, walls, players, enemies, sprites)
    spike_19 = add_enemy(Spike, 525, 300 - block, 0, walls, players, enemies, sprites)
    spike_20 = add_enemy(Spike, 550, 300 - block, 0, walls, players, enemies, sprites)
    spike_21 = add_enemy(Spike, 575, 300 - block, 0, walls, players, enemies, sprites)
    spike_22 = add_enemy(Spike, 600, 300 - block, 0, walls, players, enemies, sprites)
    spike_23 = add_enemy(Spike, 625, 300 - block, 0, walls, players, enemies, sprites)
    spike_24 = add_enemy(Spike, 650, 300 - block, 0, walls, players, enemies, sprites)
    spike_25 = add_enemy(Spike, 675, 300 - block, 0, walls, players, enemies, sprites)
    spike_26 = add_enemy(Spike, 700, 300 - block, 0, walls, players, enemies, sprites)
    spike_27 = add_enemy(Spike, 725, 300 - block, 0, walls, players, enemies, sprites)
    spike_28 = add_enemy(Spike, 750, 300 - block, 0, walls, players, enemies, sprites)

    # Update player lists
    player.update_lists(walls, enemies, extra_lives, coins, doors, platforms)
    # Music
    background = r'sounds\level_background3.wav'
    pygame.mixer.music.load(background)
    pygame.mixer.music.play(-1)

    # ---MAIN LOOP---
    while not player.dead and not player.clear:
        clock.tick(fps)
        # ---Game Logic

        # ---Drawing Code---
        # Background
        stone_background(disp)

        # Objects
        sprites.update(round(dt / 1000, 2), gravity)

        # Display spikes
        disp.blit(spike.image, (spike.rect.x, spike.rect.y))
        disp.blit(spike_1.image, (spike_1.rect.x, spike_1.rect.y))
        disp.blit(spike_2.image, (spike_2.rect.x, spike_2.rect.y))
        disp.blit(spike_3.image, (spike_3.rect.x, spike_3.rect.y))
        disp.blit(spike_4.image, (spike_4.rect.x, spike_4.rect.y))
        disp.blit(spike_5.image, (spike_5.rect.x, spike_5.rect.y))
        disp.blit(spike_6.image, (spike_6.rect.x, spike_6.rect.y))
        disp.blit(spike_7.image, (spike_7.rect.x, spike_7.rect.y))
        disp.blit(spike_8.image, (spike_8.rect.x, spike_8.rect.y))
        disp.blit(spike_9.image, (spike_9.rect.x, spike_9.rect.y))
        disp.blit(spike_10.image, (spike_10.rect.x, spike_10.rect.y))
        # TODO Display Tunnel
        disp.blit(spike_12.image, (spike_12.rect.x, spike_12.rect.y))
        disp.blit(spike_13.image, (spike_13.rect.x, spike_13.rect.y))
        disp.blit(spike_14.image, (spike_14.rect.x, spike_14.rect.y))
        disp.blit(spike_15.image, (spike_15.rect.x, spike_15.rect.y))
        disp.blit(spike_16.image, (spike_16.rect.x, spike_16.rect.y))
        disp.blit(spike_17.image, (spike_17.rect.x, spike_17.rect.y))
        disp.blit(spike_18.image, (spike_18.rect.x, spike_18.rect.y))
        disp.blit(spike_19.image, (spike_19.rect.x, spike_19.rect.y))
        disp.blit(spike_20.image, (spike_20.rect.x, spike_20.rect.y))
        disp.blit(spike_21.image, (spike_21.rect.x, spike_21.rect.y))
        disp.blit(spike_22.image, (spike_22.rect.x, spike_22.rect.y))
        disp.blit(spike_23.image, (spike_23.rect.x, spike_23.rect.y))
        disp.blit(spike_24.image, (spike_24.rect.x, spike_24.rect.y))
        disp.blit(spike_25.image, (spike_25.rect.x, spike_25.rect.y))
        disp.blit(spike_26.image, (spike_26.rect.x, spike_26.rect.y))
        disp.blit(spike_27.image, (spike_27.rect.x, spike_27.rect.y))
        disp.blit(spike_28.image, (spike_28.rect.x, spike_28.rect.y))

        disp.blit(zombie.image, (zombie.rect.x, zombie.rect.y))
        disp.blit(demon.image, (demon.rect.x, demon.rect.y))
        disp.blit(player.image, (player.rect.x, player.rect.y))
        sprites.draw(disp)

        # HUD
        player.show_hud(disp)

        # Mouse Pointer
        pointer = MousePointer()
        disp.blit(pointer.image, pointer.get_pos())

        # --Flip Display--
        pygame.display.flip()

    pygame.mixer.music.stop()
    player.if_win(win, disp, clock, fps)
    player.if_dead(end, disp, clock, fps)


# --- Display ---

def fill_background(disp, width, height, block):
    """ Fill background with stone blocks; high CPU usage."""
    for x in range(0, width, block):
        for y in range(0, height, block):
            img = pygame.image.load("graphics/stone.png")
            disp.blit(img, (x, y))


def stone_background(disp):
    """ Display dark stone background image"""
    img = pygame.image.load("graphics/stone_background.png")
    disp.blit(img, (0, 0))


# --- Event Processing ---
def if_quit(event, esc):
    """ Exit game if user inputs a quit command.
     :param event: input event
     :param esc: Boolean Value:  True if 'esc'  will exit """
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if esc and (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()

# --- Control Flow ---


# --- Create Game Objects ---

# --- Build Map ---
def add_border(width, height, block, walls, sprites):
    """
    Draws main border around screen
    :param width: screen width
    :param height: screen height
    :param block: block size
    :param walls: wall list
    :param sprites: sprites list
    """
    # Floor
    for x in range(0, width, block):
        wall = Block(x, height - block, block, block)
        walls.add(wall)
        sprites.add(wall)

    # Right side wall
    for y in range(0 - (10 * block), height, block):
        wall = Block(width - block, y, block, block)
        walls.add(wall)
        sprites.add(wall)

    # Left side wall
    for y in range(0 - (10 * block), height + (block // 2), block):
        wall = Block(0, y, block, block)
        walls.add(wall)
        sprites.add(wall)

    # Column on floor left wall
    # add_column(0, height - 80, height, block, walls, sprites)

    # Column on floor right wall
    # add_column(width - block, height - 80, height, block, walls, sprites)

    # Top left side ledge entrance
    add_ledge(block, 100 + block, 80, block, walls, sprites)


def add_ledge(start_x, end_x, y, block, walls, sprites):
    """
    Draw a horizontal ledge
    :param start_x: starting position x
    :param end_x: ending position x
    :param y: y position
    :param block: block size
    :param walls: wall list
    :param sprites: sprites list
    """
    for x in range(start_x, end_x, block):
        wall = Block(x, y, block, block)
        walls.add(wall)
        sprites.add(wall)


def add_column(x, start_y, end_y, block, walls, sprites):
    """
    Draw a vertical column
    :param x: x position
    :param start_y: top position y
    :param end_y: bottom position y
    :param block: block size
    :param walls: wall list
    :param sprites: sprites list
    """
    for y in range(start_y, end_y, block):
        wall = Block(x, y, block, block)
        walls.add(wall)
        sprites.add(wall)


def add_platform(x, y, x_speed, y_speed, platforms, walls, sprites):
    """
    Draw a movable horizontal platform
    :param x: x position
    :param y: y position
    :param x_speed: speed in x direction
    :param y_speed: speed in y direction
    :param platforms: platform list
    :param walls: wall list
    :param sprites: sprites list
    """
    platform = Platform(x, y)
    platform.change_x = x_speed
    platform.change_y = y_speed
    platforms.add(platform)
    platform.walls = walls
    sprites.add(platform)
    return platform


def add_door(x, y, block, doors, sprites, left=False):
    """
    Draw the door object on right side of screen by default, left by input
    :param x: x position
    :param y: y position
    :param block: block size
    :param doors: door list
    :param sprites: sprites list
    :param left: Default False, enter True to place on left side
    """
    if left:
        door = DoorLeft(x, y, block, block + 50)
        doors.add(door)
        sprites.add(door)
    else:
        door = Door(x, y, block, block + 50)
        doors.add(door)
        sprites.add(door)


# --- Player and Enemies ---

def add_enemy(obj, x, y, speed, walls, players, enemies, sprites):
    """
    Adds a specific enemy type to the level
    :param obj: Enemy class
    :param x: start x
    :param y: start y
    :param speed: change x speed
    :param walls: wall list
    :param players: player list
    :param enemies: enemy list
    :param sprites: all sprite list
    Returns: New enemy object
    """
    start_x = x
    start_y = y
    enemy = obj(start_x, start_y)
    enemy.change_x = speed
    enemy.walls = walls
    enemy.player = players
    enemies.add(enemy)
    sprites.add(enemy)
    return enemy


# --- Other Objects ---
def add_power_up(obj, x, y, power_list, sprites):
    """
    Add a power up to the level
    :param obj: power up object to add
    :param x: x position
    :param y: y position
    :param power_list: power up list
    :param sprites: sprites list
    """
    power = obj(x, y)
    power_list.add(power)
    sprites.add(power)


# ======================
# -------Run game-------

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('The Depths Of Madness      -- {}--'.format(VERSION))
    main(SCREEN)
