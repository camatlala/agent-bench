from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/runs/{run_id}/stream")
async def run_stream(websocket: WebSocket, run_id: int):
    await websocket.accept()
    await websocket.send_json({"type": "connected", "run_id": run_id})
    await websocket.close()
