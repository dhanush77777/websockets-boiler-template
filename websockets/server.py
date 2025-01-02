import asyncio
import websockets
import json

async def stream_response(websocket):
    try:
        # Receive initial message from client
        message = await websocket.recv()
        print(f"Received message: {message}")
        
        # Simulate streaming data
        data = ["Hello", "This", "is", "a", "streaming", "response"]
        
        # Stream each word with a delay
        for word in data:
            # Simulate processing time
            await asyncio.sleep(1)
            
            # Create a message object
            response = {
                "type": "data",
                "content": word
            }
            
            # Send the message
            await websocket.send(json.dumps(response))
        
        # Send completion message
        await websocket.send(json.dumps({
            "type": "done",
            "content": "Stream completed"
        }))
        
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(stream_response, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    # For server:
    asyncio.run(main())


# server.py
# import asyncio
# import websockets
# import json
# import psutil
# import datetime

# async def get_system_metrics():
#     """Get real-time system metrics"""
#     cpu_percent = psutil.cpu_percent(interval=1)
#     memory = psutil.virtual_memory()
    
#     return {
#         "timestamp": datetime.datetime.now().isoformat(),
#         "cpu_usage": cpu_percent,
#         "memory": {
#             "total": memory.total,
#             "available": memory.available,
#             "percent": memory.percent,
#             "used": memory.used,
#             "free": memory.free
#         },
#         "disk": {
#             "percent": psutil.disk_usage('/').percent,
#             "used": psutil.disk_usage('/').used,
#             "free": psutil.disk_usage('/').free
#         },
#         "network": {
#             "bytes_sent": psutil.net_io_counters().bytes_sent,
#             "bytes_recv": psutil.net_io_counters().bytes_recv
#         }
#     }

# async def stream_metrics(websocket):
#     try:
#         await websocket.send(json.dumps({
#             "type": "connected",
#             "message": "Started streaming system metrics"
#         }))
        
#         while True:
#             metrics = await get_system_metrics()
            
#             # Send metrics to client
#             await websocket.send(json.dumps({
#                 "type": "metrics",
#                 "data": metrics
#             }))
            
#             # Wait before sending next update
#             await asyncio.sleep(2)
            
#     except websockets.exceptions.ConnectionClosed:
#         print("Client disconnected")
#     except Exception as e:
#         print(f"Error: {e}")
#         await websocket.send(json.dumps({
#             "type": "error",
#             "message": str(e)
#         }))

# async def main():
#     async with websockets.serve(stream_metrics, "localhost", 8765):
#         print("Metrics streaming server started on ws://localhost:8765")
#         await asyncio.Future()  # run forever

# if __name__ == "__main__":
#     asyncio.run(main())