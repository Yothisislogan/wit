#!/usr/bin/env python3
"""
lh_seed_part1.py  —  Life & Health course, modules 1-5
Modules: Life Insurance Basics, Term Life, Whole Life,
         Universal/Variable Life, Life Policy Provisions
Run from pc-license-prep-server-v2/:
    .venv/bin/python3 scripts/lh_seed_part1.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import select, text
from app.database import SessionLocal, create_all
from app.models import Module, Lesson, Term, Question, AnswerChoice

MODULES = [
  {
    "slug": "life-insurance-basics",
    "title": "Life Insurance Basics",
    "description": "Foundational concepts — purpose, insurable interest, parties to the contract, and underwriting.",
    "sort_order": 101,
    "lessons": [
      { "slug": "lh-purpose-of-life-insurance", "title": "Purpose of Life Insurance", "sort_order": 1, "estimated_minutes": 7,
        "summary": "Life insurance replaces income lost when a breadwinner dies, protecting dependents from financial hardship.",
        "body": "Life insurance exists to solve a fundamental financial problem: the death of a person who supports others financially. When a breadwinner dies, the income disappears but the expenses do not. Mortgage payments, car loans, grocery bills, and college tuition continue. Life insurance replaces that lost income stream with a lump sum paid to the people who depended on it.\n\nBeyond income replacement, life insurance serves several other purposes: paying off debts so survivors are not burdened, funding a child's education, covering final expenses, estate planning (providing liquidity to pay estate taxes), and business continuity (funding buy-sell agreements when a partner dies).\n\nThe principle of indemnity works differently in life insurance than in property insurance. A life insurance policy pays a stated death benefit -- a fixed face amount agreed at policy inception. This stated amount approach makes life insurance a valued policy rather than an indemnity policy.\n\nFor the exam: income replacement, debt payoff, final expenses, education funding, estate planning, and business continuation are all recognized purposes of life insurance.",
        "example": "A 35-year-old father earns $80,000/year with a $300,000 mortgage and two young children. A $1.5M life policy pays off the mortgage and replaces income for his family if he dies.",
        "memory_tip": "Life insurance solves the what-if-the-income-stops problem. Death ends the paycheck but not the bills." },
      { "slug": "lh-insurable-interest-life", "title": "Insurable Interest in Life Insurance", "sort_order": 2, "estimated_minutes": 7,
        "summary": "Insurable interest must exist at the time of application and requires a financial or personal stake in the insured's continued life.",
        "body": "Insurable interest means the policyowner would suffer a financial or significant personal loss if the insured died. Without it, the policy is an unenforceable wagering agreement.\n\nTiming matters: in life insurance, insurable interest must exist at the time of application -- not at the time of death. This differs from property insurance where insurable interest must exist at the time of loss.\n\nWho has insurable interest? You always have insurable interest in your own life. Spouses have insurable interest in each other. Parents have insurable interest in dependent children. Business partners have insurable interest in each other. Creditors have insurable interest in debtors up to the amount of the debt. Employers have insurable interest in key employees.\n\nWho does NOT have insurable interest? A person generally does not have insurable interest in a stranger. Stranger-originated life insurance (STOLI) is prohibited or strictly limited in most states because it creates a moral hazard.",
        "example": "A sole proprietor takes out a $2M policy on their business partner. The partner's death would cause the business financial harm -- clear insurable interest.",
        "memory_tip": "Insurable interest = you would suffer financially if they died. Life insurance: must exist at APPLICATION, not at death." },
      { "slug": "lh-life-insurance-contract", "title": "The Life Insurance Contract", "sort_order": 3, "estimated_minutes": 7,
        "summary": "Life insurance contracts require offer and acceptance, consideration, legal purpose, competent parties, and insurable interest.",
        "body": "A life insurance policy must meet all contract requirements: offer and acceptance, consideration, legal purpose, and competent parties. It also requires insurable interest.\n\nThe incontestability clause is critical. After two years in force, the insurer cannot contest the policy based on misrepresentations in the application -- even material ones. During the two-year period the insurer can investigate and rescind for material fraud. After two years the policy is incontestable.\n\nLife insurance contracts are unilateral (only the insurer makes an enforceable promise), conditional (insurer pays only if insured dies while policy is in force), and aleatory (exchange of values depends on an uncertain event).\n\nThe entire contract provision states that the policy and attached application constitute the complete agreement. Oral promises made by agents that are not in the written contract are not enforceable.",
        "example": "An insured fails to disclose a prior heart condition. He dies 18 months after issue. The insurer discovers the misrepresentation and rescinds -- the 2-year contestability period had not expired.",
        "memory_tip": "Incontestability = after 2 years, insurer cannot contest misrepresentations. Two years to investigate, then locked in." },
      { "slug": "lh-policy-parties", "title": "Parties to a Life Insurance Policy", "sort_order": 4, "estimated_minutes": 7,
        "summary": "Four parties: the insurer, policyowner, insured, and beneficiary -- each with distinct rights.",
        "body": "The insurer is the company that issues the policy and promises to pay the death benefit.\n\nThe policyowner controls the contract -- pays premiums, names beneficiaries, takes loans, and can surrender the policy. The policyowner need not be the insured.\n\nThe insured is the person whose life is covered. Death of the insured triggers the death benefit.\n\nThe beneficiary receives the death benefit. A revocable beneficiary can be changed anytime without consent. An irrevocable beneficiary cannot be changed without their written consent -- they have a vested interest.\n\nContingent (secondary) beneficiaries receive the death benefit if the primary predeceases the insured. Without a contingent beneficiary, proceeds pass to the insured's estate.",
        "example": "A husband (policyowner and insured) names his wife as revocable primary beneficiary. He can change the beneficiary anytime without her consent.",
        "memory_tip": "Four parties: Insurer promises, Policyowner controls, Insured is covered, Beneficiary collects. Revocable = changeable anytime. Irrevocable = locked without their consent." },
      { "slug": "lh-underwriting-basics", "title": "Life Insurance Underwriting", "sort_order": 5, "estimated_minutes": 7,
        "summary": "Underwriting evaluates mortality risk and assigns applicants to premium classes: preferred, standard, substandard, or declined.",
        "body": "Underwriting evaluates applications to determine whether to accept the risk and at what price. Life insurance underwriters assess the probability of the insured dying during the policy period.\n\nInformation sources: the application, medical examination, attending physician statements, motor vehicle records, and inspection reports. For larger policies, blood tests and financial questionnaires may be required.\n\nRisk classifications: Preferred applicants have excellent health and get the lowest premiums. Standard applicants have average health. Substandard (rated) applicants have elevated risks and pay higher premiums or receive modified coverage. Declined applicants are risks the insurer will not cover at any price.\n\nMortality tables are the statistical foundation of pricing. Material misrepresentations on the application (those that would have affected the decision to issue or the premium charged) can void the policy during the two-year contestability period.",
        "example": "A 45-year-old smoker with high blood pressure is classified substandard and charged a table rating (extra premium) to reflect elevated mortality risk.",
        "memory_tip": "Underwriting = assessing mortality risk. Preferred = lowest. Standard = average. Substandard = higher premium. Declined = no coverage at any price." },
    ],
    "terms": [
      {"term": "Death Benefit", "plain": "The amount paid to the beneficiary when the insured dies", "exam": "The face amount specified in a life insurance policy, paid to the named beneficiary upon the insured's death.", "example": "A $500,000 death benefit is paid to the surviving spouse when the insured dies."},
      {"term": "Policyowner", "plain": "The person who owns and controls the life insurance policy", "exam": "The person or entity that owns a life insurance contract, pays premiums, and has the right to exercise all policy options.", "example": "The policyowner changes the beneficiary designation after a divorce."},
      {"term": "Insured", "plain": "The person whose life is covered by the policy", "exam": "The person on whose life the insurance policy is written; the death of the insured triggers payment of the death benefit.", "example": "The 40-year-old executive is the insured whose death triggers the $2M payout."},
      {"term": "Beneficiary", "plain": "The person who receives the death benefit", "exam": "The person or entity designated to receive the life insurance death benefit upon the insured's death.", "example": "The named beneficiary receives $250,000 from the life insurance policy."},
      {"term": "Insurable Interest", "plain": "A financial stake in someone's continued life that justifies buying insurance on them", "exam": "A financial or personal relationship causing the policyowner to suffer loss upon the insured's death; must exist at the time of application in life insurance.", "example": "A business partner has insurable interest because the partner's death would harm the business financially."},
      {"term": "Incontestability Clause", "plain": "After 2 years the insurer cannot void the policy for misrepresentation", "exam": "A provision stating that after the policy has been in force for two years, the insurer cannot contest its validity based on misrepresentations in the application.", "example": "After the two-year period expires, the insurer must pay the death benefit even if the application had misrepresentations."},
      {"term": "Revocable Beneficiary", "plain": "A beneficiary the policyowner can change at any time", "exam": "A beneficiary designation that the policyowner can change, remove, or modify at any time without the beneficiary's consent.", "example": "The policyowner changes the revocable beneficiary from ex-spouse to children after a divorce."},
      {"term": "Irrevocable Beneficiary", "plain": "A beneficiary that cannot be changed without their written consent", "exam": "A beneficiary designation that cannot be changed without the written consent of the named beneficiary; the beneficiary has a vested interest.", "example": "The mortgage lender named as irrevocable beneficiary cannot be removed without the lender's consent."},
      {"term": "Substandard Risk", "plain": "An applicant with higher-than-average mortality risk who pays higher premiums", "exam": "An insurance applicant whose health or lifestyle presents higher-than-average mortality risk; may be offered coverage at a higher premium or with modified benefits.", "example": "A smoker with diabetes is classified substandard and charged a table rating."},
      {"term": "Mortality Table", "plain": "Statistical table of death rates by age used to price life insurance", "exam": "A statistical table showing the probability of death at each age, used by actuaries to calculate life insurance premiums and reserves.", "example": "Mortality tables show a 65-year-old has a much higher annual death probability than a 25-year-old."},
    ],
    "questions": [
      ("Insurable interest in a life insurance policy must exist:",
       "multiple_choice", "standard",
       "In life insurance, insurable interest must exist at the time of application -- not at the time of death. Once issued, the policy remains valid even if the insurable interest later disappears.",
       [("At the time of the application", True, "Correct. Life insurance insurable interest is required at application, not at the insured's death."),
        ("At the time of the insured's death", False, "This is the rule for property insurance, not life insurance."),
        ("At both the time of application and the time of death", False, "Insurable interest only needs to exist at application in life insurance."),
        ("Only if the policy is for more than $100,000", False, "Insurable interest is required for all life insurance policies regardless of face amount.")]),
      ("The incontestability clause in a life insurance policy means the insurer:",
       "multiple_choice", "standard",
       "After two years the insurer cannot challenge the validity of the policy based on misrepresentations in the application.",
       [("Cannot contest the policy after it has been in force for two years", True, "Correct. After the two-year contestability period the policy cannot be voided for misrepresentation."),
        ("Must pay any death claim without investigation", False, "The insurer can still investigate claims; it simply cannot void the policy for application misrepresentations after two years."),
        ("Cannot raise premiums after the policy has been issued", False, "Premium guarantees are separate from the incontestability clause."),
        ("Must refund premiums if the insured dies within the first year", False, "This describes the suicide exclusion provision, not incontestability.")]),
      ("Which party to a life insurance contract has the right to change the beneficiary?",
       "multiple_choice", "standard",
       "The policyowner controls the contract, including the right to change a revocable beneficiary designation at any time without the beneficiary's consent.",
       [("The policyowner", True, "Correct. The policyowner has full control over the policy including beneficiary changes."),
        ("The insured", False, "The insured controls the policy only if they are also the policyowner."),
        ("The revocable beneficiary", False, "A revocable beneficiary has no vested right and no policy control."),
        ("The insurer", False, "The insurer cannot unilaterally change beneficiary designations.")]),
      ("An insured misrepresents a material fact on the application. The insurer discovers this 18 months after issue. The insurer will most likely:",
       "scenario", "standard",
       "The contestability period is two years. At 18 months the policy is still contestable, so the insurer may void the policy based on the material misrepresentation.",
       [("Rescind the policy because it is within the two-year contestability period", True, "Correct. Material misrepresentation within the contestability period allows the insurer to void the policy."),
        ("Be required to pay the death benefit because the insured paid premiums", False, "Payment of premiums does not waive the insurer's right to contest within the contestability period."),
        ("Have no recourse because the policy was issued", False, "The insurer retains contestability rights for two years after issue."),
        ("Reduce the death benefit proportionally", False, "The remedy for material misrepresentation is rescission, not benefit reduction.")]),
      ("An irrevocable beneficiary designation means:",
       "multiple_choice", "standard",
       "An irrevocable beneficiary has a vested interest. The policyowner cannot change the designation or take a policy loan without the irrevocable beneficiary's written consent.",
       [("The designation cannot be changed without the beneficiary's written consent", True, "Correct. Irrevocable beneficiaries have a vested interest requiring their consent for policy changes."),
        ("The beneficiary will automatically receive the death benefit regardless of any conditions", False, "The irrevocability refers to the designation, not to unconditional payment."),
        ("The beneficiary cannot be changed under any circumstances", False, "An irrevocable designation CAN be changed with the beneficiary's written consent."),
        ("The policyowner cannot make any changes to the policy", False, "Only changes affecting the irrevocable beneficiary require their consent.")]),
    ],
  },
  {
    "slug": "term-life-insurance",
    "title": "Term Life Insurance",
    "description": "Pure death protection for a specified period with no cash value accumulation.",
    "sort_order": 102,
    "lessons": [
      { "slug": "lh-term-life-overview", "title": "Term Life Insurance Overview", "sort_order": 1, "estimated_minutes": 7,
        "summary": "Term life provides pure death protection for a specified period with no cash value.",
        "body": "Term life insurance is the simplest and most affordable form of life insurance. If the insured dies during the term, the beneficiary receives the face amount. If the insured survives the term, coverage expires with no payment and no accumulated value.\n\nLevel term keeps both the premium and death benefit constant for the entire term. Annual renewable term (ART) renews each year at increasing premiums reflecting advancing age. Decreasing term reduces the death benefit over the term while keeping premiums level -- often used to match a declining mortgage balance.\n\nRenewability allows renewal at term end without evidence of insurability. Premiums increase at renewal to reflect the older age. Convertibility allows conversion to permanent insurance without evidence of insurability -- critical if health deteriorates during the term.\n\nFor the exam: term = no cash value. Three types: level, ART, decreasing. Renewable = renew without health exam. Convertible = switch to permanent without health exam.",
        "example": "A 35-year-old buys a 20-year level term policy for $500,000. If she dies before 55 the family receives $500,000. If she survives to 55 the policy expires with nothing returned.",
        "memory_tip": "Term = temporary + no cash value. Level = same premium and benefit. Decreasing = declining benefit. Renewable = renew without exam. Convertible = switch without exam." },
      { "slug": "lh-term-provisions", "title": "Term Policy Provisions and Riders", "sort_order": 2, "estimated_minutes": 7,
        "summary": "Renewability, convertibility, waiver of premium, and accidental death benefit are the key term policy features.",
        "body": "The renewability provision allows renewal without evidence of insurability. The insurer must renew regardless of health changes. Premiums increase at each renewal to reflect the insured's advancing age.\n\nThe convertibility provision allows conversion to permanent insurance without evidence of insurability, typically within a specified window or before a stated age. The permanent policy is issued at the attained age premium.\n\nThe waiver of premium rider waives all future premiums if the insured becomes totally disabled -- one of the most valuable riders since disability is statistically more likely than premature death for working-age adults.\n\nThe accidental death benefit (double indemnity) rider pays an additional death benefit equal to the face amount if death results from an accident. The total payout doubles.\n\nFor the exam: renewable = keep coverage without health exam; convertible = switch to permanent without health exam; waiver of premium = disability stops premiums; double indemnity = accidental death pays double.",
        "example": "A policyholder diagnosed with cancer during his term is protected by renewability -- when the term expires he can renew without a health exam despite his diagnosis.",
        "memory_tip": "Renewable = keep term, no health exam. Convertible = go permanent, no health exam. Waiver of premium = disability stops payments. Double indemnity = accident doubles the payout." },
    ],
    "terms": [
      {"term": "Level Term", "plain": "Term where premium and death benefit stay constant throughout", "exam": "A term life insurance policy in which both the death benefit and the premium remain constant for the entire policy term.", "example": "A 20-year level term maintains the same $500,000 death benefit and $35/month premium for all 20 years."},
      {"term": "Decreasing Term", "plain": "Term insurance where the death benefit declines over time", "exam": "A term life policy in which the death benefit decreases over the policy period, typically matching a declining debt obligation like a mortgage.", "example": "A 30-year decreasing term policy starts at $300,000 and declines to zero as the mortgage is paid off."},
      {"term": "Convertibility", "plain": "Right to switch a term policy to permanent insurance without a health exam", "exam": "A term policy provision giving the policyowner the right to convert to permanent insurance without evidence of insurability, typically before a stated age or within a specified period.", "example": "After developing diabetes, the insured converts his term to whole life using convertibility -- no health exam required."},
      {"term": "Renewability", "plain": "Right to renew a term policy without proving good health", "exam": "A term policy provision giving the policyowner the right to renew coverage at term end without evidence of insurability; premiums increase at renewal to reflect the older age.", "example": "After being diagnosed with a chronic illness, the insured renews her 10-year term -- the renewability provision requires acceptance."},
      {"term": "Waiver of Premium", "plain": "Rider waiving premium payments if the insured becomes totally disabled", "exam": "A life insurance rider that waives all premium payments while the insured is totally disabled; coverage remains in force during the disability.", "example": "After a disabling accident, the waiver of premium rider keeps the $1M policy in force with no premium payments."},
      {"term": "Accidental Death Benefit", "plain": "Rider paying an extra death benefit if death results from an accident", "exam": "A life insurance rider that pays an additional death benefit equal to the face amount if the insured dies from an accident; also called double indemnity.", "example": "A $500,000 policy with accidental death benefit pays $1,000,000 if the insured dies in a car accident."},
    ],
    "questions": [
      ("A level term life insurance policy differs from an annual renewable term policy in that:",
       "multiple_choice", "standard",
       "Level term keeps the premium constant throughout the term. Annual renewable term renews each year at an increasing premium to reflect advancing age.",
       [("Level term maintains the same premium for the entire policy period", True, "Correct. Level term has a fixed premium; ART premiums increase each year."),
        ("Level term provides a higher death benefit than annual renewable term", False, "The death benefit structure is not what distinguishes these -- it is the premium structure."),
        ("Level term can be converted to permanent insurance but ART cannot", False, "Either type can include a convertibility provision."),
        ("Level term has no cash value while ART accumulates cash value", False, "Neither level term nor ART accumulates cash value.")]),
      ("The primary advantage of the convertibility provision in a term policy is:",
       "multiple_choice", "standard",
       "Convertibility allows conversion to permanent insurance without evidence of insurability -- most valuable if the insured's health deteriorates during the term.",
       [("It allows conversion to permanent insurance without evidence of insurability", True, "Correct. Convertibility protects against becoming uninsurable by allowing conversion without a health exam."),
        ("It reduces the premium during the conversion period", False, "Conversion involves paying the permanent policy premium at attained age, which is higher."),
        ("It guarantees the same face amount in the converted policy", False, "The converted amount may differ; the key feature is no evidence of insurability."),
        ("It extends the term period without a new application", False, "Extension without a health exam is the renewability provision, not convertibility.")]),
      ("A policyowner has a $500,000 policy with a waiver of premium rider. If the insured becomes totally disabled:",
       "scenario", "standard",
       "The waiver of premium rider waives all premium payments during total disability while keeping the policy in force.",
       [("All future premiums are waived and the policy remains in force", True, "Correct. The waiver of premium rider maintains coverage without premium payments during total disability."),
        ("The policy face amount is reduced to reflect the waived premiums", False, "The face amount is not reduced -- only the premium obligation is waived."),
        ("The policy converts to paid-up term insurance equal to accumulated cash value", False, "This describes a non-forfeiture option, not the waiver of premium rider."),
        ("Premiums are waived for a maximum of two years", False, "The waiver continues throughout the period of total disability, not just two years.")]),
      ("Decreasing term insurance is most often used to:",
       "multiple_choice", "standard",
       "Decreasing term is designed to match a declining obligation. As the insured pays down a mortgage, the death benefit decreases to match the remaining balance.",
       [("Match a declining debt obligation such as a mortgage", True, "Correct. Decreasing term is commonly used for mortgage protection because the death benefit declines as the mortgage balance declines."),
        ("Provide increasing protection as the insured's income grows", False, "This describes an increasing term rider, not decreasing term."),
        ("Replace income during retirement when expenses are lower", False, "Retirement income replacement is addressed with annuities or permanent life insurance."),
        ("Provide temporary coverage until a permanent policy is approved", False, "Temporary coverage pending approval uses a binder or conditional receipt.")]),
      ("An accidental death benefit rider on a life insurance policy is also known as:",
       "multiple_choice", "standard",
       "The accidental death benefit rider pays an additional death benefit equal to the face amount if death results from an accident. Because the total payout doubles, it is called double indemnity.",
       [("Double indemnity", True, "Correct. Accidental death benefit = double indemnity because the total payout doubles on accidental death."),
        ("Waiver of premium", False, "Waiver of premium is a different rider relating to disability, not accidental death."),
        ("Guaranteed insurability", False, "Guaranteed insurability allows future coverage purchases without evidence of insurability."),
        ("Term rider", False, "A term rider adds term coverage to a permanent policy.")]),
    ],
  },
  {
    "slug": "whole-life-insurance",
    "title": "Whole Life Insurance",
    "description": "Permanent life insurance with lifelong coverage, level premiums, and guaranteed cash value.",
    "sort_order": 103,
    "lessons": [
      { "slug": "lh-whole-life-overview", "title": "Whole Life Insurance Overview", "sort_order": 1, "estimated_minutes": 8,
        "summary": "Whole life provides permanent death protection with three guarantees: death benefit for life, level premiums, and cash value growth.",
        "body": "Whole life insurance provides lifelong death protection, accumulates a guaranteed cash value, and keeps premiums level. Three guarantees distinguish it from term: guaranteed death benefit (paid whenever the insured dies), guaranteed cash value growth (savings component at a guaranteed minimum rate), and guaranteed level premiums (never increase).\n\nThe cash value is the living benefit. Each premium consists of a mortality charge and a savings component. Cash value grows tax-deferred. The policyowner can access it through policy loans, partial surrenders, or full surrender.\n\nWhole life costs more than term for the same face amount because it covers the entire lifetime and because part of each premium funds the savings component.\n\nFor the exam: three whole life guarantees -- death benefit for LIFE, LEVEL premiums forever, cash VALUE accumulates. Term has none of these three.",
        "example": "A 30-year-old buys a $500,000 whole life policy. By age 65 the policy has $180,000 in cash value. She can borrow against it or leave it in force knowing her beneficiaries receive $500,000 when she dies.",
        "memory_tip": "Whole life = 3 guarantees: death benefit for life, level premiums forever, cash value accumulates. Term has NONE of these." },
      { "slug": "lh-cash-value", "title": "Cash Value and Policy Loans", "sort_order": 2, "estimated_minutes": 7,
        "summary": "Cash value grows tax-deferred and can be accessed through policy loans without surrendering the policy.",
        "body": "Cash value grows tax-deferred -- interest credited is not taxed as it accumulates. This tax advantage distinguishes life insurance savings from most other vehicles.\n\nPolicy loans allow borrowing against cash value without surrendering the policy. There is no mandatory repayment schedule. If the insured dies with an outstanding loan, the death benefit is reduced by the loan balance. Policy loans are not taxable income.\n\nSurrender value is the amount received if the policy is cancelled. Surrender charges may apply in early years. The automatic premium loan (APL) provision automatically uses policy loans to pay overdue premiums, preventing inadvertent lapse.\n\nTax treatment: cash value grows tax-deferred. Loans are not taxable income. Withdrawals in excess of cost basis are taxable.",
        "example": "A policyowner has $80,000 in cash value and takes a $30,000 loan for a renovation. No repayment required. If the insured dies with the loan outstanding, the beneficiary receives face amount minus $30,000.",
        "memory_tip": "Cash value: grows TAX-DEFERRED. Loans: NOT taxable, no mandatory repayment. Die with a loan = death benefit REDUCED by loan balance." },
      { "slug": "lh-whole-life-types", "title": "Types of Whole Life Policies", "sort_order": 3, "estimated_minutes": 7,
        "summary": "Limited pay, single premium, survivorship, and endowment are the main whole life variations.",
        "body": "Straight (ordinary) life requires premium payments throughout the insured's lifetime at the lowest whole life premium.\n\nLimited pay whole life allows paying up the policy in fewer years: 10-pay, 20-pay, or paid-up at 65. After the payment period coverage continues for life with no more premiums due. Higher annual premiums but paid off sooner.\n\nSingle premium whole life (SPWL) is purchased with one lump sum. Immediately fully paid up. Subject to modified endowment contract (MEC) rules affecting the tax treatment of withdrawals and loans.\n\nJoint life covers two people. First-to-die pays when the first insured dies. Survivorship life (second-to-die) pays when the second insured dies -- used for estate planning.\n\nEndowment policies pay the face amount either at death or at a maturity date, whichever comes first. Fast cash value growth but expensive; largely replaced by modern UL products.",
        "example": "A 50-year-old buys a 10-pay whole life policy. She makes 10 annual payments and at 60 the policy is fully paid up -- $500,000 coverage continues for life with no further premiums.",
        "memory_tip": "Limited pay = fewer years paying, higher premiums, then paid up forever. Single premium = one payment, MEC rules apply. Survivorship = second-to-die (estate planning)." },
    ],
    "terms": [
      {"term": "Cash Value", "plain": "The savings component of permanent life insurance that grows over time", "exam": "The savings element of a permanent life insurance policy that accumulates on a tax-deferred basis; accessible through loans, withdrawals, or surrender.", "example": "After 20 years the whole life policy has accumulated $95,000 in cash value."},
      {"term": "Policy Loan", "plain": "Money borrowed against the cash value of a life insurance policy", "exam": "A loan against accumulated cash value; not taxable income, no mandatory repayment, reduces the death benefit if outstanding at death.", "example": "The policyowner takes a $25,000 policy loan for college tuition with no required repayment schedule."},
      {"term": "Surrender Value", "plain": "Cash received when a life insurance policy is cancelled", "exam": "The amount the policyowner receives upon cancelling a policy; equals cash value minus surrender charges and outstanding loans.", "example": "After surrendering her whole life policy the policyowner receives $42,000 after surrender charges."},
      {"term": "Limited Pay Whole Life", "plain": "Whole life where premiums are paid over a shorter period but coverage lasts for life", "exam": "A whole life policy in which premiums are paid for a specified period after which the policy is fully paid up and coverage continues for life.", "example": "A 10-pay whole life requires 10 annual payments; no more premiums due but $500,000 coverage continues for life."},
      {"term": "Survivorship Life", "plain": "Policy covering two people that pays when the second person dies", "exam": "A joint life policy insuring two lives and paying the death benefit upon the death of the second insured; also called second-to-die, commonly used for estate planning.", "example": "A survivorship life policy on a married couple pays $2M when the second spouse dies to cover estate taxes."},
      {"term": "Modified Endowment Contract (MEC)", "plain": "An overfunded life policy that loses some tax advantages on loans and withdrawals", "exam": "A life insurance policy that fails the seven-pay test by being overfunded; loans and withdrawals are taxable income and subject to a 10% penalty before age 59.5.", "example": "A single-premium whole life policy is automatically a MEC, making withdrawals taxable."},
    ],
    "questions": [
      ("Which of the following is NOT a guarantee of a standard whole life insurance policy?",
       "multiple_choice", "standard",
       "Whole life guarantees: a fixed death benefit for life, level premiums that never increase, and minimum cash value accumulation. Market-linked returns are not guaranteed -- that is a feature of indexed or variable products.",
       [("Returns tied to a stock market index", True, "Correct -- this is NOT a whole life guarantee. Market-linked returns belong to indexed or variable products."),
        ("Level premiums for the life of the policy", False, "Level premiums are one of the three whole life guarantees."),
        ("A death benefit for the insured's entire lifetime", False, "Lifetime death benefit is one of the three whole life guarantees."),
        ("Guaranteed minimum cash value accumulation", False, "Guaranteed cash value growth is one of the three whole life guarantees.")]),
      ("A policyowner takes a policy loan against the cash value of a whole life policy. The loan is:",
       "multiple_choice", "standard",
       "Policy loans are not taxable income. The policyowner is borrowing against their own asset. No repayment is required, but interest accrues. Outstanding loans reduce the death benefit.",
       [("Not taxable income and requires no mandatory repayment schedule", True, "Correct. Policy loans are non-taxable and have no mandatory repayment schedule."),
        ("Taxable income in the year received", False, "Policy loans are not taxable income."),
        ("Required to be repaid within five years or the policy lapses", False, "There is no mandatory repayment schedule for policy loans, though unpaid interest accrues."),
        ("Deductible as interest expense on the policyowner's tax return", False, "Interest on personal policy loans is generally not tax-deductible.")]),
      ("A 10-pay whole life policy differs from a straight (ordinary) life policy in that:",
       "multiple_choice", "standard",
       "Limited pay whole life compresses premium payments into a shorter period. After 10 payments the policy is fully paid up. Straight life requires premiums throughout the insured's lifetime.",
       [("Premiums are paid for only 10 years after which no further premiums are due", True, "Correct. A 10-pay policy is paid up after 10 payments; straight life requires lifetime payments."),
        ("The death benefit is lower than straight life with the same initial premium", False, "The death benefit can be the same; it is the premium payment structure that differs."),
        ("The policy has no cash value during the premium payment period", False, "Cash value accumulates in all whole life policies including limited pay."),
        ("The policy terminates after 10 years if the insured is still alive", False, "Limited pay whole life does not terminate -- it is fully paid up and coverage continues for life.")]),
      ("Survivorship life insurance (second-to-die) is most commonly used for:",
       "multiple_choice", "standard",
       "Survivorship life pays the death benefit when the second insured dies. Estate taxes are typically due after both spouses die, making it an efficient estate planning tool.",
       [("Estate planning to provide funds to pay estate taxes after both spouses die", True, "Correct. Survivorship life pays on the second death, coinciding with when estate taxes are due."),
        ("Income replacement when one spouse dies and leaves the other without support", False, "This need is addressed by a first-to-die joint policy or individual policies."),
        ("Business continuation when a key executive becomes disabled", False, "Business continuation uses key person insurance and buy-sell agreements."),
        ("Retirement income supplementation through policy loans", False, "Survivorship life is primarily an estate planning tool.")]),
      ("What happens to the cash value of a whole life policy when the insured dies?",
       "multiple_choice", "hard",
       "In standard whole life, the beneficiary receives the face amount -- not the face amount plus cash value. The accumulated cash value is absorbed into the insurer's reserve and used to fund the death benefit.",
       [("It is absorbed by the insurer; the beneficiary receives only the face amount", True, "Correct. The beneficiary receives the face amount; cash value is incorporated into the insurer's reserve."),
        ("It is paid to the beneficiary in addition to the face amount", False, "In standard whole life, cash value is not paid separately in addition to the face amount."),
        ("It is returned to the policyowner's estate", False, "Cash value does not pass separately to the estate in a standard whole life death claim."),
        ("It is used to pay outstanding loans before the beneficiary receives the remainder", False, "Outstanding loans reduce the death benefit paid, but this is not how cash value mechanics work at death.")]),
    ],
  },
  {
    "slug": "universal-variable-life",
    "title": "Universal and Variable Life Insurance",
    "description": "Flexible permanent life -- universal life offers adjustable premiums; variable life adds investment sub-accounts.",
    "sort_order": 104,
    "lessons": [
      { "slug": "lh-universal-life", "title": "Universal Life Insurance", "sort_order": 1, "estimated_minutes": 8,
        "summary": "Universal life separates the insurance and savings components, offering flexible premiums and adjustable death benefits.",
        "body": "Universal life (UL) unbundles the three components of whole life: the mortality charge, expense charge, and savings component. Flexibility is the defining feature.\n\nPremium flexibility: the policyowner can pay more or less than the target premium as long as cash value covers monthly deductions. In a good year overfund to build cash value faster; in a tight year underpay or skip. If cash value depletes and no premium is paid, the policy lapses.\n\nDeath benefit options: Option A (level) -- death benefit stays level while net amount at risk decreases as cash value grows. Option B (increasing) -- death benefit equals face amount plus cash value; total benefit grows as cash value grows.\n\nCash value earns current interest rates subject to a guaranteed minimum -- interest rate sensitive, not the fixed guaranteed growth of whole life.\n\nFor the exam: UL = flexible premiums + adjustable benefits + unbundled. Option A = level. Option B = increasing. Interest rate sensitive.",
        "example": "A UL policyowner pays $300/month normally, increases to $500 in a good income year, and pays only $150 in a tight year -- all within the same policy.",
        "memory_tip": "Universal = flexible and unbundled. Option A = level benefit. Option B = benefit grows with cash value. Interest rate sensitive -- not guaranteed growth." },
      { "slug": "lh-variable-life", "title": "Variable Life Insurance", "sort_order": 2, "estimated_minutes": 7,
        "summary": "Variable life invests cash value in sub-accounts; the policyowner bears investment risk and must hold a securities license to sell it.",
        "body": "Variable life allows cash value to be directed into sub-accounts that function like mutual funds. The policyowner bears all investment risk -- cash value can grow significantly or decrease with markets. No guaranteed minimum cash value.\n\nBecause variable life is a security, producers must hold both a life insurance license AND a FINRA securities registration (Series 6 or Series 7). This dual-licensing requirement is one of the most tested facts about variable products.\n\nVariable universal life (VUL) combines the flexibility of universal life (adjustable premiums and benefits) with the investment options of variable life. Most flexible and complex life product.\n\nFor the exam: variable products require Series 6 or 7 PLUS life license. Investment risk to policyowner. No guaranteed minimum cash value. VUL = universal flexibility + variable investments.",
        "example": "A variable life policyowner directs cash value into a stock sub-account. In a bull market it grows from $50,000 to $90,000. In a bear market it drops to $35,000. The policyowner bears both outcomes.",
        "memory_tip": "Variable = investment risk to policyowner. SECURITIES LICENSE required (Series 6 or 7) plus life license. No guaranteed cash value. VUL = variable + universal combined." },
    ],
    "terms": [
      {"term": "Universal Life", "plain": "Flexible permanent life insurance with adjustable premiums and death benefits", "exam": "A permanent life insurance policy that unbundles the mortality charge, expense charge, and cash value accumulation, offering flexible premiums and adjustable death benefits.", "example": "A UL policyowner increases the death benefit from $500,000 to $750,000 after a second child without buying a new policy."},
      {"term": "Variable Life", "plain": "Permanent life where cash value is invested in securities sub-accounts", "exam": "A permanent life policy in which cash value is invested in separate sub-accounts similar to mutual funds; investment risk rests with the policyowner.", "example": "The variable life policyowner allocates 60% to a stock sub-account and 40% to bonds."},
      {"term": "Variable Universal Life (VUL)", "plain": "Life insurance combining universal flexibility with variable investment options", "exam": "A permanent life policy combining flexible premiums and adjustable death benefits of universal life with the investment sub-accounts of variable life.", "example": "A VUL policyowner adjusts premiums quarterly and shifts between sub-accounts based on market conditions."},
      {"term": "Securities License", "plain": "FINRA registration required to sell variable life insurance and annuities", "exam": "A FINRA registration (Series 6 or Series 7) required in addition to a life insurance license to sell variable life insurance and variable annuities.", "example": "An agent must hold both a life license and a Series 6 before selling variable universal life."},
      {"term": "Death Benefit Option A", "plain": "UL option where death benefit stays level while cash value grows", "exam": "A universal life death benefit option in which the death benefit remains level; as cash value increases the net amount at risk decreases.", "example": "Under Option A a $500,000 UL policy pays $500,000 at death regardless of accumulated cash value."},
      {"term": "Death Benefit Option B", "plain": "UL option where death benefit increases as cash value grows", "exam": "A universal life death benefit option in which the death benefit equals the face amount plus accumulated cash value; total benefit grows with cash value.", "example": "Under Option B with $100,000 in cash value a $500,000 UL policy pays $600,000 at death."},
    ],
    "questions": [
      ("Under universal life insurance Death Benefit Option B, the death benefit:",
       "multiple_choice", "standard",
       "Under Option B the death benefit equals the face amount plus the accumulated cash value. As cash value grows, the total death benefit increases.",
       [("Equals the face amount plus the accumulated cash value", True, "Correct. Option B death benefit = face amount + cash value, increasing as cash value grows."),
        ("Remains level regardless of cash value accumulation", False, "This describes Option A, not Option B."),
        ("Decreases as cash value increases to keep net amount at risk constant", False, "This describes the mechanics of Option A from the insurer's perspective."),
        ("Is guaranteed and cannot be changed after issue", False, "Universal life death benefit options can typically be changed, subject to evidence of insurability for increases.")]),
      ("Which individual is required to hold a FINRA securities license in addition to a life insurance license?",
       "multiple_choice", "standard",
       "Variable life and variable annuities are classified as securities because investment risk rests with the policyowner. Selling them requires both a life insurance license AND a FINRA securities registration.",
       [("A producer who sells variable universal life insurance", True, "Correct. Variable products require both a life insurance license and a FINRA securities registration."),
        ("A producer who sells whole life insurance with a guaranteed 4% cash value return", False, "Guaranteed fixed return whole life is not a security; only a life insurance license is required."),
        ("A producer who sells universal life insurance", False, "Standard (non-variable) universal life requires only a life insurance license."),
        ("A producer who sells term life insurance with a guaranteed insurability rider", False, "Term life is not a security regardless of the attached riders.")]),
      ("The primary risk borne by the policyowner under a variable life insurance policy is:",
       "multiple_choice", "standard",
       "In variable life the policyowner directs cash value into investment sub-accounts. Unlike whole life or universal life, variable life has no guaranteed minimum cash value -- the policyowner bears all investment risk.",
       [("Investment risk -- the cash value may decrease due to poor market performance", True, "Correct. The policyowner bears all investment risk in variable life."),
        ("Mortality risk -- the insured may die before the policy accumulates sufficient cash value", False, "Mortality risk rests with the insurer, not the policyowner."),
        ("Interest rate risk -- premiums may increase if credited rates fall", False, "Interest rate risk is specific to universal life, not variable life."),
        ("Longevity risk -- the insured may outlive the policy benefit period", False, "Permanent life insurance has no expiration; longevity risk refers to annuities.")]),
      ("A universal life insurance policy will lapse if:",
       "multiple_choice", "standard",
       "Universal life uses cash value to pay monthly deductions. If cash value is depleted and no premium is paid, the policy lapses.",
       [("The cash value is insufficient to cover monthly deductions and no premium is paid", True, "Correct. UL lapses when cash value cannot cover the monthly mortality and expense charges."),
        ("The policyowner misses a single premium payment", False, "Universal life allows missed payments as long as cash value covers monthly charges."),
        ("The death benefit is increased without evidence of insurability", False, "Increasing the death benefit requires evidence of insurability but does not cause a lapse."),
        ("The policy is in force for more than 20 years without a premium increase", False, "Universal life can remain in force indefinitely if cash value is sufficient.")]),
      ("Which universal life death benefit option results in the highest premium cost?",
       "multiple_choice", "hard",
       "Option B costs more because the net amount at risk remains constant as cash value grows. Option A is less expensive because the net amount at risk decreases as cash value accumulates.",
       [("Option B (increasing death benefit)", True, "Correct. Option B maintains a constant net amount at risk, requiring higher mortality charges than Option A."),
        ("Option A (level death benefit)", False, "Option A is less expensive because the net amount at risk decreases as cash value grows."),
        ("Both options cost the same", False, "The options have different costs because of different net amounts at risk."),
        ("Option A for older insureds; Option B for younger insureds", False, "Option B generally costs more regardless of age because the insurer maintains a higher net amount at risk.")]),
    ],
  },
  {
    "slug": "life-policy-provisions",
    "title": "Life Insurance Policy Provisions",
    "description": "Standard provisions, settlement options, non-forfeiture options, and common exclusions in life insurance.",
    "sort_order": 105,
    "lessons": [
      { "slug": "lh-standard-provisions", "title": "Standard Life Insurance Provisions", "sort_order": 1, "estimated_minutes": 8,
        "summary": "Free look, grace period, reinstatement, and non-forfeiture options are mandatory standard provisions.",
        "body": "The free look period gives the new policyowner 10-30 days after delivery to review and return the policy for a full premium refund.\n\nThe grace period allows 31 days after a missed premium due date to pay without losing coverage. If the insured dies during the grace period the insurer pays the death benefit minus the unpaid premium.\n\nThe reinstatement provision allows a lapsed policy to be restored within 3-5 years by paying all back premiums with interest and providing evidence of insurability.\n\nThe misstatement of age provision adjusts the death benefit rather than voiding the policy if the insured's age was incorrectly stated -- the insurer pays what the actual premium would have purchased at the correct age.\n\nNon-forfeiture options protect the policyowner who stops paying premiums on a cash value policy. Three options: cash surrender value (take the cash), reduced paid-up insurance (smaller fully paid-up policy), or extended term insurance (original face amount as term insurance using cash value).\n\nFor the exam: free look, grace period, reinstatement, and non-forfeiture options are the most tested standard provisions.",
        "example": "A policyowner misses a premium on the 15th. The 31-day grace period keeps the policy in force until the 15th of next month. If the insured dies on the 25th the insurer pays the full death benefit minus the unpaid premium.",
        "memory_tip": "Free look = return for refund (10-30 days). Grace = 31 days to pay late. Reinstatement = back premiums + evidence of insurability. Non-forfeiture = 3 options: cash, reduced paid-up, extended term." },
      { "slug": "lh-settlement-options", "title": "Life Insurance Settlement Options", "sort_order": 2, "estimated_minutes": 7,
        "summary": "Settlement options determine how death benefit proceeds are paid -- lump sum, interest only, fixed period, fixed amount, or life income.",
        "body": "Lump sum is the default -- entire death benefit paid in one payment. Most common and most flexible.\n\nInterest only: insurer holds the proceeds and pays interest to the beneficiary. Principal paid out later.\n\nFixed period: proceeds paid in equal installments over a specified period (5, 10, or 20 years). Both principal and interest distributed over the period.\n\nFixed amount: beneficiary specifies an amount each period; payments continue until proceeds plus interest are exhausted.\n\nLife income options convert proceeds into a lifetime annuity: life only (stops at death, highest payment), life with period certain (guaranteed payments for a minimum period even if beneficiary dies early), joint and survivor (continues until both primary and secondary beneficiaries die).\n\nFor the exam: fixed period = duration is fixed. Fixed amount = payment amount is fixed. Life income = annuity for life.",
        "example": "A widow receives $500,000 and chooses life income with 20-year period certain. She receives monthly payments for life; if she dies within 20 years payments continue to her children for the remainder.",
        "memory_tip": "5 options: Lump sum, Interest only, Fixed period (time fixed), Fixed amount (dollar fixed), Life income (annuity). Period vs amount: period = time is fixed; amount = dollar is fixed." },
      { "slug": "lh-exclusions-riders", "title": "Life Insurance Exclusions and Riders", "sort_order": 3, "estimated_minutes": 7,
        "summary": "The suicide exclusion, guaranteed insurability, and payor benefit are the key exclusions and riders.",
        "body": "The suicide exclusion: if the insured commits suicide within 1-2 years of policy issue, the insurer returns premiums paid rather than the full death benefit. After the exclusion period, suicide is covered.\n\nWar exclusions were common in older policies but are rare today.\n\nHazardous activities exclusions may apply for high-risk occupations or hobbies.\n\nKey riders: waiver of premium (waives premiums during total disability), accidental death benefit (double indemnity), guaranteed insurability rider (future purchase rights without evidence), term rider (adds term coverage to a permanent policy).\n\nThe payor benefit rider waives premiums if the policyowner (typically a parent) becomes disabled or dies before the insured child reaches a specified age -- important for policies on children.\n\nFor the exam: suicide exclusion = return of premium within 1-2 years, full benefit after. Guaranteed insurability = buy more without health exam.",
        "example": "A policy has a 2-year suicide exclusion. The insured commits suicide 15 months after issue. The insurer returns premiums paid rather than the $300,000 death benefit.",
        "memory_tip": "Suicide exclusion = return premiums within 1-2 years, full benefit after. Guaranteed insurability = buy more later without health exam. Payor benefit = protects children's policies if parent dies." },
    ],
    "terms": [
      {"term": "Free Look Period", "plain": "Window after receiving a new policy to return it for a full refund", "exam": "A mandatory provision giving a new policyowner a specified period (typically 10-30 days) after delivery to review and return the policy for a full premium refund.", "example": "The policyowner returns her new whole life policy within the 10-day free look period after deciding the premium is too expensive."},
      {"term": "Grace Period", "plain": "Extra time after a missed premium to pay without losing coverage", "exam": "A mandatory policy provision giving the policyowner 31 days after a premium due date to pay without coverage lapsing.", "example": "The insured dies 20 days after missing a premium. The grace period keeps the policy in force so the beneficiary receives the death benefit minus the unpaid premium."},
      {"term": "Non-Forfeiture Options", "plain": "Rights protecting cash value when the policyowner stops paying premiums", "exam": "Mandatory provisions protecting accumulated cash value if premiums are discontinued; options include cash surrender value, reduced paid-up insurance, and extended term insurance.", "example": "The policyowner who can no longer afford premiums chooses reduced paid-up, receiving a smaller fully paid-up policy."},
      {"term": "Suicide Exclusion", "plain": "Provision limiting benefits if the insured commits suicide early in the policy", "exam": "A life insurance provision returning only premiums paid if the insured commits suicide within a specified period (typically 1-2 years) after issue; full benefit paid after the exclusion period.", "example": "A policy with a 1-year suicide exclusion pays only return of premiums if suicide occurs 6 months after issue."},
      {"term": "Guaranteed Insurability Rider", "plain": "Rider allowing future purchase of additional coverage without proving good health", "exam": "A rider giving the policyowner the right to purchase additional coverage at specified future dates without evidence of insurability.", "example": "The policyowner increases coverage by $100,000 at age 30 using the guaranteed insurability rider -- no health exam required."},
      {"term": "Payor Benefit Rider", "plain": "Rider waiving premiums on a child's policy if the parent dies or becomes disabled", "exam": "A rider on a juvenile life insurance policy that waives premiums if the policyowner (typically a parent) dies or becomes totally disabled before the insured child reaches a specified age.", "example": "After the father who owns his child's life policy becomes disabled, the payor benefit rider waives all premiums until the child turns 21."},
    ],
    "questions": [
      ("A policyowner stops paying premiums on a whole life policy with $45,000 in cash value. Under non-forfeiture options the policyowner could:",
       "scenario", "standard",
       "Non-forfeiture options protect the policyowner's cash value. Three options: cash surrender, reduced paid-up insurance, or extended term insurance.",
       [("Receive $45,000 in cash, take a smaller paid-up policy, or receive term coverage for the original face amount", True, "Correct. The three non-forfeiture options are cash surrender, reduced paid-up, and extended term insurance."),
        ("Lose all cash value since premiums were not paid", False, "Non-forfeiture provisions prevent the loss of cash value; the policyowner always has options."),
        ("Continue coverage indefinitely without paying premiums", False, "Coverage continues through non-forfeiture options but is not unlimited without using cash value."),
        ("Receive the cash value plus unpaid dividends only from a mutual company", False, "Non-forfeiture options apply to all whole life policies, not just mutual company policies.")]),
      ("The free look provision in a life insurance policy:",
       "multiple_choice", "standard",
       "The free look period gives the policyowner a specified period (typically 10-30 days after delivery) to review and return the policy for a full refund of premiums paid.",
       [("Allows the policyowner to return the policy for a full premium refund within a specified period", True, "Correct. The free look provision gives the policyowner the right to rescind for a full refund within the designated period."),
        ("Allows the insurer to review and cancel the policy within the first 30 days", False, "The free look period benefits the policyowner, not the insurer."),
        ("Waives the first year's premium as a promotional offer", False, "Free look is a mandatory consumer protection provision, not a promotional waiver."),
        ("Permits the policyowner to request changes within 30 days", False, "The free look allows return for refund; changes are addressed through endorsements.")]),
      ("Under the fixed amount settlement option, the beneficiary:",
       "multiple_choice", "standard",
       "Under the fixed amount option the beneficiary specifies a payment amount each period. Payments continue until proceeds plus interest are exhausted. Duration depends on total proceeds and chosen amount.",
       [("Specifies a payment amount and receives that amount until the proceeds are exhausted", True, "Correct. Fixed amount = dollar amount is fixed; duration varies based on total proceeds and interest."),
        ("Receives equal installments over a fixed period specified in advance", False, "This describes the fixed period option, not the fixed amount option."),
        ("Receives interest only, with the principal held by the insurer indefinitely", False, "This describes the interest-only option."),
        ("Receives income for life regardless of total proceeds available", False, "This describes a life income annuity option.")]),
      ("A life insurance policy lapses. The policyowner wishes to reinstate it. Requirements typically include:",
       "multiple_choice", "standard",
       "Reinstatement requires payment of all overdue premiums with interest and evidence of insurability. The reinstatement period is typically 3-5 years from lapse.",
       [("Payment of all back premiums with interest and evidence of insurability", True, "Correct. Reinstatement requires back premiums with interest plus proof of continued insurability."),
        ("Payment of a reinstatement fee only, with no evidence of insurability", False, "Evidence of insurability is required for reinstatement in most cases."),
        ("A new application as if applying for the first time with current age rates", False, "Reinstatement restores the original policy terms; it is not a new application."),
        ("Payment of only the most recent overdue premium to restore coverage", False, "All overdue premiums plus interest must be paid, not just the most recent.")]),
      ("The misstatement of age provision in a life insurance policy:",
       "multiple_choice", "standard",
       "Rather than voiding the policy for a misstatement of age, the provision adjusts the death benefit to what the actual premium paid would have purchased at the correct age.",
       [("Adjusts the death benefit to what the premium paid would have purchased at the correct age", True, "Correct. The misstatement of age provision adjusts the benefit rather than voiding the policy."),
        ("Voids the policy if the insured's age was misstated by more than two years", False, "The provision adjusts benefits rather than voiding the policy."),
        ("Requires the policyowner to pay additional premiums to account for the correct age", False, "The insurer adjusts the benefit; it does not demand back premiums."),
        ("Only applies if the insured is younger than stated, since a higher age means higher premiums", False, "The provision applies whether the insured is older or younger than stated.")]),
    ],
  },
]


def seed_part1():
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
        print(f"\n=== Part 1 complete: {mod_count} modules, {lesson_count} lessons, {term_count} terms, {q_count} questions ===")
    finally:
        db.close()


if __name__ == "__main__":
    seed_part1()
