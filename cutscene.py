import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
import random 
import Auxiliares as aux

def animacao_cutscene(tela, clock, estado): 
    background = pygame.image.load("Sprites/megaman_inicial.jpg")
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))
    assets = a.carrega_assets()
    frames = 2000
    preto = pygame.Surface((16, 16))
    preto.fill((0, 0, 0))
    bloco_preto = aux.Bloco(0, 0, preto )
    tempo = 0
    while tempo <= frames:
        tempo += 1
        if tempo == frames:
            i = 0
            while i in range (0, 1820):
                tela.blit(bloco_preto.image,i, 0)
                i += 100
            tempo == 0  
    
    tela.blit(background, (0, 0))
    pygame.display.update()
    clock.tick(p.FPS)