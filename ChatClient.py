import asyncio
import json
import websockets
import aioconsole

async def receive_messages(ws):
    async for message in ws:
        try:
            data = json.loads(message)
            print(f"\n{data['nickname']}: {data['content']}")
            print("enter message:", end=" ")               
        except Exception as e:
            print(f"Error receiving message: {e}")
async def send_message(ws, message):
    await ws.send(json.dumps(message))

async def sender(ws):
    nickname = input("enter your nick: ")
    while True:
        print("enter message1: ", end="")
        console_input = await aioconsole.ainput()
        await send_message(ws, {'nickname' : nickname, 'content' : console_input})

async def main():
    ws = await websockets.connect("ws://localhost:8765")
    receive_task = asyncio.create_task(receive_messages(ws))
    sender_task = asyncio.create_task(sender(ws))
    await asyncio.gather(receive_task, sender_task)
    
asyncio.run(main())