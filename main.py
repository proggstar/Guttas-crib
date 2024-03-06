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
        self.burger = []
        self.soda = []
        self.star = []

        self.jump_count = 0
        self.dt = self.clock.tick(FPS) / 1000
        self.score = 0
        
        self.run()


    # Metode som kjører spillet
    def run(self):
        # Game loop
        self.playing = True

        t1 = time.time()

        while self.playing:
            self.clock.tick(FPS)
            self.events()

            t2 = time.time()

            dt = t2-t1

            if dt >= 1:
                a = random.randint(1,2)
                if a == 1:
                    ny = HindringV()
                elif a == 2:
                    ny = HindringH()
                
                self.hindringer.append(ny)

                t1 = time.time()

            while len(self.burger) < 1:
                self.burger.append(Burger())

            while len(self.soda) < 1:
                self.soda.append(Soda())

            while len(self.star) < 1:
                self.star.append(Star())
            
            self.update()
            self.draw()
            
    
    def antallPoeng(self):
        global timer
        timer += self.dt
        
        font = pg.font.SysFont('Arial', 20)
        text_img = font.render(f"Poengscore: {self.score}", True, BLACK)
        self.screen.blit(text_img, (10, FREEZONE_UP//3))
        
        
        
    
        if timer >= 1:
            self.score += 1
            timer = 0


    def scroll_background(self):
        # Laster inn bakgrunnsbildet
        bg_img = pg.image.load('bg.png')
        # Fikser bakgrunnsbildet til størrelsen på skjermen
        bg_img = pg.transform.scale(bg_img, SIZE_BG)
        
        # Beregn x-posisjon for bakgrunnsbildet basert på tiden som har gått
        scroll_speed = 4  # Juster denne verdien for ønsket rullehastighet
        global scroll_x
        scroll_x -= scroll_speed
        if scroll_x <= -WINDOW_WIDTH:
            scroll_x = 0
        
        # Tegn to kopier av bakgrunnsbildet ved siden av hverandre for å oppnå rullingseffekten
        self.screen.blit(bg_img, (scroll_x, 60))
        self.screen.blit(bg_img, (scroll_x + WINDOW_WIDTH, 60))

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
                if event.key == pg.K_SPACE and self.jump_count < 2:
                    self.jump_count += 1
                    self.player.jump()

    # Metode som oppdaterer
    def update(self):
        self.fuelbar.decrease_fuelbar()

        if len(self.hindringer) > 0 and self.hindringer[0].x+self.hindringer[0].w < 0:
                self.hindringer.remove(self.hindringer[0])
        
        for h in self.hindringer:
            if pg.Rect.colliderect(h.rect, self.player.rect):
                if self.playing:
                    self.playing = False
                time.sleep(1)
                self.running = False
            
            h.update()
            
        



        for b in self.burger:
            b.update()

            if b.x+b.w < 0: 
                self.burger.remove(b)
            
            if pg.Rect.colliderect(b.rect, self.player.rect):
                self.fuelbar.fuel += b.food
                b.x = 0-b.w
        
        for s in self.soda:
            s.update()

            if s.x+s.w < 0: 
                self.soda.remove(s)
            
            if pg.Rect.colliderect(s.rect, self.player.rect):
                self.fuelbar.fuel += s.food
                s.x = 0-s.w
        
        for s in self.star:
            s.update()

            if s.x+s.w < 0: 
                self.star.remove(s)
            
            if pg.Rect.colliderect(s.rect, self.player.rect):
                self.score += 10
                s.x = 0-s.w
        
        if self.fuelbar.fuel > self.fuelbar.max_fuel:
            self.fuelbar.fuel = self.fuelbar.max_fuel
            
        if (self.player.pos[1] + PLAYER_HEIGHT >= FREEZONE_DOWN):
            self.jump_count = 0
        
        self.player.update()

    # Metode som tegner ting på skjermen
    def draw(self):
        # Fyller skjermen med en farge
        self.screen.fill(WHITE)
        self.scroll_background()
        self.antallPoeng()
        
        # Tegner spilleren
        self.screen.blit(self.player.image, self.player.rect.center)
        self.fuelbar.draw_fuelbar(self.screen)
        
        for h in self.hindringer:
            self.screen.blit(h.image, h.rect.center)
        
        for b in self.burger:
            self.screen.blit(b.image, b.rect.center)
        
        for s in self.soda:
            self.screen.blit(s.image, s.rect.center)
        
        for s in self.star:
            self.screen.blit(s.image, s.rect.center)
        
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
print(f"Du endte med {game_object.score} poeng!")
