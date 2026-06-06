from __future__ import annotations

from copy import deepcopy

# Extra state-neutral P&C content layered on top of the compact base seed.
# This avoids one giant course_seed.py overwrite while still deepening the course.

EXTRA_CONTENT = {
    "insurance-basics": {
        "lessons": [
            ("risk-management-methods", "Risk Management Methods", "Risk can be handled by avoidance, retention, sharing, reduction, or transfer. Insurance is a transfer method because the financial effect of certain losses is shifted to the insurer."),
            ("law-of-large-numbers", "Law of Large Numbers", "Insurers use large groups of similar risks to predict losses more accurately. The larger the similar exposure group, the more predictable the overall loss experience becomes."),
            ("insurable-interest", "Insurable Interest", "Insurable interest means the insured must have a real financial interest in the property or person being insured. For property insurance, it generally must exist at the time of loss."),
        ],
        "terms": [
            ("Avoidance", "Not doing the risky activity.", "A risk management method that eliminates exposure to a loss by avoiding the activity.", "A business avoids delivery exposure by not offering delivery."),
            ("Retention", "Keeping some or all of the risk.", "A risk management method where a person or business accepts financial responsibility for loss.", "Choosing a deductible is partial retention."),
            ("Transfer", "Shifting financial risk to another party.", "A risk management method where financial consequences are shifted, often by insurance.", "Buying insurance transfers certain covered loss costs."),
            ("Insurable Interest", "A real financial stake in the insured item.", "A legal or financial interest that would result in loss if the insured property is damaged or destroyed.", "A homeowner has insurable interest in their house."),
        ],
    },
    "insurance-contracts": {
        "lessons": [
            ("parts-of-an-insurance-policy", "Parts of an Insurance Policy", "A policy is usually read by starting with declarations, then definitions, insuring agreement, exclusions, conditions, and endorsements. Endorsements can change the original printed policy."),
            ("named-insured-vs-insured", "Named Insured vs Insured", "The named insured is listed on the declarations page. Other people may also qualify as insureds depending on definitions and coverage forms."),
            ("conditions-and-duties", "Conditions and Duties", "Conditions explain what the insured and insurer must do. Duties after loss may include giving prompt notice, protecting property, and cooperating with the insurer."),
        ],
        "terms": [
            ("Insuring Agreement", "The insurer promise to pay covered losses.", "The policy section stating the insurer's coverage promise, subject to other terms.", "The agreement says the insurer will pay covered damages."),
            ("Condition", "A policy rule or duty.", "A policy provision that sets obligations or rules for coverage.", "Prompt notice after loss is a condition."),
            ("Named Insured", "The person or entity named on the declarations page.", "The individual or organization listed as the named insured in the policy declarations.", "ABC LLC is the named insured on a CGL policy."),
            ("Duties After Loss", "Steps the insured must take after a loss.", "Policy duties such as notice, protection of property, inventory of damaged property, and cooperation.", "Calling the insurer after a fire is part of duties after loss."),
        ],
    },
    "property-fundamentals": {
        "lessons": [
            ("open-perils-vs-named-perils", "Open Perils vs Named Perils", "Named perils coverage applies only to listed causes of loss. Open perils coverage applies unless the cause of loss is excluded or limited."),
            ("deductibles", "Deductibles", "A deductible is the insured portion of a covered loss. Deductibles help reduce small claims and can lower premium."),
            ("coinsurance", "Coinsurance", "Coinsurance requires the insured to carry a certain percentage of insurance to value. If the requirement is not met, a penalty may apply to partial losses."),
        ],
        "terms": [
            ("Named Perils", "Only listed causes of loss are covered.", "Coverage for only the perils specifically listed in the policy.", "Fire and lightning may be named perils."),
            ("Open Perils", "Covered unless excluded.", "Coverage for direct physical loss unless the cause is excluded or limited.", "A special form may use open perils for a dwelling."),
            ("Deductible", "The insured share of a covered loss.", "The amount the insured must pay before the insurer pays a covered claim.", "A $1,000 deductible applies to a covered property claim."),
            ("Coinsurance", "Insurance-to-value requirement.", "A provision requiring insurance to be carried at a stated percentage of value to avoid a penalty.", "An 80% coinsurance clause may penalize underinsurance."),
        ],
    },
    "casualty-fundamentals": {
        "lessons": [
            ("legal-liability", "Legal Liability", "Liability coverage generally requires legal responsibility. The insured may be responsible because of negligence, statute, contract, or other legal basis."),
            ("defense-costs", "Defense Costs", "Liability policies often provide defense for covered claims. Defense may be inside or outside the limit depending on the policy."),
            ("damages", "Damages", "Damages may include bodily injury, property damage, and sometimes personal or advertising injury depending on the policy. Punitive damages are treated differently by policy and jurisdiction."),
        ],
        "terms": [
            ("Legal Liability", "Legal responsibility for injury or damage.", "Responsibility imposed by law or contract for damages to another party.", "A negligent driver is legally liable for another driver's damage."),
            ("Defense Costs", "Costs to defend a claim.", "Attorney fees and related expenses incurred to defend a covered liability claim.", "A CGL insurer hires counsel to defend a lawsuit."),
            ("Occurrence", "An accident or repeated exposure.", "An accident, including continuous or repeated exposure to substantially the same harmful conditions.", "A slip and fall can be an occurrence."),
            ("Damages", "Money claimed or awarded for loss.", "Compensation sought or awarded because of injury, damage, or covered offense.", "A court awards damages after a liability suit."),
        ],
    },
    "personal-auto": {
        "lessons": [
            ("medical-payments-and-pip", "Medical Payments and PIP", "Medical payments coverage can pay medical expenses for insureds and passengers regardless of fault. Personal injury protection is broader in some states, but details are state-specific."),
            ("uninsured-underinsured-motorists", "Uninsured and Underinsured Motorists", "UM and UIM coverages can protect insureds when an at-fault driver has no insurance or not enough insurance, subject to policy and state rules."),
            ("auto-policy-exclusions", "Personal Auto Exclusions", "Auto policies contain exclusions such as intentional injury, certain business use, racing, and using vehicles without a reasonable belief of entitlement."),
        ],
        "terms": [
            ("Medical Payments", "Auto medical expense coverage.", "Coverage for reasonable medical expenses for covered persons, usually regardless of fault.", "A passenger has medical bills after an accident."),
            ("Uninsured Motorist", "Coverage when the at-fault driver has no insurance.", "Coverage for insureds injured by a driver without applicable liability insurance.", "The other driver has no insurance."),
            ("Underinsured Motorist", "Coverage when the at-fault driver lacks enough limits.", "Coverage when the legally responsible driver's limits are insufficient.", "The at-fault driver's limits are lower than the damages."),
            ("Collision Deductible", "Deductible for collision damage.", "The amount the insured pays before collision coverage responds.", "A $500 collision deductible applies after a covered crash."),
        ],
    },
    "homeowners": {
        "lessons": [
            ("additional-coverages", "Homeowners Additional Coverages", "Homeowners policies include additional coverages such as debris removal, reasonable repairs, fire department service charge, and property removed, subject to limits."),
            ("special-limits", "Special Limits of Liability", "Certain classes of personal property have special limits, such as money, securities, watercraft, trailers, jewelry, firearms, and silverware."),
            ("homeowners-exclusions", "Homeowners Exclusions", "Common exclusions include flood, earth movement, neglect, intentional loss, power failure, war, and nuclear hazard, subject to policy wording."),
        ],
        "terms": [
            ("Coverage D", "Loss of use coverage.", "Coverage for additional living expense and fair rental value after a covered loss.", "A family needs a hotel after a covered fire."),
            ("Coverage E", "Personal liability coverage.", "Coverage for damages because of bodily injury or property damage for which an insured is legally liable.", "A guest sues after slipping on the porch."),
            ("Coverage F", "Medical payments to others.", "Coverage for certain medical expenses of others, regardless of fault, subject to limits.", "A guest has a minor injury at the home."),
            ("Special Limit", "A lower limit for certain property.", "A policy limit that applies to specific categories of personal property.", "Money may have a special limit."),
        ],
    },
    "dwelling-policies": {
        "lessons": [
            ("dwelling-coverages", "Dwelling Policy Coverages", "Dwelling policies may include Coverage A dwelling, Coverage B other structures, Coverage C personal property, Coverage D fair rental value, and Coverage E additional living expense depending on form."),
            ("fair-rental-value", "Fair Rental Value", "Fair rental value can pay lost rental income when covered damage makes rented premises unfit for normal use."),
            ("dwelling-eligibility", "Dwelling Policy Eligibility", "Dwelling forms are often used for rental dwellings, seasonal homes, vacant dwellings, or properties that do not fit homeowners eligibility."),
        ],
        "terms": [
            ("Fair Rental Value", "Lost rental income after covered damage.", "Coverage for rental income loss when covered property damage makes premises unfit for normal use.", "A rental home cannot be occupied after a covered fire."),
            ("Additional Living Expense", "Extra living costs after covered damage.", "Coverage for necessary increased living costs after covered damage makes the residence unfit.", "The insured rents temporary lodging."),
            ("Dwelling Coverage", "Coverage for the residence building.", "Coverage for the dwelling structure described in the policy.", "The rental house itself is covered."),
            ("Broad Form", "Coverage that adds more named perils.", "A form providing broader named-perils coverage than a basic form.", "DP-2 is commonly called broad form."),
        ],
    },
    "commercial-property": {
        "lessons": [
            ("causes-of-loss-forms", "Causes of Loss Forms", "Commercial property coverage often uses basic, broad, or special causes of loss forms. Special form is generally open perils subject to exclusions."),
            ("value-reporting", "Value Reporting", "Value reporting allows a business with fluctuating values to report inventory or property values periodically. Accurate reporting is critical."),
            ("ordinance-or-law", "Ordinance or Law", "Ordinance or law coverage addresses increased costs caused by enforcement of building codes after covered damage, when added or included."),
        ],
        "terms": [
            ("Business Income Period of Restoration", "Time needed to resume operations.", "The period beginning after covered damage and ending when property should be repaired or replaced with reasonable speed.", "A store reopens after repairs are complete."),
            ("Causes of Loss", "Perils form for commercial property.", "The form that identifies covered and excluded causes of loss.", "Basic, broad, and special forms are causes of loss forms."),
            ("Ordinance or Law", "Coverage for code-related costs.", "Coverage for increased costs due to enforcement of building laws or ordinances after loss.", "A city requires updated wiring during repair."),
            ("Value Reporting", "Periodic reporting of property values.", "A method for reporting changing property values during the policy period.", "A retailer reports inventory monthly."),
        ],
    },
    "commercial-general-liability": {
        "lessons": [
            ("products-completed-operations", "Products and Completed Operations", "Products-completed operations coverage addresses certain bodily injury or property damage arising from products or completed work after possession is relinquished or work is complete."),
            ("cgl-exclusions", "Common CGL Exclusions", "CGL policies exclude many exposures such as expected or intended injury, workers compensation, employer liability, auto, aircraft, watercraft, and damage to your work."),
            ("cgl-limits", "CGL Limits and Aggregates", "CGL policies include per-occurrence limits and aggregate limits. The general aggregate and products-completed operations aggregate are commonly tested."),
        ],
        "terms": [
            ("Products-Completed Operations", "Liability from products or completed work.", "Coverage for certain injury or damage arising out of products or completed operations.", "A completed repair later causes property damage."),
            ("General Aggregate", "Total policy limit for many CGL claims.", "The most the insurer will pay for certain claims during the policy period.", "Multiple slip-and-fall claims reduce the aggregate."),
            ("Personal and Advertising Injury", "Injury from listed offenses.", "Coverage for offenses such as libel, slander, false arrest, or certain advertising injury.", "A business is accused of libel in an ad."),
            ("Occurrence Limit", "Limit per covered occurrence.", "The maximum paid for one occurrence, subject to aggregate limits.", "One customer injury triggers one occurrence limit."),
        ],
    },
    "business-auto": {
        "lessons": [
            ("business-auto-physical-damage", "Business Auto Physical Damage", "Commercial auto physical damage may include comprehensive, specified causes of loss, and collision coverage, depending on selected coverages and symbols."),
            ("garage-and-motor-carrier", "Garage and Motor Carrier Concepts", "Some auto businesses need specialized forms such as garage coverage or motor carrier coverage. These are separate from a standard business auto exposure."),
            ("auto-symbol-strategy", "Reading Auto Symbols", "Always match the covered auto symbol to the specific coverage. A symbol may apply to liability but not physical damage."),
        ],
        "terms": [
            ("Symbol 1", "Any auto for liability.", "A business auto symbol generally used for any auto liability coverage.", "Symbol 1 is broad for liability."),
            ("Symbol 7", "Specifically described autos.", "Coverage applies only to autos listed in the declarations.", "A scheduled truck is covered under Symbol 7."),
            ("Specified Causes of Loss", "Listed commercial auto physical damage causes.", "Coverage for listed perils such as fire, theft, windstorm, hail, and flood depending on form.", "Theft of a covered truck may be included."),
            ("Garagekeepers", "Coverage for customers' autos in care.", "Coverage for loss to customers' autos left with the insured for service, repair, storage, or safekeeping.", "A repair shop stores a customer's car overnight."),
        ],
    },
    "workers-compensation": {
        "lessons": [
            ("wc-benefit-types", "Workers Compensation Benefit Types", "Workers compensation benefits generally include medical benefits, disability income, rehabilitation, and death benefits, subject to state law."),
            ("course-and-scope", "Course and Scope of Employment", "A work injury generally must arise out of and occur in the course of employment. Commuting and non-work activities may be treated differently by state rules."),
            ("classification-and-payroll", "Classification and Payroll", "Workers compensation premium is commonly based on classification codes, payroll, rates, and experience modification factors."),
        ],
        "terms": [
            ("Experience Modification Factor", "A rating factor based on loss history.", "A factor that adjusts premium based on actual loss experience compared with expected losses.", "A business with poor loss history may have a higher mod."),
            ("Classification Code", "A code for job/work type.", "A code used to classify workplace exposure for workers compensation rating.", "Clerical employees and roofers have different codes."),
            ("Medical Benefits", "Payment for work injury medical care.", "Benefits for necessary medical treatment related to a covered work injury or disease.", "An injured worker receives treatment after a workplace accident."),
            ("Death Benefits", "Benefits paid after fatal work injury.", "Benefits payable to eligible dependents after a covered work-related death.", "Dependents receive benefits after a fatal workplace accident."),
        ],
    },
    "crime-bonds-specialty": {
        "lessons": [
            ("money-and-securities", "Money and Securities", "Crime coverage often distinguishes money, securities, and other property. The type of property and cause of loss matter."),
            ("burglary-robbery-theft", "Burglary, Robbery, and Theft", "Burglary usually involves unlawful entry or exit, robbery involves taking by force or threat, and theft is broader unlawful taking."),
            ("bond-parties", "Bond Parties", "A surety bond involves the principal, obligee, and surety. It is not the same as two-party insurance."),
        ],
        "terms": [
            ("Burglary", "Theft involving unlawful entry or exit.", "Taking property from inside premises with evidence of unlawful entry or exit.", "A locked business is broken into after hours."),
            ("Robbery", "Taking by force or threat.", "Taking property from a person by force or threat of force.", "A cashier is forced to hand over money."),
            ("Principal", "The party whose performance is guaranteed.", "The party that promises to perform under a surety bond.", "A contractor is the principal on a performance bond."),
            ("Obligee", "The party protected by a bond.", "The party to whom the principal owes an obligation.", "A project owner is the obligee."),
        ],
    },
    "ethics-producer-responsibilities": {
        "lessons": [
            ("express-implied-apparent-authority", "Express, Implied, and Apparent Authority", "Express authority is written or spoken authority given by the insurer. Implied authority is necessary to carry out express authority. Apparent authority is what a reasonable person believes the producer has based on insurer conduct."),
            ("handling-premiums", "Handling Premiums", "Producers have fiduciary responsibility when handling premiums. Funds must be handled honestly, promptly, and according to law and contract."),
            ("advertising-and-disclosure", "Advertising and Disclosure", "Insurance advertising must not mislead consumers. Producers should be clear about insurers, products, and limitations."),
        ],
        "terms": [
            ("Express Authority", "Authority clearly given.", "Authority specifically granted by the insurer to the producer.", "A contract authorizes the producer to solicit applications."),
            ("Implied Authority", "Authority needed to do the job.", "Authority not stated but reasonably necessary to carry out express authority.", "Scheduling appointments with prospects."),
            ("Apparent Authority", "Authority others reasonably believe exists.", "Authority created when insurer actions lead a reasonable person to believe the producer is authorized.", "The insurer lets a producer use company materials."),
            ("Rebating", "Giving an improper inducement.", "Offering something of value not stated in the policy to induce purchase, where prohibited.", "Offering part of commission to buy a policy."),
        ],
    },
    "exam-prep": {
        "lessons": [
            ("eliminating-distractors", "Eliminating Distractors", "Strong exam strategy is to eliminate answers that are too broad, state-specific when not asked, unrelated to the policy section, or based only on fairness."),
            ("scenario-question-method", "Scenario Question Method", "For scenario questions, identify the line of insurance, the coverage part, the key fact, and any exclusion or condition before choosing an answer."),
            ("final-week-review", "Final Week Review", "In the final week, focus on weak areas, missed questions, flashcards, and timed practice. Do not spend all time rereading lessons passively."),
        ],
        "terms": [
            ("Distractor", "A believable wrong answer.", "An answer choice designed to distract from the best answer.", "A true statement that does not answer the question."),
            ("Qualifier", "A word that changes the question.", "A word such as except, not, best, first, or most likely that controls the answer.", "The word except asks for the wrong statement."),
            ("Timed Practice", "Practicing under time limits.", "A study method that simulates test pacing and pressure.", "Taking a 50-question timed quiz."),
            ("Active Recall", "Testing memory instead of rereading.", "A study method that forces retrieval through questions, flashcards, or explaining concepts.", "Answering missed questions again without notes."),
        ],
    },
}


