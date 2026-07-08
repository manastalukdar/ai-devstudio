---
name: query-optimize
description: SQL/NoSQL query optimization with N+1 detection and index recommendations
disable-model-invocation: false
---

# Query Optimization & Performance Analysis

I'll analyze your database queries for performance issues, detect N+1 problems, recommend indexes, and provide query plan analysis.

**Supported Databases:**
- PostgreSQL (EXPLAIN ANALYZE)
- MySQL/MariaDB (EXPLAIN)
- MongoDB (explain())
- SQLite (EXPLAIN QUERY PLAN)

**Supported ORMs:**
- Prisma, TypeORM, Sequelize (JavaScript/TypeScript)
- Django ORM, SQLAlchemy (Python)
- Mongoose (MongoDB)

## Token Optimization

**Expected range**: 1,500–2,500 tokens (initial), 400 tokens (cache hit)

**Caching**: No persistent caching — analyzes queries from current staged/changed files.

**Early exit**: Returns immediately if no slow or unindexed queries are detected.

**Patterns used**: Grep-before-Read, early exit, git diff scope default
