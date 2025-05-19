# importamos as bibliotecas e arquivos necessários para montar a tela inicial
import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b

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
    # colocamos o background na fase
    assets = a.carrega_assets()
    background = assets["fundo mapa"]
    background = pygame.transform.scale(background, (1920, 1080))
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
    chao_y = 800
    player.rect.bottom = chao_y
    # enquanto a fase acontecer
    while estado["DK"]: 
        # analisamos os eventos
        eventos = pygame.event.get()
        # fazemos o boss continuamente atacar 
        boss.update_tiro()
        boss.ataque_chuva()
        # analisamos as teclas que o player pode ativar
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
                    player.pular()
                if evento.key == pygame.K_b: 
                    estado["DK"] = False
                    estado["Bowser"] = True
            if evento.type == pygame.KEYUP: 
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a: 
                    player.speedx += 8
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    player.speedx -= 8
                player.i_animacao = assets["animacao player"]
        # atualizamos na tela o background, as animacoes do player, do boss de dos projéteis
        tela.blit(background, (0, 0))
        player.update_deslocar()
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
                player.vida -= 20
                print(f"Vida do jogador: {player.vida}")
                barril.kill()
        for tiro in tiros:
            if boss.rect.colliderect(tiro.rect):
                dano = getattr(tiro, "dano", 2) 
                boss.levar_dano(dano)
                print(f"Vida do Donkey Kong: {boss.vida}")
                tiro.kill()
        for fogo in foguinho:
            if player.rect.colliderect(fogo.rect):
                player.vida -= 5
                print(f"Vida do jogador: {player.vida}")
                fogo.kill()
        # checando se o player ou o boss morreram (isso muda se a tela será de vitória ou de derrota)
        if player.vida <= 0: 
            estado["DK"] = False
            estado["Perder"] = True
        if boss.vida <= 0: 
            estado["DK"] = False
            estado["Ganhar"] = True
        # atualizando a vida do boss e do player
        desenhar_barra_vida(tela, boss)
        desenhar_barra_vida_player(tela, player)
        # por fim, atualizamos a cada momento o jogo e determinamos sua taxa de atualizacao
        pygame.display.update()
        clock.tick(p.FPS)