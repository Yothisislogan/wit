"""Only source-checked exam facts are published; unknown values stay absent.

Format review does not certify the practice question bank or its topic coverage.
"""
from copy import deepcopy

STATE_NAMES = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}
NC_SOURCE = "https://www.pearsonvue.com/content/dam/VUE/vue/en/documents/publications/123400.pdf"
STATE_EXAM_INFO = {
    code: {"state_name": name, "review_status": "pending", "vendor": "Exam details awaiting verification",
           "pc_exam": None, "lh_exam": None, "profiles": [], "state_topics": [],
           "outline_url": None, "content_review_status": "pending"}
    for code, name in STATE_NAMES.items()
}
STATE_EXAM_INFO["NC"].update({
    "review_status": "format_verified", "vendor": "Pearson VUE", "outline_url": NC_SOURCE,
    "reviewed_at": "2026-09-13",
    "profiles": [
        {"id": "nc-" + line, "name": name, "course": course,
         "scored_questions": 55, "pretest_questions_max": 5, "duration_minutes": 75,
         "passing_score": 70, "score_type": "scaled", "source_url": NC_SOURCE,
         "outline_effective_from": "2024-03-15", "reviewed_at": "2026-09-13"}
        for line, name, course in [
            ("property", "Property", "pc"), ("casualty", "Casualty", "pc"),
            ("life", "Life", "lh"), ("health", "Accident & Health or Sickness", "lh")]
    ]
})


def state_profile(code):
    return {"state": code, **deepcopy(STATE_EXAM_INFO[code])}
