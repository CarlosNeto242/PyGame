import pygame
import parametros as p
import assets as a

pygame.init()

def inicio(tela, clock, estado): 
    assets = a.carrega_assets()
    background = assets["imagem tela inicial"]
    background = pygame.transform.scale(background, (1920, 1080))
    fonte1 = assets["fonte apertar inicial"] 
    fonte2 =   assets["fonte titulo inicial"]
    while estado["Inicial"]: 
        tela.blit(background, (0, 0))
        fonte_tecla = fonte1.render("Clique espaço para começar", True, (0, 195, 255))
        fonte_rect1 = fonte_tecla.get_rect()
        fonte_rect1.midtop = (p.WIDHT/2, 800)
        tela.blit(fonte_tecla, fonte_rect1)
        fonte_titulo = fonte2.render(" Mega\nMan", True, (255, 255, 255) )
        fonte_rect2 = fonte_titulo.get_rect()
        fonte_rect2.midtop = (p.WIDHT - 1400, 200)
        tela.blit(fonte_titulo, fonte_rect2)
        eventos = pygame.event.get()

        for evento in eventos: 
            if evento.type == pygame.QUIT:
                estado["Inicial"] = False
                estado["Jogando"] = False 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado["Inicial"] = False
                    estado["Mapa"] = True

        pygame.display.update()
        clock.tick(p.FPS)