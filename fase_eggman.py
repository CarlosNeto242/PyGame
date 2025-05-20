import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b

def desenhar_barra_vida(tela, boss):
    largura = 400
    altura = 30
    x = (p.WIDHT - largura) // 2
    y = 20
    vida_percent = boss.vida / boss.max_vida
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura)) 
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura * vida_percent, altura)) 
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 4)
# definimos uma função que desenha a barra de vida do player na tela
def desenhar_barra_vida_player(tela, player):
    largura = 200
    altura = 20
    x = 50
    y = 20
    vida_percent = player.vida / player.max_vida
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura))  
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura * vida_percent, altura))  
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 3)  

def fase(tela, clock, estado): 
    assets = a.carrega_assets()
    background = assets["fundo eggman"]
    background = pygame.transform.scale(background, (1820, 980))
    
    tiros = pygame.sprite.Group()
    robozinhos = pygame.sprite.Group()
    grupos = {}
    grupos["tiros"] = tiros
    grupos["robozinhos"] = robozinhos