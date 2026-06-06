# Course Content System

This project should win because the course content is clear, practical, and easy to expand. The goal is not just to pass a test. The goal is to help a beginner understand insurance well enough to answer exam questions with confidence.

## Content philosophy

Every lesson should follow this pattern:

1. Plain-English explanation
2. Exam vocabulary
3. Real-world example
4. Memory tip
5. Audio-friendly script
6. Practice questions
7. Mistake review

The content should stay general until state-specific modules are intentionally added.

## Core content objects

### Modules

Modules are the top-level course sections.

Current module map:

1. Insurance Basics
2. Insurance Contracts
3. Property Insurance Fundamentals
4. Casualty Insurance Fundamentals
5. Personal Auto
6. Homeowners
7. Dwelling Policies
8. Commercial Property
9. Commercial General Liability
10. Business Auto
11. Workers Compensation and Employers Liability
12. Crime, Bonds, and Specialty Coverages
13. Ethics and Producer Responsibilities
14. Exam Prep and Final Review

### Lessons

Lessons should be short enough to finish in 5 to 10 minutes.

Each lesson has:

- title
- summary
- body
- example
- memory tip
- audio script
- estimated minutes

The `audio_script` field matters. Audio should sound conversational, not like someone reading a textbook.

### Terms

Each glossary term should have:

- term
- plain-English definition
- exam definition
- example

Example:

```text
Term: Peril
Plain English: The thing that causes the loss.
Exam Definition: A cause of loss, such as fire, theft, wind, hail, or collision.
Example: If lightning damages a home, lightning is the peril.
```

### Questions

Questions should not only mark right or wrong. They should teach.

Each question should have:

- module
- lesson
- question text
- question type
- difficulty
- explanation
- answer choices
- explanation for each answer choice

Current question types:

- multiple choice
- scenario
- final_exam

Recommended future question types:

- true/false
- definition
- coverage applies
- exclusion recognition
- best-answer exam style

### Answer explanations

Every wrong answer should explain why it is wrong.

This matters because students often learn more from missed questions than from lessons.

## Current question-bank volume

The V2 seed system now uses `app/question_expander.py` to generate a large study bank from the curated module, lesson, and glossary content.

Current targets:

```text
Baseline review: 14 modules x 75 = 1,050 questions
Scenario bank:   14 modules x 25 =   350 questions
Hard bank:       14 modules x 10 =   140 questions
Final simulation:                     100 questions
Estimated total:                    1,640 questions
```

This gets the project above the 1,000 to 1,500 question-pool target. The next quality step is SME review and hand-polishing of the most important scenario and final-exam questions.

## Quality tiers

The bank is organized into four practical tiers:

1. **Baseline review** — definition, memory, and concept questions.
2. **Scenario bank** — fact-pattern questions that ask the candidate to apply a concept.
3. **Hard bank** — questions with tricky wording like except, not, best, most likely, always, and only.
4. **Final simulation** — mixed-topic exam-style questions across the full course.

## Difficulty levels

Use these values:

- beginner
- standard
- challenging
- exam_style

## Tags to add later

The next version should add tagging so weak areas can be measured more precisely.

Recommended tags:

- property
- casualty
- auto
- homeowners
- commercial
- contracts
- ethics
- valuation
- liability
- exclusions
- conditions
- definitions

## Import/export direction

The current V2 seed system loads Python seed data and generated question banks. The next upgrade should support admin upload/export of JSON or CSV content.

Recommended admin workflows:

- upload new question bank
- export all questions
- edit individual question
- deactivate bad question
- clone lesson
- preview as student
- flag question for review

## Why admin comes after this

Admin tools should come after the database structure is stable. Otherwise the admin panel gets built around the wrong content model.

The priority order is:

1. Correct content schema
2. Reliable import/seed flow
3. Student-facing API
4. Progress and quiz tracking
5. Admin editing tools
