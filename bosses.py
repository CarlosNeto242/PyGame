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
        self.image = pygame.transform.flip(self.image, True, False)
        self.assets = assets
        self.groups = grupos
        self.rect = self.image.get_rect()
        self.rect.centerx = 1600
        self.rect.bottom = 800

        self.speedx = -2  
        self.vida = 100
        self.max_vida = 100

        self.ultimo_ataque = pygame.time.get_ticks()

    def update_comportamento(self, player):
        self.movimentar()
        self.atacar(player)

    def movimentar(self):
        self.rect.x += self.speedx
        if self.rect.left <= 1200 or self.rect.right >= 1800:
            self.speedx *= -1

    def atacar(self, player):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque < 2000:
            return
        self.ultimo_ataque = agora

        if self.vida > 60:
            self.ataque_chuva()
        elif self.vida > 30:
            self.ataque_chuva()
            self.ataque_investida(player)
        else:
            self.ataque_chuva()
            self.ataque_investida(player)
            self.ataque_lateral()

    def ataque_chuva(self):
        for _ in range(4):
            x = random.randint(100, 1700)
            nova_bola = BolaDeFogo(x, 0)
            self.groups["bolas_de_fogo"].add(nova_bola)

    def ataque_investida(self, player):
        if abs(player.rect.centery - self.rect.centery) < 200:
            self.rect.x -= 80  

    def ataque_lateral(self):
        nova_bola = BolaDeFogo(self.rect.centerx, self.rect.centery, vertical=False)
        self.groups["bolas_de_fogo"].add(nova_bola)

    def levar_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.kill()
    def fase_atual(self):
        if self.vida > 60:
            return 1
        elif self.vida > 30:
            return 2
        else:
            return 3


class BolaDeFogo(pygame.sprite.Sprite):
    def __init__(self, x, y, vertical=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Chefes/bola_fogo.png"), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vertical = vertical
        self.speed = 10
    def update(self):
        if self.vertical:
            self.rect.y += self.speed
        else:
            self.rect.x -= self.speed
        if self.rect.top > 1080 or self.rect.right < 0:
            self.kill()
