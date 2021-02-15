# PONG PROGRAMMED IN PYTHON

import pygame
import os.path
import random
import time


# OPEN FILES AND LOAD IMAGES


def get_file(file):

    file = os.path.join(main_dir, "graphics", file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit("The file %s could not be loaded: %s" % (file, pygame.get_error()))
    return surface

# ----------------------------------------------------------------------------------------------------------------------

# CONSTANTS ------------------------------------------------------------------------------------------------------------

SCREEN_W = 800
SCREEN_H = 600
SCREENRECT = pygame.Rect(0, 0, SCREEN_W, SCREEN_H)
SPEED = 3
TRACK = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

music_playing = True

# ----------------------------------------------------------------------------------------------------------------------

main_dir = os.path.split(os.path.abspath(__file__))[0]

pygame.init()

# CREATE THE WINDOW
winstyle = 0  # FULLSCREEN
bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

pygame.display.set_caption("PONG")
icon = pygame.transform.scale(get_file("ball1.png"), (32, 32))
pygame.display.set_icon(icon)
# ------------------------------------

clock = pygame.time.Clock()

# ----------------------------------------------------------------------------------------------------------------------

# PLAYER CLASS ---------------------------------------------------------------------------------------------------------


class Player(pygame.sprite.Sprite):

    width = 15
    height = 70

    containers = []

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.score = 0

    def move(self, movement, speed):

        self.rect.move_ip(0, speed * movement)

        if self.rect.y < 0:
            self.rect.y = 0

        elif self.rect.y > SCREEN_H - self.height:
            self.rect.y = SCREEN_H - self.height

        # self.rect.clamp_ip(SCREENRECT) -> THIS WOULD AUTOM. PREVENT THE RECTANGLE FROM EXITING THE SCREEN
# ----------------------------------------------------------------------------------------------------------------------

# BALL CLASS -----------------------------------------------------------------------------------------------------------


class Ball(pygame.sprite.Sprite):

    direction = random.choice((-1, 1))

    acceleration = 0.1

    ball_x = direction
    ball_y = direction

    containers = []

    def __init__(self, x, y, radius):

        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = get_file("ball1.png")
        self.image = pygame.transform.scale(self.image, (radius*2, radius*2))
        self.radius = radius
        self.x, self.y = x, y

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def move(self, ai_x, ai_y, player_x, player_y):

        if self.alive():

            if not 0 < self.rect.y < SCREEN_H - self.radius * 2:
                self.ball_y *= -1

            if ai_x < self.rect.x < ai_x + AI.width and ai_y <= self.rect.y + self.radius <= ai_y + AI.height:

                self.rect.x = ai_x + AI.width

                if self.ball_x >= 5 or self.ball_x <= -5:
                    self.ball_x *= -1
                    self.ball_y += random.choice((-1, 1)) * random.randint(1, 3)
                    pygame.mixer.Sound("music\\ball_bounce.wav").play()

                else:
                    self.ball_y *= random.choice((-1, 1))
                    self.ball_x = -1 * self.ball_x + (self.acceleration * -self.ball_x)
                    pygame.mixer.Sound("music\\ball_bounce.wav").play()

            elif player_x + Player.width > self.rect.x + self.radius * 2 > player_x and \
                                    player_y <= self.rect.y + self.radius <= player_y + Player.height:

                self.rect.x = player_x - self.radius * 2   # SET THE X POSITION TO THE BOUNDARY OF THE PADDLE
                # THIS WILL MAKE THE GAME SEEM SMOOTHER AND MORE ACCURATE

                if self.ball_x >= 5 or self.ball_x <= -5:
                    self.ball_x *= -1
                    self.ball_y += random.choice((-1, 1)) * random.randint(1, 3)
                    pygame.mixer.Sound("music\\ball_bounce.wav").play()

                else:
                    self.ball_y *= random.choice((-1, 1))
                    self.ball_x = -1 * self.ball_x + (self.acceleration * -self.ball_x)
                    pygame.mixer.Sound("music\\ball_bounce.wav").play()

            # SOLVE THE BOUNCING ON THE TOP AND BOTTOM ISSUE

            if self.rect.x < ai_x - 80:
                time.sleep(1)
                self.kill()
                return 1

            elif self.rect.x + (self.radius * 2) > player_x + Player.width + 60:
                time.sleep(1)
                self.kill()
                return 2

            self.rect.move_ip(self.ball_x * 2, self.ball_y * 2)

    def redraw(self, *groups):

        self.add(*groups)

        self.rect.x = self.x
        self.rect.y = self.y

# ----------------------------------------------------------------------------------------------------------------------

# AI CLASS -------------------------------------------------------------------------------------------------------------


class AI(Player):  # We don't need to inherit from pygame.sprite.Sprite again, because the Player
    # class already inherits from it

    def __init__(self, x, y):
        Player.__init__(self, x, y)

    def tracking(self, ball_sprite):

        if self.rect.y > ball_sprite.rect.y:
            self.rect.y += 3 * -1

        elif self.rect.y < ball_sprite.rect.y:
            self.rect.y += 3 * 1

        # IMPOSSIBLE TO CODE EFFECTIVE AI W/OUT CALCULUS ?
        # THIS SOLUTION IS PRETTY GOOD THOUGH!

        if self.rect.y < 0:
            self.rect.y = 0

        elif self.rect.y > SCREEN_H - self.height:
            self.rect.y = SCREEN_H - self.height

    def redraw(self):
        self.rect.x = 50
        self.rect.y = 262.5

# ----------------------------------------------------------------------------------------------------------------------

# SCORE CLASS ----------------------------------------------------------------------------------------------------------


class Score:

    def __init__(self):
        self.font = pygame.font.Font("C:\\Windows\\Fonts\\8_bit_party.ttf", 50)

    def score(self, score1, score2, surf, pos1, pos2):

        player1 = self.font.render(str(score1), True, WHITE)
        player2 = self.font.render(str(score2), True, WHITE)

        surf.blit(player1, (pos1[0], pos1[1]))
        surf.blit(player2, (pos2[0], pos2[1]))
# ----------------------------------------------------------------------------------------------------------------------

# BUTTON CLASS ---------------------------------------------------------------------------------------------------------


class Button(pygame.sprite.Sprite):

    button_width = 220
    button_height = 150

    containers = []
    trigger = True

    def __init__(self, file1, msg, x, y, window, width, height, file2=None, action1=None):

        pygame.sprite.Sprite.__init__(self, self.containers)

        self.x = x
        self.y = y

        self.image = get_file(file1)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x + self.button_width > mouse[0] > self.x and \
                                        self.y + self.button_height > mouse[1] > self.y:
            if file2 is not None:
                self.image = get_file(file2)
                self.image = pygame.transform.scale(self.image, (width, height))
                self.rect = self.image.get_rect()

                self.rect.x = self.x
                self.rect.y = self.y

            else:
                self.image = get_file(file1)
                self.image = pygame.transform.scale(self.image, (width, height))
                self.rect = self.image.get_rect()

                self.rect.x = self.x
                self.rect.y = self.y

            if click[0] == 1 and action1 is not None:
                    action1()

        font = pygame.font.Font("C:\\Windows\\Fonts\\8_bit_party.ttf", 20)
        textSurf = font.render(str(msg), True, WHITE)
        textSurf.set_colorkey(WHITE)
        text_rect = textSurf.get_rect()
        text_rect.center = (self.x + (self.button_width / 2), self.y + (self.button_height / 2) - 10)
        window.blit(textSurf, text_rect)

# ----------------------------------------------------------------------------------------------------------------------

# MENU -------------------------------------------------------------------------------------------------------------


def game_intro():
    intro = True

    global music_playing
    music_playing = True

    buttons = pygame.sprite.RenderUpdates()
    Button.containers = buttons

    pygame.mixer.music.load("music\\Menu_music.wav")
    pygame.mixer.music.play(-1)

    sound = get_file("sound_button.png")
    mute = get_file("mute_button.png")

    sound = pygame.transform.scale(sound, (50, 50))
    mute = pygame.transform.scale(mute, (50, 50))

    while intro:

        for event in pygame.event.get():

            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()

            # BUTTON FUNCTIONALITY FOR ON/ OFF -----------------------------
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 70 > event.pos[0] > 20 and 590 > event.pos[1] > 540:
                    if music_playing:
                        pygame.mixer.music.pause()
                        music_playing = False

                    else:
                        pygame.mixer.music.unpause()
                        music_playing = True
            # -------------------------------------------------------------

        background = get_file("MENU.png")
        background = pygame.transform.scale(background, (SCREEN_W, SCREEN_H))
        screen.blit(background, (0, 0))

        if music_playing:
            screen.blit(sound, (20, 540))

        else:
            screen.blit(mute, (20, 540))

        buttons.clear(screen, background)
        buttons.update()

        for sprite in buttons:  # Kill previous sprites in the group so that you can re-draw the sprite each time
            sprite.kill()

        Button("button1.png", "1 Player", 275, 300, screen, 220, 150, "button2.png", main)
        Button("button1.png", "Exit Game", 275, 450, screen, 220, 150, "button2.png", quit)

        dirty = buttons.draw(screen)
        pygame.display.update(dirty)

        pygame.display.flip()
        clock.tick(60)

# ----------------------------------------------------------------------------------------------------------------------


# MAIN GAME FUNCTION ---------------------------------------------------------------------------------------------------


def main():

    global TRACK
    global music_playing

    # CLOCK AND FPS COUNTER
    # FPS = clock.get_fps()
    type = pygame.font.Font("C:\\Windows\\Fonts\\8_bit_party.ttf", 55)
    # ------------------------------------

    # DEFAULTS
    movement = 0
    # ------------

    # SPRITE GROUPS AND DEFINITIONS

    all = pygame.sprite.RenderUpdates()
    balls = pygame.sprite.Group()

    Player.containers = all
    Ball.containers = all, balls
    Button.containers = all

    player = Player(750, 262.5)
    ai = AI(50, 262.5)
    ball = Ball(((SCREEN_W / 2) - 15), ((SCREEN_H / 2) - 15), 10)
    points = Score()

    ball.add(balls)

    # -----------------------------------

    # QUE IN SOME MUSIC !----------------

    if music_playing:

        pygame.mixer.music.load("music\\background_8_bit_music.wav")
        pygame.mixer.music.play(-1)

    # -----------------------------------

    is_running = True

    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT \
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                is_running = False

            # MOUSE PRESSES
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w \
                or event.key == pygame.K_UP:
                        movement = -1

                elif event.key == pygame.K_s \
                or event.key == pygame.K_DOWN:
                        movement = 1

            elif event.type == pygame.KEYUP:
                movement = 0

            # --------------------

        background = pygame.Surface(SCREENRECT.size)
        background.fill(BLACK)
        for t in range(0, SCREEN_H, 30):
            pygame.draw.line(background, WHITE, (400, t), (400, t+20), 3)

        # CLEAR OLD FRAMES
        all.clear(screen, background)
        balls.clear(screen, background)

        # UPDATE ALL SPRITES
        all.update()
        balls.update()

        # LOGIC --------------------------------------------------------------------------------------------------------

        if movement != 0:
            player.move(movement, SPEED)

        ai.tracking(ball)
        move = ball.move(ai.rect.x, ai.rect.y, player.rect.x, player.rect.y)

        # --------------------------------------------------------------------------------------------------------------

        # RENDER GRAPHICS ----------------------------------------------------------------------------------------------
        screen.blit(background, (0, 0))
        # text = type.render(str(int(FPS)), True, (123, 100, 12))
        # screen.blit(text, (10, 0))

        points.score(player.score, ai.score, screen, (500, 10), (300, 10))

        if move == 1:
            player.score += 1

            ai.redraw()
            ball.redraw(all, balls)

            ball.ball_x = -2
            ball.ball_y = random.choice((-1, 1))

        elif move == 2:
            ai.score += 1

            ai.redraw()
            ball.redraw(all, balls)

            ball.ball_x = 2
            ball.ball_y = random.choice((-1, 1)) * 2

        if player.score == 10 or ai.score == 10:

            for sprite in all:
                sprite.kill()

            screen.fill(BLACK)

            Button("button1.png", "Return to Menu", 120, 400, screen, 220, 150, "button2.png", game_intro)
            Button("button1.png", "Quit", 450, 400, screen, 220, 150, "button2.png", quit)

            if ai.score == 10:

                # THERE SEEMS TO BE NO WAY TO PLAY MUSIC INSIDE THE LOOP!

                txt1 = type.render("Bad Luck, Player...", True, WHITE)
                txt2 = type.render("GAME OVER", True, WHITE)
                screen.blit(txt1, (0.20 * SCREEN_W, 0.3 * SCREEN_H))
                screen.blit(txt2, (0.3 * SCREEN_W, 0.4 * SCREEN_H))

            elif player.score == 10:

                # THERE SEEMS TO BE NO WAY TO PLAY MUSIC INSIDE THE LOOP!

                txt1 = type.render("Congratulations, Player", True, WHITE)
                txt2 = type.render("YOU WIN", True, WHITE)
                screen.blit(txt1, (30, 0.35 * SCREEN_H))
                screen.blit(txt2, (300, 0.50 * SCREEN_H))

        # --------------------------------------------------------------------------------------------------------------

        # DRAW SCENE
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        # ----------------------

        pygame.display.flip()

        # CLOCK and FPS counter
        clock.tick(60)
        # FPS = clock.get_fps()
        # ----------------------
# ----------------------------------------------------------------------------------------------------------------------

    pygame.quit()
    quit()

if __name__ == "__main__":
    game_intro()
