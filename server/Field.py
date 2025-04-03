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
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.players_list: list[Tank] = []
        self.projectile_list = []
    
    def update(self):
        self.players_list.sort(key=lambda player: player.score)
        self.players_list: list[Tank]= [p for p in self.players_list if p.id in id_players_dict]

        for player in self.players_list:
            self.check_boundaries(player)
            self.start_eat_food(player)

            for other_player in self.players_list:
                if(player.check_player_eat(other_player)):
                    player.score += other_player.score
                    self.players_list.remove(other_player)
                    id_players_dict[other_player.id].remove(other_player)

            if(player.division_flag):
                player.division_flag = False
                if len(id_players_dict[player.id]) < 16:
                    part = player.division(self.players_list)
                    if part:
                        id_players_dict[part.id].append(part)

            player.update()

    async def check_game_over(self):
        disconnected_players = [pid for pid in id_players_dict if not id_players_dict[pid]]
        for player_id in disconnected_players:
            client = next((k for k, v in clients_players_dict.items() if v == player_id), None)
            if client:
                await send_message(client, {"game_over": True}) 
                print("game over sent to", player_id)
            
            id_players_dict.pop(player_id) 
            await self.add_new_player(client)

    async def check_new_clients(self):
        new_clients = [c for c in clients if c not in clients_players_dict]
        for client in new_clients:
            await self.add_new_player(client)
                
    def check_boundaries(self, player: Unit):
        player.pos.x = max(player.get_radius(), min(self.WIDTH - player.get_radius(), player.pos.x))
        player.pos.y = max(player.get_radius(), min(self.HEIGHT - player.get_radius(), player.pos.y))

    async def add_new_player(self, client):
        free_id = next(i for i in range(1, 10000) if i not in id_players_dict)
    
        nickname = client_nickname_dict.get(client, "unknown")
        player = Tank( nickname=nickname, id=free_id)

        margin = 50
        player.pos = pygame.math.Vector2(
                random.randint(margin, WINDOW_HEIGHT - margin),
                random.randint(margin, WINDOW_HEIGHT - margin))
        
        self.players_list.append(player)
        id_players_dict.setdefault(free_id, []).append(player)

        clients_players_dict[client] = player.id
        await send_message(client, {"player_id": player.id})