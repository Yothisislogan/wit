#!/usr/bin/env python3
"""
load_lesson_content_batch2.py
Run from pc-license-prep-server-v2/ directory:
    .venv/bin/python3 scripts/load_lesson_content_batch2.py

Adds real lesson content for:
- Property Fundamentals (remaining lessons)
- Casualty Fundamentals (all lessons)
- Personal Auto Insurance (all lessons)
- Homeowners Insurance (all lessons)

Safe to re-run — skips lessons already over 300 chars.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_all
from app.models import Lesson
from sqlalchemy import select

LESSON_CONTENT = {

# ═══════════════════════════════════════════════════════════════════════
# MODULE 3 — PROPERTY FUNDAMENTALS (remaining lessons)
# ═══════════════════════════════════════════════════════════════════════

"direct-vs-indirect-loss": (
    """Property insurance distinguishes between two types of losses that flow from a covered peril, and the distinction determines which part of the policy responds.

A direct loss is the immediate, physical damage caused by the covered peril itself. When fire burns a building, the structural damage is the direct loss. When a thief breaks a window and steals merchandise, the broken window and the stolen goods are direct losses. Direct losses are covered under the property coverage (Coverage A for the dwelling, Coverage C for personal property, or the Building and Personal Property form for commercial accounts).

An indirect loss (also called a consequential loss) is a financial loss that flows as a consequence of the direct loss. The classic examples are lost rental income when a damaged building cannot be rented out, and additional living expenses when a damaged home is uninhabitable. These losses do not involve physical damage to property — they are financial consequences of physical damage.

The distinction matters because standard property policies cover direct losses but do NOT automatically cover indirect losses. Additional coverages or separate policy provisions are needed for indirect losses. A homeowners policy includes a limited amount of additional living expense coverage (Coverage D) as a built-in indirect loss protection. A commercial property policy may include business income coverage for the same reason.

For the exam, always identify whether a described loss is physical (direct) or financial/consequential (indirect). If someone asks whether a property policy covers lost profits after a fire destroys a store, the answer is: not under the basic property coverage — business income coverage is needed. If they ask about the cost to repair the fire damage itself, that is covered under the property form.
""",
    "A direct loss is physical damage from the peril itself; an indirect loss is a financial consequence flowing from the direct loss.",
    "A fire destroys a restaurant's kitchen (direct loss — covered under property). The restaurant closes for three months while repairs are made, losing $60,000 in revenue (indirect loss — requires business income coverage).",
    "Direct = the physical damage. Indirect = the money lost because of that damage. Property covers direct. Business income covers indirect."
),

"named-vs-open-perils": (
    """One of the most fundamental distinctions in property insurance is whether a policy is written on a named perils or open perils basis. This distinction determines which losses are covered and who bears the burden of proof in a claim.

A named perils policy covers only the specific perils (causes of loss) listed in the policy. Common named perils include fire, lightning, windstorm, hail, explosion, smoke, vandalism, theft, and water damage from plumbing. If a loss is caused by a peril not on the list, the claim is denied — regardless of how unexpected or damaging the loss was. The insured bears the burden of proving the loss was caused by a listed peril.

An open perils policy (also called special form or all-risk coverage) covers all causes of loss EXCEPT those specifically excluded. Rather than listing what is covered, the policy lists what is NOT covered. Standard exclusions include flood, earthquake, intentional acts, normal wear and tear, and government action. If a loss occurs and the cause is not listed as an exclusion, it is covered. The insurer bears the burden of proving a loss falls within an exclusion to deny a claim.

Open perils coverage is broader than named perils coverage because it covers unexpected, unusual causes of loss that might not be listed in a named perils form — a raccoon chewing through a water pipe, for example, would not be on any named perils list but would be covered under open perils.

For the exam, know that the homeowners HO-3 form provides open perils coverage on the dwelling (Coverage A) but named perils on personal property (Coverage C). The commercial property special form provides open perils on the building and business personal property. This hybrid approach appears frequently on exam questions.
""",
    "Named perils policies cover only listed perils; open perils policies cover all perils except those specifically excluded.",
    "A pipe freezes and bursts during a cold snap, damaging floors and walls. Under a named perils policy, coverage depends on whether 'freezing of plumbing' is listed. Under open perils, it is automatically covered unless freezing is specifically excluded.",
    "Named = must be on the list to be covered. Open = covered unless excluded. Named = insured proves the peril. Open = insurer proves the exclusion."
),

"property-coverage-forms": (
    """Property insurance policies are built from standardized coverage forms developed by the Insurance Services Office (ISO). Understanding the three main cause-of-loss forms — basic, broad, and special — is essential for the exam.

The Basic Form is the most restrictive. It covers a specific list of named perils: fire, lightning, explosion, windstorm or hail, smoke, aircraft, vehicles, riot or civil commotion, vandalism, sprinkler leakage, sinkhole collapse, and volcanic action. If the cause of loss is not on this short list, the basic form does not respond.

