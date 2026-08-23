# spider-runtime

Monorepo for the spider platform's runtime services and operations docs.
Each top-level directory was imported from its former standalone repository
with full git history preserved.

| Directory | Formerly | Purpose |
|---|---|---|
| `spider-doctor/` | `cl0udarch1t3cts/spider-doctor` | Autonomous repair/create worker (`doctor-1`) that patches scrapers in `spider-scripts` |
| `spider-executor/` | `cl0udarch1t3cts/spider-executor` | Scraper execution stack (MongoDB, registration API, worker, runner) |
| `spider-devops/` | `cl0udarch1t3cts/spider-devops` | Architecture, operations, and VM setup documentation |

The scrapers themselves live in the separate `spider-scripts` repository,
which the Doctor clones and commits into.
