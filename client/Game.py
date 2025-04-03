import asyncio
import pygame


from client.Tank.ControlledTank import ControlledTank
from client.Tank.Control import Control, Keyset
from client.Field import Field


class Game():
    def __init__(self, wsHandler):
        from Client import WSHandler
        self.wsHandler: WSHandler = wsHandler
        
    async def start_game(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("World Of Tanks")
        field = Field(self.wsHandler)
        player_wasd_keyset = Keyset(
            key_up = pygame.K_w,
            key_down = pygame.K_s,
            key_left = pygame.K_a,
            key_right = pygame.K_d,
            key_division = pygame.K_SPACE
            )
    
        controllerWASD = Control(player_wasd_keyset)
        player = ControlledTank(controller=controllerWASD, wsHandler = self.wsHandler)
        player.position = pygame.Vector2(300,300)
        field.player = player
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            await field.update()
            field.draw(screen)

            pygame.display.flip()
            await asyncio.sleep(1/60)

        pygame.quit()
