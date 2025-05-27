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
    bloco_preto.image = pygame.transform.scale(bloco_preto.image, (p.WIDHT, p.HEIGHT))
    tempo = 0

    while estado["Cutscene"]: 
        tela.blit(background, (0, 0))
        pygame.display.update()
        clock.tick(p.FPS)
        for i in range(5):
            tela.blit(bloco_preto.image, (0, 0))
            pygame.display.update()
            pygame.time.delay(300)
            tela.blit(background, (0, 0))
            pygame.display.update()
            pygame.time.delay(200)
            estado["Cutscene"] = False
            estado["Aviso"] = True