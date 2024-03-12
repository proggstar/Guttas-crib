import pygame as pg
from settings import *
import random
import time

class Player:
    def __init__(self):
        self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (
            START_X_PLAYER,
            START_Y_PLAYER
        )
        
        self.pos = list(self.rect.center)
        self.vel = [0, 0]
        self.acc = [0, 0.8]

        self.image = pg.transform.scale(pg.image.load('player.png'), (PLAYER_WIDTH,PLAYER_HEIGHT))

    
    def jump(self):
        self.vel[1] = -18
    
    def update(self):
        # Bevegelseslikning i y-retning
        self.vel[1] += self.acc[1]
        self.pos[1] += self.vel[1] + 0.5*self.acc[1]
        
        if (self.pos[1] + PLAYER_HEIGHT >= FREEZONE_DOWN):
            self.pos[1] = FREEZONE_DOWN - PLAYER_HEIGHT
        
        if (self.pos[1] <= FREEZONE_UP):
            self.pos[1] = FREEZONE_UP
            self.vel[1] = 0
        
        if self.pos[1] + PLAYER_HEIGHT == FREEZONE_DOWN:
            self.image = pg.transform.scale(pg.image.load('player.png'), (PLAYER_WIDTH,PLAYER_HEIGHT))
        else:
            self.image = pg.transform.scale(pg.image.load('diddy_jump.png'), (64,PLAYER_HEIGHT))
        
        self.rect.center = self.pos


class Object:
    def __init__(self):
        self.y = random.randint(FREEZONE_UP, FREEZONE_DOWN - 80)

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
        self.x = WINDOW_WIDTH
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
        self.image = pg.transform.scale(pg.image.load('obst_h.png'), (self.w,self.h))

class ObstV(Obst):
    def __init__(self, speed):
        self.speed = speed
        self.w = 20
        self.h = 80
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('obst_v.png'), (self.w,self.h))


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
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('star.png'), (self.w,self.h))
        #self.image.fill(YELLOW)

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
        self.image = pg.transform.scale(pg.image.load('burger.png'), (self.w,self.h))
        #self.image.fill(LIGHTBLUE)

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
        self.image = pg.transform.scale(pg.image.load('soda.png'), (self.w,self.h))

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
        self.fuel -= 0.04
        if self.fuel < 0:
            self.fuel = 0
            time.sleep(1)
            pg.quit()
