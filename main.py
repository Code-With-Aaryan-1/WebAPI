import random
import asyncio
import json
from fastapi import FastAPI, WebSocket
from typing import List

app=FastAPI()

movies=["Inception","Interstellar","Titanic","Avatar","The Dark Knight"]
connected_clients: List[WebSocket]=[]

async def send_movie_data():

  while True:
    if connected_clients:
      movie_data={
        "movie_name": random.choice(movies),
        "user_id":random.randint(1,100),
        "watch_time":random.randint(1,180)
      }
      json_data=json.dumps(movie_data)
      for client in connected_clients:
        await client.send_text(json_data)

  await asyncio.sleep(2)

@app.websocket("/stream")
async def stream_data(websocket:WebSocket):
  await websocket.accept()
  connected_clients.append(websocket)
  print("New Websocket Connection Established")

  try:
    while True:
      await websocket.receive_text()
  except  WebSocketDisconnect: 
      print("Websocket Connection Closed")
  finally:
      conncted_clients.remove(websocket)

@app.on_event("startup")
async def start_stream():
  asyncio.create_task(send_movie_data())
    
