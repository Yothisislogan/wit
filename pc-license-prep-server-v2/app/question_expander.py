from __future__ import annotations

from copy import deepcopy

# Question-bank volume targets.
# 14 modules at these settings produces roughly:
# baseline 1,050 + scenario 350 + hard 140 + final simulation 100 = 1,640 questions.
BASELINE_QUESTIONS_PER_MODULE = 75
SCENARIO_QUESTIONS_PER_MODULE = 25
HARD_QUESTIONS_PER_MODULE = 10
FINAL_EXAM_SIMULATION_QUESTIONS = 100

GENERIC_DISTRACTORS = [
    ("It means every possible loss is automatically covered.", "No insurance policy automatically covers every possible loss."),
    ("It is only a state-specific licensing rule.", "This course section is testing general P&C knowledge, not state-specific licensing rules."),
    ("It is mainly a life insurance concept.", "This question is about general property and casualty insurance."),
    ("It removes the need to read the policy.", "Coverage depends on the actual policy terms, conditions, and exclusions."),
    ("It is the same thing as a premium payment.", "Premium is the price paid for coverage, not the concept being tested."),
]

SCENARIO_SETUPS = [
    "A customer gives a short claim story and asks which concept applies.",
    "A candidate must identify the key policy concept from a fact pattern.",
    "An insured asks why a claim may depend on policy wording.",
    "A producer is explaining coverage basics to a new client.",
    "A practice exam question includes extra facts that may distract the candidate.",
]

HARD_CLUES = [
    "except",
    "not",
    "best",
    "most likely",
    "first",
    "only if supported by policy language",
]


def _choice(text: str, correct: bool, explanation: str, order: int) -> dict:
    return {
        "choice_text": text,
        "is_correct": correct,
        "explanation": explanation,
        "sort_order": order,
    }


def _ordered(correct: tuple[str, str], wrongs: list[tuple[str, str]], rotate: int) -> list[dict]:
    raw = [(correct[0], True, correct[1])] + [(w[0], False, w[1]) for w in wrongs[:3]]
    shift = rotate % len(raw)
    raw = raw[shift:] + raw[:shift]
    return [_choice(text, ok, exp, idx + 1) for idx, (text, ok, exp) in enumerate(raw)]


def _terms(module: dict) -> list[dict]:
    return module.get("terms", []) or [{
        "term": module["title"],
        "plain_english_definition": module["description"],
        "exam_definition": module["description"],
        "example": module["description"],
    }]


def _lessons(module: dict) -> list[dict]:
    return module.get("lessons", []) or [{
        "slug": module["slug"],
        "title": module["title"],
        "summary": module["description"],
        "body": module["description"],
        "memory_tip": module["description"],
    }]


def _other_term_names(module: dict, current: str) -> list[str]:
    names = [t["term"] for t in _terms(module) if t["term"] != current]
    return names or ["Premium", "Deductible", "Exclusion"]


