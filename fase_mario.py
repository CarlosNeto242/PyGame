# ===============================
# 1. IMPORTAÇÃO E INICIALIZAÇÃO
# ===============================
import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
from plataformas import Bloco, PlataformaMovel, PlataformaQuebravel

pygame.init()
pygame.font.init()
pygame.mixer.init()

# =============================================
# 2. FUNÇÕES AUXILIARES: BARRAS DE VIDA NA TELA
# =============================================
def desenhar_barra_vida_player(tela, player):
    largura = 200
    altura = 20
    x = 50
    y = 20
    vida_percent = player.vida / player.max_vida
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura))  
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura * vida_percent, altura))  
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 3)  

# =============================
# 3. FUNÇÃO PRINCIPAL DA FASE
# =============================
def fase_bowser(tela, clock, estado):
    pegou_flor = False
    mostrando_texto = False
    semtiro_texto = False
    tempo_texto = 0

    # --- 3.2 Carregamento de assets ---
    assets = a.carrega_assets()
    background = assets["fundo mario"]

    # --- 3.3 Criação dos grupos de sprites ---
    tiros = pygame.sprite.Group()
    bolas_de_fogo = pygame.sprite.Group()
    grupos = {"tiros": tiros, "bolas_de_fogo": bolas_de_fogo}

    player = pl.Player(grupos, assets) 
    flor = b.FlorDeFogo(400, 800) 
    grupo_floresta = pygame.sprite.Group()
    grupo_floresta.add(flor)

    plataformas = pygame.sprite.Group()
    plataformas.add(Bloco(400, 700, assets["bloco"]))
    plataformas.add(PlataformaMovel(800, 650, assets["bloco"], 750, 1000))
    plataformas.add(PlataformaQuebravel(600, 750, assets["bloco"]))

    chao_y = 801.5
    player.rect.bottom = chao_y

    camera_x = 0

    # --- 3.4 Spawn de mais inimigos ---
    
    inimigos = pygame.sprite.Group()
    inimigos_list = [
        # (b.PlantaCarnivora, 400, chao_y),
        # (b.Goomba, 500, chao_y),
        # (b.PlantaCarnivora, 800, chao_y)
    ]

    for classe, x, y in inimigos_list:
        inimigos.add(classe(assets, x, y))

    # ==============================
    # 4. LOOP PRINCIPAL DA FASE
    # ==============================
    while estado["Bowser"]:
        eventos = pygame.event.get()

        # --- 4.1 Coleta da flor de fogo ---
        if not pegou_flor and player.rect.colliderect(flor.rect):
            pegou_flor = True
            mostrando_texto = True
            tempo_texto = pygame.time.get_ticks()
            grupo_floresta.remove(flor)

        # --- 4.2 Eventos do teclado ---
        for evento in eventos:
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["Bowser"] = False
            if evento.type == pygame.KEYDOWN:
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

        # --- 4.3 Atualizações de estado ---
        player.update_deslocar(0, 100000)
        player.update_animacao()
        player.update_gravidade(chao_y)
        bolas_de_fogo.update()
        tiros.update()
        inimigos.update()
        plataformas.update()

        # --- 4.4 Colisão entre tiros e plataformas ---
        for tiro in tiros:
            blocos_colididos = pygame.sprite.spritecollide(tiro, plataformas, False)
            if blocos_colididos:
                tiro.kill()

        # --- 4.5 Jogador pisa em plataformas móveis ---
        for plataforma in plataformas:
            if isinstance(plataforma, PlataformaMovel):
                if player.rect.colliderect(plataforma.rect) and player.speedy >= 0 and player.rect.bottom <= plataforma.rect.bottom:
                    player.rect.bottom = plataforma.rect.top
                    player.speedy = 0
                    player.pulando = False
                    player.rect.x += plataforma.speed * plataforma.direcao

        # --- 4.6 Atualização da câmera ---
        target_camera_x = player.rect.centerx - p.WIDHT // 2
        camera_x += (target_camera_x - camera_x) * 0.1

        # --- 4.7 Fundo infinito ---
        largura_fundo = background.get_width()
        inicio = int(camera_x // largura_fundo) - 1
        fim = int((camera_x + p.WIDHT) // largura_fundo) + 2

        for i in range(inicio, fim):
            x_pos = i * largura_fundo - camera_x
            tela.blit(background, (x_pos, 0))

        # --- 4.8 Desenho dos elementos ---
        for flor in grupo_floresta:
            tela.blit(flor.image, (flor.rect.x - camera_x, flor.rect.y))

        for plataforma in plataformas:
            tela.blit(plataforma.image, (plataforma.rect.x - camera_x, plataforma.rect.y))

        for inimigo in inimigos:
            tela.blit(inimigo.image, (inimigo.rect.x - camera_x, inimigo.rect.y))

        tela.blit(player.image, (player.rect.x - camera_x, player.rect.y))

        for tiro in tiros:
            tela.blit(tiro.image, (tiro.rect.x - camera_x, tiro.rect.y))
        for bola in bolas_de_fogo:
            tela.blit(bola.image, (bola.rect.x - camera_x, bola.rect.y))

        # --- 4.9 Colisões com bolas de fogo ---
        for bola in bolas_de_fogo:
            if player.rect.colliderect(bola.rect):
                player.vida -= 10
                bola.kill()

        # --- 4.10 Colisão com inimigos ---
        enemy_hits = pygame.sprite.spritecollide(player, inimigos, False)
        for enemy in enemy_hits:
            if isinstance(enemy, b.Goomba) and player.speedy > 0:
                enemy.kill()
                player.speedy = -5
            else:
                direcao = 1 if player.rect.centerx < enemy.rect.centerx else -1
                player.knockback_x = -direcao * 10
                player.knockback_frames = 5
                player.vida -= enemy.dano * 0.1

        # --- 4.11 Fim de jogo ---
        if player.vida <= 0:
            estado["Bowser"] = False
            estado["Perder"] = True

        # --- 4.12 Interface e textos ---
        desenhar_barra_vida_player(tela, player)

        if mostrando_texto:
            fonte = pygame.font.SysFont("Arial", 40)
            texto1 = fonte.render("Você adquiriu um novo poder: Tiro de Fogo!", True, (255, 255, 0))
            texto2 = fonte.render("Use o botão C para disparar. Requer tempo de recarga.", True, (255, 255, 0))
            tela.blit(texto1, ((p.WIDHT - texto1.get_width()) // 2, 300))
            tela.blit(texto2, ((p.WIDHT - texto2.get_width()) // 2, 360))
            if pygame.time.get_ticks() - tempo_texto > 4000:
                mostrando_texto = False

        if semtiro_texto:
            fonte = pygame.font.SysFont("Arial", 40)
            texto1 = fonte.render("Parece que o meu tiro normal não funciona nesse mundo", True, (255, 255, 0))
            texto2 = fonte.render("Tenho que descobrir outra forma de eliminar os inimigos!", True, (255, 255, 0))
            tela.blit(texto1, ((p.WIDHT - texto1.get_width()) // 2, 300))
            tela.blit(texto2, ((p.WIDHT - texto2.get_width()) // 2, 360))
            if pygame.time.get_ticks() - tempo_texto > 4000:
                semtiro_texto = False

        pygame.display.update()
        clock.tick(p.FPS)
