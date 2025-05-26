# Fases completas com fase principal e bosses isolados
import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
from Auxiliares import Bloco, PlataformaMovel, PlataformaQuebravel, desenhar_barra_vida_player, desenhar_barra_vida_boss

# -------------------------
# FASE PRINCIPAL - fase_mario
# -------------------------
def fase_mario(tela, clock, estado):
    assets = a.carrega_assets()
    background = assets["fundo mario"]

    tiros = pygame.sprite.Group()
    projeteis_inimigos = pygame.sprite.Group()
    itens = pygame.sprite.Group()
    grupos = {"tiros": tiros, "projeteis_inimigos": projeteis_inimigos, "itens": itens}

    player = pl.Player(grupos, assets)
    player.rect.bottom = 801.5
    camera_x = 0

    plataformas = pygame.sprite.Group(
        Bloco(300, 700, assets["bloco"]),
        PlataformaMovel(500, 650, assets["bloco"], 450, 650),
        PlataformaQuebravel(700, 600, assets["bloco"])
    )

    for i in range(1000, 10000, 1000):
        plataformas.add(Bloco(i, 700, assets["bloco"]))

    while estado["Mario"]:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["Mario"] = False
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

        player.update_deslocar(0, 10000)
        player.update_animacao()
        player.update_gravidade(801.5)
        tiros.update()
        projeteis_inimigos.update()
        plataformas.update()
        itens.update()

        for plataforma in plataformas:
            if player.rect.colliderect(plataforma.rect) and player.speedy >= 0 and player.rect.bottom <= plataforma.rect.bottom:
                player.rect.bottom = plataforma.rect.top
                player.speedy = 0
                player.pulando = False
                if isinstance(plataforma, PlataformaMovel):
                    player.rect.x += plataforma.speed * plataforma.direcao

        if player.vida <= 0:
            estado["Mario"] = False
            estado["Perder"] = True

        target_camera_x = player.rect.centerx - p.WIDHT // 2
        camera_x += (target_camera_x - camera_x) * 0.1

        largura_fundo = background.get_width()
        for i in range(int(camera_x // largura_fundo) - 1, int((camera_x + p.WIDHT) // largura_fundo) + 2):
            tela.blit(background, (i * largura_fundo - camera_x, 0))

        for grupo in [plataformas, tiros, projeteis_inimigos, itens]:
            for entidade in grupo:
                tela.blit(entidade.image, (entidade.rect.x - camera_x, entidade.rect.y))
        tela.blit(player.image, (player.rect.x - camera_x, player.rect.y))
        desenhar_barra_vida_player(tela, player)

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

    plataformas = pygame.sprite.Group(
        Bloco(500, 700, assets["bloco"]),
        Bloco(700, 600, assets["bloco"]),
        PlataformaMovel(900, 650, assets["bloco"], 850, 1050)
    )

    boss = b.BowserJr(assets, grupos)
    grupo_boss = pygame.sprite.Group(boss)

    while estado["BowserJr"]:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["BowserJr"] = False
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

        player.update_deslocar(400, 1600)  # Limita a movimentação
        player.update_animacao()
        player.update_gravidade(801.5)
        boss.update(player)
        tiros.update()
        projeteis_inimigos.update()
        plataformas.update()
        itens.update()

        if player.vida <= 0:
            estado["BowserJr"] = False
            estado["Perder"] = True

        if len(grupo_boss) == 0:
            estado["BowserJr"] = False
            estado["KingBoo"] = True
            return

        tela.blit(background, (0, 0))
        for grupo in [plataformas, tiros, projeteis_inimigos, itens, grupo_boss]:
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

    plataformas = pygame.sprite.Group(
        Bloco(500, 700, assets["bloco"]),
        Bloco(800, 600, assets["bloco"])
    )

    boss = b.KingBoo(assets, grupos)
    grupo_boss = pygame.sprite.Group(boss)

    while estado["KingBoo"]:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["KingBoo"] = False
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
        boss.update(player)
        tiros.update()
        projeteis_inimigos.update()
        plataformas.update()
        itens.update()

        if player.vida <= 0:
            estado["KingBoo"] = False
            estado["Perder"] = True

        if len(grupo_boss) == 0:
            estado["KingBoo"] = False
            estado["Bowser"] = True
            return

        tela.blit(background, (0, 0))
        for grupo in [plataformas, tiros, projeteis_inimigos, itens, grupo_boss]:
            for entidade in grupo:
                tela.blit(entidade.image, (entidade.rect.x, entidade.rect.y))
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

    plataformas = pygame.sprite.Group(
        Bloco(500, 700, assets["bloco"]),
        Bloco(800, 600, assets["bloco"]),
        PlataformaMovel(1000, 550, assets["bloco"], 950, 1150)
    )

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
        plataformas.update()
        itens.update()

        if player.vida <= 0:
            estado["Bowser"] = False
            estado["Perder"] = True

        if len(grupo_boss) == 0:
            estado["Bowser"] = False
            estado["Venceu"] = True
            return

        tela.blit(background, (0, 0))
        for grupo in [plataformas, tiros, bolas_de_fogo, projeteis_inimigos, itens, grupo_boss]:
            for entidade in grupo:
                tela.blit(entidade.image, (entidade.rect.x, entidade.rect.y))
        tela.blit(player.image, (player.rect.x, player.rect.y))

        desenhar_barra_vida_player(tela, player)
        desenhar_barra_vida_boss(tela, boss, 0)

        pygame.display.update()
        clock.tick(p.FPS)

# (continuação do código anterior...)

# -------------------------
# GERENCIADOR DE FASES COM TRANSIÇÃO
# -------------------------
def transicao(tela, clock, texto):
    fonte = pygame.font.SysFont("Arial", 50, bold=True)
    fundo = pygame.Surface((p.WIDHT, p.HEIGHT))
    fundo.fill((0, 0, 0))

    texto_render = fonte.render(texto, True, (255, 255, 255))
    texto_rect = texto_render.get_rect(center=(p.WIDHT // 2, p.HEIGHT // 2))

    tela.blit(fundo, (0, 0))
    tela.blit(texto_render, texto_rect)
    pygame.display.update()
    pygame.time.delay(2500)  # 2.5 segundos

def gerenciador_de_fases(tela, clock):
    estado = {
        "Jogando": True,
        "Mario": True,
        "BowserJr": False,
        "KingBoo": False,
        "Bowser": False,
        "Perder": False,
        "Venceu": False
    }

    transicao(tela, clock, "Prepare-se para a aventura!")
    fase_mario(tela, clock, estado)

    if estado["Perder"]: return
    transicao(tela, clock, "Bowser Jr. está chegando!")
    estado["BowserJr"] = True
    fase_bowser_jr(tela, clock, estado)

    if estado["Perder"]: return
    transicao(tela, clock, "King Boo apareceu!")
    estado["KingBoo"] = True
    fase_king_boo(tela, clock, estado)

    if estado["Perder"]: return
    transicao(tela, clock, "Prepare-se para o Bowser Final!")
    estado["Bowser"] = True
    fase_bowser_final(tela, clock, estado)

    if estado["Venceu"]:
        transicao(tela, clock, "Você venceu todos os chefes!")
    elif estado["Perder"]:
        transicao(tela, clock, "Game Over")

# -------------------------
# FUNÇÃO PRINCIPAL DO JOGO
# -------------------------
def main():
    pygame.init()
    tela = pygame.display.set_mode((p.WIDHT, p.HEIGHT))
    pygame.display.set_caption("Jogo Mario Boss Rush")
    clock = pygame.time.Clock()

    gerenciador_de_fases(tela, clock)

    pygame.quit()

if __name__ == '__main__':
    main()
