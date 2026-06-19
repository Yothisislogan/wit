#!/usr/bin/env python3
"""
load_lesson_content_batch3.py
Run from pc-license-prep-server-v2/ directory:
    .venv/bin/python3 scripts/load_lesson_content_batch3.py

Adds real lesson content for:
- Dwelling Policies
- Commercial Property Insurance
- Commercial General Liability
- Business Auto Insurance
- Workers Compensation and Employers Liability
- Crime, Bonds, and Specialty Coverages
- Exam Prep and Final Review

Safe to re-run — skips lessons already over 300 chars.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_all
from app.models import Lesson
from sqlalchemy import select

LESSON_CONTENT = {

# ═══════════════════════════════════════════════════════════════════════
# MODULE 7 — DWELLING POLICIES
# ═══════════════════════════════════════════════════════════════════════

"dwelling-policy-overview": (
    """Dwelling policies are designed for residential properties that do not qualify for homeowners insurance or that are used as investment properties rather than owner-occupied residences. Understanding when to use a dwelling policy instead of a homeowners policy is a common exam topic.

The most common situations requiring a dwelling policy include: rental properties owned by landlords, owner-occupied homes in poor condition that do not meet homeowners underwriting standards, vacant properties, and homes that are being renovated or are otherwise unusual risks.

The key structural difference between a dwelling policy and a homeowners policy is that the dwelling policy does NOT automatically include personal liability coverage or medical payments coverage. These must be added by endorsement. A landlord who wants liability protection for slip-and-fall claims at their rental property must add a personal liability endorsement to the dwelling policy.

The Insurance Services Office (ISO) has developed three dwelling policy forms. The DP-1 (Basic Form) covers only fire, lightning, and internal explosion — the most restrictive coverage available. The DP-2 (Broad Form) adds windstorm, hail, explosion, riot, aircraft, vehicles, smoke, vandalism, and limited theft — a named perils form with more covered causes. The DP-3 (Special Form) covers the dwelling on an open perils basis (all causes except exclusions) — the broadest and most common dwelling form for investment properties.

For the exam, know which form applies to which situation and which perils each form covers. The DP-1 is rarely used because its coverage is so narrow. The DP-3 is preferred for most rental properties because open perils coverage eliminates gaps from unexpected causes. Note that even under DP-3, personal property is covered on a named perils basis — the open perils treatment applies only to the dwelling structure itself.
""",
    "Dwelling policies cover residential properties ineligible for homeowners insurance, with three forms ranging from basic (DP-1) to open perils (DP-3).",
    "A landlord who rents three houses cannot use homeowners policies for the rental properties. They use DP-3 forms for the structures and add personal liability endorsements to protect against tenant injury claims.",
    "Dwelling policy = landlord's tool. DP-1 = fire only. DP-2 = broader named perils. DP-3 = open perils on dwelling. No automatic liability — must add endorsement."
),

"dwelling-coverages": (
    """The dwelling policy provides four primary coverages, designated A through D, that parallel — but differ from — the homeowners policy coverages with the same letter designations.

Coverage A — Dwelling covers the main residential structure at the described location. Under DP-3, this is on an open perils basis. The coverage includes the structure itself, built-in appliances, and permanently installed fixtures. The coverage is written for the dwelling at the address shown on the declarations — unlike homeowners, dwelling policies are location-specific and do not follow the insured to other properties.

Coverage B — Other Appurtenant Structures covers detached structures on the property — garages, fences, and storage sheds. This is similar to Coverage B under the homeowners policy and is typically limited to 10% of Coverage A. Structures rented to non-tenants (other than a garage) and structures used for business are excluded.

Coverage C — Personal Property is optional under dwelling policies — it must specifically be added. When included, it covers the insured's personal property (landlord's furnishings left in the rental, for example) on a named perils basis. Tenant's personal property is NOT covered under the landlord's dwelling policy — tenants need their own renters insurance (HO-4) for their belongings.

Coverage D — Fair Rental Value (and Additional Living Expense) covers lost rental income when a covered loss makes the property unrentable while repairs are made. This is the most important coverage difference from the homeowners policy — homeowners have additional living expenses; landlords have fair rental value. If the landlord also occupies part of the property, there may be an additional living expense component.

