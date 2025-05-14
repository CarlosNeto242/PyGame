import pygame
import parametros as p
import assets as a
assets = a.carrega_assets()
class Player:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.i_animacao = assets["animacao player"]
        self.frame = 0 
        self.image = self.i_animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = 900
        self.speedx = 0

        self.ultimo_frame = pygame.time.get_ticks()
        self.frames_ticks = 50

    def update_deslocar(self):
        self.rect.x += self.speedx
        
        if self.rect.right > p.WIDHT: 
            self.rect.right = p.WIDHT
        if self.rect.left < 0:
            self.rect.left = 0
    def update_animacao(self): 
        agora = pygame.time.get_ticks()
        ticks_passados = agora - self.ultimo_frame
        if ticks_passados > self.frames_ticks and self.speedx > 0: 
            self.ultimo_frame = agora
            self.frame += 1
            self.image = self.i_animacao[self.frame % len(self.i_animacao)]
        elif ticks_passados > self.frames_ticks and self.speedx < 0:
            self.ultimo_frame = agora
            self.frame += 1
            self.image = self.i_animacao[self.frame % len(self.i_animacao)]
            self.image = pygame.transform.flip(self.image, True, False)
        if self.speedx == 0:
            self.image = self.i_animacao[0]
        