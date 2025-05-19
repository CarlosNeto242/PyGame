import pygame
import parametros as p
import assets as a

class Botao(pygame.sprite.Sprite): 
    def __init__(self, assets, grupos, nome_da_fase):
    
        pygame.sprite.Sprite.__init__(self)

        self.assets = assets
        self.nome_da_fase = nome_da_fase
        self.image = assets[nome_da_fase]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0
