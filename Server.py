import asyncio
import websockets
import json

from server.Game import Game
class WSController():
    def __init__(self):
        self.active_connections = set()
        self.con_to_nickname = {}

    async def remove_connection(self, websocket):
        if websocket in self.con_to_nickname:
            nickname = self.con_to_nickname[websocket]
            del self.con_to_nickname[websocket]
            await self.send_message_to_all({"content": "disconnect", "nickname": nickname})
        self.active_connections.discard(websocket)

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
        if 'nickname' not in data or 'content' not in data:
            raise ValueError("Missing required fields: nickname and content")
        if not data['nickname'].strip():
            raise ValueError("Nickname cannot be empty")
        if not data['content'].strip():
            raise ValueError("Message content cannot be empty")

    async def websocket_handler(self, websocket, path=""):
        self.active_connections.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.validate_message(data)
                    
                    nickname = data['nickname']
                    message_content = data['content']
                    self.con_to_nickname[websocket] = nickname
                    print(f"{nickname} sending: {message_content}")
                    await asyncio.gather(*[self.send_message(con, data) for con in self.active_connections if con != websocket])

                except Exception as e:
                    print(f"Unexpected error: {str(e)}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Internal server error"
                    }))

        except websockets.exceptions.ConnectionClosed:
            print(f"User {self.con_to_nickname.get(websocket, 'Unknown')} disconnected")
            await self.remove_connection(websocket)

async def main():
    wsController = WSController()
    game = Game(wsController)
    asyncio.create_task(game.start_game()) 
    server = await websockets.serve(wsController.websocket_handler, "localhost", 8765)
    print("Server started on ws://localhost:8765")
    await server.wait_closed()
    
if __name__ == "__main__":
    asyncio.run(main())