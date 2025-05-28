# importamos as bibliotecas e arquivos necessários para criar a tela de selação de fase do jogo

import pygame
import parametros as p
import assets as a
import botao as b

# criando uma função que irá rodar a tela de seleção de fase do jogo
def selecionar(tela, clock, estado):
    # carregando os assets principais que vão compor a tela (músicas, sprites...)
    pygame.mixer.music.load('Sprites/Sound Effects/bgm_action_2.mp3')
    pygame.mixer.music.play(loops=-1)
    assets = a.carrega_assets()
    fonte = assets["fonte apertar inicial"]
    background = assets["background fliperama"]
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))
    # definindo o espaçamento entre os botões para selecionar a fase
    espacamento = 400
    x = espacamento
    y = 500
    botoes = pygame.sprite.Group()
    # criando os botões que serão usados para selecionar as fases
    botao0 = b.Botao(assets, botoes, "Icon DK")
    botao0.rect.x = x
    botao0.rect.centery = y
    
    botao1 = b.Botao(assets, botoes, "Icon Bowser")
    botao1.rect.x = x + 800
    botao1.rect.centery = y
    # enquanto a tela de seleção de fase estiver ativa
    while estado["Mapa"]: 
        # todos os assets serão atualizados e desenhados na tela
        tela.blit((background), (0, 0))
        for botao in botoes:
            tela.blit(botao.image, botao.rect)
        fonte1 = fonte.render("Selecione o jogo para invadir", True, (255, 255, 255))
        fonte_rect1 = fonte1.get_rect()
        fonte_rect1.midtop = (p.WIDHT/2, 800)
        tela.blit(fonte1, fonte_rect1)
        # analisando as possíveis ações do usuário na tela de seleção de fase
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
                            estado["Mario"] = True
                            estado["Mapa"] = False
                        pygame.mixer.music.stop()
        # por fim, atualizamos a cada momento o jogo e determinamos sua taxa de atualizacao
        pygame.display.update()
        clock.tick(p.FPS)
