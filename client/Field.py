from Client import WSHandler
from client.Projectile import Projectile
from client.Tank.Tank import Tank


class Field():

    def __init__(self, wsHandler: WSHandler):
        self.width: int = 600
        self.height: int = 600
        self.tank_list: set[Tank] = set()
        self.projectile_list: set[Projectile] = set()
        self.wsHandler = wsHandler
        self.player: Tank
        
    async def update(self):
        self.tank_list = self.wsHandler.players_list
        self.projectile_list = self.wsHandler.projectile_list
        await self.player.update()
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        for tank in self.tank_list:
            tank.draw(screen)

        for projectile in self.projectile_list:
            projectile.draw(screen)
        
        
    
    