def _lesson(slug: str, title: str, body: str, order: int) -> dict:
    first = body.split(".")[0] + "."
    return {
        "slug": slug,
        "title": title,
        "summary": first,
        "body": body,
        "example": f"Example: An exam question may ask the candidate to apply {title.lower()} to a short insurance scenario.",
        "memory_tip": f"For {title}, identify the key fact first, then match it to the policy concept.",
        "audio_script": f"{title}. {body}",
        "estimated_minutes": 7,
        "sort_order": order,
    }


def _term(term: str, plain: str, exam: str, example: str) -> dict:
    return {
        "term": term,
        "plain_english_definition": plain,
        "exam_definition": exam,
        "example": example,
    }


def enrich_course(course: dict) -> dict:
    enriched = deepcopy(course)
    modules = {m["slug"]: m for m in enriched.get("modules", [])}

    for module_slug, payload in EXTRA_CONTENT.items():
        module = modules.get(module_slug)
        if not module:
            continue

        existing_lesson_slugs = {l["slug"] for l in module.get("lessons", [])}
        next_order = len(module.get("lessons", [])) + 1
        for slug, title, body in payload.get("lessons", []):
            if slug not in existing_lesson_slugs:
                module.setdefault("lessons", []).append(_lesson(slug, title, body, next_order))
                existing_lesson_slugs.add(slug)
                next_order += 1

        existing_terms = {t["term"].lower() for t in module.get("terms", [])}
        for term, plain, exam, example in payload.get("terms", []):
            if term.lower() not in existing_terms:
                module.setdefault("terms", []).append(_term(term, plain, exam, example))
                existing_terms.add(term.lower())

    return enriched
