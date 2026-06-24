# Example 1 — "build me a recipe app" — vague scope + unknown stack

## The original prompt
What a newer programmer might actually type:

> ok so i want to build a thing where users can make an account and save their favorite recipes. like they log in and see their saved recipes. can you make this? i dont really know what stack to use, im still kinda new

---

## Without the skill
A coding agent takes the prompt at face value and runs with it:

# Recipe Saver App — Full Build Guide

Great project for learning! I'll recommend a beginner-friendly stack and walk you through building the whole thing. This will take some setup time but is very doable even as someone newer to development.

---

## Stack Recommendation

Since you're new, I'd suggest this combination — it's popular, well-documented, and all JavaScript so you only need to learn one language:

| Layer | Technology | Why |
|---|---|---|
| Frontend | **React** (via Vite) | Lots of tutorials, huge community |
| Backend | **Node.js + Express** | Simple, same language as frontend |
| Database | **SQLite** (via Prisma) | No server setup needed, file-based |
| Auth | **JWT tokens** | Industry standard, straightforward |

Later you could swap SQLite for PostgreSQL when you want to deploy to the web. For now, SQLite keeps things simple — it's just a file on your computer.

---

## Project Structure

> _…baseline truncated — the full no‑skill response ran 541 lines (it just started building)._

---

## With Vibecode Check

Before I hand you a sharpened prompt, I have a couple of questions — because two of the gaps here would genuinely send the agent in very different directions. Recommended defaults are included so you can reply "use the defaults" and I'll proceed.

---

**1. What does "saving a recipe" look like for you?**

This determines the entire data model.

- **Option A (default):** User types in a recipe manually — title, ingredients (as a list), and step-by-step instructions. The app stores it in your database.
- **Option B:** User pastes a URL to a recipe on another site and it saves that link (no scraping, just bookmark-style).
- **Option C:** Just a title and some freeform notes — a lightweight personal note per recipe.

*Default: Option A. It's the most common expectation for a "recipe saver" and makes for the most complete learning project.*

---

**2. How do users log in?**

- **Option A (default):** Email + password they create themselves. Simple, no third-party dependencies.
- **Option B:** "Sign in with Google" (or another social provider). Easier for the user to log in, but more setup for you.

*Default: Option A (email + password). It's the straightforward starting point and teaches the fundamentals.*

---

*Answer as many or as few as you like — or just say "use the defaults" and I'll build the full prompt from there.*

---

Proceeding on defaults: **Option A for both** (manual recipe entry with title/ingredients/steps; email + password auth).

---

## Cleaned-up prompt

```
Build a new full-stack web app from scratch: a recipe-saver where users can create an account, log in, and manage a personal list of saved recipes.

**Stack (recommended for a beginner, no existing project):**
- Framework: Next.js 14 (React-based; handles both frontend and backend API routes in one project, so you don't need to set up two separate codebases)
- Database: SQLite via Prisma ORM (no separate database server to install; everything lives in a single file — easy to get running locally)
- Auth: NextAuth.js with the credentials provider (email + password; stores sessions in the database)
- Styling: Tailwind CSS (utility classes; no separate CSS files to manage)

**What to build:**

1. Auth pages
   - /register — sign up with email and password
   - /login — sign in with email and password
   - /logout — signs the user out and redirects to /login

2. Recipes (authenticated users only — redirect to /login if not signed in)
   - /recipes — lists all recipes saved by the logged-in user (title and a one-line description if present)
   - /recipes/new — form to create a recipe: title (required), ingredients (one per line, required), step-by-step instructions (textarea, required), and an optional short description
   - /recipes/[id] — view a single saved recipe in full
   - /recipes/[id]/delete — delete a recipe (POST, not GET); confirm with a simple "Are you sure?" before submitting

3. Data model (Prisma schema)
   - User: id, email (unique), passwordHash, createdAt
   - Recipe: id, title, description (optional), ingredients (stored as newline-separated text), instructions (text), createdAt, userId (foreign key → User)

**Out of scope for now:** recipe editing after creation, image uploads, search/filter, sharing recipes with other users, and any deployment — just get it running locally.

**Setup steps to include:**
- Initialize a Next.js 14 project with `npx create-next-app@latest`
- Install and configure Prisma with SQLite
- Install and configure NextAuth.js
- Run `npx prisma migrate dev` to create the database

**Verification:** After building, start the dev server (`npm run dev`), then:
1. Register a new user account at http://localhost:3000/register
2. Log in at /login
3. Create a recipe at /recipes/new and confirm it appears at /recipes
4. View the recipe at /recipes/[id]
5. Delete it and confirm it's gone from /recipes
Show me the output of each step (a screenshot or the terminal output) so I can confirm everything works end to end.
```

