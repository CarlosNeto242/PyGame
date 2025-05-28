# importamos as bibliotecas e arquivos necessários para montar o looping principal do jogo
import pygame
import parametros as p
import tela_inicial 
import bosses
import perder 
import ganhar
import ctypes
import fase_mario
import Fase_dk
import cutscene
import aviso
# comando para ajustar a escala de DPI no Windows, para evitar problemas de resolução (os dois participantes tinham notebooks com dierentes resoluções)
try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass
# inicianndo os módulos do pygame e criando a tela principal do jogo, juntamente com sua taxa de atualização
pygame.init()
pygame.font.init()
pygame.mixer.init()
tela = pygame.display.set_mode((p.WIDHT, p.HEIGHT))
clock = pygame.time.Clock()
estados = {"Jogando": True, "Inicial": True, "Aviso" : False, "Cutscene" : False, "Mapa": False, "Ganhar": False, "Perder": False, "DK": False , "Mario": False, "Final": False}

while estados["Jogando"]: 
    if estados["Inicial"]: 
        tela_inicial.inicio(tela, clock, estados)
    elif estados["Cutscene"]:
        cutscene.animacao_cutscene(tela, clock, estados)
    elif estados["Aviso"]:
        aviso.aviso(clock, tela, estados)
    elif estados["DK"]:
        Fase_dk.mapa(tela, clock, estados)
        atual = "DK"
        proxima = "Bowser"
    elif estados["Mario"]:
        atual = "Mario"
        fase_mario.fase_mario(tela, clock, estados) 
    elif estados["Perder"]: 
        perder.gameover(tela, clock, estados)
    elif estados["Ganhar"]: 
        ganhar.win(tela, clock, estados)
    elif estados["Final"]: 
        pass


pygame.quit()



