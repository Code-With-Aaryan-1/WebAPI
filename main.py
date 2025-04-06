
import random
import asyncio
import json
from fastapi import FastAPI, WebSocket
from typing import List
import uvicorn

app = FastAPI()

movies = ["Inception", "Interstellar", "Titanic", "Avatar", "The Dark Knight"]
connected_clients: List[WebSocket] = []


@app.get("/")
async def root():
    return {"message":"Websocket server is live"}

async def send_movie_data():
    while True:
        if connected_clients:
            movie_data = {
                "movie_name": random.choice(movies),
                "user_id": random.randint(1, 100),
                "watch_time": random.randint(1, 180)
            }
            json_data = json.dumps(movie_data)
            for client in connected_clients:
                await client.send_text(json_data)
        await asyncio.sleep(2)

@app.websocket("/stream/")
async def stream_data(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print("New Websocket Connection Established")

    try:
        while True:
            await asyncio.sleep(10)
    except Exception:
        pass
    finally:
        connected_clients.remove(websocket)

@app.on_event("startup")
async def startup():
    asyncio.create_task(send_movie_data())

if __name__ == "__main__":
    port = 10000
    uvicorn.run(app, host="0.0.0.0", port=port)
