# Dependency Audit — Examples

## 1. Single Node.js Repo — Outdated Dependencies

**User Request:**
> `/dep-audit ~/Repos/my-saas-app`

**Detection:**
- Package manager: npm (found `package.json` + `package-lock.json`)
- 42 direct dependencies (34 production, 8 dev)
- 318 resolved packages in lock file

**Outdated Packages:**

| Package | Current | Latest | Update Type | Notes |
|---------|---------|--------|-------------|-------|
| express | 4.18.2 | 4.21.2 | minor | Includes security patches |
| jsonwebtoken | 8.5.1 | 9.0.2 | major | Breaking: algorithm default changed |
| mongoose | 6.12.0 | 8.9.3 | major | Breaking: dropped Node 14, new query API |
| axios | 1.4.0 | 1.7.9 | minor | Bug fixes, keep-alive improvements |
| dotenv | 16.0.3 | 16.4.7 | minor | Performance improvements |
| @types/node | 18.15.0 | 22.10.5 | major | Dev-only, follow your Node target version |

**Security Audit (npm audit):**

| Severity | Package | Advisory | Fix |
|----------|---------|----------|-----|
| HIGH | jsonwebtoken@8.5.1 | CVE-2022-23529 — insecure key handling | Upgrade to 9.0.0+ |
| MEDIUM | semver@7.3.8 | CVE-2022-25883 — ReDoS | Upgrade to 7.5.2+ (transitive via npm update) |

**License Scan:** All clear. 318 packages, all MIT/Apache-2.0/ISC/BSD.

**Update Plan:**

| Priority | Action | Packages | Risk |
|----------|--------|----------|------|
| 1 | Fix HIGH advisory | jsonwebtoken 8.5.1 -> 9.0.2 | Major version. Review: default algorithm changed from HS256 to require explicit setting. Update all `jwt.sign()` / `jwt.verify()` calls. |
| 2 | Fix MEDIUM advisory | Run `npm update semver` | Patch-level transitive update. Low risk. |
| 3 | Minor updates (batch) | express, axios, dotenv | Run `npm update`. All semver-minor, backward-compatible. |
| 4 | Plan major migration | mongoose 6 -> 8 | Read migration guide. Major query API changes. Schedule for dedicated sprint. |
| 5 | Dev dependency update | @types/node | Match to your Node.js target version. No production risk. |

---

## 2. Cross-Repo Audit — Version Conflicts

**User Request:**
> `/dep-audit ~/Repos/api-service ~/Repos/worker-service ~/Repos/shared-lib`

**Detection:**
- api-service: npm (package.json + package-lock.json) — 56 direct deps
- worker-service: npm (package.json + package-lock.json) — 38 direct deps
- shared-lib: npm (package.json + package-lock.json) — 12 direct deps

**Cross-Repo Version Conflicts:**

| Package | api-service | worker-service | shared-lib | Recommended |
|---------|-------------|---------------|------------|-------------|
| typescript | 5.2.2 | 5.6.3 | 4.9.5 | 5.6.3 (align all) |
| zod | 3.21.4 | 3.24.1 | 3.21.4 | 3.24.1 (align all) |
| @prisma/client | 5.8.1 | 5.22.0 | -- | 5.22.0 (align api + worker) |
| winston | 3.11.0 | 3.11.0 | 3.8.2 | 3.11.0 (align shared-lib up) |
| lodash | 4.17.21 | -- | 4.17.19 | 4.17.21 (patch, has CVE fix) |

**Key Findings:**
- **shared-lib on TypeScript 4.9.5** while both services are on 5.x. This blocks adoption of TS 5 features (decorators, `satisfies`) in shared code. High priority to align.
- **lodash 4.17.19 in shared-lib** has a known prototype pollution CVE (CVE-2021-23337) fixed in 4.17.21. Critical fix.
- **Prisma version divergence** between api-service and worker-service means schema changes tested against one version may break on the other.

**Update Plan:**

| Priority | Action | Repos Affected |
|----------|--------|---------------|
| 1 | Update lodash to 4.17.21 in shared-lib | shared-lib (CVE fix) |
| 2 | Align TypeScript to 5.6.3 across all repos | shared-lib (major), api-service (minor) |
| 3 | Align Prisma to 5.22.0 | api-service (minor, test migrations) |
| 4 | Align zod and winston | shared-lib, api-service (minor) |

**Recommendation:** Consider a monorepo or shared workspace config (npm workspaces, Turborepo) to enforce single versions of shared dependencies across these three repos.

---

## 3. Security Advisory — Prioritized Response

**User Request:**
> "A critical CVE just dropped for `next` (Next.js). Run `/dep-audit` on all our frontend repos to assess exposure."
>
> `/dep-audit ~/Repos/marketing-site ~/Repos/customer-portal ~/Repos/admin-dashboard`

**Detection:**

| Repo | Next.js Version | Vulnerable? | Exposure |
|------|----------------|-------------|----------|
| marketing-site | 14.1.0 | YES — CVE-2025-29927 (CVSS 9.1) | Server-side middleware auth bypass. Critical — this repo uses middleware for auth. |
| customer-portal | 14.2.21 | NO — patched in 14.2.15 | Safe. No action needed. |
| admin-dashboard | 13.5.6 | YES — CVE-2025-29927 affects 13.x | Vulnerable. Patch available: 13.5.9. |

**CVE-2025-29927 Details:**
- **Severity**: Critical (CVSS 9.1)
- **Vector**: Attackers can bypass `middleware.ts` authorization by sending a crafted `x-middleware-subrequest` header
- **Impact**: Complete auth bypass on any route protected by Next.js middleware
- **Fix**: Upgrade to Next.js >= 14.2.15 (14.x) or >= 13.5.9 (13.x)

**Prioritized Response Plan:**

| Priority | Repo | Action | Timeline |
|----------|------|--------|----------|
| 1 | marketing-site | Upgrade next 14.1.0 -> 14.2.25 | TODAY. Auth bypass is exploitable now. |
| 2 | admin-dashboard | Upgrade next 13.5.6 -> 13.5.9 | TODAY. Same vulnerability, admin-facing. |
| 3 | marketing-site | After emergency patch, plan migration to 15.x | This quarter. 14.1.0 is far behind. |

**Immediate Mitigation (if upgrade cannot be deployed within hours):**

```bash
# Block the attack vector at the reverse proxy / CDN level
# Add a rule to strip or reject requests with the x-middleware-subrequest header
# Example for nginx:
#   proxy_set_header x-middleware-subrequest "";
# Example for Cloudflare WAF:
#   Block requests where http.request.headers["x-middleware-subrequest"] exists
```

**Post-Incident:**
- Set up Dependabot or Renovate on all three repos for automated security PRs
- Add `npm audit --audit-level=high` to CI pipeline to catch future advisories before merge
- Schedule quarterly dependency audit cadence using this skill
