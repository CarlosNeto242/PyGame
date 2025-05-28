# importamos as bibliotecas e arquivos necessários para criar os bosses do jogo
import pygame
import parametros as p
import player as pl 
import random
import math

# Criando uma classe para o boss Donkey Kong
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
        self.tacada_ticks = 1000
        self.ultimo_ataque_chuva = pygame.time.get_ticks()
        self.intervalo_chuva = random.randint(300, 1000)
    
    def update_tiro(self): # atualiza a animação do barril jogado pelo Donkey Kong
        agora = pygame.time.get_ticks()
        tipo_barril = random.choice(["normal", "especial"])
        ticks_passados = agora - self.ultima_tacada
        if ticks_passados > self.tacada_ticks:
            self.ultima_tacada = agora
            self.image = self.assets['boss jogando barril'] 
            altura_do_barril = self.rect.bottom + 15
            novo_barril = Barril(altura_do_barril, self.rect.centerx, self.assets, tipo_barril)
            self.groups["barris"].add(novo_barril)
        if 500 < ticks_passados < 1000: 
            self.image = self.assets["chefe idle"]
    
    def levar_dano(self, dano): # atualiza a vida do Donkey Kong
        self.vida -= dano
        if self.vida <= 0:
            self.kill()

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

# Criando uma classe para os barris atirados pelo Donkey Kong
class Barril(pygame.sprite.Sprite): 
    def __init__(self, bottom, centerx, assets, tipo_do_barril):
        pygame.sprite.Sprite.__init__(self)
        if tipo_do_barril == "normal":
            self.animacao = assets["barril rolando"]
        else: 
            self.animacao = assets["barril especial"]
        self.frame = 0
        self.image = self.animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom 
        self.tipo_do_barril = tipo_do_barril
        if tipo_do_barril == "especial":
            self.speedx = random.uniform(-17, -12)           
            self.speedy = random.uniform(-25, -18)          
            self.gravity = random.uniform(0.4, 0.7)         
        else:
            self.speedx = -8
            self.speedy = 0
            self.gravity = 0.6
        self.ultimo_frame = pygame.time.get_ticks() 
        self.frame_ticks = 50
        
    def update_posicao(self):
        if self.tipo_do_barril == "normal":
            self.rect.x += self.speedx

            if self.rect.x > p.WIDHT:
                self.kill()
        elif self.tipo_do_barril == "especial":
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.bottom == 0:
                self.rect.bottom = 0
                self.speedy = 0
            else:
                self.speedy += self.gravity

            if self.rect.x > p.WIDHT or self.rect.y > p.HEIGHT:
                self.kill()
            
    def update_animacao(self): 
        if self.tipo_do_barril == "normal":
            agora = pygame.time.get_ticks()
            ticks_passados = agora - self.ultimo_frame
            if ticks_passados > self.frame_ticks:
                self.ultimo_frame = agora
                self.frame += 1
                self.image = self.animacao[self.frame % len(self.animacao)]
        agora = pygame.time.get_ticks()
        ticks_passados = agora - self.ultimo_frame
        if ticks_passados > self.frame_ticks:
            self.ultimo_frame = agora
            self.frame += 1
            self.image = self.animacao[self.frame % len(self.animacao)]
    def update(self):
        self.update_animacao()
        self.update_posicao()

# criamos uma classe para o fogo que cai do céu na fase do Donkey Kong
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

# criando uma classe para o boss do Bowser
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

# Criando uma classe para a bola de fogo que o Bowser atira
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

# Criando uma classe para a flor de fogo que o Bowser atira
class FlorDeFogo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Chefes/flor_de_fogo.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

# criando uma classe para os inimigos na fase do Bowser
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
# Subclasses específicas para os inimigos da fase do Bowser
# --------------------------


class Goomba(pygame.sprite.Sprite):
    def __init__(self, assets, x, y):
        super().__init__()
        self.animacao = assets["goomba"]
        self.frame = 0
        self.image = self.animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speedx = -2
        self.dano = 10
        self.ultimo_frame = pygame.time.get_ticks()
        self.intervalo = 250

    def update(self):
        self.rect.x += self.speedx
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.intervalo:
            self.ultimo_frame = agora
            self.frame = (self.frame + 1) % len(self.animacao)
            self.image = self.animacao[self.frame]

