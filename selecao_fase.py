import pygame
import parametros as p
import assets as a
import botao as b

def selecionar(tela, clock, estado):
    assets = a.carrega_assets()
    espacamento = 300 
    x = espacamento
    y = 500
    botoes = pygame.sprite.Group()
    # Carregando os assets necessários para a tela de seleção
    botao = b.Botao(assets, botoes, "Icon DK")

    botao.rect.x = x
    botao.rect.centery = y
    botoes.add(botao)
    
    botao = b.Botao(assets, botoes, "Icon Bowser")

    botao.rect.x += x
    botao.rect.centery = y
    botoes.add(botao)

    pygame.display.update()
    clock.tick(p.FPS)