def _term_question(module: dict, lesson_slug: str, term: dict, number: int, bank_label: str = "baseline") -> dict:
    variant = number % 15
    term_name = term["term"]
    others = _other_term_names(module, term_name)
    wrong_terms = [(others[0], f"{others[0]} is a different term."), (others[-1], f"{others[-1]} is a different term.")]
    generic = GENERIC_DISTRACTORS[number % len(GENERIC_DISTRACTORS)]

    if variant == 0:
        prompt = f"Which plain-English definition best matches {term_name}?"
        correct = (term["plain_english_definition"], f"Correct. {term_name}: {term['plain_english_definition']}")
        wrongs = wrong_terms + [generic]
    elif variant == 1:
        prompt = f"Which exam-style definition best matches {term_name}?"
        correct = (term["exam_definition"], f"Correct. This is the exam-style meaning of {term_name}.")
        wrongs = wrong_terms + [generic]
    elif variant == 2:
        prompt = f"A question describes this situation: {term['example']} Which term is most closely related?"
        correct = (term_name, f"Correct. The example describes {term_name}.")
        wrongs = wrong_terms + [generic]
    elif variant == 3:
        prompt = f"Which statement is NOT accurate about {term_name}?"
        correct = ("It guarantees every claim will be paid.", "Correct. No term or coverage concept guarantees every claim will be paid.")
        wrongs = [
            (term["plain_english_definition"], "This is accurate, so it is not the best answer to a NOT question."),
            (term["exam_definition"], "This is accurate, so it is not the best answer to a NOT question."),
            (f"Example: {term['example']}", "This is consistent with the term."),
        ]
    elif variant == 4:
        prompt = f"A candidate keeps confusing {term_name} with another term. What should they remember?"
        correct = (term["plain_english_definition"], "Correct. Start with the plain-English meaning, then connect it to the exam definition.")
        wrongs = [generic] + wrong_terms
    elif variant == 5:
        prompt = f"In the {module['title']} module, why is {term_name} important?"
        correct = ("It helps identify what the question is really testing.", "Correct. Key terms are clues to the coverage concept being tested.")
        wrongs = [generic] + wrong_terms
    elif variant == 6:
        prompt = f"Which answer best applies {term_name} to a real insurance situation?"
        correct = (term["example"], "Correct. This example applies the term in context.")
        wrongs = [generic] + wrong_terms
    elif variant == 7:
        prompt = f"What is the safest exam approach when you see the term {term_name}?"
        correct = ("Match the term to its definition before choosing a coverage answer.", "Correct. Definitions drive many P&C exam questions.")
        wrongs = [generic] + wrong_terms
    elif variant == 8:
        prompt = f"Which phrase would be the best flashcard answer for {term_name}?"
        correct = (term["plain_english_definition"], "Correct. This is concise enough for flashcard review.")
        wrongs = [generic] + wrong_terms
    elif variant == 9:
        prompt = f"Which statement about {term_name} should a new candidate trust most?"
        correct = (term["exam_definition"], "Correct. Exam wording is usually closest to the formal definition.")
        wrongs = [generic] + wrong_terms
    elif variant == 10:
        prompt = f"If a practice question uses this clue — {term['example']} — what should the candidate think of first?"
        correct = (term_name, "Correct. The clue points to this term.")
        wrongs = wrong_terms + [generic]
    elif variant == 11:
        prompt = f"Which option is the best reason to study {term_name}?"
        correct = ("It appears in scenario questions and definition questions.", "Correct. Most core terms are tested in both ways.")
        wrongs = [generic] + wrong_terms
    elif variant == 12:
        prompt = f"What should a candidate avoid assuming about {term_name}?"
        correct = ("That it means coverage applies in every situation.", "Correct. A term may help identify coverage, but policy terms still control.")
        wrongs = [generic] + wrong_terms
    elif variant == 13:
        prompt = f"Which answer best connects {term_name} to the policy-reading process?"
        correct = ("Use the term to find the relevant coverage, condition, or exclusion.", "Correct. Exam questions often test how terms fit into policy structure.")
        wrongs = [generic] + wrong_terms
    else:
        prompt = f"Which statement would be most helpful for a quick review of {term_name}?"
        correct = (f"{term_name}: {term['plain_english_definition']}", "Correct. This is a useful quick-review statement.")
        wrongs = [generic] + wrong_terms

    return {
        "lesson_slug": lesson_slug,
        "question_text": f"[{bank_label.upper()}][{module['title']}] {prompt}",
        "question_type": "scenario" if variant in {2, 6, 10} else "multiple_choice",
        "difficulty": "beginner" if variant in {0, 1, 8, 14} else "standard",
        "explanation": term["exam_definition"],
        "choices": _ordered(correct, wrongs, number),
    }


