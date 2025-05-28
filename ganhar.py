# importamos as bibliotecas e arquivos necessários para montar a tela inicial
import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b

pygame.init()
# definindo uma função responsável por montar a tela de vitória (será posteriormente chamada no loop principal)
def win(tela, clock, estado): 
    pygame.mixer.music.load('Sprites/Sound Effects/bgm_action_5.mp3')
    pygame.mixer.music.play()
    # começamos chamando o tela de fundo de vitória do assets e configurando seus parâmetros
    assets = a.carrega_assets()
    background = assets["tela de vitória"]
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))
    assets["fonte apertar inicial"] = pygame.font.Font("Fontes/PressStart2P.ttf", 30)
    # em seguida, chamamos a fontes usadas no texto da tela de vitória
    fonte1 = assets["fonte apertar inicial"]
    # enquanto a tela de vitória estiver rodando
    while estado["Ganhar"]: 
         # colocamos na tela o seu fundo e os textos com as respectivas fontes 
        tela.blit(background, (0, 0))
        fonte_tecla = fonte1.render("Clique espaço para selecionar outra fase", True, (0, 195, 255))
        fonte_rect1 = fonte_tecla.get_rect()
        fonte_rect1.midtop = (p.WIDHT/2, 800)
        tela.blit(fonte_tecla, fonte_rect1)
        # agora, consideramos os eventos que podem acontecer na tela
        eventos = pygame.event.get()

        for evento in eventos: 
            # se o usuário clicar no botão de fechar o programa, ele de fato fechará
            if evento.type == pygame.QUIT:
                estado["Ganhar"] = False
                estado["Jogando"] = False 
            if evento.type == pygame.KEYDOWN:
            # se o usuário clicar espaço, ele será direcionado para a primeira fase (o jogo reinicia)
                if evento.key == pygame.K_SPACE:
                    estado["Ganhar"] = False
                    estado["Mapa"] = True
        # por fim, atualizamos a cada momento o jogo e determinamos sua taxa de atualizacao
        pygame.display.update()
        clock.tick(p.FPS)