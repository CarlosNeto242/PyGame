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
        self.som_tiro = assets["som_tiro"]
        self.som_tiroespecial = assets["som_tiroespecial"]
        self.tiro_especial_dano = 30
        self.tiro_especial_cooldown = 1  # segundos
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
        self.direcao = 1 # 1 para direita, -1 para esquerda
        self.pulando = False
        self.gravity = 900 # A gravidade agora é por pixel/segundo^2
        self.vida = 90000
        self.max_vida = 90000
        self.knockback_x = 0
        self.knockback_frames = 0
        self.pegou_flor = False
        self.invulneravel = False
        self.tempo_invulneravel = 0.0 # Tempo em segundos


        self.ultimo_frame = pygame.time.get_ticks()
        self.frames_ticks = 80

        self.ultimo_tiro = pygame.time.get_ticks() 
        self.tiro_ticks = 200 # milissegundos

    def knockback(self, forca):
        self.knockback_x = forca
        self.knockback_frames = 10 # Número de frames que o knockback dura

    def update_deslocar(self, limite_esquerdo, limite_direito, dt): # Adicionado dt
        if self.invulneravel:
            self.tempo_invulneravel -= dt # Usa dt para decrementar o tempo
            if self.tempo_invulneravel <= 0:
                self.invulneravel = False

        self.rect.x += self.speedx * dt # Multiplica por dt

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


    def update_deslocar_fixo(self, dt): # Adicionado dt
        # O movimento agora é baseado em pixels/segundo
        self.rect.x += self.speedx * dt 

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
            # A animação de pulo pode ter menos frames ou ser diferente
            # Certifique-se de que o índice do frame não exceda o tamanho da lista
            if ticks_passados > self.frames_ticks:
                self.ultimo_frame = agora
                if self.frame < len(self.animacao_pulo) - 1:
                    self.frame += 1

            # Garante que o índice nunca seja inválido
            frame_index = min(self.frame, len(self.animacao_pulo) - 1)
            frame_atual = self.animacao_pulo[frame_index]
            self.image = frame_atual if self.direcao == 1 else pygame.transform.flip(frame_atual, True, False)
            return
        
        # Animação de corrida
        if ticks_passados > self.frames_ticks and self.speedx != 0: # Só anima se estiver em movimento
            self.ultimo_frame = agora
            self.frame = (self.frame + 1) % len(self.i_animacao)
            frame_atual = self.i_animacao[self.frame]
            self.image = frame_atual if self.direcao == 1 else pygame.transform.flip(frame_atual, True, False)
        elif self.speedx == 0 and not self.pulando: # Volta para idle se parado e não pulando
            if self.direcao == 1:
                self.image = self.i_animacao[0]
            else:
                self.image = pygame.transform.flip(self.i_animacao[0], True, False)

    def atirar(self):
        # A animação de atirar deve ser temporária, não uma mudança permanente em i_animacao
        # Você pode criar uma animação separada para o tiro, ou apenas mudar para um frame de tiro
        # por um curto período. Por simplicidade, vou manter como está por enquanto, mas é algo a considerar.
        self.i_animacao = assets["animacao player atirando"]
        self.frame = 0 # Reinicia a animação de tiro
        self.image = self.i_animacao[self.frame] # Define a imagem inicial da animação de tiro

        agora = pygame.time.get_ticks()
        elapsed_ticks = agora - self.ultimo_tiro
        if elapsed_ticks > self.tiro_ticks: 
            self.ultimo_tiro = agora
            altura_do_tiro = self.rect.centery + 14
            # O tiro do player é adicionado ao grupo 'player_tiros'
            novo_tiro = Tiro(altura_do_tiro, self.rect.centerx, self.direcao, self.rect.x)
            self.groups["player_tiros"].add(novo_tiro) # Mudei aqui para o grupo correto
            self.som_tiro.play()
        
        # Esta parte da animação já está em update_animacao, não precisa repetir aqui
        # if elapsed_ticks > self.frames_ticks and self.speedx > 0: 
        #     self.ultimo_frame = agora
        #     self.frame += 1
        #     self.image = self.i_animacao[self.frame % len(self.i_animacao)]
        # elif elapsed_ticks > self.frames_ticks and self.speedx < 0:
        #     self.ultimo_frame = agora
        #     self.frame += 1
        #     self.image = self.i_animacao[self.frame % len(self.i_animacao)]
        #     self.image = pygame.transform.flip(self.image, True, False)


    def atirar_especial(self, pegou_flor):
        if not pegou_flor:
            return
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro_especial >= self.tiro_especial_cooldown * 1000: # Cooldown em ms
            self.ultimo_tiro_especial = agora
            # O tiro especial do player é adicionado ao grupo 'player_tiros'
            novo_tiro = TiroEspecial(self.rect.bottom, self.rect.centerx, self.direcao)
            self.groups["player_tiros"].add(novo_tiro) # Mudei aqui para o grupo correto
            self.som_tiroespecial.play()


    def update_gravidade(self, chao_y, dt): # Adicionado dt
        self.speedy += self.gravity * dt # Multiplica por dt
        self.rect.y += self.speedy * dt # Multiplica por dt

        if self.rect.bottom >= chao_y:
            self.rect.bottom = chao_y
            self.speedy = 0
            self.pulando = False
    
    def take_damage(self, dmg):
        if not self.invulneravel:
            self.vida -= dmg
            self.invulneravel = True
            self.tempo_invulneravel = 1.0 # 1 segundo de invulnerabilidade
            self.knockback( -150 if self.direcao > 0 else 150 ) # Força de knockback ajustada para dt

    def pular(self, forca): # Força de pulo agora é em pixels/segundo
        if not self.pulando:
            self.pulando = True
            self.frame = 0  # Reinicia animação de pulo
            self.ultimo_frame = pygame.time.get_ticks()
            self.speedy = -forca
        