---

## What I changed & corrected — and the convention behind it

**Stack added from scratch.** Your prompt had no stack at all, which would force a coding agent to guess — and different agents guess differently (one might use plain Node + Express + PostgreSQL, another might reach for Django, another a barebones React app with no backend at all). I recommended **Next.js + SQLite/Prisma + NextAuth.js** because:
- Next.js bundles the frontend and backend into one project — for a beginner, not having to wire two separate codebases together is a significant simplification.
- SQLite needs zero setup (no database server to install or run); it lives in a file on your disk. Postgres or MySQL are more powerful but they're separate programs you have to install, configure, and keep running. A common mistake is picking Postgres too early and spending the first day on setup instead of building the actual app.
- NextAuth.js is the standard auth library for Next.js apps; reinventing auth from scratch (hashing passwords by hand, writing session logic) is where beginners get burned.

**"Save their favorite recipes" → concrete fields.** "Saving a recipe" is a goal, not a spec. A coding agent has to guess: save a URL? A title? Full ingredient lists? This ambiguity forked the entire data model. I specified title + ingredients + instructions as the stored fields, which is the conventional shape for a recipe entry.

**"Make an account and log in" → named auth pages and a specific library.** The intent was clear, but "make it" is too vague for an agent to act on. I named the specific routes (/register, /login, /logout) and the library (NextAuth.js credentials provider) so the agent has an unambiguous target.

**Scope explicitly bounded.** I added an "out of scope" clause covering editing, image uploads, search, sharing, and deployment. Without this, an agent often "helpfully" adds features you didn't want and can spend its context budget on the wrong things.

**Verification step added.** Your original had no way to tell when the app was working. I added a concrete walkthrough (register → login → create → view → delete) ending with "show me the output" — this is the single highest-leverage habit to build. Without it, the agent can hand you code and declare victory, and you have no signal whether it actually runs.

---

## Assumptions & possible misunderstandings — are we still in sync?

- I took "users can make an account" to mean a traditional email + password sign-up, not social login (Google, GitHub, etc.). Correct me if you wanted social login — it changes the NextAuth setup meaningfully.
- I assumed this is a brand-new project, not an addition to an existing codebase. If you have something started, tell the agent which files already exist.
- I assumed "run it locally on my computer" rather than deploying it to a server or hosting service. If you need it live on the internet, the stack is the same but the deploy step (Vercel is the natural fit for Next.js) needs to be added.
- I picked SQLite over Postgres because you're new and local setup friction matters. If you're on a team or planning to deploy soon, Postgres is the more production-ready choice — but it's a separate server to run. Easy to migrate later with Prisma.
- "Ingredients stored as newline-separated text" is a deliberate simplification. A proper ingredient model would be a separate table with quantity, unit, and name columns — but that complexity is worth skipping for a first build.

---

## Prompt tips for next time

**Name your stack up front — even if it's just "I don't have one yet."** A coding agent has no idea what language, framework, or tools you're using unless you say so. "I'm new and open to suggestions" is a perfectly valid thing to include; it tells the agent to pick something beginner-friendly and explain the choice, rather than silently defaulting to whatever it was trained on most recently.

**End every prompt with a verification step.** Notice I added: *"Start the dev server, then: register → login → create recipe → view → delete. Show me the output."* That one sentence turns the agent from a code-dropper into a self-checker — it runs the app, catches its own mistakes, and shows you evidence rather than just asserting "done." This is the single habit that will save you the most round-trips as you keep building.
