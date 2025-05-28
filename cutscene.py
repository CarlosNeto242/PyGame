# importamos as bibliotecas e arquivos necessários para criar os bosses do jogo

import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
import random 
import Auxiliares as aux

# criando uma função que irá criar a animação da cutscene do jogo
def animacao_cutscene(tela, clock, estado): 
    #carregando os assets
    pygame.mixer.music.load("Sprites/Sound Effects/sound_effects/sound_effects/odd2.wav")
    pygame.mixer.music.play()
    background = pygame.image.load("Sprites/megaman_inicial.jpg")
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))
    assets = a.carrega_assets()
    frames = 2000
    tempo = 0
    # enquanto a cutscene estiver ativa, o jogo irá desenhar o fundo e alternar entre preto e o fundo normal
    while estado["Cutscene"]: 
        if (tempo // 30) % 2 == 0:
            tela.fill((0, 0, 0)) 
        else:
            tela.blit(background, (0, 0)) 
        pygame.display.update()
        clock.tick(p.FPS)
        tempo += 20
        # quando chegar a um certo tempo, o jogo irá parar a cutscene e mostrar outra tela
        if tempo > frames:
            estado["Cutscene"] = False
            estado["Aviso"] = True
