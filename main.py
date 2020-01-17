import pygame
import random
import math
from pygame import mixer
import os
import sys

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load(resource_path('resources/bg.jpg'))

# Sounds
background_music = mixer.music.load(resource_path('resources/song.mp3'))
mixer.music.play(-1)

laser_sound = mixer.Sound(resource_path('resources/laser7.wav'))
collision_sound = mixer.Sound(resource_path('resources/Explosion1.wav'))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(resource_path('resources/rocket.png'))
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font(resource_path('resources/freesansbold.ttf'), 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render('Score:' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Player
player_img = pygame.image.load(resource_path('resources/rocket.png'))
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
player_speed = 2


def player(x, y):
    screen.blit(player_img, (x, y))  # blit to draw on screen


# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyX_speed = []
enemyY_speed = []
num_of_enemies = 6
enemy_acceleration = 0.0002

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load(resource_path('resources/pacman.png')))
    enemyX.append(random.randint(32, 735))
    enemyY.append(random.randint(32, 100))
    enemyX_change.append(0.8)
    enemyY_change.append(20)
    enemyX_speed.append(0.8)
    enemyY_speed.append(0.1)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# Bullet
bullet_img = pygame.image.load(resource_path('resources/bullet.png'))
bulletX = 0
bulletY = 480
bulletX_change = 0.8
bulletY_change = 5
bulletX_speed = 0.8
bulletY_speed = 0.1
bullet_state = 'ready'  # ready - not visible, fire - on screen


def bullet(x, y):
    screen.blit(bullet_img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    bullet(x, y - 20)


def is_collision(ax, ay, bx, by):
    distance = math.sqrt(math.pow(ax - bx, 2) + math.pow(ay - by, 2))
    if distance <= 16:
        return True
    return False


# game over
game_over_font = pygame.font.Font(resource_path('resources/freesansbold.ttf'), 80)
is_game_over = False


def game_over():
    game_over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over_text, (200, 200))

# game loop
running = True
# clock = pygame.time.Clock()
while running:
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_speed
            if event.key == pygame.K_RIGHT:
                playerX_change = player_speed
            if event.key == pygame.K_DOWN:
                playerY_change = player_speed
            if event.key == pygame.K_UP:
                playerY_change = -player_speed
            if event.key == pygame.K_SPACE and bullet_state is 'ready':
                laser_sound.play(fade_ms=2)
                bulletX = playerX
                bulletY = playerY
                fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_RETURN:
                is_game_over = False
                for j in range(num_of_enemies):
                    enemyY_speed[j] = 0.1
                    enemyX_speed[j] = 0.8
                    enemyY[j] = 100
                    score_value = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerY_change = 0

    # update player position
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 32:
        playerX = 32
    elif playerX >= 736:
        playerX = 736
    if playerY <= 32:
        playerY = 32
    elif playerY >= 536:
        playerY = 536

    # enemy position
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 32:
            enemyX_change[i] = enemyX_speed[i]
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemyX_speed[i]
            enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 32:
            enemyY[i] = 32
        elif enemyY[i] >= 536 and enemyY[j]<2000:
            enemyY[i] = 536

        player_hit = is_collision(playerX, playerY, enemyX[i], enemyY[i])
        if player_hit:
            collision_sound.play()
            for j in range(num_of_enemies):
                enemyY[j] = 2500
            is_game_over = True
            break
        bullet_hit = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if bullet_hit:
            collision_sound.play(fade_ms=2)
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(32, 735)
            enemyY[i] = random.randint(32, 400)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = playerY
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    for j in range(num_of_enemies):
        enemyY_speed[j] = enemyY_speed[j] + enemy_acceleration
        enemyX_speed[j] = enemyX_speed[j] + enemy_acceleration

    if is_game_over:
        game_over()
    pygame.display.update()