# criando uma outra classe para o tiro do player, que será um sprite que se movimenta horizontalmente
class Tiro(pygame.sprite.Sprite): 
    def __init__(self, bottom, centerx, direcao, player_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets["tiro player"]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom 
        self.speedx = 500 * direcao # Ajustado para dt
        self.dano = 10 # Adicionado dano
        # self.player_x = player_x  # A posição do player não é mais relevante para o tiro sair da tela
                                    # se o tiro é removido quando sai da tela geral
    def update(self, dt): # Adicionado dt
        self.rect.x += self.speedx * dt

        # Remova o tiro quando ele sai da tela
        if self.rect.right < 0 or self.rect.left > p.WIDHT:
            self.kill()

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

        self.speedx = 400 * direcao # Ajustado para dt
        self.speedy = -400 # Ajustado para dt
        self.gravity = 1000 # Ajustado para dt
        self.bounces = 0
        self.max_bounces = 3
        self.chao_y = 801.5
        self.dano = 30 # Dano ajustado para ser mais razoável

        self.ultimo_frame = pygame.time.get_ticks()
        self.frame_intervalo = 100  # milissegundos por frame

    def update(self, dt): # Adicionado dt
        # Animação
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.frame_intervalo:
            self.ultimo_frame = agora
            self.frame = (self.frame + 1) % len(self.animacao)
            self.image = self.animacao[self.frame]

        # Movimento
        self.rect.x += self.speedx * dt
        self.speedy += self.gravity * dt
        self.rect.y += self.speedy * dt

        # Quicar no chão
        if self.rect.bottom >= self.chao_y:
            self.rect.bottom = self.chao_y
            self.speedy = -400 # Força do quique ajustada
            self.bounces += 1

        if self.bounces > self.max_bounces:
            self.kill()
        
        # Remover se sair da tela lateralmente
        if self.rect.right < 0 or self.rect.left > p.WIDHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y, assets):
        super().__init__()
        self.tipo = tipo
        self.image = assets[f"powerup_{tipo}"][0]  # primeiro frame
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speedy = -200 # Ajustado para dt
        self.gravity = 500 # Ajustado para dt

    def update(self, dt): # Adicionado dt
        self.speedy += self.gravity * dt
        self.rect.y += self.speedy * dt
        if self.rect.bottom > 801.5:
            self.rect.bottom = 801.5
            self.speedy = 0