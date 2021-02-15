# Playing around with sprites in pygame

import pygame
import os.path
# from pygame.locals import *


# DEFINE CONSTANTS AT THIS LEVEL ---------------------------------------------------------------------------------------

# Other way to just CONSTRUCT a rectangle, but not blit it
SCREENRECT = pygame.Rect(0, 0, 800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ----------------------------------------------------------------------------------------------------------------------

pygame.init()

# By using the os.path(os.path.abspath(__file__)) we retrieve a list containing
# the absolute directory of the file and the name of the file
main_dir = os.path.split(os.path.abspath(__file__))[0]
print(main_dir)

# HOW TO LOAD IN MULTIPLE IMAGES AT ONCE -------------------------------------------------------------------------------
def get_file(file):
    # This command will load the images from where they are by getting the main_dir,
    # the folder in which it is stored, and the name of the file
    file = os.path.join(main_dir, "graphics", file)
    try:
        surface = pygame.image.load(file)

    except pygame.error:
        raise SystemExit("The file %s could not be loaded: %s" % (file, pygame.get_error()))
    # Basically changes the surface to the window's pixel format
    return surface.convert()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(get_file(file))
    return imgs
# ----------------------------------------------------------------------------------------------------------------------


# EXAMPLE OF A SPRITE BEING USED ---------------------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = get_file("ball1.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300

    def move(self, speed, direction):
        self.rect.move_ip(speed * direction, 0)
        # self.rect = self.rect.clamp(SCREENRECT)


# MAIN FUNCTION IN OUR GAME... -----------------------------------------------------------------------------------------
def main(winstyle=0):

    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    all = pygame.sprite.RenderUpdates()  # Dirty sprites keep track of the changes made to them

    # The Player class container will only be the dirty sprite... (So we can update its pos)
    Player.containers = all

    movement = 0

    player = Player()

    isRunning = True

    while isRunning:

        clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    movement = 1

                elif event.key == pygame.K_LEFT:
                    movement = -1

            elif event.type == pygame.KEYUP:
                movement = 0

        background = pygame.Surface(SCREENRECT.size)
        # CLEAR ALL DIRTY SPRITES FROM PREVIOUS FRAMES...
        all.clear(screen, background)

        # UPDATE THE POSITION OF ALL DIRTY SPRITES
        all.update()

        # LOGIC --------------------------------------------------------------------------------------------------------
        if movement != 0:
            player.move(7, movement)

        # --------------------------------------------------------------------------------------------------------------

        screen.fill(BLACK)

        # DRAW ALL DIRTY SPRITES ONTO THE SCREEN
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        # --------------------------------------------------------------------------------------------------------------

        clock.tick(60)

# ----------------------------------------------------------------------------------------------------------------------
main()