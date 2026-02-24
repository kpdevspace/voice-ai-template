#!/usr/bin/env python3
"""Simple WebSocket test client for /ws/stream.

Usage:
  python scripts/ws_test_client.py --url ws://localhost:8080/ws/stream --text "hello" --final-text "what time is it"
"""
import argparse
import asyncio
import json
import websockets


async def run(url: str, text: str, final_text: str):
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({"text": text, "final": False}))
        await ws.send(json.dumps({"text": final_text, "final": True}))

        try:
            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=10)
                print(msg)
                payload = json.loads(msg)
                if payload.get("type") == "final":
                    break
        except asyncio.TimeoutError:
            print("No final response received within timeout")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="ws://localhost:8080/ws/stream")
    p.add_argument("--text", default="สวัสดี")
    p.add_argument("--final-text", default="วันนี้มีนัดไหม")
    args = p.parse_args()
    asyncio.run(run(args.url, args.text, args.final_text))


if __name__ == "__main__":
    main()
