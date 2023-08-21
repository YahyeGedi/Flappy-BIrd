import pygame
import time
import os
import random


pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
Bird_Images = [pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy bird images", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy bird images", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy bird images", "bird3.png")))]
Pipe_Image =  pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy bird images", "pipe.png")))
BG_Image = pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy bird images", "bg.png")))
Base_Image = pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy bird images", "base.png")))
Font = pygame.font.SysFont("comicsans", 50)

class Bird:
    IMGS = Bird_Images
    MAX_ROTATION = 25
    ROTATION_Vel = 20
    Animation_Time = 5


    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = y
        self.image_count = 0
        self.images = self.IMGS[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self, bird):
        move_down = False
        move_up = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_up = True
                if event.key == pygame.K_DOWN:
                   move_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                   move_down = False
        if move_down:
            bird.y += 7
        elif move_up:
            bird.y -= 7
        
    
    def draw(self, win):
        self.image_count +=1
         
        if self.image_count < self.Animation_Time:
            self.images = self.IMGS[0]
        elif self.image_count < self.Animation_Time*2:
            self.images = self.IMGS[1]
        elif self.image_count < self.Animation_Time*3:
            self.images = self.IMGS[2]
        elif self.image_count < self.Animation_Time*4:
            self.images = self.IMGS[1]
        elif self.image_count < self.Animation_Time*5:
            self.images = self.IMGS[0]

        if self.tilt <= -80:
            self.images = self.IMGS[1]
            self.image_count = self.Animation_Time*2
        
        rotated_image = pygame.transform.rotate(self.images, self.tilt)
        new = rotated_image.get_rect(center=self.images.get_rect(topleft = (self.x, self.y)).center) 
        win.blit(rotated_image, new.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.images)
    

class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self, x) -> None:
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(Pipe_Image, False, True)
        self.PIPE_BOTTOM = Pipe_Image
        self.passed = False
        self.Set_height()

    def Set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask =  pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask =  pygame.mask.from_surface(self.PIPE_BOTTOM)

        t_offset = (self.x - bird.x, self.top - round(bird.y))
        b_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        t_point = bird_mask.overlap(top_mask, t_offset)
        b_point = bird_mask.overlap(bottom_mask, b_offset)

        if t_point or b_point:
            return True
        return False  


class Base:
    VELOCITY = 5
    Width = Base_Image.get_width()
    Image = Base_Image

    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.Width

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.Width < 0:
            self.x1 = self.x2 + self.Width
        
        if self.x2 + self.Width < 0:
            self.x2 = self.x1 + self.Width

    def draw(self, win):
        win.blit(self.Image, (self.x1, self.y))
        win.blit(self.Image, (self.x2, self.y))

    



def draw_window(win, bird, pipes, base, score):
    win.blit(BG_Image, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    
    text = Font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    
    base.draw(win)

    bird.draw(win)

    pygame.display.update()



def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(550)]
    score = 0
    speed_up = 1

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(45)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and bird.y > 0 :
            bird.y -= 8
        if keys[pygame.K_DOWN] and bird.y < WIN_HEIGHT:
            bird.y += 8

        add_pipe = False
        remove = []
        for pipe in pipes:
            if pipe.collide(bird):
                run = False
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        if add_pipe:
            score += 1
            pipes.append(Pipe(550 - 2*speed_up))
        
        for r in remove:
            pipes.remove(r)
        
        if score > 10*speed_up:
            pipe.VELOCITY += 1
            base.VELOCITY +=1
            speed_up +=1
            



        base.move()
        
        draw_window(window, bird, pipes, base, score)

    print("\nYour Score Was:" ,score, "\n")
    pygame.quit()
    quit()  

main()

