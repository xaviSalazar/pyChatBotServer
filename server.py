#!/usr/bin/env python

import asyncio
import websockets
# importing chat script in python 
from chat import get_response
# websocket implementation 
import os
import signal
# import logging
# import redis
# import gevent
# from flask import Flask, render_template
# from flask_sockets import Sockets

# REDIS_URL = os.environ['REDIS_URL']
# REDIS_CHAN = 'chat'

# app = Flask(__name__)
# app.debug = 'DEBUG' in os.environ

# sockets = Sockets(app)
# redis = redis.from_url(REDIS_URL)

# Response message server
async def server(websocket):
    async for message in websocket:
        answer = get_response(message)
        await websocket.send(answer)

async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        server,
        host="",
        port=int(os.environ["PORT"]),
    ):
        await stop
        # await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

# class ChatBackend(object):
#     """Interface for registering and updating WebSocket clients."""

#     def __init__(self):
#         self.clients = list()
#         self.pubsub = redis.pubsub()
#         self.pubsub.subscribe(REDIS_CHAN)

#     def __iter_data(self):
#         for message in self.pubsub.listen():
#             data = message.get('data')
#             if message['type'] == 'message':
#                 app.logger.info(u'Sending message: {}'.format(data))
#                 yield data

#     def register(self, client):
#         """Register a WebSocket connection for Redis updates."""
#         self.clients.append(client)

#     def send(self, client, data):
#         """Send given data to the registered client.
#         Automatically discards invalid connections."""
#         try:
#             client.send(data)
#         except Exception:
#             self.clients.remove(client)

#     def run(self):
#         """Listens for new messages in Redis, and sends them to clients."""
#         for data in self.__iter_data():
#             for client in self.clients:
#                 gevent.spawn(self.send, client, data)

#     def start(self):
#         """Maintains Redis subscription in the background."""
#         gevent.spawn(self.run)

# chats = ChatBackend()
# chats.start()


# @app.route('/')
# def hello():
#     return render_template('chat_client.html')

# @sockets.route('/submit')
# def inbox(ws):
#     """Receives incoming chat messages, inserts them into Redis."""
#     while not ws.closed:
#         # Sleep to prevent *constant* context-switches.
#         gevent.sleep(0.1)
#         message = ws.receive()

#         if message:
#             app.logger.info(u'Inserting message: {}'.format(message))
#             redis.publish(REDIS_CHAN, message)

# @sockets.route('/receive')
# def outbox(ws):
#     """Sends outgoing chat messages, via `ChatBackend`."""
#     chats.register(ws)

#     while not ws.closed:
#         # Context switch while `ChatBackend.start` is running in the background.
#         gevent.sleep(0.1)