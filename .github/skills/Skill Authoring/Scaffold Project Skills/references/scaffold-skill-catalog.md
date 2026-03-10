# Skill Catalog by Technology

Map from detected technologies → skill domains and skill folder names. The agent picks only what applies to the project.

## Universal Skills (always include)

| Domain | Skills |
|---|---|
| Product & Architecture | Product Requirements & Scope, Domain Modeling, Design Patterns & Refactoring, Folder & Module Organization, Configuration-as-Code, Technical Decision Records (TDR) |
| Developer Experience & Governance | Code Review Standards, Documentation System, Style Guide Enforcement, Dependency Hygiene |
| Data Privacy & Compliance Basics | Data Privacy Fundamentals |

## Stack-Specific Mappings

### Frontend Detection

| If project has | Add domain | Skills |
|---|---|---|
| React, Vue, Svelte, Angular | UI-UX & Design System | Component Library Engineering, Accessibility (a11y) Compliance, Responsive Layout Engineering, UX Flows & Interaction Design, Iconography & Visual Consistency |
| Tailwind CSS | UI-UX & Design System | Design System Tokens (Tailwind) |

### Next.js Detection

| If project has | Add domain | Skills |
|---|---|---|
| Next.js | Next.js Mastery | App Router Routing Strategy, Server Components Boundaries, Client Component Interactivity, Data Fetching & Caching, SSR-SSG-ISR Strategy, Route Handlers (API), Server Actions Design, SEO & Metadata, Performance Budgeting |

### Backend / API Detection

| If project has | Add domain | Skills |
|---|---|---|
| REST / GraphQL API | API Design & Data Contracts | API Response Standards, Schema-First Validation, Error Handling & Problem Details, Idempotency & Retries, Webhooks & Event Handling |

### Auth Detection

| If project has | Add domain | Skills |
|---|---|---|
| Any auth | Auth & Security | RBAC-Permissions, Session Security, OAuth Hardening, Secrets & Key Management, Security Headers & CSP, Input Validation (Zod), Rate Limiting & Abuse Prevention, Vulnerability Management |
| NextAuth / Auth.js | Auth & Security | Auth.js (NextAuth v5) Setup |

### Database Detection

| If project has | Add domain | Skills |
|---|---|---|
| Prisma | Database & ORM | Data Modeling (Prisma), Migration Strategy, Seeding & Fixtures, Query Performance & Indexing, Transactional Integrity, Connection & Pooling Strategy |
| Neon | Database & ORM | Neon Branching Workflow |
| Other SQL/NoSQL | Database & ORM | Data Modeling, Migration Strategy, Seeding & Fixtures, Query Performance & Indexing |

### TypeScript Detection

| If project has | Add domain | Skills |
|---|---|---|
| TypeScript | TypeScript & Code Quality | Type System Architecture, API Contract Typing, Error-Resilient Typing, Linting Policy Enforcement, Formatting & Style Consistency, Git Hooks Governance, Conventional Commits & Changelogs |

### Testing Detection

| If project has | Add domain | Skills |
|---|---|---|
| Any test framework | Testing & QA | Unit Testing Strategy, Integration Testing, E2E Testing (User Flows), Mocking & Test Utilities, Test Data Management |
| SonarQube | Testing & QA | SonarQube Quality Gates |

### DevOps Detection

| If project has | Add domain | Skills |
|---|---|---|
| GitHub Actions / CI | CI-CD & Deployment | CI Pipeline Engineering, Preview Deployments, Production Deployment Strategy, Versioning & Release Automation, Environment Promotion Workflow |
| Docker | Docker & Runtime Operations | Container Build Patterns, Container Runtime & Operations |
| Git | branching-and-deployment | branching-and-deployment |

### Observability Detection

| If project has | Add domain | Skills |
|---|---|---|
| Logging / monitoring | Observability & Analytics | Structured Logging, Error Tracking Strategy, Performance Monitoring, Audit Logging |
| Vercel | Observability & Analytics | Vercel Analytics Integration |

### Scalability Concerns

| If project has | Add domain | Skills |
|---|---|---|
| Queues, workers, caching | Performance & Reliability | Caching Strategy, Background Jobs Pattern, Concurrency & Load Safety, Resilience Patterns |

### Privacy / Compliance

| If project has | Add domain | Skills |
|---|---|---|
| Cookie consent, GDPR | Data Privacy & Compliance Basics | Data Privacy Fundamentals |

### Monorepo Detection

| If project has | Add domain | Skills |
|---|---|---|
| pnpm workspaces, Turborepo, Nx | Developer Experience & Governance | Monorepo Workspace Management (pnpm), Project Templates & Generators |

### Meta / Skill Authoring

| If project has | Add domain | Skills |
|---|---|---|
| .github/skills/ folder | Skill Authoring | Skill Authoring |
