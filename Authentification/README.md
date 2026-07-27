# Auth Toolkit (bcrypt + JWT + RBAC)

A small, self-contained authentication library in Python: password hashing, JWT session tokens, role-based access control, a SQLite user store, and a password-reset token flow.

## What it does
- Hashes and verifies passwords with bcrypt (salted, adaptive work factor).
- Issues and validates stateless JWT tokens (HS256, one-hour expiry).
- Enforces role-based access with a decorator and a numeric role hierarchy, so an `admin` also satisfies a `user` requirement.
- Stores users in SQLite using parameterized queries, with lookups by username and email.
- Generates password-reset tokens with `secrets` and verifies them in constant time against a 30-minute expiry.

## Architecture
Each concern lives in its own module under `auth/`: `passwords.py`, `tokens.py`, `rbac.py`, `db.py`, `reset.py`, and a `User` dataclass in `models.py`. `demo.py` at the project root runs an end-to-end example.

Key decisions:
- SQLite over a server database because the design target is a single-host, zero-config project, not multi-node scale.
- bcrypt rather than a fast general-purpose hash, because password storage wants a deliberately slow, salted algorithm.
- JWT for stateless auth, so no server-side session store is needed to validate a request.
- RBAC as a decorator (`@require_role("admin")`) so access rules sit directly above the function they protect.
- Parameterized SQL everywhere, so user input never reaches a query string directly.

## Getting started
- pip install -r requirements.txt
- python demo.py

Run it from the project folder (the one holding `demo.py` and the `auth/` package). The demo exercises the password, token, and RBAC pieces. The SQLite store and reset-token flow are library components you import; `init_db()` creates the users table on first use.

## Project status
Working project, built to production practices. The password, token, and RBAC components are complete and shown in `demo.py`. The SQLite store and reset-token flow are implemented as importable functions but not yet wired into a web layer.

Planned: a small Flask layer to expose register / login / reset over HTTP, and a pytest suite.

## Security considerations
- The demo uses a hardcoded JWT signing key so the project clones and runs with no setup. A real deployment must load the key from an environment variable or secret manager and never commit it.
- `create_user` stores the password it is given; callers hash with `hash_password` first, so the store never persists plaintext.
- No rate limiting or account lockout on repeated failed attempts. Out of scope for this project.
- No transport for reset tokens. The flow generates and verifies them; delivering the token to the user is the caller's responsibility.
- JWTs are bearer tokens: anyone holding a valid, unexpired token is treated as that user. Keep them secret in transit and at rest.
- SQLite targets single-host use, not high-concurrency or multi-node deployment.