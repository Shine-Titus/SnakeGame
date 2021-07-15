import pygame
import sys
from random import randint
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.reverse_direction = Vector2(-1,0)
    
    def draw_snake(self):
        for block in self.body:
            x_pos = block.x*cell_size
            y_pos = block.y*cell_size
            snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183,111,122), snake_rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        tail = self.body[-1]
        curr_direction = self.direction
        new_tail = curr_direction - tail
        self.body.append(new_tail)

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)

class FRUIT:
    def __init__(self):
        self.snake = SNAKE()
        self.randomize()
        
    # draw the fruit
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size , self.pos.y*cell_size , cell_size, cell_size)
        pygame.draw.rect(screen, (126,166,114), fruit_rect)

    def draw_poison_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size , self.pos.y*cell_size , cell_size, cell_size)
        pygame.draw.rect(screen, (126,45,114), fruit_rect)

    def randomize(self):
        self.x = randint(0, cell_number-1)
        self.y = randint(0, cell_number-1)
        self.pos = Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.snake.draw_snake()
        self.draw_score()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                self.game_over()
        

    def game_over(self):
        self.snake.reset()

    def draw_score(self):
        score = str(len(self.snake.body) - 3)
        display_score = game_font.render(score, True, (56,74,12))
        score_x = int(cell_size)
        score_y =  int(cell_size)
        score_rect = display_score.get_rect(center = (score_x, score_y))
        screen.blit(display_score, score_rect)

pygame.init()
cell_size = 30
cell_number = 15
screen = pygame.display.set_mode((cell_size*cell_number, cell_size*cell_number))
pygame.display.set_caption('Snake!')
clock = pygame.time.Clock()

main = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1,0)
            if event.key == pygame.K_UP:
                if main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_LEFT:
                if main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1,0)

    screen.fill((175,215,70))
    main.draw_elements()
    pygame.display.update()
    clock.tick(60)

