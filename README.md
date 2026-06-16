# ft-interview-django

Take-home / pairing boilerplate for a **Fresh Tracks Canada** interview.

A working end-to-end hotel search:

- **Backend** — Django 5 + Django REST Framework, talks to the [Amadeus Hotel Search API](https://developers.amadeus.com/self-service/category/hotels) sandbox.
- **Frontend** — Next.js 14 (App Router) + Tailwind, with a search form and a results list.
- **Database** — PostgreSQL 16. Hotel searches are persisted so you have something concrete to extend.
- **Everything boots with one command.**

---

## Quick start

```bash
# 1. Get free Amadeus sandbox credentials (takes 2 min)
#    → https://developers.amadeus.com/register
#    Create a "Self-Service" app, copy its API Key + Secret.

cp .env.example .env
# Open .env and paste your AMADEUS_CLIENT_ID / AMADEUS_CLIENT_SECRET.

# 2. Boot it.
docker compose up --build
```

Then open:

- Frontend → <http://localhost:3000>
- Backend health → <http://localhost:8000/api/health>

Try a search with `cityCode=PAR` (Paris) — the Amadeus sandbox has the richest test data there.

---

## What's wired up

| Endpoint | What it does |
| --- | --- |
| `GET /api/health` | Liveness check. |
| `GET /api/hotels/search?cityCode=PAR&checkInDate=YYYY-MM-DD&checkOutDate=YYYY-MM-DD&adults=1` | Resolves hotels in `cityCode`, then fetches Amadeus offers for them. Logs the search to Postgres. |
| `GET /api/hotels/history` | Last 20 searches from Postgres. |

The Amadeus client lives at [`backend/hotels/amadeus.py`](backend/hotels/amadeus.py) — it handles OAuth token caching and batches hotel-IDs into 20-at-a-time offer requests. The view is in [`backend/hotels/views.py`](backend/hotels/views.py).

---

## Project layout

```
.
├── docker-compose.yml          # postgres + backend + frontend
├── .env.example                # copy → .env, fill in Amadeus creds
├── backend/
│   ├── Dockerfile
│   ├── entrypoint.sh           # runs migrate + runserver
│   ├── requirements.txt
│   ├── ft_backend/             # Django project (settings, urls)
│   └── hotels/                 # the app
│       ├── amadeus.py          # Amadeus REST client
│       ├── views.py            # /search + /history endpoints
│       ├── models.py           # HotelSearch model (audit log)
│       ├── serializers.py
│       └── urls.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── app/
    │   ├── layout.tsx
    │   └── page.tsx            # search form + results list
    └── lib/
        └── api.ts              # typed fetch client
```

---

## Suggested extensions for the interview

The boilerplate is intentionally thin. Pick whichever your interviewer suggests, or whichever feels most natural to you:

- Add a **hotel detail page** that hits a `/api/hotels/<hotelId>` endpoint.
- **Persist favorites** — let the user star a hotel and list them on `/favorites`.
- Add **filters** (price range, board type, rating) on the results page.
- Replace the SSR-less client component with a **React Server Component** that streams results.
- Add **tests** (pytest + DRF APIClient on the backend, Playwright on the frontend).
- Cache Amadeus responses (Redis, or `cache_page`) — the sandbox is rate-limited.
- Add **observability**: structured logs, a `/metrics` Prometheus endpoint, traces.

---

## Local development without Docker

The Docker compose is the supported path. If you really want to run things locally:

```bash
# Postgres
docker compose up db

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export POSTGRES_HOST=localhost
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev
```

---

## Notes on Amadeus

- The sandbox lives at `https://test.api.amadeus.com`.
- Tokens are valid ~30 minutes; the client caches them on the instance.
- Hotel data is sparse outside major cities. **PAR / LON / NYC / MAD** are the most reliable for testing.
- If a search returns 0 results, try a date 1–2 weeks in the future — past dates always 400.