def _lesson_question(module: dict, lesson: dict, number: int, bank_label: str = "baseline") -> dict:
    variant = number % 15
    title = lesson["title"]
    summary = lesson.get("summary") or lesson.get("body", "").split(".")[0] + "."
    body = lesson.get("body", summary)
    generic = GENERIC_DISTRACTORS[number % len(GENERIC_DISTRACTORS)]

    if variant == 0:
        prompt = f"What is the main point of the lesson '{title}'?"
        correct = (summary, "Correct. This captures the central lesson point.")
    elif variant == 1:
        prompt = f"A candidate is reviewing '{title}'. What should they focus on first?"
        correct = ("Identify the key coverage concept before reading the answer choices.", "Correct. This is a strong exam strategy.")
    elif variant == 2:
        prompt = f"Which statement best summarizes '{title}' for exam prep?"
        correct = (body.split(".")[0] + ".", "Correct. This sentence captures the core concept.")
    elif variant == 3:
        prompt = f"What mistake should a candidate avoid in '{title}' questions?"
        correct = ("Assuming coverage without checking terms, conditions, and exclusions.", "Correct. Coverage depends on policy language.")
    elif variant == 4:
        prompt = f"Which study action best fits the lesson '{title}'?"
        correct = ("Create a plain-English definition, then test it with a scenario.", "Correct. This builds both memory and application.")
    elif variant == 5:
        prompt = f"Why might '{title}' appear on a licensing exam?"
        correct = ("It tests whether the candidate can apply a general P&C concept.", "Correct. The exam often tests application, not just memorization.")
    elif variant == 6:
        prompt = f"Which answer is the best exam habit for '{title}'?"
        correct = ("Read the full question stem before selecting an answer.", "Correct. Small words can change the meaning of the question.")
    elif variant == 7:
        prompt = f"When reviewing '{title}', what should the candidate write in notes?"
        correct = (summary, "Correct. Notes should capture the key point in simple language.")
    elif variant == 8:
        prompt = f"Which response best applies '{title}' to a scenario question?"
        correct = ("Find the fact pattern, connect it to the coverage concept, then eliminate distractors.", "Correct. This is the best scenario-question approach.")
    elif variant == 9:
        prompt = f"What does '{title}' help a candidate understand?"
        correct = (module["description"], "Correct. The lesson supports this module objective.")
    elif variant == 10:
        prompt = f"Which answer is most consistent with the audio review for '{title}'?"
        correct = (summary, "Correct. The audio script reinforces the main point.")
    elif variant == 11:
        prompt = f"If a candidate misses questions from '{title}', what should they do next?"
        correct = ("Review the lesson, study the glossary terms, and retry missed questions.", "Correct. That is the intended learning loop.")
    elif variant == 12:
        prompt = f"Which answer choice would usually be suspicious in a '{title}' question?"
        correct = ("An answer using absolute words like always or every without policy support.", "Correct. Absolute wording is often a warning sign.")
    elif variant == 13:
        prompt = f"What is the best way to remember '{title}'?"
        correct = (lesson.get("memory_tip") or summary, "Correct. The memory tip is designed for quick recall.")
    else:
        prompt = f"Which statement is most useful for final review of '{title}'?"
        correct = (summary, "Correct. This is the key takeaway.")

    wrongs = [
        generic,
        ("Ignore the policy language and rely on what seems fair.", "Insurance exams test policy concepts, not only what seems fair."),
        ("Only memorize state-specific rules for this general module.", "This course section is state-neutral general P&C study."),
    ]
    return {
        "lesson_slug": lesson["slug"],
        "question_text": f"[{bank_label.upper()}][{module['title']}] {prompt}",
        "question_type": "scenario" if variant in {8, 11} else "multiple_choice",
        "difficulty": "exam_style" if variant in {3, 6, 12} else "standard",
        "explanation": body,
        "choices": _ordered(correct, wrongs, number),
    }


def _scenario_question(module: dict, lesson: dict, term: dict, number: int) -> dict:
    setup = SCENARIO_SETUPS[number % len(SCENARIO_SETUPS)]
    prompt = (
        f"[SCENARIO][{module['title']}] {setup} The fact pattern says: {term['example']} "
        f"Which answer best connects this fact pattern to {lesson['title']}?"
    )
    correct = (term["term"], f"Correct. The scenario points to {term['term']}: {term['exam_definition']}")
    wrongs = [
        ("Assume the loss is covered without reading the policy.", "Coverage cannot be assumed without policy language."),
        ("Treat it as a state-specific law question.", "This is testing the general P&C concept in the scenario."),
        ("Ignore the described fact pattern and choose the broadest sounding answer.", "Scenario questions require matching the facts to the concept."),
    ]
    return {
        "lesson_slug": lesson["slug"],
        "question_text": prompt,
        "question_type": "scenario",
        "difficulty": "challenging" if number % 3 == 0 else "standard",
        "explanation": f"Scenario review: {term['term']} means {term['exam_definition']}",
        "choices": _ordered(correct, wrongs, number),
    }


