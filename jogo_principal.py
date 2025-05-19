import pygame
import parametros as p
import tela_inicial 
import bosses
import Fase_dk
import perder
import ctypes
import fase_bowser

try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

pygame.init()
pygame.font.init()


tela = pygame.display.set_mode((p.WIDHT, p.HEIGHT),)
clock = pygame.time.Clock()
estados = {"Jogando" : True, "Inicial" : True, "Ganhar" : False, "Perder" : False, "DK" : False, "Bowser" : False, "Final" : False}

while estados["Jogando"]: 
    if estados["Inicial"]: 
        tela_inicial.inicio(tela, clock, estados)
    elif estados["DK"]:
        Fase_dk.mapa(tela, clock, estados)
    elif estados["Bowser"]:
        fase_bowser.fase_bowser(tela, clock, estados)
    elif estados["Perder"]: 
        perder.gameover(tela, clock, estados)
    elif estados["Final"]: 
        pass


pygame.quit()



