---
name: changelog
description: Version history and migration guides for Solo Unicorn Builder.
---

# Changelog

All notable changes to this project are documented here. This project follows [Semantic Versioning](https://semver.org/).

## [2.0.0] - 2026-02-13

### Rebrand: "Unicorn Project" is now "Solo Unicorn Builder"

This is a major release with breaking changes. If you forked the previous version, read the **Migration Guide** below before pulling upstream changes.

### What's New

- **5 new skills (36 total):** `document-creation`, `generative-art`, `mcp-builder`, `skill-creator`, `webapp-testing`
- **Coding agents comparison:** New [docs/coding-agents.md](docs/coding-agents.md) comparing Claude Code, Gemini CLI, Kiro CLI, Codex CLI, and OpenCode
- **Kiro CLI and OpenCode support:** Agent symlinks now cover 5 CLI tools instead of 2
- **Starter project templates:** `template_projects/` ships with ready-to-copy projects so you're not starting from zero
- **GitHub community files:** Issue templates (bug, feature, skill proposal), PR template, Code of Conduct, Contributing guide
- **Expanded existing skills:** Significant updates to `frontend-ui-ux`, `marketing-brand`, `operations`, `technical-writing`, `career-advisor`, and `obsidian-knowledge`

### Breaking Changes

| # | Change | Impact |
|---|--------|--------|
| 1 | Repo renamed from `pingwu/unicorn` to `pingwu/solo-unicorn` | Remote URLs break |
| 2 | `projects/agentic-landing-template/` moved to `template_projects/landing-page/` | Path references break |
| 3 | `personal_knowledge/` replaced by `template_knowledge/` + `my_knowledge/` | Path references break |
| 4 | User code now lives in sibling `my_projects/`, not `projects/` | Workflow change |
| 5 | `my_*` wildcard in `.gitignore` ignores all `my_`-prefixed directories | Check for unintended ignores |
| 6 | Agent symlink setup expanded from 2 to 5 agents | Must re-run init |
| 7 | Root `AGENTS.md` replaced by `UNICORN_CONSTITUTION.md` | Agent config change |

### New Directory Layout

```
workspace/
  solo-unicorn/
    skills/                  # 36 agent skills (committed, contribute via PR)
    template_knowledge/      # Starter knowledge vault (committed, read-only)
    template_projects/       # Starter projects (committed, read-only)
      landing-page/          # The landing page template (was projects/agentic-landing-template)
    docs/                    # Documentation
    .claude/skills -> skills # Agent symlinks (created during init)
    .gemini/skills -> skills
    .kiro/steering -> skills
    .opencode/skills -> skills
  my_knowledge/              # YOUR knowledge vault (separate git repo)
  my_projects/               # YOUR projects (separate git repos per project)
```

**Key concept:** The Solo Unicorn repo is your "command center" — it receives upstream updates to skills and templates. Your personal work (`my_knowledge/`, `my_projects/`) lives next to the repo and should have its own independent version control.

---

## Migration Guide (from v1.x fork)

### Option A: Fresh Start (Recommended if you have minimal custom changes to the repo itself)

This is the cleanest approach. Your personal data and projects are preserved.

```bash
# 1. Back up your personal data from the old fork
cd your-old-unicorn-fork
cp -R personal_knowledge ~/unicorn-backup-knowledge
cp -R projects ~/unicorn-backup-projects

# 2. Fork and clone the new repo
gh repo fork pingwu/solo-unicorn --clone

# 3. Run init (or tell your AI agent: "Run the init unicorn setup")
UNICORN_DIR="$(pwd)/solo-unicorn"
PROJECT_ROOT="$(pwd)"
mkdir -p "$UNICORN_DIR/.claude" && ln -s "$UNICORN_DIR/skills" "$UNICORN_DIR/.claude/skills"
mkdir -p "$UNICORN_DIR/.agent" && ln -s "$UNICORN_DIR/skills" "$UNICORN_DIR/.agent/skills"
mkdir -p "$UNICORN_DIR/.gemini" && ln -s "$UNICORN_DIR/skills" "$UNICORN_DIR/.gemini/skills"
mkdir -p "$UNICORN_DIR/.kiro" && ln -s "$UNICORN_DIR/skills" "$UNICORN_DIR/.kiro/steering"
mkdir -p "$UNICORN_DIR/.opencode" && ln -s "$UNICORN_DIR/skills" "$UNICORN_DIR/.opencode/skills"

# 4. Set up your knowledge vault
mkdir -p "$PROJECT_ROOT/my_knowledge"
cp -R "$UNICORN_DIR/template_knowledge/"* "$PROJECT_ROOT/my_knowledge/"
cp -R ~/unicorn-backup-knowledge/* "$PROJECT_ROOT/my_knowledge/"   # Restore your data

# 5. Set up your projects
mkdir -p "$PROJECT_ROOT/my_projects"
cp -R "$UNICORN_DIR/template_projects/landing-page" "$PROJECT_ROOT/my_projects/landing-page"
# If you customized the landing page, overwrite with your version:
# cp -R ~/unicorn-backup-projects/agentic-landing-template/* "$PROJECT_ROOT/my_projects/landing-page/"

# 6. Initialize separate git repos for your private directories
cd "$PROJECT_ROOT/my_knowledge" && git init && git add . && git commit -m "Initial knowledge vault"
cd "$PROJECT_ROOT/my_projects/landing-page" && git init && git add . && git commit -m "Initial project"
```

### Option B: In-Place Merge (if you have custom skills or docs you want to preserve)

```bash
# 1. Back up your personal data FIRST
cp -R personal_knowledge personal_knowledge_backup
cp -R projects projects_backup

# 2. Update your remote URLs
git remote set-url origin https://github.com/<your-username>/solo-unicorn.git
git remote set-url upstream https://github.com/pingwu/solo-unicorn.git

# 3. Fetch and merge (expect conflicts due to renames)
git fetch upstream
git merge upstream/main
# Resolve conflicts manually

# 4. After merge, set up the new sibling structure
UNICORN_DIR="$(pwd)"
PROJECT_ROOT="$(dirname "$UNICORN_DIR")"
mkdir -p "$PROJECT_ROOT/my_knowledge"
cp -R "$UNICORN_DIR/template_knowledge/"* "$PROJECT_ROOT/my_knowledge/"
cp -R personal_knowledge_backup/* "$PROJECT_ROOT/my_knowledge/"

mkdir -p "$PROJECT_ROOT/my_projects"
cp -R projects_backup/agentic-landing-template "$PROJECT_ROOT/my_projects/landing-page"

# 5. Re-run symlink setup
mkdir -p "$UNICORN_DIR/.claude" && ln -s "$UNICORN_DIR/skills" "$UNICORN_DIR/.claude/skills"
mkdir -p "$UNICORN_DIR/.agent" && ln -s "$UNICORN_DIR/skills" "$UNICORN_DIR/.agent/skills"
mkdir -p "$UNICORN_DIR/.gemini" && ln -s "$UNICORN_DIR/skills" "$UNICORN_DIR/.gemini/skills"
mkdir -p "$UNICORN_DIR/.kiro" && ln -s "$UNICORN_DIR/skills" "$UNICORN_DIR/.kiro/steering"
mkdir -p "$UNICORN_DIR/.opencode" && ln -s "$UNICORN_DIR/skills" "$UNICORN_DIR/.opencode/skills"

# 6. Initialize separate git repos for private directories
cd "$PROJECT_ROOT/my_knowledge" && git init && git add . && git commit -m "Initial knowledge vault"
cd "$PROJECT_ROOT/my_projects/landing-page" && git init && git add . && git commit -m "Initial project"

# 7. Clean up old directories
rm -rf "$UNICORN_DIR/personal_knowledge" "$UNICORN_DIR/personal_knowledge_backup" "$UNICORN_DIR/projects" "$UNICORN_DIR/projects_backup"
```

### Verify Your Migration

After either option, confirm:

```bash
ls -la "$UNICORN_DIR/.claude/skills" "$UNICORN_DIR/.gemini/skills" "$UNICORN_DIR/.kiro/steering" "$UNICORN_DIR/.opencode/skills"  # Symlinks exist
ls "$PROJECT_ROOT/my_knowledge/career/"                                                                                                # Knowledge vault populated
ls "$PROJECT_ROOT/my_projects/"                                                                                                        # Projects directory exists
ls "$UNICORN_DIR/skills/" | wc -l                                                                                                      # Should show 36 skills
```

---

## [1.0.0] - 2025-12-01

Initial release as "Unicorn Project" with 31 skills, `projects/agentic-landing-template`, and `personal_knowledge/` vault.
