# Personal Projects Catalog

> Derived from `data_profile.json` -> `personal_projects[]`.
> Pick 2-3 per CV, matching the target role's stack.

## Veinpal — Founder platform (flagship)

- **Type:** Personal / Founder | **Dates:** 2025 - Present | **URL:** https://veinpal.com/apps
- **EN:** Solo-founded platform for building and distributing Windows apps, web
  tools, and games. Full-stack monorepo with Next.js 15 (App Router, React
  Server Components), TypeScript 5, PostgreSQL 16, Redis caching, S3 object
  storage, OAuth authentication, and a complete CI/CD pipeline. Ships 5
  products including a Windows desktop app (Trayline) and multiple web utilities.
- **Tech:** Next.js 15, React 19, TypeScript 5, Tailwind CSS, shadcn/ui,
  PostgreSQL 16, Prisma, Redis, S3/MinIO, NextAuth.js v5, Zod, Turborepo,
  pnpm Workspaces, Vitest, Playwright, GitHub Actions, ESLint, Prettier, Commitlint
- **Best for:** Next.js, full-stack TS, React, startup roles. Shows ownership.

## OverlayOS — Windows widget host

- **Type:** Personal
- **EN:** Production-grade Windows desktop widget host with a secure community
  plugin system. Clean Architecture with .NET 8, C# and WPF, EF Core + SQLite
  persistence, isolated AssemblyLoadContext plugin loading, DPAPI-based secure
  storage, observability with Serilog + Application Insights.
- **Tech:** .NET 8, C#, WPF, CommunityToolkit.Mvvm, EF Core 8, SQLite,
  AssemblyLoadContext, DPAPI, Serilog, Application Insights, WebView2, MinIO,
  xUnit, Inno Setup, GitHub Actions
- **Best for:** .NET/desktop roles; architecture-heavy postings.

## Secryx — Secret inventory desktop app

- **Type:** Personal
- **EN:** Desktop secret inventory and monitoring app scanning env-like files
  across projects. Lifecycle tracking for found/changed/removed/restored
  secrets, metadata and history in SQLite, secure storage via OS keychain.
- **Tech:** Tauri v2, Rust 2021, React 19, TypeScript 5, Vite 7, Tailwind CSS,
  Zustand, SQLite (rusqlite), OS Keychain (keyring), Serde, Tokio
- **Best for:** security-minded roles, Rust/Tauri, tooling teams.

## TypeW — Typing & cognitive training platform

- **Type:** Personal
- **EN:** Browser-based typing and cognitive training platform with 41 playable
  modes and mini-games across typing, reflex, memory, brain, and puzzle
  categories. Scalable game registry architecture, modular React components,
  centralized Zustand state, live WPM/accuracy tracking, CI/CD pipelines.
- **Tech:** React 19, TypeScript 5, Vite 6, Tailwind CSS 4, Zustand 5, Vitest,
  ESLint, GitHub Actions, Vercel
- **Best for:** frontend/React roles; shows scale (41 modes) and architecture.

## Event-driven e-commerce (in progress)

- **Type:** Personal | **Status:** In progress — say "in progress" on CVs
- **EN:** Small e-commerce system using event-driven patterns with reliability
  features (retries/idempotency) and an admin view for failures.
- **Tech:** React, TypeScript, NestJS, Node.js, PostgreSQL, MongoDB,
  RabbitMQ/Kafka, Docker, Kubernetes (basics), Helm, Prometheus, Grafana,
  OpenTelemetry, CI workflow
- **Best for:** backend/microservices/DevOps-flavored postings.

## Portfolio Website

- **Type:** Personal | **URL:** https://portfolio-yosr.vercel.app/en
- **EN:** Responsive, multilingual portfolio website to present projects,
  skills, and CV versions.
- **Tech:** Next.js, React, TypeScript, Vercel
- **Best for:** always link in the CV header; list as a project only if space allows.

---

## Selection guide by role

| Target role | Projects to feature |
|-------------|--------------------|
| React / Frontend | TypeW, Veinpal, (Secryx) |
| Full Stack Node/NestJS | Veinpal, Event-driven e-commerce, TypeW |
| Next.js | Veinpal, Portfolio |
| Java / Spring | (projects less relevant — lead with Ooredoo experience) |
| AI Engineer | (lead with PFE) + Veinpal for engineering breadth |
| .NET / Desktop | OverlayOS, Secryx |
| QA Automation | Veinpal (Vitest+Playwright), TypeW (CI quality) |
| DevOps-flavored | Event-driven e-commerce, Veinpal |
