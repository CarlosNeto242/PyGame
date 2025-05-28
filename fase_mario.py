# importamos as bibliotecas e arquivos necessários para criar os bosses do jogo
import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
from bosses import Bowser, PowerUp
from Auxiliares import desenhar_barra_vida_player, desenhar_barra_vida_boss
import random
# criando uma função para a fase
def fase_mario(tela, clock, estado):
    
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
    base_texto_intro = "Invasão de jogo em processamento" # Texto base sem os pontos

    # Define a duração total da tela de introdução em milissegundos
    duracao_total_intro = 3000 # 3 segundos (como o seu delay original)
    tempo_inicial = pygame.time.get_ticks()

    frame_atual_pontos = 0
    intervalo_animacao_pontos = 500 # 500 milissegundos para cada mudança de ponto

    while pygame.time.get_ticks() - tempo_inicial < duracao_total_intro:
        # Lidar com eventos para que a janela não congele
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                # É importante permitir que o usuário feche o jogo
                # mesmo durante a introdução.
                estado["Mario"] = estado["Jogando"] = False
                return # Sai da função fase_mario

        # Atualiza a animação dos pontos
        agora = pygame.time.get_ticks()
        if agora - tempo_inicial > frame_atual_pontos * intervalo_animacao_pontos:
            frame_atual_pontos += 1
            # Garante que os pontos se repetem de forma cíclica (., .., ...)
            num_pontos = (frame_atual_pontos % 3) + 1
            pontos = "." * num_pontos
            texto_completo = base_texto_intro + pontos
            
            texto_intro = fonte.render(texto_completo, True, (255, 255, 255))
            
            # Limpa a tela e redesenha o texto
            tela.fill((0, 0, 0)) 
            tela.blit(texto_intro, (p.WIDHT // 2 - texto_intro.get_width() // 2, p.HEIGHT // 2))
            pygame.display.update()

        # Pequena pausa para evitar que o loop rode muito rápido e consuma CPU
        pygame.time.delay(10) # Ajuste este valor se precisar

    # Após o tempo total, o texto final (com os últimos pontos) estará na tela
    # e o código continuará para a próxima mensagem.

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
    for i, x in enumerate(range(600, 13000, 350)):  # espaçamento reduzido para mais inimigos
        if i % 6 == 0:
            inimigos.add(b.Goomba(assets, x, 800))
        elif i % 6 == 1:
            inimigos.add(b.Koopa(assets, x, 800))
        elif i % 6 == 2:
            inimigos.add(b.PlantaCarnivora(assets, x, 800))
        elif i % 6 == 3:
            inimigos.add(b.Goomba(assets, x, 800))
            inimigos.add(b.Koopa(assets, x + 50, 800))
        elif i % 6 == 4:
            inimigos.add(b.PlantaCarnivora(assets, x, 800))
            inimigos.add(b.Koopa(assets, x + 50, 800))
        else:
            inimigos.add(b.Goomba(assets, x, 800))
            inimigos.add(b.PlantaCarnivora(assets, x + 50, 800))
            inimigos.add(b.PlantaCarnivora(assets, x, 800))
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
                    player.speedx += -11
                elif evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.speedx += 11
                elif evento.key in [pygame.K_UP, pygame.K_w]:
                    player.pular(21.5)
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
            estado["DK"] = True
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
    return player

