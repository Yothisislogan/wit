# Study reliability update

This PR fixes existing study flows and adds repeatable content loading and timed general practice. Startup creates a new `timed_exams` table.

- Question choices are shuffled when served, while grading uses their stable IDs.
- Quiz review matches results by question ID and shows the selected answer, the
  correct answer, and any stored answer explanations. The original question
  loader now safely backfills blank rationales when the stored choices and answer key match the bundled question.
- Anonymous and signed-in students use the same course/state selection rules for
  modules, lessons, terms, quizzes, progress, mistake review, and coach context.
  An explicit `/api/modules?course=pc|lh` still supports browsing another track.
  Personalized content requests need the existing session or `X-Anon-Id` header.
- State-law modules are identified by the seed scripts' existing
  `state-law-{state}-{course}` slugs. Without a selected state, only general
  material is included. New state modules should keep this convention until an
  explicit jurisdiction field is introduced.
- Old mixed-course quiz attempts are summarized using only answers relevant to
  the current selection. Stored quiz attempts and other-course progress remain.
- Corrected mistakes leave the active review queue, and another incorrect answer
  puts them back. This is a review queue, not a spaced-repetition mastery measure.
- Flashcards support click, Enter, and Space. Quiz choices are keyboard buttons.
- Lessons restore saved notes, confidence, and review flags. Saving notes does not
  complete a lesson; completion-only API updates preserve omitted fields.
- Empty question banks and failed saves/submissions show recovery states.
- The heuristic dashboard indicator is labeled **Study progress**. Ordinary
  practice is no longer labeled as an exam simulator.

## Regression checks

From `pc-license-prep-server-v2`, with `requirements.txt` installed and Node 20+:

```sh
python -m unittest discover -s tests -v
node --test tests/frontend.test.cjs
```

The backend tests use an isolated in-memory database. They do not start the
application's content-seeding lifespan or call a live AI provider.

## Content and timed practice update

Startup and `python scripts/sync_content.py --apply` use the same validated,
non-destructive catalog. `--check` (also the default) validates without connecting
to the database. The former P&C, L&H, and gap-question import entry points now
delegate to this loader instead of appending duplicates or deleting questions.

A fresh database receives:

| Course | Modules | Lessons | Questions |
| --- | ---: | ---: | ---: |
| P&C | 15 | 90 | 230 |
| Life & Health | 19 | 33 | 174 |

Repeat imports preserve existing IDs, inactive flags, edited question keys,
custom lesson bodies, notes, quiz history, and mistakes. They fill missing
modules/lessons/terms/questions and safely backfill blank explanations. Bundled
lesson stubs are upgraded only when their current fields exactly match the
original bundled text. Existing duplicate questions are retained to preserve
history; timed practice deduplicates question text. Imports use a PostgreSQL
transaction advisory lock or SQLite immediate write transaction at startup.
Unexpected migration errors now fail startup instead of being swallowed.

Generated state-law banks are excluded from automatic imports pending legal
source review. Previously imported state material remains available in scoped
study flows, labelled as awaiting review; it is excluded from timed practice.
The catalog's structural validation is not an expert certification of its claims.

Timed practice is available from the workspace's **Timed Practice** tile:

- 50 unique general-course questions, 60 minutes, shuffled choices and broad
  module sampling. Insufficient banks return an explicit error.
- Server-owned deadlines, saved answers and flags, question navigation, resume,
  final submission, and results with explanations and module scores.
- Immutable question/choice snapshots preserve a session when content changes.
- Ownership checks, revision checks, and one active session per user protect
  against cross-user reads and conflicting tabs. Expiry rejects late answers;
  repeat submissions preserve results. Refresh can recover the latest result.
- Scores are raw practice percentages. There is no official pass/fail claim,
  blueprint weighting, held-out bank, or state-law coverage. Timed results are
  stored separately from ordinary quiz history and its mistake queue.

Exam metadata no longer publishes unsupported numbers for all states. North
Carolina's four separate major-line formats are recorded with source and review
dates: Property, Casualty, Life, and Accident & Health or Sickness; each has 55
scored questions, up to 5 pretest questions, and 75 minutes. The passing 70 is a
scaled score, not a raw percentage. Source: [Pearson VUE North Carolina candidate
handbook](https://www.pearsonvue.com/content/dam/VUE/vue/en/documents/publications/123400.pdf),
reviewed September 13, 2026; content outline effective March 15, 2024. All other
state format records remain explicitly pending. Format verification does not
certify the state-law bank.

## Verification and limits

20 backend and 12 frontend regression tests pass. They cover existing study
flows, import repeatability/history preservation, incomplete import repair,
invalid-catalog rejection, session ownership, snapshots, resume, conflicting
revisions, expiry, scoring, course switching, and frontend save failure recovery.
A separate real-lifespan SQLite smoke check starts the app twice, confirms
unchanged counts, and starts a full session for both courses. Browser/visual
validation remains outstanding because no browser is installed. PostgreSQL
concurrency has not been exercised against a running PostgreSQL server.

## Remaining roadmap

| Area | Status | Remaining work |
| --- | --- | --- |
| Grading, notes, flashcards, scope, mistake review | Implemented in this PR | Browser acceptance check |
| Repeatable P&C/L&H imports | Implemented in this PR | Source-backed editorial review; historical duplicate reconciliation |
| State exam accuracy | Partial | Verify remaining jurisdictions; track effective editions and review dates |
| State-law content | Pending | Review every legal claim with primary sources and publish reviewed banks |
| Timed exam engine | General practice implemented | Official line-specific counts/timing, blueprint weights, reviewed state coverage, held-out bank |
| Readiness assessment | Pending | Calibrated evidence; current indicator is only study progress |
| Accounts and recovery | Pending | Link anonymous work to optional sign-in and support recovery |
| Daily study plan | Pending | Diagnostic-driven schedule, weak-topic review, milestones |
| Coach improvements | Pending | Source citations, persistent learning context, stronger teaching flows |
| Scenario lab | Pending | Practical insurance cases and feedback |
| Licensing/career pathway | Pending | Verified checklists, milestones, career preparation |
| Workspace/navigation | Partial | Remove unfinished source/import controls; simplify navigation |

This PR is not a completed all-state licensing curriculum. It does not merge or
deploy itself; the running site changes only after normal release steps.
