#!/usr/bin/env python3
"""
lh_seed_part3.py  —  Life & Health course, modules 11-14
Modules: Government Health Programs, Disability Income Insurance,
         Long-Term Care Insurance, Ethics and Producer Responsibilities (L&H)
Run from pc-license-prep-server-v2/:
    .venv/bin/python3 scripts/lh_seed_part3.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import select, text
from app.database import SessionLocal, create_all
from app.models import Module, Lesson, Term, Question, AnswerChoice

MODULES = [
  {
    "slug": "government-health-programs",
    "title": "Government Health Programs",
    "description": "Medicare, Medicaid, and the ACA -- the public health insurance landscape every L&H producer must understand.",
    "sort_order": 111,
    "lessons": [
      { "slug": "lh-medicare", "title": "Medicare", "sort_order": 1, "estimated_minutes": 8,
        "summary": "Medicare has four parts: A (hospital), B (medical), C (Medicare Advantage), and D (prescription drugs).",
        "body": "Medicare is a federal health insurance program for Americans 65+ and certain disabled individuals. Administered by CMS.\n\nPart A (Hospital Insurance): covers inpatient hospital, skilled nursing facility, home health, and hospice. Premium-free for most people with 10+ years of Medicare tax contributions (40 quarters). Has a per-benefit-period deductible.\n\nPart B (Medical Insurance): covers physician services, outpatient care, preventive services, and durable medical equipment. Has a monthly premium (income-adjusted), annual deductible, and 20% coinsurance. Voluntary but penalties for late enrollment.\n\nPart C (Medicare Advantage): alternative to traditional Medicare offered by private insurers approved by Medicare. Provides all Part A and B benefits plus often Part D. Members pay Part B premium plus any plan premium.\n\nPart D (Prescription Drug Coverage): voluntary prescription drug benefit through private insurers. Requires monthly premium, deductible, and cost sharing.\n\nFor the exam: A = hospital (free for most). B = medical (premium + 20% coinsurance). C = Medicare Advantage (private). D = drugs (voluntary).",
        "example": "A 67-year-old uses Part A for a hip replacement hospitalization and Part B for post-surgical physician visits. She enrolled in Part D for her prescription medications.",
        "memory_tip": "A = Admitted/hospital. B = Bills/doctor visits. C = Choice/private plans. D = Drugs. A free for most; B has premium and 20% coinsurance." },
      { "slug": "lh-medicaid-aca", "title": "Medicaid and the ACA", "sort_order": 2, "estimated_minutes": 7,
        "summary": "Medicaid covers low-income individuals; the ACA eliminated pre-existing condition exclusions and created marketplace metal tiers.",
        "body": "Medicaid is a joint federal-state program covering low-income individuals and families. Eligibility is based on financial need. Covers long-term care in nursing homes -- critical coverage Medicare does not provide. Administered by states within federal guidelines. ACA expanded Medicaid eligibility to adults earning up to 138% of the federal poverty level in participating states.\n\nThe Affordable Care Act (ACA): prohibits denial of coverage for pre-existing conditions in individual and small group markets. Prohibits annual and lifetime benefit limits. Requires coverage of essential health benefits. Extends dependent coverage to age 26. Establishes Health Insurance Marketplaces with tax credits for eligible individuals.\n\nACA metal tiers: Bronze (lowest premium/highest cost sharing), Silver, Gold, Platinum (highest premium/lowest cost sharing). Catastrophic plans available to those under 30.\n\nFor the exam: Medicaid = income-based, state-administered, covers long-term care. ACA = no pre-existing exclusions, marketplaces, metal tiers, dependent to age 26.",
        "example": "A 28-year-old freelancer uses the ACA Marketplace to buy a Silver plan. Her income qualifies for a tax credit reducing her premium from $350 to $125/month.",
        "memory_tip": "Medicare = age 65+ (federal). Medicaid = low income (federal-state). ACA = no pre-existing exclusions, marketplaces, metal tiers, age 26 dependent rule." },
    ],
    "terms": [
      {"term": "Medicare Part A", "plain": "Federal hospital insurance for those 65+ covering inpatient care", "exam": "The Medicare part covering inpatient hospital care, skilled nursing facility care, home health, and hospice; premium-free for most with 10+ years of Medicare tax contributions.", "example": "Medicare Part A covers an 80-year-old's 5-day hospital stay following a heart attack."},
      {"term": "Medicare Part B", "plain": "Federal medical insurance covering physician visits and outpatient services", "exam": "The Medicare part covering physician services, outpatient care, preventive services, and durable medical equipment; requires a monthly premium and has an annual deductible and 20% coinsurance.", "example": "Medicare Part B covers a doctor's office visit with the beneficiary paying 20% coinsurance after the deductible."},
      {"term": "Medicare Part D", "plain": "Voluntary prescription drug coverage for Medicare beneficiaries", "exam": "A voluntary Medicare benefit providing prescription drug coverage through private insurance companies; requires a monthly premium and cost sharing.", "example": "Medicare Part D covers the 70-year-old's monthly prescriptions for blood pressure medications."},
      {"term": "Medicaid", "plain": "Joint federal-state health insurance for low-income individuals", "exam": "A joint federal-state program providing health coverage for low-income individuals, families, the disabled, and elderly meeting financial eligibility requirements; covers long-term care.", "example": "A family earning below the poverty level qualifies for Medicaid covering medical expenses with minimal cost sharing."},
      {"term": "ACA Metal Tiers", "plain": "ACA plan categories based on cost sharing split between insurer and insured", "exam": "The four categories of ACA Marketplace plans -- Bronze, Silver, Gold, and Platinum -- differing in premium and cost sharing; Bronze = lowest premium/highest cost sharing; Platinum = highest premium/lowest cost sharing.", "example": "A healthy 25-year-old chooses a Bronze plan for the low premium, accepting higher out-of-pocket costs."},
    ],
    "questions": [
      ("Medicare Part A covers which of the following services?",
       "multiple_choice", "standard",
       "Medicare Part A is hospital insurance. It covers inpatient hospital care, skilled nursing facility care following a qualifying hospital stay, home health care, and hospice care.",
       [("Inpatient hospital care and skilled nursing facility care", True, "Correct. Part A covers hospital-related services including inpatient care and skilled nursing."),
        ("Physician office visits and outpatient surgery", False, "Physician services and outpatient care are covered by Medicare Part B."),
        ("Prescription medications", False, "Prescription drugs are covered under Medicare Part D."),
        ("Vision and dental care", False, "Standard Medicare does not cover routine vision or dental.")]),
      ("A 66-year-old Medicare beneficiary visits her physician. After meeting her annual deductible, Medicare Part B will pay:",
       "multiple_choice", "standard",
       "Medicare Part B covers physician services with 80/20 coinsurance after the annual deductible. Medicare pays 80%; the beneficiary pays 20%.",
       [("80% of the approved amount with the beneficiary paying 20%", True, "Correct. Medicare Part B uses 80/20 coinsurance after the annual deductible."),
        ("100% of all covered physician services", False, "Medicare Part B uses 80/20 coinsurance; the beneficiary is responsible for 20%."),
        ("50% of covered services up to a maximum benefit", False, "Medicare Part B coinsurance is 80/20, not 50/50."),
        ("All covered services after a 10% copayment per visit", False, "Medicare Part B uses percentage coinsurance, not a per-visit copayment.")]),
      ("Medicaid differs from Medicare primarily in that:",
       "multiple_choice", "standard",
       "The key difference is eligibility basis. Medicare eligibility is based on age (65+) or disability. Medicaid eligibility is based on financial need. Medicaid is a joint federal-state program; Medicare is federal.",
       [("Medicaid eligibility is based on financial need rather than age", True, "Correct. Medicare = age-based (65+). Medicaid = income/financial need-based."),
        ("Medicaid covers only inpatient hospital services", False, "Medicaid covers a broad range of services including long-term care."),
        ("Medicaid is administered entirely by the federal government", False, "Medicaid is a joint federal-state program administered by individual states."),
        ("Medicaid only covers individuals who have paid into the program through payroll taxes", False, "Medicaid is funded by federal and state taxes; there is no individual contribution requirement.")]),
      ("Under the ACA, health insurance plans in the individual market must:",
       "multiple_choice", "standard",
       "The ACA prohibits individual and small group health plans from denying coverage or charging higher premiums based on pre-existing medical conditions.",
       [("Accept applicants regardless of pre-existing conditions", True, "Correct. The ACA prohibits pre-existing condition exclusions in individual and small group health insurance."),
        ("Offer coverage at no premium to low-income applicants", False, "The ACA provides premium tax credits for eligible individuals, but plans are not free."),
        ("Cover only services included in the federal government's recommended benefits list", False, "ACA plans must cover essential health benefits, which is broader than a narrow recommended list."),
        ("Limit annual deductibles to no more than $1,000 per person", False, "The ACA sets maximum out-of-pocket limits but does not cap deductibles at $1,000.")]),
      ("The ACA Bronze tier health plan is characterized by:",
       "multiple_choice", "standard",
       "Bronze plans have the lowest premiums but the highest cost sharing. They are appropriate for healthy individuals who want low monthly costs.",
       [("The lowest premium and highest out-of-pocket cost sharing", True, "Correct. Bronze = lowest premium + highest cost sharing."),
        ("The highest premium and lowest out-of-pocket cost sharing", False, "This describes Platinum plans."),
        ("Premiums and cost sharing equal to 80% of average plan costs", False, "80/20 cost sharing describes coinsurance within a plan, not the Bronze tier."),
        ("Coverage only for catastrophic medical events", False, "Catastrophic plans are a separate category; Bronze plans provide comprehensive coverage with higher cost sharing.")]),
    ],
  },
  {
    "slug": "disability-income-insurance",
    "title": "Disability Income Insurance",
    "description": "Insurance replacing earned income when illness or injury prevents the insured from working.",
    "sort_order": 112,
    "lessons": [
      { "slug": "lh-disability-basics", "title": "Disability Income Insurance Basics", "sort_order": 1, "estimated_minutes": 8,
        "summary": "DI replaces 60-70% of income; the elimination period, benefit period, and definition of disability are the key features.",
        "body": "Disability income insurance replaces a portion (60-70%) of earned income when a covered disability prevents working. Benefits are typically tax-free when paid from a personally purchased policy (premiums paid with after-tax dollars). Benefits from employer-paid group DI are taxable.\n\nElimination period (waiting period): time of disability that must pass before benefits begin. Typical: 30, 60, 90, 180, or 365 days. Longer elimination period = lower premium. 90 days is most common for long-term DI.\n\nBenefit period: how long benefits are paid once they begin. Short-term DI: 13-26 weeks. Long-term DI: 2 years, 5 years, to age 65, or lifetime. To age 65 is most comprehensive.\n\nDefinition of disability -- most important DI provision. Own occupation (most favorable): benefits paid if insured cannot perform the duties of their OWN specific occupation. Any occupation (most restrictive): benefits paid only if insured cannot perform the duties of ANY occupation for which reasonably qualified.\n\nFor the exam: elimination period = waiting time (longer = cheaper). Benefit period = how long (to 65 = best). Own occupation = most favorable definition.",
        "example": "A surgeon develops essential tremor. Under own occupation she qualifies for DI -- she cannot perform surgery even though she could teach medicine. Under any occupation she might be denied because she could work in another capacity.",
        "memory_tip": "Elimination = waiting time (longer = cheaper). Benefit period = how long (to 65 = best). Own occupation = can't do YOUR job = benefits. Any occupation = can't do ANY job = much harder." },
      { "slug": "lh-disability-provisions", "title": "Disability Income Policy Provisions", "sort_order": 2, "estimated_minutes": 7,
        "summary": "Residual disability, presumptive disability, and the recurrent disability clause are key DI policy provisions.",
        "body": "Residual (partial) disability pays a proportional benefit when the insured works at reduced capacity or reduced income. If disability causes 40% income loss, residual benefits pay 40% of the DI benefit.\n\nPresumptive disability automatically qualifies certain severe impairments as totally disabling: loss of both hands, both feet, both eyes, or one hand and one foot. Triggers benefits immediately without an elimination period.\n\nRecurrent disability: if the same or related disability returns within a specified period (typically 6 months) after recovery and return to work, it is treated as a continuation of the original disability -- the elimination period does not start over.\n\nSocial Security integration (offset): reduces DI benefits by the amount of Social Security disability benefits received, preventing total disability income from exceeding working income.\n\nFor the exam: residual = proportional benefit for partial disability. Presumptive = certain impairments automatically qualify. Recurrent = same disability within 6 months = continuation (no new elimination period).",
        "example": "An attorney recovers from a back injury and returns to work, then re-injures the same disc 4 months later. Recurrent disability treats it as a continuation -- no new elimination period required.",
        "memory_tip": "Residual = partial disability, proportional benefit. Presumptive = loss of both limbs/eyes = automatic total disability. Recurrent = same disability within 6 months = continuation, no new elimination." },
    ],
    "terms": [
      {"term": "Elimination Period (DI)", "plain": "Waiting period before disability income benefits begin", "exam": "The period of continuous disability that must pass before DI benefits begin; functions as a time deductible. Longer elimination periods result in lower premiums.", "example": "With a 90-day elimination period an insured who becomes disabled in January receives no DI benefits until April."},
      {"term": "Own Occupation", "plain": "DI definition paying benefits if the insured cannot do their specific job", "exam": "The most favorable DI definition of disability; pays benefits if the insured cannot perform the material duties of their own specific occupation, even if they could perform another.", "example": "A dentist with hand tremors qualifies for own-occupation DI because she cannot perform dentistry even though she could teach."},
      {"term": "Any Occupation", "plain": "DI definition paying benefits only if the insured cannot work in any capacity", "exam": "The most restrictive DI definition; pays benefits only if the insured cannot perform the duties of any occupation for which they are reasonably qualified by education, training, or experience.", "example": "A surgeon with hand tremors is denied DI under any-occupation because she could perform administrative medical work."},
      {"term": "Residual Disability", "plain": "Partial disability reducing income but not preventing work entirely", "exam": "A disability allowing the insured to work but at reduced capacity or earning; residual DI benefits pay proportionally based on the percentage of income loss.", "example": "After a back injury a salesperson works 3 days per week earning 60% of former income. Residual benefits pay 40% of the DI benefit."},
      {"term": "Presumptive Disability", "plain": "Severe impairments automatically qualifying as total disability", "exam": "A DI provision automatically classifying certain severe impairments (typically loss of two limbs, both eyes, or one limb and one eye) as total disability, triggering immediate benefits without an elimination period.", "example": "An insured who loses both legs is automatically totally disabled under the presumptive disability provision."},
    ],
    "questions": [
      ("The elimination period in a disability income policy is most similar to:",
       "multiple_choice", "standard",
       "The elimination period is a waiting period before benefits begin. It functions like a deductible but measured in time rather than dollars.",
       [("A deductible, but measured in time rather than dollars", True, "Correct. The elimination period is a time deductible -- the insured bears the financial impact of the first days/months of disability."),
        ("A grace period that allows the insured to miss premium payments", False, "A grace period relates to premium payment, not the disability waiting period."),
        ("A coinsurance provision that requires the insured to share in each benefit payment", False, "Coinsurance involves percentage sharing; the elimination period is a time-based waiting period."),
        ("A deductible that reduces each monthly benefit payment by a fixed amount", False, "The elimination period eliminates early payments entirely, not reduces ongoing payments.")]),
      ("A producer cannot perform her insurance sales duties due to a back injury but can work as a receptionist. Under the own occupation DI definition:",
       "scenario", "standard",
       "Under own occupation, benefits are paid if the insured cannot perform the material duties of their specific occupation. The ability to do other work is irrelevant.",
       [("She qualifies for DI benefits because she cannot perform her duties as a producer", True, "Correct. Own occupation pays if she cannot perform her specific occupation; other work ability is irrelevant."),
        ("She does not qualify because she can work as a receptionist", False, "Under own occupation the ability to do other work does not disqualify the insured."),
        ("She qualifies only if she actually works as a receptionist and earns less than before", False, "Own occupation does not require the insured to work in another capacity."),
        ("She qualifies only if her back injury is permanent and total", False, "Own occupation does not require permanent total disability.")]),
      ("Presumptive disability in a DI policy means:",
       "multiple_choice", "standard",
       "Presumptive disability automatically classifies certain severe impairments as total disability -- triggering full benefits immediately without an elimination period.",
       [("Certain severe impairments automatically qualify as total disability without an elimination period", True, "Correct. Presumptive disability waives the elimination period for specified catastrophic losses."),
        ("Any disability lasting more than 90 days is presumed to be permanent", False, "Presumptive disability refers to specific severe impairments, not duration."),
        ("The insurer presumes the insured is totally disabled if they cannot perform their own occupation", False, "Presumptive disability applies to specific physical losses like limb or sight."),
        ("A disability is presumed to exist if the attending physician certifies it", False, "Presumptive disability is triggered by specific physical losses, not physician certification alone.")]),
      ("Benefits from an individually purchased disability income policy are generally:",
       "multiple_choice", "standard",
       "When an individual pays DI insurance premiums with after-tax dollars, the benefits received are income-tax-free. Benefits from employer-paid group DI ARE taxable.",
       [("Income-tax-free to the insured because the premiums were paid with after-tax dollars", True, "Correct. Personally purchased DI benefits are tax-free because premiums were paid with after-tax money."),
        ("Taxable as ordinary income because they replace wages", False, "Personally purchased DI benefits are NOT taxable. Employer-paid group DI benefits ARE taxable."),
        ("Tax-deductible by the insured in the year the premiums are paid", False, "Personally purchased DI premiums are not tax-deductible for most individuals."),
        ("Subject to Social Security payroll taxes", False, "Disability income benefits are not subject to Social Security or FICA taxes.")]),
      ("An insured recovers from a disability and returns to work. The same disability recurs 5 months later. Under the recurrent disability provision:",
       "scenario", "standard",
       "The recurrent disability provision provides that if the same or related disability recurs within 6 months, it is treated as a continuation of the original. No new elimination period must be satisfied.",
       [("The disability is treated as a continuation and no new elimination period is required", True, "Correct. Recurrence within 6 months is treated as a continuation -- no new elimination period."),
        ("The insured must satisfy a new elimination period before benefits resume", False, "The recurrent disability provision prevents a new elimination period for related disabilities recurring within the specified period."),
        ("The insurer may deny benefits because the insured already recovered from this condition", False, "Recurrence does not allow the insurer to deny benefits that would otherwise be payable."),
        ("The insured receives double benefits for the recurrent disability period", False, "Recurrent disability provisions prevent a new elimination period; they do not provide double benefits.")]),
    ],
  },
  {
    "slug": "long-term-care-insurance",
    "title": "Long-Term Care Insurance",
    "description": "Coverage for extended custodial care services not covered by Medicare or health insurance.",
    "sort_order": 113,
    "lessons": [
      { "slug": "lh-ltc-basics", "title": "Long-Term Care Insurance Basics", "sort_order": 1, "estimated_minutes": 7,
        "summary": "LTC covers custodial care when the insured cannot perform 2 of 6 ADLs or has cognitive impairment -- Medicare does not cover this.",
        "body": "Long-term care insurance covers extended custodial care when the insured needs help with activities of daily living (ADLs) due to chronic illness, disability, or cognitive impairment. Medicare and health insurance generally do not cover this.\n\nThe six ADLs: bathing, dressing, eating, toileting, transferring (moving from bed to chair), and continence. LTC benefits triggered when the insured needs help with 2 or more ADLs.\n\nCognitive impairment (Alzheimer's, dementia) also triggers LTC benefits regardless of ADL status.\n\nCare settings: nursing home (most intensive), assisted living facility, adult day care, home health care. Modern LTC policies typically cover all settings.\n\nWhy Medicare does not cover LTC: Medicare covers skilled nursing after a qualifying hospital stay for up to 100 days (with cost sharing after day 20). Medicare does NOT cover custodial care (help with ADLs by non-skilled aides).\n\nMedicaid covers nursing home care but only after the insured has depleted virtually all assets -- a financial catastrophe plan, not a planning strategy.\n\nFor the exam: 2 of 6 ADLs or cognitive impairment triggers benefits. Medicare covers skilled care (limited). Medicaid covers nursing home after asset depletion.",
        "example": "An 82-year-old with Alzheimer's cannot bathe, dress, or remember to eat independently. Her LTC policy pays $5,000/month toward memory care. Medicare covers none of this custodial care.",
        "memory_tip": "6 ADLs: Bathing, Dressing, Eating, Toileting, Transferring, Continence. LTC pays when 2+ impaired OR cognitive impairment. Medicare = skilled care, limited. Medicaid = poverty plan. LTC = planning." },
      { "slug": "lh-ltc-policy-features", "title": "LTC Policy Features and Provisions", "sort_order": 2, "estimated_minutes": 7,
        "summary": "Elimination period, benefit period, inflation protection, and tax-qualified status are the key LTC policy features.",
        "body": "Elimination period: days of LTC services required before benefits begin (30-180 days). 90-day is common. Insured pays for care during this period.\n\nBenefit period: how long benefits will be paid (2 years, 5 years, lifetime). Lifetime provides greatest protection but is most expensive.\n\nInflation protection is critical -- LTC policies may be purchased decades before use and care costs rise significantly. Compound inflation protection increases benefits by a fixed percentage compounded annually (most expensive but most valuable). Simple inflation protection increases by a fixed percentage of the original benefit (cheaper but less powerful long-term).\n\nTax-qualified LTC policies (meeting IRS requirements): premiums may be treated as medical expenses for itemized deductions (age-based limits). Benefits are excluded from income.\n\nFree look period for LTC: 30 days (longer than standard 10 days, reflecting policy complexity).\n\nFor the exam: elimination period (30-180 days), benefit period (2 years to lifetime), compound inflation (best), tax-qualified (premiums deductible, benefits tax-free).",
        "example": "A 65-year-old buys LTC with 90-day elimination period, 5-year benefit, $200/day, and 5% compound inflation. By age 85 the daily benefit has grown to $530 due to 20 years of compounding.",
        "memory_tip": "LTC features: Elimination period (waiting days), Benefit period (how long), Daily amount, Inflation protection (compound = best). Tax-qualified = premiums deductible (limited), benefits tax-free." },
    ],
    "terms": [
      {"term": "Activities of Daily Living (ADLs)", "plain": "Basic self-care activities used to determine LTC eligibility", "exam": "The six basic self-care activities (bathing, dressing, eating, toileting, transferring, and continence) used to measure functional impairment; LTC pays when the insured cannot perform two or more ADLs.", "example": "An 80-year-old who cannot bathe or dress independently qualifies for LTC benefits -- two of six ADLs impaired."},
      {"term": "Long-Term Care Insurance", "plain": "Insurance covering extended custodial care not covered by Medicare", "exam": "Insurance covering the cost of extended custodial care when the insured cannot perform 2+ ADLs or has cognitive impairment; fills the gap left by Medicare and health insurance.", "example": "LTC insurance pays $6,000/month toward a memory care facility for an insured with Alzheimer's."},
      {"term": "Cognitive Impairment", "plain": "Mental conditions like Alzheimer's that also trigger LTC benefits", "exam": "A deterioration or loss of intellectual capacity including Alzheimer's and other dementias requiring substantial supervision; qualifies for LTC benefits regardless of ADL status.", "example": "An insured with severe Alzheimer's who can still perform ADLs qualifies for LTC benefits due to cognitive impairment."},
      {"term": "Inflation Protection (LTC)", "plain": "LTC feature increasing benefit amount to keep pace with rising care costs", "exam": "An LTC provision increasing the daily or monthly benefit over time -- compound (fixed % compounded annually) or simple (fixed % of original benefit) -- to offset rising care costs.", "example": "A $150/day LTC benefit with 5% compound inflation grows to $399/day after 20 years."},
      {"term": "Tax-Qualified LTC Policy", "plain": "LTC policy meeting IRS requirements allowing premium deductions and tax-free benefits", "exam": "An LTC policy meeting IRS requirements under HIPAA; premiums may be treated as medical expenses for itemized deductions (age-based limits) and benefits are excluded from gross income.", "example": "A 65-year-old can deduct up to $4,510 of tax-qualified LTC premiums as medical expenses."},
    ],
    "questions": [
      ("Long-term care insurance benefits are typically triggered when the insured:",
       "multiple_choice", "standard",
       "LTC benefits are triggered by inability to perform two or more of the six ADLs without substantial assistance, or by cognitive impairment requiring substantial supervision.",
       [("Cannot perform two or more activities of daily living or has cognitive impairment", True, "Correct. LTC benefits require inability to perform 2+ ADLs or the presence of cognitive impairment."),
        ("Is hospitalized for more than 60 consecutive days", False, "LTC covers custodial care needs, not primarily hospitalization."),
        ("Cannot perform any gainful employment", False, "Inability to work is the trigger for disability income insurance, not LTC."),
        ("Reaches age 65 and elects to begin receiving care", False, "LTC benefits are triggered by functional impairment, not by age alone.")]),
      ("Why does Medicare not cover most long-term care expenses?",
       "multiple_choice", "standard",
       "Medicare covers skilled nursing care after a qualifying hospital stay for a limited period. Medicare does NOT cover custodial care -- assistance with ADLs by non-skilled aides -- which is what most LTC involves.",
       [("Medicare covers skilled care but does not cover custodial care for ADL assistance", True, "Correct. Medicare's LTC limitation is its exclusion of custodial (non-skilled) care."),
        ("Medicare only covers care received in the beneficiary's home", False, "Medicare covers some care in skilled nursing facilities and home health settings."),
        ("Medicare covers long-term care only for beneficiaries under age 75", False, "Medicare has no age limitation for LTC coverage; it is the type of care that matters."),
        ("Medicare covers only the first 30 days of any long-term care stay", False, "Medicare covers up to 100 days in skilled nursing after a qualifying hospital stay, but this is skilled care only.")]),
      ("Compound inflation protection in a long-term care policy is preferred over simple inflation protection because:",
       "multiple_choice", "standard",
       "Compound inflation grows the benefit exponentially (on the growing balance). Simple inflation grows linearly (always on the original amount). Over long periods compound inflation significantly outpaces simple inflation.",
       [("Compound inflation grows the benefit exponentially, providing greater increases over time", True, "Correct. Compound inflation is more powerful long-term because each year's increase builds on the prior year's already-increased benefit."),
        ("Compound inflation protection costs less in premium than simple inflation protection", False, "Compound inflation protection is more expensive because it provides greater benefit increases."),
        ("Simple inflation protection guarantees a higher daily benefit amount in the first year", False, "Both options start with the same base benefit; the difference is how future increases are calculated."),
        ("Compound inflation protection has no maximum benefit limit", False, "LTC policies may have maximum benefit periods and amounts; inflation protection type does not remove these limits.")]),
      ("The free look period for long-term care insurance policies is:",
       "multiple_choice", "standard",
       "The free look period for LTC policies is 30 days, longer than the standard 10-day free look for most other insurance types, reflecting the complexity of LTC contracts.",
       [("30 days, longer than the standard free look for most insurance policies", True, "Correct. LTC policies have a 30-day free look period."),
        ("10 days, same as most other insurance policies", False, "LTC policies specifically provide a 30-day free look to allow adequate review."),
        ("60 days because of the complexity of LTC policy terms", False, "The LTC free look period is 30 days, not 60 days."),
        ("No free look period -- LTC policies are non-cancellable once issued", False, "All LTC policies must include a free look period; it is 30 days.")]),
      ("Which statement about tax-qualified long-term care insurance policies is correct?",
       "multiple_choice", "standard",
       "Tax-qualified LTC policies allow premiums to be treated as medical expenses for itemized deductions, subject to age-based limits. Benefits received are excluded from gross income.",
       [("Premiums may be deductible as medical expenses and benefits are received tax-free", True, "Correct. Tax-qualified LTC: premiums partially deductible (age-based limits) and benefits are tax-free."),
        ("Premiums are fully deductible regardless of the amount paid or the taxpayer's age", False, "Premium deductibility is subject to age-based limits, not unlimited."),
        ("Benefits are taxable income because they replace wages", False, "LTC benefits from qualified policies are tax-free; they are not wage replacement."),
        ("Tax-qualified LTC policies have the same benefit triggers as non-qualified policies", False, "Tax-qualified policies must meet specific IRS benefit trigger requirements to maintain tax-advantaged status.")]),
    ],
  },
  {
    "slug": "lh-ethics-producer",
    "title": "Ethics and Producer Responsibilities (L&H)",
    "description": "Ethical obligations, suitability requirements, and key regulations for life and health producers.",
    "sort_order": 114,
    "lessons": [
      { "slug": "lh-producer-ethics", "title": "L&H Producer Ethics and Suitability", "sort_order": 1, "estimated_minutes": 7,
        "summary": "Suitability requires recommending only products fitting the client's needs; replacement regulations prevent twisting and churning.",
        "body": "Suitability is a fundamental ethical obligation for life insurance and annuity sales. A producer must recommend only products suitable for the client's financial situation, needs, risk tolerance, and time horizon.\n\nThe NAIC Suitability in Annuity Transactions Model Regulation requires producers to obtain client financial information before recommending an annuity. Many states have adopted a best interest standard requiring the producer to act in the client's best interest.\n\nReplacement regulations require specific disclosure procedures when recommending replacement of an existing life or annuity policy. Replacement often disadvantages the client: new contestability period, new surrender charges, loss of cash value. Producers must provide comparison disclosures and notify the existing insurer.\n\nTwisting: using misrepresentation to induce replacement -- prohibited.\n\nChurning: recommending replacement primarily to generate a new commission within the same company -- prohibited.\n\nFor the exam: suitability, replacement regulations, twisting, and churning are the most tested L&H ethics topics.",
        "example": "A producer recommends replacing an elderly client's paid-up whole life policy with a new policy primarily because it pays a higher commission. This is churning -- recommending replacement for the producer's benefit, not the client's.",
        "memory_tip": "Suitability = must fit client needs. Replacement = disclose comparisons, notify prior insurer. Twisting = lying to get replacement. Churning = replacement for commission. All unethical and illegal." },
      { "slug": "lh-life-health-regulations", "title": "Life and Health Insurance Regulations", "sort_order": 2, "estimated_minutes": 7,
        "summary": "HIPAA, ERISA, and state insurance laws govern life and health insurance products and producer conduct.",
        "body": "State insurance regulation covers: producer licensing (licensed in each state), policy forms and rates (filed and approved), claims handling (prompt payment), and unfair trade practices (misrepresentation, rebating, twisting).\n\nERISA (Employee Retirement Income Security Act) governs employer-sponsored group benefit plans. It preempts state insurance laws for self-funded employer plans. Producers must understand ERISA disclosure requirements and fiduciary standards.\n\nHIPAA (Health Insurance Portability and Accountability Act) protects workers from losing health coverage when changing jobs. Limits pre-existing condition exclusions in group health plans. Establishes privacy protections (the Privacy Rule) for medical information.\n\nThe Affordable Care Act (ACA) changed individual and small group markets: no pre-existing condition exclusions, essential health benefits requirements, guaranteed issue, and community rating.\n\nThe Internal Revenue Code governs tax treatment: life insurance death benefits are generally income-tax-free under IRC Section 101. Annuity earnings grow tax-deferred. Employer health insurance premiums are generally tax-deductible.\n\nFor the exam: HIPAA = portability + privacy. ERISA = employer plans. ACA = individual/small group reforms. State = licensing + forms + unfair practices.",
        "example": "An employee changes jobs. Under HIPAA, the new group health plan must credit prior coverage toward any pre-existing condition waiting period, limiting gaps in coverage.",
        "memory_tip": "HIPAA = portability + privacy (health). ERISA = employer plans (preempts state law for self-funded). ACA = no pre-existing in individual/small group. State = licensing + forms + unfair practices." },
    ],
    "terms": [
      {"term": "Suitability", "plain": "Requirement to recommend only products fitting the client's needs and situation", "exam": "The obligation requiring insurance producers to recommend only products appropriate for the client's financial situation, needs, risk tolerance, time horizon, and objectives.", "example": "Selling a 75-year-old a 10-year deferred annuity when she needs funds in 3 years violates the suitability requirement."},
      {"term": "Replacement (Life/Annuity)", "plain": "Replacing an existing life or annuity policy with a new one", "exam": "A transaction in which new life insurance or an annuity is purchased and an existing policy is lapsed or surrendered; subject to specific disclosure and notification requirements.", "example": "The producer provides a comparison disclosure and notifies the existing insurer when recommending replacing a whole life policy."},
      {"term": "Twisting", "plain": "Using misrepresentation to induce replacement of an existing policy", "exam": "An unfair trade practice in which a producer uses misrepresentation to induce a policyowner to replace an existing policy; illegal in all states.", "example": "A producer falsely tells a client their existing policy has no value to convince them to replace it -- this is twisting."},
      {"term": "HIPAA", "plain": "Federal law protecting health coverage portability and medical information privacy", "exam": "The Health Insurance Portability and Accountability Act; limits pre-existing condition exclusions in group health plans, protects workers changing jobs, and establishes privacy protections for medical information.", "example": "Under HIPAA an employee moving to a new employer gets credit for prior coverage, limiting pre-existing condition waiting periods."},
      {"term": "ERISA", "plain": "Federal law governing employer-sponsored benefit plans", "exam": "The Employee Retirement Income Security Act; establishes standards for employer-sponsored pension and health benefit plans and preempts state insurance laws for self-funded employer health plans.", "example": "A self-funded employer health plan is governed by ERISA rather than state insurance law."},
    ],
    "questions": [
      ("A producer recommends that an elderly client replace her paid-up whole life policy with a new whole life policy primarily because the new policy pays a higher commission. This is:",
       "scenario", "standard",
       "Churning is recommending replacement primarily for the producer's financial benefit (commission) rather than the client's best interest.",
       [("Churning, which is recommending replacement primarily to generate a new commission", True, "Correct. Recommending replacement for commission rather than client benefit is churning."),
        ("Twisting, which involves using misrepresentation to induce replacement", False, "Churning involves replacement for commission without misrepresentation; twisting uses false information."),
        ("Misrepresentation, since the producer misled the client about the policy terms", False, "The scenario describes commission motivation without misrepresentation, making it churning."),
        ("Rebating, since the higher commission benefits the producer financially", False, "Rebating involves giving something of value to the client; churning involves self-serving replacement.")]),
      ("Under replacement regulations, when a producer recommends replacing an existing life insurance policy, the producer must:",
       "multiple_choice", "standard",
       "Replacement regulations require producers to provide a written comparison of the existing and replacement policies and to notify the existing insurer.",
       [("Provide a comparison of the existing and replacement policies and notify the existing insurer", True, "Correct. Replacement requires written comparison disclosure and notification to the existing insurer."),
        ("Obtain written approval from the state insurance department before completing the replacement", False, "State approval is not required; the requirements are disclosure and notification."),
        ("Cancel the existing policy before the new policy is issued", False, "The existing policy should be replaced after the new policy is issued to avoid a coverage gap."),
        ("Reduce the commission on the replacement policy by 50%", False, "Commission reduction is not a replacement regulation requirement.")]),
      ("The suitability requirement for annuity sales requires the producer to:",
       "multiple_choice", "standard",
       "Suitability requires producers to obtain information about the client's financial situation, needs, and objectives and to recommend only products appropriate for that client.",
       [("Obtain information about the client's financial situation and recommend only suitable products", True, "Correct. Suitability requires gathering client information and recommending products fitting their needs."),
        ("Recommend the annuity with the highest surrender charge as it has the best guarantees", False, "Suitability focuses on client needs, not maximizing surrender charges."),
        ("Recommend the annuity with the highest commission rate to maximize producer compensation", False, "Producer compensation is irrelevant to suitability -- the client's interest is paramount."),
        ("Recommend annuities only to clients over age 65", False, "Suitability analysis is required for all clients regardless of age.")]),
      ("HIPAA's portability provisions protect workers who change jobs by:",
       "multiple_choice", "standard",
       "HIPAA portability provisions require new group health plans to credit prior creditable coverage toward any pre-existing condition waiting period, limiting gaps in health coverage when workers change employers.",
       [("Crediting prior group coverage toward pre-existing condition waiting periods at the new employer", True, "Correct. HIPAA portability gives credit for prior coverage, limiting pre-existing condition waiting periods."),
        ("Requiring the new employer to provide identical coverage as the old employer", False, "HIPAA does not require identical coverage; it credits prior coverage toward waiting periods."),
        ("Guaranteeing the worker can continue the old employer's plan for 18 months", False, "18-month continuation is COBRA, not HIPAA portability."),
        ("Prohibiting any pre-existing condition exclusions in group health plans", False, "HIPAA limits exclusions by crediting prior coverage; the ACA more broadly prohibits them in individual markets.")]),
      ("A life and health insurance producer who sells variable life insurance must hold:",
       "multiple_choice", "standard",
       "Variable life insurance is a security because the policyowner bears investment risk. Selling it requires both a state life insurance license AND a FINRA securities registration.",
       [("Both a life insurance license and a FINRA securities registration", True, "Correct. Variable products require both insurance and securities credentials."),
        ("Only a life insurance license since variable life is an insurance product", False, "Variable life's investment component makes it a security requiring both credentials."),
        ("Only a FINRA securities license since the investment component dominates", False, "Both credentials are required; neither alone is sufficient."),
        ("A life insurance license plus a Series 65 investment adviser license", False, "Variable product sales require a Series 6 or 7 (broker-dealer), not a Series 65 (investment adviser).")]),
    ],
  },
]


def seed_part3():
    create_all()
    db = SessionLocal()
    try:
        mod_count = lesson_count = term_count = q_count = 0

        for mod_data in MODULES:
            existing = db.scalar(select(Module).where(Module.slug == mod_data["slug"]))
            if existing:
                print(f"  SKIP (exists): {mod_data['slug']}")
                continue

            mod = Module(
                slug=mod_data["slug"],
                title=mod_data["title"],
                description=mod_data["description"],
                sort_order=mod_data["sort_order"],
                is_active=True,
            )
            db.add(mod)
            db.flush()
            db.execute(text("UPDATE modules SET course='lh' WHERE id=:id"), {"id": mod.id})
            mod_count += 1
            print(f"  MODULE: {mod.title}")

            for i, ld in enumerate(mod_data["lessons"], 1):
                db.add(Lesson(
                    module_id=mod.id, slug=ld["slug"], title=ld["title"],
                    summary=ld.get("summary", ""), body=ld.get("body", ""),
                    example=ld.get("example", ""), memory_tip=ld.get("memory_tip", ""),
                    audio_script="", estimated_minutes=ld.get("estimated_minutes", 7),
                    sort_order=ld.get("sort_order", i), is_active=True,
                ))
                lesson_count += 1

            for td in mod_data["terms"]:
                db.add(Term(
                    module_id=mod.id, lesson_id=None,
                    term=td["term"],
                    plain_english_definition=td["plain"],
                    exam_definition=td["exam"],
                    example=td["example"],
                ))
                term_count += 1

            db.flush()

            lessons = db.scalars(
                select(Lesson).where(Lesson.module_id == mod.id).order_by(Lesson.sort_order)
            ).all()
            first_lesson_id = lessons[0].id if lessons else None

            for q_text, q_type, difficulty, explanation, choices in mod_data["questions"]:
                q = Question(
                    module_id=mod.id, lesson_id=first_lesson_id,
                    question_text=q_text, question_type=q_type,
                    difficulty=difficulty, explanation=explanation, is_active=True,
                )
                db.add(q)
                db.flush()
                for sort_i, (ct, correct, ce) in enumerate(choices, 1):
                    db.add(AnswerChoice(
                        question_id=q.id, choice_text=ct,
                        is_correct=correct, explanation=ce, sort_order=sort_i,
                    ))
                q_count += 1

        db.commit()
        print(f"\n=== Part 3 complete: {mod_count} modules, {lesson_count} lessons, {term_count} terms, {q_count} questions ===")

        # Final summary across all LH modules
        total_lh = db.execute(
            text("SELECT COUNT(*) FROM modules WHERE course='lh'")
        ).scalar()
        total_lessons = db.execute(
            text("SELECT COUNT(*) FROM lessons l JOIN modules m ON m.id=l.module_id WHERE m.course='lh'")
        ).scalar()
        total_terms = db.execute(
            text("SELECT COUNT(*) FROM terms t JOIN modules m ON m.id=t.module_id WHERE m.course='lh'")
        ).scalar()
        total_q = db.execute(
            text("SELECT COUNT(*) FROM questions q JOIN modules m ON m.id=q.module_id WHERE m.course='lh'")
        ).scalar()
        print(f"\n=== FULL L&H COURSE TOTALS ===")
        print(f"Modules:   {total_lh}")
        print(f"Lessons:   {total_lessons}")
        print(f"Terms:     {total_terms}")
        print(f"Questions: {total_q}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_part3()
