import pygame
import parametros as p
import assets as a

def selecionar(tela, clock, estado): 
    # começamos chamando o tela de fundo inicial do assets e configurando seus parâmetros
    assets = a.carrega_assets()
    background = assets["imagem tela inicial"]
    icon_DK = assets["Icon DK"]
    icon_groups = pygame.sprite.Group()
    icon_groups.add(icon_DK)
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))
    # em seguida, chamamos a fontes usadas no texto da tela inicial
    fonte1 = assets["fonte apertar inicial"] 
    while estado["Mapa"]: 
        # desenhamos o background na tela
        tela.blit(background, (0, 0))
        # desenhamos o texto na tela
        texto = fonte1.render("Selecione a fase", True, (255, 255, 255))
        tela.blit(texto, (p.WIDHT // 2 - texto.get_width() // 2, p.HEIGHT // 2 - texto.get_height() // 2))
        # desenhamos o ícone do DK na tela
        icon_groups.draw(tela)
        icon_groups.update()
        # analisamos os eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["Mapa"] = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    estado["DK"] = True
                    estado["Mapa"] = False
                elif evento.key == pygame.K_ESCAPE:
                    estado["Jogando"] = False
                    estado["Mapa"] = False
    pygame.display.update()
    clock.tick(p.FPS)
