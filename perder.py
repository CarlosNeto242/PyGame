import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b

pygame.init()

def gameover(tela, clock, estado): 
    assets = a.carrega_assets()
    background = assets["tela de gameover"]
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))
    fonte1 = assets["fonte apertar inicial"] 
    while estado["Perder"]: 
        tela.blit(background, (0, 0))
        fonte_tecla = fonte1.render("Clique espaço para recomeçar", True, (0, 195, 255))
        fonte_rect1 = fonte_tecla.get_rect()
        fonte_rect1.midtop = (p.WIDHT/2, 800)
        tela.blit(fonte_tecla, fonte_rect1)
        eventos = pygame.event.get()

        for evento in eventos: 
            if evento.type == pygame.QUIT:
                estado["Perder"] = False
                estado["Jogando"] = False 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado["Perder"] = False
                    estado["DK"] = True

        pygame.display.update()
        clock.tick(p.FPS)