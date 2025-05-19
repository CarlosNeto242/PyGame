import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b

pygame.init()

def win(tela, clock, estado): 
    assets = a.carrega_assets()
    background = assets["tela de vitória"]
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))
    assets["fonte apertar inicial"] = pygame.font.Font("Fontes/PressStart2P.ttf", 30)
    fonte1 = assets["fonte apertar inicial"]
    while estado["Ganhar"]: 
        tela.blit(background, (0, 0))
        fonte_tecla = fonte1.render("Clique espaço para avançar para próxima fase", True, (0, 195, 255))
        fonte_rect1 = fonte_tecla.get_rect()
        fonte_rect1.midtop = (p.WIDHT/2, 800)
        tela.blit(fonte_tecla, fonte_rect1)
        eventos = pygame.event.get()

        for evento in eventos: 
            if evento.type == pygame.QUIT:
                estado["Ganhar"] = False
                estado["Jogando"] = False 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado["Ganhar"] = False

        pygame.display.update()
        clock.tick(p.FPS)