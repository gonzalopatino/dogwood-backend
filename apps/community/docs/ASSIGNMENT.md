# Developer C — Community Support Directory

**Branch name:** `feature/community-app`  
**Deadline:** PRs up for review by Thursday  
**Reference:** DW-SRS-001-v3, Section 3.5

---

## What You're Building

The current site has a "Community Support" page listing local organizations that help seniors: Arthritis Support Group, Alzheimer Society's Minds in Motion, BC Seniors Line, Fraser Health Crisis Line, Stroke Recovery Branch, Tri-Cities Better at Home, Tri-Cities Caregivers Support Network, and more.

Each entry has an organization name, description, contact info (phone, email, address, website), and schedule.

Your job: store these in the database and expose them through a read-only public API. Staff manage the entries through Django Admin.

---

## SRS Requirements You're Covering

| Req ID | What It Means |
|--------|---------------|
| FR-12 | Store Community Support resources with org name, description, phone, email, address, website, schedule |
| FR-13 | Public read-only API to list all community support resources |

---

## Files You're Creating

```
apps/community/models.py        — SupportResource model
apps/community/admin.py          — SupportResourceAdmin
apps/community/serializers.py    — SupportResourceSerializer
apps/community/views.py          — SupportResourceListView
apps/community/urls.py           — 1 URL pattern
tests/test_community.py          — Tests
```

Don't touch any files outside of `apps/community/` and `tests/test_community.py`.

---

## How to Start

```bash
# 1. Make sure you're on the latest develop branch
git checkout develop
git pull origin develop

# 2. Create your feature branch
git checkout -b feature/community-app

# 3. Write your model, admin, serializer, view, and URL files

# 4. Generate and apply migrations
docker compose exec web python manage.py makemigrations community
docker compose exec web python manage.py migrate

# 5. Run your tests
#docker compose exec web pytest tests/test_community.py -v
docker compose exec web pytest apps/community/tests/test_community.py -v


# 6. Run the linter
# docker compose exec web ruff apps/community/
docker compose exec web ruff check apps/community/


# docker compose exec web ruff format apps/community/
docker compose exec web ruff format --check apps/community/

# 7. If everything passes, commit and push
git add .
git commit -m "Add community support directory with API and admin"
git push -u origin feature/community-app

# 8. Open a Pull Request on GitHub: feature/community-app → develop
#    Assign the SE Lead as reviewer. Do NOT merge it yourself.
```

---

## How to Verify Your Work Manually

With `docker compose up` running:

1. Go to http://localhost:8000/admin/ and log in
2. Click "Support Resources" → "Add" → fill in org name, phone, schedule, etc. → save
3. Add 2–3 more resources
4. Go to http://localhost:8000/api/v1/community/ — all resources should appear as JSON
5. Verify all fields are present in the response (org_name, phone, email, etc.)

---

## PR Rules

- Open your PR from `feature/community-app` → `develop`
- Paste the acceptance criteria checklist below into your PR description
- Assign the SE Lead as reviewer
- **Do NOT merge your own PR.** The SE Lead reviews and merges all PRs.

---

## Acceptance Criteria Checklist

Paste this into your PR description and check each box:

- [ ] `makemigrations community` works with no errors
- [ ] `migrate` applies successfully
- [ ] Support Resources can be created in Django Admin with all fields
- [ ] `GET /api/v1/community/` returns all support resources as JSON
- [ ] Response includes all fields: org_name, description, phone, email, address, website, schedule
- [ ] Empty optional fields appear as empty strings (not errors)
- [ ] All tests in `tests/test_community.py` pass
- [ ] `ruff check .` and `ruff format --check .` pass
