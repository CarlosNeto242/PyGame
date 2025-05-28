# importamos as bibliotecas e arquivos necessários para montar a tela inicial
import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b

pygame.init()
# definindo uma função responsável por montar a tela de vitória (será posteriormente chamada no loop principal)
def win(tela, clock, estado): 
    pygame.mixer.music.load('Assets/Sound Effects/bgm_action_5.mp3')
    pygame.mixer.music.play()
    # começamos chamando o tela de fundo de vitória do assets e configurando seus parâmetros
    assets = a.carrega_assets()
    vitoria = assets["triunfo"]
    vitoria = pygame.transform.scale(vitoria, (500, 500))
    assets["fonte apertar inicial"] = pygame.font.Font("Fontes/PressStart2P.ttf", 40)
    # em seguida, chamamos a fontes usadas no texto da tela de vitória
    fonte1 = assets["fonte apertar inicial"]
    # enquanto a tela de vitória estiver rodando
    while estado["Ganhar"]: 
         # colocamos na tela o seu fundo e os textos com as respectivas fontes 
        tela.fill((0, 0, 0))
        tela.blit(vitoria, (600, 200))
        fonte_tecla = fonte1.render("Parabéns!", True, (0, 195, 255))
        fonte_rect1 = fonte_tecla.get_rect()
        fonte_rect1.midtop = (p.WIDHT/2, 780)
        tela.blit(fonte_tecla, fonte_rect1)
        fonte_tecla2 = fonte1.render("sua energia foi recuperada", True, (0, 195, 255))
        fonte_rect2 = fonte_tecla2.get_rect()
        fonte_rect2.midtop = (p.WIDHT/2, 850)
        tela.blit(fonte_tecla2, fonte_rect2)
        # agora, consideramos os eventos que podem acontecer na tela
        eventos = pygame.event.get()

        for evento in eventos: 
            # se o usuário clicar no botão de fechar o programa, ele de fato fechará
            if evento.type == pygame.QUIT:
                estado["Ganhar"] = False
                estado["Jogando"] = False 
            if evento.type == pygame.KEYDOWN:
            # se o usuário clicar espaço, ele será direcionado para a primeira fase (o jogo reinicia)
                    estado["Ganhar"] = False
                    estado["Jogando"] = False
        # por fim, atualizamos a cada momento o jogo e determinamos sua taxa de atualizacao
        pygame.display.update()
        clock.tick(p.FPS)