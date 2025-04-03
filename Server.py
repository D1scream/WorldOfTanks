import asyncio
from pygame import Vector2
import websockets
import json

from server.Tank.Tank import Tank


class WSController():
    def __init__(self):
        self.active_connections = set()
        self.con_to_id = {}
        self.id_players_dict = {}

    async def remove_connection(self, websocket):
        try:
            player_id = self.con_to_id.get(websocket)
            self.active_connections.discard(websocket)
            
            if websocket in self.con_to_id:
                del self.con_to_id[websocket]
            
            if player_id in self.id_players_dict:
                del self.id_players_dict[player_id]
                
                
            print(f"{len(self.active_connections)} {len(self.con_to_id)} {len(self.id_players_dict)}")
                
        except Exception as e:
            print(f"Error removing connection: {e}")
            

    async def send_message(self, websocket, message):
        try:
            await websocket.send(json.dumps(message))
        except websockets.exceptions.ConnectionClosed:
            print(f"Client disconnected, cant send message")
            return False
        return True

    async def send_message_to_all(self, message):
        await asyncio.gather(
            *(self.send_message(connection, message) for connection in self.active_connections))

    async def validate_message(self, data):
        if not isinstance(data, dict):
            raise ValueError("Invalid message format")
        if 'nickname' not in data or 'direction' not in data:
            raise ValueError("Missing required fields: nickname and direction")
        if not data['direction'].strip():
            raise ValueError("Message direction cannot be empty")

    async def websocket_handler(self, websocket, path=""):
        print("Server started on ws://localhost:8765")
        self.active_connections.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    #await self.validate_message(data)
                        
                    if 'direction' in data:
                        x,y = data['direction']
                        player_id = self.con_to_id[websocket]
                        player: Tank = self.id_players_dict[player_id]
                        player.direction = Vector2(x, y)
                        player.shoot_flag = data['shoot']
                        
                except Exception as e:
                    print(f"Unexpected error: {str(e)}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Internal server error"
                    }))

        except websockets.exceptions.ConnectionClosed:
            await self.remove_connection(websocket)

async def main():
    wsController = WSController()
    from server.Game import Game
    game = Game(wsController)
    server_task = websockets.serve(wsController.websocket_handler, "localhost", 8765)

    server = await server_task
    print("Server started on ws://localhost:8765")
    await asyncio.gather(server.wait_closed(), game.start_game())

if __name__ == "__main__":
    asyncio.run(main())