# -*- coding: utf-8 -*-
"""
The Depths Of Madness
 ver. 1.00.0

 - Tim Seymore  2018
"""

import pygame
import sys

from Scripts.colors import Color


# ===============
# ---CONSTANTS---

VERSION = "ver. 1.00.0"
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
BLOCK = 25
FPS = 60
GRAVITY = 47


# =====================
# --Data Definitions--


class Player(pygame.sprite.Sprite):
    """
     Player is a Player(Integer[0, WIDTH], Integer[0, HEIGHT])
     interp. p = Player(x, y) creates a playable character p where:
              - x is the x coordinate
              - y is the y coordinate
     p = Player(20, 10)  - create a Player p at x position 20 and y position 10

     def fn-for-player(p):
         ...
             p.rect.x    - Integer[0, WIDTH]
             p.rect.y    - Integer[0, HEIGHT]
             ...
     """
    # PLAYER STATES
    gender = "male"
    score = 0
    coins = 0
    lives = 0

    win = False
    dead = False
    clear = False

    jumping = False
    falling = False
    resting = False

    dy = 0
    change_x = 0
    change_y = 0

    # Object lists
    walls = None
    doors = None
    platforms = None
    enemies = None
    coins_list = None
    extra_lives = None

    def __init__(self, x, y):
        """
        Integer[0, WIDTH] Integer[0, HEIGHT] -> Player
        constructor for Player object
          - x: x location to spawn
          - y: y location to spawn
        p = Player(10, 20)  - create a Player p at x position 10 and y position 20
        """
        super().__init__()
        self.image = pygame.image.load("Graphics\male_right.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.origin_x = x
        self.origin_y = y

    def get_gender(self):
        """
        Player -> String
        return player gender outside of class definition
          - Prints error message to console if no gender is defined.
        Player.get_gender()  - returns gender as String
        """
        if self.gender == "male" or self.gender == "female":
            return self.gender
        else:
            print("AttributeError: Player gender not defined.")

    def get_score(self):
        """
         Player -> Integer
         return the Player score outside of class definition
         Player.get_score()  - returns score as Integer
        """
        return self.score

    def get_coins(self):
        """
        Player -> Integer
        return number of coins player is holding outside of class definition
        Player.get_coins()  - returns coins as Integer
        """
        return self.coins

    def get_lives(self):
        """
        Player -> Integer
        return number of lives player has left outside of class definition
        Player.get_lives()  - returns lives as Integer
        """
        return self.lives

    def get_state(self):
        """
        Player -> String
        return player state outside of class definition
          - "resting"
          - "jumping"
          - "falling"
          - prints error message to console if no state is active.
        Player.get_state()  - returns state as String
        """
        if self.resting:
            return "resting"
        elif self.jumping:
            return "jumping"
        elif self.falling:
            return "falling"
        else:
            return "AttributeError: Player state not defined."

    def show_hud(self, ds):
        """
        Player (Integer, Integer) -> Image
        display HUD on display screen (score, lives, coins)
          - ds: display screen
        Player.show_hud(SCREEN)  - displays HUD to game screen
        """
        self.show_score(ds, 650, 10, 20)
        self.show_lives(ds)
        self.show_coins(ds)

    def show_score(self, ds, x, y, s):
        """
        Player (Integer, Integer) Integer[0, WIDTH] Integer[0, HEIGHT] Integer -> Image
        display the player score on screen
           - ds: display screen
           - x: x axis
           - y: y axis
           - s: text size
        Player.show_score(SCREEN, 10, 20, 16)  - displays score at coord (10, 20) font size 16
        """
        font = pygame.font.SysFont("Times Roman", s)
        text = font.render("SCORE {}".format(self.score), False, Color.RedBrown, Color.Black)
        ds.blit(text, (x, y))

    # TODO - Continue maintenance from this point.
    def show_lives(self, disp):
        """
        Displays how many lives the player has left
        :param disp: display screen
        """
        icon_x = 40
        icon_y = 5
        icon = LifeIcon(icon_x, icon_y)
        for x in range(self.lives + 1):
            disp.blit(icon.image, (icon.x, icon.y))
            icon.x += 20

    def show_coins(self, disp):
        """
        Displays how many coins the player is holding
        :param disp: display screen
        """
        icon_x = 40
        icon_y = 20
        coin = CoinIcon(icon_x, icon_y)
        for x in range(self.coins):
            disp.blit(coin.image, (coin.x, coin.y))
            coin.x += 20

    def add_player_start(self, players, sprites):
        """
        Adds a player to level 1;
        To be added before enemy objects.
        :param players: player list
        :param sprites: all sprite list
        """
        self.add_player_next(players, sprites)
        self.lives = 1
        self.dead = False
        self.win = False

    def add_player_next(self, players, sprites):
        """
        Adds a player to a level greater than 1;
        To be added before enemy objects.
        :param players: player list
        :param sprites: all sprite list
        """
        players.add(self)
        sprites.add(self)
        self.reset()

    def switch_img(self, last, new):
        """ Switches player image based on direction of movement. """
        if last.right < new.right:
            self.image = pygame.image.load("Graphics\male_right.png")
        elif last.left > new.left:
            self.image = pygame.image.load("Graphics\male_left.png")

    def reset(self):
        """ Reset player to original location in level. """
        self.rect.x = self.origin_x
        self.rect.y = self.origin_y

    def change_spawn(self, x, y):
        """ Change spawn point of player. """
        self.origin_x = x
        self.origin_y = y

    def check_lives(self):
        """
        Checks number of lives and
        determines if player is dead.
        Resets player if 1 or more lives are present.
        """
        effect = pygame.mixer.Sound(r'Sounds\lose_life.wav')
        if self.lives == 0:
            self.dead = True
        else:
            effect.play()
            self.lives -= 1
            self.reset()

    def if_dead(self, img, disp, time, fps):
        """
        Checks for player death and runs Game Over loop if True.
        :param img: event box image
        :param disp: display screen
        :param time: game clock
        :param fps: frames per second
        """
        font = pygame.font.SysFont("Comic Sans MS", 30)
        text_surface = font.render("Press 'Enter' to continue", False, Color.RedBrown)
        background = r'Sounds\over_background.wav'
        pygame.mixer.music.load(background)
        pygame.mixer.music.play(-1)

        if self.dead:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.reset()
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.reset()
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            running = False
                disp.fill(Color.Blood)
                self.show_score(disp, 300, 25, 40)
                disp.blit(img.image, (200, 100))
                disp.blit(text_surface, (220, 500))
                pygame.display.flip()
                time.tick(fps)
            pygame.mixer.music.stop()

    def if_clear(self, img, disp, time, fps):
        """
        Checks for level completion and runs level clear loop if True.
        :param img: event box image
        :param disp: display screen
        :param time: game clock
        :param fps: frames per second
        """
        font = pygame.font.SysFont("Comic Sans MS", 30)
        font1 = pygame.font.SysFont("Times Roman", 50)
        text_surface = font.render("Press 'Enter' to play next level.", False, Color.DarkSlateBlue)
        text_surface1 = font1.render("Level Clear", False, Color.DarkSlateBlue)
        background = r'Sounds\win_background.wav'
        pygame.mixer.music.load(background)
        pygame.mixer.music.play(-1)
        while self.clear:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.reset()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.reset()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self.clear = False
            disp.fill(Color.DeepSkyBlue)
            self.show_score(disp, 300, 55, 35)
            disp.blit(img.image, (200, 100))
            disp.blit(text_surface1, (280, 5))
            disp.blit(text_surface, (180, 525))
            pygame.display.flip()
            time.tick(fps)
        pygame.mixer.music.stop()

    def if_win(self, img, disp, time, fps):
        """ Checks for game win and runs Win Game loop if True """
        font = pygame.font.SysFont("Comic Sans MS", 30)
        font1 = pygame.font.SysFont("Times Roman", 45)
        text_surface = font.render("Press 'Enter' to continue.", False, Color.DarkSlateBlue)
        text_surface1 = font1.render("Congratulations You Beat The Game!", False, Color.DarkSlateBlue)
        background = r'Sounds\win_background.wav'
        pygame.mixer.music.load(background)
        pygame.mixer.music.play(-1)

        if self.clear:
            self.win = True
        while self.win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.reset()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.reset()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self.win = False
            disp.fill(Color.DeepSkyBlue)
            self.show_score(disp, 300, 55, 35)
            disp.blit(img.image, (200, 100))
            disp.blit(text_surface1, (65, 5))
            disp.blit(text_surface, (225, 525))
            pygame.display.flip()
            time.tick(fps)
        pygame.mixer.music.stop()

    def update_lists(self, walls, enemies, lives, coins, doors, platforms):
        """" Updates lists before entering game loop """
        self.enemies = enemies
        self.walls = walls
        self.extra_lives = lives
        self.coins_list = coins
        self.doors = doors
        self.platforms = platforms
        self.win = False

    def control_player(self, dt, gravity):
        """ Player Controls """
        # Check for quick key presses
        for event in pygame.event.get():
            # Quit by closing window or Escape key
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        # Check key holding
        key = pygame.key.get_pressed()
        # Jump by Space bar
        effect = pygame.mixer.Sound(r'Sounds\jump.wav')
        if self.resting and key[pygame.K_SPACE]:
            effect.play()
            self.resting = False
            self.jumping = True
            self.dy = -600
        # Move Left/Right
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.change_speed(-300 * dt, 0)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.change_speed(300 * dt, 0)
        # Set y position
        self.dy = min(450, self.dy + gravity)
        self.change_speed(0, self.dy * dt)

    def change_speed(self, x, y):
        """ Change player speed. """
        self.rect.x += x
        self.rect.y += y

    def check_walls(self, last, new):
        """
        Check walls for collisions.
        :param last: Player position before movement
        :param new: Player position after movement
        """
        for cell in pygame.sprite.spritecollide(self, self.walls, False):
            # Side to side collision
            if last.right <= cell.rect.left < new.right:
                new.right = cell.rect.left
            if new.left < cell.rect.right <= last.left:
                new.left = cell.rect.right
            # Standing on top of block
            if last.bottom <= cell.rect.top < new.bottom:
                self.resting = True
                self.jumping = False
                self.falling = False
                new.bottom = cell.rect.top
                self.dy = 0
            # Hitting bottom from underneath
            if new.top < cell.rect.bottom <= last.top:
                new.top = cell.rect.bottom
                self.dy = 0
                self.falling = True

    def check_platforms(self, last, new):
        """
        Player Coord Coord -> Player
        Checks for player collisions with platforms and handles the collision
         - last: Player position before movement
         - new: Player position after movement
         Player.check_platforms(10, 20) >>> Checks for and handles platform collision at coord (20, 30)
        """
        platform_hits = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in platform_hits:
            # Side to side collision
            if last.right <= platform.rect.left < new.right:
                new.right = platform.rect.left
                self.resting = False
                self.falling = True
            if new.left < platform.rect.right <= last.left:
                new.left = platform.rect.right
                self.resting = False
                self.falling = True
            # TODO Standing on Platform ==BUG== not moving w/ plat at correct speed
            if last.bottom >= platform.rect.top < new.bottom:
                new.bottom = platform.rect.top
                self.change_speed(platform.change_x, platform.change_y)
                self.resting = True
                self.jumping = False
                self.falling = False
                self.dy = 0
            # Hitting bottom from underneath
            if new.top < platform.rect.bottom <= last.top:
                new.top = platform.rect.bottom
                self.dy = 0
                self.falling = True

    def check_doors(self):
        """ Check if player touches door. """
        # Check Doors
        door_hits = pygame.sprite.spritecollide(self, self.doors, False)
        for door in door_hits:
            self.clear = True
            self.score += 100
            self.score += self.lives * 10
            print(door.get_text())

    def map_collisions(self, last, new):
        """
        Check and handle all map collisions
        :param last: Player position before movement
        :param new: Player position after movement
        """
        self.check_walls(last, new)
        self.check_platforms(last, new)
        self.check_doors()

    # TODO Separate object detection from enemy detection
    def object_collisions(self, last, new):
        """
        Checks for object collisions.
        :param last: Player position before movement
        :param new: Player position after movement
        """
        # Check Enemies
        enemy_hits = pygame.sprite.spritecollide(self, self.enemies, False)
        for enemy in enemy_hits:
            enemy = enemy.rect
            if last.right <= enemy.left < new.right:
                new.right = enemy.left
                self.check_lives()
            elif new.left < enemy.right <= last.left:
                new.left = enemy.right
                self.check_lives()
            else:
                self.check_lives()
        # Check Power Ups
        extra_life_list = pygame.sprite.spritecollide(self, self.extra_lives, True)
        for life in extra_life_list:
            self.lives += 1
            self.score += 10
            effect = pygame.mixer.Sound(life.sound)
            effect.play()
        coin_hit_list = pygame.sprite.spritecollide(self, self.coins_list, True)
        for coin in coin_hit_list:
            self.coins += 1
            self.score += 20
            effect = pygame.mixer.Sound(coin.sound)
            effect.play()

    def update(self, dt, gravity):
        """
        Update the player position and state.
        :param dt: Delta time
        :param gravity: Gravity constant
        """
        last = self.rect.copy()
        self.control_player(dt, gravity)
        new = self.rect
        self.switch_img(last, new)
        self.map_collisions(last, new)
        self.object_collisions(last, new)


class Male(Player):
    """
     Male is a Player(Integer[0, WIDTH], Integer[0, HEIGHT])
     interp. m = Male(x, y) creates a playable male character where:
              - x is the x coordinate
              - y is the y coordinate
     m = Male(20, 10)  creates a male player at x position 20 and y position 10

     def fn-for-male(m):        Male
         ... m.x                Integer[0, WIDTH]
             m.y                Integer[0, HEIGHT]
     """


class Female(Player):
    """
     Female is a Player(Integer[0, WIDTH], Integer[0, HEIGHT])
     interp. f = Female(x, y) creates a playable female character where:
              - x is the x coordinate
              - y is the y coordinate
     f = Female(20, 10)  creates a female player at x position 20 and y position 10

     def fn-for-female(f):      Female
         ... f.x                Integer[0, WIDTH]
             f.y                Integer[0, HEIGHT]
     """
    def __init__(self, x, y):
        """
        Constructor method
        :param x: x location to spawn
        :param y: y location to spawn
        """
        super().__init__(x, y)
        self.image = pygame.image.load("Graphics\\female_right.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.gender = "female"

    def switch_img(self, last, new):
        """ Switches img based on direction of movement. """
        if last.right < new.right:
            self.image = pygame.image.load("Graphics\\female_right.png")
        elif last.left > new.left:
            self.image = pygame.image.load("Graphics\\female_left.png")


# Enemy Objects
class Enemy(pygame.sprite.Sprite):
    """ This class represents an enemy that the player
    battles. """
    def __init__(self, x, y):
        """
        Constructor method
        :param x: x location to spawn
        :param y: y location to spawn
        """
        super().__init__()

        # Class states
        self.walls = None
        self.platforms = None
        self.player = None

        self.change_x = 0
        self.change_y = 0

        self.origin_x = x
        self.origin_y = y

        self.image = pygame.image.load("Graphics\demon_right.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

    def switch_img(self):
        """ Switches img based on direction of movement """
        if self.change_x < 0:
            self.image = pygame.image.load("Graphics\demon_left.png")
        elif self.change_x > 0:
            self.image = pygame.image.load("Graphics\demon_right.png")

    def update(self, dt, gravity):
        """ Update the enemy position. """
        # Move left/right
        last = self.rect.copy()
        self.rect.x += self.change_x
        self.switch_img()
        new = self.rect

        for cell in pygame.sprite.spritecollide(self, self.walls, False):
            cell = cell.rect
            if last.right <= cell.left < new.right:
                new.right = cell.left
                self.change_x *= -1
            if new.left < cell.right <= last.left:
                new.left = cell.right
                self.change_x *= -1
            if last.bottom <= cell.top < new.bottom:
                new.bottom = cell.top
            if new.top < cell.bottom <= last.top:
                new.top = cell.bottom


class Demon(Enemy):
    """A Default Demon Enemy Class"""


class Insect(Enemy):
    """ An Insect Enemy Class """
    def __init__(self, x, y):
        """
        Constructor method
        :param x: x location to spawn
        :param y: y location to spawn
        """
        super().__init__(x, y)

        # Set Insect image
        self.image = pygame.image.load("Graphics\insect_right.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

    def switch_img(self):
        """ Switches img based on direction of movement """
        if self.change_x < 0:
            self.image = pygame.image.load("Graphics\insect_left.png")
        elif self.change_x > 0:
            self.image = pygame.image.load("Graphics\insect_right.png")


class Zombie(Enemy):
    """A Zombie Enemy Class"""
    def __init__(self, x, y):
        """
        Constructor method
        :param x: x location to spawn
        :param y: y location to spawn
        """
        super().__init__(x, y)

        # Set Zombie image
        self.image = pygame.image.load("Graphics\zombie_right.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

    def switch_img(self):
        """ Switches img based on direction of movement """
        if self.change_x < 0:
            self.image = pygame.image.load("Graphics\zombie_left.png")
        elif self.change_x > 0:
            self.image = pygame.image.load("Graphics\zombie_right.png")


class Spike(Enemy):
    """ A Spike Block Class """
    def __init__(self, x, y):
        """
        Constructor method
        :param x: x location to spawn
        :param y: y location to spawn
        """
        super().__init__(x, y)

        # Set Spike image
        self.image = pygame.image.load("Graphics\spikes.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())


# Environment Objects

class Wall(pygame.sprite.Sprite):
    """ A wall that the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor Method """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(Color.Mist)
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())


class Block(Wall):
    """ A stone block to build a wall."""
    def __init__(self, x, y, width, height):
        """ Constructor Method """
        super().__init__(x, y, width, height)

        self.image = pygame.image.load("Graphics\stone.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())


class Platform(pygame.sprite.Sprite):
    """Platform that floats or moves in the game."""
    def __init__(self, x, y):
        """ Constructor Method """
        super().__init__()

        self.image = pygame.image.load("Graphics\platform.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

        self.change_x = 0
        self.change_y = 0

        self.min_x = 25
        self.max_x = 775
        self.min_y = 25
        self.max_y = 575

        self.walls = None

    def change_bounds(self, min_x, max_x, min_y, max_y):
        """ Change the upper and lower bounds on x and y"""
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def change_speed(self, x, y):
        """ Change the speed of the platform. """
        self.change_x += x
        self.change_y += y

    def update(self, dt, gravity):
        """ Update the platform position. """
        # Move left/right
        if self.min_x <= self.rect.x <= self.max_x:
            self.rect.x += self.change_x
        else:
            self.change_x *= -1

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of block
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x *= -1
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                self.change_x *= -1

        # Move up/down
        if self.min_y < self.rect.y < self.max_y:
            self.rect.y += self.change_y
        else:
            self.change_y *= -1
            self.rect.y += self.change_y

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving down, set our bottom side to the top side of block
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_y *= -1
            else:
                # Otherwise if we are moving up, do the opposite.
                self.rect.top = block.rect.bottom
                self.change_y *= -1


class Door(pygame.sprite.Sprite):
    """ The door that clears the current level."""
    text = "A door that exits the level."

    def __init__(self, x, y, width, height):
        """ Constructor Method """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(Color.DarkBrown)
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        pygame.draw.circle(self.image, Color.Black, (5, 40), 3, 1)

    def get_text(self):
        """ Prints description """
        return self.text


class DoorLeft(Door):
    """ A door that appears on the left side of screen. """
    def __init__(self, x, y, width, height):
        """ Constructor Method """
        super().__init__(x, y, width, height)
        self.image = pygame.Surface([width, height])
        self.image.fill(Color.Brown)
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        pygame.draw.circle(self.image, Color.Black, (width - 5, 40), 5, 2)


# Event Boxes
class EventBox(object):
    """ A pop up box with text describing events. """
    def __init__(self, x, y):
        """ Constructor Method """
        self.x = x
        self.y = y
        self.image = None
        self.music = None


class GameOver(EventBox):
    """ Event box for end of game by death. """
    def __init__(self, x, y):
        """ Constructor Method """
        super().__init__(x, y)

        self.image = pygame.image.load('Graphics\game_over.png')
        self.music = r'Sounds\over_background.wav'


class WinGame(EventBox):
    """ Event box for clearing the level / win game. """
    def __init__(self, x, y):
        """ Constructor Method """
        super().__init__(x, y)

        self.image = pygame.image.load('Graphics\win_game.png')
        self.music = r'Sounds\win_background.wav'


class TitleScreen(EventBox):
    """ Event box for the title screen. """
    def __init__(self, x, y):
        """ Constructor Method """
        super().__init__(x, y)

        self.image = pygame.image.load('Graphics\menu.png')
        self.music = r'Sounds\menu_background.wav'


# Game Icons
class MousePointer(object):
    """ The Mouse Pointer Object """
    def __init__(self):
        self.image = pygame.image.load("Graphics\mouse_cursor.png")
        self.rect = self.image.get_size()
        pygame.mouse.set_visible(False)

    @staticmethod
    def get_pos():
        """ Returns: Tuple (x, y) position of mouse """
        return pygame.mouse.get_pos()

    @staticmethod
    def get_pressed():
        """
        Returns the state of the mouse buttons
        (button1, button2, button3) Boolean values
        """
        return pygame.mouse.get_pressed

    @staticmethod
    def get_focused():
        """ Returns Boolean; True if mouse is active """
        return pygame.mouse.get_focused()


class LifeIcon(object):
    """
    An icon representing the 'player life' object
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("Graphics\life_icon.png")
        self.text = "An icon representing the player's lives."

    def get_text(self):
        """ Prints description """
        return self.text


class CoinIcon(object):
    """
    An icon representing the 'coins' object
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("Graphics\coin_icon.png")
        self.text = "An icon representing the player's coins."

    def get_text(self):
        """ Prints description """
        return self.text


# Power Ups
class PowerUp(pygame.sprite.Sprite):
    """ Game object with positive effect on character """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Graphics\power_up.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.text = "A powerful upgrade."
        self.sound = r'Sounds\power_up.wav'

    def get_x(self):
        """ Returns current x position."""
        return self.rect.x

    def get_y(self):
        """ Returns current y position. """
        return self.rect.y

    def get_text(self):
        """ Prints description """
        return self.text


class Coin(PowerUp):
    """ Coin Power Up Object """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("Graphics\coin.png")
        self.text = "Used for extra exp points."


class ExtraLife(PowerUp):
    """ Extra Life Object """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("Graphics\life.png")
        self.text = "Gives player one extra life."


# ====================
# -----Functions------

def main(screen):
    """
    (Integer, Integer) -> Image
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
    background = r'Sounds\menu_background.wav'
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
    img_1 = pygame.image.load("Graphics\male_right.png")
    img_2 = pygame.image.load("Graphics\\female_left.png")
    menu_border = pygame.Surface([600, 400])
    menu_border.fill(Color.Eigengrau)
    menu_box = pygame.Surface([550, 350])
    menu_box.fill(Color.Blood)
    font = pygame.font.SysFont("Comic Sans MS", 60)
    font_1 = pygame.font.SysFont("Comic Sans MS", 15)
    text_surface = font.render("Choose your character", False, Color.RedBrown)
    text_surface_1 = font_1.render("1. Male", False, Color.RedBrown)
    text_surface_2 = font_1.render("2. Female", False, Color.RedBrown)
    background = r'Sounds\level_background2.wav'
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
    background = r'Sounds\level_background1.wav'
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
    background = r'Sounds\level_background2.wav'
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
    background = r'Sounds\level_background3.wav'
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
            img = pygame.image.load("Graphics\stone.png")
            disp.blit(img, (x, y))


def stone_background(disp):
    """ Display dark stone background image"""
    img = pygame.image.load("Graphics\stone_background.png")
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
