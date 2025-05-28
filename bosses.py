# importamos as bibliotecas e arquivos necessários para criar os bosses do jogo
import pygame
import parametros as p
import player as pl 
import random
import math
from pygame.sprite import Sprite

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

    def ataque_chuva(self, intervalo1, intervalo2, n): 
        agora = pygame.time.get_ticks()
        passados = agora - self.ultimo_ataque_chuva
        if passados >= self.intervalo_chuva: 
            self.ultimo_ataque_chuva = agora
            for _ in range(n):
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

class Bowser(Sprite):
    def __init__(self, assets, grupos):
        super().__init__()
        self.assets = assets
        self.grupos = grupos

        # Animação idle ⬅ lista de Surfaces em assets["bowser_idle"]
        self.frames_idle = assets.get("bowser_idle", [])
        self.frame_idx = 0
        self.image = self.frames_idle[self.frame_idx]
        self.rect = self.image.get_rect(midbottom=(grupos["room_width"] - 200, grupos["ground_y"]))

        # Vida
        self.max_vida = 300
        self.vida = self.max_vida

        # Controle de invulnerabilidade após hit
        self.invul = False
        self.invul_timer = 0.0

        # Cooldowns de ataque
        self.attack_cd = 0.0
        self.attack_phase = 0

    def update(self, player, dt):
        # Animação idle
        self.frame_idx = (self.frame_idx + 5 * dt) % len(self.frames_idle)
        self.image = self.frames_idle[int(self.frame_idx)]

        # Atualiza invulnerabilidade
        if self.invul:
            self.invul_timer -= dt
            if self.invul_timer <= 0:
                self.invul = False

        # Gerencia ataques
        self.attack_cd -= dt
        if self.attack_cd <= 0:
            self.attack_phase = (self.attack_phase + 1) % 3
            if self.attack_phase == 0:
                self._fireballs()
            elif self.attack_phase == 1:
                self._ground_slam()
            else:
                self._flame_breath(player)
            self.attack_cd = 2.0  # 2s entre padrões

    def take_damage(self, dmg):
        if not self.invul:
            self.vida = max(0, self.vida - dmg)
            self.invul = True
            self.invul_timer = 1.0  # 1s de invulnerabilidade

    # --- ATAQUES ---

    def _fireballs(self, count=5, speed=220):
        tex = self.assets.get("bowser_fireball")
        for i in range(count):
            angle = random.uniform(-0.5, 0.5)
            fb = Fireball(tex, speed, self.rect.center, angle, self.grupos)
            self.grupos["projectiles"].add(fb)

    def _ground_slam(self):
        slam = GroundSlam(self.rect.midbottom, self.grupos)
        self.grupos["projectiles"].add(slam)

    def _flame_breath(self, player):
        tex = self.assets.get("bowser_flame")
        breath = FlameBreath(tex, self.rect.midright, player.rect.center, self.grupos)
        self.grupos["projectiles"].add(breath)


class Fireball(Sprite):
    def __init__(self, image, speed, origin, angle, grupos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=origin)
        self.speed = speed
        self.dx = -1 + angle
        self.dy = angle
        self.dmg = 8
        self.grupos = grupos

    def update(self, dt):
        self.rect.x += int(self.dx * self.speed * dt)
        self.rect.y += int(self.dy * self.speed * dt)
        if (self.rect.right < 0 or self.rect.left > self.grupos["room_width"] or 
            self.rect.top > self.grupos["room_height"] or self.rect.bottom < 0):
            self.kill()


class GroundSlam(Sprite):
    def __init__(self, origin, grupos):
        super().__init__()
        self.image = pygame.Surface((self.groups["room_width"], 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 100, 0, 200), self.image.get_rect())
        self.rect = self.image.get_rect(midtop=(origin[0], origin[1] - 10))
        self.timer = 0.5
        self.dmg = 15
        self.grupos = grupos

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()


class FlameBreath(Sprite):
    def __init__(self, image, origin, target, grupos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midleft=origin)
        self.speed = 300
        self.target = target
        self.dmg = 12
        self.grupos = grupos

    def update(self, dt):
        # avança reto em direção ao player
        dir_vec = pygame.math.Vector2(self.target) - pygame.math.Vector2(self.rect.topleft)
        if dir_vec.length() != 0:
            dir_vec = dir_vec.normalize()
        self.rect.x += int(dir_vec.x * self.speed * dt)
        self.rect.y += int(dir_vec.y * self.speed * dt)
        if not pygame.Rect(0, 0, self.grupos["room_width"], self.grupos["room_height"]).colliderect(self.rect):
            self.kill()