import pygame
import parametros as p
import assets as a
import botao as b

def selecionar(tela, clock, estado):
    assets = a.carrega_assets()
    fonte = assets["fonte apertar inicial"]
    background = assets["background fliperama"]
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))

    espacamento = 400
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

    botao2 = b.Botao(assets, botoes, "Icon EggMan")
    botao2.rect.x = 3*x
    botao2.rect.centery = y

    while estado["Mapa"]: 
        tela.blit((background), (0, 0))
        for botao in botoes:
            tela.blit(botao.image, botao.rect)
        fonte1 = fonte.render("Selecione a fase desejada", True, (255, 255, 255))
        fonte_rect1 = fonte1.get_rect()
        fonte_rect1.midtop = (p.WIDHT/2, 800)
        tela.blit(fonte1, fonte_rect1)
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                estado["Mapa"] = False
                estado["Jogando"] = False
            if event.type == pygame.MOUSEMOTION: 
                for botao in botoes: 
                    if botao.rect.collidepoint(event.pos):
                        botao.image = pygame.transform.scale(botao.image, (300, 300))
                    else:
                        botao.image = pygame.transform.scale(botao.image, (200, 200))
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
                            estado["EggMan"] = True
                            estado["Mapa"] = False
        pygame.display.update()
        clock.tick(p.FPS)
