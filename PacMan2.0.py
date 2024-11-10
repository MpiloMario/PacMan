import pygame
import math
import random
import time

pygame.init()

class PacMan():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.direction = 1
        self.angle = 1
        self.sign = 1
        self.speed = 2

    def updateAngle(self):
        self.angle += self.sign * 0.1

        if self.angle < 0:
            self.angle = 0
        elif self.angle > math.pi / 3:
            self.angle = math.pi / 3

        if self.angle >= math.pi / 3:
            self.sign = -1
        elif self.angle <= 0:
            self.sign = 1

    def can_move(self, maze):
        next_x, next_y = self.x, self.y
        if self.direction == 1: 
            next_x -= self.speed
        elif self.direction == 2: 
            next_y -= self.speed
        elif self.direction == 3:  
            next_x += self.speed
        elif self.direction == 4:  
            next_y += self.speed

        tile_x = int(next_x // 20)
        tile_y = int(next_y // 20)

        if 0 <= tile_x < len(maze[0]) and 0 <= tile_y < len(maze):
            return maze[tile_y][tile_x] != 'X'
        return False
        

    def drawMouth(self, num):
        if self.direction == 1:
            mouth = [(self.x, self.y), (self.x - 27.5*math.cos(self.angle), self.y + 27.5*math.sin(self.angle)), (self.x - 27.5*math.cos(self.angle), self.y - 27.5*math.sin(self.angle))]
            pygame.draw.polygon(screen, (0, 0, 0), mouth)    
        elif self.direction == 4:
            mouth = [(self.x, self.y), (self.x - 27.5*math.sin(self.angle), self.y + 27.5*math.cos(self.angle)), (self.x + 27.5*math.sin(self.angle), self.y + 27.5*math.cos(self.angle))]
            pygame.draw.polygon(screen, (0, 0, 0), mouth)
        elif self.direction == 3:
            mouth = [(self.x, self.y), (self.x + 27.5*math.cos(self.angle), self.y + 27.5*math.sin(self.angle)), (self.x + 27.5*math.cos(self.angle), self.y - 27.5*math.sin(self.angle))]
            pygame.draw.polygon(screen, (0, 0, 0), mouth)
        else:
            mouth = [(self.x, self.y), (self.x - 27.5*math.sin(self.angle), self.y - 27.5*math.cos(self.angle)), (self.x + 27.5*math.sin(self.angle), self.y - 27.5*math.cos(self.angle))]
            pygame.draw.polygon(screen, (0, 0, 0), mouth)
            
    def drawFace(self):
        pygame.draw.circle(screen, (255, 255, 55), (self.x, self.y), self.radius)
    
    def draw(self, maze):
        if self.can_move(maze):
            if self.direction == 1:
                self.x -= 2
            elif self.direction == 2:
                self.y -= 2
            elif self.direction == 3:
                self.x += 2
            else:
                self.y += 2

        self.updateAngle()

        if self.x <= 0 and self.direction == 1:
            self.x = 800
        if self.x >= 800 and self.direction == 3:
            self.x = 0
        if self.y <= 0 and self.direction == 2:
            self.y = 600
        if self.y >= 600 and self.direction == 4:
            self.y = 0

        self.drawFace()
        self.drawMouth(self.direction)
            

class Ghost():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice([1, 2, 3, 4])  # Random initial direction
        self.speed = 2
        self.mode = "scatter"
        self.scatter_target = (random.randint(0, 800), random.randint(0, 600))
        self.chase_target = None

    def switch_mode(self):
        if self.mode == "scatter":
            self.mode = "chase"
        else:
            self.mode = "scatter"

    def move(self, maze, pacman_position):
        old_x, old_y = self.x, self.y

        if self.mode == "chase":
            self.chase_target = pacman_position
            self.move_towards_target(self.chase_target)
        elif self.mode == "scatter":
            self.move_towards_target(self.scatter_target)

        if self.collides_with_wall(maze):
            self.x, self.y = old_x, old_y
            self.change_direction()  

    def move_towards_target(self, target):
        target_x, target_y = target

        if abs(self.x - target_x) > abs(self.y - target_y):
            if self.x > target_x:
                self.direction = 1 
            else:
                self.direction = 3  
        else:
            if self.y > target_y:
                self.direction = 2  
            else:
                self.direction = 4  

        if self.direction == 1:
            self.x -= self.speed
        elif self.direction == 2:
            self.y -= self.speed
        elif self.direction == 3:
            self.x += self.speed
        elif self.direction == 4:
            self.y += self.speed

    def collides_with_wall(self, maze):
        tile_x = int(self.x // 20)
        tile_y = int(self.y // 20)
        if 0 <= tile_x < len(maze[0]) and 0 <= tile_y < len(maze):
            return maze[tile_y][tile_x] == 'X'
        return True

    def change_direction(self):
        self.direction = random.choice([1, 2, 3, 4])

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)


def load_maze(text_file):     
    maze = []
    with open(text_file, 'r') as file:
        for line in file:
            maze.append(line.strip())
    return maze
    
def draw_maze(maze):
    for row_i, row in enumerate(maze):
        for col_i, tile in enumerate(row):
            x = col_i*20
            y = row_i *20
            if tile == 'X':  
                pygame.draw.rect(screen, 'blue', pygame.Rect(x, y, 20, 20))
            elif tile == '.':  
                pygame.draw.circle(screen, 'white', (x + 10, y + 10), 2)
            elif tile == '+':  
                pygame.draw.circle(screen, 'red', (x + 10, y + 10), 5)
            elif tile == '=': 
                pygame.draw.rect(screen, 'yellow', pygame.Rect(x, y, 20, 20))
                
    
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width,screen_height))

ghosts = [
        Ghost(100,100,(255,0,0)),
        Ghost(200,100,(0,255,0)),
        Ghost(300,100,(50,150,255)),
        Ghost(400,100,(255,165,0)),
        ]
pygame.mixer.init()
pygame.mixer.music.load("Pac.mp3")

pygame.mixer.music.play(-1)
 

pygame.display.set_caption("Pac-Man")

last_switch = time.time()
switch_interval = 7

player_x = 300
player_y = 300 


score = 0
running = True

player = PacMan(player_x, player_y)
maze = load_maze('maze.txt')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.direction = 1
            elif event.key == pygame.K_RIGHT:
                player.direction = 3
            elif event.key == pygame.K_UP:
                player.direction = 2
            elif event.key == pygame.K_DOWN:
                player.direction = 4
    current_time = time.time()
    if current_time - last_switch > switch_interval:
        for ghost in ghosts:
            ghost.switch_mode()
        last_switch = current_time
    
    pacman_position = (player.x, player.y)
    screen.fill((0,0,0))
    draw_maze(maze)
    player.draw(maze)
    for ghost in ghosts:
        ghost.draw()
        ghost.move(maze,pacman_position)
    
    font = pygame.font.Font("freesansbold.ttf",32)
    text = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(text,(10,10))
    pygame.display.update()
    pygame.time.Clock().tick(60)
  
pygame.quit()
    
