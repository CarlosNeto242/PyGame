# importamos as bibliotecas e arquivos necessários para montar a tela inicial
import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b

pygame.init()
pygame.font.init()
pygame.mixer.init()

def desenhar_barra_vida(tela, boss):
    largura = 400
    altura = 30
    x = (p.WIDHT - largura) // 2
    y = 20
    vida_percent = boss.vida / boss.max_vida
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura)) 
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura * vida_percent, altura)) 
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 4) 

def desenhar_barra_vida_player(tela, player):
    largura = 200
    altura = 20
    x = 50
    y = 20
    vida_percent = player.vida / player.max_vida
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura))  
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura * vida_percent, altura))  
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 3)  

def fase_bowser(tela, clock, estado):
    pegou_flor = False
    mostrando_texto = False
    tempo_texto = 0
    pode_usar_fogo = False
    bowser = False

    assets = a.carrega_assets()
    background = assets["fundo mario"]

    tiros = pygame.sprite.Group()
    bolas_de_fogo = pygame.sprite.Group()
    grupos = {"tiros": tiros, "bolas_de_fogo": bolas_de_fogo}

    player = pl.Player(grupos, assets) 
    # bowser = b.Bowser(assets, grupos)
    flor = b.FlorDeFogo(400, 800) 
    grupo_floresta = pygame.sprite.Group()
    grupo_floresta.add(flor)

    chao_y = 801.5
    player.rect.bottom = chao_y

    camera_x = 0

    while estado["Bowser"]: 
        eventos = pygame.event.get()
        if not pegou_flor and player.rect.colliderect(flor.rect):
            pegou_flor = True
            mostrando_texto = True
            tempo_texto = pygame.time.get_ticks()
            grupo_floresta.remove(flor)

        # if not mostrando_texto and not pode_usar_fogo:
        #     bowser.update_comportamento(player)

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
                    player.atirar()
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    player.pular()
                if evento.key == pygame.K_c:
                    player.atirar_especial(pegou_flor)
            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                    player.speedx = 0
                player.i_animacao = assets["animacao player"]
        if bowser:
            limite_direito=0
            limite_esquerdo=100000
        else:
            limite_direito=0
            limite_esquerdo=100000
        player.update_deslocar(limite_direito, limite_esquerdo)
        player.update_animacao()
        player.update_gravidade(chao_y)
        bolas_de_fogo.update()
        tiros.update()

        target_camera_x = player.rect.centerx - p.WIDHT // 2
        camera_x += (target_camera_x - camera_x) * 0.1

        largura_fundo = background.get_width()
        inicio = int(camera_x // largura_fundo) - 1
        fim = int((camera_x + p.WIDHT) // largura_fundo) + 2

        for i in range(inicio, fim):
            x_pos = i * largura_fundo - camera_x
            tela.blit(background, (x_pos, 0))

        for flor in grupo_floresta:
            tela.blit(flor.image, (flor.rect.x - camera_x, flor.rect.y))

        tela.blit(player.image, (player.rect.x - camera_x, player.rect.y))
        # tela.blit(bowser.image, (bowser.rect.x - camera_x, bowser.rect.y))
        for tiro in tiros:
            tela.blit(tiro.image, (tiro.rect.x - camera_x, tiro.rect.y))
        for bola in bolas_de_fogo:
            tela.blit(bola.image, (bola.rect.x - camera_x, bola.rect.y))

        for bola in bolas_de_fogo:
            if player.rect.colliderect(bola.rect):
                player.vida -= 10
                bola.kill()
        # for tiro in tiros:
        #     if bowser.rect.colliderect(tiro.rect):
        #         dano = getattr(tiro, "dano", 10)
        #         bowser.levar_dano(dano)
        #         tiro.kill()

        if player.vida <= 0: 
            estado["Bowser"] = False
            estado["Perder"] = True
        # if bowser.vida <= 0: 
        #     estado["Bowser"] = False
        #     estado["Ganhar"] = True

        # desenhar_barra_vida(tela, bowser)
        desenhar_barra_vida_player(tela, player)

        if mostrando_texto:
            fonte = pygame.font.SysFont("Arial", 40)
            texto1 = fonte.render("Você adquiriu um novo poder: Tiro de Fogo!", True, (255, 255, 0))
            texto2 = fonte.render("Use o botão C para disparar. Requer tempo de recarga.", True, (255, 255, 0))
            tela.blit(texto1, ((p.WIDHT - texto1.get_width()) // 2, 300))
            tela.blit(texto2, ((p.WIDHT - texto2.get_width()) // 2, 360))

            if pygame.time.get_ticks() - tempo_texto > 4000:
                mostrando_texto = False
                pode_usar_fogo = True

        pygame.display.update()
        clock.tick(p.FPS)