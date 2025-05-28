# importamos as bibliotecas e arquivos necessários para criar os bosses do jogo
import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
from bosses import Bowser, PowerUp
from Auxiliares import desenhar_barra_vida_player, desenhar_barra_vida_boss
import random

# -------------------------
# FASE BOWSER JR - estática
# -------------------------
# definindo uma função para a fase do Bowser. Jr

def fase_bowser_jr(tela, clock, estado):
    # carregando os assets
    assets = a.carrega_assets()
    background = assets["fundo mario"]

    tiros = pygame.sprite.Group()
    projeteis_inimigos = pygame.sprite.Group()
    itens = pygame.sprite.Group()
    grupos = {"tiros": tiros, "projeteis_inimigos": projeteis_inimigos, "itens": itens}
    # definindo as entidades da fase
    player = pl.Player(grupos, assets)
    player.rect.bottom = 801.5
    camera_x = 0

    # plataformas = pygame.sprite.Group(
    #     Bloco(300, 700, assets["bloco"]))

    boss = b.BowserJr(assets, grupos)
    grupo_boss = pygame.sprite.Group(boss)
    # enquanto a fase rodar, o seguintes eventos serão analizados
    while estado["Bowser_Junior"]:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["BowserJr"] = False
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_LEFT, pygame.K_a]:
                    player.speedx -= 15
                if evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.speedx += 15
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    player.pular()
                if evento.key == pygame.K_v:
                    player.atirar_especial(True)
            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                    player.speedx = 0
        # atualiza as coisas na tela 
        player.update_deslocar(400, 1600)  # Limita a movimentação
        player.update_animacao()
        player.update_gravidade(801.5)
        boss.update(player)
        tiros.update()
        projeteis_inimigos.update()
        # plataformas.update()
        itens.update()
        # checando quem morreu 
        if player.vida <= 0:
            estado["BowserJr"] = False
            estado["Perder"] = True

        if len(grupo_boss) == 0:
            estado["BowserJr"] = False
            estado["KingBoo"] = True
            return
        # desenha o fundo e as entidades na tela
        tela.blit(background, (0, 0))
        for grupo in [tiros, projeteis_inimigos, itens, grupo_boss]:
            for entidade in grupo:
                tela.blit(entidade.image, (entidade.rect.x, entidade.rect.y))
        tela.blit(player.image, (player.rect.x, player.rect.y))
        # desenha a vida do boss e do player
        desenhar_barra_vida_player(tela, player)
        desenhar_barra_vida_boss(tela, boss, 0)

        pygame.display.update()
        clock.tick(p.FPS)

# -------------------------
# FASE KING BOO - estática
# -------------------------
# definindo uma função para a fase do King Boo
def fase_king_boo(tela, clock, estado):
    # carregando os assets
    assets = a.carrega_assets()
    background = assets["fundo mario"]

    tiros = pygame.sprite.Group()
    projeteis_inimigos = pygame.sprite.Group()
    itens = pygame.sprite.Group()
    grupos = {"tiros": tiros, "projeteis_inimigos": projeteis_inimigos, "itens": itens}
    # definindo as entidades da fase
    player = pl.Player(grupos, assets)
    player.rect.bottom = 801.5

    # plataformas = pygame.sprite.Group(
    #     Bloco(500, 700, assets["bloco"]),
    #     Bloco(800, 600, assets["bloco"])
    # )

    boss = b.KingBoo(assets, grupos)
    grupo_boss = pygame.sprite.Group(boss)
    # enquanto a fase rodar, o seguintes eventos serão analizados
    while estado["KingBoo"]:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["KingBoo"] = False
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_LEFT, pygame.K_a]:
                    player.speedx -= 15
                if evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.speedx += 15
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    player.pular()
                if evento.key == pygame.K_v:
                    player.atirar_especial(True)
                if evento.key == pygame.K_b:
                    estado["KingBoo"] = False
                    estado["Bowser "] = False
            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                    player.speedx = 0
        # atualiza as coisas na tela
        player.update_deslocar(400, 1600)
        player.update_animacao()
        player.update_gravidade(801.5)
        boss.update(player)
        tiros.update()
        projeteis_inimigos.update()
        # plataformas.update()
        itens.update()
        # checando quem morreu
        if player.vida <= 0:
            estado["KingBoo"] = False
            estado["Perder"] = True

        if len(grupo_boss) == 0:
            estado["KingBoo"] = False
            estado["Bowser"] = True
            return
        # desenha o fundo e as entidades na tela
        tela.blit(background, (0, 0))
        # for grupo in [plataformas, tiros, projeteis_inimigos, itens, grupo_boss]:
        #     for entidade in grupo:
        #         tela.blit(entidade.image, (entidade.rect.x, entidade.rect.y))
        tela.blit(player.image, (player.rect.x, player.rect.y))
        # desenha a vida do boss e do player
        desenhar_barra_vida_player(tela, player)
        desenhar_barra_vida_boss(tela, boss, 0)

        pygame.display.update()
        clock.tick(p.FPS)

# -------------------------
# FASE BOWSER FINAL - estática
# -------------------------

# definindo uma função para a fase final do Bowser
def fase_bowser_final(tela, clock, estado):
    # carregando os assets
    assets = a.carrega_assets()
    background = assets["fundo mario"]

    tiros = pygame.sprite.Group()
    bolas_de_fogo = pygame.sprite.Group()
    projeteis_inimigos = pygame.sprite.Group()
    itens = pygame.sprite.Group()
    grupos = {
        "tiros": tiros,
        "bolas_de_fogo": bolas_de_fogo,
        "projeteis_inimigos": projeteis_inimigos,
        "itens": itens
    }
    # definindo as entidades da fase
    player = pl.Player(grupos, assets)
    player.rect.bottom = 801.5

    # plataformas = pygame.sprite.Group(
    #     Bloco(500, 700, assets["bloco"]),
    #     Bloco(800, 600, assets["bloco"]),
    #     PlataformaMovel(1000, 550, assets["bloco"], 950, 1150)
    # )

    boss = b.Bowser(assets, grupos)
    grupo_boss = pygame.sprite.Group(boss)
     # enquanto a fase rodar, o seguintes eventos serão analizados
    while estado["Bowser"]:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["Bowser"] = False
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_LEFT, pygame.K_a]:
                    player.speedx -= 50
                if evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.speedx += 50
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    player.pular()
                if evento.key == pygame.K_v:
                    player.atirar_especial(True)
            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                    player.speedx = 0
        # atualiza as coisas na tela
        player.update_deslocar(400, 1600)
        player.update_animacao()
        player.update_gravidade(801.5)
        boss.update_comportamento(player)
        tiros.update()
        bolas_de_fogo.update()
        projeteis_inimigos.update()
        # plataformas.update()
        itens.update()
        # checando quem morreu
        if player.vida <= 0:
            estado["Bowser"] = False
            estado["Perder"] = True

        if len(grupo_boss) == 0:
            estado["Bowser"] = False
            estado["Venceu"] = True
            return
        # desenha o fundo e as entidades na tela
        tela.blit(background, (0, 0))
        # for grupo in [plataformas, tiros, bolas_de_fogo, projeteis_inimigos, itens, grupo_boss]:
        #     for entidade in grupo:
        #         tela.blit(entidade.image, (entidade.rect.x, entidade.rect.y))
        tela.blit(player.image, (player.rect.x, player.rect.y))
        # desenha a vida do boss e do player
        desenhar_barra_vida_player(tela, player)
        desenhar_barra_vida_boss(tela, boss, 0)
        pygame.display.update()
        clock.tick(p.FPS)

   