class Koopa(pygame.sprite.Sprite):
    def __init__(self, assets, x, y):
        super().__init__()
        self.estado = "vivo"
        self.animacoes = {
            "koopa": assets["koopa"],
            "casco": assets["casco"]
        }
        self.frame = 0
        self.image = self.animacoes["koopa"][self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speedx = -1.5
        self.dano = 15
        self.ultimo_frame = pygame.time.get_ticks()
        self.frame_interval = 150  # animação mais rápida
        self.direcao = -1

    def update(self):
        agora = pygame.time.get_ticks()
        if self.estado == "vivo":
            self.rect.x += self.speedx
            if agora - self.ultimo_frame > self.frame_interval:
                self.ultimo_frame = agora
                self.frame = (self.frame + 1) % len(self.animacoes["koopa"])
                self.image = self.animacoes["koopa"][self.frame]

        elif self.estado == "casco_andando":
            self.rect.x += 10 * self.direcao
            if agora - self.ultimo_frame > self.frame_interval:
                self.ultimo_frame = agora
                self.frame = (self.frame + 1) % len(self.animacoes["casco"])
                self.image = self.animacoes["casco"][self.frame]
            if self.rect.right < 0 or self.rect.left > 21000:
                self.kill()

        elif self.estado == "casco_parado":
            self.image = self.animacoes["casco"][0]

    def levar_pulo(self, player):
        if self.estado == "vivo":
            self.estado = "casco_parado"
            bottom = self.rect.bottom
            x = self.rect.x
            self.image = self.animacoes["casco"][0]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.x = x
            player.speedy = -18

        elif self.estado == "casco_parado":
            self.estado = "casco_andando"
            self.direcao = 1 if player.rect.centerx < self.rect.centerx else -1
            player.speedy = -18



class PlantaCarnivora(pygame.sprite.Sprite):
    def __init__(self, assets, x, y):
        super().__init__()
        self.animacao = assets["planta"]
        self.frame = 0
        self.image = self.animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.dano = 25
        self.ultimo_frame = pygame.time.get_ticks()
        self.intervalo = 250

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.intervalo:
            self.ultimo_frame = agora
            self.frame = (self.frame + 1) % len(self.animacao)
            self.image = self.animacao[self.frame]


class PlantaCarnivora(Inimigo):
    def __init__(self, assets, x, y):
        super().__init__(assets["planta"], x, y, speedx=0)
        self.dano = 25

class KingBoo(pygame.sprite.Sprite):
    def __init__(self, assets, grupos):
        pygame.sprite.Sprite.__init__(self)
        self.animacao = assets["king boo"]
        self.frame = 0
        self.image = self.animacao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = 1500
        self.rect.centery = 400
        self.assets = assets
        self.groups = grupos
        
        self.vida = 120
        self.max_vida = 120
        self.velocidade = 3
        self.estado = "voando"
        self.tempo_estado = pygame.time.get_ticks()
        self.intervalo_estado = 3000
        self.ultimo_ataque = pygame.time.get_ticks()
        self.intervalo_ataque = 1500
        self.ultimo_frame = pygame.time.get_ticks()
    
    def update(self, player):
        agora = pygame.time.get_ticks()
        
        # Máquina de estados
        if agora - self.tempo_estado > self.intervalo_estado:
            self.tempo_estado = agora
            if self.estado == "voando":
                self.estado = random.choice(["atacando", "invisivel"])
            else:
                self.estado = "voando"
                self.image = self.animacao[self.frame]
                self.rect = self.image.get_rect(center=self.rect.center)
        
        # Comportamentos
        if self.estado == "voando":
            self.voar(player)
            self.atacar(player)
        elif self.estado == "atacando":
            self.ataque_raio()
        
        # Animação
        if self.estado != "invisivel":
            self.atualizar_animacao()
    
    def voar(self, player):
        tempo = pygame.time.get_ticks() / 1000
        self.rect.centerx = 1500 + 200 * math.sin(tempo * 0.5)
        self.rect.centery = 400 + 100 * math.sin(tempo)
    
    def atacar(self, player):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque > self.intervalo_ataque:
            self.ultimo_ataque = agora
            self.lancar_bolas_fantasmas()
    
    def lancar_bolas_fantasmas(self):
        for _ in range(3):
            angulo = random.uniform(0, 2 * math.pi)
            velocidade = random.uniform(3, 6)
            bola = BolaFantasma(self.rect.centerx, self.rect.centery, 
                               math.cos(angulo) * velocidade, 
                               math.sin(angulo) * velocidade)
            self.groups["projeteis_inimigos"].add(bola)
    
    def ataque_raio(self):
        if pygame.time.get_ticks() - self.ultimo_ataque > 500:
            self.ultimo_ataque = pygame.time.get_ticks()
            raio = RaioEletrico(self.rect.centerx, self.rect.bottom)
            self.groups["projeteis_inimigos"].add(raio)
    
    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > 100:
            self.ultimo_frame = agora
            self.frame = (self.frame + 1) % len(self.animacao)
            self.image = self.animacao[self.frame]
    
    def levar_dano(self, dano):
        if self.estado != "invisivel":
            self.vida -= dano
            if self.vida <= 0:
                self.kill()
                estrela = ItemEstrela(self.rect.centerx, self.rect.centery)
                self.groups["itens"].add(estrela)

class BolaFantasma(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (200, 200, 255, 200), (15, 15), 15)
        self.rect = self.image.get_rect(center=(x, y))
        self.speedx = speedx
        self.speedy = speedy
        self.tempo_vida = 120
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.tempo_vida -= 1
        if self.tempo_vida <= 0:
            self.kill()

class RaioEletrico(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 800), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (100, 255, 255, 150), (0, 0, 20, 800))
        self.rect = self.image.get_rect(midtop=(x, y))
        self.tempo_vida = 30
    
    def update(self):
        self.tempo_vida -= 1
        if self.tempo_vida <= 0:
            self.kill()

