import pygame
import parametros as p

pygame.init()

def inicio(tela, clock, estado): 
    background = pygame.image.load("Sprites/megaman_inicial.jpg")
    background = pygame.transform.scale(background, (2880, 1800))
    while estado["Inicial"]: 
        tela.blit(background, (0, 0))
        eventos = pygame.event.get()

        for evento in eventos: 
            if evento == pygame.QUIT:
                estado["Inicial"] = False

        pygame.display.update()
        clock.tick(p.FPS)