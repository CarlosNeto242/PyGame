import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
import random 
import Auxiliares as aux

def animacao_cutscene(tela, clock, estado): 
    pygame.mixer.music.load("Sprites/Sound Effects/sound_effects/sound_effects/odd2.wav")
    pygame.mixer.music.play()
    background = pygame.image.load("Sprites/megaman_inicial.jpg")
    background = pygame.transform.scale(background, (p.WIDHT, p.HEIGHT))
    assets = a.carrega_assets()
    frames = 2000
    tempo = 0

    while estado["Cutscene"]: 
        if (tempo // 30) % 2 == 0:
            tela.fill((0, 0, 0))  # preenche a tela de preto
        else:
            tela.blit(background, (0, 0))  # desenha o fundo normalmente
        pygame.display.update()
        clock.tick(p.FPS)
        tempo += 20
        # condição de saída do estado, exemplo fictício
        if tempo > frames:
            estado["Cutscene"] = False
            estado["Aviso"] = True
