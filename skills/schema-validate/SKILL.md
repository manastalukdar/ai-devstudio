---
name: schema-validate
description: Database schema validation and drift detection across environments
disable-model-invocation: false
---

# Database Schema Validation & Drift Detection

I'll validate your database schema for consistency, detect drift across environments, identify missing indexes, and verify constraints.

**Supported ORMs & Databases:**
- Prisma (PostgreSQL, MySQL, SQLite)
- TypeORM (PostgreSQL, MySQL, MariaDB, SQLite)
- SQLAlchemy (PostgreSQL, MySQL, SQLite)
- Django ORM (PostgreSQL, MySQL, SQLite)
- Sequelize (PostgreSQL, MySQL, MariaDB, SQLite)

## Token Optimization

**Expected range**: 700–2,500 tokens (initial), 100 tokens (cached validation)

**Caching**: No persistent caching — validates current schemas on each run.

**Early exit**: Returns immediately if schema has not changed since last validation.

**Patterns used**: Grep-before-Read, early exit, checksum-based validation, git diff scope default
