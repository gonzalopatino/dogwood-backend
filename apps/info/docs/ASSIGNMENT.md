# Developer D — Board, Contact Form, Email Subscriptions, Health Check

**Branch name:** `feature/info-app`  
**Deadline:** PRs up for review by Thursday  
**Reference:** DW-SRS-001-v3, Sections 3.6, 3.7, 3.10, and NFR-07/NFR-10

---

## What You're Building

Four features in the `apps/info/` app:

### 1. Board Information
The current site has a "Board of Directors" page (now called Advisory Board) showing the current board members with names, positions, photos, and term year. You store board members and expose the current board through a read-only API.

### 2. Contact Form
The current site has a "Contact Us" page with a form (name, email, phone, message). Your API endpoint accepts the submission, saves it to the database, and (in a future week) will send emails. Rate-limited to 3 submissions per hour per IP to prevent spam.

### 3. Email Subscriptions (Follow Blog)
The current site has a "Follow Blog via Email" widget. Visitors enter their email to get notified when new posts are published. Your implementation:
- Visitor submits email → subscription created (unverified)
- System sends a verification email with a unique link (future week)
- Visitor clicks the link → subscription verified
- Each notification email includes a one-click unsubscribe link

### 4. Health Check
A simple endpoint that confirms the app and database are running. Used by monitoring tools.

---

## SRS Requirements You're Covering

| Req ID | What It Means |
|--------|---------------|
| FR-14 | Store Board Members with name, position, photo, term year, is_current flag |
| FR-15 | Public read-only API listing current board members |
| FR-16 | Accept contact form: name (required), email (required), phone (optional), message (required) |
| FR-18 | Store all contact submissions, viewable by Staff in Admin |
| FR-19 | Allow visitors to subscribe by email |
| FR-20 | Subscriptions require double opt-in (verification email click) |
| FR-22 | All notification emails include one-click unsubscribe link |
| NFR-07 | Contact form rate-limited to 3 per hour per IP |
| NFR-10 | Health check endpoint at /api/v1/health/ |

---

## Files You're Creating

```
apps/info/models.py          — BoardMember, ContactSubmission, EmailSubscription models
apps/info/admin.py            — Admin configuration for all three models
apps/info/serializers.py      — Serializers for board, contact, subscribe
apps/info/views.py            — BoardMemberListView, ContactSubmitView, EmailSubscribeView, EmailVerifyView, EmailUnsubscribeView, HealthCheckView
apps/info/urls.py             — 6 URL patterns
tests/test_info.py            — Tests for all of the above
```

Don't touch any files outside of `apps/info/` and `tests/test_info.py`.

---

## How to Start

```bash
# 1. Make sure you're on the latest develop branch
git checkout develop
git pull origin develop

# 2. Create your feature branch
git checkout -b feature/info-app

# 3. Write your models, admin, serializers, views, and URL files

# 4. Generate and apply migrations
docker compose exec web python manage.py makemigrations info
docker compose exec web python manage.py migrate

# 5. Run your tests
docker compose exec web pytest tests/test_info.py -v

# 6. Run the linter
docker compose exec web ruff check apps/info/
docker compose exec web ruff format --check apps/info/

# 7. If everything passes, commit and push
git add .
git commit -m "Add info app: board members, contact form, subscriptions, health check"
git push -u origin feature/info-app

# 8. Open a Pull Request on GitHub: feature/info-app → develop
#    Assign the SE Lead as reviewer. Do NOT merge it yourself.
```

---

## How to Verify Your Work Manually

With `docker compose up` running:

### Board
1. Django Admin → Add Board Members (e.g., "Wilhelmina Martin", position "President", is_current=True)
2. Add one past member with is_current=False
3. `GET /api/v1/board/` — only current members should appear, as a plain list (not paginated)

### Contact Form
4. Send a test submission:
   ```
   curl -X POST http://localhost:8000/api/v1/contact/ \
     -H "Content-Type: application/json" \
     -d '{"name":"John","email":"john@example.com","message":"Hello!"}'
   ```
   Should return 201.
5. Submit 4 times quickly — 4th should return 429 (rate limited)
6. Django Admin → Contact Submissions — your submissions should be there, read-only

### Subscriptions
7. Subscribe: `curl -X POST http://localhost:8000/api/v1/subscribe/ -H "Content-Type: application/json" -d '{"email":"reader@example.com"}'` — should return 201
8. Django Admin → Email Subscriptions — should show as unverified
9. Copy the verification_token from Admin, then visit: `http://localhost:8000/api/v1/subscribe/verify/{token}/` — should return 200 and set is_verified=True

### Health Check
10. `GET /api/v1/health/` — should return `{"status": "healthy", "database": "connected"}`

---

## PR Rules

- Open your PR from `feature/info-app` → `develop`
- Paste the acceptance criteria checklist below into your PR description
- Assign the SE Lead as reviewer
- **Do NOT merge your own PR.** The SE Lead reviews and merges all PRs.

---

## Acceptance Criteria Checklist

Paste this into your PR description and check each box:

**Board:**
- [ ] Board Members can be created in Django Admin with photo upload
- [ ] `GET /api/v1/board/` returns only current board members (is_current=True)
- [ ] Board endpoint returns a plain list (not paginated)
- [ ] Past board members (is_current=False) do not appear

**Contact Form:**
- [ ] `POST /api/v1/contact/` with name, email, message returns 201
- [ ] `POST /api/v1/contact/` without required fields returns 400
- [ ] 4th submission within an hour from the same IP returns 429
- [ ] Contact submissions appear in Django Admin as read-only

**Subscriptions:**
- [ ] `POST /api/v1/subscribe/` with email returns 201, creates unverified subscription
- [ ] Subscribing with an already-verified email returns 200 "Already subscribed"
- [ ] `GET /api/v1/subscribe/verify/{token}/` sets is_verified=True
- [ ] `GET /api/v1/subscribe/verify/{bad-token}/` returns 404
- [ ] `GET /api/v1/subscribe/unsubscribe/{token}/` unsubscribes the user

**Health:**
- [ ] `GET /api/v1/health/` returns 200 with `{"status": "healthy"}`

**General:**
- [ ] All tests in `tests/test_info.py` pass
- [ ] `ruff check .` and `ruff format --check .` pass
