import pygame as pg
from settings import *
import random
import time

class Player:
    def __init__(self):
        self.image = pg.transform.scale(pg.image.load('Bilder/player.png'), (PLAYER_WIDTH,PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (
            START_X_PLAYER,
            START_Y_PLAYER
        )
        
        self.pos = list(self.rect.center)
        self.vel = [0, 0]
        self.acc = [0, 0.8]
        self.t1 = time.time()
        self.pictures = ['Bilder/diddy_walk2.png', 'Bilder/diddy_walk1.png']


    
    def jump(self):
        self.vel[1] = -18
    
    def update(self):
        # Bevegelseslikning i y-retning
        self.vel[1] += self.acc[1]
        self.pos[1] += self.vel[1] + 0.5*self.acc[1]
        
        if (self.pos[1] + PLAYER_HEIGHT//2 >= FREEZONE_DOWN):
            self.pos[1] = FREEZONE_DOWN - PLAYER_HEIGHT//2
        
        if (self.pos[1] - PLAYER_HEIGHT//2 <= FREEZONE_UP):
            self.pos[1] = FREEZONE_UP + PLAYER_HEIGHT//2
            self.vel[1] = 0

        if self.pos[1] + PLAYER_HEIGHT >= FREEZONE_DOWN:
            t2 = time.time()

            dt = t2 -self.t1

            if dt >= 0.25:
                self.image = pg.transform.scale(pg.image.load(self.pictures[0]), (46,PLAYER_HEIGHT))
                self.pictures.append(self.pictures[0])
                self.pictures.remove(self.pictures[0])
                self.t1 = time.time()
        elif self.vel[1] > 0 and self.pos[1] >= FREEZONE_DOWN-200:
            self.image = pg.transform.scale(pg.image.load('Bilder/diddy_walk2.png'), (46,PLAYER_HEIGHT))
        else:
            self.image = pg.transform.scale(pg.image.load('Bilder/diddy_jump.png'), (64,PLAYER_HEIGHT))
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


class Object:
    def __init__(self):
        self.y = random.randint(FREEZONE_UP+40, FREEZONE_DOWN - 40)

        self.image = pg.Surface((self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.center = (
            self.x,
            self.y
        )

    
    def update(self):
        self.x -= self.vx
        self.rect.center = (
            self.x,
            self.y
        )

# Hindringer
class Obst(Object):
    def __init__(self):
        self.x = WINDOW_WIDTH + 40
        super().__init__()
        self.image.fill(BLACK)
    
    def update(self):
        self.vx = self.speed
        super().update()
        
class ObstH(Obst):
    def __init__(self, speed):
        self.speed = speed
        self.w = 80
        self.h = 20
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('Bilder/obst_h.png'), (self.w,self.h))

class ObstV(Obst):
    def __init__(self, speed):
        self.speed = speed
        self.w = 20
        self.h = 80
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('Bilder/obst_v.png'), (self.w,self.h))


# Powerups
class Powerup(Object):
    def __init__(self):
        self.w = POWERUP_WIDTH
        self.h = POWERUP_HEIGHT
        super().__init__()

class Star(Powerup):
    def __init__(self, speed):
        self.x = random.randint(WINDOW_WIDTH*12, WINDOW_WIDTH*20)
        self.speed = speed
        self.food = 100
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('Bilder/star.png'), (self.w,self.h))

    def update(self):
        self.vx = self.speed*2.5
        super().update()


class Burger(Object):
    def __init__(self, speed):
        self.x = random.randint(WINDOW_WIDTH*4, WINDOW_WIDTH*5)
        self.speed = speed
        self.food = 50

        self.w = 50
        self.h = 50
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('Bilder/burger.png'), (self.w,self.h))

    def update(self):
        self.vx = self.speed*1.25
        super().update()

class Soda(Object):
    def __init__(self, speed):
        self.x = random.randint(WINDOW_WIDTH*3, WINDOW_WIDTH*4)
        self.speed = speed
        self.food = 25
        self.w = 20
        self.h = 50
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('Bilder/soda.png'), (self.w,self.h))

    def update(self):
        self.vx = self.speed*1.75
        super().update()


# Fuelbar
class Fuelbar:
    def __init__(self, x, y, w, h, max_fuel):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fuel = max_fuel
        self.max_fuel = max_fuel
        
    def draw_fuelbar(self, surface):
        ratio = self.fuel / self.max_fuel
        
        pg.draw.rect(surface, RED, [self.x, self.y, self.w, self.h])
        pg.draw.rect(surface, GREEN, [self.x, self.y, self.w*ratio, self.h])
        
    
    def decrease_fuelbar(self):  
        self.fuel -= 0.05
        
