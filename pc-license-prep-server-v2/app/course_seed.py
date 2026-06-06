from __future__ import annotations

DEFAULT_COURSE = {
    "modules": [
        {
            "slug": "insurance-basics",
            "title": "Insurance Basics",
            "description": "Core language and concepts every P&C student needs first.",
            "sort_order": 1,
            "lessons": [
                {
                    "slug": "what-is-insurance",
                    "title": "What Is Insurance?",
                    "summary": "Insurance transfers the financial impact of certain losses.",
                    "body": "Insurance is a contract where the insured pays premium and the insurer promises to pay covered losses according to the policy. The goal is indemnity, which means helping the insured recover financially after a covered loss.",
                    "example": "A homeowner pays premium for homeowners insurance. If a covered fire damages the home, the insurer pays according to the policy terms.",
                    "memory_tip": "Insurance transfers financial risk. It does not remove risk from life.",
                    "audio_script": "Insurance is a way to transfer financial risk. The insured pays premium. The insurer promises to pay covered losses. Insurance helps pay for covered losses after they happen.",
                    "estimated_minutes": 6,
                },
                {
                    "slug": "risk-peril-hazard",
                    "title": "Risk, Peril, and Hazard",
                    "summary": "Risk is chance of loss. Peril causes loss. Hazard increases loss.",
                    "body": "Risk is the possibility of loss. A peril is the actual cause of loss, such as fire, theft, wind, or collision. A hazard is a condition that increases the chance or severity of a loss.",
                    "example": "Fire is a peril. Faulty wiring is a physical hazard because it increases the chance of fire.",
                    "memory_tip": "Peril causes. Hazard raises the chances.",
                    "audio_script": "A peril is what causes the loss. A hazard is something that makes loss more likely or more serious.",
                    "estimated_minutes": 8,
                },
            ],
            "terms": [
                {"term": "Risk", "plain_english_definition": "The chance that a loss could happen.", "exam_definition": "The uncertainty or possibility of financial loss.", "example": "There is risk that a house could burn, a car could crash, or a business could be sued."},
                {"term": "Peril", "plain_english_definition": "The thing that causes the loss.", "exam_definition": "A cause of loss, such as fire, theft, wind, hail, or collision.", "example": "If lightning damages a home, lightning is the peril."},
                {"term": "Hazard", "plain_english_definition": "Something that makes a loss more likely or more severe.", "exam_definition": "A condition that increases the chance, frequency, or severity of loss.", "example": "Faulty wiring is a hazard because it increases the chance of fire."},
            ],
            "questions": [
                {
                    "lesson_slug": "risk-peril-hazard",
                    "question_text": "Which statement best describes a peril?",
                    "question_type": "multiple_choice",
                    "difficulty": "standard",
                    "explanation": "A peril is the cause of loss. Fire, theft, wind, and collision are common examples.",
                    "choices": [
                        {"choice_text": "The cause of loss", "is_correct": True, "explanation": "Correct. A peril causes the loss.", "sort_order": 1},
                        {"choice_text": "A policy premium", "is_correct": False, "explanation": "Premium is the price paid for coverage.", "sort_order": 2},
                        {"choice_text": "A policy condition", "is_correct": False, "explanation": "Conditions are rules and duties in the policy.", "sort_order": 3},
                        {"choice_text": "A deductible", "is_correct": False, "explanation": "A deductible is the insured's share of a covered loss.", "sort_order": 4},
                    ],
                },
            ],
        },
        {
            "slug": "insurance-contracts",
            "title": "Insurance Contracts",
            "description": "How insurance policies are structured and interpreted.",
            "sort_order": 2,
            "lessons": [
                {
                    "slug": "policy-sections",
                    "title": "Main Parts of an Insurance Policy",
                    "summary": "Policies usually include declarations, insuring agreement, conditions, exclusions, and endorsements.",
                    "body": "The declarations page identifies the insured, policy period, limits, premium, and covered property or exposures. The insuring agreement states the insurer's promise. Conditions explain duties and rules. Exclusions remove coverage. Endorsements change the policy.",
                    "example": "A homeowners declarations page may show the dwelling limit, deductible, policy dates, and named insured.",
                    "memory_tip": "Declarations summarize. Insuring agreement promises. Exclusions remove.",
                    "audio_script": "Think of a policy in sections. The declarations page gives the snapshot. The insuring agreement explains the promise. Conditions give rules. Exclusions remove coverage. Endorsements change the policy.",
                    "estimated_minutes": 7,
                },
            ],
            "terms": [
                {"term": "Declarations", "plain_english_definition": "The policy snapshot page.", "exam_definition": "The section that identifies key policy information such as insured, limits, dates, premium, and covered property or exposures.", "example": "The declarations page may list a dwelling limit."},
                {"term": "Exclusion", "plain_english_definition": "Something the policy does not cover.", "exam_definition": "Policy language that removes coverage for certain causes, people, property, or situations.", "example": "A flood exclusion removes coverage for flood loss under many property policies."},
            ],
            "questions": [
                {
                    "lesson_slug": "policy-sections",
                    "question_text": "Which policy section usually shows the named insured, policy period, and limits?",
                    "question_type": "multiple_choice",
                    "difficulty": "standard",
                    "explanation": "The declarations page is the policy snapshot and shows key identifying information.",
                    "choices": [
                        {"choice_text": "Declarations", "is_correct": True, "explanation": "Correct. Declarations summarize key policy information.", "sort_order": 1},
                        {"choice_text": "Exclusions", "is_correct": False, "explanation": "Exclusions remove coverage.", "sort_order": 2},
                        {"choice_text": "Subrogation", "is_correct": False, "explanation": "Subrogation is a recovery right, not the policy snapshot section.", "sort_order": 3},
                        {"choice_text": "Coinsurance", "is_correct": False, "explanation": "Coinsurance is a valuation or insurance-to-value condition.", "sort_order": 4},
                    ],
                },
            ],
        },
    ]
}