The Broad Form adds several perils to the basic form list, most importantly: falling objects, weight of snow/ice/sleet, water damage from plumbing, and collapse from specified causes. The broad form is still a named perils form — coverage remains limited to the listed perils.

The Special Form (open perils or all-risk) is the most comprehensive. It covers all causes of loss except those specifically excluded. Common exclusions include flood, earthquake, ordinance or law, earth movement, and intentional acts. The special form is what most commercial property buyers want because it eliminates coverage gaps from unexpected causes.

In the homeowners line, the three forms correspond roughly to HO-1 (basic), HO-2 (broad), and HO-3 (special for dwelling, broad for personal property). HO-5 provides open perils on both the dwelling AND personal property — the broadest homeowners form available.

For the exam, be prepared to identify which form applies to a described scenario and which form would cover or exclude a specific cause of loss. The typical question: "A building insured on the basic form is damaged by falling ice from a neighboring building. Is the loss covered?" Under basic form, no — falling objects is not a listed peril. Under broad or special form, yes.
""",
    "The three cause-of-loss forms — basic (named perils), broad (more named perils), and special (open perils) — determine which causes of loss trigger coverage.",
    "A retail store insured on the broad form has its roof collapse under accumulated snow weight. Covered — weight of ice/snow is one of the broad form additions. Under the basic form, it would not be covered.",
    "Basic = short list. Broad = longer list. Special = everything except exclusions. More coverage = higher premium. HO-3 = special for dwelling, broad for personal property."
),

"additional-coverages": (
    """Most property policies include additional coverages — limited coverages that extend beyond the core property protection, often at no extra premium. These appear frequently on exams because they represent coverage that exists automatically, without the insured needing to request it.

Debris removal coverage pays the cost to remove debris of covered property after a covered loss. If a fire destroys part of a building, the cost to haul away the charred remains is covered in addition to (not as part of) the building damage payment. Debris removal is typically limited to a percentage of the loss amount (often 25%) or a flat dollar amount.

Preservation of property covers the cost to move covered property to safety to protect it from an impending covered loss. If a wildfire is approaching and the insured rents a truck to evacuate equipment, that cost may be covered. Coverage typically applies for a limited period (often 30 days) after the property is moved.

Fire department service charges covers the fee charged by a fire department that responds to a fire on the insured's property. Some municipalities charge for fire suppression services; this additional coverage pays those bills.

Pollutant cleanup and removal covers the cost to extract pollutants from land or water caused by a covered loss. If a fire causes a chemical spill, the cleanup cost is covered as an additional coverage.

Collapse coverage under the broad and special forms covers sudden collapse caused by specified causes — hidden decay, hidden insect damage, weight of contents, and similar factors. Collapse from normal settling or deterioration is not covered.

For the exam, remember that additional coverages are automatic (no endorsement needed) but limited in scope and dollar amount. They exist in addition to — not instead of — the primary coverage limits.
""",
    "Additional coverages automatically extend property policies to include debris removal, preservation of property, fire department charges, and other limited protections.",
    "After a fire destroys a warehouse, the insurer pays $200,000 for the building damage and an additional $18,000 for debris removal — the debris removal is a separate additional coverage, not taken from the building limit.",
    "Additional coverages = bonus protection at no extra cost, but always limited. Know them: debris removal, preservation, fire dept charges, pollutant cleanup, collapse."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 4 — CASUALTY FUNDAMENTALS (all lessons)
# ═══════════════════════════════════════════════════════════════════════

"liability-basics": (
    """Liability insurance covers the insured's legal obligation to pay damages to others because of bodily injury or property damage the insured caused. Understanding the basic structure of liability coverage is essential before studying specific liability policies.

Liability exposure arises whenever the insured's actions (or failure to act) create a legal obligation to compensate another party. The most common basis is negligence — the failure to exercise reasonable care. Other bases include strict liability (liability without fault, common in products liability and certain hazardous activities) and intentional torts (deliberate harmful acts, which are generally excluded from insurance).

A liability insurance policy has two key components: the duty to defend and the duty to indemnify. The duty to defend is broader — the insurer must provide a legal defense whenever a claim is made that could potentially be covered by the policy, even if the claim is ultimately proven groundless, false, or fraudulent. Defense costs are typically paid in addition to the policy limits (supplementary payments), not subtracted from them.

The duty to indemnify is the obligation to pay damages the insured is legally obligated to pay, up to the policy limits. Indemnity requires an actual legal liability — a finding (by judgment or settlement) that the insured is legally responsible for the harm.

Policy limits in liability insurance can be structured as a single (combined single limit) covering all types of claims in a single amount, or as split limits with separate amounts for each type of loss (per person bodily injury / per occurrence bodily injury / property damage). Aggregate limits cap total payments across all claims during the policy period.

