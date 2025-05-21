import pygame
import parametros as p
import tela_inicial 
import bosses
import Fase_dk
import perder 
import ganhar
import ctypes
import fase_bowser
import selecao_fase

class Bloco(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(x, y))