import pygame

from client.Field import Field
from models.Models import TanksListModel, ProjectileListModel


class Game():
    def __init__(self,wsController):
        self.start_game()
        self.wsController = wsController
    
    def start_game(self):
        
        self.field = Field()
        clock = pygame.time.Clock()
        running = True
        print("ServerStarted")
        while running:
            self.field.update()
            clock.tick(60)

    async def send_game_state(self,field : Field):
        players_data = TanksListModel(field.players_list)
        projectile_data = ProjectileListModel(field.projectile_list)
        data = {"player_list" : players_data.to_json(), "projectile_list": projectile_data.to_json()}

        await field.check_new_clients()
        await field.check_game_over()

        await self.wsController.send_message_to_all(data)
