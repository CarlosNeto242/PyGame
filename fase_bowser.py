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
def fase_bowser(tela, clock, estado):
      # colocamos o background na fase
    assets = a.carrega_assets()
    background = assets["fundo mario"]
    background = pygame.transform.scale(background, (1920, 1080))
    # criamos grupos associados as sprites "disparadas" no jogo
    tiros = pygame.sprite.Group()
    bolas_de_fogo = pygame.sprite.Group()
    grupos = {}
    grupos["tiros"] = tiros
    grupos["bolas_de_fogo"] = bolas_de_fogo
    # declarando as entidades principais do jogo com base nas classes criadas
    player = pl.Player(grupos, assets)
    bowser = b.Bowser(assets, grupos)
    # criando um chão
    chao_y = 800
    player.rect.bottom = chao_y
    # enquanto a fase acontecer
    while estado["Bowser"]: 
        # analisamos os eventos
        eventos = pygame.event.get()
        # fazemos o boss continuamente atacar
        bowser.update_comportamento(player)
        # analisamos as teclas que o player pode ativar
        for evento in eventos:
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["Bowser"] = False
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_LEFT, pygame.K_a]:
                    player.speedx -= 8
                if evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.speedx += 8
                if evento.key == pygame.K_v:
                    player.atirar()
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    player.pular()
                if evento.key == pygame.K_c:
                    player.atirar_especial()
            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_a]:
                    player.speedx += 8
                if evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.speedx -= 8
                player.i_animacao = assets["animacao player"]
        # atualizamos na tela o background, as animacoes do player, do boss de dos projéteis
        player.update_deslocar()
        player.update_animacao()
        player.update_gravidade(chao_y)
        bolas_de_fogo.update()
        tiros.update()
        tela.blit(background, (0, 0))
        tela.blit(player.image, player.rect)
        tela.blit(bowser.image, bowser.rect)
        tiros.draw(tela)
        bolas_de_fogo.draw(tela)
         # checamos as diferentes hitboxes possíveis
        for bola in bolas_de_fogo:
            if player.rect.colliderect(bola.rect):
                player.vida -= 10
                print(f"Vida do jogador: {player.vida}")
                bola.kill()
        for tiro in tiros:
            if bowser.rect.colliderect(tiro.rect):
                dano = getattr(tiro, "dano", 10) 
                bowser.levar_dano(dano)
                print(f"Vida do Bowser: {bowser.vida}")
                tiro.kill()
        # checando se o player ou o boss morreram (isso muda se a tela será de vitória ou de derrota)
        if player.vida <= 0: 
            estado["Bowser"] = False
            estado["Perder"] = True
        if bowser.vida <= 0: 
            estado["Bowser"] = False
            estado["Ganhar"] = True
        # atualizando a vida do boss e do player
        desenhar_barra_vida(tela, bowser)
        desenhar_barra_vida_player(tela, player)
        # por fim, atualizamos a cada momento o jogo e determinamos sua taxa de atualizacao
        pygame.display.update()
        clock.tick(p.FPS)
