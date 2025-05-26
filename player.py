# importamos as bibliotecas e arquivos necessários para montar a tela inicial
import pygame
import parametros as p
import assets as a
# carregamos os assetas para usar nas classes
assets = a.carrega_assets()
# a primeira classe criada se refere ao player 
class Player(pygame.sprite.Sprite):
    def __init__(self, grupos, assets):
        pygame.sprite.Sprite.__init__(self)

        self.i_animacao = assets["animacao player"]  
        # self.som_tiro = assets["som_tiro"]
        self.som_tiroespecial = assets["som_tiroespecial"]
        self.tiro_especial_dano = 30
        self.tiro_especial_cooldown = 3000
        self.ultimo_tiro_especial = pygame.time.get_ticks()
        # self.som_tiro.set_volume(0.5)
        self.frame = 0 
        self.animacao_pulo = assets["animacao pulo"]
        self.image = self.i_animacao[self.frame]
        self.som_tiro = assets["som_tiro"]
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
        self.knockback_x = 0
        self.knockback_frames = 0


        self.ultimo_frame = pygame.time.get_ticks()
        self.frames_ticks = 50

        self.ultimo_tiro = pygame.time.get_ticks() 
        self.tiro_ticks = 200

    def update_deslocar(self, limite_esquerdo, limite_direito):
        self.rect.x += self.speedx

        if self.knockback_frames > 0:
            self.rect.x += self.knockback_x
            self.knockback_frames -= 1

        if self.rect.right > limite_direito: 
            self.rect.right = limite_direito
        if self.rect.left < limite_esquerdo:
            self.rect.left = limite_esquerdo   
        if self.speedx > 0:
            self.direcao = 1
        elif self.speedx < 0:
            self.direcao = -1

    def update_deslocar_fixo(self):
        self.rect.x += self.speedx

        if self.knockback_frames > 0:
            self.rect.x += self.knockback_x
            self.knockback_frames -= 1
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
            novo_tiro = Tiro(altura_do_tiro, self.rect.centerx, self.direcao, self.rect.x)
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

    def atirar_especial(self,pegou_flor):
        if not pegou_flor:
            return
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro_especial >= self.tiro_especial_cooldown:
            self.ultimo_tiro_especial = agora
            novo_tiro = TiroEspecial(self.rect.bottom, self.rect.centerx, self.direcao)
            self.groups["tiros"].add(novo_tiro)
            self.som_tiroespecial.play()

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
        
# criando uma outra classe para o tiro do player, que será um sprite que se movimenta horizontalmente
class Tiro(pygame.sprite.Sprite): 
    def __init__(self, bottom, centerx, direcao, player_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets["tiro player"]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom 
        self.speedx = 15 * direcao
        self.player_x = player_x  # salva posição do player no momento do tiro

    def update(self):
        self.rect.x += self.speedx

        if self.rect.x > self.player_x + p.WIDHT or self.rect.x < self.player_x - p.WIDHT:
            self.kill()

            print("Tiro saiu da tela")

# criando uma classe para o tiro especial do player, que será um sprite que se movimenta horizontalmente e quica no chão  
class TiroEspecial(pygame.sprite.Sprite):
    def __init__(self, bottom, centerx, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.animacao = assets["animacao fogo"]
        self.frame = 0
        self.image = self.animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom

        self.speedx = 10 * direcao
        self.speedy = -10
        self.gravity = 0.5
        self.bounces = 0
        self.max_bounces = 3
        self.chao_y = 801.5
        self.dano = 30

        self.ultimo_frame = pygame.time.get_ticks()
        self.frame_intervalo = 100  # milissegundos por frame

    def update(self):
        # Animação
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.frame_intervalo:
            self.ultimo_frame = agora
            self.frame = (self.frame + 1) % len(self.animacao)
            self.image = self.animacao[self.frame]

        # Movimento
        self.rect.x += self.speedx
        self.speedy += self.gravity
        self.rect.y += self.speedy

        # Quicar no chão
        if self.rect.bottom >= self.chao_y:
            self.rect.bottom = self.chao_y
            self.speedy = -10
            self.bounces += 1

        if self.bounces > self.max_bounces:
            self.kill()


        
        