import asyncio
import websockets
import json

async def remove_connection(websocket):
    if websocket in con_to_nickname:
        nickname = con_to_nickname[websocket]
        del con_to_nickname[websocket]
        await send_message_to_all({"content": "disconnect", "nickname": nickname})
    active_connections.discard(websocket)

async def send_message(websocket, message):
    try:
        await websocket.send(json.dumps(message))
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected, cant send message")
        return False
    return True

async def send_message_to_all(message):
    await asyncio.gather(
        *(send_message(connection, message) for connection in active_connections))

active_connections = set()
con_to_nickname = {}

async def validate_message(data):
    if not isinstance(data, dict):
        raise ValueError("Invalid message format")
    if 'nickname' not in data or 'content' not in data:
        raise ValueError("Missing required fields: nickname and content")
    if not data['nickname'].strip():
        raise ValueError("Nickname cannot be empty")
    if not data['content'].strip():
        raise ValueError("Message content cannot be empty")

async def websocket_handler(websocket, path=""):
    active_connections.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                await validate_message(data)
                
                nickname = data['nickname']
                message_content = data['content']
                con_to_nickname[websocket] = nickname
                print(f"{nickname} sending: {message_content}")
                await asyncio.gather(*[send_message(con, data) for con in active_connections if con != websocket])

            except json.JSONDecodeError:
                print("JSON decode error")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
            except ValueError as e:
                print(f"Validation error: {str(e)}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": str(e)
                }))
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Internal server error"
                }))

    except websockets.exceptions.ConnectionClosed:
        print(f"User {con_to_nickname.get(websocket, 'Unknown')} disconnected")
        await remove_connection(websocket)

async def main():
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    print("Server started on ws://localhost:8765")
    await server.wait_closed()
    
if __name__ == "__main__":
    asyncio.run(main())