For the exam, always remember: the duty to defend is triggered by allegations; the duty to indemnify is triggered by proven legal liability. Defense costs are supplementary (outside the limit). The insurer controls the defense — the insured cannot independently hire attorneys or admit liability without the insurer's consent.
""",
    "Liability insurance covers the insured's legal obligation to pay damages to others, with both a duty to defend and a duty to indemnify.",
    "A visitor trips on a cracked sidewalk and sues the homeowner for $80,000. The insurer provides a defense attorney (duty to defend) and, if a judgment or settlement is reached, pays the amount owed up to the policy limit (duty to indemnify).",
    "Duty to defend = triggered by allegations, even groundless ones. Duty to indemnify = triggered by proven legal liability. Defense costs are outside the limit. Insurer controls the defense."
),

"liability-exclusions": (
    """Liability policies exclude certain categories of claims because they are either uninsurable, covered elsewhere, or present moral hazard concerns. Knowing the most common exclusions helps you identify when coverage applies and when it does not.

The intentional acts exclusion removes coverage for harm the insured deliberately caused. Insurance exists to cover accidental losses — not to fund intentional wrongdoing. An insured who deliberately strikes someone cannot collect under their liability policy for the resulting injury claim. Note that the severability of interests (separation of insureds) provision means this exclusion only applies to the insured whose act was intentional — other innocent insureds may retain coverage.

The workers compensation exclusion removes coverage for bodily injury to the insured's employees arising out of their employment. This exposure belongs under workers compensation and employers liability insurance, not general liability. The CGL is designed for third-party (non-employee) liability.

The contractual liability exclusion removes coverage for liability the insured assumed under a contract — EXCEPT for liability assumed in an insured contract (hold harmless agreements in certain written contracts). This exception is important in construction where subcontractors routinely assume the general contractor's liability.

The care, custody, and control exclusion removes coverage for damage to property in the insured's possession. A repair shop that damages a customer's car while working on it cannot collect under its CGL — the car was in the shop's care, custody, and control. Garagekeepers legal liability provides this coverage for auto-related businesses.

The pollution exclusion in modern CGL policies is absolute — it excludes virtually all pollution-related claims. Separate environmental liability policies exist for this exposure.

For the exam, the most frequently tested exclusions are intentional acts, workers compensation, care/custody/control, and contractual liability. Practice identifying which exclusion applies to a given scenario.
""",
    "Liability policies exclude intentional acts, employee injuries, contractual liability, property in the insured's care, and pollution.",
    "A painting contractor spills paint on a customer's expensive hardwood floor. The CGL denies the claim under the care, custody, and control exclusion — the floor was in the contractor's care when damaged. The contractor needs a separate inland marine bailee policy.",
    "Intentional = excluded. Employee injury = WC instead. Contract liability = excluded except insured contracts. Care/custody/control = excluded. Pollution = absolute exclusion."
),

"damages-types": (
    """When someone is found liable for causing harm, the court may award several types of damages. Insurance policies are specifically designed around these categories, and the exam tests whether you know which types of damages are covered.

Compensatory damages are the most common — they compensate the plaintiff for actual losses suffered. Compensatory damages have two subcategories. Special damages (also called economic damages) are quantifiable financial losses: medical bills, lost wages, property repair costs, and future earnings lost due to permanent disability. These are calculated with reasonable precision. General damages (also called non-economic damages) compensate for harm that is real but harder to quantify: pain and suffering, emotional distress, loss of consortium, and disfigurement.

Punitive damages (also called exemplary damages) are awarded not to compensate the plaintiff but to punish the defendant for particularly egregious, reckless, or malicious conduct and to deter similar behavior. Most liability policies exclude or severely limit punitive damages coverage because insuring punitive damages is contrary to public policy in many states — the punishment loses its deterrent effect if insurance pays it.

Nominal damages are a small, token award (often $1) when the plaintiff proves a legal violation but cannot demonstrate significant actual harm.

For the exam, the key distinction is between compensatory (designed to make the plaintiff whole) and punitive (designed to punish the defendant). Standard liability policies cover compensatory damages — bodily injury and property damage caused by the insured. Punitive damages coverage varies by policy and state; some policies expressly exclude them.

Also know that defense costs — attorney fees, court costs, and similar expenses — are typically covered by liability policies as supplementary payments, outside and in addition to the policy's indemnity limits.
""",
    "Liability insurance covers compensatory damages (special and general) arising from covered claims, with punitive damages often excluded.",
    "A contractor is sued for flooding a neighbor's basement. The court awards $15,000 for property damage (special damages), $5,000 for the neighbor's stress and inconvenience (general damages), and $50,000 in punitive damages for deliberately ignoring warnings. The liability policy covers $20,000; the punitive award may not be covered.",
    "Compensatory = making the plaintiff whole (special = economic, general = non-economic). Punitive = punishment, often excluded. Defense costs = supplementary payments outside the limit."
),

"umbrella-liability": (
    """Umbrella and excess liability policies provide an additional layer of protection above the limits of underlying liability policies. They are essential for individuals and businesses whose exposure exceeds the limits of standard liability policies.

