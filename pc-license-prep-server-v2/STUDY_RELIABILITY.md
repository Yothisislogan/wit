# Study reliability update

This update fixes the existing study flows without a database migration.

- Question choices are shuffled when served, while grading uses their stable IDs.
- Quiz review matches results by question ID and shows the selected answer, the
  correct answer, and any stored answer explanations. The original question
  loader now retains explanations on future imports; existing blank explanations
  are not backfilled. Do not rerun that destructive loader just to add explanations.
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

## Follow-up work

1. Verify state exam profiles and law content against official sources; preserve
   source links and effective/review dates. The existing exam metadata is unchanged.
2. Replace separate, partly destructive content scripts with a repeatable import
   process that validates course/question completeness and preserves student history.
3. Add exam-specific timing and topic weights, held-out questions, and an evidence
   based readiness assessment.
4. Add optional sign-in that links anonymous progress and supports recovery.
5. Add the daily study plan and practical insurance scenarios after these foundations.
