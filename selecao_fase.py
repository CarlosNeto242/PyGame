import pygame
import parametros as p
import assets as a
import botao as b

def selecionar(tela, clock, estado):
    assets = a.carrega_assets()
    espacamento = 300 
    x = espacamento
    y = 500
    botoes = pygame.sprite.Group()
    # Carregando os assets necessários para a tela de seleção
    botao0 = b.Botao(assets, botoes, "Icon DK")
    botao0.rect.x = x
    botao0.rect.centery = y
    
    botao1 = b.Botao(assets, botoes, "Icon Bowser")
    botao1.rect.x = 2*x
    botao1.rect.centery = y

    botao2 = b.Botao(assets, botoes, "Icon PacMan")
    botao2.rect.x = 3*x
    botao2.rect.centery = y

    while estado["Mapa"]: 
        tela.fill((0, 0, 0))
        for botao in botoes:
            tela.blit(botao.image, botao.rect)
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                estado["Mapa"] = False
                estado["Jogando"] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for botao in botoes: 
                    if botao.rect.collidepoint(event.pos):
                        if botao.nome_da_fase == "Icon DK":
                            estado["DK"] = True
                            estado["Mapa"] = False
                        elif botao.nome_da_fase == "Icon Bowser":
                            estado["Bowser"] = True
                            estado["Mapa"] = False
                        elif botao.nome_da_fase == "Icon PacMan": 
                            estado["PacMan"] = True
                            estado["Mapa"] = False
        pygame.display.update()
        clock.tick(p.FPS)
