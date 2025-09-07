import pygame
import sys
import random
import time
import pickle
# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cars")

# Background setup
background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (1660,600))
background1x = 0
background2x = WIDTH
background_speed = 7
button_font = pygame.font.SysFont("Arial", 36)
score_font = pygame.font.Font('freesansbold.ttf', 32)

score = 0
hi_score = 0
# Button class


class Button:
    def __init__(self, text, x, y, w, h, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255,0,0)
        self.action = action 

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        label = button_font.render(self.text, True, (0,0,0))
        screen.blit(label, (self.rect.x + (self.rect.width - label.get_width()) // 2,
                            self.rect.y + (self.rect.height - label.get_height()) // 2))

    def check_click(self, pos, change_color = False):
        if self.rect.collidepoint(pos):
            if change_color:
                self.color = (0,255,0)
            if self.action:
                self.action()              
class Car:
    def __init__(self, image, y, x):
        self.car_image = pygame.image.load(image)
        self.y = y
        self.x = x
        self.move_downward = False
        self.move_upward = False

    def draw(self):
        if self.move_downward:
            self.y += 40
        if self.move_upward:
            self.y -= 40
        if self.y in (100, 300, 500):
            self.move_downward, self.move_upward = False, False
        screen.blit(self.car_image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y,
                           self.car_image.get_width(),
                           self.car_image.get_height())

class Obs:
    def __init__(self, lane,  x):
        global background_speed
        self.obs = pygame.transform.scale(pygame.image.load("images/OBS.png"), (75, 115))
        self.speed = background_speed
        self.x = x
        # Lane positions (y)
        self.y = 50 if lane == 1 else (250 if lane == 2 else 450)

    def draw(self):
        global background_speed
        self.x -= background_speed
        screen.blit(self.obs, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y,
                           self.obs.get_width(),
                           self.obs.get_height())

class Preset:
    def __init__(self):
        self.obstacles = []
        self.first_obs = None

    def make_preset(self):
        choice = random.randint(1, 5)
        if choice == 1:
            new_obstacles = [Obs(1, WIDTH+75), Obs(2, WIDTH+75),
                               Obs(3, WIDTH+675), Obs(2, WIDTH+675)]
            self.first_obs = new_obstacles[0]
            self.obstacles += new_obstacles
            
        elif choice == 2:
            new_obstacles = [Obs(1, WIDTH+75), Obs(2, WIDTH+75), Obs(3, WIDTH+575)]
            self.first_obs = new_obstacles[0]
            self.obstacles += new_obstacles
        elif choice == 3:
            new_obstacles = [Obs(3, WIDTH+75), Obs(2, WIDTH+75), Obs(1, WIDTH+575)]
            self.first_obs = new_obstacles[0]
            self.obstacles += new_obstacles
        elif choice == 4:
                        new_obstacles = [Obs(2, WIDTH+75), Obs(3, WIDTH+75),
                                            Obs(1, WIDTH+675), Obs(2, WIDTH+675)]
                        self.first_obs = new_obstacles[0]
                        self.obstacles += new_obstacles
        elif choice == 5:
            new_obstacles = [Obs(1, WIDTH+75), Obs(2, WIDTH+275), Obs(2, WIDTH+365),
                                Obs(3, WIDTH+775)]
            self.first_obs = new_obstacles[0]
            self.obstacles += new_obstacles



    def draw_preset(self):
        for obstacle in self.obstacles:
            obstacle.draw()
        # Keep only onscreen obstacles
        self.obstacles = [o for o in self.obstacles if o.x > -100]
        if self.first_obs.x <  500:
            self.make_preset()

# Clock & FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Game state
car = Car("images/paintcar.png", 300, 260)


def quit_game():
    sys.exit()
def main_game():
    pre = Preset()
    pre.make_preset()
    global background, background1x, background2x, WHITE, car, background_speed, score, score_font, hi_score
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        score += background_speed
        text = score_font.render(f'high score: {hi_score} Score: {score}', True, (0,255,0), (0,0,255))
        textRect = text.get_rect()
        
        # --- Update ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            if car.y < 500 and not car.move_upward:
                car.move_downward = True
        if keys[pygame.K_w]:
            if car.y > 100 and not car.move_downward:
                car.move_upward = True
        
        for obstacle in pre.obstacles: # each obstacle
            rect_car = car.get_rect()
            if rect_car.colliderect(obstacle.get_rect()):
                pre.obstacles = [] # we're going to the menu screen, no obstacles now please
                if score > hi_score:
                    hi_score = score
                score = 0
                return # check collision with of each obstacle

        if keys[pygame.K_a]:
            return
        
        # --- Background ---
        background1x -= background_speed
        background2x -= background_speed
        if background1x <= -WIDTH:
            background1x = WIDTH
        if background2x <= -WIDTH:
            background2x = WIDTH
        # --- Draw ---
        screen.fill(WHITE)
        screen.blit(background, (background1x, 0))
        screen.blit(background, (background2x, 0))
        pre.draw_preset()
        car.draw()
        screen.blit(text, textRect)
        
        pygame.display.flip()

        clock.tick(FPS)
def easy():
    global background_speed
    background_speed = 13
def medium():
    global background_speed
    background_speed = 17

def hard():
    global background_speed
    background_speed = 24


# Game loop
running = True
play_button = Button("Play", WIDTH//2 - 100, HEIGHT//2 - 60, 200, 60, main_game)
quit_button = Button("Quit", WIDTH//2 - 100, HEIGHT//2 + 20, 200, 60, quit_game)
# Difficulty buttons (same row, centered under Quit)
button_width = 150
button_height = 50
spacing = 20  # space between buttons

# Calculate starting x so they are centered as a row
start_x = WIDTH//2 - (button_width*3 + spacing*2)//2
y_pos = HEIGHT//2 + 100   # a bit lower than Quit

easy_button = Button("Easy", start_x, y_pos, button_width, button_height, easy)
medium_button = Button("Medium", start_x + button_width + spacing, y_pos, button_width, button_height, medium)
hard_button = Button("Hard", start_x + (button_width + spacing)*2, y_pos, button_width, button_height, hard)
#menu screen
while running:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                play_button.check_click(event.pos)
                quit_button.check_click(event.pos)
                easy_button.check_click(event.pos, change_color= True)
                medium_button.check_click(event.pos, change_color= True)
                hard_button.check_click(event.pos, change_color= True)

    
    
    # --- Background ---
    background1x -= background_speed
    background2x -= background_speed
    if background1x <= -WIDTH:
        background1x = WIDTH
    if background2x <= -WIDTH:
        background2x = WIDTH

    # --- Draw ---
    screen.fill(WHITE)
    screen.blit(background, (background1x, 0))
    screen.blit(background, (background2x, 0))
    car.draw()
    play_button.draw(screen)
    quit_button.draw(screen)
    easy_button.draw(screen)
    medium_button.draw(screen)
    hard_button.draw(screen)
    
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
