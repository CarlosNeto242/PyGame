# carregando as bibliotecas e arquivos necessários para rodar os assets do jogo

import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
import random 
import Auxiliares as aux
# definimos a função para a tela de aviso
def aviso(clock, tela, estado): 
    # carregamos os assets necessários
    assets = a.carrega_assets()
    fonte_maior = pygame.font.Font("Fontes/PressStart2P.ttf", 25)
    imagem = assets["desligado"]
    imagem = pygame.transform.scale(imagem, (200, 200))
    imagem2 = assets["celula_energia"]
    imagem2 = pygame.transform.scale(imagem2, (200, 200))
    # colocamos esses na tela enquanto ela aparecer
    while estado["Aviso"]: 
        tela.fill((0, 0, 0))
        tela.blit(imagem, (800, 300))
        tela.blit(imagem2, (800, 650))
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
        # verificamos os eventos do pygame
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                estado["Aviso"] = False
                estado["Jogando"] = False
            if evento.type == pygame.KEYDOWN:
                    estado["Aviso"] = False
                    estado["Mario"] = True
        pygame.display.update()
        clock.tick(p.FPS)