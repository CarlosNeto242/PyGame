import pygame
import random

class Bloco(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(x, y))

class Cano(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(x, y))

class Bloco_Marro(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(x, y))

class Bloco_Interrogacao(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(x, y))

# Desenha a barra de vida do jogador
def desenhar_barra_vida_player(tela, player):
    largura = 200
    altura = 20
    x = 50
    y = 20
    vida_percent = player.vida / player.max_vida
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura))  # fundo vermelho
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura * vida_percent, altura))  # vida verde
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 3)  # borda

# Desenha a barra de vida do boss ativo
def desenhar_barra_vida_boss(tela, boss, camera_x):
    largura = 400
    altura = 30
    x = boss.rect.centerx - camera_x - largura // 2
    y = boss.rect.top - 50
    vida_percent = boss.vida / boss.max_vida
    pygame.draw.rect(tela, (100, 0, 0), (x, y, largura, altura))
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura * vida_percent, altura))
    pygame.draw.rect(tela, (255, 255, 255), (x, y, largura, altura), 3)
    fonte = pygame.font.SysFont("Arial", 24, bold=True)
    texto = fonte.render(f"{type(boss).__name__}", True, (255, 255, 255))
    tela.blit(texto, (x + largura // 2 - texto.get_width() // 2, y - 30))