An umbrella policy has two key features that distinguish it from a simple excess policy. First, it provides excess coverage over the underlying policy limits — when the underlying policy is exhausted, the umbrella continues to pay up to its own limits. Second, most umbrellas also provide drop-down coverage for certain claims that fall outside the underlying policy's coverage but within the umbrella's coverage. This drop-down coverage fills gaps, subject to a self-insured retention (SIR) — essentially a large deductible the insured pays before the umbrella responds to unscheduled claims.

Underlying insurance requirements are a critical condition. The umbrella insurer requires the insured to maintain specific minimum limits on underlying policies (auto liability, CGL, employers liability). If the insured fails to maintain these underlying limits and a loss occurs, the umbrella insurer treats the underlying coverage as if it were in place at the required limit — meaning the insured pays the gap out of pocket.

Excess liability policies are simpler than umbrellas — they sit on top of a specific underlying policy and provide additional limits, but they do not provide drop-down coverage and do not cover claims not covered by the underlying policy.

For the exam, know that umbrella policies require maintenance of underlying limits, have a retained limit (SIR) for drop-down coverage, and are broader than simple excess policies. The umbrella responds after the underlying policy is exhausted; the SIR applies to covered claims that the underlying policy does not reach.
""",
    "Umbrella policies provide excess coverage above underlying policy limits and drop-down coverage for certain gaps, subject to a self-insured retention.",
    "A business carries $1,000,000 CGL limit and a $5,000,000 umbrella. A $2,500,000 judgment exceeds the CGL limit. The CGL pays $1,000,000; the umbrella pays the remaining $1,500,000.",
    "Umbrella = excess above underlying + drop-down for gaps. Requires maintaining underlying limits. SIR = the umbrella's deductible for unscheduled claims. Excess = only adds limits, no drop-down."
),

"professional-liability": (
    """Professional liability insurance (also called errors and omissions, or E&O) covers claims arising from the negligent performance of professional services. It fills a critical gap in the CGL, which excludes professional services from its coverage.

Standard CGL policies exclude bodily injury and property damage arising from the rendering or failure to render professional services. A doctor, lawyer, accountant, architect, or insurance agent whose professional advice causes harm to a client needs a separate professional liability policy.

Professional liability claims are almost always written on a claims-made basis. This is because professional negligence claims often surface years after the alleged error — a lawyer's negligent advice might not result in a lawsuit for several years. Claims-made coverage ensures the policy in force when the claim is made (rather than when the error occurred) responds.

Because claims-made policies can leave gaps when coverage is discontinued, professionals need either an extended reporting period (tail coverage) when they retire or change insurers, or prior acts coverage (nose coverage) when a new claims-made policy is purchased. Tail coverage extends the reporting window after the policy terminates; nose coverage extends backward to pick up claims from acts that predated the new policy.

Insurance agents and brokers carry E&O insurance to protect against claims that they failed to procure proper coverage, gave incorrect advice, or failed to inform a client of a coverage gap. An agent who tells a client they are covered for flood (when they are not) faces an E&O claim if a flood loss occurs and the insurer denies the claim.

For the exam, know that professional liability covers negligent professional acts, is almost always claims-made, and requires tail coverage when discontinued to avoid a coverage gap.
""",
    "Professional liability (E&O) insurance covers negligent professional acts that cause financial harm to clients — a gap not covered by the CGL.",
    "An insurance agent fails to add an umbrella policy the client requested. The client suffers a $1.5M judgment that exceeds their $1M auto policy. The agent faces an E&O claim for the $500,000 gap they failed to cover.",
    "E&O = professional negligence. Claims-made basis. CGL excludes professional services. Need tail (extended reporting) when policy ends to protect against late-surfacing claims."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 5 — PERSONAL AUTO INSURANCE (all lessons)
# ═══════════════════════════════════════════════════════════════════════

"pap-overview": (
    """The Personal Auto Policy (PAP) is the standard policy form used for personal auto insurance throughout the United States. It is developed by the Insurance Services Office (ISO) and contains four distinct coverage parts, each addressing a different aspect of automobile-related risk.

Part A — Liability Coverage protects the insured against legal liability for bodily injury and property damage caused to others in an auto accident. It includes both the duty to defend (paying legal costs) and the duty to indemnify (paying damages). Liability coverage is required by law in virtually every state at minimum limits.

Part B — Medical Payments Coverage (or Personal Injury Protection in no-fault states) pays medical expenses for the insured and passengers injured in an accident, regardless of fault. Medical Payments is secondary to health insurance in most cases and applies to the insured as a pedestrian struck by a vehicle as well.

