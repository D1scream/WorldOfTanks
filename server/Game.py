import asyncio
import random
import pygame

from server.Field import Field
from models.Models import TanksListModel, ProjectileListModel
from server.Tank import Tank

FIELD_WIDTH, FIELD_HEIGHT = 600, 600
class Game():
    def __init__(self,wsController):
        self.start_game()
        self.wsController = wsController
        self.clients_players_dict = {}
        self.clients = set()
        self.id_players_dict = {}
        self.client_nickname_dict = {}
    
    async def start_game(self):
        print("Server Started")
        self.field = await self.create_field()
        running = True
        while running:
            asyncio.create_task(self.send_game_state())
            self.field.update()
            await asyncio.sleep(1/60)

    async def send_game_state(self):
        players_data = TanksListModel(self.field.players_list)
        projectile_data = ProjectileListModel(self.field.projectile_list)
        data = {"player_list" : players_data.to_json(), "projectile_list": projectile_data.to_json()}

        await self.check_new_clients()
        await self.check_game_over()
        self.field.update()
        await self.wsController.send_message_to_all(data)

    async def create_field(self):
        field = Field(FIELD_WIDTH, FIELD_HEIGHT, self.id_players_dict, self.clients_players_dict)
        await asyncio.gather(
            *(self.add_new_player(client) for client in self.clients))
            
        return field
    
    async def check_game_over(self):
            disconnected_players = [pid for pid in self.id_players_dict if not self.id_players_dict[pid]]
            for player_id in disconnected_players:
                client = next((k for k, v in self.clients_players_dict.items() if v == player_id), None)
                if client:
                    await self.wsController.send_message(client, {"game_over": True}) 
                    print("game over sent to", player_id)
                
                self.id_players_dict.pop(player_id) 
                await self.add_new_player(client)

    async def check_new_clients(self):
        new_clients = [c for c in self.clients if c not in self.clients_players_dict]
        for client in new_clients:
            await self.add_new_player(client)
                
    async def add_new_player(self, client):
        free_id = next(i for i in range(1, 10000) if i not in self.id_players_dict)
    
        nickname = self.client_nickname_dict.get(client, "unknown")
        player = Tank( nickname=nickname, id=free_id)

        margin = 50
        player.pos = pygame.math.Vector2(
                random.randint(margin, FIELD_HEIGHT - margin),
                random.randint(margin, FIELD_HEIGHT - margin))
        
        self.players_list.append(player)
        self.id_players_dict.setdefault(free_id, []).append(player)

        self.clients_players_dict[client] = player.id
        await self.wsController.send_message(client, {"player_id": player.id})
