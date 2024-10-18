import pygame
import time
import random

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Enhanced Snake Game")

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_blue = (0, 0, 139)
gray = (128, 128, 128)

# Snake settings
snake_block = 20
snake_speed = 15

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 35)
score_font = pygame.font.SysFont("comicsansms", 35)

# High score
try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except:
    highscore = 0

def display_score(score):
    """Display the current score and high score on the screen."""
    value = score_font.render("Score: " + str(score), True, yellow)
    screen.blit(value, [0, 0])

    high = score_font.render("High Score: " + str(highscore), True, yellow)
    screen.blit(high, [0, 40])

def draw_snake(snake_block, snake_list):
    """Draw the snake on the screen with a border effect."""
    for x in snake_list:
        pygame.draw.rect(screen, dark_blue, [x[0], x[1], snake_block, snake_block])
        pygame.draw.rect(screen, blue, [x[0]+4, x[1]+4, snake_block-8, snake_block-8])

def show_message(msg, color, y_displace=0):
    """Display a message on the screen."""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3 + y_displace])

def game_loop():
    """Main game loop."""
    global highscore
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block

    clock = pygame.time.Clock()

    while not game_over:

        while game_close:
            screen.fill(dark_blue)
            show_message("You Lost! Press C-Play Again or Q-Quit", red, -50)
            display_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(gray)

        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        display_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            if Length_of_snake - 1 > highscore:
                highscore = Length_of_snake - 1
                with open("highscore.txt", "w") as f:
                    f.write(str(highscore))

        clock.tick(snake_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    # Start screen
    screen.fill(blue)
    title_font = pygame.font.SysFont("bahnschrift", 50)
    title = title_font.render("Welcome to the Enhanced Snake Game!", True, white)
    screen.blit(title, [screen_width / 6, screen_height / 3])
    pygame.display.update()
    time.sleep(2)
    game_loop()
