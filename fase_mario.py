import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
from bosses import Bowser, PowerUp
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
    pygame.time.delay(3000)

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
    # for i, x in enumerate(range(600, 13000, 450)):  # espaçamento reduzido para mais inimigos
    #     if i % 6 == 0:
    #         inimigos.add(b.Goomba(assets, x, 800))
    #     elif i % 6 == 1:
    #         inimigos.add(b.Koopa(assets, x, 800))
    #     elif i % 6 == 2:
    #         inimigos.add(b.PlantaCarnivora(assets, x, 800))
    #     elif i % 6 == 3:
    #         inimigos.add(b.Goomba(assets, x, 800))
    #         inimigos.add(b.Koopa(assets, x + 50, 800))
    #     elif i % 6 == 4:
    #         inimigos.add(b.PlantaCarnivora(assets, x, 800))
    #         inimigos.add(b.Koopa(assets, x + 50, 800))
    #     else:
    #         inimigos.add(b.Goomba(assets, x, 800))
    #         inimigos.add(b.PlantaCarnivora(assets, x + 50, 800))
    #         inimigos.add(b.PlantaCarnivora(assets, x, 800))
    # Power-up flor fixo
    flor = b.PowerUp("flor", 14050, 700, assets)
    itens.add(flor)
    flor_mensagem_mostrada = False

    # Definição da porta do castelo
    porta_castelo = pygame.Rect(14605, 0, 80, 801.5)

    while estado["Mario"]:
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado["Mario"] = estado["Jogando"] = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_LEFT, pygame.K_a]:
                    player.speedx += -80
                elif evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.speedx += 80
                elif evento.key in [pygame.K_UP, pygame.K_w]:
                    player.pular(121.5)
                    pygame.mixer.Sound("Sprites/smw_jump.wav").play()  # Som de pulo
                elif evento.key == pygame.K_v:
                    player.atirar_especial(player.pegou_flor)
                    if player.pegou_flor:
                        pygame.mixer.Sound("Sprites/smw_fireball.wav").play()  # Som de pulo
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                    player.speedx = 0

        # Atualizações
        player.update_deslocar(0, 15000)
        player.update_animacao()
        player.update_gravidade(801.5)
        tiros.update()
        itens.update()
        for inimigo in inimigos:
            inimigo.update()

        # Colisão com inimigos (ordem ajustada para priorizar o pulo no Koopa)
        for inimigo in inimigos:
            if player.rect.colliderect(inimigo.rect):
                
                # KOOPA
                if isinstance(inimigo, b.Koopa):
                    if player.speedy > 0 and player.rect.bottom - inimigo.rect.top <= 20:
                        inimigo.levar_pulo(player)
                    elif inimigo.estado in ["casco_andando", "vivo"] and not player.invulneravel:
                        player.vida -= inimigo.dano
                        knock_dir = -15 if player.rect.centerx < inimigo.rect.centerx else 15
                        player.knockback(knock_dir)

                # GOOMBA
                elif isinstance(inimigo, b.Goomba):
                    if player.speedy > 0 and player.rect.bottom - inimigo.rect.top <= 20:
                        inimigo.kill()
                        player.speedy = -18
                    elif not player.invulneravel:
                        player.vida -= inimigo.dano
                        knock_dir = -15 if player.rect.centerx < inimigo.rect.centerx else 15
                        player.knockback(knock_dir)

                # OUTROS inimigos com dano direto (ex: Planta)
                elif hasattr(inimigo, "dano") and not player.invulneravel:
                    player.vida -= inimigo.dano
                    knock_dir = -15 if player.rect.centerx < inimigo.rect.centerx else 15
                    player.knockback(knock_dir)



        # Coleta de itens
        for item in itens:
            if player.rect.colliderect(item.rect):
                if item.tipo == "flor":
                    player.pegou_flor = True
                    pygame.mixer.Sound("Sprites/smw_power-up.wav").play()
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
            pygame.mixer.music.stop()
            pygame.display.update()
            pygame.time.delay(100)  # pequena pausa para suavizar a transição
            return

        # Atualização da câmera
        target_camera_x = player.rect.centerx - p.WIDHT // 2
        camera_x += (target_camera_x - camera_x) * 0.1

        # Desenho da tela
        largura_fundo = background.get_width()
        for i in range(int(camera_x // largura_fundo) - 1, int((camera_x + p.WIDHT) // largura_fundo) + 2):
            tela.blit(background, (i * largura_fundo - camera_x, 0))

        tela.blit(castelo_img, (14500 - camera_x, 826.5 - castelo_img.get_height()))


        for grupo in [inimigos, tiros, itens]:
            for entidade in grupo:
                tela.blit(entidade.image, (entidade.rect.x - camera_x, entidade.rect.y))
        tela.blit(player.image, (player.rect.x - camera_x, player.rect.y))
        desenhar_barra_vida_player(tela, player)

        # Mensagem da flor
        if flor_mensagem_mostrada:
            if pygame.time.get_ticks() - flor_msg_timer < 3000:
                # Linha 1 – mensagem de poder
                texto_flor = fonte.render("Você adquiriu o poder de fogo!", True, (255, 0, 0))
                tela.blit(texto_flor, (p.WIDHT // 2 - texto_flor.get_width() // 2, 450))

                # Linha 2 – instruções
                instrucoes = fonte.render("Use a tecla V para atirar", True, (255, 255, 0))
                tela.blit(instrucoes, (p.WIDHT // 2 - instrucoes.get_width() // 2, 500))
            else:
                flor_mensagem_mostrada = False

        pygame.display.update()
        clock.tick(p.FPS)


def fase_bowser(tela, clock, estado):
    """
    Combate único contra o Bowser na sala.
    """
    # Inicialização
    assets = a.carrega_assets()
    bg = assets.get("fundo_bowser", None)
    background = pygame.transform.scale(bg, (p.WIDHT, p.HEIGHT)) if bg else pygame.Surface((p.WIDHT, p.HEIGHT))
    
    # pygame.mixer.music.load(assets.get("bgm_boss", ""))
    # pygame.mixer.music.play(-1)

    # Grupos de sprite
    # Criamos um grupo para todos os sprites para facilitar a atualização e desenho
    all_sprites = pygame.sprite.Group() 
    # Grupo para tiros do jogador
    player_tiros = pygame.sprite.Group() 
    # Grupo para projéteis do Bowser
    bowser_projectiles = pygame.sprite.Group() 

    grupos = {
        "player_tiros": player_tiros,
        "bowser_projectiles": bowser_projectiles,
        "all_sprites": all_sprites, # Adicionado para facilitar
        "room_width": p.WIDHT,
        "room_height": p.HEIGHT,
        "ground_y": p.HEIGHT - 50, # Defina o chão da fase do Bowser
    }

    # Player
    player = pl.Player(grupos, assets)
    player.rect.midbottom = (150, grupos["ground_y"]) # Posiciona o jogador no chão
    all_sprites.add(player)

    # Bowser
    boss = Bowser(assets, grupos)
    all_sprites.add(boss)

    estado['fase_bowser'] = True # Define o estado inicial da fase

    while estado['fase_bowser']:
        dt = clock.tick(p.FPS) / 1000.0  # Calcula o delta tempo em segundos

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                estado['fase_bowser'] = estado['Jogando'] = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key in [pygame.K_LEFT, pygame.K_a]: player.speedx = -250 # Ajustado para dt
                elif ev.key in [pygame.K_RIGHT, pygame.K_d]: player.speedx = 250 # Ajustado para dt
                elif ev.key in [pygame.K_UP, pygame.K_w]: 
                    player.pular(350) # Ajustado para dt
                    pygame.mixer.Sound(assets.get("smw_jump", "")).play() # Som de pulo
                elif ev.key == pygame.K_z: 
                    player.atirar()
                    pygame.mixer.Sound(player.som_tiro).play() # Som de tiro
                elif ev.key == pygame.K_v: # Adicionado tiro especial
                    player.atirar_especial(player.pegou_flor)
                    if player.pegou_flor:
                        pygame.mixer.Sound(player.som_tiroespecial).play() # Som de tiro especial
            elif ev.type == pygame.KEYUP:
                if ev.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                    player.speedx = 0

        # Atualizações
        # Passa dt para as funções de update que precisam dele
        player.update_deslocar_fixo(dt) # Usa update_deslocar_fixo para movimento sem limites de tela
        player.update_gravidade(grupos["ground_y"], dt) 
        player.update_animacao() # A animação não precisa de dt, mas é bom chamá-la aqui
        
        player_tiros.update(dt) # Atualiza os tiros do player
        bowser_projectiles.update(dt) # Atualiza os projéteis do Bowser
        boss.update(player, dt) # Atualiza o Bowser e seus ataques

        # Colisões inimigo (projéteis do Bowser) ← player
        for proj in bowser_projectiles:
            if player.rect.colliderect(proj.rect):
                player.take_damage(proj.dmg)
                proj.kill() # Remove o projétil após a colisão

        # Colisões boss ← player tiro
        for tiro in player_tiros:
            if boss.rect.colliderect(tiro.rect):
                boss.take_damage(tiro.dano) # Use 'dano' para tiros do player
                tiro.kill()

        # Desenho
        tela.blit(background, (0, 0))
        # Desenha todos os sprites nos grupos
        for s in all_sprites:
            tela.blit(s.image, s.rect)
        for s in player_tiros: # Desenha os tiros do jogador
            tela.blit(s.image, s.rect)
        for s in bowser_projectiles: # Desenha os projéteis do Bowser
            tela.blit(s.image, s.rect)


        # HUD
        desenhar_barra_vida_player(tela, player)
        desenhar_barra_vida_boss (tela, boss, p.WIDHT - 300) # Ajuste a posição da barra de vida do boss

        pygame.display.flip()

        # Checa fim de combate
        if player.vida <= 0:
            estado['fase_bowser'] = False
            estado['Perder'] = True
        elif boss.vida <= 0:
            estado['fase_bowser'] = False
            estado['Vencer'] = True
        
    pygame.mixer.music.stop()