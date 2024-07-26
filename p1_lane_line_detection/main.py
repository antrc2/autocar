import asyncio
import websockets
from PIL import Image
import json
import cv2
import numpy as np
import base64
from io import BytesIO
import time
import keyboard
from lane_line_detection import calculate_control_signal

running = False

async def echo(websocket, path):
    async for message in websocket:
        # Get image from simulation
        data = json.loads(message)
        image = Image.open(BytesIO(base64.b64decode(data["image"])))
        image = np.asarray(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Prepare visualization image
        draw = image.copy()
        
        # Send back throttle and steering angle
        throttle, steering_angle = calculate_control_signal(image, draw=draw)

        # Show the result to a window
        cv2.imshow("Result", draw)
        cv2.waitKey(1)
        
        # Send back throttle and steering angle
        message = json.dumps({"throttle": throttle, "steering": steering_angle})
        # print(message)
        
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "0.0.0.0", 4567, ping_interval=None):
        await asyncio.Future()  # run forever

def check():
    global running
    if keyboard.is_pressed("c") and not running:
        running = True
        asyncio.run(main())
    elif keyboard.is_pressed("x"):
        running = False
        asyncio.get_event_loop().stop()
        cv2.destroyAllWindows()
        exit()

if __name__ == "__main__":
    while True:
        check()
        time.sleep(0.1)
