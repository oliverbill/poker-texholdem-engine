import asyncio
import pathlib
import ssl
import websockets
async def hello(websocket):
    name = await websocket.recv()
    print(f"Name received: {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"Greeting sent: {greeting}")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_cert_chain(localhost_pem)
async def main():
    async with websockets.serve(hello, "localhost", 8765, ssl=ssl_context):
        await asyncio.Future()  # run forever

asyncio.run(main())