Part C — Uninsured/Underinsured Motorist Coverage (UM/UIM) protects the insured when they are injured by a driver with no insurance (UM) or insufficient insurance (UIM). It fills the gap left when the at-fault party cannot pay the full damages.

Part D — Coverage for Damage to Your Auto covers physical damage to the insured's own vehicle through two sub-coverages: collision (damage from striking another vehicle or object, or rollover) and comprehensive/other-than-collision (damage from non-collision events like theft, fire, hail, or animal strikes).

The PAP also contains several general provisions: the definitions section, the duties after an accident (notice, cooperation), the policy period, and the termination provisions.

For the exam, be able to identify which Part applies to a described claim. The key questions: Was someone else hurt? (Part A). Was the insured hurt? (Part B or C). Was the insured's car damaged? (Part D).
""",
    "The PAP has four parts: Liability (A), Medical Payments (B), UM/UIM (C), and Physical Damage (D).",
    "An insured runs a red light, injuring a pedestrian (Part A responds). The insured is also injured in the crash (Part B). Their car is totaled (Part D — collision). A week later, they are hit by an uninsured driver (Part C).",
    "Parts A B C D: A = your fault/others hurt, B = you're hurt, C = uninsured hit you, D = your car damaged. Think: A=At-fault, B=Body (yours), C=Can't-pay driver, D=Damage to your car."
),

"pap-liability": (
    """Part A of the PAP — Liability Coverage — is the most important coverage from a financial protection standpoint and the most heavily tested on the exam. It protects the insured against claims from others arising out of auto accidents.

Covered persons under Part A include the named insured and family members while using any auto, any person using the named insured's covered auto with permission (permissive use), and any person or organization legally responsible for the use of a covered auto on behalf of the named insured.

The permissive use rule is critical: coverage follows the vehicle. A person who borrows your car with your permission is covered under your PAP as a permissive user — even if they have their own insurance. Your PAP is primary; their policy is excess.

Policy limits for liability can be structured as a combined single limit (one amount for all liability claims per accident) or split limits. Split limits are expressed as three numbers — for example, 25/50/25 — meaning $25,000 per person for bodily injury, $50,000 per occurrence for all bodily injury claims, and $25,000 for property damage.

Several important exclusions apply to Part A: intentional injury, bodily injury to an employee of the insured (covered by workers compensation), property damage to property the insured owns or is renting, use of a vehicle as a public livery conveyance (Uber/Lyft/delivery use), and liability arising from a vehicle being used in a business (other than cars, private passenger vans, or pickups).

Supplementary payments — additional payments the insurer makes on top of the liability limit — include bail bonds up to $250, premiums for appeal bonds, costs of interest accruing after judgment, and loss of earnings up to $200 per day while assisting in the insurer's investigation.
""",
    "PAP Part A covers liability to others for bodily injury and property damage caused by the insured's use of a covered auto.",
    "A named insured loans their car to a college-age neighbor (with permission). The neighbor runs a stop sign and causes $35,000 in injuries to another driver. The named insured's PAP Part A covers the claim — permissive use is covered.",
    "Coverage follows the car. Permissive user = covered. Split limits: BI per person / BI per occurrence / PD. Exclusions: intentional acts, employee injuries, business use, public livery."
),

"pap-physical-damage": (
    """Part D of the PAP covers physical damage to the insured's own vehicle. It contains two distinct sub-coverages with important differences in what they cover and how deductibles apply.

Collision coverage pays for damage to the covered auto resulting from collision with another vehicle or object, or from the vehicle's overturn (rollover). Fault is irrelevant for collision — it pays regardless of who caused the accident. However, if the insured was not at fault, the insurer may pursue subrogation against the responsible party. Collision has a deductible that applies per loss.

Comprehensive coverage (also called Other-Than-Collision or OTC) pays for damage to the covered auto from causes other than collision. Covered causes include theft, fire, explosion, earthquake, flood, hail, windstorm, vandalism, falling objects, contact with an animal, and more. Comprehensive also has a deductible, though it is often lower than the collision deductible.

One key distinction: theft of the vehicle is covered under comprehensive. But theft of items from inside the vehicle (GPS unit, briefcase) is not covered under the PAP — personal property inside the car is covered under the homeowners or renters policy (Coverage C), not the auto policy.

Actual cash value (ACV) is the standard valuation for Part D losses — the insurer pays what the vehicle was worth at the time of loss, minus the deductible. On a total loss (when repair cost exceeds ACV), the insurer pays the ACV of the vehicle.

Transportation expense coverage (rental reimbursement) is an optional additional coverage that pays for a rental car while the insured's vehicle is being repaired after a covered Part D loss.

