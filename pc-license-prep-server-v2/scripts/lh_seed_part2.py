#!/usr/bin/env python3
"""
lh_seed_part2.py  —  Life & Health course, modules 6-10
Modules: Annuities, Health Insurance Basics, Health Policy Provisions,
         Individual Health Policies, Group Health Insurance
Run from pc-license-prep-server-v2/:
    .venv/bin/python3 scripts/lh_seed_part2.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import select, text
from app.database import SessionLocal, create_all
from app.models import Module, Lesson, Term, Question, AnswerChoice

MODULES = [
  {
    "slug": "annuities",
    "title": "Annuities",
    "description": "Insurance products providing guaranteed income -- the opposite of life insurance, protecting against outliving your money.",
    "sort_order": 106,
    "lessons": [
      { "slug": "lh-annuity-basics", "title": "Annuity Basics", "sort_order": 1, "estimated_minutes": 7,
        "summary": "Annuities provide guaranteed income -- life insurance protects against dying too soon; annuities protect against living too long.",
        "body": "An annuity is a contract where the policyholder pays a premium and the insurer promises periodic income payments beginning immediately or at a future date.\n\nLife insurance protects against dying too soon. Annuities protect against living too long -- outliving retirement savings. Together they address the two sides of longevity risk.\n\nTwo phases: accumulation phase (contract grows tax-deferred) and distribution phase (annuitization -- insurer begins income payments).\n\nDeferred annuities grow before distributions begin. Immediate annuities (SPIAs) begin paying immediately after a single premium -- used by retirees converting a lump sum into guaranteed income.\n\nTax treatment: earnings grow tax-deferred. Withdrawals are taxed as ordinary income to the extent of earnings (cost basis returned tax-free). 10% penalty on withdrawals before age 59.5.\n\nFor the exam: deferred = grow first, pay later. Immediate = pay right away. Tax-deferred growth, ordinary income on withdrawals, 10% penalty before 59.5.",
        "example": "A 65-year-old invests $300,000 in an immediate annuity. The insurer pays $1,500/month for the rest of his life regardless of how long he lives.",
        "memory_tip": "Life insurance = too soon (death). Annuity = too long (outliving money). Deferred = grow then pay. Immediate = pay now. Penalty before 59.5." },
      { "slug": "lh-annuity-types", "title": "Types of Annuities", "sort_order": 2, "estimated_minutes": 8,
        "summary": "Fixed, variable, and indexed annuities differ in how interest is credited and who bears investment risk.",
        "body": "Fixed annuities credit interest at a guaranteed minimum rate set by the insurer. Insurer bears all investment risk. Most conservative option.\n\nVariable annuities allow investment in sub-accounts like mutual funds. Account value fluctuates with markets. Contract owner bears investment risk. Requires insurance license AND FINRA securities license (Series 6 or Series 7).\n\nIndexed annuities (equity-indexed) credit interest based on a market index (like the S&P 500) subject to a cap (maximum credit) and floor (minimum, typically 0%). Participates in market gains up to the cap; protected from losses below the floor.\n\nAnnuitization options: life only (highest payment, stops at death), life with period certain (guaranteed minimum payment period), joint and survivor (continues until both annuitants die), fixed period (specified period regardless of survival).\n\nFor the exam: fixed = insurer's risk, guaranteed rate. Variable = owner's risk, securities license required. Indexed = cap and floor.",
        "example": "A 60-year-old splits retirement savings: $200,000 into a fixed annuity (safety) and $150,000 into a variable annuity (growth potential).",
        "memory_tip": "Fixed = safe, insurer's risk. Variable = market, your risk, needs securities license. Indexed = middle ground, cap and floor. Life only = highest payment, no guarantee." },
    ],
    "terms": [
      {"term": "Annuity", "plain": "Insurance contract providing guaranteed periodic income payments", "exam": "An insurance contract in which the insurer promises periodic income payments in exchange for a lump sum or series of premiums; protects against outliving retirement savings.", "example": "A retiree purchases an annuity paying $2,000/month for life regardless of how long she lives."},
      {"term": "Accumulation Phase", "plain": "The growth period of an annuity before income payments begin", "exam": "The period during which an annuity contract grows through premium payments and tax-deferred interest accumulation before annuitization.", "example": "During the 20-year accumulation phase the deferred annuity grows from $50,000 to $135,000."},
      {"term": "Immediate Annuity", "plain": "An annuity beginning income payments right after a single premium", "exam": "A single-premium annuity that begins making income payments within one payment period after the premium is paid.", "example": "A 70-year-old invests $400,000 in an immediate annuity and receives the first payment 30 days later."},
      {"term": "Fixed Annuity", "plain": "Annuity with guaranteed minimum interest; insurer bears investment risk", "exam": "An annuity that credits interest at a guaranteed minimum rate; the insurer bears all investment risk and the value cannot decrease due to market performance.", "example": "A fixed annuity guarantees 3.5% annual interest regardless of market performance."},
      {"term": "Variable Annuity", "plain": "Annuity where value is invested in sub-accounts and fluctuates with markets", "exam": "An annuity in which the accumulation value is invested in sub-accounts; the contract owner bears investment risk and value fluctuates with markets; requires a securities license to sell.", "example": "A variable annuity invested in stock sub-accounts grew 18% one year and lost 12% the next."},
      {"term": "Life Annuity with Period Certain", "plain": "Annuity paying income for life but guaranteeing a minimum payment period", "exam": "An annuity payout option paying income for the annuitant's lifetime but guaranteeing payments for a minimum period even if the annuitant dies early.", "example": "A life annuity with 10-year period certain continues paying children for the remaining period if the annuitant dies after 3 years."},
    ],
    "questions": [
      ("An annuity differs from life insurance in that an annuity primarily protects against:",
       "multiple_choice", "standard",
       "Life insurance protects against dying too soon. Annuities protect against living too long -- outliving retirement savings. This is the fundamental distinction between the two products.",
       [("Living too long and outliving retirement savings", True, "Correct. Annuities address longevity risk -- the financial risk of outliving one's assets."),
        ("Dying prematurely and leaving dependents without income", False, "This is what life insurance protects against, not annuities."),
        ("Medical expenses during a serious illness", False, "Medical expense protection is provided by health insurance."),
        ("Property damage and liability claims", False, "These are P&C insurance exposures, unrelated to annuities.")]),
      ("The accumulation phase of a deferred annuity:",
       "multiple_choice", "standard",
       "During the accumulation phase the contract value grows tax-deferred. No taxes are due on earnings until withdrawals are taken.",
       [("Allows earnings to grow on a tax-deferred basis", True, "Correct. Tax-deferred growth during accumulation is a primary annuity advantage."),
        ("Requires distributions to begin within one year of purchase", False, "Deferred annuities may accumulate for many years before distributions are required."),
        ("Provides a guaranteed death benefit to the beneficiary", False, "The accumulation phase relates to growth, not death benefits."),
        ("Is taxed at capital gains rates when withdrawals are taken", False, "Annuity withdrawals are taxed as ordinary income, not capital gains.")]),
      ("A variable annuity differs from a fixed annuity in that:",
       "multiple_choice", "standard",
       "In a variable annuity the contract owner bears investment risk and the value may decrease. In a fixed annuity the insurer bears investment risk and guarantees a minimum rate.",
       [("The contract owner bears investment risk and the account value may decrease", True, "Correct. Variable annuity owners bear investment risk; fixed annuity insurers bear the risk."),
        ("The insurer guarantees a fixed minimum return regardless of market performance", False, "This describes a fixed annuity; variable annuity values fluctuate with markets."),
        ("Variable annuity premiums are tax-deductible", False, "Neither fixed nor variable annuity premiums are generally tax-deductible."),
        ("Variable annuities cannot be annuitized into a lifetime income stream", False, "Variable annuities can be annuitized just like fixed annuities.")]),
      ("Under the life income with period certain annuity payout option:",
       "multiple_choice", "standard",
       "Life income with period certain pays for the annuitant's lifetime AND guarantees a minimum payment period. If the annuitant dies before the period expires, payments continue to the named beneficiary.",
       [("Payments continue for the annuitant's lifetime and are guaranteed for a minimum period", True, "Correct. Period certain guarantees payments for a minimum time even if the annuitant dies early."),
        ("Payments continue only for the specified period regardless of whether the annuitant is alive", False, "This describes a fixed period annuity, not life income with period certain."),
        ("The annuitant receives the highest possible monthly payment of any payout option", False, "Life only (no period certain) provides the highest monthly payment."),
        ("Payments cease immediately upon the annuitant's death with no further benefits", False, "This describes a life-only payout option, not life with period certain.")]),
      ("A withdrawal from a non-qualified deferred annuity before age 59.5 is subject to:",
       "multiple_choice", "standard",
       "Non-qualified annuity withdrawals are taxed as ordinary income on the earnings portion. Withdrawals before age 59.5 also incur a 10% IRS penalty.",
       [("Ordinary income tax plus a 10% IRS early withdrawal penalty", True, "Correct. Pre-59.5 annuity withdrawals are subject to income tax on earnings plus a 10% penalty."),
        ("Capital gains tax at the preferential 15% or 20% rate", False, "Annuity withdrawals are taxed as ordinary income, not capital gains."),
        ("No tax since annuities receive special tax-exempt treatment", False, "Annuities are tax-deferred, not tax-exempt -- withdrawals are taxable."),
        ("A 10% penalty only, with no income tax owed", False, "Both income tax and the 10% penalty apply to pre-59.5 withdrawals.")]),
    ],
  },
  {
    "slug": "health-insurance-basics",
    "title": "Health Insurance Basics",
    "description": "Fundamental health insurance concepts -- coverage types, cost-sharing, and managed care.",
    "sort_order": 107,
    "lessons": [
      { "slug": "lh-health-insurance-overview", "title": "Health Insurance Overview", "sort_order": 1, "estimated_minutes": 8,
        "summary": "Health insurance covers medical expenses through cost-sharing -- premium, deductible, copay, coinsurance, and out-of-pocket maximum.",
        "body": "Health insurance protects individuals and families from the financial impact of illness and injury. Unlike life insurance (fixed benefit at death), health insurance reimburses actual medical expenses.\n\nCost-sharing components: Premium (monthly payment to maintain coverage). Deductible (amount insured pays before insurance begins). Copayment (fixed dollar amount per covered service). Coinsurance (percentage of costs shared after deductible -- 80/20 means insurer pays 80%, insured pays 20%). Out-of-pocket maximum (annual cap on insured's costs -- after this insurer covers 100%).\n\nCoordination of benefits (COB) applies when a person is covered by more than one plan. Establishes which plan is primary (pays first) and which is secondary (pays remainder up to 100% of costs -- never exceeding 100% total).\n\nFor the exam: know all five cost-sharing components and how they interact.",
        "example": "Deductible $1,500. Coinsurance 80/20 up to $5,000 out-of-pocket max. A $10,000 bill: insured pays $1,500 deductible + 20% of $8,500 ($1,700) = $3,200 total.",
        "memory_tip": "Cost sharing: Premium, Deductible, Copay, Coinsurance, Out-of-pocket max. PDCCO. Out-of-pocket max = your annual ceiling." },
      { "slug": "lh-managed-care", "title": "Managed Care Plans", "sort_order": 2, "estimated_minutes": 7,
        "summary": "HMOs require a PCP gatekeeper and network-only care; PPOs allow out-of-network at higher cost; EPOs require network but no gatekeeper.",
        "body": "HMO (Health Maintenance Organization): comprehensive health services through a defined network. Members must use network providers (except emergencies). A primary care physician (PCP) acts as gatekeeper, coordinating all care and referring to specialists. No coverage for out-of-network care. Lowest premiums but least flexibility.\n\nPPO (Preferred Provider Organization): contracts with preferred providers but allows out-of-network at higher cost. No PCP gatekeeper -- members self-refer to specialists. More flexibility than HMO at higher premiums.\n\nEPO (Exclusive Provider Organization): requires in-network use like HMO, but no PCP gatekeeper like PPO. No out-of-network coverage except emergencies.\n\nPOS (Point of Service): combines HMO and PPO. Members choose a PCP like HMO but can go out-of-network with higher cost sharing.\n\nFor the exam: HMO = gatekeeper + network only. PPO = no gatekeeper + in/out network. EPO = no gatekeeper + network only. POS = hybrid.",
        "example": "An HMO member needs a cardiologist. She must first see her PCP who provides an in-network referral. Without the referral the HMO will not cover the specialist visit.",
        "memory_tip": "HMO = gatekeeper PCP + network only (most restrictive). PPO = no gatekeeper + in/out network (most flexible). EPO = no gatekeeper + network only. POS = hybrid." },
    ],
    "terms": [
      {"term": "Deductible (Health)", "plain": "Amount the insured pays before health insurance starts paying", "exam": "The dollar amount the insured must pay for covered health expenses in a plan year before the insurer begins paying benefits.", "example": "With a $2,000 deductible the insured pays the first $2,000 of medical bills before the insurer contributes."},
      {"term": "Copayment", "plain": "Fixed dollar amount paid each time a covered service is used", "exam": "A fixed dollar amount the insured pays for a covered health service at time of service, regardless of the total cost.", "example": "The insured pays a $25 copay for each primary care visit and $50 for each specialist visit."},
      {"term": "Coinsurance (Health)", "plain": "Percentage of costs shared between insured and insurer after the deductible", "exam": "The percentage of covered health costs the insured pays after meeting the deductible; 80/20 means the insurer pays 80% and the insured pays 20%.", "example": "After the $1,000 deductible, 80/20 coinsurance applies: insurer pays $800 and insured pays $200 of a $1,000 bill."},
      {"term": "Out-of-Pocket Maximum", "plain": "Annual cap on the insured's health care costs", "exam": "The maximum amount the insured must pay out of pocket for covered health services in a plan year; after this the insurer covers 100% of covered costs.", "example": "After reaching the $6,000 out-of-pocket maximum the insured pays nothing for the rest of the plan year."},
      {"term": "HMO", "plain": "Managed care plan requiring a PCP gatekeeper and network-only care", "exam": "A managed care plan providing health services through a defined network; requires a primary care physician for referrals and does not cover out-of-network care except emergencies.", "example": "The HMO member cannot see a dermatologist directly -- a PCP referral is required."},
      {"term": "PPO", "plain": "Managed care plan with network discounts but allowing out-of-network care at higher cost", "exam": "A managed care plan contracting with preferred providers at discounted rates; members can self-refer to specialists and use out-of-network providers at higher cost sharing.", "example": "A PPO member sees an out-of-network orthopedic surgeon and pays 40% coinsurance instead of the 20% in-network rate."},
      {"term": "Coordination of Benefits (COB)", "plain": "Rules determining which health insurer pays first when a person has two plans", "exam": "A provision determining which plan is primary and which is secondary when an insured has multiple health coverages, preventing total payments from exceeding 100% of costs.", "example": "Covered by both employer plan and spouse's plan, COB ensures combined payments do not exceed 100% of the cost."},
    ],
    "questions": [
      ("An insured has a $1,500 deductible, 80/20 coinsurance, and $5,000 out-of-pocket max. The insured incurs $8,000 in covered medical expenses. How much does the insured pay?",
       "scenario", "hard",
       "Step 1: insured pays $1,500 deductible. Step 2: 20% coinsurance on the remaining $6,500 = $1,300. Total insured: $1,500 + $1,300 = $2,800. This is below the $5,000 out-of-pocket max.",
       [("$2,800 ($1,500 deductible plus 20% of $6,500)", True, "Correct. $1,500 deductible + 20% of remaining $6,500 ($1,300) = $2,800 total."),
        ("$1,600 (20% of the total $8,000 bill)", False, "The deductible must be applied first before coinsurance."),
        ("$5,000 (the out-of-pocket maximum)", False, "The out-of-pocket max is only reached when the calculated cost sharing exceeds $5,000."),
        ("$1,500 (the deductible only)", False, "Coinsurance also applies after the deductible is met.")]),
      ("A patient covered by an HMO wants to see a dermatologist. The patient must:",
       "scenario", "standard",
       "HMOs require members to see their PCP first. The PCP acts as a gatekeeper who coordinates care and provides referrals to specialists.",
       [("First see the primary care physician to obtain a referral", True, "Correct. HMOs require PCP referrals before specialist visits."),
        ("Contact the insurance company directly to approve the specialist visit", False, "The PCP provides the referral; the patient does not contact the insurer directly."),
        ("See any specialist in the network without prior authorization", False, "This describes PPO access; HMOs require referrals from the PCP."),
        ("Pay the full cost of the specialist visit and seek reimbursement", False, "This describes an out-of-network PPO scenario, not how HMO referrals work.")]),
      ("The out-of-pocket maximum in a health insurance plan:",
       "multiple_choice", "standard",
       "The out-of-pocket maximum is the annual cap on the insured's cost sharing. After reaching this limit the insurer covers 100% of covered expenses for the rest of the plan year.",
       [("Caps the total amount the insured pays in a plan year; after which the insurer covers 100%", True, "Correct. The out-of-pocket maximum protects the insured from catastrophic cost sharing."),
        ("Limits the total amount the insurer will pay for all claims in a plan year", False, "This describes a policy maximum, not the out-of-pocket maximum."),
        ("Applies only to prescription drug costs", False, "The out-of-pocket maximum applies to all covered health expenses."),
        ("Resets every month regardless of prior payments", False, "The out-of-pocket maximum is an annual limit and accumulates throughout the plan year.")]),
      ("Coordination of benefits (COB) in health insurance is designed to:",
       "multiple_choice", "standard",
       "When a person is covered by two health plans, COB determines which pays first (primary) and which pays second (secondary). The purpose is to prevent collecting more than 100% of actual medical costs.",
       [("Prevent double recovery when an insured is covered by more than one health plan", True, "Correct. COB ensures total payments do not exceed 100% of the covered costs."),
        ("Allow the insured to collect benefits from both plans without limitation", False, "COB prevents duplicate recovery, not unlimited collection."),
        ("Determine which plan will cover services the other plan excludes", False, "COB determines payment priority, not coverage gaps."),
        ("Require both insurers to pay 50% of every claim", False, "COB assigns primary/secondary priority; it does not require 50/50 splits.")]),
      ("A PPO member uses an out-of-network provider. Compared to an in-network visit, the PPO member will most likely:",
       "multiple_choice", "standard",
       "PPOs cover out-of-network care but at higher cost sharing than in-network care. The member typically pays higher coinsurance for out-of-network providers.",
       [("Pay higher coinsurance or a higher percentage of the bill", True, "Correct. PPO out-of-network care involves higher cost sharing than in-network care."),
        ("Receive no coverage because PPOs only cover in-network providers", False, "PPOs cover out-of-network care, unlike HMOs and EPOs which generally do not."),
        ("Pay the same cost sharing as an in-network visit", False, "The PPO incentivizes in-network use by making out-of-network more expensive."),
        ("Need prior authorization from the PCP before the out-of-network visit is covered", False, "PPOs generally do not require PCP referrals or gatekeeper authorization.")]),
    ],
  },
  {
    "slug": "health-policy-provisions",
    "title": "Health Insurance Policy Provisions",
    "description": "Mandatory provisions, renewability classifications, and key exclusions in individual health insurance.",
    "sort_order": 108,
    "lessons": [
      { "slug": "lh-health-mandatory-provisions", "title": "Mandatory Health Insurance Provisions", "sort_order": 1, "estimated_minutes": 7,
        "summary": "Grace period (31 days), notice of claim (20 days), claim forms (15 days), and time limit on defenses (2 years) are key mandatory provisions.",
        "body": "The entire contract provision states that the policy and application constitute the complete agreement.\n\nTime limit on certain defenses: after 2 years the policy cannot be contested except for fraudulent misrepresentations.\n\nGrace period: 31 days for monthly premium policies; policy stays in force after a missed premium.\n\nReinstatement: lapsed health policy may be reinstated within 2-3 years with evidence of insurability and back premiums.\n\nNotice of claim: insured must notify insurer within 20 days of a covered loss (or as soon as reasonably possible).\n\nClaim forms: insurer must provide claim forms within 15 days of receiving notice. If not provided, insured may submit proof in any written format.\n\nPayment of claims: insurer must pay claims promptly, typically within 60 days of receiving proof of loss.\n\nFor the exam: grace period = 31 days. Notice of claim = 20 days. Claim forms = 15 days. Time limit on defenses = 2 years. Payment = 60 days.",
        "example": "An insured is hospitalized Tuesday. Her agent notifies the insurer Thursday (2 days later). The 20-day requirement is satisfied. The insurer must provide claim forms within 15 days.",
        "memory_tip": "Key timelines: Grace = 31 days. Notice of claim = 20 days. Claim forms = 15 days. Time limit on defenses = 2 years. Payment = 60 days." },
      { "slug": "lh-renewability", "title": "Health Insurance Renewability Provisions", "sort_order": 2, "estimated_minutes": 7,
        "summary": "Renewability ranges from cancellable (weakest) to non-cancellable (strongest); know what rights each provides.",
        "body": "Cancellable: insurer can cancel at any time with proper notice. Least protective.\n\nOptionably renewable: insurer can non-renew on any premium due date for any reason. Cannot cancel mid-term.\n\nConditionally renewable: insurer can non-renew only for specific stated reasons (change of occupation, attainment of a maximum age).\n\nGuaranteed renewable: insurer MUST renew as long as premiums are paid. Cannot cancel or change benefits for an individual. CAN increase premiums -- but only for an entire class, not for an individual based on health changes.\n\nNon-cancellable (and guaranteed renewable): strongest -- insurer cannot cancel, increase premiums, or reduce benefits as long as premiums are paid. Most individual disability income policies.\n\nFor the exam hierarchy weakest to strongest: Cancellable, Optionally Renewable, Conditionally Renewable, Guaranteed Renewable, Non-Cancellable. Guaranteed renewable = can raise CLASS rates. Non-cancellable = locked premiums and benefits.",
        "example": "A guaranteed renewable health policy covers a 45-year-old. The insurer cannot cancel because of her health claims but CAN raise premiums for all 40-50 year olds in her class.",
        "memory_tip": "Weakest to strongest: Cancellable, Optional, Conditional, Guaranteed, Non-cancellable. Guaranteed = can raise CLASS rates. Non-cancellable = locked premiums AND benefits. COCGN." },
    ],
    "terms": [
      {"term": "Guaranteed Renewable", "plain": "Health coverage that must be renewed as long as premiums are paid, though class rates can increase", "exam": "A renewability provision requiring the insurer to renew as long as premiums are paid; the insurer can increase premiums for an entire class but cannot cancel individual policies or reduce benefits.", "example": "A guaranteed renewable policy cannot be cancelled because the insured develops cancer, but the insurer can raise rates for the entire age class."},
      {"term": "Non-Cancellable", "plain": "The strongest renewability -- insurer cannot cancel, raise premiums, or reduce benefits", "exam": "A renewability provision prohibiting the insurer from cancelling, increasing premiums, or reducing benefits as long as premiums are paid; typically used in individual disability income policies.", "example": "A non-cancellable DI policy cannot have its premium increased or benefit reduced even if the insured later develops a serious condition."},
      {"term": "Notice of Claim", "plain": "Requirement to notify the insurer within 20 days of a covered health loss", "exam": "A mandatory health insurance provision requiring the insured to notify the insurer of a covered loss within 20 days or as soon as reasonably possible.", "example": "After hospitalization the insured notifies the insurer within 20 days as required."},
      {"term": "Time Limit on Certain Defenses", "plain": "After 2 years the insurer cannot contest the policy except for fraud", "exam": "A mandatory health insurance provision limiting the period during which the insurer can contest the policy based on misrepresentations to two years from issue; after that only fraudulent misrepresentations can be used.", "example": "After the 2-year period expires the insurer cannot deny a claim based on an innocent misrepresentation in the original application."},
      {"term": "Pre-existing Condition", "plain": "A health condition that existed before coverage began", "exam": "A medical condition present before a health insurance policy's effective date; under the ACA individual and small group plans cannot exclude pre-existing conditions.", "example": "Under the ACA an insurer cannot deny coverage or charge higher premiums based on a pre-existing condition like diabetes."},
    ],
    "questions": [
      ("Under a guaranteed renewable health insurance policy, the insurer:",
       "multiple_choice", "standard",
       "A guaranteed renewable policy must be renewed as long as premiums are paid. The insurer cannot cancel or reduce benefits for an individual. However the insurer CAN increase premiums for an entire class of policyholders.",
       [("Must renew the policy but can increase premiums for an entire class", True, "Correct. Guaranteed renewable = must renew + can raise class rates; cannot cancel individuals or reduce benefits."),
        ("Cannot increase premiums under any circumstances", False, "Only non-cancellable policies guarantee both renewability and premium stability."),
        ("Can cancel the policy for any reason with 30 days notice", False, "This describes a cancellable or optionally renewable policy."),
        ("Can reduce benefits when the insured's health deteriorates", False, "A guaranteed renewable policy cannot reduce benefits for individual insureds.")]),
      ("The mandatory 20-day notice of claim provision requires:",
       "multiple_choice", "standard",
       "The notice of claim provision requires the insured to notify the insurer of a covered loss within 20 days (or as soon as reasonably possible). The insurer must then provide claim forms within 15 days.",
       [("The insured to notify the insurer within 20 days of a covered loss", True, "Correct. The insured has 20 days to give notice; the insurer then has 15 days to provide claim forms."),
        ("The insurer to acknowledge a claim within 20 days of receiving notice", False, "The 20-day requirement applies to the insured's notice obligation, not the insurer's response."),
        ("Claims to be paid within 20 days of filing proof of loss", False, "Payment is typically required within 60 days of receiving proof of loss."),
        ("The insurer to provide claim forms within 20 days of a covered loss", False, "The insurer has 15 days to provide claim forms after receiving the insured's 20-day notice.")]),
      ("From weakest to strongest consumer protection, the correct order of health insurance renewability provisions is:",
       "multiple_choice", "hard",
       "The hierarchy from least to most protective: cancellable, optionally renewable, conditionally renewable, guaranteed renewable, non-cancellable.",
       [("Cancellable, optionally renewable, conditionally renewable, guaranteed renewable, non-cancellable", True, "Correct. This is the correct hierarchy from least to most protective."),
        ("Non-cancellable, guaranteed renewable, conditionally renewable, optionally renewable, cancellable", False, "This is the reverse of the correct order."),
        ("Optionally renewable, cancellable, non-cancellable, conditionally renewable, guaranteed renewable", False, "This order is incorrect."),
        ("Guaranteed renewable, non-cancellable, conditionally renewable, optionally renewable, cancellable", False, "Non-cancellable provides stronger protection than guaranteed renewable.")]),
      ("A non-cancellable health insurance policy provides which of the following guarantees?",
       "multiple_choice", "standard",
       "Non-cancellable is the strongest renewability provision. The insurer cannot cancel, increase premiums, or reduce benefits as long as premiums are paid.",
       [("The insurer cannot cancel, raise premiums, or reduce benefits", True, "Correct. Non-cancellable = cannot cancel + cannot raise premiums + cannot reduce benefits."),
        ("The insurer cannot cancel but can raise premiums for all policyholders in the same class", False, "This describes guaranteed renewable, not non-cancellable."),
        ("The insurer can cancel only for nonpayment of premium", False, "This describes conditionally or guaranteed renewable, not non-cancellable."),
        ("The insurer guarantees payment of all claims regardless of policy exclusions", False, "Non-cancellable refers to renewability and premium stability, not scope of covered benefits.")]),
      ("If a health insurer fails to provide claim forms within 15 days of receiving notice of a claim, the insured:",
       "multiple_choice", "standard",
       "The claim forms provision requires the insurer to provide forms within 15 days. If not provided, the insured can submit proof of loss in any written format.",
       [("May submit proof of loss in any reasonable written form", True, "Correct. If the insurer fails to provide forms within 15 days, the insured can use any written format."),
        ("Loses the right to file the claim", False, "The insured's rights are not forfeited because the insurer failed to provide forms."),
        ("Must wait until the insurer provides the official forms before filing", False, "The insured does not need to wait -- they can file in any written format."),
        ("Receives an automatic extension of the proof of loss deadline", False, "The solution is permitting any written format, not extending the deadline.")]),
    ],
  },
  {
    "slug": "individual-health-policies",
    "title": "Individual Health Insurance Policies",
    "description": "Types of individual health coverage -- basic, major medical, and supplemental policies.",
    "sort_order": 109,
    "lessons": [
      { "slug": "lh-medical-expense-policies", "title": "Medical Expense Policies", "sort_order": 1, "estimated_minutes": 7,
        "summary": "Basic medical expense policies cover specific services at lower limits; major medical covers catastrophic expenses with high limits and cost sharing.",
        "body": "Basic hospital expense policies pay for inpatient hospital costs: room and board at a daily rate, miscellaneous hospital services, and a specified number of covered days.\n\nBasic surgical expense policies pay surgeons' fees using a surgical schedule listing covered procedures and maximum payments.\n\nMajor medical insurance provides broad, high-limit coverage for catastrophic expenses. Features: large maximum benefit (often unlimited), high deductibles, and coinsurance. Covers virtually all medically necessary services.\n\nThe stop-loss provision caps the insured's coinsurance payments. Once out-of-pocket coinsurance reaches a specified amount, the insurer covers 100% of additional covered expenses.\n\nComprehensive major medical combines basic and major medical. The first layer covers common expenses; the major medical layer covers catastrophic expenses above basic limits.\n\nFor the exam: basic = specific services, low limits. Major medical = broad, high limits, deductible + coinsurance. Stop-loss = cap on insured's coinsurance.",
        "example": "Patient has comprehensive major medical with $1,000 deductible, 80/20 coinsurance, and $5,000 stop-loss. A $50,000 bill: insured pays $1,000 + 20% of $49,000 = $9,800 but stop-loss caps this at $5,000. Total insured pays: $6,000.",
        "memory_tip": "Basic = specific services, low limits. Major medical = broad + high limits + deductible + coinsurance. Stop-loss = cap on insured's coinsurance portion." },
      { "slug": "lh-supplemental-health", "title": "Supplemental and Limited Benefit Health Policies", "sort_order": 2, "estimated_minutes": 7,
        "summary": "Supplemental policies pay cash benefits directly to the insured for specific conditions or events.",
        "body": "Supplemental health policies pay specific cash benefits that complement primary coverage.\n\nAccident policies pay a lump sum or scheduled benefits when the insured is injured in an accident, paid directly to the policyholder regardless of actual medical costs.\n\nCritical illness (specified disease) insurance pays a lump sum cash benefit upon diagnosis of a specified covered illness -- cancer, heart attack, stroke, organ failure. Payment is made regardless of actual medical expenses.\n\nHospital indemnity insurance pays a fixed daily benefit for each day hospitalized (e.g., $200/day) regardless of actual hospital costs. Used to cover out-of-pocket costs and deductibles.\n\nDental and vision insurance cover routine care often excluded from major medical.\n\nFor the exam: supplemental = cash DIRECTLY to insured, not to providers. Critical illness = lump sum at diagnosis. Hospital indemnity = daily cash per hospital day. All add to primary coverage.",
        "example": "An insured is diagnosed with cancer. Her critical illness policy pays $50,000 directly to her -- she uses $20,000 for medical costs and $30,000 for mortgage payments while unable to work.",
        "memory_tip": "Supplemental = cash to you, not providers. Critical illness = lump sum at diagnosis. Hospital indemnity = daily cash per hospital day. All ADD TO primary coverage." },
    ],
    "terms": [
      {"term": "Major Medical Insurance", "plain": "Comprehensive health insurance for catastrophic expenses with high limits", "exam": "A health insurance policy providing broad coverage for catastrophic medical expenses with high overall maximum benefits, deductibles, and coinsurance covering virtually all medically necessary services.", "example": "Major medical covers the full $150,000 cancer treatment after the insured meets deductible and coinsurance."},
      {"term": "Stop-Loss Provision", "plain": "Cap on the insured's coinsurance after which insurer covers 100%", "exam": "A health insurance provision limiting the insured's out-of-pocket coinsurance to a specified maximum; after this the insurer covers 100% of remaining covered expenses.", "example": "After reaching the $4,000 stop-loss the insurer covers 100% of additional medical expenses for the year."},
      {"term": "Critical Illness Insurance", "plain": "Insurance paying a lump sum at diagnosis of a specified serious illness", "exam": "A supplemental health policy paying a lump sum cash benefit directly to the insured upon diagnosis of a specified illness such as cancer, heart attack, or stroke, regardless of actual medical expenses.", "example": "Upon diagnosis of a heart attack the critical illness policy pays $75,000 directly to the insured for any purpose."},
      {"term": "Hospital Indemnity Insurance", "plain": "Insurance paying a fixed daily benefit for each day hospitalized", "exam": "A supplemental health policy paying a fixed daily benefit for each day hospitalized, regardless of actual costs; paid directly to the insured.", "example": "A hospital indemnity policy paying $300/day pays $3,000 for a 10-day hospitalization."},
      {"term": "Specified Disease Policy", "plain": "Insurance covering only specific named diseases like cancer", "exam": "A limited health insurance policy providing benefits only for specifically named diseases, most commonly cancer; also called dread disease insurance.", "example": "A cancer-only specified disease policy pays benefits for chemotherapy but provides no coverage for a heart attack."},
    ],
    "questions": [
      ("A critical illness insurance policy pays:",
       "multiple_choice", "standard",
       "Critical illness insurance pays a lump sum cash benefit directly to the insured upon diagnosis of a specified covered illness, regardless of actual medical expenses.",
       [("A lump sum cash benefit upon diagnosis of a specified covered illness", True, "Correct. Critical illness pays a lump sum at diagnosis, regardless of actual medical costs."),
        ("Reimbursement of actual medical expenses after treatment", False, "Critical illness pays a lump sum benefit, not reimbursement of specific expenses."),
        ("A daily benefit for each day the insured is hospitalized", False, "Daily hospital benefits are paid by hospital indemnity insurance."),
        ("The difference between actual expenses and the primary health insurance deductible", False, "Critical illness pays a fixed lump sum regardless of how expenses compare to deductibles.")]),
      ("The stop-loss provision in a major medical policy:",
       "multiple_choice", "standard",
       "The stop-loss provision caps the insured's coinsurance payments. Once out-of-pocket coinsurance reaches the stop-loss amount, the insurer covers 100% of additional covered expenses.",
       [("Limits the insured's total coinsurance payments to a specified maximum amount", True, "Correct. The stop-loss caps the insured's coinsurance obligations for the plan year."),
        ("Limits the insurer's total payments to a specified maximum amount", False, "A policy maximum limits insurer payments; stop-loss limits the insured's coinsurance."),
        ("Eliminates the deductible for catastrophic claims", False, "The stop-loss applies to coinsurance, not deductibles."),
        ("Automatically increases the deductible after multiple claims", False, "Stop-loss reduces the insured's cost sharing burden; it does not increase deductibles.")]),
      ("Hospital indemnity insurance differs from major medical insurance in that:",
       "multiple_choice", "standard",
       "Hospital indemnity insurance pays a fixed daily benefit directly to the insured for each day hospitalized, regardless of actual costs. Major medical reimburses actual covered medical expenses.",
       [("It pays a fixed daily benefit regardless of the actual hospital costs incurred", True, "Correct. Hospital indemnity pays a flat daily amount; major medical pays based on actual expenses."),
        ("It provides broader coverage for all medical expenses including outpatient care", False, "Hospital indemnity is more limited, not broader -- it covers only the daily hospital benefit."),
        ("It requires the insured to pay a deductible before benefits are paid", False, "Hospital indemnity typically pays from the first day without a deductible."),
        ("It must be the primary health insurance plan", False, "Hospital indemnity is supplemental coverage, not primary insurance.")]),
      ("A major medical policy has a $1,000 deductible, 80/20 coinsurance, and $3,500 stop-loss. If a covered individual incurs $20,000 in expenses, the insured pays:",
       "scenario", "hard",
       "Deductible: $1,000. Coinsurance: 20% of $19,000 = $3,800. But the stop-loss caps coinsurance at $3,500. Total insured: $1,000 + $3,500 = $4,500.",
       [("$4,500 ($1,000 deductible plus $3,500 coinsurance capped by stop-loss)", True, "Correct. Deductible ($1,000) + coinsurance capped at stop-loss ($3,500) = $4,500 total."),
        ("$3,500 (the stop-loss maximum)", False, "The stop-loss only caps the coinsurance portion; the deductible is separate and additional."),
        ("$4,000 ($1,000 deductible plus 20% of $15,000)", False, "20% of $19,000 = $3,800, which exceeds the $3,500 stop-loss, so the cap applies."),
        ("$1,000 (only the deductible since the stop-loss covers all coinsurance)", False, "The stop-loss caps coinsurance but does not eliminate the deductible.")]),
      ("Specified disease (dread disease) insurance:",
       "multiple_choice", "standard",
       "Specified disease policies cover only specifically named illnesses, most commonly cancer. They provide limited coverage compared to comprehensive major medical insurance.",
       [("Provides benefits only for the specific diseases named in the policy", True, "Correct. Specified disease policies are limited to the named diseases and provide no coverage for other conditions."),
        ("Covers all diseases not covered by the insured's major medical policy", False, "Specified disease covers only named diseases, not everything the major medical excludes."),
        ("Replaces major medical insurance with broader coverage at lower cost", False, "Specified disease is supplemental insurance, not a replacement for major medical."),
        ("Pays benefits based on actual medical expenses for all covered illnesses", False, "Specified disease typically pays a lump sum or scheduled benefit, not actual expense reimbursement.")]),
    ],
  },
  {
    "slug": "group-health-insurance",
    "title": "Group Health Insurance",
    "description": "Employer-sponsored group health coverage -- how it works, COBRA, and key differences from individual coverage.",
    "sort_order": 110,
    "lessons": [
      { "slug": "lh-group-insurance-basics", "title": "Group Insurance Fundamentals", "sort_order": 1, "estimated_minutes": 7,
        "summary": "Group insurance covers multiple people under one master policy; members are not individually underwritten and receive certificates of coverage.",
        "body": "Group insurance is a single contract (master policy) covering a group of people -- typically employees or association members. Individual members receive certificates of coverage, not policies.\n\nGroup underwriting: members are generally not individually underwritten. The group is underwritten as a whole based on demographics and claims experience, enabling coverage for people who might not qualify individually.\n\nEligibility requirements: typically full-time employees (minimum hours, often 30/week), past a waiting period (30-90 days), and actively at work on the eligibility date.\n\nOpen enrollment: annual period during which eligible employees can enroll or change coverage without evidence of insurability. Special enrollment periods triggered by qualifying life events (marriage, birth, loss of other coverage).\n\nParticipation requirements: insurers typically require 75% of eligible employees to participate to prevent adverse selection.\n\nFor the exam: master policy to employer, certificate to employee. No individual underwriting. Open enrollment = no evidence required. 75% participation minimum.",
        "example": "A company requires 75% participation (150 of 200 employees). Only 100 enroll -- below minimum. Insurer may increase premiums or decline to renew due to adverse selection.",
        "memory_tip": "Group: master policy to employer, certificate to employee. No individual underwriting. Open enrollment = no health questions. 75% minimum participation." },
      { "slug": "lh-cobra-continuation", "title": "COBRA and Continuation of Coverage", "sort_order": 2, "estimated_minutes": 7,
        "summary": "COBRA requires employers with 20+ employees to offer continued group health coverage after qualifying events, at up to 102% of the full premium.",
        "body": "COBRA (Consolidated Omnibus Budget Reconciliation Act) requires employers with 20 or more employees to offer continuation of group health coverage to employees and dependents who lose coverage due to a qualifying event.\n\nQualifying events: termination of employment (except gross misconduct), reduction in hours, divorce or legal separation, the covered employee enrolling in Medicare, and a dependent child aging out of coverage.\n\nCOBRA continuation lasts: 18 months for termination or reduction in hours (with possible 36-month extension for disability), 36 months for other qualifying events (divorce, dependent aging out).\n\nThe COBRA premium: individual pays up to 102% of the full group premium (employee + employer share + 2% admin fee). Much higher than what the employee paid because the employer no longer subsidizes.\n\nNotice requirements: employer notifies plan administrator within 30 days. Plan administrator notifies qualified beneficiary within 14 days. Qualified beneficiary has 60 days to elect COBRA.\n\nFor the exam: 20+ employees. 60 days to elect. 102% premium. 18 months (termination) or 36 months (divorce, dependent).",
        "example": "An employee is laid off. She has 60 days to elect COBRA. If she elects, she pays $650/month (full premium + 2%) instead of the $150/month she paid as an employee, for up to 18 months.",
        "memory_tip": "COBRA: 20+ employees, 60 days to elect, 102% of full premium, 18 months (termination) or 36 months (divorce/dependent). Federal minimum requirements." },
    ],
    "terms": [
      {"term": "Master Policy", "plain": "The single group insurance contract issued to the employer", "exam": "The group insurance contract issued to the employer or association providing coverage for all eligible group members; individual members receive certificates of coverage.", "example": "The employer holds the master group health policy; each employee receives a certificate summarizing their coverage."},
      {"term": "Certificate of Coverage", "plain": "Document given to individual group members summarizing their coverage", "exam": "A document provided to individual members summarizing coverage under the master group policy; not the insurance contract itself.", "example": "Each employee receives a certificate of coverage booklet describing their health benefits and copays."},
      {"term": "COBRA", "plain": "Federal law requiring employers with 20+ employees to offer continued group health coverage after qualifying events", "exam": "The Consolidated Omnibus Budget Reconciliation Act; requires employers with 20+ employees to offer continuation of group health coverage at up to 102% of the full premium after qualifying events.", "example": "After being laid off, an employee elects COBRA and pays $720/month for the same coverage that cost $120/month as an employee."},
      {"term": "Open Enrollment", "plain": "Annual period when employees can enroll or change group coverage without health questions", "exam": "A designated period during which eligible employees can enroll in or change group insurance coverage without evidence of insurability.", "example": "During open enrollment an employee adds dental coverage and increases life insurance without any medical exam."},
      {"term": "Participation Requirement", "plain": "Minimum percentage of eligible employees who must enroll in a group plan", "exam": "An insurer requirement that a minimum percentage of eligible employees (typically 75%) enroll in the group plan, protecting against adverse selection.", "example": "An insurer requires 75% participation; if only 60% enroll the insurer may decline to renew the group policy."},
    ],
    "questions": [
      ("Under COBRA, a terminated employee has how many days after the qualifying event to elect continuation coverage?",
       "multiple_choice", "standard",
       "COBRA requires the qualified beneficiary to be given 60 days to elect continuation coverage after receiving notice of the qualifying event.",
       [("60 days", True, "Correct. COBRA provides 60 days to elect continuation coverage."),
        ("30 days", False, "The employer must notify the plan administrator within 30 days; the employee has 60 days to elect."),
        ("90 days", False, "90 days is not the COBRA election period; 60 days is correct."),
        ("14 days", False, "The plan administrator has 14 days to notify the beneficiary; the beneficiary then has 60 days to elect.")]),
      ("The maximum COBRA continuation period for an employee who is terminated is:",
       "multiple_choice", "standard",
       "Termination of employment (other than gross misconduct) triggers 18 months of COBRA continuation. Divorce and dependent aging out trigger 36 months.",
       [("18 months", True, "Correct. Termination or reduction in hours triggers 18 months of COBRA continuation."),
        ("12 months", False, "12 months is not the COBRA duration for termination."),
        ("36 months", False, "36 months applies to other qualifying events (divorce, dependent aging out), not termination."),
        ("24 months", False, "24 months is not the standard COBRA continuation period.")]),
      ("Under a group insurance plan, individual employees receive:",
       "multiple_choice", "standard",
       "The master policy is issued to the employer. Individual employees receive certificates of coverage, not policies, that summarize their coverage.",
       [("Certificates of coverage, not individual policies", True, "Correct. The employer holds the master policy; employees receive certificates summarizing their coverage."),
        ("Individual policies identical to the master policy", False, "Individual policies are not issued to group members."),
        ("Declarations pages showing their individual coverage limits", False, "Declarations pages are part of individual policies; group members receive certificates."),
        ("Endorsements modifying the master policy for their specific needs", False, "Endorsements modify the master policy at the employer level, not for individual employees.")]),
      ("Open enrollment in a group health plan allows employees to:",
       "multiple_choice", "standard",
       "Open enrollment is the annual window during which eligible employees can enroll or change coverage without providing evidence of insurability.",
       [("Enroll or change coverage without providing evidence of insurability", True, "Correct. Open enrollment allows changes without health questions."),
        ("Obtain coverage at a discounted rate compared to mid-year enrollment", False, "Open enrollment does not provide discounted rates; the benefit is waiving evidence of insurability."),
        ("Cancel coverage without consequence if they do not want group benefits", False, "Employees can waive coverage during open enrollment, but this is not the primary benefit."),
        ("Add dental and vision coverage that is otherwise unavailable", False, "Open enrollment applies to all group benefits, not just dental and vision.")]),
      ("An employer with 15 employees is not subject to federal COBRA requirements because:",
       "multiple_choice", "standard",
       "Federal COBRA applies to employers with 20 or more employees. Employers with fewer than 20 employees are not subject to federal COBRA, though some states have mini-COBRA laws.",
       [("Federal COBRA only applies to employers with 20 or more employees", True, "Correct. COBRA's 20-employee threshold means smaller employers are not subject to the federal law."),
        ("COBRA only applies to publicly traded companies", False, "COBRA applies to private and public employers with 20+ employees."),
        ("COBRA does not apply to employers with fewer than 50 employees", False, "The COBRA threshold is 20 employees, not 50."),
        ("COBRA only applies to employers who offer both medical and dental benefits", False, "COBRA applies to employers with 20+ employees regardless of which benefits they offer.")]),
    ],
  },
]


def seed_part2():
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
        print(f"\n=== Part 2 complete: {mod_count} modules, {lesson_count} lessons, {term_count} terms, {q_count} questions ===")
    finally:
        db.close()


if __name__ == "__main__":
    seed_part2()
