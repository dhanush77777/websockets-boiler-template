import asyncio
import websockets
import json

async def receive_stream():
    async with websockets.connect("ws://localhost:8765") as websocket:
        # Send initial request
        await websocket.send("Start streaming")
        
        # Receive streaming responses
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                
                if data["type"] == "data":
                    print(f"Received: {data['content']}")
                elif data["type"] == "done":
                    print("Stream completed")
                    break
                    
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break

# Run server
if __name__ == "__main__":
    # For server:
    # asyncio.run(main())
    
    # For client:
    asyncio.run(receive_stream())



# client.py
# import asyncio
# import websockets
# import json
# from datetime import datetime

# def format_bytes(bytes):
#     """Convert bytes to human readable format"""
#     for unit in ['B', 'KB', 'MB', 'GB']:
#         if bytes < 1024:
#             return f"{bytes:.2f} {unit}"
#         bytes /= 1024
#     return f"{bytes:.2f} TB"

# async def display_metrics():
#     async with websockets.connect("ws://localhost:8765") as websocket:
#         while True:
#             try:
#                 response = await websocket.recv()
#                 data = json.loads(response)
                
#                 if data["type"] == "metrics":
#                     metrics = data["data"]
#                     # Clear screen (works on Unix-like systems)
#                     print("\033c", end="")
#                     print(f"System Metrics - {metrics['timestamp']}")
#                     print("-" * 50)
#                     print(f"CPU Usage: {metrics['cpu_usage']}%")
#                     print("\nMemory:")
#                     print(f"  Used: {format_bytes(metrics['memory']['used'])} ({metrics['memory']['percent']}%)")
#                     print(f"  Free: {format_bytes(metrics['memory']['free'])}")
#                     print(f"  Total: {format_bytes(metrics['memory']['total'])}")
#                     print("\nDisk:")
#                     print(f"  Used: {format_bytes(metrics['disk']['used'])} ({metrics['disk']['percent']}%)")
#                     print(f"  Free: {format_bytes(metrics['disk']['free'])}")
#                     print("\nNetwork:")
#                     print(f"  Bytes Sent: {format_bytes(metrics['network']['bytes_sent'])}")
#                     print(f"  Bytes Received: {format_bytes(metrics['network']['bytes_recv'])}")
                    
#                 elif data["type"] == "error":
#                     print(f"Error: {data['message']}")
                    
#             except websockets.exceptions.ConnectionClosed:
#                 print("Connection to server closed")
#                 break
#             except Exception as e:
#                 print(f"Error: {e}")
#                 break

# if __name__ == "__main__":
#     asyncio.run(display_metrics())