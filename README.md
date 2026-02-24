# Voice AI Low-Latency Template

FastAPI + WebSocket + Redis cache + AI worker routing.

## Run
```bash
docker compose up --build
```

## Health
- `GET /health`
- `WS /ws/stream`

## Message format
```json
{"text":"สวัสดี","final":false}
{"text":"วันนี้มีนัดไหม","final":true}
```
