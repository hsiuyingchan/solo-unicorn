---
name: landing-page
description: AI-powered personal landing page template. Your first portfolio project — tells your story and showcases your work.
---

# Agentic Landing Page Template

> **"When AI can do anything for you, what will you build?"**

A production-ready landing page template that teaches AI-assisted cloud development. Go from `git clone` to a live deployed site using natural language prompts and container commands.

## Quick Start

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/), [Git](https://git-scm.com/), and an AI coding assistant ([Claude Code](https://docs.anthropic.com/en/docs/claude-code) or [Gemini CLI](https://github.com/google-gemini/gemini-cli)).

> **Zero host installation:** You do NOT need Node.js, npm, or any other dev tools on your machine. Everything runs inside the Docker container.

Solo Unicorn Builder fills that gap with AI. You bring the expertise in your domain. AI covers the rest — so you can finally ship the whole thing, not just your piece of it.

Don't let the word "coding" scare you. In an AI-native workflow, your daily conversation language — natural language — is the new code.

## Your AI-Augmented Team

The 36 core skills are organized as an "Office" — each role is an AI-powered expert you can call on:

| Role | What it does for you | Example skills |
|------|---------------------|----------------|
| **CTO** | Architect, build, test, deploy | `multi-file-architecture`, `test-first-development`, `docker-expert`, `mcp-builder`, `webapp-testing` |
| **CPO** | Define what to build and for whom | `product`, `idea-validation`, `pm-design-thinking`, `frontend-ui-ux` |
| **CMO** | Position, brand, reach your audience | `marketing-brand`, `go-to-market`, `growth-analytics`, `generative-art` |
| **CRO** | Grow revenue, build partnerships | `sales`, `business-development`, `business-model` |
| **CFO** | Manage costs, plan finances | `finance-accounting`, `fundraising`, `aws-cli-architect` |
| **COO** | Run operations, build your career | `operations`, `career-advisor`, `portfolio-strategy`, `document-creation` |

You don't need to hire a team. You need to ask the right questions — and let AI handle the execution. [Full list of skills →](docs/skills-reference.md)

## Add-on Skills

Beyond the 36 core skills, 7 add-on skills extend the platform:

| Skill | What it does |
|-------|-------------|
| `career-advisor` | Full-lifecycle career management — self-discovery, gap analysis, resume generation, interview prep, onboarding, achievement tracking, and self-reviews. Replaces the former `career-resume` skill. |
| `startup-explorer` | Pre-validation startup idea explorer — bridges career strengths to market opportunities before you commit to building |
| `notebooklm` | Query Google NotebookLM notebooks directly from your coding agent |
| `youtube-knowledge-extractor` | Extract key ideas, summaries, and actionable insights from YouTube videos |
| `oci-expert` | Oracle Cloud Infrastructure expertise — Always Free tier, A1 ARM64 instances, networking, and common errors |
| `landing-page-service-discovery` | Synthesize professional accomplishments into high-converting landing page copy |
| `review` | Lightweight code review skill for bugs, security issues, performance, and readability; adapted from LangChain Deep Agents. |

Add-on skills work exactly like core skills — just describe what you need and the AI applies the right one. Want to contribute your own? [How to contribute →](docs/contributing.md)

## Why This Exists

Here's the real problem:

- **Specialization created blind spots.** You've spent years going deep in one area. But shipping a product requires breadth — requirements, architecture, testing, deployment, marketing, legal, finance. Nobody taught you the other 80%.
- **AI can fill the gaps — but only with structure.** A chatbot can answer questions. It can't guide you through a product launch, a deployment pipeline, or a fundraising round — unless it has a framework for each one.
- **Your thinking is scattered.** A thread in ChatGPT, a conversation in Claude, notes in one app, code in another. Nothing connects.

Solo Unicorn Builder gives you 36 core structured skills, 7 add-on skills, a knowledge vault, and a project workspace — so AI can operate as your team across every function you've never done before.

## What You Get

When you clone this project and go through this process, you get:

- **Bootstrap your AI agent command center** — 43 AI-powered skills: 36 core skills plus 7 add-ons. Not just coding: product development, sales, marketing, legal, finance, operations, code review, and more. Just describe what you need in natural language and the AI applies the right expertise. [Full list →](docs/skills-reference.md)
- **A private knowledge vault** — Your ideas, notes, goals, technical decisions, and learning in one place. Never checked into the public repo. Ships with `template_knowledge/` as a starter — copied to your private `my_knowledge/` on init.
- **Starter projects you can build on** — `template_projects/` ships with example projects (like the landing page template) so you're not starting from zero. Your own work lives in `my_projects/` — build and ship real projects with AI-assisted workflows. A "project" can be anything: a blog post, a marketing research brief, a deployed web application, or an automated workflow.
- **AI agent vendor-agnostic** — Works with any CLI coding agent: Claude Code, Gemini CLI, Kiro CLI, Codex CLI, OpenCode, or any tool that reads markdown. No vendor lock-in. [Compare agents →](docs/coding-agents.md)
- **Local sandbox execution** — Docker Desktop turns natural-language instructions into safe, containerized execution on your own Mac or Windows machine, then carries the same container path toward production. [Why it matters →](docs/local-sandbox.md)

## Start Here

### 1. Check Prerequisites

Before cloning, make sure you have the required tools. **[Read the Prerequisites Guide →](PREREQUISITES.md)**

**TL;DR:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop). Everything else runs inside a container.

### 2. Clone and Set Up

```bash
# Clone the project
git clone https://github.com/pingwu/solo-unicorn.git
cd solo-unicorn
```

