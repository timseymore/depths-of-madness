# -*- coding: utf-8 -*-
""" The Depths Of Madness
                ver. 1.00

 A 2-D platform game using pygame

 - Tim Seymore  2018
"""


import sys
import random
import pygame

from src.models.enemies.enemy import Enemy
from src.models.enemies.demon import Demon
from src.models.enemies.insect import Insect
from src.models.enemies.spike import Spike
from src.models.enemies.zombie import Zombie
from src.models.enviroment.block import Block
from src.models.enviroment.door import Door
from src.models.enviroment.doorLeft import DoorLeft
from src.models.enviroment.platform import Platform
from src.models.players.player import Player
from src.models.players.female import Female
from src.models.players.male import Male
from src.models.powerUps.powerUp import PowerUp
from src.models.powerUps.coin import Coin
from src.models.powerUps.extraLife import ExtraLife
from src.models.groups.spritegroup import SpriteGroup
from src.ui.tools.colors import Color
from src.ui.tools.gameOver import GameOver
from src.ui.tools.mousePointer import MousePointer
from src.ui.tools.titleScreen import TitleScreen
from src.ui.tools.winGame import WinGame


# =================
# --- CONSTANTS ---

VERSION = "ver. 1.00.0"
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
BLOCK = 25
FPS = 60
GRAVITY = 47
CLOCK = pygame.time.Clock()
MENU_SCREEN = TitleScreen(200, 100)
END_SCREEN = GameOver(200, 100)
WIN_SCREEN = WinGame(200, 100)


# ======================
# ------ Classes -------

