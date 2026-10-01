---
name: teach
description: Teach the user a skill or concept over multiple sessions, using the current directory as a stateful workspace with lessons, reference documents, and learning records. Use when the user wants to learn something deeply over time.
disable-model-invocation: true
risk: none
---

# Teach

The user has asked you to teach them something. This is a stateful request — they intend to learn the topic over multiple sessions.

## Teaching Workspace

Treat the current directory as a teaching workspace. State is captured in several files:

- `MISSION.md`: Why the user is interested in the topic. Used to ground all teaching. Establish this first.
- `./reference/*.html`: Reference materials — compressed learnings from lessons; cheat sheets, glossaries, syntax references. Designed for quick reference and designed to print well.
- `RESOURCES.md`: A list of high-quality, high-trust resources for grounding teaching in primary knowledge.
- `./learning-records/*.md`: Learning records capturing what the user has learned (non-obvious lessons, key insights). Titled `0001-<dash-case-name>.md` with incrementing numbers. Used to calculate the zone of proximal development.
- `./lessons/*.html`: Lessons — one self-contained HTML file per lesson, teaching one tightly-scoped thing tied to the mission. The primary unit of teaching.
- `./assets/*`: Reusable components shared across lessons (stylesheets, quiz widgets, simulators).
- `NOTES.md`: Scratchpad for user preferences and working notes.

## Philosophy

To learn at a deep level, the user needs three things:

- **Knowledge**: captured from high-quality, high-trust resources
- **Skills**: acquired through interactive lessons
- **Wisdom**: from interacting with other learners and practitioners

Before `RESOURCES.md` is well-populated, focus on finding high-quality resources. **Never trust parametric knowledge** — ground everything in primary sources.

### Fluency vs Storage Strength

- **Fluency strength**: in-the-moment retrieval
- **Storage strength**: long-term retention (the real goal)

Design lessons for long-term retention via desirable difficulty:
- Retrieval practice (recall from memory)
- Spacing (distributing practice over time)
- Interleaving (mixing related topics — for skills practice only)

## Lessons

A lesson is the main output: one self-contained HTML file saved to `./lessons/`, titled `0001-<dash-case-name>.html` with incrementing numbers.

A lesson should be:
- **Beautiful**: clean, readable typography and layout. Think Tufte.
- **Short**: completable quickly. Learners' working memory is small.
- **Tied to the mission**: directly relevant to why the user wants to learn.
- **In the zone of proximal development**: challenging just enough.
- **Interactive**: with a feedback loop (quizzes, real-world steps).
- **Cited**: every claim links to its primary source.

Each lesson should:
- Recommend a primary source for the user to read or watch
- Contain a reminder to ask followup questions to the agent
- Link via HTML anchors to other lessons and reference documents

Open the lesson file for the user by running a CLI command where possible.

## Assets

Reuse is the default. Before authoring a lesson, read `./assets/` and build from existing components. When a lesson needs something new and reusable, write it as a component in `./assets/` and link to it — never inline code a future lesson would duplicate.

A shared stylesheet is the first component every workspace earns.

## The Mission

**If the mission is unclear or `MISSION.md` is not populated, your first job is to question the user on why they want to learn this.** Failing to understand the mission means lessons feel too abstract and you have no way of judging what to teach next.

Missions may change as the user develops. Confirm with the user before updating `MISSION.md`, and add a learning record to capture the change.

## Zone of Proximal Development

Each lesson should challenge the user "just enough." If the user doesn't specify what to learn:

1. Read their `learning-records/`
2. Figure out what fits their mission and zone of proximal development
3. Teach the most relevant next thing

## Knowledge in lessons

Teach only the knowledge required to acquire the lesson's skill. Gather knowledge from `RESOURCES.md` first. For knowledge acquisition, difficulty is the enemy — keep it accessible.

## Skills in lessons

For skill acquisition, difficulty is the tool. Effortful retrieval builds storage strength. Use:
- Interactive lessons with quizzes and in-browser tasks
- Guided real-world step lists (e.g., yoga poses, coding exercises)

Each should have a **tight feedback loop** — feedback immediately and automatically. For quizzes, each answer should be the same number of words (no formatting clues).

## Acquiring Wisdom

When the user asks something requiring wisdom, attempt an answer but ultimately delegate to a **community** (forum, subreddit, local group). Find high-reputation communities relevant to the topic. Respect if the user prefers not to join one.

## Reference Documents

Create reference documents alongside lessons — compressed essences of the lesson content for quick reference. Lessons are rarely revisited; reference docs are.

Especially valuable: syntax references, algorithm cheat sheets, glossaries.

## Token Optimization

**Expected range**: 300–1,500 tokens per lesson session (reads learning-records + MISSION.md, generates one lesson HTML file)

**Patterns used**: Glob for structure (checks `./learning-records/`, `./lessons/`, `./assets/` before writing), progressive disclosure (mission → resources → lesson), lazy file creation (only creates workspace files when needed)

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
