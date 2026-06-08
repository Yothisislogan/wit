#!/usr/bin/env python3
"""
load_questions_batch3.py
Run from pc-license-prep-server-v2/ directory:
    .venv/bin/python3 scripts/load_questions_batch3.py

Adds 70 additional real P&C licensing exam questions (5 per module, 14 modules).
Batch 3 focuses on harder scenario questions and exam-edge concepts.
Does NOT delete existing questions — appends to the current bank.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_all
from app.models import Module, Lesson, Question, AnswerChoice
from sqlalchemy import select, func

BATCH3_QUESTIONS = {

"insurance-basics": [
    (
        "A morale hazard differs from a moral hazard in that:",
        "multiple_choice", "standard",
        "A moral hazard involves intentional dishonesty or fraud. A morale hazard involves carelessness or indifference — the insured doesn't intend to cause a loss but is less careful because they know they are covered.",
        [
            ("A morale hazard involves indifference or carelessness due to having insurance; a moral hazard involves intentional dishonesty.", True, "Correct. Morale = careless attitude; moral = intentional bad acts."),
            ("A moral hazard involves carelessness; a morale hazard involves fraud.", False, "This reverses the definitions. Moral hazard = dishonesty; morale hazard = carelessness."),
            ("Both terms describe the same concept with different spellings.", False, "They are distinct concepts — morale and moral hazards are defined differently."),
            ("A morale hazard only applies to life insurance; a moral hazard applies to property insurance.", False, "Both types of hazards apply across all lines of insurance."),
        ]
    ),
    (
        "An insured deliberately sets fire to their own warehouse to collect the insurance proceeds. The insurer will:",
        "scenario", "hard",
        "Intentional acts are excluded from all property insurance policies. An insured cannot profit from their own deliberate wrongdoing. The insurer will deny the claim and may refer the matter for criminal prosecution.",
        [
            ("Deny the claim because intentional losses are excluded.", True, "Correct. Intentional destruction by the insured voids coverage under the policy's intentional acts exclusion."),
            ("Pay the claim because the insured owns the property.", False, "Owning the property does not entitle the insured to collect on intentional losses."),
            ("Pay 50% of the claim under the comparative fault doctrine.", False, "Comparative fault applies to liability claims, not intentional property destruction by the policyholder."),
            ("Pay the claim but cancel the policy at renewal.", False, "The insurer will deny the claim entirely — not pay it and cancel later."),
        ]
    ),
    (
        "The 'principle of utmost good faith' places a higher duty of disclosure on insurance applicants than on parties to ordinary commercial contracts because:",
        "multiple_choice", "hard",
        "In insurance, the insurer cannot inspect every risk in detail before agreeing to insure it. The insurer relies heavily on the applicant's representations. This information asymmetry justifies the higher duty of disclosure.",
        [
            ("The insurer relies on the applicant's knowledge of the risk since it cannot independently verify all material facts.", True, "Correct. Information asymmetry between insured and insurer justifies the heightened duty."),
            ("Insurance contracts involve larger sums of money than most commercial contracts.", False, "The amount of money involved does not determine the standard of disclosure required."),
            ("Insurance is a regulated industry subject to stricter legal standards.", False, "Regulation is a separate matter from the contractual duty of utmost good faith."),
            ("The applicant is always represented by a licensed agent who verifies all facts.", False, "Agents verify what they can, but the applicant's duty of disclosure exists regardless of agent involvement."),
        ]
    ),
    (
        "Reinsurance is best described as:",
        "multiple_choice", "standard",
        "Reinsurance is insurance purchased by an insurer from another insurer (the reinsurer) to spread risk. It allows insurers to take on more risk than they could safely retain alone.",
        [
            ("Insurance purchased by an insurer to transfer a portion of its risk to another insurer.", True, "Correct. Reinsurance is essentially insurance for insurance companies."),
            ("Insurance purchased by large corporations to cover risks too big for standard policies.", False, "This describes excess and surplus lines, not reinsurance."),
            ("A government-backed program that guarantees insurer solvency.", False, "Government solvency guarantees are handled by state guaranty funds, not reinsurance."),
            ("A second policy purchased by an insured when the first policy's limits are insufficient.", False, "This describes excess or umbrella coverage, not reinsurance."),
        ]
    ),
    (
        "A physical hazard is best illustrated by which of the following?",
        "scenario", "standard",
        "A physical hazard is a tangible condition of the property or person that increases the likelihood or severity of a loss — such as a building's construction type, condition, or location.",
        [
            ("A building with defective electrical wiring that increases the probability of fire.", True, "Correct. Defective wiring is a physical condition that directly increases fire risk."),
            ("An insured who plans to burn down their business to collect insurance proceeds.", False, "Planning fraud is a moral hazard, not a physical hazard."),
            ("An insured who stops locking their doors because they have theft coverage.", False, "Reduced care due to having insurance is a morale hazard."),
            ("A dense population in an area that increases the number of potential claimants.", False, "Population density is an underwriting consideration, not a physical hazard of the insured property."),
        ]
    ),
],

"insurance-contracts": [
    (
        "An insurance policy is considered a 'conditional contract' because:",
        "multiple_choice", "standard",
        "An insurance contract is conditional because the insurer's obligation to pay is conditioned on the insured fulfilling certain duties — such as paying the premium, providing timely notice of loss, and cooperating in the investigation.",
        [
            ("The insurer's duty to pay depends on the insured meeting specific conditions like notice and cooperation.", True, "Correct. Coverage is conditional on the insured performing their contractual obligations."),
            ("The insured can cancel the policy at any time without penalty.", False, "Cancellation rights are a policy provision, not the reason it is called conditional."),
            ("The insurer can change the policy terms at any time during the policy period.", False, "Insurers generally cannot unilaterally change terms mid-policy; that is not what conditional means."),
            ("Coverage only applies if the insured can prove the loss was accidental.", False, "While accidents are generally required, this is not why the contract is called conditional."),
        ]
    ),
    (
        "A producer tells a homeowner that their policy covers flood damage when it does not. The insured later suffers a flood loss. Under the doctrine of estoppel, the insurer may be:",
        "scenario", "hard",
        "Estoppel prevents a party from denying a position they previously asserted when another party relied on that assertion to their detriment. If the insurer's agent misrepresented coverage, the insurer may be estopped from denying the claim.",
        [
            ("Prevented from denying the flood claim if the insured relied on the producer's representation.", True, "Correct. Estoppel may bind the insurer when its agent created a reasonable belief of coverage."),
            ("Able to deny the claim because flood is clearly excluded in the written policy.", False, "While flood is excluded, the doctrine of estoppel may override the written policy when an agent misrepresented coverage."),
            ("Required to pay only 50% of the loss under comparative fault principles.", False, "Estoppel is an all-or-nothing doctrine — it either applies or it does not."),
            ("Protected from paying because producers are independent contractors, not employees.", False, "Whether the producer is an employee or independent contractor affects liability analysis differently; estoppel can still apply."),
        ]
    ),
    (
        "A 'liberalization clause' in an insurance policy means:",
        "multiple_choice", "standard",
        "A liberalization clause provides that if the insurer broadens coverage under the policy form without additional premium, that broadened coverage automatically applies to all existing policies of the same type.",
        [
            ("If the insurer broadens coverage without extra premium, the improvement applies to all existing similar policies.", True, "Correct. Liberalization automatically extends coverage improvements to in-force policies."),
            ("The insured can liberally interpret ambiguous policy language in their favor.", False, "This describes the reasonable expectations doctrine or the contra proferentem rule, not the liberalization clause."),
            ("The insurer can liberally interpret exclusions to deny more claims.", False, "Liberalization benefits the insured by extending coverage, not restricting it."),
            ("The insured is not required to strictly comply with policy conditions.", False, "Policy conditions must still be met; liberalization only addresses coverage breadth."),
        ]
    ),
    (
        "An 'occurrence' policy form differs from a 'claims-made' form in that the occurrence form:",
        "multiple_choice", "standard",
        "An occurrence policy covers events that happen during the policy period regardless of when the claim is filed. Claims-made covers claims reported during the policy period regardless of when the event occurred.",
        [
            ("Covers events occurring during the policy period even if the claim is filed years later.", True, "Correct. Occurrence coverage follows when the injury happened, not when it was reported."),
            ("Requires claims to be reported within 30 days of the policy expiration date.", False, "This describes an extended reporting period requirement for claims-made, not occurrence."),
            ("Only covers claims that are both made and occur during the policy period.", False, "This describes the most restrictive claims-made form, not an occurrence form."),
            ("Provides broader coverage for professional liability than a claims-made form.", False, "Neither form is inherently broader — they differ in the triggering event, not the scope of covered activities."),
        ]
    ),
    (
        "The 'incontestability' clause in an insurance policy provides that:",
        "multiple_choice", "standard",
        "An incontestability clause (common in life insurance but also in some health policies) prevents the insurer from voiding the policy or denying claims based on misrepresentation after the policy has been in force for a specified period (typically 2 years).",
        [
            ("After a specified period, the insurer cannot void the policy based on misrepresentation.", True, "Correct. Incontestability protects the insured from having coverage rescinded after the contestable period expires."),
            ("The insured cannot contest a claim denial after 30 days.", False, "Incontestability restricts the insurer's right to contest, not the insured's."),
            ("The policy cannot be cancelled for any reason after the first year.", False, "Incontestability relates to misrepresentation contestability, not cancellation rights."),
            ("All policy provisions become permanent and cannot be changed after issuance.", False, "Incontestability addresses misrepresentation rescission rights, not general policy modification."),
        ]
    ),
],

"property-fundamentals": [
    (
        "A building is insured for $150,000. After a total loss, the insurer determines the replacement cost is $200,000 and the actual cash value is $120,000. The policy is written on a replacement cost basis. How much does the insurer pay?",
        "scenario", "hard",
        "A replacement cost policy pays the actual cost to repair or replace with like kind and quality, up to the policy limit. The policy limit is $150,000, which is less than the $200,000 replacement cost, so the insurer pays the policy limit.",
        [
            ("$150,000 — the policy limit, since replacement cost exceeds the limit.", True, "Correct. The insurer pays the lesser of the replacement cost or the policy limit."),
            ("$200,000 — the full replacement cost since this is a replacement cost policy.", False, "Replacement cost policies pay up to the policy limit, not unlimited replacement cost."),
            ("$120,000 — the actual cash value, regardless of the policy type.", False, "This is a replacement cost policy; ACV would only apply under an ACV policy."),
            ("$50,000 — the difference between the policy limit and the ACV.", False, "This calculation has no basis in standard property insurance valuation."),
        ]
    ),
    (
        "Under the 'pro rata' cancellation method, a policyholder pays $1,200 for a one-year policy and cancels after 3 months. The return premium is:",
        "scenario", "standard",
        "Pro rata cancellation returns the exact unearned premium — the proportion of the policy period remaining. 9 months remain out of 12, so the return is 9/12 × $1,200 = $900.",
        [
            ("$900 — the exact unearned premium for the remaining 9 months.", True, "Correct. Pro rata = 9/12 × $1,200 = $900."),
            ("$800 — calculated using the short rate penalty for early cancellation.", False, "Short rate applies when the insured cancels; pro rata gives the full unearned premium."),
            ("$300 — the earned premium for the 3 months of coverage used.", False, "$300 is what the insurer earned; $900 is what is returned to the insured."),
            ("$1,200 — the full premium is refunded on cancellation.", False, "Only the unearned (unused) portion is refunded, not the full premium."),
        ]
    ),
    (
        "A 'short rate' cancellation penalty applies when:",
        "multiple_choice", "standard",
        "Short rate cancellation applies when the insured (not the insurer) cancels the policy before expiration. The insured receives less than the full pro rata unearned premium as a penalty for early cancellation, compensating the insurer for policy issuance costs.",
        [
            ("The insured cancels the policy before the expiration date.", True, "Correct. Short rate is the penalty for insured-initiated early cancellation."),
            ("The insurer cancels the policy for nonpayment of premium.", False, "When the insurer cancels, the return is pro rata — the full unearned premium."),
            ("The insured files more than two claims in a policy year.", False, "Claim frequency affects renewal decisions, not cancellation return premium calculations."),
            ("The insured requests a policy extension beyond the expiration date.", False, "Extensions are handled through endorsement or renewal, not short rate cancellation."),
        ]
    ),
    (
        "Under the 'pair and set' clause in a property policy, if one item of a pair is lost or damaged, the insurer:",
        "multiple_choice", "hard",
        "The pair and set clause limits recovery when one item of a matched pair or set is lost. The insurer pays the difference in value between the set before and after the loss — not the full value of the remaining items.",
        [
            ("Pays only the reduction in value of the set, not the full value of the remaining items.", True, "Correct. The insurer pays the difference in set value, not replacement of all remaining items."),
            ("Pays the full replacement cost of the entire pair or set.", False, "Paying for the undamaged items would give the insured a windfall beyond the actual loss."),
            ("Pays nothing because pairs and sets are always excluded.", False, "Pairs and sets are covered; the clause limits recovery to the actual reduction in set value."),
            ("Requires the insured to surrender the undamaged item to the insurer.", False, "Some policies may offer this as an option at the insurer's election, but it is not automatic."),
        ]
    ),
    (
        "A neighbor's tree falls onto the insured's fence during a windstorm. The cost to remove the tree and repair the fence is $3,500. The insured's homeowners policy would most likely:",
        "scenario", "standard",
        "Under a homeowners policy, windstorm is a covered peril. Damage to the fence (Coverage B) from a falling tree is covered. Debris removal may also be covered. The neighbor is not liable if the tree fell due to natural causes (windstorm).",
        [
            ("Cover the fence repair and debris removal under the homeowners policy.", True, "Correct. Windstorm damage to fences is covered under HO Coverage B; the neighbor has no liability for natural windfall."),
            ("Require the neighbor to pay because the tree was on their property.", False, "A neighbor is not liable for damage caused by a healthy tree falling due to an act of nature."),
            ("Deny the claim because falling objects are excluded from Coverage B.", False, "Falling objects caused by covered perils (windstorm) are covered under standard homeowners forms."),
            ("Cover only the debris removal, not the fence repair.", False, "Both the fence repair and debris removal are covered under the standard homeowners policy."),
        ]
    ),
],

"casualty-fundamentals": [
    (
        "An insured is 30% at fault in an accident in a 'pure comparative negligence' state. The total damages are $100,000. How much can the insured recover from the other party?",
        "scenario", "hard",
        "In a pure comparative negligence state, a plaintiff can recover even if they are mostly at fault. Recovery is reduced by their percentage of fault. The insured is 30% at fault, so they recover 70% × $100,000 = $70,000.",
        [
            ("$70,000 — 70% of damages since the insured is 30% at fault.", True, "Correct. Pure comparative negligence reduces recovery proportionally regardless of the plaintiff's fault percentage."),
            ("$0 — the insured cannot recover because they were partially at fault.", False, "This describes contributory negligence. Pure comparative allows recovery regardless of fault percentage."),
            ("$100,000 — the full damages because comparative negligence bars any reduction.", False, "Comparative negligence reduces recovery by the plaintiff's fault percentage."),
            ("$50,000 — damages are split equally in any shared-fault situation.", False, "Damages are split according to actual fault percentages, not automatically 50/50."),
        ]
    ),
    (
        "The 'sudden and accidental' pollution exclusion in a liability policy means:",
        "multiple_choice", "hard",
        "Absolute pollution exclusions bar all pollution claims. Policies with a 'sudden and accidental' exception cover pollution that was sudden (abrupt, not gradual) and accidental (unintended). Gradual seepage or long-term contamination is still excluded.",
        [
            ("Pollution that occurs abruptly and unintentionally may be covered; gradual pollution is excluded.", True, "Correct. The exception restores coverage only for sudden, accidental pollution events."),
            ("All pollution claims are covered as long as the insured did not intend the pollution.", False, "Intent alone is not sufficient — the pollution must also be sudden, not gradual."),
            ("Pollution coverage is completely excluded with no exceptions.", False, "An absolute exclusion would bar all pollution; the sudden and accidental exception creates limited coverage."),
            ("Pollution claims are covered only if the insured reports them within 24 hours.", False, "The timing of reporting affects notice requirements, not whether the sudden and accidental exception applies."),
        ]
    ),
    (
        "A business owner is sued by a customer who claims the owner's employee assaulted them. The CGL's 'expected or intended injury' exclusion will:",
        "scenario", "hard",
        "The expected or intended exclusion removes coverage for injuries the insured deliberately caused. However, the exclusion applies to the insured whose conduct was intentional. Other insureds (like the business owner who did not direct the assault) may still have coverage under the severability of interests provision.",
        [
            ("Exclude the employee's coverage but may not exclude the business owner's coverage due to severability.", True, "Correct. Severability applies the exclusion separately — the owner who didn't direct the assault may retain coverage."),
            ("Exclude coverage entirely because the injury arose from an intentional act.", False, "Severability of interests means the exclusion applies separately to each insured — the innocent employer may still be covered."),
            ("Not apply because assault is a covered personal injury offense.", False, "Personal and advertising injury covers specific offenses; assault by the insured is typically excluded."),
            ("Apply only if the employee was acting outside the scope of employment.", False, "The expected or intended exclusion looks at intent, not scope of employment."),
        ]
    ),
    (
        "Under the CGL, 'bodily injury' is defined to include:",
        "multiple_choice", "standard",
        "Bodily injury under the CGL means physical harm to a person's body, including sickness, disease, and death. It includes associated mental anguish and emotional distress when they flow from the physical injury.",
        [
            ("Physical injury, sickness, disease, and death resulting therefrom.", True, "Correct. The CGL bodily injury definition encompasses all physical harm and its direct consequences."),
            ("Only injuries that result in medical treatment or hospitalization.", False, "Bodily injury is defined broadly and is not limited to injuries requiring medical treatment."),
            ("Physical and emotional injuries whether or not accompanied by physical harm.", False, "Pure emotional distress without physical injury is typically not covered under the bodily injury definition."),
            ("Only injuries that are permanent or result in loss of earning capacity.", False, "Bodily injury includes all physical harm, not just permanent or disabling injuries."),
        ]
    ),
    (
        "A garage owner's customer leaves their car for repairs. The garage owner negligently damages the customer's car. Under the CGL, this loss is:",
        "scenario", "standard",
        "The CGL excludes property damage to property in the insured's care, custody, or control. A customer's car left for repairs is in the garage owner's care, custody, and control. The CGL does not cover this — the garage owner needs Garagekeepers Legal Liability coverage.",
        [
            ("Excluded under the care, custody, and control exclusion — Garagekeepers coverage is needed.", True, "Correct. Property left in the insured's care is excluded from the CGL."),
            ("Covered under the CGL premises and operations coverage.", False, "The care, custody, and control exclusion specifically removes coverage for property entrusted to the insured."),
            ("Covered because the damage was caused by the insured's negligence.", False, "Negligence is a trigger for coverage, but the care/custody/control exclusion still applies regardless of fault."),
            ("Excluded only if the car was worth more than $10,000.", False, "The exclusion applies regardless of the value of the property."),
        ]
    ),
],

"personal-auto": [
    (
        "An insured drives their personal auto to make deliveries for a pizza restaurant as a side job. They cause an accident while delivering. The PAP will most likely:",
        "scenario", "hard",
        "The PAP excludes use of a vehicle as a 'public or livery conveyance' — meaning using it for delivery services for compensation. Business delivery use is typically excluded from personal auto coverage.",
        [
            ("Deny the claim because the vehicle was being used for commercial delivery purposes.", True, "Correct. The public or livery conveyance exclusion bars coverage for commercial delivery use."),
            ("Cover the claim because the insured was driving their own insured vehicle.", False, "Owning the vehicle does not override the use exclusion for commercial purposes."),
            ("Cover the claim up to $10,000 because it was occasional use.", False, "There is no occasional-use exception for the commercial delivery exclusion."),
            ("Cover the claim if the pizza restaurant's commercial auto policy did not apply.", False, "The PAP exclusion applies regardless of other available coverage."),
        ]
    ),
    (
        "Under the PAP, 'underinsured motorist coverage' (UIM) responds when:",
        "multiple_choice", "standard",
        "UIM coverage responds when the at-fault driver has liability insurance but their limits are insufficient to cover the insured's damages. The insured's UIM coverage pays the gap between the at-fault driver's limits and the insured's actual damages.",
        [
            ("The at-fault driver has liability insurance but with limits too low to cover all damages.", True, "Correct. UIM fills the gap when the responsible driver is insured but underinsured."),
            ("The at-fault driver has no insurance at all.", False, "No insurance = uninsured motorist (UM) coverage, not underinsured motorist (UIM)."),
            ("The insured's own vehicle damage exceeds their collision deductible.", False, "UIM applies to bodily injury and sometimes property damage from an underinsured driver, not collision deductibles."),
            ("The insured is at fault and their liability limits are exceeded.", False, "UIM protects the insured as a victim, not as an at-fault driver."),
        ]
    ),
    (
        "A vehicle is listed on the PAP declarations as a covered auto. The named insured sells the vehicle and purchases a new one. Coverage on the new vehicle:",
        "scenario", "standard",
        "Under the PAP, newly acquired autos are automatically covered for a specified period (typically 14 or 30 days depending on the situation). The insured must notify the insurer within that period to maintain continuous coverage.",
        [
            ("Automatically applies for the specified reporting period; the insured must notify the insurer to continue coverage.", True, "Correct. The PAP automatically covers newly acquired autos during the reporting window."),
            ("Does not apply until the insured specifically adds the new vehicle to the policy.", False, "The PAP provides automatic coverage during the reporting period — the insured doesn't need to call first."),
            ("Applies permanently without any notification requirement.", False, "Notification is required to maintain coverage beyond the automatic coverage period."),
            ("Only applies if the new vehicle costs less than the vehicle it replaces.", False, "Vehicle value does not determine automatic coverage eligibility under the PAP."),
        ]
    ),
    (
        "The PAP's 'transportation expense' coverage (rental reimbursement) pays:",
        "multiple_choice", "standard",
        "Transportation expense coverage pays for rental car or other transportation costs when the insured's vehicle is disabled due to a covered loss. It typically has a daily limit and a maximum total limit.",
        [
            ("Rental car or transportation costs while the insured's vehicle is being repaired after a covered loss.", True, "Correct. Transportation expense covers temporary substitute transportation after a covered auto loss."),
            ("All transportation costs the insured incurs regardless of the reason.", False, "Coverage is triggered only by a covered loss to the insured's vehicle."),
            ("The cost of a new vehicle if the insured's vehicle is totaled.", False, "Total loss settlement is handled under collision or comprehensive coverage, not transportation expense."),
            ("Taxi or rideshare costs if the insured chooses not to rent a car.", False, "While some policies do cover rideshare, transportation expense traditionally covers rental cars or similar substitutes."),
        ]
    ),
    (
        "An insured loans their car to a friend who has a suspended license. The friend causes an accident. Under the PAP:",
        "scenario", "hard",
        "The PAP covers permissive users regardless of their license status in most cases. However, if the insured knew the driver had a suspended license, some policies may apply an exclusion for knowingly entrusting a vehicle to an unlicensed driver. Coverage analysis depends on policy language and state law.",
        [
            ("Coverage likely applies because the PAP covers permissive users, though the insured may face an exclusion for knowingly entrusting a vehicle to an unlicensed driver.", True, "Correct. Permissive use generally creates coverage, but knowing entrustment to an unlicensed driver creates a coverage question."),
            ("Coverage is automatically denied because the driver had a suspended license.", False, "License suspension does not automatically void coverage; it depends on what the insured knew and the specific policy language."),
            ("Coverage applies in full because the insured gave permission to use the vehicle.", False, "While permission is generally sufficient, knowingly entrusting to an unlicensed driver may trigger an exclusion."),
            ("The friend's own auto policy is the only applicable coverage.", False, "The vehicle owner's PAP is primary; the friend may have no coverage since they had no insured vehicle."),
        ]
    ),
],

"homeowners": [
    (
        "A homeowner installs a swimming pool. Their insurer is not notified. Six months later, a neighbor's child drowns in the pool. The homeowner's CGL-type liability under Coverage E would:",
        "scenario", "hard",
        "Swimming pools are generally covered under homeowners Coverage E (personal liability) even if not specifically reported to the insurer. The insurer may have underwriting concerns, but failure to report a pool does not automatically void liability coverage.",
        [
            ("Likely provide coverage because pools are generally covered under personal liability without specific notification.", True, "Correct. Coverage E covers personal liability broadly; pools are not a standard notification requirement under most HO policies."),
            ("Be void because the insured made a material change to the risk without notifying the insurer.", False, "Adding a pool is a material change affecting underwriting, but it does not automatically void liability coverage already in force."),
            ("Cover only bodily injury to the insured's family members.", False, "Coverage E covers third-party bodily injury; family members are not covered as 'others.'"),
            ("Be excluded because drowning is specifically listed as an excluded peril.", False, "Drowning is not a standard exclusion under homeowners personal liability coverage."),
        ]
    ),
    (
        "Under the homeowners policy, 'business pursuits' are generally excluded from Coverage E (Personal Liability) because:",
        "multiple_choice", "standard",
        "Business activities create liability exposures that are more frequent and severe than personal activities. Business liability requires a commercial general liability policy. The homeowners policy is designed for personal, non-business activities.",
        [
            ("Business activities generate commercial liability exposures that require commercial insurance, not a homeowners policy.", True, "Correct. The homeowners policy is for personal liability; business pursuits need a CGL or BOP."),
            ("Business activities are too profitable to qualify for standard homeowners rates.", False, "Profitability is not the reason for the exclusion — the nature and frequency of the exposure is."),
            ("Only businesses with employees are excluded; self-employed individuals are covered.", False, "The business pursuits exclusion applies to all business activities, not just those with employees."),
            ("The exclusion only applies to businesses operated from outside the home.", False, "Business pursuits are excluded regardless of where they are conducted."),
        ]
    ),
    (
        "An insured's teenager accidentally breaks a neighbor's window while playing baseball. The homeowners Coverage E would:",
        "scenario", "standard",
        "Coverage E (personal liability) covers the named insured and resident family members for accidental property damage to others. A resident teenager is an insured under the homeowners policy.",
        [
            ("Cover the property damage because resident family members are insureds under Coverage E.", True, "Correct. The teenager is a covered insured under the homeowners policy as a resident family member."),
            ("Deny the claim because the damage was caused by a minor child.", False, "Age does not determine coverage — resident family members are covered regardless of age."),
            ("Cover the claim only if the neighbor files a formal lawsuit.", False, "Coverage E covers property damage regardless of whether a lawsuit is filed."),
            ("Deny the claim because property damage to neighbors is excluded from homeowners.", False, "Third-party property damage caused by the insured is a core coverage under Coverage E."),
        ]
    ),
    (
        "The homeowners policy's 'business property' sublimit typically applies to:",
        "multiple_choice", "standard",
        "Standard homeowners policies limit coverage for business personal property (computers, equipment used for business) to a sublimit, typically $2,500 on premises and $500 off premises. A home office endorsement or separate policy is needed for full business property coverage.",
        [
            ("Business personal property such as office equipment and inventory used for business purposes.", True, "Correct. Business property has a sublimit under Coverage C of the homeowners policy."),
            ("All property owned by a person who operates a business, regardless of use.", False, "The sublimit applies specifically to property used for business purposes, not all property owned by a business owner."),
            ("Only property located in a dedicated home office room.", False, "The business property sublimit applies to all property used for business, not just property in a specific room."),
            ("Vehicles used for business purposes parked in the garage.", False, "Vehicles are excluded from homeowners coverage entirely; the sublimit applies to personal property items."),
        ]
    ),
    (
        "Under a homeowners policy, 'earth movement' is excluded. This means all of the following losses are excluded EXCEPT:",
        "multiple_choice", "hard",
        "The earth movement exclusion covers earthquake, landslide, subsidence, and sinkhole. However, if an explosion causes earth movement that damages the structure, the proximate cause is the explosion (a covered peril), not earth movement. The explosion exception preserves coverage.",
        [
            ("Earth movement caused by an explosion that is otherwise covered under the policy.", True, "Correct. When a covered peril (explosion) causes earth movement, the resulting damage is covered."),
            ("Foundation cracking caused by soil settlement over many years.", False, "Gradual soil settlement causing foundation damage is excluded under earth movement and deterioration."),
            ("Structural damage from a minor earthquake.", False, "Earthquake is specifically included in the earth movement exclusion."),
            ("Landslide damage after heavy rain.", False, "Landslide is included in the earth movement exclusion regardless of the triggering event."),
        ]
    ),
],

"dwelling-policies": [
    (
        "Under a DP-2 (broad form) dwelling policy, which of the following perils is covered that is NOT covered under the DP-1?",
        "multiple_choice", "standard",
        "The DP-2 broad form adds several perils to the DP-1 basic form, including windstorm, hail, explosion, riot, aircraft, vehicles, smoke, vandalism, and theft (limited). Windstorm is one of the most significant additions.",
        [
            ("Windstorm and hail damage to the dwelling.", True, "Correct. Windstorm and hail are added in the DP-2 broad form but are not covered in the DP-1 basic form."),
            ("Fire damage to the dwelling.", False, "Fire is covered under both the DP-1 and DP-2 — it is the most basic covered peril."),
            ("Flood damage from surface water.", False, "Flood is excluded under all DP forms; separate flood insurance is required."),
            ("Damage caused by earthquake.", False, "Earthquake is excluded under all standard DP forms."),
        ]
    ),
    (
        "A landlord owns a rental property insured under a DP-3. The tenant accidentally starts a fire that damages the kitchen. The landlord's DP-3 will:",
        "scenario", "standard",
        "A DP-3 covers the dwelling structure on an open perils basis. Fire caused by the tenant's negligence is a covered peril. The landlord's policy covers the structural damage. The insurer may then subrogate against the tenant.",
        [
            ("Cover the structural damage; the insurer may then subrogate against the negligent tenant.", True, "Correct. The landlord's DP-3 covers the structure; the insurer can pursue the at-fault tenant for recovery."),
            ("Deny the claim because the tenant caused the fire, not the insured.", False, "Property policies cover accidental losses regardless of who caused them; the named insured is the landlord."),
            ("Cover the damage but void the policy at renewal for the tenant's negligence.", False, "Policies are not voided mid-term for a covered loss, though the insurer may nonrenew."),
            ("Require the tenant's renters insurance to pay first.", False, "The landlord's dwelling policy is the primary coverage for structural damage to the landlord's building."),
        ]
    ),
    (
        "Under a dwelling policy, which party is the 'named insured' and who is protected by the liability coverage if added by endorsement?",
        "multiple_choice", "standard",
        "The named insured on a dwelling policy is the property owner (landlord). If personal liability is added by endorsement, it protects the named insured (landlord) for their liability arising from the property — not the tenant.",
        [
            ("The property owner is the named insured; liability endorsement protects the owner, not the tenant.", True, "Correct. The DP covers the owner's interest; tenants need their own HO-4 for liability protection."),
            ("Both the landlord and all tenants are named insureds under the dwelling policy.", False, "Tenants are not named insureds under a landlord's dwelling policy."),
            ("The mortgage lender is the primary named insured under a dwelling policy.", False, "The mortgage lender is typically a loss payee or additional insured, not the named insured."),
            ("The tenant becomes the named insured once they occupy the property.", False, "The property owner remains the named insured regardless of who occupies the dwelling."),
        ]
    ),
    (
        "A property is vacant for more than 60 consecutive days. Under most dwelling policies, this will:",
        "multiple_choice", "standard",
        "Vacant properties present increased risk — higher probability of vandalism, undetected damage, and arson. Most property policies suspend or limit coverage after 60 consecutive days of vacancy unless a vacancy permit endorsement is obtained.",
        [
            ("Suspend or restrict coverage unless a vacancy permit endorsement is obtained.", True, "Correct. Extended vacancy triggers coverage restrictions under standard dwelling and property policies."),
            ("Have no effect on coverage because the policy covers the structure regardless of occupancy.", False, "Vacancy is a material change in risk that affects coverage under standard property policies."),
            ("Automatically cancel the policy and return all unearned premium.", False, "Policies are not automatically cancelled for vacancy — coverage is suspended or restricted."),
            ("Increase the premium retroactively for the vacancy period.", False, "Retroactive premium increases are not the typical response; coverage restriction is."),
        ]
    ),
    (
        "A dwelling policy's Coverage C (Personal Property) has a sublimit for theft. This means:",
        "multiple_choice", "standard",
        "Even when theft is a covered peril under a dwelling policy, Coverage C often imposes sublimits on certain categories of personal property (jewelry, silverware, firearms, etc.) that are more susceptible to theft.",
        [
            ("Coverage for theft of certain high-value items like jewelry may be limited to a sublimit.", True, "Correct. Theft sublimits are common under dwelling policies for categories of valuable personal property."),
            ("All theft claims are covered up to the full Coverage C limit with no restrictions.", False, "Theft sublimits apply to specific categories; not all theft is subject to the full Coverage C limit."),
            ("Theft is excluded entirely from dwelling policy personal property coverage.", False, "Some DP forms cover theft with sublimits; it is not categorically excluded."),
            ("The sublimit only applies to theft by the tenant, not by outsiders.", False, "Theft sublimits apply based on the category of property stolen, not who committed the theft."),
        ]
    ),
],

"commercial-property": [
    (
        "A commercial property policy has a $500,000 limit and an 80% coinsurance requirement. The building's replacement cost is $800,000. A $200,000 partial loss occurs. How much does the insurer pay?",
        "scenario", "hard",
        "Required insurance = $800,000 × 80% = $640,000. Carried = $500,000. Payment = ($500,000 / $640,000) × $200,000 = 0.78125 × $200,000 = $156,250.",
        [
            ("$156,250 — because the property is underinsured relative to the 80% coinsurance requirement.", True, "Correct. ($500,000 ÷ $640,000) × $200,000 = $156,250. The insured bears the remaining $43,750."),
            ("$200,000 — the full loss amount because partial losses are always paid in full.", False, "Partial losses are subject to the coinsurance formula when the property is underinsured."),
            ("$160,000 — 80% of the loss amount based on the coinsurance percentage.", False, "The coinsurance formula uses the ratio of carried to required insurance, not the coinsurance percentage itself."),
            ("$500,000 — the full policy limit since the loss is less than the limit.", False, "The coinsurance penalty reduces the payment even when the loss is below the policy limit."),
        ]
    ),
    (
        "Under commercial property coverage, 'peak season endorsement' is used when:",
        "multiple_choice", "standard",
        "A peak season endorsement (also called seasonal automatic increase) increases the coverage limit for business personal property or stock during specified high-inventory periods — such as a retailer increasing inventory before the holiday season.",
        [
            ("A business has higher inventory values during certain seasons and needs increased coverage.", True, "Correct. Peak season endorsements automatically increase limits during high-value periods."),
            ("A business wants to reduce premium by decreasing coverage during slow periods.", False, "The endorsement increases coverage during peak periods; it doesn't reduce coverage in slow periods."),
            ("A business operates in a region with higher storm risk during certain seasons.", False, "Seasonal storm risk is a rating consideration, not what the peak season endorsement addresses."),
            ("A business wants to add coverage for seasonal employees.", False, "Employee coverage is handled under workers compensation and employers liability, not the peak season endorsement."),
        ]
    ),
    (
        "The commercial property 'builders risk' coverage form is designed for:",
        "multiple_choice", "standard",
        "Builders risk insurance covers a building or structure while it is under construction. Coverage begins when construction starts and typically ends when the building is completed, occupied, or the policy expires.",
        [
            ("Buildings under construction — from groundbreaking until the project is completed.", True, "Correct. Builders risk is specifically designed for the construction phase of a project."),
            ("Buildings that have been partially demolished and are being rebuilt.", False, "While rebuilding after demolition may qualify, builders risk specifically covers new construction and renovation projects."),
            ("Buildings that are vacant while the owner seeks a new tenant.", False, "Vacant building coverage is handled under standard property forms with vacancy permits."),
            ("Equipment used by contractors to construct buildings.", False, "Contractor's equipment is covered under inland marine equipment floaters, not builders risk."),
        ]
    ),
    (
        "A 'business income with extra expense' policy covers a restaurant that is forced to close for two months after a fire. Which of the following is covered?",
        "scenario", "standard",
        "Business income coverage pays lost net income and continuing expenses during the restoration period. Extra expense pays additional costs to continue or expedite operations. Together they cover lost revenue, payroll, rent, and costs to resume operations sooner.",
        [
            ("Lost revenue, ongoing payroll and rent, and extra costs to expedite repairs and reopen sooner.", True, "Correct. Business income covers lost income and continuing expenses; extra expense covers additional resumption costs."),
            ("Only the lost revenue for the two months the restaurant was closed.", False, "The policy also covers continuing expenses (payroll, rent) and extra expense to reopen sooner."),
            ("Only the extra costs to repair — lost revenue is covered under a separate business interruption policy.", False, "Business income with extra expense is a combined form covering both lost income and extra costs."),
            ("The market value of food spoiled in the freezers during the closure.", False, "Spoiled food would be covered under the building and personal property form; business income covers lost revenue."),
        ]
    ),
    (
        "Under the commercial property 'causes of loss — special form,' which of the following losses is most likely EXCLUDED?",
        "multiple_choice", "standard",
        "The special form covers all risks of physical loss except those specifically excluded. Standard exclusions include flood, earthquake, ordinance or law, intentional acts, wear and tear, mechanical breakdown, and earth movement.",
        [
            ("Gradual deterioration and wear and tear of roofing materials.", True, "Correct. Wear and tear and deterioration are standard exclusions even under the open perils special form."),
            ("Theft of business personal property from the insured premises.", False, "Theft is covered under the special form unless specifically excluded."),
            ("Water damage from a burst sprinkler pipe.", False, "Sudden and accidental water damage from plumbing/sprinklers is typically covered under the special form."),
            ("Wind damage to the building's roof during a storm.", False, "Windstorm is a covered cause of loss under the special form unless excluded by endorsement."),
        ]
    ),
],

"commercial-general-liability": [
    (
        "An insured hires a subcontractor who negligently installs a gas line. Three months after the work is completed, a gas leak causes an explosion. Under the CGL, who has coverage?",
        "scenario", "hard",
        "The insured (general contractor) has CGL coverage for claims arising from the subcontractor's work under completed operations. The subcontractor's own CGL also covers their completed work. The general contractor may be sued under vicarious liability for the subcontractor's negligence.",
        [
            ("Both the general contractor and the subcontractor may have coverage under their respective CGL policies.", True, "Correct. The GC has completed operations coverage; the sub has their own CGL for their completed work."),
            ("Neither party has coverage because the loss occurred after the work was completed.", False, "Completed operations coverage specifically covers losses that occur after work is finished."),
            ("Only the subcontractor has coverage since they performed the negligent work.", False, "The general contractor may be vicariously liable and has their own CGL coverage."),
            ("Only the general contractor has coverage since they hired the subcontractor.", False, "Both parties have separate CGL policies that can respond to their respective liability exposures."),
        ]
    ),
    (
        "The CGL 'liquor liability exclusion' applies to insureds who:",
        "multiple_choice", "standard",
        "The liquor liability exclusion in the CGL applies to insureds in the business of manufacturing, distributing, selling, or serving alcoholic beverages. A bar or restaurant needs a separate liquor liability policy. The exclusion does not apply to a business that serves alcohol at a company party.",
        [
            ("Are in the business of manufacturing, distributing, or selling alcoholic beverages.", True, "Correct. The exclusion targets businesses for which alcohol is a core part of their operations."),
            ("Serve any alcoholic beverages at their business premises.", False, "The exclusion applies to those in the alcohol business, not all businesses that serve alcohol."),
            ("Allow employees to consume alcohol during working hours.", False, "Employee alcohol consumption is an HR matter; the CGL liquor exclusion targets commercial alcohol sales."),
            ("Host occasional parties where alcohol is served to guests.", False, "Incidental alcohol service at non-alcohol businesses is generally NOT subject to the liquor liability exclusion."),
        ]
    ),
    (
        "The CGL 'pollution exclusion' most commonly excludes coverage for:",
        "multiple_choice", "standard",
        "The absolute pollution exclusion in modern CGL policies excludes bodily injury or property damage arising from the discharge, dispersal, or release of pollutants. This covers traditional environmental contamination claims.",
        [
            ("Bodily injury or property damage from the release of pollutants into the environment.", True, "Correct. The pollution exclusion targets environmental contamination and toxic substance releases."),
            ("All chemical reactions that occur on the insured's premises.", False, "Not all chemical reactions involve pollutants; the exclusion is specific to pollutant releases."),
            ("Product liability claims involving hazardous materials.", False, "Products liability is covered under products/completed operations; pollution exclusion applies to environmental releases."),
            ("Claims by employees injured by workplace chemicals under OSHA regulations.", False, "Employee injury claims are excluded under the workers compensation exclusion, not the pollution exclusion."),
        ]
    ),
    (
        "Under the CGL, 'contractual liability' coverage applies to:",
        "multiple_choice", "standard",
        "The CGL excludes contractual liability in general but restores coverage for liability the insured assumes in an 'insured contract' — primarily hold harmless or indemnification agreements in construction or service contracts where the insured assumes the other party's tort liability.",
        [
            ("Liability the insured assumes under an 'insured contract' such as a hold harmless agreement.", True, "Correct. The contractual liability coverage exception applies to insured contracts — typically written hold harmless agreements."),
            ("All obligations the insured assumes under any written contract.", False, "Only liability assumed under 'insured contracts' (as defined in the policy) is covered — not all contractual obligations."),
            ("Penalty clauses and liquidated damages in construction contracts.", False, "Penalties and liquidated damages are contract-specific obligations, not tort liability assumed in insured contracts."),
            ("Warranty claims arising from products the insured sold.", False, "Warranty obligations are contractual but are generally covered under products liability, not specifically under contractual liability."),
        ]
    ),
    (
        "A CGL policy's 'aggregate limit' has been reduced by prior claims to $500,000. A new $800,000 judgment is entered against the insured. The insurer pays:",
        "scenario", "hard",
        "The aggregate limit is the maximum the insurer will pay for all claims during the policy period. If the aggregate has been reduced to $500,000 by prior payments, the insurer pays only $500,000 on the new judgment. The insured is responsible for the remaining $300,000.",
        [
            ("$500,000 — the remaining aggregate limit; the insured is responsible for the $300,000 excess.", True, "Correct. The aggregate caps total payments; once reduced, only the remaining amount is available."),
            ("$800,000 — the full judgment because each occurrence has its own per-occurrence limit.", False, "The aggregate limit overrides the per-occurrence limit once the aggregate is reduced."),
            ("$0 — the aggregate is exhausted so the insurer pays nothing.", False, "The aggregate is not exhausted — $500,000 remains, so the insurer pays that amount."),
            ("$300,000 — the difference between the judgment and the per-occurrence limit.", False, "This calculation has no basis; the insurer pays the remaining aggregate, not a difference figure."),
        ]
    ),
],

"business-auto": [
    (
        "A company's BAP is written on Symbol 1 (any auto). An employee uses their personal vehicle for a business errand and causes an accident. Which policy responds first?",
        "scenario", "hard",
        "When an employee uses their personal vehicle for business, the employee's personal auto policy (PAP) is primary. The employer's BAP with non-owned auto coverage is excess over the employee's PAP.",
        [
            ("The employee's personal auto policy is primary; the employer's BAP is excess.", True, "Correct. The PAP on the vehicle is primary; the BAP's non-owned auto coverage is excess."),
            ("The employer's BAP is primary because the employee was on company business.", False, "Coverage follows the vehicle first — the employee's PAP is primary regardless of business use."),
            ("Both policies share the loss equally on a pro rata basis.", False, "There is a primary/excess relationship, not pro rata sharing, between personal and commercial auto policies."),
            ("Only the employer's BAP responds because personal policies exclude business use.", False, "The PAP covers occasional business use; it responds first as the vehicle's primary policy."),
        ]
    ),
    (
        "Under the BAP, 'loading and unloading' of a covered auto is considered:",
        "multiple_choice", "standard",
        "Under the BAP, the use of a vehicle includes loading and unloading. An injury occurring while cargo is being loaded onto or unloaded from a covered auto is treated as arising from the use of the auto and is covered under the BAP.",
        [
            ("Part of the use of the auto — covered under the BAP liability coverage.", True, "Correct. Loading and unloading is specifically included in the definition of 'use' under the BAP."),
            ("A separate operations exposure covered only under a CGL policy.", False, "While a CGL may also apply, loading and unloading is within the BAP's coverage scope."),
            ("Excluded because the vehicle was stationary at the time of injury.", False, "The BAP covers loading and unloading regardless of whether the vehicle was moving."),
            ("Covered only if the cargo being loaded caused the injury.", False, "Coverage applies to injuries during loading and unloading regardless of the specific cause."),
        ]
    ),
    (
        "The BAP's 'Fellow Employee' exclusion means:",
        "multiple_choice", "standard",
        "The fellow employee exclusion in the BAP prevents one employee from suing the employer's liability coverage for injuries caused by another employee while operating a covered auto. Workers compensation is the exclusive remedy for these injuries.",
        [
            ("Coverage does not apply for bodily injury to a fellow employee caused while operating a covered auto.", True, "Correct. Fellow employee injuries are covered under workers compensation, not the BAP."),
            ("All employees are excluded from coverage as passengers in company vehicles.", False, "Passengers are covered; the exclusion specifically applies to bodily injury claims between employees."),
            ("No employee can be named as an insured under the BAP.", False, "Employees operating covered autos with permission are covered; the exclusion is for fellow employee injury claims."),
            ("Coverage is excluded for all employment-related accidents regardless of fault.", False, "The fellow employee exclusion is specific to employees injured by other employees — other accidents are covered."),
        ]
    ),
    (
        "A business purchases a new delivery truck in the middle of the policy period. Under the BAP with Symbol 2 (owned autos only), coverage on the new truck:",
        "scenario", "standard",
        "Symbol 2 covers owned private passenger autos. For a newly acquired auto that is not a private passenger type (like a delivery truck), the insured must notify the insurer within 30 days to obtain coverage. Private passenger autos have automatic coverage.",
        [
            ("Requires notification within 30 days since delivery trucks are not private passenger autos under Symbol 2.", True, "Correct. Symbol 2 auto-covers private passenger autos; commercial trucks require timely notification."),
            ("Is automatic because Symbol 2 covers all newly acquired owned autos.", False, "Symbol 2 automatically covers private passenger autos; non-passenger vehicles require notification."),
            ("Does not apply because delivery trucks require a separate commercial auto policy.", False, "Delivery trucks can be covered under a BAP; they just require notification under Symbol 2."),
            ("Is retroactive to the date of purchase without any notification requirement.", False, "Notification within 30 days is required for non-private-passenger newly acquired autos."),
        ]
    ),
    (
        "An employer is vicariously liable for an employee's negligent driving during business hours. The employer's BAP covers this liability primarily under:",
        "multiple_choice", "standard",
        "The BAP covers liability arising from the ownership, maintenance, or use of covered autos. An employee driving a covered auto during business hours creates a covered liability exposure for the employer under the BAP.",
        [
            ("The liability coverage for use of a covered auto by an insured.", True, "Correct. The employer's BAP covers their vicarious liability for employee auto accidents during business use."),
            ("The medical payments coverage for the injured third party.", False, "Medical payments covers occupants of the insured's vehicle; liability coverage responds to third-party claims."),
            ("The uninsured motorist coverage since the employer didn't directly cause the accident.", False, "UM covers the insured when hit by an uninsured driver; it does not apply to the employer's own liability."),
            ("The physical damage coverage for any vehicles involved in the accident.", False, "Physical damage covers the insured's own vehicle; liability coverage responds to third-party injury claims."),
        ]
    ),
],

"workers-compensation": [
    (
        "An employee is injured at a company-sponsored softball game held off company premises. Workers compensation coverage would most likely:",
        "scenario", "hard",
        "Whether a company-sponsored recreational activity is covered under workers compensation depends on whether participation was required or if the event primarily benefited the employer. Voluntary off-premises social events often are NOT covered; mandatory or employer-benefiting events often are.",
        [
            ("Depend on whether attendance was mandatory or primarily benefited the employer.", True, "Correct. Voluntary social events without employer benefit are typically not covered; employer-directed or mandatory events often are."),
            ("Always cover injuries at company events regardless of location.", False, "The 'arising out of and in the course of employment' test must be met; off-premises voluntary social events often fail this test."),
            ("Never cover injuries at events off company premises.", False, "Workers comp can cover off-premises injuries during work-related activities; it depends on the specific facts."),
            ("Cover the injury only if the employee was injured by a co-worker.", False, "The cause of injury is not the test; the employment connection test determines coverage."),
        ]
    ),
    (
        "Under workers compensation, the 'second injury fund' is designed to:",
        "multiple_choice", "hard",
        "Second injury funds (also called subsequent injury funds) encourage employers to hire workers with pre-existing disabilities. If a pre-existing condition combines with a new work injury to create a greater disability, the employer's WC policy pays the portion attributable to the new injury, and the fund pays the rest.",
        [
            ("Encourage hiring of workers with pre-existing conditions by limiting the employer's liability to only the new injury.", True, "Correct. Second injury funds prevent employers from avoiding hiring disabled workers by limiting their WC liability."),
            ("Provide additional benefits to workers whose employers have gone bankrupt.", False, "Insolvency protection is handled by state guaranty funds, not second injury funds."),
            ("Fund medical research into workplace injury prevention.", False, "Second injury funds are worker benefit mechanisms, not research funds."),
            ("Pay benefits to workers injured on their second job with the same employer.", False, "Second injury funds relate to prior disabilities, not multiple positions with one employer."),
        ]
    ),
    (
        "A sole proprietor operates a small contracting business. Under most state workers compensation laws, the sole proprietor:",
        "multiple_choice", "standard",
        "In most states, sole proprietors are exempt from mandatory workers compensation requirements for themselves (though they must cover employees). They may voluntarily elect coverage for themselves.",
        [
            ("Is typically exempt from mandatory WC coverage for themselves but may elect to be covered.", True, "Correct. Sole proprietors are typically exempt from mandatory WC for themselves; coverage is voluntary."),
            ("Must purchase workers compensation immediately upon starting the business.", False, "Sole proprietors are generally exempt from mandatory coverage for themselves, though employees must be covered."),
            ("Is covered automatically under their general liability policy.", False, "General liability does not cover work-related injuries to the business owner; that is a WC function."),
            ("Cannot purchase workers compensation under any circumstances.", False, "Sole proprietors may voluntarily elect WC coverage in most states."),
        ]
    ),
    (
        "Under workers compensation, the 'subrogation' right allows the insurer to:",
        "multiple_choice", "standard",
        "After paying workers compensation benefits, the insurer acquires the employee's right to sue the responsible third party. This prevents double recovery by the employee and allows the insurer to recover its payments.",
        [
            ("Recover WC benefits paid from a negligent third party who caused the workplace injury.", True, "Correct. The WC insurer may subrogate against liable third parties after paying benefits."),
            ("Reduce future WC benefits if the employee was partially at fault.", False, "WC is a no-fault system; the employee's fault is irrelevant to their benefits."),
            ("Cancel the policy after paying a large WC claim.", False, "Subrogation is a recovery right, not a cancellation mechanism."),
            ("Require the employer to reimburse the insurer for excessive claims.", False, "Experience-rated employers may see premium adjustments, but subrogation is against third parties, not employers."),
        ]
    ),
    (
        "An employee suffers a work-related injury but refuses reasonable medical treatment that would hasten recovery. The effect on workers compensation benefits is:",
        "scenario", "hard",
        "Workers compensation requires injured employees to cooperate with reasonable medical treatment. If an employee unjustifiably refuses treatment that would reduce disability, the insurer may suspend or reduce disability benefits. Medical benefits continue regardless.",
        [
            ("Disability benefits may be reduced or suspended; the employee cannot be forced to accept treatment.", True, "Correct. WC can reduce disability benefits for refusal of reasonable treatment but cannot force treatment."),
            ("All WC benefits are immediately terminated for non-compliance.", False, "Benefits are not immediately terminated; a formal process reduces or suspends disability benefits."),
            ("The employer bears the cost of extended disability because the employee refused treatment.", False, "The WC system reduces the employee's benefits for unjustified refusal — it does not shift responsibility to the employer."),
            ("No effect — the employee has the absolute right to refuse all medical treatment.", False, "While employees have medical autonomy, unjustified refusal of reasonable treatment can result in benefit reduction."),
        ]
    ),
],

"crime-bonds-specialty": [
    (
        "Under a commercial crime policy, 'computer fraud' coverage protects against:",
        "multiple_choice", "standard",
        "Computer fraud coverage responds to the fraudulent transfer of money or property by computer — including unauthorized access to computer systems to direct funds to unintended recipients.",
        [
            ("Fraudulent transfer of funds initiated through unauthorized computer access.", True, "Correct. Computer fraud covers manipulation of computer systems to cause unauthorized money transfers."),
            ("Physical theft of company computers and hardware.", False, "Physical theft of computers is covered under commercial property or employee theft, not computer fraud."),
            ("System downtime caused by a virus or malware attack.", False, "Business interruption from cyber attacks may be covered under cyber liability policies, not standard computer fraud coverage."),
            ("Data breaches that expose customer personal information.", False, "Data breach costs are covered under cyber liability insurance, not commercial crime computer fraud coverage."),
        ]
    ),
    (
        "A 'license and permit bond' guarantees that the principal will:",
        "multiple_choice", "standard",
        "A license and permit bond (required to obtain a business license or permit) guarantees that the bonded party will comply with applicable laws and regulations governing their licensed activity. It protects the public from losses caused by the principal's failure to comply.",
        [
            ("Comply with applicable laws and regulations in conducting their licensed business.", True, "Correct. License and permit bonds protect the public by guaranteeing regulatory compliance."),
            ("Complete a specific construction project on time and within budget.", False, "Project completion is guaranteed by a performance bond, not a license and permit bond."),
            ("Pay subcontractors and suppliers on a construction project.", False, "Payment of subcontractors is guaranteed by a payment bond."),
            ("Compensate clients for financial losses due to professional negligence.", False, "Professional negligence is covered under professional liability (E&O) insurance, not license bonds."),
        ]
    ),
    (
        "The 'discovery period' in a fidelity bond means:",
        "multiple_choice", "standard",
        "The discovery period is the time after a bond expires (or is cancelled) during which the insured can discover and report losses that occurred during the bond period. It is typically 12 months after termination.",
        [
            ("The period after bond termination during which losses from the bond period can still be discovered and claimed.", True, "Correct. The discovery period extends the reporting window beyond the bond's termination date."),
            ("The time the insurer has to investigate and pay a reported claim.", False, "The discovery period relates to when the insured discovers losses, not how long the insurer takes to investigate."),
            ("The time during which the insurer can discover and rescind the bond for misrepresentation.", False, "Discovery periods benefit the insured for late-discovered losses; rescission rights are separate."),
            ("The maximum time that can pass between a loss and when the employee must be terminated.", False, "Employment decisions are separate from the bond's discovery period."),
        ]
    ),
    (
        "Inland marine insurance covers a contractor's bulldozer while it is:",
        "scenario", "standard",
        "Contractor's equipment floaters (a type of inland marine) cover mobile equipment wherever it is located — on job sites, in transit, or in storage. This is the purpose of inland marine coverage for contractor's tools and equipment.",
        [
            ("Being used on a job site away from the contractor's home base.", True, "Correct. Inland marine contractor's equipment floaters cover mobile equipment at any location."),
            ("Parked permanently at the contractor's shop address.", False, "Equipment parked permanently at a fixed location may be covered under commercial property, not inland marine."),
            ("Being used on a project in another country.", False, "Standard inland marine coverage is typically limited to the United States and Canada; foreign projects need special coverage."),
            ("Operated by an independent contractor who rented it.", False, "Inland marine equipment floaters cover the owner's equipment; rented-out equipment to others requires different coverage."),
        ]
    ),
    (
        "A 'consequential loss' in a crime policy refers to:",
        "multiple_choice", "hard",
        "In crime insurance, a consequential loss is an indirect loss resulting from a covered crime loss — such as lost profit from the inability to fill orders after theft of inventory. Standard crime policies cover only direct losses; consequential losses require a specific endorsement.",
        [
            ("Indirect losses that flow from a direct crime loss, such as lost business income after theft.", True, "Correct. Consequential losses are indirect; standard crime policies cover only direct losses."),
            ("The legal consequences faced by an employee who committed the crime.", False, "Legal consequences to the employee are not an insured loss under a crime policy."),
            ("Multiple crime losses that are connected to the same scheme or act.", False, "Connected losses are addressed by the 'single loss' provisions in crime policies."),
            ("Property damage that occurs as a direct result of a covered burglary.", False, "Property damage during burglary is a direct loss, not a consequential loss."),
        ]
    ),
],

"ethics-producer-responsibilities": [
    (
        "A producer who accepts a commission from both the insured and the insurer for the same transaction is engaging in:",
        "multiple_choice", "hard",
        "Accepting compensation from both sides of a transaction without full disclosure to both parties is a conflict of interest and may constitute a violation of fiduciary duty. Some states prohibit dual compensation; others require written disclosure and consent.",
        [
            ("A conflict of interest that may violate fiduciary duty without full disclosure and consent.", True, "Correct. Dual compensation creates a conflict of interest; full disclosure to both parties is required."),
            ("Standard industry practice that is always permissible.", False, "Dual compensation is not universally permissible — it requires disclosure and consent and may be prohibited."),
            ("Rebating, which is always illegal regardless of disclosure.", False, "Dual compensation is a conflict of interest issue; rebating specifically involves returning value to the insured as an inducement."),
            ("Only a violation if the amounts from each party are unequal.", False, "The conflict of interest arises from the dual relationship, not from the amounts received."),
        ]
    ),
    (
        "Under the 'replacement regulations' in most states, when a producer replaces an existing life or health policy, they must:",
        "multiple_choice", "standard",
        "Replacement regulations require producers to provide a comparison of the old and new policies so the consumer can make an informed decision. The producer must also notify the existing insurer. These rules protect against twisting.",
        [
            ("Provide a written comparison of the existing and replacement policies and notify the existing insurer.", True, "Correct. Replacement regulations ensure the consumer understands what they are giving up and gaining."),
            ("Obtain written approval from the state insurance department before completing the replacement.", False, "State approval is not required for individual replacements; notification and comparison are required."),
            ("Refund the first year's premium on the new policy to offset any surrender charges.", False, "Refunding premium would be rebating; replacement regulations require disclosure, not premium refunds."),
            ("Cancel the existing policy before the new policy is issued.", False, "The new policy should be issued first; the consumer should not have a coverage gap during replacement."),
        ]
    ),
    (
        "An insurance producer's license can be suspended or revoked for all of the following EXCEPT:",
        "multiple_choice", "standard",
        "License revocation and suspension are serious regulatory actions triggered by fraud, misrepresentation, criminal convictions, incompetence, and violations of insurance laws. Choosing not to write a certain type of insurance is a legal business decision, not a violation.",
        [
            ("Declining to write certain types of insurance the producer finds unprofitable.", True, "Correct — this is NOT a basis for revocation. Producers may choose which products to offer."),
            ("Misappropriating client premium funds.", False, "Misappropriation of funds is a serious violation that will result in revocation and criminal charges."),
            ("Willfully misrepresenting the terms of a policy.", False, "Willful misrepresentation is grounds for revocation."),
            ("Felony conviction involving dishonesty or a breach of trust.", False, "Criminal convictions involving dishonesty or breach of trust are automatic grounds for revocation in most states."),
        ]
    ),
    (
        "A producer who gives a client free tickets to a sporting event worth $200 as an inducement to purchase a policy is most likely guilty of:",
        "scenario", "standard",
        "Rebating is the practice of giving or offering anything of value as an inducement to purchase insurance. Free tickets constitute a rebate because they represent something of value given to influence the insurance purchase decision.",
        [
            ("Rebating, because the tickets represent something of value given as a purchase inducement.", True, "Correct. Giving gifts of value to induce insurance purchases is rebating, regardless of form."),
            ("Twisting, because the producer used deception to influence the client.", False, "Twisting involves misrepresenting policies to induce switching; free tickets are rebating."),
            ("Nothing, because gifts under $250 are always permissible.", False, "There is no universal $250 gift threshold — rebating laws in most states prohibit any inducement of value."),
            ("Unfair trade practice, but not rebating specifically.", False, "Rebating IS an unfair trade practice; this is a rebating violation."),
        ]
    ),
    (
        "Under agency law, an insurance agent's 'express authority' is authority that is:",
        "multiple_choice", "standard",
        "Express authority is authority that is explicitly granted to the agent in writing — typically through the agency agreement or contract between the agent and the insurance company. It is the most clearly defined form of authority.",
        [
            ("Explicitly granted to the agent in writing through the agency agreement.", True, "Correct. Express authority is written, explicit authority granted by the principal."),
            ("Implied from the agent's position and the customs of the industry.", False, "This describes implied authority — authority that arises from the agent's role, not from explicit grants."),
            ("Created when the principal's conduct leads third parties to believe the agent has authority.", False, "This describes apparent authority — authority created by the principal's conduct toward third parties."),
            ("Emergency authority that arises when the principal is unavailable.", False, "Emergency authority (authority of necessity) is a narrow doctrine; express authority is explicitly granted."),
        ]
    ),
],

"exam-prep": [
    (
        "When the P&C exam asks about 'subrogation,' the key concept to remember is:",
        "multiple_choice", "standard",
        "Subrogation prevents double recovery. After the insurer pays a claim, it steps into the insured's shoes to recover from the responsible third party. The insured cannot collect from both the insurer and the tortfeasor.",
        [
            ("The insurer steps into the insured's shoes to recover from the responsible third party after paying a claim.", True, "Correct. Subrogation = insurer recovery from the party actually responsible for the loss."),
            ("The insured can collect from both the insurer and the responsible party.", False, "Subrogation prevents this double recovery — that is its purpose."),
            ("The insurer can cancel the policy after recovering through subrogation.", False, "Subrogation recovery does not affect the policy itself."),
            ("Subrogation only applies to property claims, not liability claims.", False, "Subrogation applies broadly across insurance lines wherever a responsible third party exists."),
        ]
    ),
    (
        "On a P&C exam, when you see the phrase 'all of the following EXCEPT,' the question is asking you to:",
        "multiple_choice", "standard",
        "EXCEPT questions require you to identify the false or inapplicable statement. Three answers are correct/true; one is wrong/false. The wrong one is the correct answer to an EXCEPT question.",
        [
            ("Identify the one statement that is FALSE or does NOT apply to the concept.", True, "Correct. EXCEPT questions are reverse logic — you're looking for what doesn't fit."),
            ("Choose the most complete and accurate statement from the options.", False, "Choosing the most complete answer is the strategy for positive questions, not EXCEPT questions."),
            ("Select all answers that apply since the question implies multiple correct answers.", False, "EXCEPT questions have exactly one correct answer — the false or inapplicable option."),
            ("Skip the question because EXCEPT questions have no definitive answer.", False, "EXCEPT questions always have exactly one correct answer."),
        ]
    ),
    (
        "A P&C exam question describes a scenario involving a 'named peril' policy. The key implication for coverage is:",
        "multiple_choice", "standard",
        "Under a named perils policy, only perils specifically listed in the policy are covered. The burden is on the insured to prove the loss was caused by a listed peril. This is the opposite of open perils, where the insurer must prove a loss is excluded.",
        [
            ("Only perils specifically listed in the policy are covered; unlisted perils are excluded.", True, "Correct. Named perils = coverage only for listed perils. Open perils = coverage for all perils except exclusions."),
            ("All perils are covered except those specifically excluded.", False, "This describes open perils (special form), not named perils."),
            ("The insurer must prove the loss was caused by an excluded peril to deny the claim.", False, "Under named perils, the insured bears the burden of proving the loss was from a listed peril."),
            ("Coverage is the same as open perils because all common perils are named.", False, "Named perils coverage is narrower than open perils; not all common perils are listed in a named perils form."),
        ]
    ),
    (
        "Which study technique is most effective for remembering which coverages apply to which policy type?",
        "multiple_choice", "standard",
        "Creating comparison tables that map coverages to policy types (PAP vs. BAP, HO-3 vs. DP-3, CGL vs. umbrella) is highly effective because insurance exam questions frequently test whether you know which coverage belongs to which policy.",
        [
            ("Creating comparison tables mapping specific coverages to each policy type.", True, "Correct. Comparison tables build the exact mental maps that insurance exam questions test."),
            ("Memorizing the premium rates for each coverage type.", False, "Premium rates are not tested on producer licensing exams."),
            ("Reading the full text of each policy form from the insurance company.", False, "Exam prep focuses on coverage concepts, not verbatim policy language."),
            ("Focusing only on the coverages that appear most often in your home state.", False, "State licensing exams test general P&C principles across all lines, not just locally common coverages."),
        ]
    ),
    (
        "A P&C exam question asks about a 'garage liability' policy. This policy is specifically designed for:",
        "multiple_choice", "standard",
        "Garage liability policies are designed for auto dealers, service stations, and repair shops. They cover both the premises/operations liability of the business and the auto liability arising from the use of autos in the garage business.",
        [
            ("Auto dealers, repair shops, and service stations that need both premises and auto liability coverage.", True, "Correct. Garage liability combines premises liability and auto liability for auto service businesses."),
            ("Homeowners who want to insure a detached garage as a separate structure.", False, "Detached garages on residential premises are covered under homeowners Coverage B, not garage liability."),
            ("Any business that operates a parking garage or lot.", False, "Parking facilities use garagekeepers legal liability; garage liability is for service-oriented auto businesses."),
            ("Commercial trucking companies that maintain their own repair facilities.", False, "Trucking companies use commercial auto and BAP policies; garage liability is for customer-facing auto service businesses."),
        ]
    ),
],

}


def load_batch3():
    create_all()
    db = SessionLocal()
    try:
        modules = {m.slug: m for m in db.scalars(select(Module)).all()}
        lessons_by_module = {}
        for slug, module in modules.items():
            lessons = db.scalars(
                select(Lesson).where(Lesson.module_id == module.id).order_by(Lesson.sort_order)
            ).all()
            lessons_by_module[slug] = lessons

        existing_count = db.scalar(select(func.count()).select_from(Question)) or 0
        print(f"Existing questions in DB: {existing_count}")

        loaded = 0
        for module_slug, questions in BATCH3_QUESTIONS.items():
            if module_slug not in modules:
                print(f"  WARNING: Module '{module_slug}' not found — skipping")
                continue
            module = modules[module_slug]
            lessons = lessons_by_module.get(module_slug, [])
            first_lesson_id = lessons[0].id if lessons else None

            for q_text, q_type, difficulty, explanation, choices in questions:
                q = Question(
                    module_id=module.id,
                    lesson_id=first_lesson_id,
                    question_text=q_text,
                    question_type=q_type,
                    difficulty=difficulty,
                    explanation=explanation,
                    is_active=True,
                )
                db.add(q)
                db.flush()
                for sort_order, (choice_text, is_correct, choice_explanation) in \
                        enumerate(choices, start=1):
                    db.add(AnswerChoice(
                        question_id=q.id,
                        choice_text=choice_text,
                        is_correct=is_correct,
                        explanation=choice_explanation,
                        sort_order=sort_order,
                    ))
                loaded += 1

        db.commit()
        total = db.scalar(select(func.count()).select_from(Question)) or 0
        print(f"Loaded {loaded} batch-3 questions.")
        print(f"Total questions in DB: {total}")
    finally:
        db.close()


if __name__ == "__main__":
    load_batch3()