For the exam, know which losses are collision versus comprehensive — this distinction appears in multiple questions. Also know that ACV applies at the time of loss.
""",
    "PAP Part D covers physical damage to the insured's vehicle: collision covers impact losses; comprehensive covers non-collision losses like theft, fire, and hail.",
    "A hailstorm damages a car's roof and hood ($4,000 in damage) — comprehensive. The same car is rear-ended the following week ($2,500 in damage) — collision. Each loss has its own separate deductible.",
    "Collision = hitting something or overturning. Comprehensive = everything else (theft, weather, animals, fire). ACV at time of loss. Theft of items inside the car = homeowners, not auto."
),

"no-fault-insurance": (
    """No-fault auto insurance is a system where each driver's own insurance pays for their own injuries after an accident, regardless of who was at fault. It was developed in the 1970s to reduce the number of small liability lawsuits clogging courts and to speed up claims payments.

In no-fault states, drivers purchase Personal Injury Protection (PIP) coverage as a required part of their auto insurance. PIP pays for the policyholder's medical expenses, lost wages, replacement services (like hiring someone to clean the house if the insured is hospitalized), and sometimes funeral expenses — without regard to fault. PIP payments are made quickly, without waiting for a fault determination.

In exchange for the speed and certainty of PIP benefits, no-fault states restrict the insured's right to sue the at-fault driver for pain and suffering. Lawsuits are typically permitted only when injuries exceed a defined threshold — either a monetary threshold (medical bills exceed a certain dollar amount) or a verbal threshold (injuries meet a specific severity level like permanent disability, disfigurement, or death).

Pure no-fault states (very few) completely eliminate lawsuits for minor accidents. Most states use a modified no-fault approach where lawsuits are permitted above the threshold.

The exam distinguishes between Medical Payments coverage (available in all states, no-fault optional) and PIP (required in no-fault states, broader coverage including lost wages). Med Pay covers only medical bills; PIP covers a broader range of economic losses.

States that do not have no-fault systems are called tort states or traditional states. In these states, the at-fault driver's liability insurance pays for all injured parties' damages.
""",
    "In no-fault states, PIP coverage pays the insured's own injury costs regardless of fault, in exchange for limited rights to sue.",
    "In a no-fault state, two drivers collide. Each driver's own PIP pays their medical bills immediately — no fault determination needed. Neither can sue for pain and suffering unless injuries meet the state threshold.",
    "No-fault = your own insurance pays your injuries. PIP = broader than Med Pay (adds lost wages, services). Trade-off: faster payment but limited right to sue. Not all states are no-fault."
),

"auto-insurance-requirements": (
    """Every state in the United States requires minimum auto liability insurance (or a financial responsibility equivalent) for registered vehicles. Understanding the structure and purpose of these requirements is tested on the exam.

Financial responsibility laws require drivers to demonstrate they can pay for damages they cause in an accident. Most states satisfy this through compulsory insurance — requiring all registered vehicles to carry minimum liability insurance as a condition of registration.

Minimum limits vary significantly by state. Many states use low minimums like 25/50/25 ($25,000 per person BI, $50,000 per occurrence BI, $25,000 PD). These minimums are often inadequate for serious accidents — a $25,000 per-person limit may not cover the full medical bills from a serious injury. This is why umbrella policies and higher liability limits are important.

The financial responsibility requirement exists to ensure that at-fault drivers can compensate their victims. Without it, injured parties would have no recovery against uninsured drivers — leaving the victim to bear costs that were caused by someone else.

Proof of insurance requirements typically include providing insurance information at the scene of an accident, to law enforcement on request, and to the DMV for vehicle registration. Electronic proof of insurance (showing an app on a smartphone) is now accepted in most states.

Uninsured motorist statistics remain significant despite mandatory insurance laws — estimates suggest that 12-13% of drivers carry no insurance at any given time. This is why UM/UIM coverage is so important even in states with mandatory insurance requirements.

For the exam, know that financial responsibility laws are state-mandated and that liability coverage is the required component — not comprehensive or collision, which remain optional.
""",
    "All states require minimum auto liability coverage to ensure drivers can pay for damages they cause — but minimums are often inadequate for serious accidents.",
    "A state requires 25/50/25 minimum limits. A serious accident results in $100,000 in injuries to one person. The at-fault driver's minimum policy pays only $25,000 — the victim must pursue the driver personally for the $75,000 gap.",
    "Financial responsibility = prove you can pay. Compulsory insurance = most states. Minimums = often inadequate. Liability required; collision/comprehensive optional. UM covers the gap left by uninsured drivers."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 6 — HOMEOWNERS INSURANCE (all lessons)
# ═══════════════════════════════════════════════════════════════════════

"homeowners-overview": (
    """Homeowners insurance is a package policy — it combines multiple coverages that would otherwise require separate policies into a single, convenient contract. The standard homeowners policy contains property coverage, liability coverage, and medical payments coverage all in one form.

