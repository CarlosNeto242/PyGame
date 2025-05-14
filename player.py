import pygame
import parametros as p
import assets as a
assets = a.carrega_assets()
class Player(pygame.sprite.Sprite):
    def __init__(self, grupos, assets):
        pygame.sprite.Sprite.__init__(self)

        self.i_animacao = assets
        self.frame = 0 
        self.image = self.i_animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = 900
        self.speedx = 0
        self.groups = grupos
        self.direcao = 1

        self.ultimo_frame = pygame.time.get_ticks()
        self.frames_ticks = 50

        self.ultimo_tiro = pygame.time.get_ticks() 
        self.tiro_ticks = 200

    def update_deslocar(self):
        self.rect.x += self.speedx
        
        if self.rect.right > p.WIDHT: 
            self.rect.right = p.WIDHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.speedx > 0:
            self.direcao = 1
        elif self.speedx < 0:
            self.direcao = -1

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
            if self.direcao == 1:
                self.image = self.i_animacao[0]
            else:
                self.image = self.i_animacao[0]
                self.image = pygame.transform.flip(self.image, True, False)
    def atirar(self):
        self.i_animacao = assets["animacao player atirando"]
        self.frame = 0
        self.image = self.i_animacao[self.frame]
        agora = pygame.time.get_ticks()
        elapsed_ticks = agora - self.ultimo_tiro
        if elapsed_ticks > self.tiro_ticks: 
            self.ultimo_tiro = agora
            novo_tiro = Tiro(self.rect.bottom - 140, self.rect.centerx, self.direcao)
            self.groups["tiros"].add(novo_tiro)
        
        if elapsed_ticks > self.frames_ticks and self.speedx > 0: 
            self.ultimo_frame = agora
            self.frame += 1
            self.image = self.i_animacao[self.frame % len(self.i_animacao)]
        elif elapsed_ticks > self.frames_ticks and self.speedx < 0:
            self.ultimo_frame = agora
            self.frame += 1
            self.image = self.i_animacao[self.frame % len(self.i_animacao)]
            self.image = pygame.transform.flip(self.image, True, False)
        
        

class Tiro(pygame.sprite.Sprite): 
    def __init__(self, bottom, centerx, direcao):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets["tiro player"]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom 

        self.speedx = 10 * direcao

    def update(self):
        self.rect.x += self.speedx

        if self.rect.x > p.WIDHT:
            self.kill()
    

        
        