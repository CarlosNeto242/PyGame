import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
import random 
import Auxiliares as aux

def aviso(clock, tela, estado): 
    assets = a.carrega_assets()
    fonte = assets["fonte apertar inicial"]

    while estado["Aviso"]: 
        tela.fill((0, 0, 0))
        texto = fonte.render("O seu jogo foi desligado", True, (255, 255, 255))
        fonte_rect = texto.get_rect()
        fonte_rect.midtop = (p.WIDHT/2, p.HEIGHT/2)
        tela.blit(texto, fonte_rect)

        tela.fill((0, 0, 0))
        texto = fonte.render("Roube a energia de outros jogos para continuar vivo", True, (255, 255, 255))
        fonte_rect = texto.get_rect()
        fonte_rect.midtop = (p.WIDHT/2, p.HEIGHT/2 + 50)
        tela.blit(texto, fonte_rect)

        pygame.display.update()
        clock.tick(p.FPS)

        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                estado["Aviso"] = False
                estado["Jogando"] = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado["Aviso"] = False
                    estado["Jogando"] = True
        pygame.display.update()
        clock.tick(p.FPS)