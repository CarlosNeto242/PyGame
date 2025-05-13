import pygame
import parametros as p

pygame.init()

def inicio(tela, clock, estado): 
    background = pygame.image.load("Sprites/megaman_inicial.jpg")
    background = pygame.transform.scale(background, (1920, 1080))
    fonte = pygame.font.Font("Fontes/PressStart2P.ttf", 50)
    while estado["Inicial"]: 
        tela.blit(background, (0, 0))
        fonte_printar = fonte.render("Clique espaço para começar", True, (0, 0, 0))
        fonte_rect = fonte_printar.get_rect()
        fonte_rect.midtop = (p.WIDHT/2, 800)
        tela.blit(fonte_printar, fonte_rect)
        eventos = pygame.event.get()

        for evento in eventos: 
            if evento == pygame.QUIT:
                estado["Inicial"] = False

        pygame.display.update()
        clock.tick(p.FPS)