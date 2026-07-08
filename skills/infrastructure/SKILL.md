---
name: infrastructure
description: Infrastructure as Code generation for Terraform, CloudFormation, and Pulumi
disable-model-invocation: false
---

# Infrastructure as Code (IaC) Management

I'll help you create, validate, and manage Infrastructure as Code templates for cloud deployments.

**Supported IaC Tools:**
- **Terraform**: HashiCorp's industry-standard IaC tool
- **AWS CloudFormation**: Native AWS infrastructure management
- **Pulumi**: Modern IaC with programming language support

Arguments: `$ARGUMENTS` - IaC tool preference, resource type, or cloud provider

---

## Token Optimization

**Expected range**: 600–2,800 tokens (initial), 200 tokens (cache hit)

**Caching**: Caches infrastructure setup in `.claude/cache/infrastructure/setup.json` for 7 days. Invalidated when IaC files change.

**Early exit**: Returns immediately if existing infrastructure matches the requested configuration.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
