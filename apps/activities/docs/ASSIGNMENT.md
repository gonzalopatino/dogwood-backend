# Developer B — Activities App

**Branch name:** `feature/activities-app`  
**Deadline:** PRs up for review by Thursday  
**Reference:** DW-SRS-001-v3, Section 3.4

---

## What You're Building

Dogwood Pavilion hosts 50+ activity groups organized into three categories:

1. **Social, Educational & Cultural** — Drama Club, Book Club, Film Group, etc.
2. **Art, Craft & Games** — Lapidary Workshop, Quilting, Bridge, Mahjong, etc.
3. **Sports & Athletics** — Table Tennis, Snooker, Badminton, Floor Curling, etc.

Each group has a name, description, schedule, location within the pavilion, and a volunteer Group Leader with contact info.

On the current WordPress site, this is spread across three separate pages (one per category) plus a separate "Activity Group Leaders" page listing all leaders and their contact info. Your app consolidates all of this.

---

## SRS Requirements You're Covering

| Req ID | What It Means |
|--------|---------------|
| FR-09 | Store Activity Groups with name, category, description, schedule, location, leader contact info |
| FR-10 | Public read-only API to list Activity Groups, filterable by category slug |
| FR-11 | Public read-only API to list all Activity Group Leaders with group name and contact details |

---

## Files You're Creating

```
apps/activities/models.py        — Category, ActivityGroup models
apps/activities/admin.py         — Admin configuration
apps/activities/serializers.py   — JSON serializers
apps/activities/views.py         — API views
apps/activities/urls.py          — URL routing
tests/test_activities.py         — Tests
```

Don't touch any files outside of `apps/activities/` and `tests/test_activities.py`.

---

## How to Start

```bash
# 1. Make sure you're on the latest develop branch
git checkout develop
git pull origin develop

# 2. Create your feature branch
git checkout -b feature/activities-app

# 3. Copy the starter files I've given you into apps/activities/ and tests/
#    (overwrite the existing stub files)

# 4. Generate and apply migrations
docker compose exec web python manage.py makemigrations activities
docker compose exec web python manage.py migrate

# 5. Run your tests
docker compose exec web pytest tests/test_activities.py -v

# 6. Run the linter
docker compose exec web ruff check apps/activities/
docker compose exec web ruff format --check apps/activities/

# 7. If everything passes, commit and push
git add .
git commit -m "Add activities app: Category, ActivityGroup with API and admin"
git push -u origin feature/activities-app

# 8. Open a Pull Request on GitHub: feature/activities-app → develop
#    Assign the SE Lead as reviewer. Do NOT merge it yourself.
```

---

## How to Verify Your Work Manually

With `docker compose up` running:

1. Django Admin → Add 3 Categories: "Social, Educational & Cultural" (slug: social), "Art, Craft & Games" (slug: arts), "Sports & Athletics" (slug: sports)
2. Add a few Activity Groups under each category with leader info
3. `GET /api/v1/activities/` — all groups should appear with nested category
4. `GET /api/v1/activities/?category=sports` — only sports groups
5. `GET /api/v1/activities/?category=fake` — empty list (not an error)
6. `GET /api/v1/activities/leaders/` — only groups with a leader_name set

---

## PR Rules

- Open your PR from `feature/activities-app` → `develop`
- Paste the acceptance criteria checklist below into your PR description
- Assign the SE Lead as reviewer
- **Do NOT merge your own PR.** The SE Lead reviews and merges all PRs.

---

## Acceptance Criteria Checklist

Paste this into your PR description and check each box:

- [ ] `makemigrations activities` works
- [ ] 3 Categories created in Admin with slugs: social, arts, sports
- [ ] Activity Groups created with leader contact info
- [ ] `GET /api/v1/activities/` returns all groups with nested category
- [ ] `GET /api/v1/activities/?category=sports` filters correctly
- [ ] `GET /api/v1/activities/?category=nonexistent` returns empty list
- [ ] `GET /api/v1/activities/leaders/` excludes groups without a leader
- [ ] Leaders endpoint returns a plain list (not paginated)
- [ ] All tests pass
- [ ] `ruff check .` and `ruff format --check .` pass
