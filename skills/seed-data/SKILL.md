---
name: seed-data
description: Generate realistic seed/fixture data based on schema analysis
disable-model-invocation: false
---

# Realistic Seed Data Generator

I'll analyze your database schema and generate realistic seed/fixture data for testing and development, maintaining proper relationships and constraints.

**Supported ORMs & Data Generators:**
- Prisma (with Faker.js)
- TypeORM (with Faker.js)
- Django (with Faker Python)
- SQLAlchemy (with Faker Python)
- Sequelize (with Faker.js)

## Token Optimization

**Expected range**: 2,000–3,000 tokens (initial), 400 tokens (cache hit)

**Caching**: No persistent caching — generates seed data based on current schema on each run.

**Early exit**: Returns immediately if seed data files already exist for the target tables.

**Patterns used**: Grep-before-Read, early exit, template-based generation
