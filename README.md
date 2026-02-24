# Voice AI Low-Latency Template

FastAPI + WebSocket + Redis cache + AI routing template for voice-to-AI workflows.

## Architecture Logic

Pipeline:
1. Client (speech-to-text) sends **partial transcript** frames via WebSocket.
2. Server aggregates partial text in memory (`buf`).
3. `fast_intent()` checks quick intents (low-latency path) and immediately returns partial hints.
4. When `final=true`, server switches to deep path:
   - Build final text from buffer
   - Check Redis cache first
   - If cache miss, call AI model endpoint (`deep_llm()`)
   - Cache final answer (TTL default 300s)
5. Return final answer and clear buffer for next utterance.

This design reduces latency by avoiding full LLM calls for every partial chunk.

## Key Modules

- `app/main.py`:
  - `/health` endpoint
  - `/ws/stream` WebSocket endpoint
  - orchestrates partial/final flow

- `app/router.py`:
  - `fast_intent(text)`
  - lightweight intent routing (rule-based starter)

- `app/workers.py`:
  - `deep_llm(text)`
  - async call to external AI model endpoint

- `app/cache.py`:
  - Redis get/set wrapper with TTL

## Run
```bash
docker compose up --build
```

## Health
- `GET /health`
- `WS /ws/stream`

## WebSocket Message Format
```json
{"text":"สวัสดี","final":false}
{"text":"วันนี้มีนัดไหม","final":true}
```

## WebSocket Test Client
```bash
pip install -r requirements-dev.txt
python scripts/ws_test_client.py --url ws://localhost:8080/ws/stream
```

## Quality Tools

### Ruff (lint)
```bash
ruff check .
```

### Black (format)
```bash
black .
black --check .
```

## CI
GitHub Actions workflow: `.github/workflows/ci.yml`
- Ruff lint check
- Black format check
- Pytest unit tests
- Docker compose config validation
