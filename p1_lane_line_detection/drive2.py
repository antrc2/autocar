import asyncio
import websockets
import json
import time
async def echo(websocket, path):
    with open('data.txt', mode='r', encoding='utf-8') as f:
        data = f.read().split("\n")
    for i in data:
        new_data = i.split()
        throttle = new_data[0]
        steering_angle = new_data[1]
        ti = float(new_data[2])  # Thời gian ngắt quãng khi gửi socket
          # Gửi Socket lên sau mỗi ti
        # time.sleep(ti)
        message = json.dumps({"throttle": throttle, "steering": steering_angle})
        await asyncio.sleep(ti)
        await websocket.send(message)
        

async def main():
    async with websockets.serve(echo, "0.0.0.0", 4567, ping_interval=None):
        await asyncio.Future()
asyncio.run(main())