For the exam, the most tested distinction is that Coverage C (tenant's personal property) is NOT included and NOT covered, and that Coverage D for a dwelling policy is fair rental value, not additional living expense.
""",
    "Dwelling policies provide Coverage A (dwelling structure), B (other structures), C (personal property — optional), and D (fair rental value).",
    "A fire damages a rental house. Coverage A pays for structural repairs ($45,000). Coverage D pays the lost rent for three months while repairs are made ($3,600). The tenant's destroyed belongings are not covered — the tenant needed their own HO-4.",
    "A = structure. B = detached structures (10% of A). C = landlord's personal property only (optional). D = fair rental value (not additional living expense). Tenant's stuff = tenant's problem."
),

"dwelling-forms-comparison": (
    """Comparing the three dwelling forms side by side is one of the most effective ways to study for exam questions about dwelling policies. Each form represents a different level of coverage, and the exam frequently tests which form would or would not cover a specific loss.

The DP-1 Basic Form covers only three perils: fire, lightning, and internal explosion. It pays on an actual cash value basis — not replacement cost. This form is rarely used in practice but appears on the exam. A loss from any other cause — windstorm, theft, vandalism — is simply not covered under DP-1.

The DP-2 Broad Form adds substantial perils to the DP-1 list: windstorm and hail, explosion (external as well as internal), riot and civil commotion, aircraft, vehicles, smoke, vandalism and malicious mischief, damage by burglar (limited), falling objects, weight of ice/snow/sleet, and water damage from plumbing. It pays on a replacement cost basis for the dwelling when insured to value. This is a named perils form — the listed perils are the complete coverage list.

The DP-3 Special Form covers the dwelling structure on an open perils basis — all causes of loss except those specifically excluded. Common exclusions include flood, earthquake, earth movement, ordinance or law costs, intentional acts, and neglect. Personal property, if added, is covered on a named perils basis identical to DP-2.

A critical distinction for the exam: under DP-3, if a loss occurs and the cause is not known, coverage applies because open perils doesn't require identifying the cause — it's covered unless excluded. Under DP-1 or DP-2, the insured must prove the loss was caused by a listed peril.

The choice of form affects not just covered perils but also valuation. DP-1 defaults to ACV. DP-2 and DP-3 offer replacement cost on the dwelling structure when the property is insured to at least 80% of its replacement cost value.
""",
    "DP-1 covers only fire/lightning/explosion at ACV; DP-2 adds named perils; DP-3 covers the dwelling on open perils — the broadest dwelling form.",
    "A rental property's roof is damaged by the weight of accumulated ice. Under DP-1: denied (not a listed peril). Under DP-2: covered (weight of ice/snow is listed). Under DP-3: covered (open perils, no exclusion for this cause).",
    "DP-1 = fire/lightning/explosion only. DP-2 = DP-1 + weather + vandalism + water damage + more. DP-3 = open perils on dwelling. More coverage = higher premium. ACV (DP-1) vs RC (DP-2/DP-3)."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 8 — COMMERCIAL PROPERTY INSURANCE
# ═══════════════════════════════════════════════════════════════════════

"commercial-property-overview": (
    """Commercial property insurance protects businesses against loss of or damage to their physical assets — buildings, equipment, inventory, and other property. Unlike personal lines, commercial property is more complex because businesses have diverse property exposures, operational dependencies, and contractual obligations.

The Commercial Package Policy (CPP) is the standard vehicle for combining commercial coverages. It allows businesses to combine commercial property, general liability, and other coverages into a single policy. The Commercial Lines Manual (CLM) governs rating; the Insurance Services Office (ISO) develops the standard forms.

The Building and Personal Property (BPP) Coverage Form is the workhorse of commercial property insurance. It covers three categories of property: the building (the structure and permanently installed fixtures), business personal property (furniture, equipment, inventory, and tenant improvements), and personal property of others (property belonging to others that is in the insured's care for storage or processing).

Business personal property under the BPP includes a broad range of items: furniture and fixtures, machinery and equipment, stock (inventory), leasehold improvements and betterments made by the tenant, labor and materials used for repairs, and property leased from others for which the insured has responsibility.

Key exclusions from the BPP include: land, water, growing crops, money and securities (covered under crime policies), vehicles (covered under commercial auto), and property more specifically described elsewhere in the policy.

The commercial property policy uses the same three cause-of-loss forms as other property coverage — basic, broad, and special — and the same coinsurance provisions. Commercial buyers almost always use the special (open perils) form to avoid coverage gaps from unexpected causes.

For the exam, know what the BPP covers and what it excludes, how the three coverage tiers differ, and the role of coinsurance in commercial property valuation.
""",
    "Commercial property insurance protects business assets through the Building and Personal Property Coverage Form covering structures, business personal property, and property of others.",
    "A fire damages a printing company's building, destroys their printing presses, burns their paper inventory, and damages a customer's files stored on their premises. The BPP covers all four: building, equipment, stock, and personal property of others.",
    "BPP = three coverages: Building + Business personal property + Personal property of others. Excludes land, money, vehicles. Three cause-of-loss forms: basic, broad, special."
),

"business-income-coverage": (
    """Business income coverage (also called business interruption insurance) is the commercial property coverage that protects against indirect losses — specifically the loss of income when a business cannot operate due to physical damage from a covered cause of loss. It is one of the most valuable and most underutilized commercial coverages.

The standard business income coverage form pays for two types of losses during the period of restoration. First, it pays net income that would have been earned had the loss not occurred. Second, it pays continuing normal operating expenses — payroll, rent, loan payments, utilities, and other expenses that go on even when the business is not generating revenue.

The period of restoration begins when the physical damage occurs (not when the claim is filed) and ends when the property is repaired or replaced with reasonable speed and similar quality. Most policies have a waiting period (commonly 72 hours) before business income coverage begins paying.

Extra expense coverage is the companion to business income. While business income replaces lost revenue, extra expense pays the additional costs incurred to minimize the interruption — renting temporary space, expediting repairs, using more expensive substitute equipment or suppliers. Extra expense coverage enables businesses to continue operating (even at higher cost) rather than shutting down completely.

The coinsurance requirement applies to business income coverage — typically at 50%, 70%, 80%, or 125% of annual net income and operating expenses. Underestimating income at policy inception can result in a coinsurance penalty at claim time, leaving the business bearing a portion of its own loss.

For the exam, know the difference between business income (replacing lost revenue) and extra expense (paying extra costs to continue operating), and know that the period of restoration is tied to physical repair time, not the policy period.
""",
    "Business income coverage pays lost net income and continuing expenses during the period of restoration after a covered physical loss prevents normal operations.",
    "A restaurant suffers a kitchen fire. Business income pays the $8,000/month net income lost while closed (2 months = $16,000) plus ongoing $4,000/month payroll for kept employees ($8,000). Extra expense pays $3,000 for temporary kitchen rental to fill catering orders.",
    "Business income = lost revenue + continuing expenses. Extra expense = additional costs to keep operating. Period of restoration = time to repair. Coinsurance applies. 72-hour waiting period common."
),

"commercial-property-conditions": (
    """Commercial property policies contain several important conditions that govern how claims are handled and what obligations the insured must meet. The exam tests these conditions because failing to meet them can result in a reduced or denied claim.

The coinsurance condition is the most calculation-intensive. As discussed, the insured must carry coverage equal to a specified percentage of the property's value (typically 80%) or face a proportional penalty on partial losses. The agreed value option suspends coinsurance entirely — when an insured and insurer agree on the property's value and the insurer endorses the policy at that amount, no coinsurance calculation applies.

The valuation condition specifies how the insurer will value losses. Commercial property policies can be written on a replacement cost basis (new for old, the most common choice) or actual cash value basis (replacement cost minus depreciation). Under replacement cost, the insurer typically pays the ACV first, then pays the additional replacement cost amount when the property is actually repaired or replaced — this prevents the insured from collecting the higher replacement cost amount and pocketing the difference without repairing.

The mortgage condition protects mortgage lenders who are listed as mortgageholders on the policy. The mortgageholder has an independent right to claim payment even if the named insured's coverage is void due to policy violations (like failing to report a material change in risk). The insurer can pay the mortgageholder and then seek recovery from the insured.

The subrogation condition preserves the insurer's right to recover from responsible third parties after paying a claim. The insured must not take any action that impairs the insurer's subrogation rights — such as signing a release or waiver with a responsible party before the insurer has been reimbursed.

For the exam, focus on coinsurance calculations, the difference between ACV and replacement cost payments, and the mortgageholder's independent rights under the policy.
""",
    "Commercial property conditions govern coinsurance calculations, loss valuation methods, mortgage protection, and subrogation rights.",
    "An insured collects $150,000 for fire damage to their building. Six months later, an investigation reveals the fire was caused by a negligent contractor. The insurer exercises subrogation rights and sues the contractor to recover the $150,000 paid — the insured must cooperate and cannot block this recovery.",
    "Coinsurance = carry enough or pay a penalty. RC pays ACV first, then extra after repair. Agreed value = suspends coinsurance. Mortgageholder has independent rights. Subrogation = insurer recovers from responsible parties."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 9 — COMMERCIAL GENERAL LIABILITY
# ═══════════════════════════════════════════════════════════════════════

"cgl-overview": (
    """The Commercial General Liability (CGL) policy is the foundational liability coverage for businesses of all sizes. It protects against the most common third-party claims that businesses face — bodily injury, property damage, personal injury, and advertising injury caused by the insured's operations.

The CGL contains three coverage parts, each addressing a distinct type of liability exposure. Coverage A covers bodily injury and property damage liability — the most common type of claim, such as a customer slipping on the business's floor or a contractor accidentally breaking a window. Coverage B covers personal and advertising injury liability — claims arising from specific offenses including libel, slander, false arrest, copyright infringement, and misappropriation of advertising ideas. Coverage C covers medical payments — a no-fault coverage that pays medical expenses for third parties injured on the insured's premises without requiring a finding of liability.

The CGL is written on an occurrence basis for most commercial accounts — the policy in force when the injury or damage OCCURRED responds, regardless of when the claim is made. Some professional liability exposures use claims-made forms (professional liability, directors and officers, etc.), but the standard CGL is occurrence-based.

The CGL policy uses two key limits: the per-occurrence limit caps what the insurer pays for any single occurrence (accident) or series of related occurrences. The general aggregate limit caps total payments for all occurrences during the policy period (excluding products/completed operations, which have their own separate aggregate).

For the exam, identify which coverage part responds to a given scenario: Coverage A (bodily injury/property damage from operations), Coverage B (personal/advertising injury offenses), or Coverage C (no-fault medical payments). Know that defense costs are supplementary payments outside the limits.
""",
    "The CGL covers business liability through three parts: Coverage A (bodily injury/property damage), Coverage B (personal/advertising injury), and Coverage C (medical payments).",
    "A retail store faces three CGL claims in one year: a customer trips on a display (Coverage A — bodily injury), a competitor sues for stealing their advertising slogan (Coverage B — advertising injury), and a child cuts their hand on a shelf (Coverage C — medical payments).",
    "CGL = three coverages. A = BI/PD from operations. B = personal/advertising injury offenses. C = no-fault medical for third parties. Occurrence-based. Per-occurrence + aggregate limits."
),

"cgl-coverage-a": (
    """Coverage A of the CGL — Bodily Injury and Property Damage Liability — is the broadest and most important component of the policy. It covers the insured's legal liability for unintentional physical harm to people and damage to property caused by the insured's business operations.

The insuring agreement for Coverage A promises to pay amounts the insured becomes legally obligated to pay as damages for bodily injury or property damage, provided the injury or damage is caused by an occurrence, happens during the policy period, and is not excluded.

Bodily injury is defined as physical injury, sickness, disease, or death. It includes associated mental anguish when it flows from physical injury. Pure emotional distress without physical harm is typically NOT covered under Coverage A.

Property damage means physical injury to tangible property, including loss of use of that property. It does not cover damage to intangible property, loss of data, or loss of use of property that was not itself physically damaged.

The occurrence trigger is important: an occurrence is an accident, including continuous or repeated exposure to substantially the same harmful conditions. This broad definition covers both sudden accidents (a customer falls) and gradual harm (long-term chemical exposure from a manufacturer's operations).

Several exclusions limit Coverage A's scope. The expected or intended injury exclusion removes coverage for harm the insured deliberately caused. The contractual liability exclusion removes coverage for liability assumed in most contracts (with exceptions for insured contracts). The workers compensation exclusion removes coverage for employee injuries. The pollution exclusion removes coverage for most pollution claims. The care, custody, and control exclusion removes coverage for property in the insured's possession.

For the exam, be able to apply Coverage A to a scenario and identify whether an exclusion prevents coverage.
""",
    "CGL Coverage A pays damages for bodily injury and property damage the insured causes to others through business operations — subject to key exclusions.",
    "A plumber's employee drops a pipe fitting that shatters a customer's antique vase (property damage, Coverage A). The homeowner tries to pick up the pieces and cuts their hand (bodily injury, Coverage A). Both are covered under a single occurrence.",
    "Coverage A = BI + PD from occurrences. Occurrence = accident including gradual harm. Key exclusions: intentional acts, employee injury, CCC, pollution, contractual (with exceptions)."
),

"cgl-completed-operations": (
    """The products and completed operations hazard is one of the most important — and most misunderstood — components of the CGL. It covers liability that arises after the insured's work is finished or after the insured's products leave their possession.

Products liability covers claims arising from products the insured manufactures, sells, handles, or distributes after those products have left the insured's possession. If a consumer is injured by a defective product the insured sold, that is a products liability claim — covered under the products and completed operations portion of Coverage A.

Completed operations liability covers claims arising from the insured's work after it has been completed and accepted by the customer. A contractor who builds a deck, turns the project over to the homeowner, and later learns the deck collapsed due to faulty construction faces a completed operations claim. This is distinct from premises and operations liability, which covers claims that arise while work is still in progress.

The distinction between premises/operations and products/completed operations matters for policy limits. The CGL has a separate aggregate limit specifically for products and completed operations claims — this aggregate is separate from the general aggregate. Exhausting the general aggregate does not affect the products/completed operations aggregate, and vice versa.

Time is a key factor. Completed operations coverage responds to injuries that occur after the work is done — even years later if the defect existed when work was completed. The occurrence policy form means the policy in force when the injury occurs (not when the work was done) responds.

For the exam, identify whether a claim arises from ongoing operations (premises/operations) or from finished work/products (completed operations). A building under construction → premises/operations. The same building after the contractor leaves → completed operations.
""",
    "Products and completed operations coverage responds to claims arising after the insured's products leave their control or work is completed and accepted.",
    "A general contractor builds an office building. Three years after completion, a section of the ceiling collapses, injuring a tenant. This is a completed operations claim under the contractor's CGL — covered under the policy in force when the injury occurred, not when the building was completed.",
    "During construction = premises/operations. After handover = completed operations. Products sold = products liability. Separate aggregate for products/completed ops. Occurrence form: when injury happens, not when work was done."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 10 — BUSINESS AUTO INSURANCE
# ═══════════════════════════════════════════════════════════════════════

"bap-overview": (
    """The Business Auto Policy (BAP) is the standard commercial auto policy for most businesses. It covers vehicles used in business operations and the liability arising from their use. Understanding the BAP is essential because it differs significantly from the Personal Auto Policy (PAP) in structure and coverage triggers.

The most fundamental difference between the BAP and PAP is how covered autos are defined. The PAP covers specifically described vehicles plus newly acquired autos. The BAP uses a numerical symbol system on the declarations page — each number defines a different category of covered vehicles, and different coverage parts can apply to different symbol categories.

The BAP contains the same basic coverage types as the PAP: liability (covering bodily injury and property damage to others), medical payments (for occupants of covered autos), uninsured motorist (protecting insured persons hit by uninsured drivers), and physical damage (collision and comprehensive for covered autos). However, the structure and limits differ from personal auto.

Liability under the BAP covers any auto, any driver, and any use described by the applicable symbol — making it potentially much broader than personal auto coverage. The insured's employees are covered while operating covered autos in the course of business.

The BAP is typically written as part of a Commercial Package Policy along with the CGL. This is important because the two policies divide the liability exposure: the CGL covers on-premises and non-auto liability; the BAP covers auto-related liability. Together they provide comprehensive commercial liability protection.

For the exam, know that the BAP uses symbols to define covered autos, that it covers business use of vehicles, and that it works alongside the CGL to provide complete commercial liability coverage.
""",
    "The Business Auto Policy uses numbered symbols to define covered vehicles and provides liability, medical payments, UM, and physical damage coverage for business vehicles.",
    "A delivery company's BAP covers all owned trucks (Symbol 2), any hired trucks rented for overflow capacity (Symbol 8), and any non-owned vehicles driven by employees on company business (Symbol 9).",
    "BAP = commercial auto. Symbol system defines covered autos. Works with CGL: CGL covers non-auto liability, BAP covers auto liability. Same coverage types as PAP but different structure."
),

"bap-symbols": (
    """The Business Auto Policy's symbol system is one of the most unique and heavily tested aspects of commercial auto insurance. Each numeric symbol defines which vehicles are covered under a specific coverage part, giving insurers and insureds precise control over the scope of coverage.

Symbol 1 — Any Auto: The broadest coverage — covers any auto the named insured owns, hires, borrows, or uses. This is the most expansive option and is typically used for the liability coverage of businesses with diverse auto exposures.

Symbol 2 — Owned Autos Only: Covers only autos the named insured owns. Rented and borrowed vehicles are not covered. Newly acquired owned autos are automatically covered for 30 days.

Symbol 3 — Owned Private Passenger Autos Only: Further restricts Symbol 2 to private passenger vehicles — excludes trucks and commercial vehicles.

Symbol 4 — Owned Autos Other Than Private Passenger: The complement of Symbol 3 — covers owned commercial vehicles but not passenger cars.

Symbol 5 — Owned Autos Subject to No-Fault: Used in no-fault states for PIP coverage — applies only to autos required to have no-fault benefits in the insured state.

Symbol 6 — Owned Autos Subject to Compulsory Uninsured Motorist: Similar to Symbol 5 but for uninsured motorist coverage.

Symbol 7 — Specifically Described Autos: Covers only the specific vehicles listed on the schedule. The most restrictive owned-auto option — no automatic coverage for vehicles not listed.

Symbol 8 — Hired Autos Only: Covers vehicles the business leases, rents, or borrows from others (not employees). A business that rents trucks for special projects adds Symbol 8 to get hired auto liability.

Symbol 9 — Non-Owned Autos Only: Covers vehicles not owned by the insured that are used in the business — typically employee-owned vehicles used for business errands. Symbol 9 protects the employer from vicarious liability when employees use personal vehicles for work.

For the exam, Symbol 1 (any auto), Symbol 7 (specifically described), Symbol 8 (hired), and Symbol 9 (non-owned) are the most frequently tested.
""",
    "BAP symbols precisely define which vehicles are covered: Symbol 1 (any auto) is broadest; Symbol 7 (specifically described) is most restrictive for owned vehicles.",
    "A law firm's BAP includes Symbol 1 for liability (covers any auto anyone drives for firm business), Symbol 7 for physical damage (only the two specific firm-owned vehicles get collision/comprehensive), and Symbol 9 for uninsured motorist (protects attorneys using personal cars for depositions).",
    "Symbol 1 = any auto (broadest). Symbol 7 = listed autos only. Symbol 8 = hired/rented. Symbol 9 = non-owned/employee vehicles. Mix symbols for different coverage parts to match actual exposure."
),

"hired-nonowned-auto": (
    """Hired auto and non-owned auto liability are two coverage extensions that many businesses need but frequently overlook until a claim occurs. Both address liability exposure from vehicles the business does not own.

Hired auto liability covers vehicles that the business rents, leases, or borrows from others (but not from employees or the named insured's household members). When a company rents a van for a trade show, the rental agreement typically requires the renter to provide their own liability coverage — that is where hired auto comes in. Hired auto is added to the BAP under Symbol 8 or as an endorsement to the CGL for businesses that do not have a BAP.

Non-owned auto liability covers vehicles that employees, partners, or members own and drive on company business. When a sales representative drives their personal car to visit a client and causes an accident, the employer may be vicariously liable. Non-owned auto coverage (Symbol 9 on the BAP) protects the employer in this situation.

An important coverage rule: when an employee uses their personal vehicle for business, the employee's personal auto policy (PAP) is primary. The employer's BAP non-owned auto coverage is excess. This means the employee's PAP responds first; only after the PAP limits are exhausted does the BAP non-owned auto coverage contribute.

Drive Other Car (DOC) coverage is a related endorsement important for executives who have company-provided vehicles and no personal auto policy of their own. Without a PAP, these individuals have no coverage when driving a rental car, a borrowed vehicle, or any auto not described in their employer's BAP. DOC provides personal auto-type coverage for these gaps.

For the exam, distinguish between hired auto (rented/borrowed from third parties) and non-owned auto (employee-owned vehicles used for business). Know that the employee's PAP is primary for non-owned auto claims.
""",
    "Hired auto covers rented/leased vehicles; non-owned auto covers employee-owned vehicles used for business — both extend the BAP to vehicles the business doesn't own.",
    "A company's accountant drives her personal car to a client meeting and rear-ends another driver. Her PAP pays first (primary). If the judgment exceeds her PAP limits, the company's BAP non-owned auto coverage pays the excess (excess coverage).",
    "Hired = rented from others. Non-owned = employee's personal car. Employee's PAP is primary; employer's BAP is excess. DOC = coverage for executives with no personal auto policy."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 11 — WORKERS COMPENSATION AND EMPLOYERS LIABILITY
# ═══════════════════════════════════════════════════════════════════════

"workers-comp-overview": (
    """Workers compensation is a system of no-fault insurance that provides guaranteed benefits to employees who suffer work-related injuries or illnesses, regardless of fault. It is the oldest and most universal form of social insurance in the United States.

The system emerged in the early 20th century as a compromise between employees and employers. Before workers compensation, an injured worker had to sue their employer for negligence to receive any compensation — a slow, expensive process with no guaranteed outcome. Workers compensation replaced this with a guaranteed benefit system: employees give up the right to sue the employer in tort (the exclusive remedy doctrine) in exchange for guaranteed medical care, wage replacement, and rehabilitation benefits, regardless of fault.

Workers compensation laws are state-specific. Each state has its own statutory benefit schedule defining what is paid for different types of injuries, how long benefits last, and which employers are required to participate. Most states require virtually all employers with even one employee to carry workers compensation insurance (some exemptions exist for sole proprietors, domestic workers, farm workers, and others depending on the state).

The workers compensation policy has two parts. Part One — Workers Compensation covers the statutory benefits required by the state workers compensation law — whatever the state law requires, the policy pays. There is no dollar limit on Part One; the insurer pays all statutory benefits. Part Two — Employers Liability covers the employer against lawsuits by employees that fall outside the workers compensation system — such as suits by spouses for loss of consortium, or cases involving gross negligence where the exclusive remedy doctrine may not apply.

For the exam, know that WC is no-fault (the injured worker does not prove negligence), the exclusive remedy doctrine protects employers from tort suits, Part One covers statutory benefits (no limit), and Part Two covers employer liability lawsuits (with a limit).
""",
    "Workers compensation provides no-fault, statutory benefits to injured workers in exchange for giving up the right to sue their employer in tort.",
    "A warehouse worker breaks her arm moving boxes. Workers comp pays 100% of her medical bills (no deductible or copay) and two-thirds of her wages during recovery — no fault determination needed, no lawsuit required.",
    "No-fault system. Exclusive remedy = can't sue employer (usually). Part One = statutory benefits, no dollar limit. Part Two = employer liability suits, has limits. State law determines benefit amounts."
),

"workers-comp-benefits": (
    """Workers compensation provides four categories of benefits to injured workers. The exam tests each category and the specific circumstances that trigger each one.

Medical benefits pay for all necessary medical treatment related to the work injury — doctor visits, hospitalization, surgery, physical therapy, prescription medication, and more. There is no deductible or copay for the employee. Medical benefits are paid without a dollar limit in most states and continue as long as the injury requires treatment.

Disability income benefits replace a portion of the worker's lost wages during the period they cannot work. There are four types. Temporary Total Disability (TTD) applies when the worker is completely unable to work but will eventually recover — this is the most common type, paying approximately two-thirds of pre-injury wages. Temporary Partial Disability (TPD) applies when the worker can return to work in a limited capacity at reduced wages during recovery — the benefit supplements the wage difference. Permanent Partial Disability (PPD) applies when a worker has a permanent impairment but can still work in some capacity — benefits compensate for the permanent loss of function. Permanent Total Disability (PTD) applies when the worker is permanently and totally unable to work — benefits continue for life or as defined by state law.

Rehabilitation benefits pay for vocational rehabilitation services to help injured workers return to the workforce when they cannot return to their original job. This might include job retraining, education assistance, or job placement services.

Death benefits pay a portion of the deceased worker's wages to eligible dependents — typically the spouse and dependent children. Most states also cover reasonable funeral expenses.

For the exam, be able to classify a described injury situation into the correct disability category and know that medical benefits have no dollar cap.
""",
    "Workers compensation provides medical benefits, four types of disability income (TTD, TPD, PPD, PTD), rehabilitation, and death benefits to eligible dependents.",
    "A construction worker severs two fingers (PPD — permanent impairment, can still work other jobs). A separate worker suffers a traumatic brain injury and can never work again (PTD — permanent total disability, benefits for life).",
    "Medical = 100%, no cap, no copay. TTD = totally disabled, temporary. TPD = working at reduced capacity. PPD = permanent impairment, can still work. PTD = never working again. Death = dependents."
),

"employers-liability": (
    """Part Two of the workers compensation policy — Employers Liability — is often misunderstood because it sounds redundant alongside Part One. In reality, it covers a completely different exposure: lawsuits against the employer that fall outside the workers compensation system.

The exclusive remedy doctrine protects employers from most tort suits by injured employees — the employee's remedy is limited to workers compensation benefits. However, several important situations can break through the exclusive remedy protection and expose the employer to common-law liability suits.

Dual capacity suits occur when the employer is also the manufacturer of the product that caused the employee's injury. The employee may sue as a products liability claimant (not as an employee), bypassing the exclusive remedy.

Third-party-over suits occur when a third party (such as an equipment manufacturer) is sued by the injured employee, and the third party then sues the employer for contribution, alleging the employer's negligence contributed to the accident.

Loss of consortium suits are brought by the injured employee's spouse or family members for their own losses (companionship, services, support) resulting from the employee's injury. The family members were never employees and are not bound by the exclusive remedy.

Employers in certain states face suits when employees can establish employer gross negligence or intentional acts — situations where courts have found the exclusive remedy unfair.

Part Two covers all these exposures up to its specified limits (typically $100,000/$500,000/$100,000 — per accident bodily injury / policy limit bodily injury / disease per employee). Part Two has dollar limits, unlike Part One's unlimited statutory coverage.

For the exam, know that Part Two covers employer liability suits that bypass the exclusive remedy, that it has policy limits (unlike Part One), and that the most common scenarios are dual capacity, third-party-over, and consortium claims.
""",
    "Employers Liability (Part Two) covers lawsuits against employers that break through the workers compensation exclusive remedy doctrine, with specified policy limits.",
    "An employee injured by a defective machine on the job collects WC benefits (Part One). She also sues the machine manufacturer (third party). The manufacturer then sues the employer, alleging faulty maintenance contributed to the injury. This third-party-over suit triggers the employer's Part Two coverage.",
    "Part Two = tort suits that escape exclusive remedy. Three common break-throughs: dual capacity, third-party-over, consortium claims. Has limits (unlike Part One). Typical limits: $100K/$500K/$100K."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 12 — CRIME, BONDS, AND SPECIALTY COVERAGES
# ═══════════════════════════════════════════════════════════════════════

"crime-coverage-overview": (
    """Commercial crime insurance protects businesses against financial losses caused by criminal acts — primarily theft, fraud, and dishonesty. While property insurance covers many physical losses, crime insurance specifically addresses losses involving the intentional taking or manipulation of money, securities, and property.

The commercial crime policy (developed by ISO under the Commercial Crime Program) can be written as a standalone policy or as a coverage part in a Commercial Package Policy. It uses a discovery form (claims must be discovered during the policy period) or a loss sustained form (losses must occur during the policy period).

The major crime coverage options include employee theft (dishonesty), forgery or alteration, theft of money and securities, robbery and safe burglary, computer fraud, funds transfer fraud, and money orders and counterfeit money. Each coverage addresses a specific type of criminal act, and each must typically be specifically selected and paid for.

Employee theft (historically called fidelity coverage or employee dishonesty) is the most important crime coverage for most businesses. It covers direct financial losses the business suffers due to theft by its own employees — embezzlement, skimming, payroll fraud, and similar schemes. Businesses are often more exposed to employee crime than external crime; studies consistently show that employee theft is a significant cause of business losses.

Crime policies exclude losses discovered after a set period following policy termination, losses caused by owners or partners (not employees), and certain other excluded parties. The definition of employee is critical — leased employees, temporary workers, and volunteers may or may not be covered depending on policy language.

For the exam, know the major crime coverage types, the distinction between discovery and loss sustained forms, and the critical role of employee theft coverage for most commercial accounts.
""",
    "Commercial crime insurance covers business losses from criminal acts including employee theft, forgery, robbery, computer fraud, and counterfeit money.",
    "A bookkeeper embezzles $85,000 over three years by writing checks to fictitious vendors. Employee theft coverage under the crime policy covers this loss — it arose from a dishonest act by an employee for financial gain.",
    "Crime policy = protection from intentional criminal acts. Major coverages: employee theft, forgery, robbery, computer fraud. Discovery form vs loss sustained form. Employee theft = most important for most businesses."
),

"surety-bonds": (
    """Surety bonds are fundamentally different from insurance, and the exam tests this distinction repeatedly. Understanding the three-party structure of a surety bond and its key differences from insurance is essential.

A surety bond involves three parties. The principal is the party who must perform an obligation — typically a contractor who must complete a project. The obligee is the party who requires the bond and is protected if the principal fails to perform — the project owner or government entity. The surety is the insurance company or bonding company that guarantees the principal will perform.

The critical difference from insurance: in insurance, the insurer expects to pay losses and prices the premium accordingly. In a surety bond, the surety does NOT expect to pay claims — the bond is a credit instrument guaranteeing the principal's performance. If the surety must pay a claim, it has the right to recover (indemnification) from the principal. The premium for a surety bond is essentially a fee for the surety's financial guarantee.

Contract bonds guarantee the performance of construction contracts. A performance bond guarantees the contractor will complete the project according to contract terms. A payment bond guarantees the contractor will pay subcontractors, suppliers, and laborers. A bid bond guarantees that a contractor who is awarded a project will enter into the contract at the bid price. A maintenance bond guarantees the contractor's work for a specified period after completion.

License and permit bonds are required by governments for businesses to obtain operating licenses. They guarantee the business will comply with applicable laws and regulations. Common examples: contractor license bonds, auto dealer bonds, mortgage broker bonds.

Court bonds (also called judicial bonds) include appeal bonds (guaranteeing payment if an appeal fails) and fiduciary bonds (guaranteeing faithful performance by executors, trustees, and guardians).

Fidelity bonds protect employers against dishonest acts by employees. Unlike employee theft coverage in a crime policy, fidelity bonds are traditionally three-party instruments, though modern crime policies have largely replaced standalone fidelity bonds.
""",
    "Surety bonds are three-party instruments (principal/obligee/surety) guaranteeing performance — not insurance, because the surety can recover from the principal if it pays a claim.",
    "A city requires a $500,000 performance bond before awarding a bridge construction contract. If the contractor abandons the project, the surety steps in to complete the project or compensate the city — then recovers the cost from the contractor.",
    "Three parties: principal (must perform), obligee (protected), surety (guarantees). Not insurance — surety recovers from principal. Performance bond = complete the job. Payment bond = pay the subs. License bond = comply with laws."
),

"specialty-lines": (
    """Specialty insurance lines cover risks that are too unique, hazardous, or large for standard insurance markets. These coverages are important for the exam because they fill critical gaps in standard commercial programs.

Ocean marine insurance is one of the oldest forms of insurance. It covers cargo transported by sea, the vessel (hull) itself, freight income (the ship owner's earnings from transporting cargo), and maritime liability. Ocean marine policies are highly customized and often placed in specialty markets like Lloyd's of London.

Inland marine insurance covers property in transit over land and certain types of movable or floating property. Examples include contractor's equipment (bulldozers, cranes that move between job sites), electronic data processing equipment, fine arts, jewelry, and goods being transported by truck or rail. Inland marine is extremely flexible — almost anything that doesn't fit neatly into standard property coverage can be written as an inland marine floater.

Aviation insurance covers aircraft hull (physical damage to the aircraft) and aviation liability (bodily injury and property damage arising from the aircraft's operation). Aviation requires specialized underwriting because of the unique risks and potentially catastrophic losses. Commercial airline policies and private aircraft policies differ significantly.

Crop insurance protects farmers against loss of crops from natural causes — drought, flood, hail, disease, and pests. The federal government heavily subsidizes crop insurance through the Federal Crop Insurance Corporation (FCIC) to ensure food security.

Title insurance protects real estate buyers and lenders against defects in the title to real property — prior liens, encumbrances, fraud, or errors in public records that could challenge ownership. Unlike other insurance that covers future events, title insurance covers past events that might affect current ownership.

For the exam, know the basics of each specialty line and, most importantly, understand inland marine as the flexible coverage for movable property.
""",
    "Specialty lines including ocean marine, inland marine, aviation, crop, and title insurance cover unique risks that don't fit standard property and liability policies.",
    "A jewelry store sends $200,000 in diamonds to a trade show via armored carrier. The standard commercial property policy doesn't cover property in transit — an inland marine jeweler's floater covers the diamonds wherever they travel.",
    "Ocean marine = cargo + hull on water. Inland marine = property in transit on land + movable property. Aviation = aircraft + aviation liability. Title = past title defects. Crop = natural disasters to crops."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 14 — EXAM PREP AND FINAL REVIEW
# ═══════════════════════════════════════════════════════════════════════

"exam-strategy": (
    """The P&C licensing exam is a multiple-choice test — typically 150 questions in most states, with a passing score of 70%. The format rewards systematic preparation and smart test-taking strategy as much as raw memorization.

Understanding the exam's structure helps you allocate study time. Most state exams are weighted toward general P&C principles (about 25-30%), property insurance (25-30%), casualty/liability insurance (25-30%), and state-specific regulations (10-20%). The weight on state-specific laws varies dramatically by state — in some states it's minimal; in others it's 25% of the exam.

For multiple-choice questions, follow a systematic approach. Read the question stem carefully before looking at the answers — identify what the question is actually asking. Watch for qualifier words: always, never, only, except, most, primarily. These words often contain the answer or eliminate wrong choices. Read all four choices before selecting — do not stop at the first answer that seems right.

When you are unsure, use elimination. Most wrong answers are wrong for a specific reason — they are true statements that don't answer the question, they apply to the wrong coverage, or they confuse similar concepts. Eliminating two wrong answers gives you a 50/50 chance on the remaining two.

Pace yourself: 150 questions in 150 minutes means one minute per question. Questions you find difficult should be flagged and returned to at the end. Never leave a question blank — there is no penalty for guessing, and a 25% chance is better than 0%.

For content review, prioritize high-frequency topics: the PAP (split limits, permissive use, UM/UIM), homeowners policy (HO-3 form, coverage letters, exclusions), the CGL (occurrence vs claims-made, products/completed operations), and workers compensation (exclusive remedy, benefit types). These appear across virtually every state exam.
""",
    "The P&C exam is 150 questions at 70% passing — succeed by knowing high-frequency topics, using systematic elimination, and pacing carefully.",
    "A test-taker eliminates two clearly wrong answers on a question about the CGL, leaving 'Coverage A' and 'Coverage B.' They recall that Coverage A is bodily injury/property damage and Coverage B is personal/advertising injury — the scenario describes a slander claim, so Coverage B is correct.",
    "150 questions, 70% to pass, ~1 minute each. Qualifier words matter. Eliminate before guessing. Never leave blank. High-frequency: PAP, HO-3, CGL, WC, basic principles."
),

"policy-comparison-review": (
    """One of the most effective exam preparation strategies is comparing similar policies side by side. Many exam questions test whether you know the difference between two related coverages — and the ability to distinguish them quickly saves time under exam conditions.

PAP vs BAP: The PAP covers personal vehicles for personal use (plus incidental business use). The BAP covers vehicles used in business operations. The PAP uses specific vehicle descriptions; the BAP uses symbols. Both provide liability, medical payments, UM/UIM, and physical damage — but the BAP applies to commercial risks with different underwriting considerations.

HO-3 vs DP-3: Both use open perils on the structure. The HO-3 is for owner-occupied residences and includes personal liability and medical payments automatically. The DP-3 is for landlord/investment properties and does NOT include liability — it must be added. Under HO-3, Coverage C (personal property) is named perils. Under DP-3, personal property coverage is optional and also named perils.

CGL vs Professional Liability: The CGL covers bodily injury and property damage from business operations. Professional liability (E&O) covers financial losses resulting from negligent professional services — a gap specifically excluded by the CGL. Most professionals need both: the CGL for premises slip-and-fall, etc., and E&O for their professional advice.

Occurrence vs Claims-Made: Occurrence forms cover events that happen during the policy period, no matter when the claim is filed. Claims-made forms cover claims that are filed during the policy period, regardless of when the injury occurred (subject to the retroactive date). Most CGL policies are occurrence; most professional liability policies are claims-made.

Workers Comp Part One vs Part Two: Part One covers statutory WC benefits — no dollar limit, pays whatever the state law requires. Part Two covers employer liability lawsuits — has policy limits, covers suits that bypass the exclusive remedy doctrine.
""",
    "Comparing similar policies side by side is the most efficient exam prep strategy — know PAP vs BAP, HO-3 vs DP-3, CGL vs E&O, and occurrence vs claims-made.",
    "On the exam: 'A landlord's dwelling policy provides personal liability coverage.' FALSE — dwelling policies do not include personal liability. A homeowners policy does. Knowing this distinction is the difference between a right and wrong answer.",
    "PAP=personal/DP-3=landlord. HO-3 includes liability/DP-3 doesn't. CGL covers BI-PD/E&O covers professional negligence. Occurrence=when it happens/claims-made=when reported. WC Part 1=unlimited/Part 2=limited."
),

"final-review-key-concepts": (
    """As you approach the exam, certain concepts appear so frequently across question types that mastering them pays dividends across multiple questions. This lesson consolidates the highest-frequency concepts from every module.

Indemnity: Insurance restores, never enriches. The insured should be no better off financially after a loss than before. This principle underlies ACV valuation, coinsurance, other insurance provisions, and subrogation.

Insurable interest: The insured must have a financial stake. Without it, the contract is a wager. For property: at time of loss. For life: at time of application.

Subrogation: After paying a claim, the insurer steps into the insured's shoes to recover from the responsible party. The insured cannot impair subrogation rights by releasing responsible parties.

Coinsurance formula: (Amount carried ÷ Amount required) × Loss = Payment. Required = Property value × Coinsurance percentage. Underinsurance = penalty.

The four negligence elements: Duty, Breach, Causation, Damages. All four must be present. Comparative negligence reduces recovery; contributory negligence bars it.

Named vs open perils: Named = only listed perils covered (insured proves cause). Open = all perils covered except exclusions (insurer must prove exclusion applies).

Claims-made vs occurrence: Occurrence = when it happened. Claims-made = when it was reported. Claims-made needs tail/prior acts coverage for gaps.

PAP structure: Part A = liability to others. Part B = your medical bills. Part C = UM/UIM (uninsured/underinsured). Part D = physical damage to your vehicle.

CGL structure: Coverage A = BI/PD. Coverage B = personal/advertising injury. Coverage C = medical payments (no-fault).

Workers compensation: No-fault. Exclusive remedy. Part One = unlimited statutory benefits. Part Two = employer liability lawsuits. Medical = 100%. Disability = 2/3 of wages.

For the final stretch of exam preparation: take full-length practice exams under timed conditions. Review every wrong answer to understand the concept, not just the correct answer. The goal is not to memorize — it is to understand why each answer is right and why the others are wrong.
""",
    "The highest-frequency exam concepts span all modules: indemnity, insurable interest, subrogation, coinsurance, negligence elements, named vs open perils, and the structures of PAP, CGL, and workers comp.",
    "An exam question asks: 'An insured collects full payment from their insurer and then also sues the responsible party and wins. What must happen?' Subrogation: the insured must reimburse the insurer for what it paid. The insured cannot keep both payments.",
    "Lock these in: Indemnity = restore not enrich. Subrogation = insurer recovers. Coinsurance = (carried÷required)×loss. Negligence = DBCD. PAP = ABCD parts. CGL = ABC coverages. WC = no-fault, exclusive remedy."
),

}


def load_content():
    create_all()
    db = SessionLocal()
    try:
        updated = 0
        skipped = 0
        not_found = 0

        for slug, (body, summary, example, memory_tip) in LESSON_CONTENT.items():
            lesson = db.scalar(select(Lesson).where(Lesson.slug == slug))
            if not lesson:
                print(f"  NOT FOUND: {slug}")
                not_found += 1
                continue

            current_len = len(lesson.body or "")
            if current_len >= 300:
                print(f"  SKIP ({current_len} chars): {slug}")
                skipped += 1
                continue

            lesson.body = body.strip()
            lesson.summary = summary.strip()
            lesson.example = example.strip()
            lesson.memory_tip = memory_tip.strip()
            updated += 1
            print(f"  UPDATED ({len(body)} chars): {slug}")

        db.commit()
        print(f"\nDone: {updated} updated, {skipped} skipped, {not_found} not found.")
    finally:
        db.close()


if __name__ == "__main__":
    load_content()
