# carregando as bibliotecas necessárias para rodar os assets do jogo
import pygame 
import os

pygame.font.init()
pygame.mixer.init()
# definindo uma função que guardará todos os assets do jogo por meio de um dicionário. 
# sempre que precisamos chamar um assets, chamamos essa função e o dicionário contido nela.
def carrega_assets():
    assets = {}
    assets["imagem tela inicial"] = pygame.image.load("Assets/megaman_inicial.jpg")
    assets["fonte titulo inicial"] = pygame.font.Font("Fontes/Thaleahfat.ttf", 200)
    assets["fonte apertar inicial"] = pygame.font.Font("Fontes/PressStart2P.ttf", 50)
    assets["fundo mapa"] = pygame.image.load("Assets/Backgrounds/donkey kong.png")
    assets["fundo mario"] = pygame.image.load("Assets/Backgrounds/mario.png")
    assets["tela de gameover"] = pygame.image.load("Assets/Telas/game over.jpg")
    assets["loading dk"] = pygame.image.load("Assets/Telas/loading_dk.jpg")
    assets["titulo megaman"] = pygame.image.load("Assets/megamen/titulo.png")
    assets["celula_energia"] = pygame.image.load("Assets/megamen/celula de energia.jpg")
    assets["triunfo"] = pygame.image.load("Assets/Backgrounds/triunfo.png")
    assets["desligado"] = pygame.image.load("Assets/Botoes/energia baixa.png")
    imagem = pygame.image.load("Assets/megamen/Planta 1.png")
    imagem = pygame.transform.scale(imagem, (60,90))
    imagem = pygame.transform.rotate(imagem, 180)
    assets["cano"] = imagem
    assets["som_tiro"] = pygame.mixer.Sound("Assets/megamen/som_tiro.wav")
    assets["som_tiroespecial"] = pygame.mixer.Sound("Assets/megamen/especial.mp3")
    
    player_animacao = []
    for i in range(11):
        arquivo = f"Assets/megamen/frame {i}.png"
        imagem = pygame.image.load(arquivo)
        imagem = pygame.transform.scale(imagem, (100,100))
        player_animacao.append(imagem)
    assets["animacao player"] = player_animacao

    player_animacao_atirando = []
    for i in range(11): 
        arquivo1 = f"Assets/megamen/frame atirando {i}.png"
        imagem1 = pygame.image.load(arquivo1)
        imagem1 = pygame.transform.scale(imagem1, (100,100))
        player_animacao_atirando.append(imagem1)
    assets["animacao player atirando"] = player_animacao_atirando
    assets["tiro player"] = pygame.image.load("Assets/megamen/tiro megaman.png")

    lista_pulo = []
    for i in range(5):
        sprite_pulo = pygame.image.load(f"Assets/megamen/Pulo/pulo {i}.png")
        frame = pygame.transform.scale(sprite_pulo, (100, 100))
        lista_pulo.append(frame)

    assets["animacao pulo"] = lista_pulo
    assets["chefe idle"] = pygame.image.load("Assets/Chefes/boss 1 parado.png")
    barril_rolando = []

    for i in range(4): 
        barril = pygame.image.load(f"Assets/Chefes/frame barril {i}.png")
        frame = pygame.transform.scale(barril, (100, 100))
        barril_rolando.append(frame)
    
    assets["barril rolando"] = barril_rolando
    assets["boss jogando barril"] = pygame.image.load(f"Assets/Chefes/boss 1 jogando barril.png")
    animacao_foguinho = []
    animacao_foguinho.append(pygame.image.load("Assets/Chefes/foguinho 1.png"))
    animacao_foguinho[0] = pygame.transform.scale(animacao_foguinho[0], (60, 60))
    animacao_foguinho.append(pygame.image.load("Assets/Chefes/foguinho 2.png"))
    animacao_foguinho[1] = pygame.transform.scale(animacao_foguinho[1], (60, 60))
    assets["foguinho dk"] = animacao_foguinho
    icon_dk = pygame.image.load("Assets/Botoes/Fase 1.jpg")
    assets["Icon DK"] = pygame.transform.scale(icon_dk, (250, 250))
    icon_bowser = pygame.image.load("Assets/Botoes/Fase 2.png")
    animacao_foguinho = []
    imagem = pygame.image.load("Assets/megamen/foguinho.png")
    imagem = pygame.transform.scale(imagem, (40,40))
    animacao_foguinho.append(imagem)
    imagem = pygame.transform.rotate(imagem, 90)
    animacao_foguinho.append(imagem)
    imagem = pygame.transform.rotate(imagem, 90)
    animacao_foguinho.append(imagem)
    imagem = pygame.transform.rotate(imagem, 90)
    animacao_foguinho.append(imagem)
    assets["animacao fogo"] = animacao_foguinho

    animacao_goomba = []
    for i in [1,2,3,4]:
        goomba = pygame.image.load(f"Assets/megamen/goomba {i}.png")
        frame = pygame.transform.scale(goomba, (55,55))
        animacao_goomba.append(frame)
    assets["goomba"] = animacao_goomba

    animacao_planta = []
    imagem = pygame.image.load("Assets/megamen/Planta 1.png")
    imagem = pygame.transform.scale(imagem, (60,90))
    imagem = pygame.transform.rotate(imagem, 180)
    animacao_planta.append(imagem)
    imagem = pygame.image.load("Assets/megamen/Planta 2.png")
    imagem = pygame.transform.scale(imagem, (60,90))
    imagem = pygame.transform.rotate(imagem, 180)
    animacao_planta.append(imagem)
    assets["planta"] = animacao_planta

    assets["koopa"] = [
        pygame.transform.scale(pygame.image.load("Assets/Chefes/tartaruga1.png"), (65,75)),pygame.transform.scale(pygame.image.load("Assets/Chefes/tartaruga2.png"), (65,75))
    ]

    assets["bullet"] = [
        pygame.image.load("Assets/Chefes/bullet.png")
    ]

    assets["bloco"] = pygame.image.load("Assets/Chefes/bloco.png")

    assets["som de dano"] = pygame.mixer.Sound("Assets/Sound Effects/expl3.wav")
    animacao_barril_especial = []
    animacao_barril_especial.append(pygame.image.load("Assets/Chefes/barril especial 1.png"))
    animacao_barril_especial[0] = pygame.transform.scale(animacao_barril_especial[0], (100, 100))
    imagem = pygame.transform.rotate(animacao_barril_especial[0], 90)
    animacao_barril_especial.append(imagem)
    assets["barril especial"] = animacao_barril_especial
    assets["bloco preto"] = pygame.image.load("Assets/bloco preto.jpg")

    imagem = pygame.image.load("Assets/Backgrounds/castelo.png")
    assets["castelo"] = pygame.transform.scale(imagem, (490,490))
    Florzinha = pygame.image.load("Assets/Chefes/flor_de_fogo.png")
    assets["powerup_flor"] = [pygame.transform.scale(Florzinha, (60,60))]
    assets["powerup_cogumelo"] = [pygame.image.load("Assets/Chefes/flor_de_fogo.png")]
    assets["powerup_estrela"] = [pygame.image.load("Assets/Chefes/flor_de_fogo.png")]
    assets["casco"] =[
        pygame.transform.scale(pygame.image.load("Assets/Chefes/casco1.png"), (60,60)),
        pygame.transform.scale(pygame.image.load("Assets/Chefes/casco2.png"), (60,47)),
        pygame.transform.scale(pygame.image.load("Assets/Chefes/casco3.png"), (60,47)),
        pygame.transform.scale(pygame.image.load("Assets/Chefes/casco4.png"), (60,47))
    ]
    assets["fundo castelo"] = pygame.image.load("Assets/Backgrounds/donkey kong.png")
    assets["bgm_boss"] = pygame.mixer.Sound("Assets/Sound Effects/expl3.wav")
    assets["fundo_bowser"] = pygame.image.load("Assets/Backgrounds/donkey kong.png")
    assets["powerup_mushroom"] = [pygame.image.load("Assets/Chefes/cogumelo.png")]
    return assets

