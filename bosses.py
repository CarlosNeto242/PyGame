import pygame
import parametros as p
import player as pl 
import random

class Boss(pygame.sprite.Sprite): 
    def __init__(self, assets, grupos): 
        pygame.sprite.Sprite.__init__(self)

        self.image = assets["chefe idle"]
        self.assets = assets
        self.groups = grupos
        self.rect = self.image.get_rect()
        self.rect.centerx = 1400
        self.rect.bottom = 800

        self.ultima_tacada = pygame.time.get_ticks() 
        self.tacada_ticks = 2000
    def update_tiro(self): 
        agora = pygame.time.get_ticks()
        ticks_passados = agora - self.ultima_tacada
        if ticks_passados > self.tacada_ticks:
            self.ultima_tacada = agora
            self.image = self.assets['boss jogando barril'] 
            altura_do_barril = self.rect.bottom
            novo_barril = Barril(altura_do_barril, self.rect.centerx, self.assets)
            self.groups["barris"].add(novo_barril)
        if 1000 < ticks_passados < 2000: 
            self.image = self.assets["chefe idle"]

class Barril(pygame.sprite.Sprite): 
    def __init__(self, bottom, centerx, assets):
        pygame.sprite.Sprite.__init__(self)

        self.animacao = assets["barril rolando"]
        self.frame = 0
        self.image = self.animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom 

        self.speedx = -9
        self.ultimo_frame = pygame.time.get_ticks() 
        self.frame_ticks = 50
        
    def update_posicao(self):
        self.rect.x += self.speedx

        if self.rect.x > p.WIDHT:
            self.kill()
            
    def update_animacao(self): 
        agora = pygame.time.get_ticks()
        ticks_passados = agora - self.ultimo_frame
        if ticks_passados > self.frame_ticks:
            self.ultimo_frame = agora
            self.frame += 1
            self.image = self.animacao[self.frame % len(self.animacao)]
    def update(self):
        self.update_animacao()
        self.update_posicao()

class Bowser(pygame.sprite.Sprite): 
    def __init__(self, assets, grupos): 
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load("Sprites/Chefes/bowser_idle.png"), (200, 200))
        self.assets = assets
        self.groups = grupos
        self.rect = self.image.get_rect()
        self.rect.centerx = 1600
        self.rect.bottom = 800

        self.ultimo_ataque = pygame.time.get_ticks() 
        self.delay_ataque = 3000  # a cada 3 segundos
        self.chuva_duracao = 2000  # dura 2 segundos
        self.chovendo = False
        self.inicio_chuva = 0

    def update_ataque(self): 
        agora = pygame.time.get_ticks()

        if not self.chovendo and agora - self.ultimo_ataque > self.delay_ataque:
            self.chovendo = True
            self.inicio_chuva = agora
            self.ultimo_ataque = agora

        if self.chovendo:
            if agora - self.inicio_chuva < self.chuva_duracao:
                if agora % 300 < 20:  # solta várias bolas a cada 300ms
                    for _ in range(3):  # 3 bolas por vez
                        x = random.randint(100, 1700)
                        nova_bola = BolaDeFogo(x, 0)
                        self.groups["bolas_de_fogo"].add(nova_bola)
            else:
                self.chovendo = False


class BolaDeFogo(pygame.sprite.Sprite): 
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Chefes/bola_fogo.png"), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = 10

    def update(self): 
        self.rect.y += self.speedy
        if self.rect.y > 1080:
            self.kill()
