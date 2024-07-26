import asyncio
import websockets
import json
import time
def list_line():
    with open('data.txt', mode='r', encoding='utf-8') as f:
        data = f.read().split("\n")
        return data[0]
# async def echo(websocket, path):
#     a=list_line()
#     print(a)
#     nowTime = time.time()
#     time.sleep(5)
#     new_data = a.split()
#     throttle = new_data[0]
#     steering_angle = new_data[1]
#     ti = float(new_data[2])  # Thời gian ngắt quãng khi gửi socket
#       # Gửi Socket lên sau mỗi ti
#     # time.sleep(ti)
#     message = json.dumps({"throttle": throttle, "steering": steering_angle})
#     print(message)
#     # await asyncio.sleep(ti)
#     time.sleep(ti)
#     # message=""
#     # message = json.dumps({"throttle": 0.5, "steering": -10})
#     await websocket.send(message)
#     print(f"Lần {throttle} {steering_angle} {time.time() - nowTime}\n")
ti=0
i=0
async def echo(websocket, path):
    global ti,i
    with open('data.txt', mode='r', encoding='utf-8') as f:
        data = f.read().split("\n")
        # print(data)
        # for i in data:
        
        async for message in websocket:
            if i<len(data)-1:
                
                throttle = float(data[i].split()[0])
                steering_angle = float(data[i].split()[1])
                i+=1
                print(i)
            else :
                throttle =0
                steering_angle=0
            # ti += 1
            # print(ti)
            message = json.dumps({"throttle": throttle, "steering": steering_angle})
            print(message)

            await websocket.send(message)
async def main():
    time.sleep(5)
    async with websockets.serve(echo, "0.0.0.0", 4567, ping_interval=None):
        await asyncio.Future()
asyncio.run(main())
# f = open("data.txt","r")
# data = f.read().split("\n")
# for i in data:
#     print(i)