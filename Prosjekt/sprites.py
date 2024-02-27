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
        
    
    def jump(self):
        self.vel[1] = -20
    
    def update(self):
        # Bevegelseslikning i y-retning
        self.vel[1] += self.acc[1]
        self.pos[1] += self.vel[1] + 0.5*self.acc[1]
        
        if (self.pos[1] + PLAYER_HEIGHT >= FREEZONE_DOWN):
            self.pos[1] = FREEZONE_DOWN - PLAYER_HEIGHT
        
        if (self.pos[1] <= FREEZONE_UP):
            self.pos[1] = FREEZONE_UP
            self.vel[1] = 0
        
        self.rect.center = self.pos


class Objekt:
    def __init__(self):
        self.x = random.randint(WINDOW_WIDTH, WINDOW_WIDTH*3)
        self.y = random.randint(FREEZONE_UP, FREEZONE_DOWN - 50)

        self.image = pg.Surface((self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.center = (
            self.x,
            self.y
        )

    
    def update(self):
        self.rect.center = (
            self.x,
            self.y
        )

# Hindringer
class Hindring(Objekt):
    def __init__(self):
        super().__init__()
        self.image.fill(BLACK)
    
    def update(self):
        self.x -= 4
        super().update()
        
class HindringH(Hindring):
    def __init__(self):
        self.w = 50
        self.h = 20
        super().__init__()

class HindringV(Hindring):
    def __init__(self):
        self.w = 20
        self.h = 50
        super().__init__()


# Powerups
class Powerup(Objekt):
    def __init__(self):
        self.w = POWERUP_WIDTH
        self.h = POWERUP_HEIGHT
        super().__init__()
        self.image.fill(RED)
    
    def update(self):
        self.x -= 6
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
        self.fuel -= 0.1
        if self.fuel < 0:
            self.fuel = 0
            time.sleep(1)
            pg.quit()
              
        
    def feed_fuelbar(self):
        self.fuel = 100
