import pygame
import random
import math
from pygame import mixer
pygame.init()

# game window
X = 1000
Y = 600
screen = pygame.display.set_mode((X, Y))
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 15
textY = 15

# Tile
pygame.display.set_caption("Space")
icon = pygame.image.load("ufo.png")
background = pygame.transform.scale(pygame.image.load("spaxe.jpg"), (X, Y))
pygame.display.set_icon(icon)
mixer.music.load("background.wav")
mixer.music.play(-1)


def show_score(score):
    score = font.render("Score : "+str(score), True, (255, 255, 255))
    screen.blit(score, (textX, textY))


# player
playerImg = pygame.image.load("spaceship.png")
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerX = X/2
playerY = 550
playerX_change = 0
score = 0


def player(playerX, playerY):
    screen.blit(playerImg, (playerX, playerY))


# enemy
enemyImg = pygame.transform.scale(
    pygame.image.load("ufo.png"), (40, 40))
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemy = 6
for i in range(no_of_enemy):
    enemyX.append(random.randint(50, X-100))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(0.05)


def enemy(enemyX, enemyY):
    screen.blit(enemyImg, (enemyX, enemyY))


# bullet
bulletImg = pygame.image.load("bullet.png")
# bulletImg = pygame.transform.scale(bulletImg, (50, 50))
bulletX = X/2
bulletY = 550
bullet_change = 1
bulletState = 0


def fire_bullet(bulletX, bulletY):
    screen.blit(bulletImg, (bulletX+10, bulletY+10))

# collsion


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))
    if distance < 30:
        return True
    else:
        return False

# game over


def gameOver():
    font = pygame.font.Font('freesansbold.ttf', 60)
    gameover = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(gameover, (X/2-220, Y/2-30))


# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE and bulletState == 0:
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                bulletState = 1
                bulletX = playerX
                bulletY = playerY
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    playerX += playerX_change
    if playerX > 950:
        playerX = 0
    if playerX < 0:
        playerX = 950

    for i in range(no_of_enemy):
        if enemyX[i] > 950 or enemyX[i] < 0:
            enemyX_change[i] = -enemyX_change[i]
        if enemyY[i] > 550:
            for j in range(no_of_enemy):
                enemyY[j] = 1000
            gameOver()
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
# collsion
        collison = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            enemyX[i] = random.randint(50, X-100)
            enemyY[i] = random.randint(50, 150)
            bulletX = X/2
            bulletY = 550
            bulletState = 0
            score += 1
            print(score)
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
        enemy(enemyX[i], enemyY[i])

    # fire_bullet(playerX, playerY)
    if bulletY <= 0:
        bulletState = 0

    if bulletState == 1:
        bulletY -= bullet_change
        fire_bullet(bulletX, bulletY)

    player(playerX, playerY)
    show_score(score)
    pygame.display.update()