The Insurance Services Office (ISO) has developed a series of homeowners forms designated by number. The HO-2 (broad form) covers the dwelling and personal property on a named perils basis. The HO-3 (special form) is the most common homeowners policy — it covers the dwelling on an open perils basis (all causes of loss except exclusions) but covers personal property on a named perils basis. The HO-5 (comprehensive form) covers both the dwelling and personal property on an open perils basis — the broadest coverage available. The HO-4 is the renters insurance form (covers personal property and liability but not the building). The HO-6 is for condominium unit owners (covers personal property, improvements to the unit, and liability). The HO-8 is for older homes where the standard replacement cost approach would result in significant improvement over original construction.

The homeowners policy is organized into Section I (property coverages) and Section II (liability coverages). Section I contains Coverage A (Dwelling), Coverage B (Other Structures), Coverage C (Personal Property), and Coverage D (Loss of Use). Section II contains Coverage E (Personal Liability) and Coverage F (Medical Payments to Others).

For the exam, the most important forms to know are HO-3 (most common homeowners), HO-4 (renters), and HO-6 (condo). Know which coverage applies to which type of property, and know the open/named perils distinction between the dwelling and personal property under HO-3.
""",
    "Homeowners insurance is a package policy combining property, liability, and medical payments coverage into one form, with several versions for different housing situations.",
    "A homeowner with an HO-3 is covered for: fire damage to their house (Coverage A — open perils), theft of their TV (Coverage C — named perils), and a lawsuit when a visitor breaks a leg on their steps (Coverage E — personal liability).",
    "HO-3 = most common, open perils on dwelling/named perils on contents. HO-4 = renters. HO-6 = condo. Section I = property. Section II = liability. Package policy = everything in one."
),

"homeowners-property-coverages": (
    """Section I of the homeowners policy contains four property coverages, each addressing a different aspect of the homeowner's property exposure.

Coverage A — Dwelling covers the residential structure at the described premises, including attached structures (garages, decks, patios connected to the main structure) and permanently installed fixtures and systems. Under HO-3, the dwelling is covered on an open perils basis — all causes of loss except those specifically excluded. Coverage A is typically written on a replacement cost basis.

Coverage B — Other Structures covers structures on the residence premises that are separated from the dwelling by clear space — detached garages, fences, storage sheds, swimming pools, and similar structures. Coverage B is typically set at 10% of Coverage A limits automatically, though it can be increased. Structures used for business or rented to others (with limited exceptions) are excluded.

Coverage C — Personal Property covers the contents of the home — furniture, clothing, appliances, electronics, and similar items. Under HO-3, personal property is covered on a named perils basis (not open perils). Coverage C protects the insured's personal property worldwide — on vacation, in storage, or at a secondary location — though coverage away from the premises is typically limited to 10% of Coverage C.

Special limits of liability apply to certain categories of personal property that are particularly susceptible to theft or are difficult to value: money and precious metals, jewelry, firearms, silverware, securities, and business property each have sublimits (commonly $200-$2,500 depending on the item). Scheduled personal property endorsements can provide higher limits for these items.

Coverage D — Loss of Use covers additional living expenses when a covered loss makes the home uninhabitable. It pays the extra cost (above normal living expenses) to maintain the standard of living while repairs are made — hotel bills, restaurant meals above normal food costs, etc.
""",
    "Homeowners Section I provides: Coverage A (dwelling), Coverage B (other structures), Coverage C (personal property), and Coverage D (additional living expenses).",
    "A kitchen fire damages the home (Coverage A) and destroys the detached garage (Coverage B). The family stays in a hotel while repairs are made (Coverage D). Their furniture and appliances are also damaged (Coverage C).",
    "A B C D: Attached structure, Beside (detached), Contents, Days away. Coverage B = 10% of A. Coverage C = named perils, worldwide but limited off-premises. Special limits for jewelry, cash, firearms."
),

"homeowners-liability": (
    """Section II of the homeowners policy provides liability protection for the insured and family members — protection that follows them wherever they go, not just at the insured premises.

Coverage E — Personal Liability covers the named insured and resident family members for their legal liability for bodily injury or property damage caused to others through personal (non-business) activities. Coverage E has no per-claim deductible — it pays from the first dollar. The standard limit is $100,000 per occurrence, though higher limits (up to $500,000 or more) are available and advisable.

The personal liability under Coverage E follows the insured — it covers incidents at home, at a neighbor's house, on the golf course, or virtually anywhere in the world. This is broader than many insureds realize.

Coverage F — Medical Payments to Others is a no-fault coverage that pays medical expenses for guests injured at the insured's premises or by the insured's activities away from home — without requiring a finding of liability. It is a goodwill coverage designed to pay small medical claims quickly, avoiding lawsuits. Typical limits are $1,000-$5,000. Coverage F does NOT cover the named insured or household residents — only guests and visitors.

Important exclusions from Section II include: business pursuits (requires a commercial policy), professional services, motor vehicle accidents (covered by auto policies), watercraft above certain size and horsepower limits, and intentional acts.

