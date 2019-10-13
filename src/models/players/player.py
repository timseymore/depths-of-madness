import pygame
import sys

from src.ui.tools.colors import Color
from src.ui.tools.lifeicon import LifeIcon
from src.ui.tools.coinicon import CoinIcon


class Player(pygame.sprite.Sprite):
    """
     Player is  Player(Integer[0, WIDTH], Integer[0, HEIGHT])
     interp. a playable character p where:
              - x is the starting x position
              - y is the starting y position
     p = Player(20, 10)  - creates a Player p at x position 20 and y position 10

    Template:

     def fn_for_player(p):
        ... p.rect.x  # Integer[0, WIDTH]
        ... p.rect.y  # Integer[0, HEIGHT]
        ... p.(...)   # PlayerState
     """
    def __init__(self, x, y):
        """
        Integer[0, WIDTH] Integer[0, HEIGHT] -> Player
        constructor for Player object
          - x: x location to spawn
          - y: y location to spawn
        p = Player(10, 20)  - create a Player p at x position 10 and y position 20
        """
        super().__init__()
        self.image = pygame.image.load("src/graphics/male_right.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.origin_x = x
        self.origin_y = y
        self.gender = None
        self.score = 0
        self.lives = 0
        self.coins = 0
        self.win = False
        self.dead = False
        self.clear = False
        self.jumping = False
        self.resting = False
        self.falling = False
        self.dy = 0
        self.change_x = 0
        self.change_y = 0
        self.walls = []
        self.doors = []
        self.platforms = []
        self.enemies = []
        self.coins_list = []
        self.extra_lives = []

    # Getters
    def get_gender(self) -> str:
        """
        return player gender outside of class definition
          - Prints error message to console if no gender is defined.
        Player.get_gender()  - return gender as String
        """
        if self.gender == "male" or self.gender == "female":
            return self.gender
        else:
            print("AttributeError: Player gender not defined.")

    def get_score(self) -> int:
        """
         return the Player score outside of class definition
         Player.get_score()  - returns score as Integer
        """
        return self.score

    def get_coins(self) -> int:
        """
        return number of coins player is holding outside of class definition
        Player.get_coins()  - returns coins as Integer
        """
        return self.coins

    def get_lives(self) -> int:
        """
        return number of lives player has left outside of class definition
        Player.get_lives()  - returns lives as Integer
        """
        return self.lives

    def get_state(self) -> str:
        """
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
            self.image = pygame.image.load("src/graphics/male_right.png")
        elif last.left > new.left:
            self.image = pygame.image.load("src/graphics/male_left.png")

    def reset(self):
        """ Reset player to original location in level. """
        self.rect.x = self.origin_x
        self.rect.y = self.origin_y

    def change_spawn(self, x, y):
        """ Change spawn point of player. """
        self.origin_x = x
        self.origin_y = y

    # TODO refactor name to be more representative of what it does
    def check_lives(self):
        """
        Checks number of lives and
        determines if player is dead.
        Resets player if 1 or more lives are present.
        """
        effect = pygame.mixer.Sound(r'src/sounds/lose_life.wav')
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
        background = r'src\sounds\over_background.wav'
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
        background = r'src\sounds\win_background.wav'
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
        background = r'src\sounds\win_background.wav'
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

    def update(self, dt, gravity):
        """
        Update the player position and state.
        :param dt: Delta time
        :param gravity: Gravity constant
        """
        # update player position
        last = self.rect.copy()
        self.control_player(dt, gravity)
        new = self.rect
        self.switch_img(last, new)
        # handle collisions
        self.map_collisions(last, new)
        self.object_collisions(last, new)

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
        effect = pygame.mixer.Sound(r'src\sounds\jump.wav')
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

    def map_collisions(self, last, new):
        """
        Check and handle all map collisions
        :param last: Player position before movement
        :param new: Player position after movement
        """
        self.check_walls(last, new)
        self.check_platforms(last, new)
        self.check_doors()

    # TODO ===BUG=== climbing and getting stuck on walls while jumping and touching sides
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
            elif new.left < cell.rect.right <= last.left:
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

    # TODO  ==BUG== player not moving along with platform at correct speed
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

            if last.bottom >= platform.rect.top < new.bottom:
                new.bottom = platform.rect.top
                self.change_speed(platform.x_speed, platform.y_speed)
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


