import asyncio
import random
import pygame

from Server import WSController
from server.Field import Field
from models.Models import TanksListModel, ProjectileListModel
from server.Tank.Tank import Tank

FIELD_WIDTH, FIELD_HEIGHT = 600, 600
class Game():
    def __init__(self,wsController):
        self.start_game()
        self.wsController: WSController = wsController
    
    async def start_game(self):
        print("Server Started")
        self.field: Field = await self.create_field()
        running = True
        while running:
            asyncio.create_task(self.send_game_state())
            self.field.update()
            await asyncio.sleep(1/60)

    async def send_game_state(self):
        players_data = TanksListModel(self.field.tank_list)
        projectile_data = ProjectileListModel(self.field.projectile_list)
        data = {"player_list" : players_data.to_json(), "projectile_list": projectile_data.to_json()}

        await self.check_new_connections()
        await self.check_game_over()
        self.field.update()
        await self.wsController.send_message_to_all(data)

    async def create_field(self):
        field = Field()
        await asyncio.gather(
            *(self.add_new_player(client) for client in self.wsController.active_connections))
            
        return field
    
    async def check_game_over(self):
            disconnected_players = [pid for pid in self.wsController.id_players_dict if not self.wsController.id_players_dict[pid]]
            for player_id in disconnected_players:
                client = next((k for k, v in self.wsController.con_to_id.items() if v == player_id), None)
                if client:
                    await self.wsController.send_message(client, {"game_over": True}) 
                    print("game over sent to", player_id)
                
                self.wsController.id_players_dict.pop(player_id) 
                await self.add_new_player(client)

    async def check_new_connections(self):
        new_clients = [c for c in self.wsController.active_connections if c not in self.wsController.con_to_id]
        for client in new_clients:
            await self.add_new_player(client)
                
    async def add_new_player(self, con):
        free_id = next(i for i in range(1, 10000) if i not in self.wsController.id_players_dict)
    
        player = Tank(id=free_id)

        margin = 50
        player.pos = pygame.math.Vector2(
                random.randint(margin, FIELD_HEIGHT - margin),
                random.randint(margin, FIELD_HEIGHT - margin))
        
        self.field.tank_list.add(player)
        self.wsController.id_players_dict[player.id] = player

        self.wsController.con_to_id[con] = player.id
        await self.wsController.send_message(con, {"player_id": player.id})