def _hard_question(module: dict, lesson: dict, term: dict, number: int) -> dict:
    clue = HARD_CLUES[number % len(HARD_CLUES)]
    prompt = (
        f"[HARD][{module['title']}] Which answer is the {clue} answer about {term['term']} "
        f"when applying the lesson '{lesson['title']}'?"
    )
    if clue in {"except", "not"}:
        correct = ("It means the policy will respond to every loss, regardless of exclusions.", "Correct. That statement is inaccurate; exclusions and conditions still matter.")
        wrongs = [
            (term["plain_english_definition"], "This is a fair description, so it is not the best answer to an EXCEPT/NOT question."),
            (term["exam_definition"], "This is consistent with the term."),
            (f"Example: {term['example']}", "This example is consistent with the term."),
        ]
    else:
        correct = ("Read the policy concept, identify the tested term, then eliminate answers with unsupported absolutes.", "Correct. This is the safest hard-question method.")
        wrongs = [
            ("Pick the answer that sounds most customer-friendly.", "Exam answers must match policy concepts, not only fairness."),
            ("Assume broad coverage unless the question says otherwise.", "Insurance questions require specific policy support."),
            ("Ignore words like not, except, always, and only.", "Those words often change the entire question."),
        ]
    return {
        "lesson_slug": lesson["slug"],
        "question_text": prompt,
        "question_type": "multiple_choice",
        "difficulty": "exam_style",
        "explanation": f"Hard question strategy: watch clue words like {', '.join(HARD_CLUES)}.",
        "choices": _ordered(correct, wrongs, number),
    }


def _final_exam_question(module: dict, lesson: dict, term: dict, number: int) -> dict:
    prompt = (
        f"[FINAL SIM][Q{number + 1}] A licensing candidate sees a mixed question from {module['title']}. "
        f"It references {term['term']} and the lesson '{lesson['title']}'. What is the best answer?"
    )
    correct = (term["exam_definition"], f"Correct. The final exam simulation is testing {term['term']} in context.")
    wrongs = [
        ("Choose the broadest answer because insurance is designed to cover all losses.", "Insurance does not cover all losses; policy wording controls."),
        ("Ignore the lesson topic and focus only on the longest answer.", "The longest answer is not automatically correct."),
        ("Treat it as a life and health question.", "This course is testing property and casualty concepts."),
    ]
    return {
        "lesson_slug": lesson["slug"],
        "question_text": prompt,
        "question_type": "final_exam",
        "difficulty": "exam_style",
        "explanation": f"Final review: {term['term']} means {term['exam_definition']}",
        "choices": _ordered(correct, wrongs, number),
    }


def _append_unique(questions: list[dict], candidate: dict, seen: set[str], number: int) -> None:
    text = candidate["question_text"]
    if text in seen:
        candidate["question_text"] = f"{text} #{number}"
    seen.add(candidate["question_text"])
    questions.append(candidate)


def expand_question_bank(course: dict) -> dict:
    expanded = deepcopy(course)
    modules = expanded.get("modules", [])

    for module in modules:
        questions = module.setdefault("questions", [])
        seen = {q.get("question_text") for q in questions}
        lessons = _lessons(module)
        terms = _terms(module)

        number = 0
        while len(questions) < BASELINE_QUESTIONS_PER_MODULE:
            if number % 2 == 0:
                term = terms[number % len(terms)]
                lesson_slug = lessons[number % len(lessons)]["slug"]
                candidate = _term_question(module, lesson_slug, term, number, "baseline")
            else:
                lesson = lessons[number % len(lessons)]
                candidate = _lesson_question(module, lesson, number, "baseline")
            _append_unique(questions, candidate, seen, number)
            number += 1

        for i in range(SCENARIO_QUESTIONS_PER_MODULE):
            lesson = lessons[i % len(lessons)]
            term = terms[(i * 2) % len(terms)]
            _append_unique(questions, _scenario_question(module, lesson, term, i), seen, i)

        for i in range(HARD_QUESTIONS_PER_MODULE):
            lesson = lessons[i % len(lessons)]
            term = terms[(i * 3) % len(terms)]
            _append_unique(questions, _hard_question(module, lesson, term, i), seen, i)

    final_seen = set()
    final_number = 0
    while final_number < FINAL_EXAM_SIMULATION_QUESTIONS and modules:
        module = modules[final_number % len(modules)]
        lessons = _lessons(module)
        terms = _terms(module)
        lesson = lessons[final_number % len(lessons)]
        term = terms[(final_number * 2) % len(terms)]
        module_questions = module.setdefault("questions", [])
        module_seen = {q.get("question_text") for q in module_questions} | final_seen
        candidate = _final_exam_question(module, lesson, term, final_number)
        _append_unique(module_questions, candidate, module_seen, final_number)
        final_seen.add(candidate["question_text"])
        final_number += 1

    return expanded
