import pygame
import parametros as p
import assets as a
import player as pl

pygame.init()

def mapa(tela, clock, estado): 
    assets = a.carrega_assets()
    background = assets["fundo mapa"]
    background = pygame.transform.scale(background, (1920, 1080))
    player = pl.Player()
    while estado["Mapa"]: 

        eventos = pygame.event.get()

        for evento in eventos: 
            if evento.type == pygame.QUIT:
                estado["Jogando"] = False
                estado["Mapa"] = False
            if evento.type == pygame.KEYDOWN: 
                if evento.key == pygame.K_LEFT: 
                    player.speedx -= 8
                if evento.key == pygame.K_RIGHT:
                    player.speedx += 8
            if evento.type == pygame.KEYUP: 
                if evento.key == pygame.K_LEFT: 
                    player.speedx += 8
                if evento.key == pygame.K_RIGHT:
                    player.speedx -= 8 
        tela.blit(background, (0, 0))
        tela.blit(player.image, (player.rect.x, 700))
        player.update_deslocar()
        player.update_animacao()
        pygame.display.update()
        clock.tick(p.FPS)