import pygame
import parametros as p
import tela_inicial 
import bosses
import perder 
import ganhar
import ctypes
import fase_mario
import selecao_fase

try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

pygame.init()
pygame.font.init()
pygame.mixer.init()
tela = pygame.display.set_mode((p.WIDHT, p.HEIGHT))
clock = pygame.time.Clock()
estados = {"Jogando": True, "Inicial": True, "Mapa": False, "Ganhar": False, "Perder": False, "DK": False, "Bowser": False, "EggMan": False, "Final": False}

while estados["Jogando"]: 
    if estados["Inicial"]: 
        tela_inicial.inicio(tela, clock, estados)
    elif estados["Mapa"]:
        selecao_fase.selecionar(tela, clock, estados)
    elif estados["DK"]:
        fase_mario.mapa(tela, clock, estados)
        fase = "Bowser"
    elif estados["Mario"]:
        fase_mario.fase_mario(tela, clock, estados) 
    elif estados["Bowser_Junior"]:
        fase_mario.fase_bowser_jr(tela, clock, estados) 
    elif estados["KingBoo"]:
        fase_mario.fase_king_boo(tela, clock, estados) 
    elif estados["Bowser"]:
        fase_mario.fase_bowser_final(tela, clock, estados) 
    elif estados["Perder"]: 
        perder.gameover(tela, clock, estados)
    elif estados["Ganhar"]: 
        ganhar.win(tela, clock, estados, fase)
    elif estados["Final"]: 
        pass


pygame.quit()



