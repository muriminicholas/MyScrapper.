# ScrapyFlow – Real-Time Web Scraping Platform

A fully automated, dynamic web scraping system built in Python with real-time task distribution, per-user tracking, live progress monitoring, and a beautiful dashboard.

Perfect for data teams, researchers, e-commerce monitoring, lead generation, and competitive intelligence.

## Features

- User authentication & isolated task space per user
- Create unlimited scraping tasks via web UI or API
- Real-time task queue with priority support
- Live progress tracking (0–100%) with logs
- Dynamic scraping using Playwright + BeautifulSoup / Scrapy
- Headless browser support (bypasses Cloudflare, CAPTCHA-ready with 2Captcha/solver integration)
- Automatic retries, proxy rotation, rate limiting
- Export results: JSON, CSV, Excel, PostgreSQL
- Admin dashboard: monitor all users & system health
- WebSocket-based real-time updates (no page refresh needed)
- Dockerized & production-ready

## Tech Stack (2025 Best Practices – All Python)

| Component              | Technology                          |
|-----------------------|-------------------------------------|
| Backend & API         | FastAPI                             |
| Real-time Dashboard   | FastAPI + WebSockets + HTMX + Tailwind |
| Task Queue            | Redis + RQ (Redis Queue)            |
| Workers               | RQ Worker + Playwright + BeautifulSoup |
| Database              | PostgreSQL + Redis                  |
| Authentication        | JWT + FastAPI Users                 |
| Frontend              | Jinja2 Templates + HTMX + Alpine.js |
| Deployment            | Docker Compose / Kubernetes         |

# ScrapyFlow – Project Structure

scrapyflow/
├── app/                        # FastAPI backend (core application)
│   ├── main.py                 # FastAPI app entry point + WebSocket manager
│   ├── api/                    # REST API routers
│   │   ├── init.py
│   │   ├── tasks.py            # Create/list/update/delete tasks
│   │   ├── auth.py             # Login, register, token endpoints
│   │   └── users.py            # User profile & admin routes
│   ├── websocket/              # Real-time connection & broadcasting
│   │   ├── init.py
│   │   └── connection_manager.py
│   ├── auth/                   # Authentication logic
│   │   ├── dependencies.py     # JWT dependency
│   │   ├── schemas.py          # Pydantic models for auth
│   │   └── utils.py            # Password hashing, token creation
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── init.py
│   │   ├── task.py             # Task model (status, progress, result, etc.)
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas for API validation
│   ├── database.py             # DB session & engine setup
│   └── config.py               # Environment variables (Settings with Pydantic)
│
├── workers/                    # RQ background workers
│   ├── scraper_worker.py       # Main worker: pulls jobs & executes spiders
│   └── tasks_registry.py       # Maps task_type → actual scraper function
│
├── tasks/                      # All scraping spiders/logic (hot-reloadable)
│   ├── init.py
│   ├── amazon_price.py
│   ├── linkedin_profile.py
│   ├── yellowpages_leads.py
│   └── generic_playwright.py   # Fallback dynamic scraper
│
├── dashboard/                  # Frontend: Jinja2 templates + static assets
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html      # Live task list with HTMX
│   │   ├── task_detail.html    # Real-time logs & progress bar
│   │   └── admin/
│   │       └── overview.html
│   └── static/
│       ├── css/
│       │   └── tailwind.css
│       ├── js/
│       │   ├── htmx.min.js
│       │   └── alpine.min.js
│       └── icons/
│
├── redis/                      # Redis configuration & custom config (optional)
│   └── redis.conf
│
├── postgres/                   # PostgreSQL init scripts (optional)
│   └── init.sql
│
├── migrations/                 # Alembic migrations (if using Alembic)
│
├── tests/                      # Pytest suite
│   ├── test_api.py
│   └── test_scrapers.py
│
├── .env.example                # Example environment variables
├── .env                        # Local dev secrets (gitignored)
├── .dockerignore
├── .gitignore
├── docker-compose.yml         (keyword: docker-compose.yml)          # Redis + Postgres + FastAPI + Worker + (optional) Flower
├── Dockerfile                  # Multi-stage production image
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Optional: for Poetry/black/ruff
├── alembic.ini                 # If using Alembic for migrations
└── README.md                   # You are here


### Key Highlights

- **100% Python** – No Node.js required
- **Real-time updates** via FastAPI WebSockets + Redis Pub/Sub
- **Live dashboard** powered by HTMX + Tailwind (zero page reloads)
- **Easy to extend** – Just drop a new `.py` file in `tasks/` and it appears in the UI
- **Production-ready** with Docker Compose (Redis, Postgres, Worker, Web)