Then customize with natural language:
```
"Update the hero section with my name 'Your Name' and title 'Your Title'"
```

**CLI Reference:**
```bash
git clone https://github.com/pingwu/landing-page.git
cd landing-page
npm run docker:dev
# Open http://localhost:3000
```

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 16 | React framework with App Router |
| React | 19 | Component-based UI |
| TypeScript | 5.9 | Type safety (strict mode) |
| Tailwind CSS | 4 | Utility-first styling |
| Vitest | 4 | Unit and component testing |
| Docker | — | Containerized development |
| AWS App Runner | — | Cloud deployment |

## Use Cases

The default template works for consulting services, professional portfolios, digital resumes, and enterprise initiative sites. Alternative templates are in `templates/`.

## Container Commands

**Important for AI agents:** `npm run docker:dev` already runs the container in detached mode with hot-reload enabled. The dev server starts automatically - do NOT run additional `npm run dev` commands inside the container.

| Natural Language | CLI Command | Purpose |
|-----------------|-------------|---------|
| "Start the dev server" | `npm run docker:dev` | Dev server with hot-reload (port 3000) - runs in background |
| "Start a production preview" | `npm run docker:prod` | Production preview (port 3001) |
| "Stop the containers" | `npm run docker:down` | Stop containers |
| "Open a shell in the container" | `npm run docker:shell` | Shell into container |
| "Show the container logs" | `docker compose logs dev -f` | View logs (follow mode) |
| "Run the tests" | `docker compose exec dev npm run test:run` | Run tests |
| "Type-check the project" | `docker compose exec dev npm run typecheck` | TypeScript check |
| "Lint the code" | `docker compose exec dev npm run lint` | ESLint |

### Correct Workflow
```bash
npm run docker:dev          # Start (runs in background automatically)
# Server is now running at http://localhost:3000
docker compose logs dev -f  # View logs if needed (optional)
npm run docker:down         # Stop when done
```

### What NOT to do
❌ `docker compose run --rm dev npm run dev` - This is redundant and blocks the terminal

## Documentation

| Document | Purpose |
|----------|---------|
| [Prompt Library](docs/prompts/PROMPT-LIBRARY.md) | Copy-paste prompts for customizing every section |
| [Content Templates](docs/prompts/CONTENT-TEMPLATES.md) | Ready-to-use content examples by use case |
| [PRD Templates](docs/product/PRD-TEMPLATES.md) | Product requirements by use case |
| [Tech Stack](docs/reference/TECH-STACK.md) | Detailed technology and agent documentation |
| [Deployment Roadmap](docs/guides/DEPLOYMENT-ROADMAP.md) | Phase-by-phase deployment guide |
| [AWS Deployment Guide](docs/guides/AWS-DEPLOYMENT-GUIDE.md) | Complete AWS setup from scratch |
| [AWS Glossary](docs/reference/AWS-GLOSSARY.md) | AWS services explained |
| [AWS Pricing Guide](docs/reference/AWS-PRICING-GUIDE.md) | Cost estimates and free tier |
| [GCP Deployment Guide](docs/guides/GCP-DEPLOYMENT-GUIDE.md) | Complete GCP Cloud Run setup from scratch |
| [GCP Deployment Roadmap](docs/guides/GCP-DEPLOYMENT-ROADMAP.md) | Phase-by-phase GCP deployment guide |
| [GCP Glossary](docs/reference/GCP-GLOSSARY.md) | GCP services explained |
| [GCP Pricing Guide](docs/reference/GCP-PRICING-GUIDE.md) | GCP cost estimates and free tier |
| [Success Stories](docs/SUCCESS-STORIES.md) | What learners have built |
| [Full Learning Journey](../../curriculum/) | Course curriculum and build guides |

## Agent Instructions

AI coding agents read these files automatically:
- `AGENTS.md` — Project goals, conventions, constraints
- `../../UNICORN_CONSTITUTION.md` — Master constitution (Solo Unicorn Builder)

## Contributing

Found an issue? [Open an issue](https://github.com/pingwu/landing-page/issues) or submit a PR.

## Production Graduation Checklist

Before exposing this app to real users or real traffic, confirm **every item below**.

### Runtime Safety

- Global error boundary is implemented (`app/error.tsx`)
- 404 handling is explicit (`app/not-found.tsx`)
- App does not crash on unexpected runtime errors
- Users never see raw stack traces

### Configuration Safety

- All required environment variables are validated at startup
- Missing or invalid config causes a clear, immediate failure
- No secrets are referenced in client components

### Deployment Signals

- `/health` endpoint returns `200 OK`
- Cloud platform health checks are configured
- Failed deploys are detectable without inspecting logs

### Security Baseline

- Security headers are explicitly set (CSP, frame, content-type, referrer)
- Dependencies are locked (`npm ci`)
- No credentials are committed or logged

### UX & Accessibility

- Keyboard navigation works end-to-end
- Mobile navigation opens and closes reliably
- No major layout shift on page load
- At least one accessibility test runs in CI

### Build & Release Confidence

- Production build runs successfully (`npm run docker:prod`)
- Tests pass in the same container used for production
- Target platform is explicit (`linux/amd64`)
- Rollback strategy is understood (even if manual)

### Documentation Honesty

- README clearly states what the app does **not** include
- Deployment steps exist for at least one platform
- Ownership is clear if the site breaks

## License

MIT — use freely for personal or commercial projects.

---

**Course**: CSE 651 — Software Development with Agentic AI ([CSTU.edu](https://cstu.edu))
**Instructor**: Ping Wu
**Evolved from**: [MACA (Multi-AI-Coding-Agent)](https://github.com/pingwu/maca)
