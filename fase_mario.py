import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
from Auxiliares import desenhar_barra_vida_player, desenhar_barra_vida_boss
import random

def fase_mario(tela, clock, estado):
    import pygame
    import parametros as p
    import assets as a
    import player as pl
    import bosses as b
    from Auxiliares import desenhar_barra_vida_player
    import random
    pygame.mixer.init()
    pygame.mixer.music.load("Sprites/mario.wav")
    pygame.mixer.music.play(-1)  # Toca em loop


    assets = a.carrega_assets()
    background = assets["fundo mario"]
    castelo_img = assets["castelo"]
    fonte = pygame.font.Font("Fontes/PressStart2P.ttf", 27)

    # Grupos de sprites
    tiros = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    itens = pygame.sprite.Group()
    grupos = {"tiros": tiros, "inimigos": inimigos, "itens": itens}

    # Criação do jogador
    player = pl.Player(grupos, assets)
    player.rect.bottom = 801.5
    camera_x = 0

    # Tela preta de introdução
    tela.fill((0, 0, 0))
    texto_intro = fonte.render("Invasão de jogo em processamento...", True, (255, 255, 255))
    tela.blit(texto_intro, (p.WIDHT // 2 - texto_intro.get_width() // 2, p.HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)

    # Mensagem narrativa
    fonte = pygame.font.Font("Fontes/PressStart2P.ttf", 20)
    tela.blit(background, (0, 0))
    texto_alerta = fonte.render(
        "Todos os inimigos do Mario estão com raiva por você estar aqui como INTRUSO!",
        True, (0, 0, 0)
    )
    tela.blit(texto_alerta, (p.WIDHT // 2 - texto_alerta.get_width() // 2, p.HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(3000)

    # Criação de inimigos fixos
    for i, x in enumerate(range(600, 18000, 450)):  # espaçamento reduzido para mais inimigos
        if i % 6 == 0:
            inimigos.add(b.Goomba(assets, x, 800))
        elif i % 6 == 1:
            inimigos.add(b.Koopa(assets, x, 800))
        elif i % 6 == 2:
            inimigos.add(b.PlantaCarnivoraAnimada(assets, x, 800))
        elif i % 6 == 3:
            inimigos.add(b.Goomba(assets, x, 800))
            inimigos.add(b.Koopa(assets, x + 50, 800))
        elif i % 6 == 4:
            inimigos.add(b.PlantaCarnivoraAnimada(assets, x, 800))
            inimigos.add(b.Koopa(assets, x + 50, 800))
        else:
            inimigos.add(b.Goomba(assets, x, 800))
            inimigos.add(b.PlantaCarnivoraAnimada(assets, x + 50, 800))
            inimigos.add(b.PlantaCarnivoraAnimada(assets, x, 800))
    # Power-up flor fixo
    flor = b.PowerUp("flor", 19000, 700, assets)
    itens.add(flor)
    flor_mensagem_mostrada = False

    # Definição da porta do castelo
    porta_castelo = pygame.Rect(19500, 0, 80, 801.5)

    while estado["Mario"]:
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado["Mario"] = estado["Jogando"] = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_LEFT, pygame.K_a]:
                    player.speedx += -11
                elif evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.speedx += 11
                elif evento.key in [pygame.K_UP, pygame.K_w]:
                    player.pular(22)
                    pygame.mixer.Sound("Sprites/smw_jump.wav").play()  # Som de pulo
                elif evento.key == pygame.K_v:
                    player.atirar_especial(player.pegou_flor)
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                    player.speedx = 0

        # Atualizações
        player.update_deslocar(0, 20000)
        player.update_animacao()
        player.update_gravidade(801.5)
        tiros.update()
        itens.update()
        for inimigo in inimigos:
            if isinstance(inimigo, b.PlantaCarnivoraAnimada):
                inimigo.update(player)
            else:
                inimigo.update()

        # Colisão com inimigos
        for inimigo in inimigos:
            if player.rect.colliderect(inimigo.rect):
                if isinstance(inimigo, b.Goomba) and player.rect.bottom < inimigo.rect.centery:
                    inimigo.kill()
                    player.speedy = -18
                elif isinstance(inimigo, b.Koopa):
                    inimigo.levar_pulo(player)
                elif not player.invulneravel:
                    player.vida -= inimigo.dano
                    knock_dir = -15 if player.rect.centerx < inimigo.rect.centerx else 15
                    player.knockback(knock_dir)


        # Coleta de itens
        for item in itens:
            if player.rect.colliderect(item.rect):
                if item.tipo == "flor":
                    player.pegou_flor = True
                    item.kill()
                    flor_mensagem_mostrada = True
                    flor_msg_timer = pygame.time.get_ticks()

        # Verifica fim de jogo
        if player.vida <= 0:
            estado["Mario"] = False
            estado["Perder"] = True

        if player.rect.colliderect(porta_castelo):
            estado["Mario"] = False
            estado["Bowser_Junior"] = True
            return

        # Atualização da câmera
        target_camera_x = player.rect.centerx - p.WIDHT // 2
        camera_x += (target_camera_x - camera_x) * 0.1

        # Desenho da tela
        largura_fundo = background.get_width()
        for i in range(int(camera_x // largura_fundo) - 1, int((camera_x + p.WIDHT) // largura_fundo) + 2):
            tela.blit(background, (i * largura_fundo - camera_x, 0))

        tela.blit(castelo_img, (19500 - camera_x, 801.5 - castelo_img.get_height()))
        pygame.draw.rect(
            tela, (255, 0, 0),
            (porta_castelo.x - camera_x, porta_castelo.y, porta_castelo.width, porta_castelo.height),
            2  # linha vermelha da porta
        )

        for grupo in [inimigos, tiros, itens]:
            for entidade in grupo:
                tela.blit(entidade.image, (entidade.rect.x - camera_x, entidade.rect.y))
        tela.blit(player.image, (player.rect.x - camera_x, player.rect.y))
        desenhar_barra_vida_player(tela, player)

        # Mensagem da flor
        if flor_mensagem_mostrada:
            if pygame.time.get_ticks() - flor_msg_timer < 2000:
                texto_flor = fonte.render("Você adquiriu o poder de fogo!", True, (255, 0, 0))
                tela.blit(texto_flor, (p.WIDHT // 2 - texto_flor.get_width() // 2, 50))
            else:
                flor_mensagem_mostrada = False

        pygame.display.update()
        clock.tick(p.FPS)



# -------------------------
# FASE BOWSER JR - estática
# -------------------------
def fase_bowser_jr(tela, clock, estado):
    assets = a.carrega_assets()
    background = assets["fundo mario"]

    tiros = pygame.sprite.Group()
    projeteis_inimigos = pygame.sprite.Group()
    itens = pygame.sprite.Group()
    grupos = {"tiros": tiros, "projeteis_inimigos": projeteis_inimigos, "itens": itens}

    player = pl.Player(grupos, assets)
    player.rect.bottom = 801.5
    camera_x = 0

    # plataformas = pygame.sprite.Group(
    #     Bloco(300, 700, assets["bloco"]))

    boss = b.BowserJr(assets, grupos)
    grupo_boss = pygame.sprite.Group(boss)

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

        player.update_deslocar(400, 1600)  # Limita a movimentação
        player.update_animacao()
        player.update_gravidade(801.5)
        boss.update(player)
        tiros.update()
        projeteis_inimigos.update()
        # plataformas.update()
        itens.update()

        if player.vida <= 0:
            estado["BowserJr"] = False
            estado["Perder"] = True

        if len(grupo_boss) == 0:
            estado["BowserJr"] = False
            estado["KingBoo"] = True
            return

        tela.blit(background, (0, 0))
        for grupo in [tiros, projeteis_inimigos, itens, grupo_boss]:
            for entidade in grupo:
                tela.blit(entidade.image, (entidade.rect.x, entidade.rect.y))
        tela.blit(player.image, (player.rect.x, player.rect.y))

        desenhar_barra_vida_player(tela, player)
        desenhar_barra_vida_boss(tela, boss, 0)

        pygame.display.update()
        clock.tick(p.FPS)

# -------------------------
# FASE KING BOO - estática
# -------------------------
def fase_king_boo(tela, clock, estado):
    assets = a.carrega_assets()
    background = assets["fundo mario"]

    tiros = pygame.sprite.Group()
    projeteis_inimigos = pygame.sprite.Group()
    itens = pygame.sprite.Group()
    grupos = {"tiros": tiros, "projeteis_inimigos": projeteis_inimigos, "itens": itens}

    player = pl.Player(grupos, assets)
    player.rect.bottom = 801.5

    # plataformas = pygame.sprite.Group(
    #     Bloco(500, 700, assets["bloco"]),
    #     Bloco(800, 600, assets["bloco"])
    # )

    boss = b.KingBoo(assets, grupos)
    grupo_boss = pygame.sprite.Group(boss)

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

        player.update_deslocar(400, 1600)
        player.update_animacao()
        player.update_gravidade(801.5)
        boss.update(player)
        tiros.update()
        projeteis_inimigos.update()
        # plataformas.update()
        itens.update()

        if player.vida <= 0:
            estado["KingBoo"] = False
            estado["Perder"] = True

        if len(grupo_boss) == 0:
            estado["KingBoo"] = False
            estado["Bowser"] = True
            return

        tela.blit(background, (0, 0))
        # for grupo in [plataformas, tiros, projeteis_inimigos, itens, grupo_boss]:
        #     for entidade in grupo:
        #         tela.blit(entidade.image, (entidade.rect.x, entidade.rect.y))
        tela.blit(player.image, (player.rect.x, player.rect.y))

        desenhar_barra_vida_player(tela, player)
        desenhar_barra_vida_boss(tela, boss, 0)

        pygame.display.update()
        clock.tick(p.FPS)

# -------------------------
# FASE BOWSER FINAL - estática
# -------------------------
def fase_bowser_final(tela, clock, estado):
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

    player = pl.Player(grupos, assets)
    player.rect.bottom = 801.5

    # plataformas = pygame.sprite.Group(
    #     Bloco(500, 700, assets["bloco"]),
    #     Bloco(800, 600, assets["bloco"]),
    #     PlataformaMovel(1000, 550, assets["bloco"], 950, 1150)
    # )

    boss = b.Bowser(assets, grupos)
    grupo_boss = pygame.sprite.Group(boss)

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

        player.update_deslocar(400, 1600)
        player.update_animacao()
        player.update_gravidade(801.5)
        boss.update_comportamento(player)
        tiros.update()
        bolas_de_fogo.update()
        projeteis_inimigos.update()
        # plataformas.update()
        itens.update()

        if player.vida <= 0:
            estado["Bowser"] = False
            estado["Perder"] = True

        if len(grupo_boss) == 0:
            estado["Bowser"] = False
            estado["Venceu"] = True
            return

        tela.blit(background, (0, 0))
        # for grupo in [plataformas, tiros, bolas_de_fogo, projeteis_inimigos, itens, grupo_boss]:
        #     for entidade in grupo:
        #         tela.blit(entidade.image, (entidade.rect.x, entidade.rect.y))
        tela.blit(player.image, (player.rect.x, player.rect.y))

        desenhar_barra_vida_player(tela, player)
        desenhar_barra_vida_boss(tela, boss, 0)

   