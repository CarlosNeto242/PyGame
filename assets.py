# carregando as bibliotecas necessárias para rodar o programa
import pygame 
import os

pygame.font.init()

# definindo uma função que guardará todos os assets do jogo por meio de um dicionário. 
# sempre que precisamos chamar um assets, chamamos essa função e o dicionário contido nela.
def carrega_assets():
    assets = {}
    assets["imagem tela inicial"] = pygame.image.load("Sprites/megaman_inicial.jpg")
    assets["fonte titulo inicial"] = pygame.font.Font("Fontes/Thaleahfat.ttf", 200)
    assets["fonte apertar inicial"] = pygame.font.Font("Fontes/PressStart2P.ttf", 50)
    assets["fundo mapa"] = pygame.image.load("Sprites/Backgrounds/floresta.png")
    assets["fundo mario"] = pygame.image.load("Sprites/Backgrounds/mario.png")
    assets["tela de gameover"] = pygame.image.load("Sprites/Telas/game over.jpg")
    assets["tela de vitória"] = pygame.image.load("Sprites/Telas/victory.png")
    # assets["som_tiro"] = pygame.mixer.Sound("Sprites/megamen/som_tiro.wav")
    assets["som_tiroespecial"] = pygame.mixer.Sound("Sprites/megamen/especial.mp3")
    player_animacao = []
    for i in range(11):
        arquivo = f"Sprites/megamen/frame {i}.png"
        imagem = pygame.image.load(arquivo)
        imagem = pygame.transform.scale(imagem, (100,100))
        player_animacao.append(imagem)
    assets["animacao player"] = player_animacao
    player_animacao_atirando = []
    for i in range(11): 
        arquivo1 = f"Sprites/megamen/frame atirando {i}.png"
        imagem1 = pygame.image.load(arquivo1)
        imagem1 = pygame.transform.scale(imagem1, (100,100))
        player_animacao_atirando.append(imagem1)
    assets["animacao player atirando"] = player_animacao_atirando
    assets["tiro player"] = pygame.image.load("Sprites/megamen/tiro megaman.png")

    lista_pulo = []
    for i in range(5):
        sprite_pulo = pygame.image.load(f"Sprites/megamen/Pulo/pulo {i}.png")
        frame = pygame.transform.scale(sprite_pulo, (100, 100))
        lista_pulo.append(frame)

    assets["animacao pulo"] = lista_pulo
    assets["chefe idle"] = pygame.image.load("Sprites/Chefes/boss 1 parado.png")
    barril_rolando = []
    for i in range(4): 
        barril = pygame.image.load(f"Sprites/Chefes/frame barril {i}.png")
        frame = pygame.transform.scale(barril, (100, 100))
        barril_rolando.append(frame)
    assets["barril rolando"] = barril_rolando
    assets["boss jogando barril"] = pygame.image.load(f"Sprites/Chefes/boss 1 jogando barril.png")
    animacao_foguinho = []
    animacao_foguinho.append(pygame.image.load("Sprites/Chefes/foguinho 1.png"))
    animacao_foguinho[0] = pygame.transform.scale(animacao_foguinho[0], (60, 60))
    animacao_foguinho.append(pygame.image.load("Sprites/Chefes/foguinho 2.png"))
    animacao_foguinho[1] = pygame.transform.scale(animacao_foguinho[1], (60, 60))
    assets["foguinho dk"] = animacao_foguinho
    icon_dk = pygame.image.load("Sprites/Botoes/Fase 1.jpg")
    assets["Icon DK"] = pygame.transform.scale(icon_dk, (250, 250))
    icon_bowser = pygame.image.load("Sprites/Botoes/Fase 2.png")
    assets["Icon Bowser"] = pygame.transform.scale(icon_bowser, (250, 250))
    icon_eggman = pygame.image.load("Sprites/Botoes/Fase 3.jpg")
    assets["Icon EggMan"] = pygame.transform.scale(icon_eggman, (250, 250))
    assets["EggMan idle"] = pygame.image.load("Sprites/Chefes/boss 3 parado.png")
    assets["fundo eggman"] = pygame.image.load("Sprites/Backgrounds/cenario_eggman.png")
    
    return assets
