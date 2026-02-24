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


## WebSocket Test Client
```bash
pip install -r requirements-dev.txt
python scripts/ws_test_client.py --url ws://localhost:8080/ws/stream
```

## CI
GitHub Actions workflow: `.github/workflows/ci.yml`
- Runs unit tests (`pytest`)
- Validates `docker compose` config
