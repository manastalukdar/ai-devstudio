---
name: container-optimize
description: Docker/container optimization for size, layers, caching, and security
disable-model-invocation: false
---

# Container Optimization

I'll optimize your Docker containers and Dockerfiles for size reduction, faster builds, better layer caching, and improved security.

Arguments: `$ARGUMENTS` - Dockerfile path or specific optimization focus areas

## Optimization Philosophy

- **Multi-Stage Builds**: Separate build and runtime dependencies
- **Layer Caching**: Optimize layer order for faster rebuilds
- **Image Size**: Minimize final image size
- **Security**: Scan for vulnerabilities in base images
- **Best Practices**: Follow Docker and container security standards

---

## Token Optimization

**Expected range**: 400–2,000 tokens (initial), 200 tokens (cache hit)

**Caching**: Caches Dockerfile analysis in `.claude/cache/container-optimize/dockerfiles.json` for 7 days. Invalidated when Dockerfiles change.

**Early exit**: Returns immediately if all Dockerfiles are already optimally configured.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
