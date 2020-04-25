import pygame
from pygame import mixer
import sys
import random

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

#Game rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

bg_color = (26, 64, 176)  # pygame.Color('grey12')
light_grey = (200,200,200)

ball_speed_x = 7
ball_speed_y = 7
opponent_speed = 7
player_speed = 0
score_value = 0
PLAYER_WIN = 1
AI_WIN = 0


def show_score():
    score = pygame.font.SysFont(None, 24)
    img = score.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(img, (20,20))
    #score = font.render(f"Score : {score_value}", True, (255, 255, 255))
    #screen.blit(score, (10, 10))
    #pygame.display.update()

def opponent_animation():
    if (opponent.top < ball.y):
        opponent.top += opponent_speed
    if (opponent.bottom > ball.y):
        opponent.bottom -= opponent_speed
    if (opponent.top <= 0):
        opponent.top = 0
    if (opponent.bottom >= screen_height):
        opponent.bottom = screen_height

def player_animation():
    player.y += player_speed
    if (player.top <= 0):
        player.top = 0
    if (player.bottom >= screen_height):
        player.bottom = screen_height

def ball_restart(who_won: int):
    global ball_speed_x, ball_speed_y, score_value
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))
    if (who_won == PLAYER_WIN):
        score_value += 10
        win_sound = mixer.Sound('./wav/cymbals.wav')
    else:
        score_value -= 10
        win_sound = mixer.Sound('./wav/buzzer.wav')
    win_sound.play()

def ball_animation():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= - 1
    if ball.left <= 0:
        ball_restart(PLAYER_WIN)
    if ball.right >= screen_width:
        ball_restart(AI_WIN)
    
    if (ball.colliderect(player) or ball.colliderect(opponent)):
        ball_speed_x *= - 1
        bounce_sound = mixer.Sound('./wav/boing.wav')
        bounce_sound.play()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 10
            if event.key == pygame.K_UP:
                player_speed -= 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 10
            if event.key == pygame.K_UP:
                player_speed += 10
                

    ball_animation()
    player_animation()
    opponent_animation()
 

    #Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    show_score()

    #Center line
    pygame.draw.aaline(screen, light_grey, (screen_width/2,0), (screen_width/2, screen_height))

    #Updating the window
    pygame.display.flip()
    clock.tick(60)  #Frames per second
    
