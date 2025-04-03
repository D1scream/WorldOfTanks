import pygame

from client.Tank.ControlledTank import ControlledTank
from client.Tank.Control import Control, Keyset
from client.Field import Field


class Game():
    def __init__(self, ws):
        self.ws = ws
        
    
    async def start_game(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("World Of Tanks")
        field = Field()
        player_wasd_keyset = Keyset(
            key_up = pygame.K_w,
            key_down = pygame.K_s,
            key_left = pygame.K_a,
            key_right = pygame.K_d,
            key_division = pygame.K_SPACE
            )
    
        controllerWASD = Control(player_wasd_keyset)
        player = ControlledTank(controller=controllerWASD, ws = self.ws)
        player.position = pygame.Vector2(300,300)
        field.tank_list.add(player)
        
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            await field.update()
            field.draw(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
