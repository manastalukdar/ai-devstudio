---
name: implement-spec
description: Implement the result of /to-spec and /to-tickets in code using parallel implementer subagents across the ticket frontier. Use when a spec and its tickets are ready and you want to orchestrate the full build.
disable-model-invocation: true
risk: safe
---

# Implement Spec

You have been provided a spec with associated tickets. The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved.

The tickets are not a list of steps. They are a **task graph** with blocking relationships. This means there is always a **frontier** of tickets ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. **Read the spec and tickets** to understand the task graph.

2. **(optional) Exploration subagent**: if tickets require codebase or external doc knowledge, spin up an exploration subagent first. It saves Markdown notes in a directory outside the repo (accessible by all future subagents) so implementer subagents can focus on implementation.

3. **Create the integration branch.** If the issue tracker closes work through PRs, open a draft PR after the first merge, marked as closing the spec and tickets.

4. **Implementer subagents**: one per ticket, each in its own worktree on its own branch. Each implementer:
   - Confirms its worktree is based on the integration branch before starting, and resets onto it if not
   - Calls the Skill tool with `tdd` to build the ticket
   - Merges the integration branch tip into its own branch before reporting done

5. **Merger subagent**: once an implementer completes, merge its work to the integration branch.

6. **Update frontier**: if the merge changes which tickets are now unblocked, kick off new implementer subagents immediately (maximum concurrency).

7. **Code review**: once all tickets are complete, call the Skill tool with `code-review` on the integration branch. Fix all issues in a single implementer subagent.

8. **Close out**: if a draft PR exists, mark it ready for review. Otherwise, resolve each ticket the way the issue tracker closes work and report the integration branch.

9. **Cleanup**: remove all implementer subagent worktrees.

## Token Optimization

**Expected range**: 500–3,000 tokens (orchestrator context only; implementer subagents run independently)

**Patterns used**: Tiered model delegation (exploration → cheap, implementation → default, code review → capable), subagent isolation keeps orchestrator context lean

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
