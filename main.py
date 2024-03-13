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
        self.playing = False

        #Musikk
        self.lobby_sfx = pg.mixer.Sound('lobby.mp3')
        self.bgmusic_sfx = pg.mixer.Sound('bgmusic.mp3')
        self.damage_sfx = pg.mixer.Sound('damage.mp3')
        self.eating_sfx = pg.mixer.Sound('eating.mp3')
        self.drinking_sfx = pg.mixer.Sound('drinking.mp3')
        self.xp_sfx = pg.mixer.Sound('xp.mp3')

        self.lobby_sfx.play()

        # Setter volumet for bakgrunnsmusikken
        self.bgmusic_volume = 0.2
        self.bgmusic_sfx.set_volume(self.bgmusic_volume)

    def show_start_screen(self):
        start_screen = pg.transform.scale(pg.image.load('start_screen.png'), SIZE_BG)

        self.screen.fill(WHITE)
        self.screen.blit(start_screen,(0,60))
        self.screen.blit(Player().image, Player().rect)

        self.events()
        pg.display.flip()
        
    # Metode for å starte et nytt spill
    def new(self):
        # Lager spiller-objekt
        self.player = Player()
        self.fuelbar = Fuelbar(WINDOW_WIDTH * 0.725, FREEZONE_UP//3, 250, 20, 100)
        self.obstacles = []
        self.burger = []
        self.soda = []
        self.star = []
        self.speed = SCROLL_SPEED

        self.jump_count = 0
        self.score = 0
        
        self.run()


    # Metode som kjører spillet
    def run(self):
        # Game loop
        self.playing = True

        t1 = time.time()

        t1p = time.time()

        while self.playing:
            self.clock.tick(FPS)
            self.events()

            t2 = time.time()

            t2p = time.time()

            dt = t2-t1

            dtp = t2p - t1p

            if dtp >= 1:
                self.score += 1
                t1p = time.time()

            if self.score < 25:
                SPR = 1
            elif self.score < 50:
                SPR = 0.8
            elif self.score < 100:
                SPR = 0.7
            
            if dt >= SPR:
                a = random.randint(1,2)
                if a == 1:
                    ny = ObstH(self.speed)
                elif a == 2:
                    ny = ObstV(self.speed)
                
                self.obstacles.append(ny)

                t1 = time.time()

            while len(self.burger) < 1:
                self.burger.append(Burger(self.speed))

            while len(self.soda) < 1:
                self.soda.append(Soda(self.speed))

            while len(self.star) < 1:
                self.star.append(Star(self.speed))
            
            self.update()
            self.draw()
            
    
    def antallPoeng(self):
        font = pg.font.SysFont('Comicsans', 20)
        text_img = font.render(f"SCORE: {self.score}", True, BLACK)
        self.screen.blit(text_img, (10, FREEZONE_UP//3))

    def scroll_background(self):
        # Laster inn bakgrunnsbildet
        bg_img = pg.image.load('bg.png')
        bg_img = pg.transform.scale(bg_img, SIZE_BG)
        
        # Beregn x-posisjon for bakgrunnsbildet basert på tiden som har gått
        global scroll_x
        scroll_x -= self.speed
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
                self.bgmusic_sfx.stop()
                self.running = False # Spillet skal avsluttes
                
            if event.type == pg.KEYDOWN:
                if self.playing == False and event.key == pg.K_SPACE:
                    self.playing = True
                    self.lobby_sfx.stop()
                    self.bgmusic_sfx.play()
                
                elif self.playing and event.key == pg.K_SPACE and self.jump_count < 2:
                    self.jump_count += 1
                    self.player.jump()
                    self.fuelbar.fuel -= 5 

    # Metode som oppdaterer
    def update(self):
        self.fuelbar.decrease_fuelbar()
        if self.fuelbar.fuel <= 0:
            self.bgmusic_sfx.stop()
            self.playing = False
            

        if len(self.obstacles) > 0 and self.obstacles[0].x+self.obstacles[0].w < 0:
                self.obstacles.remove(self.obstacles[0])
        
        for h in self.obstacles:
            if pg.Rect.colliderect(h.rect, self.player.rect):
                self.bgmusic_sfx.stop()
                self.damage_sfx.play()
                self.playing = False
            
            h.update()
            
        for b in self.burger:
            b.update()

            if b.x+b.w < 0: 
                self.burger.remove(b)
            
            if pg.Rect.colliderect(b.rect, self.player.rect):
                self.bgmusic_sfx.set_volume(0)
                self.eating_sfx.play()
                self.bgmusic_sfx.set_volume(self.bgmusic_volume)
                self.fuelbar.fuel += b.food
                b.x = 0-b.w
        
        for s in self.soda:
            s.update()

            if s.x+s.w < 0: 
                self.soda.remove(s)
            
            if pg.Rect.colliderect(s.rect, self.player.rect):
                self.bgmusic_sfx.set_volume(0)
                self.drinking_sfx.play()
                self.bgmusic_sfx.set_volume(self.bgmusic_volume)
                self.fuelbar.fuel += s.food
                s.x = 0-s.w
        
        for s in self.star:
            s.update()

            if s.x+s.w < 0: 
                self.star.remove(s)
            
            if pg.Rect.colliderect(s.rect, self.player.rect):
                self.bgmusic_sfx.set_volume(0)
                self.xp_sfx.play()
                self.bgmusic_sfx.set_volume(self.bgmusic_volume)
                self.score += 10
                self.fuelbar.fuel += s.food
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
        self.screen.blit(self.player.image, self.player.rect)
        self.fuelbar.draw_fuelbar(self.screen)
        
        for h in self.obstacles :
            self.screen.blit(h.image, h.rect)
        
        for b in self.burger:
            self.screen.blit(b.image, b.rect)
        
        for s in self.soda:
            self.screen.blit(s.image, s.rect)
        
        for s in self.star:
            self.screen.blit(s.image, s.rect)
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
    
    def show_end_screen(self):

        #start_screen = pg.transform.scale(pg.image.load('start_screen.png'), SIZE_BG)

        self.screen.fill(WHITE)

        #self.screen.blit(start_screen,(0,60))

        font = pg.font.SysFont('Comicsans', 50)
        text_img = font.render(f"FINAL SCORE: {self.score}", True, BLACK)
        self.screen.blit(text_img, ((WINDOW_WIDTH//2)-200, (WINDOW_HEIGHT//2)))
        
        pg.display.flip()
        time.sleep(3)
        self.running = False




# Lager et spill-objekt
game_object = Game()


# Spill-løkken
while game_object.running:
    # Starter et nytt spill
    
    while game_object.playing == False:
        game_object.show_start_screen()
    
    while game_object.playing:
        game_object.new()

    game_object.show_end_screen()
    



# Avslutter pygame
pg.quit()
#sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()
print(f"Du endte med {game_object.score} poeng!")