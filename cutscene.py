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
    bloco_preto = aux.Bloco(0, 0, assets["bloco preto"])
    bloco_preto.image = pygame.transform.scale(bloco_preto.image, (100, 100))
    tempo = 0

    while tempo <= frames:
        tela.blit(background, (0, 0))
        pygame.display.update()
        clock.tick(p.FPS)
        tempo += 1

    # Depois do loop principal, exibir os blocos pretos
    for i in range(0, p.WIDHT, 100):
        tela.blit(bloco_preto.image, (i, 0))
    pygame.display.update()