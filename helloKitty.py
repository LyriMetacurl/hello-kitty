import pygame, sys, time, random
from pygame.locals import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Hello Kitty')

# set up the colors
BLACK = (0, 0, 0)

# set up the block data structure
player = pygame.Rect(300, 100, 115, 95)
playerImage = pygame.image.load('cat.png')
playerStretchedImage = pygame.transform.scale(playerImage, (115, 95))
foodImage = pygame.image.load('mouse.png')
foods = []
for i in range(33):
    foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - 33), random.randint(0, WINDOWHEIGHT - 33), 33, 33))

foodCounter = 0
NEWFOOD = 40

# set up keyboard variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6

# set up music
pickUpSound = pygame.mixer.Sound('MOUSE_5.wav')
pickUpSound2 = pygame.mixer.Sound('MOUSE_7.wav')
pygame.mixer.music.load('nut5chin.mid')
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == ord('w'):
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == ord('s'):
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == K_UP or event.key == ord('w'):
                moveUp = False
            if event.key == K_DOWN or event.key == ord('s'):
                moveDown = False
            if event.key == ord('x'):
                player.top = random.randint(0, WINDOWHEIGHT - player.height)
                player.left = random.randint(0, WINDOWWIDTH - player.width)
            if event.key == ord('m'):
                if musicPlaying:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0)
                musicPlaying = not musicPlaying

        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0] - 17, event.pos[1] - 17, 33, 33))

    foodCounter += 1
    if foodCounter >= NEWFOOD:
        # add new food
        foodCounter = 0
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - 33), random.randint(0, WINDOWHEIGHT - 33), 33, 33))

    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    # move the player
    if moveDown and player.bottom < WINDOWHEIGHT:
        player.top += MOVESPEED
    if moveUp and player.top > 0:
        player.top -= MOVESPEED
    if moveLeft and player.left > 0:
        player.left -= MOVESPEED
    if moveRight and player.right < WINDOWWIDTH:
        player.right += MOVESPEED


    # draw the block onto the surface
    windowSurface.blit(playerStretchedImage, player)

    # check if the block has intersected with any food squares.
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
            playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
            if musicPlaying:
                pickUpSound.play()
                time.sleep(0.25)
                pickUpSound2.play()

    # draw the food
    for food in foods:
        windowSurface.blit(foodImage, food)

    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(40)
