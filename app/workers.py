import os

import httpx

AI_URL = os.getenv("AI_URL", "http://localhost:11434/api/generate")
AI_MODEL = os.getenv("AI_MODEL", "llama3.1")


async def deep_llm(text: str) -> str:
    async with httpx.AsyncClient(timeout=20) as c:
        payload = {"model": AI_MODEL, "prompt": text, "stream": False}
        res = await c.post(AI_URL, json=payload)
        res.raise_for_status()
        data = res.json()
        return data.get("response", "")[:2000]
