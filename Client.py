import asyncio
import json
import pygame
import websockets

from client.Game import Game

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
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

async def startGame(ws):
    nickname = input("MyCoolNick")
    game = Game(ws)

async def main():
    ws = await websockets.connect("ws://localhost:8765")
    receive_task = asyncio.create_task(receive_messages(ws))
    sender_task = asyncio.create_task(startGame(ws))
    await asyncio.gather(receive_task, sender_task)
    
asyncio.run(main())