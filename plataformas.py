import pygame
import random

class Bloco(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(x, y))
        self.solid = True  # Pode ser usado para plataformas que não são sólidas

class PlataformaMovel(Bloco):
    def __init__(self, x, y, imagem, limite_esquerdo, limite_direito, speed=2):
        super().__init__(x, y, imagem)
        self.limite_esquerdo = limite_esquerdo
        self.limite_direito = limite_direito
        self.speed = speed
        self.direcao = 1  # 1 para direita, -1 para esquerda
    
    def update(self):
        self.rect.x += self.speed * self.direcao
        if self.rect.right > self.limite_direito:
            self.direcao = -1
        elif self.rect.left < self.limite_esquerdo:
            self.direcao = 1

class PlataformaQuebravel(Bloco):
    def __init__(self, x, y, imagem):
        super().__init__(x, y, imagem)
        self.resistencia = 3
        self.pisando = False
        self.tempo_pisado = 0 

    def update(self):
        if self.pisando:
            if pygame.time.get_ticks() - self.tempo_pisado > 1000:  # 1 segundo pisando
                self.atingida()
            self.pisando = False  # reseta a flag a cada frame

    def atingida(self):
        self.resistencia -= 1
        if self.resistencia <= 0:
            self.kill()
