# importamos as bibliotecas e arquivos necessários para montar a tela inicial
import pygame
import parametros as p
import assets as a

pygame.init()

# definindo uma função responsável por montar a tela inicial (será posteriormente chamada no loop principal)
def inicio(tela, clock, estado):
    pygame.mixer.music.load('Sprites/Sound Effects/bgm_action_1.mp3')
    pygame.mixer.music.play(loops=-1)
    # começamos chamando o tela de fundo inicial do assets e configurando seus parâmetros
    assets = a.carrega_assets()
    background = assets["imagem tela inicial"]
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))
    # em seguida, chamamos a fontes usadas no texto da tela inicial
    fonte1 = assets["fonte apertar inicial"] 
    fonte2 = assets["fonte titulo inicial"]
    # enquanto a tela inicial estiver rodando
    while estado["Inicial"]: 
        # colocamos na tela o seu fundo e os textos com as respectivas fontes 
        tela.blit(background, (0, 0))
        fonte_tecla = fonte1.render("Clique espaço para começar", True, (0, 195, 255))
        fonte_rect1 = fonte_tecla.get_rect()
        fonte_rect1.midtop = (p.WIDHT/2, 800)
        tela.blit(fonte_tecla, fonte_rect1)
        fonte_titulo = fonte2.render(" Mega\nMan", True, (255, 255, 255) )
        fonte_rect2 = fonte_titulo.get_rect()
        fonte_rect2.midtop = (p.WIDHT - 1400, 200)
        tela.blit(fonte_titulo, fonte_rect2)
        # agora, consideramos os eventos que podem acontecer na tela
        eventos = pygame.event.get()

        for evento in eventos: 
            # se o usuário clicar no botão de fechar o programa, ele de fato fechará
            if evento.type == pygame.QUIT:
                estado["Inicial"] = False
                estado["Jogando"] = False 
            # se o usuário clicar espaço, ele será direcionado para primeira fase
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado["Inicial"] = False
                    estado["Mapa"] = True
                    pygame.mixer.music.stop()
        # por fim, atualizamos a cada momento o jogo e determinamos sua taxa de atualizacao
        pygame.display.update()
        clock.tick(p.FPS)