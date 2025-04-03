import asyncio
import json
from pygame import Vector2
import websockets



from client.Projectile import Projectile
from client.Tank.Tank import Tank
from models.Models import ProjectileListModel, TanksListModel


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

def parse_tanks(json_str: str) -> set[Tank]:
    data = json.loads(json_str)
    tanks = set()
    for tank_data in data:
        tank_data['position'] = Vector2(**tank_data['position'])
        tank_data['rotate'] = Vector2(**tank_data['rotate'])
        tank_data['direction'] = Vector2(**tank_data['direction'])
        tanks.add(Tank(**tank_data))
    return tanks

def parse_projectiles(json_str: str) -> set[Projectile]:
    data = json.loads(json_str)
    for proj_data in data:
        proj_data['position'] = Vector2(**proj_data['position'])
        proj_data['rotate'] = Vector2(**proj_data['rotate'])
    return {Projectile(**p) for p in data}
    
class WSHandler():
    def __init__(self, ws):
        self.ws = ws
        from client.Tank.Tank import Tank
        self.players_list: set[Tank] = []
        self.projectile_list: set[Tank] = []
        
    async def receive_messages(self):
        async for message in self.ws:
            try:
                data = json.loads(message)
                if 'player_list' in data:
                    self.players_list = parse_tanks(data['player_list'])
                if 'projectile_list' in data:
                    self.projectile_list = parse_projectiles(data['projectile_list'])
                
            except Exception as e:
                print(f"Error receiving message: {e}")

    async def send_message(self, message):
        await self.ws.send(message)

async def startGame(wsHandler):
    from client.Game import Game
    game = Game(wsHandler)
    await game.start_game()

async def main():
    ws = await websockets.connect("ws://localhost:8765")
    wsHandler = WSHandler(ws)
    receive_task = asyncio.create_task(wsHandler.receive_messages())
    sender_task = asyncio.create_task(startGame(wsHandler))
    await asyncio.gather(receive_task, sender_task)
    
if __name__ == "__main__":
    asyncio.run(main())