class Level(object):
    """ A playable level in the game """

    def __init__(self, player: Player):
        """ Constructor """

        self.player = player
        self.dt = CLOCK.tick(FPS)
        self.sprites = SpriteGroup()
        self.walls = SpriteGroup()
        self.platforms = SpriteGroup()
        self.extra_lives = SpriteGroup()
        self.coins = SpriteGroup()
        self.doors = SpriteGroup()
        self.players = SpriteGroup()
        self.enemies = SpriteGroup()

    @staticmethod
    def fill_background():
        """ Fill background with stone blocks; high CPU usage."""

        for x in range(0, WIDTH, BLOCK):
            for y in range(0, HEIGHT, BLOCK):
                img = pygame.image.load(r'src/graphics/stone.png')
                SCREEN.blit(img, (x, y))

    def add_border(self):
        """ Draws main border around screen """

        # Floor
        for x in range(0, WIDTH, BLOCK):
            wall = Block(x, HEIGHT - BLOCK, BLOCK, BLOCK)
            self.walls.add(wall)
            self.sprites.add(wall)

        # Right side wall
        for y in range(0 - (10 * BLOCK), HEIGHT, BLOCK):
            wall = Block(WIDTH - BLOCK, y, BLOCK, BLOCK)
            self.walls.add(wall)
            self.sprites.add(wall)

        # Left side wall
        for y in range(0 - (10 * BLOCK), HEIGHT + (BLOCK // 2), BLOCK):
            wall = Block(0, y, BLOCK, BLOCK)
            self.walls.add(wall)
            self.sprites.add(wall)

        # Top left side ledge entrance
        self.add_ledge(BLOCK, 100 + BLOCK, 80)

    def add_ledge(self, start_x, end_x, y):
        """ Draw a horizontal ledge

         - start_x: int : starting position x
         - end_x: int : ending position x
         - y: int : y position
        """

        for x in range(start_x, end_x, BLOCK):
            wall = Block(x, y, BLOCK, BLOCK)
            self.walls.add(wall)
            self.sprites.add(wall)

    def add_column(self, x, start_y, end_y):
        """ Draw a vertical column

         - x: int : x position
         - start_y: int : top position y
         - end_y: int : bottom position y
        """

        for y in range(start_y, end_y, BLOCK):
            wall = Block(x, y, BLOCK, BLOCK)
            self.walls.add(wall)
            self.sprites.add(wall)

    def add_platform(self, x, y, x_speed, y_speed):
        """ Draw a movable horizontal platform and add to all lists

         - x: int : x position
         - y: int : y position
         - x_speed: int : speed in x direction
         - y_speed: int : speed in y direction
         Returns: Platform : New platform instance with given parameters
        """

        platform = Platform(x, y, x_speed, y_speed, BLOCK, WIDTH - BLOCK, 0, HEIGHT - BLOCK)
        self.platforms.add(platform)
        platform.walls = self.walls
        self.sprites.add(platform)
        return platform

    def add_door(self, x, y, exit_level, left=False):
        """ Draw the door object on right side of screen by default, left by input

         - x: int : x position
         - y: int : y position
         - exit_level: Level: level that door will lead to
         - left: bool : Default False, enter True to place on left side
        """

        if left:
            door = DoorLeft(x, y, BLOCK, BLOCK + 50, exit_level)
            self.doors.add(door)
            self.sprites.add(door)
        else:
            door = Door(x, y, BLOCK, BLOCK + 50, exit_level)
            self.doors.add(door)
            self.sprites.add(door)

    def add_enemy(self, obj, x, y, speed):
        """ Adds a specific enemy type to the level

         - obj: Enemy : Enemy class name
         - x: int : start x
         - y: int : start y
         - speed: int : change x speed
        Returns: Enemy : new Enemy instance with given parameters
        """

        enemy = obj(x, y)
        enemy.change_x = speed
        enemy.walls = self.walls
        enemy.player = self.players
        self.enemies.add(enemy)
        self.sprites.add(enemy)
        return enemy

    def add_power_up(self, obj, x, y, power_list):
        """ Adds a power up object to the sprites list

         - obj: PowerUP : power up object to add
         - x: int : x position
         - y: int : y position
         - power_list: SpriteGroup : SpriteGroup to add power up to
        """

        power = obj(x, y)
        power_list.add(power)
        self.sprites.add(power)

    @staticmethod
    def stone_background():
        """ Display dark stone background image"""

        img = pygame.image.load(r'src/graphics/stone_background.png')
        SCREEN.blit(img, (0, 0))


class Game:
    """ Main game object

    Start game with Game().main()
    """

    def main(self):
        """ Main run function """

        running = True
        while running:
            # Show menu -> player selection -> start game
            # NOTE: game clock ticks inside each inner function
            self.main_menu()
            player = self.character_selection()
            self.level_1(player)
            self.level_2(player)
            self.level_3(player)
            # self.level_4(player)

        # player presses 'esc' to exit game
        pygame.mixer.quit()
        pygame.quit()

    def main_menu(self):
        """ Title screen for the game with main menu options """

        # set up menu screen gui
        menu_border = pygame.Surface([400, 150])
        menu_border.fill(Color.Eigengrau)
        menu_box = pygame.Surface([390, 140])
        menu_box.fill(Color.Blood)
        # set up text surfaces
        font = pygame.font.SysFont("Comic Sans MS", 30)
        text_surface = font.render("Enter: Start Game", False, Color.RedBrown)
        text_surface_1 = font.render("Tab: Controls", False, Color.RedBrown)
        text_surface_2 = font.render("Esc: Quit", False, Color.RedBrown)
        # set up background music
        background = r'src\sounds\menu_background.wav'
        pygame.mixer.music.load(background)
        pygame.mixer.music.play(-1)

        menu = True
        while menu:
            CLOCK.tick(FPS)
            # check for and handle player input
            for event in pygame.event.get():
                # 'esc' or closing the window exits the game
                self.check_for_quit(event, True)
                if event.type == pygame.KEYDOWN:
                    # 'enter' exits menu and continues game
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        pygame.mixer.music.stop()
                        menu = False
                    # 'tab' toggles between main menu and control menu
                    if event.key == pygame.K_TAB:
                        self.controls_menu()
            # draw menu to screen
            self.fill_background()
            SCREEN.blit(MENU_SCREEN.image, (200, 20))
            SCREEN.blit(menu_border, (200, 430))
            SCREEN.blit(menu_box, (205, 435))
            SCREEN.blit(text_surface, (250, 430))
            SCREEN.blit(text_surface_1, (250, 480))
            SCREEN.blit(text_surface_2, (250, 530))
            pygame.display.flip()

    def controls_menu(self):
        """ Runs the menu showing controls for the game """

        # set up menu gui
        menu_border = pygame.Surface([700, 500])
        menu_border.fill(Color.Eigengrau)
        menu_box = pygame.Surface([650, 450])
        menu_box.fill(Color.Blood)
        # set up text surfaces
        font = pygame.font.SysFont("Times Roman", 35)
        text_surface = font.render("Player Controls: ", False, Color.RedBrown, Color.Black)
        text_surface_1 = font.render("Arrow Keys or 'a'/'d': Move Left/ Right", False, Color.RedBrown)
        text_surface_2 = font.render("Space Bar: Jump", False, Color.RedBrown)
        text_surface_3 = font.render("Mouse Pointer: Aim", False, Color.RedBrown)
        text_surface_4 = font.render("Left Mouse Button: Ability 1", False, Color.RedBrown)
        text_surface_5 = font.render("Right Mouse Button: Ability 2", False, Color.RedBrown)
        text_surface_6 = font.render("Tab: Toggle Menu", False, Color.RedBrown)
        text_surface_7 = font.render("Esc: Quit Game", False, Color.RedBrown)

        menu = True
        while menu:
            CLOCK.tick(FPS)

            # check for and handle player input
            for event in pygame.event.get():
                # 'esc' or closing the window exits the game
                self.check_for_quit(event, True)
                if event.type == pygame.KEYDOWN:
                    # 'tab' toggles between control menu and main menu
                    if event.key == pygame.K_TAB:
                        menu = False

            # draw control menu to  screen
            self.fill_background()
            SCREEN.blit(menu_border, (50, 50))
            SCREEN.blit(menu_box, (75, 75))
            SCREEN.blit(text_surface, (100, 100))
            SCREEN.blit(text_surface_1, (100, 150))
            SCREEN.blit(text_surface_2, (100, 200))
            SCREEN.blit(text_surface_3, (100, 250))
            SCREEN.blit(text_surface_4, (100, 300))
            SCREEN.blit(text_surface_5, (100, 350))
            SCREEN.blit(text_surface_6, (100, 400))
            SCREEN.blit(text_surface_7, (100, 450))
            pygame.display.flip()

    def character_selection(self):
        """ Runs the character selection screen.

        returns: Player : Player instance
        """

        img_1 = pygame.image.load(r"src/graphics/male_right.png")
        img_2 = pygame.image.load(r"src/graphics/female_left.png")
        menu_border = pygame.Surface([600, 400])
        menu_border.fill(Color.Eigengrau)
        menu_box = pygame.Surface([550, 350])
        menu_box.fill(Color.Blood)
        font = pygame.font.SysFont("Comic Sans MS", 60)
        font_1 = pygame.font.SysFont("Comic Sans MS", 15)
        text_surface = font.render("Choose your character", False, Color.RedBrown)
        text_surface_1 = font_1.render("1. Male", False, Color.RedBrown)
        text_surface_2 = font_1.render("2. Female", False, Color.RedBrown)
        background = r'src\sounds\level_background2.wav'
        pygame.mixer.music.load(background)
        pygame.mixer.music.play(-1)

        while True:
            CLOCK.tick(FPS)
            for event in pygame.event.get():
                self.check_for_quit(event, True)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        return Male(BLOCK + 10, 40)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        return Female(BLOCK + 10, 40)
            self.fill_background()
            SCREEN.blit(menu_border, (100, 130))
            SCREEN.blit(menu_box, (125, 155))
            SCREEN.blit(img_1, (200, 220))
            SCREEN.blit(img_2, (300, 220))
            SCREEN.blit(text_surface, (75, 25))
            SCREEN.blit(text_surface_1, (190, 255))
            SCREEN.blit(text_surface_2, (290, 255))
            pygame.display.flip()

    # TODO 2: Refactor first 3 levels using EmptyLevel class
    def level_1(self, player):
        """ Create playable Level 1

        - player: Player : player to play trough level
        """

        # Delta time
        dt = CLOCK.tick(FPS)

        # Create Sprites Lists
        sprites = SpriteGroup()
        walls = SpriteGroup()
        platforms = SpriteGroup()
        extra_lives = SpriteGroup()
        coins = SpriteGroup()
        doors = SpriteGroup()
        players = SpriteGroup()
        enemies = SpriteGroup()

        # ---BUILD THE MAP--
        self.add_border(WIDTH, HEIGHT, BLOCK, walls, sprites)

        # Top right side ledge
        self.add_ledge(690, 790, 80, BLOCK, walls, sprites)

        # Left side ledge
        self.add_ledge(BLOCK, 200 + BLOCK, 300, BLOCK, walls, sprites)

        # Stationary platform, right side
        self.add_ledge(500 - BLOCK, 690, 225, BLOCK, walls, sprites)
        self.add_ledge(550 + BLOCK, WIDTH - BLOCK, 300, BLOCK, walls, sprites)
        self.add_column(550 + BLOCK, 225, 300, BLOCK, walls, sprites)

        # Columns on floor
        self.add_column(200, (HEIGHT - BLOCK) - 60,  HEIGHT - BLOCK, BLOCK, walls, sprites)
        self.add_column(WIDTH - 200, (HEIGHT - BLOCK) - 60, HEIGHT - BLOCK, BLOCK, walls, sprites)

        # Floating platform
        self.add_platform(420, 80, .2 * dt, 0, platforms, walls, sprites)

        # Power Ups
        # noinspection PyTypeChecker
        self.add_power_up(ExtraLife, 625, 275, extra_lives, sprites)
        # noinspection PyTypeChecker
        self.add_power_up(Coin, 40, HEIGHT - 60, coins, sprites)

        # Door
        self.add_door(WIDTH - (BLOCK * 2), HEIGHT - (BLOCK + 75), BLOCK, doors, sprites, random.randint(0, 1))

        # ---Player---
        player.add_player_start(players, sprites)

        # ---Enemies---
        # noinspection PyTypeChecker
        spider = self.add_enemy(Insect, WIDTH//2, (HEIGHT - BLOCK) - 35, -4, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        bug = self.add_enemy(Insect, 60, (HEIGHT - BLOCK) - 35, 4, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike = self.add_enemy(Spike, WIDTH - 225, HEIGHT - 50, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_1 = self.add_enemy(Spike, 225, HEIGHT - 50, 0, walls, players, enemies, sprites)

        # Update player lists
        player.update_lists(walls, enemies, extra_lives, coins, doors, platforms)

        # Set background music
        background = r'src\sounds\level_background1.wav'
        pygame.mixer.music.load(background)
        pygame.mixer.music.play(-1)

        while not player.dead and not player.clear:
            CLOCK.tick(FPS)

            # ---Event Processing

            # ---Game Logic
            print(player.get_state())

            # ---Drawing Code
            self.stone_background()

            # Sprites
            sprites.update(round(dt / 1000, 2), GRAVITY)
            SCREEN.blit(spike.image, (spike.rect.x, spike.rect.y))
            SCREEN.blit(spike_1.image, (spike_1.rect.x, spike_1.rect.y))
            SCREEN.blit(spider.image, (spider.rect.x, spider.rect.y))
            SCREEN.blit(bug.image, (bug.rect.x, bug.rect.y))
            SCREEN.blit(player.image, (player.rect.x, player.rect.y))
            sprites.draw(SCREEN)

            # HUD
            player.show_hud(SCREEN)

            # Mouse Pointer
            pointer = MousePointer()
            SCREEN.blit(pointer.image, pointer.get_pos())

            pygame.display.flip()

        pygame.mixer.music.stop()
        player.if_clear(WIN_SCREEN, SCREEN, CLOCK, FPS)
        player.if_dead(END_SCREEN, SCREEN, CLOCK, FPS)

    def level_2(self, player):
        """ Create playable Level 2

        - player: Player : player to play trough level
        """

        # Delta time
        dt = CLOCK.tick(FPS)

        # Create Sprites Lists
        sprites = SpriteGroup()
        walls = SpriteGroup()
        platforms = SpriteGroup()
        extra_lives = SpriteGroup()
        coins = SpriteGroup()
        doors = SpriteGroup()
        players = SpriteGroup()
        enemies = SpriteGroup()

        # ---BUILD THE MAP---

        # Main Border
        self.add_border(WIDTH, HEIGHT, BLOCK, walls, sprites)

        # Top right side ledge
        self.add_ledge(690, 790, 80, BLOCK, walls, sprites)

        # Second from top, left side ledge
        self.add_ledge(BLOCK, 200 + BLOCK, 225, BLOCK, walls, sprites)

        # Second from top, right side ledge
        self.add_ledge(600 + BLOCK, WIDTH - BLOCK, 300, BLOCK, walls, sprites)

        # Stationary platform, right side
        self.add_ledge(495 - BLOCK, 690, 225, BLOCK, walls, sprites)

        # Top left side ledge
        self.add_ledge(BLOCK, 210 + BLOCK, 200, BLOCK, walls, sprites)

        # Floor
        for i in range(5):
            self.add_ledge(BLOCK, 470, HEIGHT - ((i + 1) * BLOCK), BLOCK, walls, sprites)

        # Column to platform, right side
        self.add_column(600 + BLOCK, 225, 300, BLOCK, walls, sprites)

        # Column on floor left
        self.add_column(470, HEIGHT - 180, HEIGHT, BLOCK, walls, sprites)

        # Create the platform objects
        platform = self.add_platform(300, 80, 0, 3, platforms, walls, sprites,)
        platform.change_bounds(BLOCK, WIDTH - BLOCK, BLOCK, HEIGHT - (BLOCK * 10))

        # ---ADD OBJECTS---

        # Add the Power Up objects
        # noinspection PyTypeChecker
        self.add_power_up(ExtraLife, 40, 400, extra_lives, sprites)
        # noinspection PyTypeChecker
        self.add_power_up(Coin, 660, 265, coins, sprites)

        # Add the door
        self.add_door(WIDTH - (BLOCK + 5), HEIGHT - (BLOCK + 75), BLOCK, doors, sprites, random.randint(0, 2))

        # Add player
        player.add_player_next(players, sprites)

        # Create the enemy objects.
        # noinspection PyTypeChecker
        zombie = self.add_enemy(Zombie, 60, (HEIGHT - 5 * BLOCK) - 37, 1, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        demon = self.add_enemy(Demon, 150, (HEIGHT - 5 * BLOCK) - 46, -2, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike = self.add_enemy(Spike, WIDTH - 255, HEIGHT - 50, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_1 = self.add_enemy(Spike, WIDTH - 280, HEIGHT - 50, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_2 = self.add_enemy(Spike, WIDTH - 305, HEIGHT - 50, 0, walls, players, enemies, sprites)

        # Update player lists
        player.update_lists(walls, enemies, extra_lives, coins, doors, platforms)

        # Set background music
        background = r'src\sounds\level_background2.wav'
        pygame.mixer.music.load(background)
        pygame.mixer.music.play(-1)

        # ---MAIN LOOP---
        while not player.dead and not player.clear:
            CLOCK.tick(FPS)

            # ---Event Processing

            # ---Game Logic
            print(player.get_state())

            # ---Drawing Code
            self.stone_background()

            # Sprites
            sprites.update(round(dt / 1000, 2), GRAVITY)
            SCREEN.blit(spike.image, (spike.rect.x, spike.rect.y))

            SCREEN.blit(spike_1.image, (spike_1.rect.x, spike_1.rect.y))
            SCREEN.blit(spike_2.image, (spike_2.rect.x, spike_2.rect.y))
            SCREEN.blit(zombie.image, (zombie.rect.x, zombie.rect.y))
            SCREEN.blit(demon.image, (demon.rect.x, demon.rect.y))
            SCREEN.blit(player.image, (player.rect.x, player.rect.y))
            sprites.draw(SCREEN)

            # HUD
            player.show_hud(SCREEN)

            # Mouse Pointer
            pointer = MousePointer()
            SCREEN.blit(pointer.image, pointer.get_pos())

            # --Flip Display--
            pygame.display.flip()

        pygame.mixer.music.stop()
        player.if_clear(WIN_SCREEN, SCREEN, CLOCK, FPS)
        player.if_dead(END_SCREEN, SCREEN, CLOCK, FPS)

    def level_3(self, player):
        """ Create playable Level 3

        - player: Player : player to play trough level
        """

        # Delta time
        dt = CLOCK.tick(FPS)

        # Create Sprites Lists
        sprites = SpriteGroup()
        walls = SpriteGroup()
        platforms = SpriteGroup()
        extra_lives = SpriteGroup()
        coins = SpriteGroup()
        doors = SpriteGroup()
        players = SpriteGroup()
        enemies = SpriteGroup()

        # ---BUILD THE MAP---
        # --Main Border--
        self.add_border(WIDTH, HEIGHT, BLOCK, walls, sprites)

        # Mid level floor
        self.add_ledge(BLOCK, 300, 300, BLOCK, walls, sprites)
        self.add_ledge(400, WIDTH - BLOCK, 300, BLOCK, walls, sprites)

        # Add the door
        self.add_door(5, HEIGHT - (BLOCK + 75), BLOCK, doors, sprites, random.randint(0, 3), True)

        # ---ADD OBJECTS---

        # Add the Power Up objects
        # noinspection PyTypeChecker
        self.add_power_up(Coin, 725, HEIGHT - 60, coins, sprites)
        # noinspection PyTypeChecker
        self.add_power_up(ExtraLife, 325, 200, extra_lives, sprites)

        # Add player
        player.add_player_next(players, sprites)

        # Create the enemy objects.
        # noinspection PyTypeChecker
        zombie = self.add_enemy(Zombie, 60, (HEIGHT - BLOCK) - 37, 1, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        demon = self.add_enemy(Demon, 150, (HEIGHT - BLOCK) - 46, -2, walls, players, enemies, sprites)

        # Add spikes to mid level
        # noinspection PyTypeChecker
        spike = self.add_enemy(Spike, 25, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_1 = self.add_enemy(Spike, 50, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_2 = self.add_enemy(Spike, 75, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_3 = self.add_enemy(Spike, 100, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_4 = self.add_enemy(Spike, 125, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_5 = self.add_enemy(Spike, 150, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_6 = self.add_enemy(Spike, 175, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_7 = self.add_enemy(Spike, 200, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_8 = self.add_enemy(Spike, 225, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_9 = self.add_enemy(Spike, 250, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_10 = self.add_enemy(Spike, 275, 300 - BLOCK, 0, walls, players, enemies, sprites)

        # TODO 3: Add Mario style tunnel leading to lower level
        # Tunnel to lower level

        # Continue mid level spikes
        # noinspection PyTypeChecker
        spike_12 = self.add_enemy(Spike, 400, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_13 = self.add_enemy(Spike, 425, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_14 = self.add_enemy(Spike, 450, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_15 = self.add_enemy(Spike, 475, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_16 = self.add_enemy(Spike, 500, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_17 = self.add_enemy(Spike, 525, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_18 = self.add_enemy(Spike, 550, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_19 = self.add_enemy(Spike, 525, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_20 = self.add_enemy(Spike, 550, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_21 = self.add_enemy(Spike, 575, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_22 = self.add_enemy(Spike, 600, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_23 = self.add_enemy(Spike, 625, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_24 = self.add_enemy(Spike, 650, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_25 = self.add_enemy(Spike, 675, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_26 = self.add_enemy(Spike, 700, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_27 = self.add_enemy(Spike, 725, 300 - BLOCK, 0, walls, players, enemies, sprites)
        # noinspection PyTypeChecker
        spike_28 = self.add_enemy(Spike, 750, 300 - BLOCK, 0, walls, players, enemies, sprites)

        # Update player lists
        player.update_lists(walls, enemies, extra_lives, coins, doors, platforms)

        # Music
        background = r'src\sounds\level_background3.wav'
        pygame.mixer.music.load(background)
        pygame.mixer.music.play(-1)

        # ---MAIN LOOP---
        while not player.dead and not player.clear:
            CLOCK.tick(FPS)
            # ---Game Logic

            # ---Drawing Code---
            # Background
            self.stone_background()

            # Objects
            sprites.update(round(dt / 1000, 2), GRAVITY)

            # Display spikes
            SCREEN.blit(spike.image, (spike.rect.x, spike.rect.y))
            SCREEN.blit(spike_1.image, (spike_1.rect.x, spike_1.rect.y))
            SCREEN.blit(spike_2.image, (spike_2.rect.x, spike_2.rect.y))
            SCREEN.blit(spike_3.image, (spike_3.rect.x, spike_3.rect.y))
            SCREEN.blit(spike_4.image, (spike_4.rect.x, spike_4.rect.y))
            SCREEN.blit(spike_5.image, (spike_5.rect.x, spike_5.rect.y))
            SCREEN.blit(spike_6.image, (spike_6.rect.x, spike_6.rect.y))
            SCREEN.blit(spike_7.image, (spike_7.rect.x, spike_7.rect.y))
            SCREEN.blit(spike_8.image, (spike_8.rect.x, spike_8.rect.y))
            SCREEN.blit(spike_9.image, (spike_9.rect.x, spike_9.rect.y))
            SCREEN.blit(spike_10.image, (spike_10.rect.x, spike_10.rect.y))
            # TODO 3: Display Mario style tunnel here
            SCREEN.blit(spike_12.image, (spike_12.rect.x, spike_12.rect.y))
            SCREEN.blit(spike_13.image, (spike_13.rect.x, spike_13.rect.y))
            SCREEN.blit(spike_14.image, (spike_14.rect.x, spike_14.rect.y))
            SCREEN.blit(spike_15.image, (spike_15.rect.x, spike_15.rect.y))
            SCREEN.blit(spike_16.image, (spike_16.rect.x, spike_16.rect.y))
            SCREEN.blit(spike_17.image, (spike_17.rect.x, spike_17.rect.y))
            SCREEN.blit(spike_18.image, (spike_18.rect.x, spike_18.rect.y))
            SCREEN.blit(spike_19.image, (spike_19.rect.x, spike_19.rect.y))
            SCREEN.blit(spike_20.image, (spike_20.rect.x, spike_20.rect.y))
            SCREEN.blit(spike_21.image, (spike_21.rect.x, spike_21.rect.y))
            SCREEN.blit(spike_22.image, (spike_22.rect.x, spike_22.rect.y))
            SCREEN.blit(spike_23.image, (spike_23.rect.x, spike_23.rect.y))
            SCREEN.blit(spike_24.image, (spike_24.rect.x, spike_24.rect.y))
            SCREEN.blit(spike_25.image, (spike_25.rect.x, spike_25.rect.y))
            SCREEN.blit(spike_26.image, (spike_26.rect.x, spike_26.rect.y))
            SCREEN.blit(spike_27.image, (spike_27.rect.x, spike_27.rect.y))
            SCREEN.blit(spike_28.image, (spike_28.rect.x, spike_28.rect.y))

            SCREEN.blit(zombie.image, (zombie.rect.x, zombie.rect.y))
            SCREEN.blit(demon.image, (demon.rect.x, demon.rect.y))
            SCREEN.blit(player.image, (player.rect.x, player.rect.y))
            sprites.draw(SCREEN)

            # HUD
            player.show_hud(SCREEN)

            # Mouse Pointer
            pointer = MousePointer()
            SCREEN.blit(pointer.image, pointer.get_pos())

            # --Flip Display--
            pygame.display.flip()

        pygame.mixer.music.stop()
        player.if_clear(WIN_SCREEN, SCREEN, CLOCK, FPS)
        player.if_dead(END_SCREEN, SCREEN, CLOCK, FPS)

    # TODO 1: Finish implementing level 4
    @staticmethod
    def level_4(player):
        """ Creates playable level 4

        - player: Player : player to play trough level
        """

        # Set up level
        dt = CLOCK.tick(FPS)
        level = Level(player)

        # ---BUILD THE MAP---
        # --Main Border--
        level.add_border()

        # add door
        level.add_door(WIDTH - (BLOCK * 2), (HEIGHT - (BLOCK + 75)) / 2, BLOCK, random.randint(0, 1))

        # ledge under door
        level.add_ledge(WIDTH - (BLOCK * 6), WIDTH - BLOCK, (HEIGHT / 2) + BLOCK)

        # middle floating platform
        level.add_platform(WIDTH / 2, (HEIGHT / 2) + (BLOCK * 2), 0, 0)

        # left floating platform
        level.add_platform(BLOCK * 8, HEIGHT - (BLOCK * 5),  1, 0)

        # ---ADD OBJECTS---

        # Add the Power Up objects

        # add player
        player.add_player_start(level.players, level.sprites)

        # add the enemy objects

        # floor spikes
        level.add_enemy(Spike, BLOCK, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 2, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 3, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 4, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 5, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 6, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 7, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 8, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 9, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 10, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 11, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 12, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 13, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 14, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 15, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 16, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 17, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 18, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 19, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 20, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 21, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 22, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 23, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 24, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 25, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 26, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 27, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 28, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 29, HEIGHT - (BLOCK * 2), 0)
        level.add_enemy(Spike, BLOCK * 30, HEIGHT - (BLOCK * 2), 0)

        # update player lists
        player.update_lists(level.walls,
                            level.enemies,
                            level.extra_lives,
                            level.coins,
                            level.doors,
                            level.platforms)

        # Set and begin playing background music
        background = r'src\sounds\level_background1.wav'
        pygame.mixer.music.load(background)
        pygame.mixer.music.play(-1)

        # Main loop
        while not player.dead and not player.clear:
            CLOCK.tick(FPS)

            # ---Event Processing---

            # ---Game Logic---
            print(player.get_state())

            # ---Drawing Code---
            level.stone_background()

            # Sprites
            level.sprites.update(round(dt / 1000, 2), GRAVITY)

            # draw sprites: SCREEN.blit(obj.image, (obj.rect.x, obj.rect.y))

            level.sprites.draw(SCREEN)

            # HUD
            player.show_hud(SCREEN)

            # Mouse Pointer
            pointer = MousePointer()
            SCREEN.blit(pointer.image, pointer.get_pos())

            pygame.display.flip()

        # ---End Main Loop---
        pygame.mixer.music.stop()
        player.if_win(WIN_SCREEN, SCREEN, CLOCK, FPS)
        player.if_dead(END_SCREEN, SCREEN, CLOCK, FPS)

    # TODO: Add level 5 (Boss level)

    @staticmethod
    def level_template(player):
        """ Creates playable empty level

        Use this template to create new levels

        - player: Player : player to play trough level
        """

        # Set up level
        dt = CLOCK.tick(FPS)
        level = Level(player)

        # ---BUILD THE MAP---
        # --Main Border--
        level.add_border()

        # add door
        level.add_door(WIDTH - (BLOCK * 2), HEIGHT - (BLOCK + 75), BLOCK, random.randint(0, 1))

        # ---ADD OBJECTS---

        # Add the Power Up objects

        # add player
        player.add_player_start(level.players, level.sprites)

        # add the enemy objects

        # update player lists
        player.update_lists(level.walls,
                            level.enemies,
                            level.extra_lives,
                            level.coins,
                            level.doors,
                            level.platforms)

        # Set and begin playing background music
        background = r'src\sounds\level_background1.wav'
        pygame.mixer.music.load(background)
        pygame.mixer.music.play(-1)

        # Main loop
        while not player.dead and not player.clear:

            CLOCK.tick(FPS)

            # ---Event Processing---

            # ---Game Logic---
            print(player.get_state())

            # ---Drawing Code---
            level.stone_background()

            # Sprites
            level.sprites.update(round(dt / 1000, 2), GRAVITY)

            # draw sprites: SCREEN.blit(obj.image, (obj.rect.x, obj.rect.y))

            level.sprites.draw(SCREEN)

            # HUD
            player.show_hud(SCREEN)

            # Mouse Pointer
            pointer = MousePointer()
            SCREEN.blit(pointer.image, pointer.get_pos())

            pygame.display.flip()

        # ---End Main Loop---
        pygame.mixer.music.stop()
        player.if_win(WIN_SCREEN, SCREEN, CLOCK, FPS)
        player.if_dead(END_SCREEN, SCREEN, CLOCK, FPS)

    @staticmethod
    def fill_background():
        """ Fill background with stone blocks; high CPU usage."""

        for x in range(0, WIDTH, BLOCK):
            for y in range(0, HEIGHT, BLOCK):
                img = pygame.image.load(r'src/graphics/stone.png')
                SCREEN.blit(img, (x, y))

    @staticmethod
    def stone_background():
        """ Display dark stone background image"""

        img = pygame.image.load(r'src/graphics/stone_background.png')
        SCREEN.blit(img, (0, 0))

    @staticmethod
    def check_for_quit(event, esc):
        """ Exit game if user inputs a quit command.

          - event: pygame.event : input event
          - esc: bool : True if 'esc'  will exit
        """

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if esc and (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    def add_border(self, width, height, block, walls, sprites):
        """ Draws main border around screen

         - width: int : screen width
         - height: int : screen height
         - block: int : block size
         - walls: SpriteGroup : wall list
         - sprites: SpriteGroup : sprites list
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
        self.add_ledge(block, 100 + block, 80, block, walls, sprites)

    @staticmethod
    def add_ledge(start_x, end_x, y, block, walls, sprites):
        """ Draw a horizontal ledge

         - start_x: int : starting position x
         - end_x: int : ending position x
         - y: int : y position
         - block: int : block size
         - walls: int : wall list
         - sprites: SpriteGroup : sprites list
        """

        for x in range(start_x, end_x, block):
            wall = Block(x, y, block, block)
            walls.add(wall)
            sprites.add(wall)

    @staticmethod
    def add_column(x, start_y, end_y, block, walls, sprites):
        """ Draw a vertical column

         - x: int : x position
         - start_y: int : top position y
         - end_y: int : bottom position y
         - block: int : block size
         - walls: SpriteGroup : wall list
         - sprites: SpriteGroup : sprites list
        """

        for y in range(start_y, end_y, block):
            wall = Block(x, y, block, block)
            walls.add(wall)
            sprites.add(wall)

    @staticmethod
    def add_platform(x, y, x_speed, y_speed, platforms, walls, sprites):
        """ Draw a movable horizontal platform and add to all lists


         - x: int : x position
         - y: int : y position
         - x_speed: int : speed in x direction
         - y_speed: int : speed in y direction
         - platforms: SpriteGroup : platform list
         - walls: SpriteGroup : wall list
         - sprites: SpriteGroup : sprites list
         Returns: Platform : New platform instance with given parameters
        """

        platform = Platform(x, y, x_speed, y_speed, BLOCK, WIDTH - BLOCK, 0, HEIGHT - BLOCK)
        platforms.add(platform)
        platform.walls = walls
        sprites.add(platform)
        return platform

    @staticmethod
    def add_door(x, y, block, doors, sprites, exit_level, left=False):
        """ Draw the door object on right side of screen by default, left by input

         - x: int : x position
         - y: int : y position
         - block: int : block size
         - doors: SpriteGroup : door list
         - sprites: SpriteGroup : sprites list
         - left: bool : Default False, enter True to place on left side
        """

        if left:
            door = DoorLeft(x, y, block, block + 50, exit_level)
            doors.add(door)
            sprites.add(door)
        else:
            door = Door(x, y, block, block + 50, exit_level)
            doors.add(door)
            sprites.add(door)

    @staticmethod
    def add_enemy(obj, x, y, speed, walls, players, enemies, sprites):
        """ Adds a specific enemy type to the level

         - obj: Enemy : Enemy class name
         - x: int : start x
         - y: int : start y
         - speed: int : change x speed
         - walls: SpriteGroup : wall list
         - players: SpriteGroup : player list
         - enemies: SpriteGroup : enemy list
         - sprites: SpriteGroup : all sprite list
        Returns: Enemy : new Enemy instance with given parameters
        """

        enemy = obj(x, y)
        enemy.change_x = speed
        enemy.walls = walls
        enemy.player = players
        enemies.add(enemy)
        sprites.add(enemy)
        return enemy

    @staticmethod
    def add_power_up(obj, x, y, power_list, sprites):
        """ Adds a power up object to the sprites list

         - obj: PowerUp : power up object to add
         - x: int : x position
         - y: int : y position
         - power_list: SpriteGroup : power up list
         - sprites: SpriteGroup : sprites list
        """

        power = obj(x, y)
        power_list.add(power)
        sprites.add(power)


# ========================
# ------- Run game -------

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('The Depths Of Madness      -- {}--'.format(VERSION))
    Game().main()
