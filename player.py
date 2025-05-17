import pygame
import parametros as p
import assets as a
assets = a.carrega_assets()
class Player(pygame.sprite.Sprite):
    def __init__(self, grupos, assets):
        pygame.sprite.Sprite.__init__(self)

        self.i_animacao = assets["animacao player"]  
        self.som_tiro = assets["som_tiro"]
        self.tiro_especial_img = pygame.transform.scale(assets["tiro player"], (60, 30))  # pode mudar depois
        self.tiro_especial_dano = 30
        self.tiro_especial_cooldown = 3000
        self.ultimo_tiro_especial = pygame.time.get_ticks()
        self.som_tiro.set_volume(0.5)
        self.frame = 0 
        self.animacao_pulo = assets["animacao pulo"]
        self.image = self.i_animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = 900
        self.speedx = 0
        self.speedy = 0
        self.groups = grupos
        self.direcao = 1
        self.pulando = False
        self.gravity = 0.8
        self.vida = 100
        self.max_vida = 100

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
        if self.pulando:
            if ticks_passados > self.frames_ticks:
                self.ultimo_frame = agora
                self.frame += 1
            frame_atual = self.animacao_pulo[self.frame % len(self.animacao_pulo)]
            self.image = frame_atual if self.direcao == 1 else pygame.transform.flip(frame_atual, True, False)
            return
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
            altura_do_tiro = self.rect.centery + 14
            novo_tiro = Tiro(altura_do_tiro, self.rect.centerx, self.direcao)
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

        self.som_tiro.play()

    def atirar_especial(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro_especial >= self.tiro_especial_cooldown:
            self.ultimo_tiro_especial = agora
            altura_do_tiro = self.rect.centery + 14
            novo_tiro = TiroEspecial(altura_do_tiro, self.rect.centerx, self.direcao, self.tiro_especial_img)
            self.groups["tiros"].add(novo_tiro)

    def update_gravidade(self, chao_y):
        self.speedy += self.gravity
        self.rect.y += self.speedy

        if self.rect.bottom >= chao_y:
            self.rect.bottom = chao_y
            self.speedy = 0
            self.pulando = False

    def pular(self):
        if not self.pulando:
            self.speedy = -21
            self.pulando = True
        
        

class Tiro(pygame.sprite.Sprite): 
    def __init__(self, bottom, centerx, direcao):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets["tiro player"]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom 

        self.speedx = 15 * direcao

    def update(self):
        self.rect.x += self.speedx

        if self.rect.x > p.WIDHT:
            self.kill()
    
class TiroEspecial(pygame.sprite.Sprite):
    def __init__(self, bottom, centerx, direcao, imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedx = 20 * direcao
        self.dano = 30

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0 or self.rect.left > p.WIDHT:
            self.kill()
        
        