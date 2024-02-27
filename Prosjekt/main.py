import pygame as pg
import sys
import random
import time
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # Initiere pygame
        pg.init()

        # Lager hovedvinduet
        self.screen = pg.display.set_mode(SIZE)

        # Lager en klokke
        self.clock = pg.time.Clock()
        
        # Attributt som styrer om spillet skal kjøres
        self.running = True
        
        
    # Metode for å starte et nytt spill
    def new(self):
        # Lager spiller-objekt
        self.player = Player()
        self.fuelbar = Fuelbar(WINDOW_WIDTH * 0.725, FREEZONE_UP//3, 250, 20, 100)
        self.hindringer = []
        self.powerups = []
        
        self.run()


    # Metode som kjører spillet
    def run(self):
        # Game loop
        self.playing = True
        
        while self.playing:
            self.clock.tick(FPS)
            self.events()


            while len(self.hindringer) < 14: 
                a = random.randint(1,2)
                if a == 1:
                    ny = HindringV()
                elif a == 2:
                    ny = HindringH()
                
                safe = True

                for h in self.hindringer:
                    if pg.Rect.colliderect(ny.rect,h.rect) or abs(h.x-ny.x) < 100:
                        safe = False
                        break
                    
                if safe:
                    self.hindringer.append(ny)

            while len(self.powerups) < 1:
                self.powerups.append(Powerup())

            
            
            self.update()
            self.draw()
        
        
    # Metode som håndterer hendelser
    def events(self):
        # Går gjennom hendelser (events)
        for event in pg.event.get():
            # Sjekker om vi ønsker å lukke vinduet
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False # Spillet skal avsluttes
                
            if event.type == pg.KEYDOWN:
                # Spilleren skal hoppe hvis vi trykker på mellomromstasten
                if event.key == pg.K_SPACE:
                    self.player.jump()
    
    # Metode som oppdaterer
    def update(self):
        self.player.update()
        self.fuelbar.decrease_fuelbar()

        if self.hindringer[0].x+self.hindringer[0].w < 0:
                self.hindringer.remove(self.hindringer[0])
        
        for h in self.hindringer:
            h.update()
            
            if pg.Rect.colliderect(h.rect, self.player.rect):
                if self.playing:
                    self.playing = False
                time.sleep(1)
                self.running = False
        
        for p in self.powerups:
            p.update()

            if p.x+p.w < 0: 
                self.powerups.remove(p)
            
            if pg.Rect.colliderect(p.rect, self.player.rect):
                self.fuelbar.feed_fuelbar()
                p.x = 0-p.w
            
    
    # Metode som tegner ting på skjermen
    def draw(self):
        # Fyller skjermen med en farge
        self.screen.fill(WHITE)
        
        # Tegner spilleren
        self.screen.blit(self.player.image, self.player.rect.center)
        self.fuelbar.draw_fuelbar(self.screen)
        
        for h in self.hindringer:
            self.screen.blit(h.image, h.rect.center)
        
        for p in self.powerups:
            self.screen.blit(p.image, p.rect.center)
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
    
    
    # Metode som viser start-skjerm
    def show_start_screen(self):
        pass


    
    
# Lager et spill-objekt
game_object = Game()


# Spill-løkken
while game_object.running:
    # Starter et nytt spill
    game_object.new()
    


# Avslutter pygame
pg.quit()
#sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()
