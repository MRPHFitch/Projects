import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)

# Dictionary to store connected clients.
# Each client is identified by its WebSocket connection and an optional ID.
# Format: {websocket: {"id": "some_id", "target": "target_id", "other_peer_ws": websocket_of_other_peer}}
CONNECTED_CLIENTS = {}

async def register_client(websocket):
    """Registers a new client connection."""
    CONNECTED_CLIENTS[websocket] = {"id": None, "target": None, "other_peer_ws": None}
    logging.info(f"New client connected: {websocket.remote_address}")

async def unregister_client(websocket):
    """Unregisters a client connection."""
    client_info = CONNECTED_CLIENTS.get(websocket)
    if client_info:
        peer_ws = client_info.get("other_peer_ws")
        if peer_ws and peer_ws in CONNECTED_CLIENTS:
            # Notify the other peer that this client disconnected
            await peer_ws.send(json.dumps({"type": "disconnect", "peerId": client_info["id"]}))
            CONNECTED_CLIENTS[peer_ws]["other_peer_ws"] = None
            logging.info(f"Notified peer {CONNECTED_CLIENTS[peer_ws].get('id')} of disconnect from {client_info['id']}")

        client_id = client_info.get("id", "Unknown")
        logging.info(f"Client disconnected: {client_id} ({websocket.remote_address})")
        del CONNECTED_CLIENTS[websocket]

async def handler(websocket):
    """Handles messages from a connected client."""
    await register_client(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            client_info = CONNECTED_CLIENTS[websocket]

            if data["type"] == "register":
                # Client wants to register with an ID and potentially a target
                client_id = data["id"]
                target_id = data.get("target")

                client_info["id"] = client_id
                client_info["target"] = target_id

                # Check if the target peer is already waiting
                found_peer = None
                for ws, info in CONNECTED_CLIENTS.items():
                    if ws != websocket and info["id"] == target_id:
                        found_peer = ws
                        break

                if found_peer:
                    # Both peers are present, establish connection
                    client_info["other_peer_ws"] = found_peer
                    CONNECTED_CLIENTS[found_peer]["other_peer_ws"] = websocket

                    await websocket.send(json.dumps({"type": "peer_connected", "peerId": target_id}))
                    await found_peer.send(json.dumps({"type": "peer_connected", "peerId": client_id}))
                    logging.info(f"Peers {client_id} and {target_id} connected.")
                else:
                    # Inform the client that they are waiting for a peer
                    await websocket.send(json.dumps({"type": "waiting_for_peer", "targetId": target_id}))
                    logging.info(f"Client {client_id} registered and waiting for {target_id}")

            elif data["type"] == "offer" or data["type"] == "answer" or data["type"] == "candidate":
                # Relay WebRTC signaling messages
                peer_ws = client_info["other_peer_ws"]
                if peer_ws:
                    await peer_ws.send(json.dumps({
                        "type": data["type"],
                        "data": data["data"],
                        "sender": client_info["id"]
                    }))
                    logging.info(f"Relayed {data['type']} from {client_info['id']} to {CONNECTED_CLIENTS[peer_ws].get('id')}")
                else:
                    logging.warning(f"No peer connected for {client_info['id']} to relay {data['type']}")

            else:
                logging.warning(f"Unknown message type: {data['type']}")

    except websockets.exceptions.ConnectionClosedOK:
        logging.info("Client closed connection normally.")
    except Exception as e:
        logging.error(f"Error handling message: {e}", exc_info=True)
    finally:
        await unregister_client(websocket)

async def main():
    port = 8080  # You can change this port
    host = "0.0.0.0" # Listen on all available interfaces

    logging.info(f"Starting signaling server on ws://{host}:{port}")
    async with websockets.serve(handler, host, port):
        await asyncio.Future() # Run forever

if __name__ == "__main__":
    asyncio.run(main())