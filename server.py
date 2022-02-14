#!/usr/bin/env python

import asyncio
import websockets
# importing chat script in python 
from chat import get_response

async def server(websocket):
    async for message in websocket:
        answer = get_response(message)
        await websocket.send(answer)

async def main():
    async with websockets.serve(server, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())