import pygame
import parametros as p
import tela_inicial 
import bosses
import Fase_dk
import perder
import ganhar
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
estados = {"Jogando" : True, "Inicial" : True, "Mapa" : False, "Ganhar" : False, "Perder" : False, "DK" : False, "Bowser" : False, "Final" : False}

while estados["Jogando"]: 
    if estados["Inicial"]: 
        tela_inicial.inicio(tela, clock, estados)
    elif estados["DK"]:
        Fase_dk.mapa(tela, clock, estados)
        fase = "Bowser"
    elif estados["Bowser"]:
        fase_bowser.fase_bowser(tela, clock, estados)
    elif estados["Perder"]: 
        perder.gameover(tela, clock, estados)
    elif estados["Ganhar"]: 
        ganhar.win(tela, clock, estados, fase)
    elif estados["Final"]: 
        pass


pygame.quit()



