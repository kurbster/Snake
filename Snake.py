# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 16:02:56 2020

@author: karby
"""

import pygame as pg
import sys
import random

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
dark_green = (0,100,0)
red = (255,0,0)

# Initialize the pygame object then set the screen
width = 800
height = 600
box_size = 20
rows = height // box_size
columns = width // box_size
screen = pg.display.set_mode((width, height))

# Adding the title and icons
pg.init()
pg.display.set_caption('Snake Game')
icon = pg.image.load('002-cobra.png')
pg.display.set_icon(icon)
clock = pg.time.Clock()

# Font objects 
font = pg.font.SysFont('ariel', 20)

# This is the draw function that will get called every frame of the game
def draw_grid():
    screen.fill(black)
    # First I draw the grid
    for r in range(rows):
        pg.draw.line(screen, white, (0, r * box_size), (width, r * box_size))
    for c in range(columns):
        pg.draw.line(screen, white, (c * box_size, 0), (c * box_size, height))
    # Then the snake
    draw_snake()
    # Then the food
    draw_food()
    pg.display.update()


def draw_snake():
    # Here I use enumerate so I can tell when I'm at the head to color it 
    # A different color
    for i, s in enumerate(snake):
        if i == 0:
            pg.draw.rect(screen, dark_green, (s[0] * box_size, s[1] * box_size, box_size, box_size))
        else:
            pg.draw.rect(screen, green, (s[0] * box_size, s[1] * box_size, box_size, box_size))


def draw_food():
    pg.draw.rect(screen, red, (food[0] * box_size, food[1] * box_size, box_size, box_size))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    
# This method is here so after the player enters the end game state they 
# Can choose to replay the game therefore this method will initialize
# The game and its default values before returning and letting the game
# Continue with the starting values
def init_game():
    # These are the global variables that we need later
    # The other variables just help us set up the game we don't need them later
    global snake, food, snake_x_change, snake_y_change
    # The starting position of the snake is in the middle of the board
    # And he starts w/ 3 sections
    snake_x = columns / 2
    snake_y = rows / 2
    snake_x_change = 0
    snake_y_change = 0
    snake = [
        [snake_x,     snake_y],
        [snake_x + 1, snake_y],
        [snake_x + 2, snake_y]
    ]
    # The food will start in the left corner of the screen
    food_x = 0
    food_y = 0
    food = [food_x, food_y]
   
  
def run_game():
    init_game()
    # I must pass in my global variables
    global snake, food, snake_x_change, snake_y_change
    # This is our game loop
    while True:
        # We delay each loop by 50 ms
        # Then the clock.tick method is like our FPS 
        # The higher it is the faster the snake because there are more actions per second
        pg.time.delay(50)
        clock.tick(10)
        draw_grid()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # I first check what the user wants to do and record the 
            # Specific changes always making sure I can't move diagonal
            # By having both x and y change
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    snake_x_change = -1
                    snake_y_change = 0
                if event.key == pg.K_RIGHT:
                    snake_x_change = 1
                    snake_y_change = 0
                if event.key == pg.K_UP:
                    snake_x_change = 0
                    snake_y_change = -1
                if event.key == pg.K_DOWN:
                    snake_x_change = 0
                    snake_y_change = 1
        # If both of these are 0 then that means we are at the start of the game
        # I do not want to start checking for food until the user has moved
        # Then for the rest of the game I know the snake will be moving
        if snake_x_change != 0 or snake_y_change != 0:  
            # I create a new_head object which is a list of the first element
            # In snake, then I make the change the user wanted. After that
            # I must check for collisions w/ the wall then w/ the food         
            new_head = [snake[0][0], snake[0][1]]     
            new_head[0] += snake_x_change
            new_head[1] += snake_y_change
            # After I get the new head I check for collision detection by checking
            # Whether my x or y value are outside of the valid range. If they
            # Are then I enter my end_game method which is a game state
            # That allows the user to quit or play again
            if new_head[0] in [-1, columns] or new_head[1] in [-1, rows] or new_head in snake[1:]:
                pg.quit()
                sys.exit()
                # Instead of quitting here I would put my endGame method
            # If the snake ran into new food then I find a new food
            # And keep the new head in the snake because we grew by one
            snake.insert(0, new_head)
            if snake[0] == food:
                food = None
                while food is None:
                    nf = [
                        random.randint(0, columns - 1),
                        random.randint(0, rows - 1)
                    ]
                    food = nf if nf not in snake else None
            # If we didn't touch food then I get rid of the tail
            else:
                snake.pop()
            
def end_game():
    while True:
        pass
    
click = False
# This is my main menu loop where I will add buttons so the
# User can choose to play the game or have an AI play it(Version 2)
def main_loop():
    global click, font
    while True:
        screen.fill(black)
        draw_text('main menu', font, white, screen, 20, 20)
        mx, my = pg.mouse.get_pos()
        
        draw_text('play game', font, white, screen, 50, 100)
        play_button = pg.Rect(50, 100, 200, 50)
        
        # ai_button = pg.Rect(50, 200, 200, 50)
        if play_button.collidepoint((mx, my)):
            if click:
                run_game()
        pg.draw.rect(screen, red, play_button)
        
        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pg.display.update()
        clock.tick(60)
        
main_loop()

    
    
    
    
    
    
    