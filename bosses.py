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
        self.rect.bottom = 830
        self.vida = 80
        self.max_vida = 80

        self.ultima_tacada = pygame.time.get_ticks() 
        self.tacada_ticks = 2000
        self.ultimo_ataque_chuva = pygame.time.get_ticks()
        self.intervalo_chuva = random.randint(300, 1000)
    
    def update_tiro(self): 
        agora = pygame.time.get_ticks()
        ticks_passados = agora - self.ultima_tacada
        if ticks_passados > self.tacada_ticks:
            self.ultima_tacada = agora
            self.image = self.assets['boss jogando barril'] 
            altura_do_barril = self.rect.bottom + 15
            novo_barril = Barril(altura_do_barril, self.rect.centerx, self.assets)
            self.groups["barris"].add(novo_barril)
        if 1000 < ticks_passados < 2000: 
            self.image = self.assets["chefe idle"]
    
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

    def ataque_chuva(self, intervalo1, intervalo2): 
        agora = pygame.time.get_ticks()
        passados = agora - self.ultimo_ataque_chuva
        if passados >= self.intervalo_chuva: 
            self.ultimo_ataque_chuva = agora
            for _ in range(3):
                x = random.randint(intervalo1, intervalo2)
                novo_fogo = Fogo(self.assets, self.groups, x, 0)
                self.groups["foguinhos"].add(novo_fogo)
            self.intervalo_chuva = random.randint(300, 1000)


class Barril(pygame.sprite.Sprite): 
    def __init__(self, bottom, centerx, assets):
        pygame.sprite.Sprite.__init__(self)

        self.animacao = assets["barril rolando"]
        self.frame = 0
        self.image = self.animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom 

        self.speedx = -6
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

class Fogo(pygame.sprite.Sprite):
    def __init__(self, assets, grupos, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.animacao = assets["foguinho dk"]
        self.frame = 0
        self.image = self.animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

        self.ultimo_ticks = pygame.time.get_ticks()
        self.ticks_animacao = 50
    
    def update(self):
        self.rect.y += self.speed
        self.update_animacao()
    
    def update_animacao(self): 
        agora = pygame.time.get_ticks()
        ticks_passados = agora - self.ultimo_ticks
        if ticks_passados > self.ticks_animacao:
            self.ultimo_frame = agora
            self.frame += 1
            self.image = self.animacao[self.frame % len(self.animacao)]

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

        LIMITE_ESQUERDO = 1000
        LIMITE_DIREITO = 1720

        if self.rect.left < LIMITE_ESQUERDO:
            self.rect.left = LIMITE_ESQUERDO
            self.speedx = abs(self.speedx)  
        elif self.rect.right > LIMITE_DIREITO:
            self.rect.right = LIMITE_DIREITO
            self.speedx = -abs(self.speedx)  

    def atacar(self, player):
        agora = pygame.time.get_ticks()
        fase = self.fase_atual()

        if fase == 1:
            intervalo = 3000
            self.speedx = -2
        elif fase == 2:
            intervalo = 2000
            self.speedx = -3
        else:
            intervalo = 1500
            self.speedx = -4

        if agora - self.ultimo_ataque < intervalo:
            return
        self.ultimo_ataque = agora

        if fase >= 1:
            self.ataque_chuva()
        if fase >= 2:
            self.ataque_investida(player)
        if fase == 3:
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

class FlorDeFogo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Chefes/flor_de_fogo.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

class EggMan(pygame.sprite.Sprite): 
    def __init__(self, assets, grupos):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets["EggMan Idle"]
        self.assets = assets
        self.groups = grupos
        self.rect = self.image.get_rect()
        self.rect.centerx = 1600
        self.rect.bottom = 800

        self.speedx = -2  
        self.vida = 100
        self.max_vida = 100

        self.ultimo_ataque = pygame.time.get_ticks()

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, animacao, x, y, speedx=0):
        super().__init__()
        self.animacao = animacao
        self.image = self.animacao[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speedx = speedx
        self.frame = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.frame_interval = 200

    def update(self):
        self.rect.x += self.speedx
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.frame_interval:
            self.ultimo_frame = agora
            self.frame = (self.frame + 1) % len(self.animacao)
            self.image = self.animacao[self.frame]

# --------------------------
# Subclasses específicas
# --------------------------

class Goomba(Inimigo):
    def __init__(self, assets, x, y):
        super().__init__(assets["goomba"], x, y, speedx=-2)
        self.dano = 10

class Koopa(Inimigo):
    def __init__(self, assets, x, y):
        super().__init__(assets["koopa"], x, y, speedx=-1.5)
        self.dano = 15

class PlantaCarnivora(Inimigo):
    def __init__(self, assets, x, y):
        super().__init__(assets["planta"], x, y, speedx=0)
        self.dano = 25