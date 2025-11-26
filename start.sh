#!/bin/bash
pkill -f uvicorn || true; pkill -f rq || true || true
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
rq worker scrapyflow-default &
echo "ScrapyFlow is LIVE → Open port 8000"
wait