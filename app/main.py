from fastapi import FastAPI, WebSocket
from app.router import fast_intent
from app.workers import deep_llm
from app.cache import get_cache, set_cache

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.websocket("/ws/stream")
async def ws_stream(ws: WebSocket):
    await ws.accept()
    buf = []

    while True:
        msg = await ws.receive_json()
        text = (msg.get("text") or "").strip()
        is_final = bool(msg.get("final", False))

        if text:
            buf.append(text)

        merged = " ".join(buf).strip()
        if len(merged) >= 8:
            quick = fast_intent(merged)
            if quick:
                await ws.send_json({"type": "partial", "result": quick})

        if is_final:
            final_text = " ".join(buf).strip()
            key = f"q:{final_text.lower()}"
            cached = get_cache(key)
            if cached:
                await ws.send_json({"type": "final", "result": cached, "cached": True})
            else:
                ans = await deep_llm(final_text)
                set_cache(key, ans, ttl=300)
                await ws.send_json({"type": "final", "result": ans, "cached": False})
            buf.clear()
