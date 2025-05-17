import pygame
import parametros as p
import assets as a
import player as pl
import bosses as b

pygame.init()
pygame.font.init()
pygame.mixer.init()

def mapa(tela, clock, estado): 
    assets = a.carrega_assets()
    background = assets["fundo mapa"]
    background = pygame.transform.scale(background, (1920, 1080))
    tiros = pygame.sprite.Group()
    barris = pygame.sprite.Group()
    grupos = {}
    grupos["tiros"] = tiros
    grupos["barris"] = barris
    player = pl.Player(grupos, assets)
    boss = b.Boss(assets, grupos)
    chao_y = 800
    player.rect.bottom = chao_y
    checador = 0
    while estado["Mapa"]: 
        eventos = pygame.event.get()
        boss.update_tiro()
        checador += 1
        for evento in eventos: 
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["Mapa"] = False
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
                    estado["Mapa"] = False
                    estado["Bowser"] = True
            if evento.type == pygame.KEYUP: 
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a: 
                    player.speedx += 8
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    player.speedx -= 8
                player.i_animacao = assets["animacao player"]

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
        pygame.display.update()
        clock.tick(p.FPS)