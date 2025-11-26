#!/bin/bash
set -e

# Install everything once
pip install --no-cache-dir \
  fastapi uvicorn[standard] sqlalchemy asyncpg redis rq \
  passlib[bcrypt] python-jose[cryptography] pydantic-settings \
  jinja2 httpx playwright

# Install Playwright browsers
playwright install chromium --with-deps

# Start services in background
sudo service postgresql start
sudo service redis-server start

# Setup DB
sudo -u postgres psql -c "CREATE DATABASE scrapyflow;"
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"

echo "Setup complete! Run: bash start.sh"
