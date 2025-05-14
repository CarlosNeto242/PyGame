import pygame 
import os



def carrega_assets():
    assets = {}
    assets["imagem tela inicial"] = pygame.image.load("Sprites/megaman_inicial.jpg")
    assets["fonte titulo inicial"] = pygame.font.Font("Fontes/Thaleahfat.ttf", 200)
    assets["fonte apertar inicial"] = pygame.font.Font("Fontes/PressStart2P.ttf", 50)
    assets["fundo mapa"] = pygame.image.load("Sprites/Backgrounds/floresta.png")
    player_animacao = []
    for i in range(1, 11):
        arquivo = f"Sprites/megamen/frame {i}.png"
        imagem = pygame.image.load(arquivo)
        imagem = pygame.transform.scale(imagem, (100,100))
        player_animacao.append(imagem)
    assets["animacao player"] = player_animacao
    player_animacao_atirando = []
    for i in range(1, 11): 
        arquivo1 = f"Sprites/megamen/frame atirando {i}.png"
        imagem1 = pygame.image.load(arquivo1)
        imagem1 = pygame.transform.scale(imagem1, (100,100))
        player_animacao_atirando.append(imagem1)
    assets["animacao player atirando"] = player_animacao_atirando
    assets["tiro player"] = pygame.image.load("Sprites/megamen/tiro megaman.png")
    return assets
