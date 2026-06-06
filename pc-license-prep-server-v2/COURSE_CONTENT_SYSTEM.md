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

Recommended final module map:

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

Recommended question types:

- multiple choice
- true/false
- scenario
- definition
- coverage applies
- exclusion recognition
- best-answer exam style

### Answer explanations

Every wrong answer should explain why it is wrong.

This matters because students often learn more from missed questions than from lessons.

## Recommended content expansion target

For the free public launch:

- 14 modules
- 75 to 100 lessons
- 500+ questions
- 150+ glossary terms
- 40+ scenarios
- 3 final practice exams

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

The current V2 seed system loads default Python seed data. The next upgrade should support admin upload/export of JSON or CSV content.

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