The homeowners policy's liability section is often overlooked, but it is an essential safety net. A guest who breaks an arm at the insured's home could result in a significant lawsuit. Coverage E defends the insured and pays any judgment up to the policy limit.
""",
    "Homeowners Section II provides personal liability (Coverage E) and medical payments to guests (Coverage F) following the insured in personal activities.",
    "A homeowner's dog bites a mail carrier, resulting in $40,000 in medical bills and a lawsuit. Coverage E provides the defense and pays the settlement. If the bite had only needed a $2,000 ER visit, Coverage F would have paid without a liability finding.",
    "Coverage E = liability to others (follows you anywhere), requires legal liability finding. Coverage F = no-fault medical for guests (no liability needed). Both exclude household members and business activities."
),

"homeowners-exclusions": (
    """The homeowners policy excludes several significant causes of loss that either require separate policies or are considered uninsurable under a standard homeowners form. Understanding these exclusions is critical — both for advising clients and for the exam.

Flood is one of the most significant and misunderstood exclusions. Surface water flooding from heavy rain, overflowing rivers, storm surge, and similar causes is excluded. Homeowners who want flood protection must purchase a separate flood insurance policy through the National Flood Insurance Program (NFIP) or a private flood insurer. Water damage from internal sources (burst pipes, appliance overflow) IS covered under the homeowners policy.

Earthquake and earth movement excludes damage from earthquakes, landslides, sinkholes, and similar earth movement events. Separate earthquake coverage is available as an endorsement or a standalone policy. Note: if an explosion causes earth movement, the explosion is the proximate cause — a covered peril — and the resulting damage is covered.

Ordinance or law exclusion removes coverage for the increased cost of rebuilding to current building codes after a covered loss. If a 1960s home with outdated electrical is destroyed by fire, the cost to rebuild with current code requirements (modern electrical, energy efficiency, etc.) exceeds the replacement cost of the original structure. Without an ordinance or law endorsement, the insured bears this additional cost.

Intentional acts are excluded across all property and liability coverages — the insured cannot profit from deliberate destruction or injury.

Neglect and maintenance are excluded — gradual deterioration, rust, rot, mold (unless from a sudden covered event), and failure to maintain the property are not insured losses.

For the exam, flood and earthquake exclusions are the most tested. Remember: flood requires the NFIP; earthquake requires a separate endorsement or policy.
""",
    "Key homeowners exclusions include flood (NFIP needed), earthquake (endorsement needed), ordinance/law costs, intentional acts, and neglect.",
    "A homeowner's basement floods after a severe rainstorm causes a nearby creek to overflow its banks. The homeowners policy denies the claim — this is flood, a standard exclusion. They needed a separate flood policy through the NFIP.",
    "Flood = NFIP. Earthquake = separate endorsement. Ordinance/law = need endorsement for code upgrades. Intentional = never covered. Maintenance/wear = never covered. Internal water damage (burst pipes) = IS covered."
),

"homeowners-additional-coverages": (
    """The HO-3 homeowners policy includes a set of additional coverages that automatically extend the basic property protection without requiring separate endorsements or additional premium. These are important because they provide meaningful coverage for situations not covered by the four basic coverage letters.

Debris removal coverage pays to haul away the debris of covered property after a loss. If a tree falls on the house (covered), the cost to remove the fallen tree and the demolished wall materials is covered. Note: the cost to remove a tree that fell on the yard (but did not damage the house) may be covered up to a limited amount as a separate provision.

Reasonable repairs coverage reimburses the insured for temporary measures taken to protect property from further damage after a covered loss — boarding up broken windows, applying a tarp to a damaged roof, etc.

Fire department service charge coverage pays up to a specified amount (typically $500) for fees charged by fire departments that respond to fires on the insured's property. Some jurisdictions bill property owners for fire suppression services.

Property removed coverage provides open perils coverage for covered property removed from the premises to protect it from a covered peril for up to 30 days.

Credit card, fund transfer card, forgery, and counterfeit money coverage provides limited protection (typically $500) against unauthorized use of the insured's credit cards, forged checks, or counterfeit currency.

Collapse coverage provides protection against sudden collapse of a building caused by specified causes — hidden decay, hidden insect or vermin damage, weight of people or contents, and similar factors. Normal settling, shrinkage, or deterioration is not collapse under the policy.

Loss assessment coverage helps condominium owners and homeowners in planned communities pay special assessments levied by the association after a covered loss to common property.
""",
    "The HO-3 automatically includes additional coverages for debris removal, reasonable repairs, fire department charges, property removed, credit card fraud, and collapse.",
    "After a windstorm tears off part of a roof, the homeowner immediately pays $800 for an emergency tarp to prevent interior water damage (reasonable repairs — covered). The fire department responds and sends a $500 bill (fire department service charge — covered).",
    "Additional coverages = automatic, no endorsement needed. Debris removal, temporary repairs, fire dept charges, collapse, credit card fraud. All limited in dollar amount but important for real-world claims."
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
