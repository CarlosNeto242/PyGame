import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b

pygame.init()
pygame.font.init()
pygame.mixer.init()

def fase_bowser(tela, clock, estado):
    assets = a.carrega_assets()
    background = assets["fundo mapa"]
    background = pygame.transform.scale(background, (1920, 1080))

    tiros = pygame.sprite.Group()
    bolas_de_fogo = pygame.sprite.Group()

    grupos = {}
    grupos["tiros"] = tiros
    grupos["bolas_de_fogo"] = bolas_de_fogo

    player = pl.Player(grupos, assets)
    bowser = b.Bowser(assets, grupos)

    chao_y = 800
    player.rect.bottom = chao_y

    while estado["Bowser"]: 
        eventos = pygame.event.get()
        bowser.update_ataque()

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
            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_a]:
                    player.speedx += 8
                if evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.speedx -= 8
                player.i_animacao = assets["animacao player"]

        # Atualizações
        player.update_deslocar()
        player.update_animacao()
        player.update_gravidade(chao_y)
        bolas_de_fogo.update()
        tiros.update()

        # Desenho
        tela.blit(background, (0, 0))
        tela.blit(player.image, player.rect)
        tela.blit(bowser.image, bowser.rect)
        tiros.draw(tela)
        bolas_de_fogo.draw(tela)
        pygame.display.update()
        clock.tick(p.FPS)
