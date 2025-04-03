
from server.Projectile import Projectile
from server.Tank.Tank import Tank

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

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
        
        projectiles_to_remove = []
        tanks_to_remove = set() 
        
        for projectile in self.projectile_list:
            projectile.update()
            
            if not (0 <= projectile.position.x <= self.width and 
                    0 <= projectile.position.y <= self.height):
                projectiles_to_remove.append(projectile)
                continue
            
            for tank in self.tank_list:
                if tank in tanks_to_remove:
                    continue
                    
                if self.check_collision(projectile, tank):
                    tanks_to_remove.add(tank)
                    projectiles_to_remove.append(projectile)
                    break 
        
        for projectile in projectiles_to_remove:
            if projectile in self.projectile_list: 
                self.projectile_list.remove(projectile)
        
        for tank in tanks_to_remove:
            if tank in self.tank_list:
                self.tank_list.remove(tank)

    def check_collision(self, projectile: Projectile, tank: Tank):
        distance = (projectile.position - tank.position).length()
        return distance < max(tank.collision_radius, projectile.collision_radius)
            

    # def check_boundaries(self, player: Tank):
    #     player.pos.x = max(player.get_radius(), min(self.WIDTH - player.get_radius(), player.pos.x))
    #     player.pos.y = max(player.get_radius(), min(self.HEIGHT - player.get_radius(), player.pos.y))