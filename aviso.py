import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
import random 
import Auxiliares as aux

def aviso(clock, tela, estado): 
    assets = a.carrega_assets()
    fonte_maior = pygame.font.Font("Fontes/PressStart2P.ttf", 25)

    while estado["Aviso"]: 
        tela.fill((0, 0, 0))
        texto = fonte_maior.render("O seu jogo foi desligado", True, (255, 255, 255))
        fonte_rect = texto.get_rect()
        fonte_rect.midtop = (p.WIDHT/2, p.HEIGHT/2)
        tela.blit(texto, fonte_rect)

        texto = fonte_maior.render("Roube a energia de outros jogos para continuar vivo", True, (255, 255, 255))
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
                    estado["Aviso"] = False
                    estado["Mapa"] = True
        pygame.display.update()
        clock.tick(p.FPS)