---
name: wayfinder
description: Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets, resolving them one at a time until the way is clear. Use for greenfield projects or huge features too foggy to spec directly.
disable-model-invocation: true
risk: none
---

# Wayfinder

A loose idea has arrived, too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** on the repo's issue tracker, then works its **decision tickets** one at a time until the route is clear.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear with nothing left to decide before someone does the thing. The pull to just do the work is usually the signal you've reached the edge of the map — that's time to hand off to `/to-spec`. Produce decisions, not deliverables.

## Refer by name

In everything the human reads (narration, map decisions), refer to issues by **title name**, never by bare id or number. Names read at a glance; `#42` does not.

## Never resolve more than one ticket per session

(Research tickets are the exception — they can be parallelised.)

## The Map

The map is a single issue on the repo's issue tracker, labelled `wayfinder:map`. Its tickets are child issues. The map is an **index**, not a store — it gists decisions and links to their tickets; it never restates them.

### Map body

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<in-scope fog you can't ticket yet; graduates as the frontier advances>

## Out of scope

<work ruled beyond the destination; closed, never graduates>
```

### Tickets

Each ticket is a child issue of the map. Its body is the question, sized to one ~100K token agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `wayfinder:<type>` label: `research`, `prototype`, `grilling`, or `task`.

A session **claims** a ticket by assigning it before any work. An open, unassigned ticket is unclaimed. The **frontier** is the open, unblocked, unclaimed children.

## Ticket Types

- **Research** (AFK): Reading docs or external resources to surface a fact. Resolved by a subagent calling the Skill tool with `research`.
- **Prototype** (HITL): Raise fidelity with a cheap concrete artifact. Call the Skill tool with `prototype`. Links the prototype as an asset.
- **Grilling** (HITL): Conversation. The default. Always call the Skill tool twice, for `grilling` and `domain-modeling`.
- **Task** (HITL or AFK): Manual work that must happen before a decision can be made (signing up for a service, provisioning access, moving data). The one type that *does* rather than decides — earns its place by unblocking a decision.

A HITL ticket only resolves through live exchange. The agent never stands in for the human's side of it.

## Fog of war

The map is deliberately incomplete: don't chart what you can't yet see. **Not yet specified** is where the dim view of coming decisions is written — suspected questions, areas to revisit. It's the undiscovered frontier toward the destination.

**Fog or ticket?** The test is whether you can state the question precisely now:
- **Ticket when** the question is already sharp, even if blocked.
- **Not yet specified when** you can't yet phrase it sharply. Don't pre-slice the fog into ticket-sized pieces.

## Out of scope

Work beyond the destination is **out of scope**. It gets its own section on the map, never graduates. When a ticket turns out to sit past the destination, **close it** and leave one line in Out of scope. A scope boundary isn't a step on the route.

## Invocation

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Call the Skill tool twice, for `grilling` and `domain-modeling`, to pin down what this map is finding its way to. **If this surfaces no fog** (the whole journey fits one session), you don't need a map — stop and ask the user how they'd like to proceed.
2. **Map the frontier.** Grill breadth-first, fanning out across the whole space rather than deep on one thread.
3. **Create the map** (label `wayfinder:map`): Destination and Notes filled in, Decisions-so-far empty, fog sketched into Not yet specified.
4. **Create the frontier tickets** as child issues, then wire blocking edges in a second pass (issues need ids before they can reference each other).
5. **Fire research subagents** for each `research` ticket, capturing findings on a throwaway `research/<name>` branch with a context pointer from the ticket.
6. Stop: charting is one session's work.

### Work through the map

User invokes with a map (URL or number). A ticket is optional — without one, you pick the next decision.

1. Load the map (the low-res view, not every ticket body).
2. Choose the ticket. If the user named one, use it; otherwise take the first frontier ticket. **Claim it** before any work.
3. Resolve it. Zoom as needed: fetch full body of related tickets on demand. If in doubt, call the Skill tool twice, for `grilling` and `domain-modeling`.
4. Record the resolution: post the answer as a resolution comment, **close** the issue, and **append a context pointer** to Decisions-so-far.
5. Add newly-surfaced tickets and graduate fog the answer has made specifiable (clearing graduated patches from Not yet specified). If a ticket turns out to sit past the destination, rule it out of scope rather than resolving it.

## Token Optimization

**Expected range**: 500–3,000 tokens per session (map load + one ticket resolution)

**Patterns used**: Progressive disclosure (map loaded at low resolution; tickets fetched on demand), subagent isolation for research tickets, early exit if the map is already clear

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
