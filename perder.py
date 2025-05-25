# importando os arquivos e bilbiotecas necessários para o programa

import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b

pygame.init()
# definindo uma função responsável por montar a tela de game over (será posteriormente chamada no loop principal)
def gameover(tela, clock, estado): 
    pygame.mixer.music.load('Sprites/Sound Effects/JRPG OST (Rev 2)/20 - Game Over.ogg')
    pygame.mixer.music.play(loops=-1)
    # começamos chamando o tela de game over do assets e configurando seus parâmetros
    assets = a.carrega_assets()
    background = assets["tela de gameover"]
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))
    # em seguida, chamamos a fontes usadas no texto da tela do game over
    fonte1 = assets["fonte apertar inicial"] 
    # enquanto a tela de game over estiver rodando
    while estado["Perder"]: 
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
                estado["Perder"] = False
                estado["Jogando"] = False 
        # se o usuário clicar espaço, ele será direcionado para a primeira fase (o jogo reinicia)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado["Perder"] = False
                    estado["DK"] = True
                    pygame.mixer.music.stop()
        # por fim, atualizamos a cada momento o jogo e determinamos sua taxa de atualizacao
        pygame.display.update()
        clock.tick(p.FPS)