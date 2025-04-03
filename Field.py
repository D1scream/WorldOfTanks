from Projectile import Projectile
from Tank.Tank import Tank


class Field():
    def __init__(self):
        self.width: int = 600
        self.height: int = 600
        self.tank_list: set[Tank] = set()
        self.projectile_list: set[Projectile] = set()
        
    def update(self):
        for tank in self.tank_list:
            projectile = tank.update()
            if projectile:
                self.projectile_list.add(projectile)
            
        to_remove = []
        for projectile in self.projectile_list:
            projectile.update()

            if not (0 <= projectile.position.x <= self.width and 0 <= projectile.position.y <= self.height):
                to_remove.append(projectile)
        for projectile in to_remove:
            self.projectile_list.remove(projectile)
            
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        for tank in self.tank_list:
            tank.draw(screen)

        for projectile in self.projectile_list:
            projectile.draw(screen)
        
        
    
    