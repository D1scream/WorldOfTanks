import random
from client.Projectile import Projectile
from client.Tank.Tank import Tank

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
            
        to_remove = []
        for projectile in self.projectile_list:
            projectile.update()

            if not (0 <= projectile.position.x <= self.width and 0 <= projectile.position.y <= self.height):
                to_remove.append(projectile)
        for projectile in to_remove:
            self.projectile_list.remove(projectile)
            

class Field:
    def __init__(self, WIDTH, HEIGHT, id_players_dict, clients_players_dict):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.players_list: list[Tank] = []
        self.projectile_list = []
        self.id_players_dict = id_players_dict
        self.clients_players_dict = clients_players_dict
    
    def update(self, ):
        self.players_list.sort(key=lambda player: player.score)
        self.players_list: list[Tank]= [p for p in self.players_list if p.id in self.id_players_dict]

        for player in self.players_list:
            self.check_boundaries(player)
            self.start_eat_food(player)

            for other_player in self.players_list:
                if(player.check_player_eat(other_player)):
                    player.score += other_player.score
                    self.players_list.remove(other_player)
                    self.id_players_dict[other_player.id].remove(other_player)

            if(player.division_flag):
                player.division_flag = False
                if len(self.check_boundariesid_players_dict[player.id]) < 16:
                    part = player.division(self.players_list)
                    if part:
                        self.id_players_dict[part.id].append(part)

            player.update()

    # def check_boundaries(self, player: Tank):
    #     player.pos.x = max(player.get_radius(), min(self.WIDTH - player.get_radius(), player.pos.x))
    #     player.pos.y = max(player.get_radius(), min(self.HEIGHT - player.get_radius(), player.pos.y))