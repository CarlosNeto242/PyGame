# importamos as bibliotecas e arquivos necessários para montar a fase do Donkey Kong
import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b
import random 

pygame.init()
pygame.font.init()
pygame.mixer.init()
# definimos uma função que desenha a barra de vida do boss na tela
def desenhar_barra_vida(tela, boss):
    largura = 400
    altura = 30
    x = (p.WIDHT - largura) // 2
    y = 20
    vida_percent = boss.vida / boss.max_vida
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura)) 
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura * vida_percent, altura)) 
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 4)
# definimos uma função que desenha a barra de vida do player na tela
def desenhar_barra_vida_player(tela, player):
    largura = 200
    altura = 20
    x = 50
    y = 20
    vida_percent = player.vida / player.max_vida
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura))  
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura * vida_percent, altura))  
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 3)  
# definimos uma função que rodará o principal da fase 
def mapa(tela, clock, estado): 
    pygame.mixer.music.load('Sprites/Sound Effects/bgm_action_3.mp3')
    pygame.mixer.music.play(loops=-1)
    # colocamos o background na fase
    assets = a.carrega_assets()
    background = assets["fundo mapa"]
    background = pygame.transform.scale(background, (1920, 1080))
    loading = assets["loading dk"]
    loading = pygame.transform.scale(loading, (p.WIDHT, p.HEIGHT))
    fonte = pygame.font.Font("Fontes/PressStart2P.ttf", 30)
    # criamos grupos associados as sprites "disparadas" no jogo
    tiros = pygame.sprite.Group()
    barris = pygame.sprite.Group()
    foguinho = pygame.sprite.Group()
    grupos = {}
    grupos["tiros"] = tiros
    grupos["barris"] = barris
    grupos["foguinhos"] = foguinho
    # declarando as entidades principais do jogo com base nas classes criadas
    player = pl.Player(grupos, assets)
    boss = b.Boss(assets, grupos)
    # criando um chão
    chao_y = 830
    player.rect.bottom = chao_y
    # enquanto a fase acontecer

    tela.blit(loading, (0, 0))
    texto_intro = fonte.render("Invasão de jogo em processamento...", True, (255, 255, 255))
    tela.blit(texto_intro, (p.WIDHT // 2 - texto_intro.get_width() // 2, p.HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)

    fonte = pygame.font.Font("Fontes/PressStart2P.ttf", 20)
    tela.blit(background, (0, 0))
    texto_alerta = fonte.render(
        "Donkey Kong está furioso pelo Mario ter sumido, e acha que VOCÊ É O CULPADO!",
        True, (255, 255, 255)
    )
    tela.blit(texto_alerta, (p.WIDHT // 2 - texto_alerta.get_width() // 2, p.HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(3000)
    while estado["DK"]: 
        # analisamos os eventos
        eventos = pygame.event.get()
        # fazemos o boss continuamente atacar 
        boss.update_tiro()
        # analisamos as teclas que o player pode ativar e relacionamos aos seus respectivos eventos
        for evento in eventos: 
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["DK"] = False
            if evento.type == pygame.KEYDOWN: 
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    player.speedx -= 8
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    player.speedx += 8
                if evento.key == pygame.K_v:
                    player.atirar()
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    player.pular(20)
                if evento.key == pygame.K_b: 
                    estado["DK"] = False
                    estado["Bowser"] = True
                if evento.key == pygame.K_c:
                    player.atirar_especial(True)
            if evento.type == pygame.KEYUP: 
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a: 
                    player.speedx += 8
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    player.speedx -= 8
                player.i_animacao = assets["animacao player"]
            if  boss.vida <= boss.max_vida * 0.8:
                boss.ataque_chuva(100, 1700,4)
        # atualizamos na tela o background, as animacoes do player, do boss de dos projéteis
        tela.fill((0, 0, 0))
        tela.blit(background, (0, 0))
        player.update_deslocar_fixo()
        player.update_animacao()
        player.update_gravidade(chao_y)
        tela.blit(player.image, player.rect)
        tela.blit(boss.image, boss.rect)
        tiros.update()
        tiros.draw(tela)
        barris.update()
        barris.draw(tela)
        foguinho.update()
        foguinho.draw(tela)
        # checamos as diferentes hitboxes possíveis 
        for barril in barris:
            if player.rect.colliderect(barril.rect):
                player.vida -= 10
                barril.kill()
                assets["som de dano"].play()
        for tiro in tiros:
            if boss.rect.colliderect(tiro.rect):
                dano = getattr(tiro, "dano", 1) 
                boss.levar_dano(dano)
                tiro.kill()
        for fogo in foguinho:
            if player.rect.colliderect(fogo.rect):
                player.vida -= 5
                fogo.kill()
                assets["som de dano"].play()
        # checando se o player ou o boss morreram (isso muda se a tela será de vitória ou de derrota)
        if player.vida <= 0: 
            estado["DK"] = False
            estado["Perder"] = True
            pygame.mixer.music.stop()
        if boss.vida <= 0: 
            estado["DK"] = False
            estado["Ganhar"] = True
            pygame.mixer.music.stop()
        # atualizando a vida do boss e do player
        desenhar_barra_vida(tela, boss)
        desenhar_barra_vida_player(tela, player)
        # por fim, atualizamos a cada momento o jogo e determinamos sua taxa de atualizacao
        pygame.display.update()
        clock.tick(p.FPS)