# Developer A — Content App (Pages & Posts)

**Branch name:** `feature/content-app`  
**Deadline:** PRs up for review by Thursday  
**Reference:** DW-SRS-001-v3, Section 3.1 and 3.2

---

## What You're Building

The content app is the core of the site. It powers two things:

1. **Pages** — Static content like "Welcome", "Insurance", "Constitution", "Code of Conduct". Each page is a scrollable block of text and images, just like the current WordPress site. Staff create and edit pages through Django Admin.

2. **Posts** — News & Events entries like "Drama Club Presents", "AGM Notice", "Olympic Viewing Party". These are blog posts displayed in reverse chronological order (newest first).

Both Pages and Posts can have **Attachments** — downloadable files like PDFs (AGM agendas, nomination forms, cafe menus) or images (event posters). Visitors see these as download links on the page.

The public API is **read-only**. Nobody logs in on the frontend. Staff manage everything through Django Admin.

---

## SRS Requirements You're Covering

| Req ID | What It Means                                                                                |
| ------ | -------------------------------------------------------------------------------------------- |
| FR-01  | Pages have: title, slug, body (HTML), status (draft or published), display_order, timestamps |
| FR-02  | Pages can have multiple downloadable file attachments                                        |
| FR-03  | API endpoint to get one page by its slug, returning body + attachments                       |
| FR-04  | API endpoint to list all published pages (for building the nav menu)                         |
| FR-05  | Posts have: title, slug, body (HTML), featured image, status, published date, author         |
| FR-06  | Posts can have multiple downloadable file attachments                                        |
| FR-07  | API endpoint to list published posts, newest first, with pagination                          |
| FR-08  | API endpoint to get one post by its slug, returning body + attachments                       |
| FR-27  | Django Admin with search, filters, and inline attachment editing                             |

---

## Files You're Creating

```
apps/content/models.py         — Page, Post, Attachment database models
apps/content/admin.py          — Django Admin configuration
apps/content/serializers.py    — Convert database records to JSON
apps/content/views.py          — API endpoint logic
apps/content/urls.py           — URL routing
tests/test_content.py          — Automated tests
```

Don't touch any files outside of `apps/content/` and `tests/test_content.py`.

---

## How to Start

```bash
# 1. Make sure you're on the latest develop branch
git checkout develop
git pull origin develop

# 2. Create your feature branch
git checkout -b feature/content-app

# 3. Copy the starter files I've given you into apps/content/ and tests/
#    (overwrite the existing stub files)

# 4. Generate the database migration files
docker compose exec web python manage.py makemigrations content

# 5. Apply migrations (creates the tables)
docker compose exec web python manage.py migrate

# 6. Run your tests
docker compose exec web pytest tests/test_content.py -v

# 7. Run the linter
docker compose exec web ruff check apps/content/
docker compose exec web ruff format --check apps/content/

# 8. If everything passes, commit and push
git add .
git commit -m "Add content app: Page, Post, Attachment models with API and admin"
git push -u origin feature/content-app

# 9. Open a Pull Request on GitHub: feature/content-app → develop
#    Assign the SE Lead as reviewer. Do NOT merge it yourself.
```

---

## How to Verify Your Work Manually

With `docker compose up` running:

1. Go to http://localhost:8000/admin/ and log in
2. Click "Pages" → "Add Page" → fill in title, slug, body, set status to "Published", save
3. Go to http://localhost:8000/api/v1/pages/ — your page should appear
4. Go to http://localhost:8000/api/v1/pages/your-slug/ — full page detail should appear
5. Create a page with status "Draft" — it should NOT appear in the API
6. Repeat for Posts: create one, check the list and detail endpoints

---

## PR Rules

- Open your PR from `feature/content-app` → `develop`
- Paste the acceptance criteria checklist below into your PR description
- Assign the SE Lead as reviewer
- **Do NOT merge your own PR.** The SE Lead reviews and merges all PRs.

---

## Acceptance Criteria Checklist

Paste this into your PR description and check each box:

- [ ] `makemigrations content` generates migration files with no errors
- [ ] `migrate` applies them successfully
- [ ] Creating a Page in Django Admin works, including inline file attachments
- [ ] Creating a Post in Django Admin works, including featured image and attachments
- [ ] `GET /api/v1/pages/` returns only published pages, ordered by display_order
- [ ] `GET /api/v1/pages/{slug}/` returns full page body + attachments list
- [ ] `GET /api/v1/pages/{draft-slug}/` returns 404
- [ ] `GET /api/v1/posts/` returns only published posts, newest first, paginated
- [ ] `GET /api/v1/posts/{slug}/` returns full post body + attachments
- [ ] Archived and draft posts return 404 on the detail endpoint
- [ ] All tests in `tests/test_content.py` pass
- [ ] `ruff check .` and `ruff format --check .` pass with no errors
