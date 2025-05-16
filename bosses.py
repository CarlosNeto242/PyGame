import pygame
import parametros as p
import player as pl 

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
