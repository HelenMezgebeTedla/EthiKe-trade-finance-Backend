# Trader Financial Resilience — Backend

Full CRUD (GET, POST, PUT, PATCH, DELETE) on every entity, JWT authentication,
role-based access control with per-trader data isolation, and a trained ML
pipeline already wired in.

## Run it

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs. Click **Authorize**, log in with a registered
user's username/password, and every endpoint below becomes callable from
the docs page directly.

## Running the tests

```bash
pytest
```

121 tests covering full CRUD on every entity, auth (register/login/JWT
validation), and RBAC (cross-trader isolation, admin-only actions).

## Security

- **Password hashing**: bcrypt via passlib. Plaintext passwords are never stored or logged.
- **JWT authentication**: `python-jose`, HS256, 60-minute expiry (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`). Every endpoint except `/auth/register` and `/auth/login` requires a valid `Bearer` token.
- **Role-based access control**: two roles, `admin` and `trader`.
  - `admin` can act on any trader's data and manage users.
  - `trader` accounts are always pinned to their own linked `trader_id` — even if a request body names a different `trader_id`, the server silently overrides it to the caller's own. Reading or writing another trader's data returns `403`, never a `404` that would leak existence.
- **Rate limiting**: `slowapi` limits `/auth/login` to 10/minute and `/auth/register` to 5/minute per IP, to blunt brute-force and spam-signup attempts.
- **Security headers**: every response gets `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and `Strict-Transport-Security`.
- **CORS**: restricted via `ALLOWED_ORIGINS` env var (comma-separated); defaults to `*` for local dev only — set this explicitly in production.
- **SQL injection**: not applicable — all queries go through SQLAlchemy's ORM with parameter binding, never raw string-formatted SQL.
- **Secrets**: `SECRET_KEY` and `DATABASE_URL` are read from `.env`, never hardcoded (a dev-only fallback exists so the app still runs without a `.env`, but you must override it before deploying).

## Layout

```
database.py, main.py            # engine/session, app startup, security middleware
dependencies.py                  # get_current_user, require_roles, ownership checks
app/
  core/
    config.py                    # SECRET_KEY, JWT algorithm, token expiry
    security.py                  # password hashing + JWT encode/decode
    rate_limit.py                 # slowapi limiter instance
  models/                        # SQLAlchemy models incl. User (with role)
  schemas/                       # Create / Update / Read pydantic models
  repositories/                  # class + singleton, raw DB access only
  services/                      # business logic + ownership-aware CRUD
  routers/                       # one APIRouter per entity, full CRUD verbs
  ml/
    ml_inference_service.py       # loads the trained .pkl models (already present)
tests/                            # 121 tests: CRUD, auth, RBAC, ownership isolation
train_models.ipynb (see below)    # trains the two ML models from scratch
```

## Connecting your Jupyter-trained models

The two `.pkl` files are already in `app/ml/` (trained on the synthetic
dataset described in `train_models.ipynb`). To retrain:

1. Open `train_models.ipynb`, adjust the `generate_*` functions if you have
   real data, and run it top to bottom.
2. It saves `replacement_cost_model.pkl` and `risk_classifier_model.pkl`.
3. Copy both into `app/ml/`, replacing the existing files.
4. Restart the server — no other code changes needed.