class BowserJr(pygame.sprite.Sprite):
    def __init__(self, assets, grupos):
        pygame.sprite.Sprite.__init__(self)
        self.animacoes = {
            "andando": assets["bowser jr andando"],
            "atacando": assets["bowser jr atacando"],
            "shell": assets["bowser jr shell"]
        }
        self.estado = "andando"
        self.image = self.animacoes[self.estado][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = 1400
        self.rect.bottom = 800
        
        self.vida = 150
        self.max_vida = 150
        self.speedx = -3
        self.direcao = -1
        self.contador_ataques = 0
        self.ultimo_ataque = pygame.time.get_ticks()
        self.intervalo_ataque = 2000
        self.groups = grupos
        self.frame = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.frame_interval = 100
    
    def update(self, player):
        self.movimentar()
        self.atacar(player)
        self.atualizar_animacao()
        
        hits = pygame.sprite.collide_rect(self, player)
        if hits and self.estado != "shell":
            player.vida -= 10
            player.knockback(15 if self.rect.centerx < player.rect.centerx else -15)
    
    def movimentar(self):
        if self.estado == "shell":
            self.speedx = 8 * self.direcao
            self.rect.x += self.speedx
            
            if self.rect.right < 0 or self.rect.left > p.WIDHT:
                self.estado = "andando"
                self.speedx = -3
        else:
            self.rect.x += self.speedx
            if self.rect.left < 1000:
                self.rect.left = 1000
                self.speedx = 3
                self.direcao = 1
            elif self.rect.right > 1700:
                self.rect.right = 1700
                self.speedx = -3
                self.direcao = -1
    
    def atacar(self, player):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque > self.intervalo_ataque:
            self.ultimo_ataque = agora
            self.contador_ataques += 1
            
            if self.contador_ataques % 3 == 0:
                self.estado = "shell"
                self.direcao = -1 if player.rect.centerx < self.rect.centerx else 1
            else:
                self.estado = "atacando"
                self.lancar_martelo()
    
    def lancar_martelo(self):
        martelo = Martelo(self.rect.centerx, self.rect.top, self.direcao)
        self.groups["projeteis_inimigos"].add(martelo)
    
    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.frame_interval:
            self.ultimo_frame = agora
            animacao = self.animacoes[self.estado]
            self.frame = (self.frame + 1) % len(animacao)
            self.image = animacao[self.frame]
    
    def levar_dano(self, dano):
        if self.estado != "shell":
            self.vida -= dano
            if self.vida <= 0:
                self.kill()
            elif self.vida < self.max_vida / 3:
                self.intervalo_ataque = 1000

class Martelo(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (150, 75, 0), (20, 20), 20)
        self.rect = self.image.get_rect(center=(x, y))
        self.direcao = direcao
        self.speedx = 5 * direcao
        self.speedy = -5
        self.gravity = 0.3
        self.rotation = 0
        self.rotation_speed = 10 * direcao
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.speedy += self.gravity
        # self.rotation += self.rotation_speed
        # self.image = pygame.transform.rotate(self.image, self.rotation)
        
        if self.rect.top > p.HEIGHT:
            self.kill()

class ItemEstrela(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 255, 0), [
            (15, 0), (20, 15), (30, 15),
            (22, 22), (27, 32), (15, 25),
            (3, 32), (8, 22), (0, 15),
            (10, 15)
        ])
        self.rect = self.image.get_rect(center=(x, y))
        self.tempo_vida = 300
    
    def update(self):
        self.tempo_vida -= 1
        if self.tempo_vida <= 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y, assets):
        super().__init__()
        self.tipo = tipo
        self.image = assets[f"powerup_{tipo}"][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speedy = -5
        self.gravity = 0.5

    def update(self):
        self.speedy += self.gravity
        self.rect.y += self.speedy
        if self.rect.bottom > 801.5:
            self.rect.bottom = 801.5
            self.speedy = 0

