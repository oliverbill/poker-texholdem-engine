import asyncio
import pathlib
import ssl
import websockets

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhost_pem)

async def hello():
    uri = "wss://localhost:8765"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)

        greeting = await websocket.recv()
        print(f" {greeting}")

#PUBLIC_CHANNEL_URI = "wss://demo.piesocket.com/v3/channel_123?api_key=VCXCEuvhGcBDP7XhiJJUDvR1e1D3eiVjgZ9VRiaV&notify_self"
#CHANNEL_URI = "wss://s8170.nyc1.piesocket.com/v3/1?api_key=FgLxflYzLhuBijqtJhU2VPqSbC2WyF7zzlSdjfet&notify_self=1"

asyncio.run(hello())
