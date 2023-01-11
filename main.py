import pygame
from pygame.locals import *
import random
import sys


RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 120)

#Functions
def event_loop():
    global again, in_action, in_action_bis, nu_head_position, program

    for event in pygame.event.get():
        if event.type == QUIT:
            program = False
            again = False

        elif event.type == KEYDOWN:
            if event.key == K_UP and in_action != "K_DOWN":
                in_action = "K_UP"
                in_action_bis = True
                nu_head_position[1] -= 20

            elif event.key == K_DOWN and in_action != "K_UP":
                in_action = "K_DOWN"
                in_action_bis = True
                nu_head_position[1] += 20

            elif event.key == K_RIGHT and in_action != "K_LEFT":
                in_action = "K_RIGHT"
                in_action_bis = True
                nu_head_position[0] += 20

            elif event.key == K_LEFT and in_action != "K_RIGHT":
                in_action = "K_LEFT"
                in_action_bis = True
                nu_head_position[0] -= 20

    if in_action_bis == False:
        if in_action == "K_UP":
            nu_head_position[1] -= 20
        elif in_action == "K_DOWN":
            nu_head_position[1] += 20
        elif in_action == "K_RIGHT":
            nu_head_position[0] += 20
        elif in_action == "K_LEFT":
            nu_head_position[0] -= 20

    in_action_bis = False


def update():
    global food_position, old_food_position, score, snake_positions

    # when the snake moves normally
    if nu_head_position != food_position:
        snake_positions.pop(-1)
        #score += 1

        snake_positions.insert(0, list(nu_head_position))

    # When the snake eats
    elif nu_head_position == food_position:
        snake_positions.insert(0, food_position)
        score += 5

        old_food_position = food_position
        # Food location
        while True:
            food_position = [random.randrange(0, 500, 20), random.randrange(100, 500, 20)]
            if food_position not in snake_positions:
                break

    # If the Snake quits the screen
    if snake_positions[0][0] < 0 or snake_positions[0][0] > 480 or snake_positions[0][1] < 100 or snake_positions[0][
        1] > 480 or snake_positions[0] in snake_positions[1:]:
        game_over()


def draw():
    global food, score_surface, snake_positions

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (GREEN), Rect(0, 0, 500, 100), 1)
    score_surface = font.render("SCORE: " + str(score), True, (YELLOW))
    screen.blit(score_surface, (0, 0))

    # If the Snake eats
    if nu_head_position == old_food_position:
        pygame.draw.rect(screen, (GREEN), Rect(0, 100, 500, 400), 1)

        for index, item in enumerate(snake_positions):
            if index == 0:
                pygame.draw.rect(screen, (YELLOW), Rect(item[0], item[1], 20, 20))
            else:
                pygame.draw.rect(screen, (GREEN), Rect(item[0], item[1], 20, 20))

    else:
        pygame.draw.rect(screen, (GREEN), Rect(0, 100, 500, 400), 1)

        for index, item in enumerate(snake_positions):
            if index == 0:
                pygame.draw.rect(screen, (YELLOW), Rect(item[0], item[1], 20, 20), 2)
            else:
                pygame.draw.rect(screen, (GREEN), Rect(item[0], item[1], 20, 20), 2)

    # Drawing Food
    food = pygame.draw.rect(screen, (RED), Rect(food_position[0], food_position[1], 20, 20), 2)


def game_over():
    global again, in_action, nu_head_position, program

    screen.blit(game_over_surface, game_over_surface_rect)

    screen.blit(rejouer_surface, rejouer_surface_rect)

    pygame.display.flip()

    user_choice = False
    while not user_choice:
        for event in pygame.event.get():
            if event.type == QUIT:
                user_choice = True
                program = False
                again = False
                sys.exit(0)

            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and (100 <= event.pos[0] <= 300) and (
                    280 <= event.pos[1] <= 305)) or ():
                user_choice = True
                program = False


def main_loop():
    while program:
        event_loop()
        update()
        draw()
        pygame.display.flip()
        timer.tick(10)


again = True
while again:
    # Pygame initialization
    pygame.init()
    # Screen Creation
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Hiba's Snake Game")

    score_zone = pygame.draw.rect(screen, (GREEN), Rect(0, 0, 500, 100), 1)
    score = 0
    # Font
    font = pygame.font.Font("./kongtext.ttf", 32)

    # Score Screen
    score_surface = font.render("Score" + str(score), True, (YELLOW))
    screen.blit(score_surface, (0, 0))

    snake_food_zone = pygame.draw.rect(screen, (GREEN), Rect(0, 100, 500, 400), 1)

    # Snake Position
    snake = pygame.draw.rect(screen, (YELLOW), Rect(0, 240, 20, 20), 2)
    snake_positions = [[0, 240]]

    # Food Position
    food = pygame.draw.rect(screen, (RED), Rect(240, 240, 20, 20), 2)
    food_position = [240, 240]

    # Game Over
    game_over_surface = font.render("GAME OVER!", True, (RED))
    game_over_surface_rect = game_over_surface.get_rect(midtop=(240, 240))

    # Play Again
    rejouer_surface = font.render("PLAY AGAIN", True, (YELLOW))

    rejouer_surface_rect = rejouer_surface.get_rect(midtop=(240, 280))

    fps = 10

    timer = pygame.time.Clock()

    pygame.display.flip()

    in_action = "K_UP"
    in_action_bis = bool()
    nu_head_position = [240, 500]
    old_food_position = []
    program = True

    main_loop()

pygame.quit()