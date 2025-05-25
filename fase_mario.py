# FASE UNIFICADA DE MARIO - COM COMENTÁRIOS
# Inclui: limite de tela de 20000, colisão com plataformas, eliminação de Goombas ao pisar,
# os três chefes (Bowser Jr, King Boo e Bowser), e código comentado.

import pygame
import math
import random
import parametros as p
import assets as a
import player as pl
import bosses as b
from plataformas import Bloco, PlataformaMovel, PlataformaQuebravel

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Desenha a barra de vida do jogador
def desenhar_barra_vida_player(tela, player):
    largura = 200
    altura = 20
    x = 50
    y = 20
    vida_percent = player.vida / player.max_vida
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura))  # fundo vermelho
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura * vida_percent, altura))  # vida verde
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 3)  # borda

# Desenha a barra de vida do boss ativo
def desenhar_barra_vida_boss(tela, boss, camera_x):
    largura = 400
    altura = 30
    x = boss.rect.centerx - camera_x - largura // 2
    y = boss.rect.top - 50
    vida_percent = boss.vida / boss.max_vida
    pygame.draw.rect(tela, (100, 0, 0), (x, y, largura, altura))
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura * vida_percent, altura))
    pygame.draw.rect(tela, (255, 255, 255), (x, y, largura, altura), 3)
    fonte = pygame.font.SysFont("Arial", 24, bold=True)
    texto = fonte.render(f"{type(boss).__name__}", True, (255, 255, 255))
    tela.blit(texto, (x + largura // 2 - texto.get_width() // 2, y - 30))

def fase_bowser(tela, clock, estado):
    # Constantes da fase
    LIMITE_FASE_DIREITA = 20000
    LIMITE_BOSS_JR = 10000
    LIMITE_KING_BOO = 15000
    LIMITE_BOWSER = 18000

    # Flags de controle de estado
    pegou_flor = False
    mostrando_texto = False
    semtiro_texto = False
    tempo_texto = 0
    boss_ativo = None
    fase_parada = False
    boss_derrotado = False
    mostrando_transicao = False
    transicao_tempo = 0

    # Carrega recursos
    assets = a.carrega_assets()
    background = assets["fundo mario"]

    # Grupos de sprites
    tiros = pygame.sprite.Group()
    bolas_de_fogo = pygame.sprite.Group()
    projeteis_inimigos = pygame.sprite.Group()
    itens = pygame.sprite.Group()
    grupos = {"tiros": tiros, "bolas_de_fogo": bolas_de_fogo, "projeteis_inimigos": projeteis_inimigos, "itens": itens}

    # Inicializa jogador e flor
    player = pl.Player(grupos, assets)
    flor = b.FlorDeFogo(400, 800)
    grupo_floresta = pygame.sprite.Group(flor)

    # Inicializa bosses
    bowser_jr = b.BowserJr(assets, grupos)
    king_boo = b.KingBoo(assets, grupos)
    bowser = b.Bowser(assets, grupos)
    grupo_boss = pygame.sprite.Group()

    # Plataformas
    plataformas = pygame.sprite.Group(
        Bloco(300, 700, assets["bloco"]),
        Bloco(500, 600, assets["bloco"]),
        Bloco(700, 500, assets["bloco"]),
        PlataformaMovel(1000, 650, assets["bloco"], 950, 1150),
        PlataformaQuebravel(1200, 400, assets["bloco"]),
        PlataformaQuebravel(1300, 400, assets["bloco"])
    )

    # Plataformas ao longo da fase
    for i in range(1500, LIMITE_FASE_DIREITA, 1000):
        if random.random() < 0.7:
            y = random.randint(400, 700)
            plataformas.add(Bloco(i, y, assets["bloco"]))
            if random.random() < 0.3:
                plataformas.add(PlataformaQuebravel(i + 100, y - 100, assets["bloco"]))

    # Posição inicial do jogador
    chao_y = 801.5
    player.rect.bottom = chao_y
    camera_x = 0

    # Inimigos ao longo da fase
    inimigos = pygame.sprite.Group()
    for i in range(400, LIMITE_FASE_DIREITA, 800):
        tipo = random.choice([b.Goomba, b.PlantaCarnivora])
        y = chao_y if tipo == b.Goomba else chao_y - 50
        inimigos.add(tipo(assets, i, y))

    while estado["Bowser"]:
        eventos = pygame.event.get()

        # Trigger dos chefes
        if not fase_parada and not boss_derrotado and not mostrando_transicao:
            if player.rect.centerx >= LIMITE_BOSS_JR and boss_ativo is None:
                boss_ativo = "BowserJr"
                fase_parada = True
                grupo_boss.add(bowser_jr)
                mostrando_transicao = True
                transicao_tempo = pygame.time.get_ticks()
            elif player.rect.centerx >= LIMITE_KING_BOO and boss_ativo == "BowserJr":
                boss_ativo = "KingBoo"
                fase_parada = True
                grupo_boss.add(king_boo)
                mostrando_transicao = True
                transicao_tempo = pygame.time.get_ticks()
            elif player.rect.centerx >= LIMITE_BOWSER and boss_ativo == "KingBoo":
                boss_ativo = "Bowser"
                fase_parada = True
                grupo_boss.add(bowser)
                mostrando_transicao = True
                transicao_tempo = pygame.time.get_ticks()

        # Derrota do boss
        if fase_parada and len(grupo_boss) == 0 and not mostrando_transicao:
            boss_derrotado = True
            fase_parada = False
            mostrando_transicao = True
            transicao_tempo = pygame.time.get_ticks()
            if boss_ativo == "Bowser":
                estado["Bowser"] = False
                estado["Venceu"] = True

        # Fim da transição
        if mostrando_transicao and pygame.time.get_ticks() - transicao_tempo > 3000:
            mostrando_transicao = False
            if boss_derrotado:
                boss_derrotado = False
                boss_ativo = None

        # Coleta da flor
        if not pegou_flor and player.rect.colliderect(flor.rect):
            pegou_flor = True
            mostrando_texto = True
            tempo_texto = pygame.time.get_ticks()
            grupo_floresta.remove(flor)

        # Eventos de teclado
        for evento in eventos:
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["Bowser"] = False
            if evento.type == pygame.KEYDOWN:
                if fase_parada:
                    continue
                if evento.key in [pygame.K_LEFT, pygame.K_a]:
                    player.speedx -= 5
                if evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.speedx += 5
                if evento.key == pygame.K_v:
                    if not pegou_flor:
                        semtiro_texto = True
                        tempo_texto = pygame.time.get_ticks()
                    else:
                        player.atirar_especial(pegou_flor)
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    player.pular()
            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                    player.speedx = 0
                player.i_animacao = assets["animacao player"]

        # Atualizações de jogo
        if not fase_parada and not mostrando_transicao:
            player.update_deslocar(0, LIMITE_FASE_DIREITA)
        player.update_animacao()
        player.update_gravidade(chao_y)
        tiros.update()
        bolas_de_fogo.update()
        projeteis_inimigos.update()
        plataformas.update()
        inimigos.update()
        itens.update()

        # Atualiza boss ativo
        if boss_ativo == "BowserJr":
            bowser_jr.update(player)
        elif boss_ativo == "KingBoo":
            king_boo.update(player)
        elif boss_ativo == "Bowser":
            bowser.update_comportamento(player)

        # Colisões de dano
        for hit in pygame.sprite.spritecollide(player, projeteis_inimigos, True):
            player.vida -= 10
            player.knockback(10 if hit.rect.centerx < player.rect.centerx else -10)

        for plataforma in plataformas:
            if player.rect.colliderect(plataforma.rect) and player.speedy >= 0 and player.rect.bottom <= plataforma.rect.bottom:
                player.rect.bottom = plataforma.rect.top
                player.speedy = 0
                player.pulando = False
                if isinstance(plataforma, PlataformaMovel):
                    player.rect.x += plataforma.speed * plataforma.direcao
                elif isinstance(plataforma, PlataformaQuebravel):
                    plataforma.pisando = True
                    if plataforma.tempo_pisado == 0:
                        plataforma.tempo_pisado = pygame.time.get_ticks()

        # Colisão com Goomba por pulo
        for enemy in pygame.sprite.spritecollide(player, inimigos, False):
            if isinstance(enemy, b.Goomba) and player.speedy > 0:
                enemy.kill()
                player.speedy = -5
            else:
                direcao = 1 if player.rect.centerx < enemy.rect.centerx else -1
                player.knockback_x = -direcao * 10
                player.knockback_frames = 5
                player.vida -= enemy.dano * 0.1

        if player.vida <= 0:
            estado["Bowser"] = False
            estado["Perder"] = True

        # Câmera
        if fase_parada and not mostrando_transicao:
            if boss_ativo == "BowserJr":
                target_camera_x = LIMITE_BOSS_JR - p.WIDHT // 2
            elif boss_ativo == "KingBoo":
                target_camera_x = LIMITE_KING_BOO - p.WIDHT // 2
            elif boss_ativo == "Bowser":
                target_camera_x = LIMITE_BOWSER - p.WIDHT // 2
        else:
            target_camera_x = player.rect.centerx - p.WIDHT // 2
        camera_x += (target_camera_x - camera_x) * 0.1

        # Desenhos na tela
        largura_fundo = background.get_width()
        for i in range(int(camera_x // largura_fundo) - 1, int((camera_x + p.WIDHT) // largura_fundo) + 2):
            tela.blit(background, (i * largura_fundo - camera_x, 0))

        for grupo in [plataformas, inimigos, grupo_floresta, tiros, bolas_de_fogo, projeteis_inimigos, itens, grupo_boss]:
            for entidade in grupo:
                tela.blit(entidade.image, (entidade.rect.x - camera_x, entidade.rect.y))

        tela.blit(player.image, (player.rect.x - camera_x, player.rect.y))
        desenhar_barra_vida_player(tela, player)

        # Vida do boss
        if fase_parada and boss_ativo and not mostrando_transicao:
            desenhar_barra_vida_boss(tela, grupo_boss.sprites()[0], camera_x)

        # Textos
        if mostrando_texto and pygame.time.get_ticks() - tempo_texto < 4000:
            fonte = pygame.font.SysFont("Arial", 40)
            tela.blit(fonte.render("Você adquiriu um novo poder: Tiro de Fogo!", True, (255, 255, 0)), (250, 300))
            tela.blit(fonte.render("Use o botão C para disparar. Requer tempo de recarga.", True, (255, 255, 0)), (100, 360))
        elif semtiro_texto and pygame.time.get_ticks() - tempo_texto < 4000:
            fonte = pygame.font.SysFont("Arial", 40)
            tela.blit(fonte.render("Parece que o meu tiro normal não funciona nesse mundo", True, (255, 255, 0)), (100, 300))
            tela.blit(fonte.render("Tenho que descobrir outra forma de eliminar os inimigos!", True, (255, 255, 0)), (100, 360))

        # Transições
        if mostrando_transicao:
            fonte = pygame.font.SysFont("Arial", 50, bold=True)
            if boss_derrotado:
                mensagens = {
                    "BowserJr": "Bowser Jr. Derrotado! Prepare-se para King Boo!",
                    "KingBoo": "King Boo Derrotado! Enfrente Bowser Final!",
                }
                texto = mensagens.get(boss_ativo, "")
            else:
                mensagens = {
                    "BowserJr": "Bowser Jr. Apareceu!",
                    "KingBoo": "King Boo Apareceu!",
                    "Bowser": "BOWSER FINAL!",
                }
                texto = mensagens.get(boss_ativo, "")
            if texto:
                fundo = pygame.Surface((p.WIDHT, 100), pygame.SRCALPHA)
                fundo.fill((0, 0, 0, 180))
                tela.blit(fundo, (0, 300))
                tela.blit(fonte.render(texto, True, (255, 255, 255)), ((p.WIDHT - 600) // 2, 310))

        pygame.display.update()
        clock.tick(p.FPS)
