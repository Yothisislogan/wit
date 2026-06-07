#!/usr/bin/env python3
"""
load_real_questions.py
Run from pc-license-prep-server-v2/ directory:
    python3 scripts/load_real_questions.py

Clears all existing seeded questions and loads 70 real exam-quality
P&C licensing questions — 5 per module across all 14 modules.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_all
from app.models import Module, Lesson, Question, AnswerChoice
from sqlalchemy import select, delete

REAL_QUESTIONS = {

"insurance-basics": [
    (
        "Which of the following best describes the principle of indemnity?",
        "multiple_choice", "standard",
        "Indemnity means the insured is restored to their pre-loss financial position — no more, no less. Insurance should not be a source of profit.",
        [
            ("The insured is restored to their financial position before the loss, no more and no less.", True, "Correct. Indemnity prevents profit from a loss."),
            ("The insured receives the full replacement cost of any damaged property.", False, "Replacement cost is a valuation method, not the principle of indemnity."),
            ("The insurer must pay claims within 30 days of notice.", False, "This describes a prompt payment requirement, not indemnity."),
            ("The insured must notify the insurer of all potential losses.", False, "This describes a notice requirement, not indemnity."),
        ]
    ),
    (
        "An insured owns a warehouse worth $500,000 and suffers a $50,000 fire loss. The insurer pays $50,000. Which risk management method did the insurance represent?",
        "scenario", "standard",
        "Purchasing insurance transfers the financial risk of loss to the insurer in exchange for a premium.",
        [
            ("Risk transfer", True, "Correct. Insurance transfers financial responsibility for losses to the insurer."),
            ("Risk avoidance", False, "Avoidance means eliminating the activity that creates the risk entirely."),
            ("Risk retention", False, "Retention means the insured assumes the financial burden of the loss."),
            ("Risk reduction", False, "Reduction means taking steps to lower the probability or severity of a loss."),
        ]
    ),
    (
        "The Law of Large Numbers allows insurers to:",
        "multiple_choice", "standard",
        "The Law of Large Numbers states that the larger the group of similar risks, the more accurately the insurer can predict future losses.",
        [
            ("Predict future losses more accurately by pooling a large number of similar risks.", True, "Correct. Larger pools produce more statistically reliable loss predictions."),
            ("Eliminate all underwriting risk by diversifying across states.", False, "The law improves prediction accuracy but does not eliminate underwriting risk."),
            ("Charge lower premiums to all policyholders regardless of risk.", False, "Premiums are based on individual risk characteristics, not just pool size."),
            ("Guarantee that actual losses will equal expected losses exactly.", False, "The law improves estimates but actual losses still vary from expected."),
        ]
    ),
    (
        "All of the following are characteristics of an insurable risk EXCEPT:",
        "multiple_choice", "standard",
        "A catastrophic loss that affects all insureds simultaneously (like a war) is not insurable because it eliminates the ability to spread risk across many independent exposures.",
        [
            ("The loss must be catastrophic enough to affect all insureds at the same time.", True, "Correct — this is NOT a characteristic. Insurable risks must be non-catastrophic for the insurer."),
            ("The loss must be definite and measurable.", False, "Definite and measurable losses are a required characteristic of insurable risks."),
            ("There must be a large number of similar exposure units.", False, "A large homogeneous group is required for the Law of Large Numbers to apply."),
            ("The loss must be accidental and unintentional from the insured's perspective.", False, "Accidental losses are required — intentional losses are excluded."),
        ]
    ),
    (
        "A business owner installs a sprinkler system to reduce fire damage potential. This is an example of:",
        "scenario", "standard",
        "Risk reduction involves taking steps to lower the frequency or severity of potential losses without transferring or avoiding the risk.",
        [
            ("Risk reduction", True, "Correct. Installing a sprinkler system reduces the severity of a potential fire loss."),
            ("Risk transfer", False, "Transfer shifts financial responsibility to another party, such as an insurer."),
            ("Risk avoidance", False, "Avoidance would mean not operating the business at all."),
            ("Risk retention", False, "Retention means accepting the financial consequences of a loss."),
        ]
    ),
],

"insurance-contracts": [
    (
        "Which element of a valid insurance contract means the insured pays a premium and the insurer promises to pay covered losses?",
        "multiple_choice", "standard",
        "Consideration in an insurance contract is the premium paid by the insured and the promise to pay covered losses made by the insurer.",
        [
            ("Consideration", True, "Correct. Consideration is the exchange of value — premium for the promise of coverage."),
            ("Offer and acceptance", False, "Offer and acceptance describes the formation process, not the exchange of value."),
            ("Legal purpose", False, "Legal purpose means the contract cannot be for an illegal activity."),
            ("Competent parties", False, "Competent parties means both parties must have legal capacity to contract."),
        ]
    ),
    (
        "An insurance policy is described as a contract of adhesion because:",
        "multiple_choice", "standard",
        "A contract of adhesion is drafted entirely by one party (the insurer). The insured must accept or reject it as written — they cannot negotiate the terms.",
        [
            ("It is written entirely by the insurer, and the insured must accept or reject it as written.", True, "Correct. Because the insured cannot negotiate, ambiguities are interpreted in their favor."),
            ("Both parties must agree to every term before the policy is issued.", False, "This describes a negotiated contract, not a contract of adhesion."),
            ("The insured must adhere to all policy conditions or coverage is void.", False, "This describes policy conditions, not the legal concept of adhesion."),
            ("The insurer can change the terms at any time during the policy period.", False, "Insurers generally cannot unilaterally change terms mid-policy."),
        ]
    ),
    (
        "A policyholder submits a claim and provides a sworn statement with false information to obtain a higher settlement. This violates which policy condition?",
        "scenario", "standard",
        "The concealment or fraud condition voids the policy if the insured intentionally misrepresents or conceals material facts, including in a claim submission.",
        [
            ("Concealment and fraud", True, "Correct. Intentional misrepresentation on a claim voids the policy."),
            ("Subrogation", False, "Subrogation is the insurer's right to recover from responsible third parties after paying a claim."),
            ("Pro rata liability", False, "Pro rata liability applies when multiple policies cover the same loss."),
            ("Insurable interest", False, "Insurable interest must exist at the time of loss, not at the time of the claim."),
        ]
    ),
    (
        "Which of the following best describes subrogation in an insurance contract?",
        "multiple_choice", "standard",
        "Subrogation gives the insurer the right to step into the insured's shoes and pursue recovery from the responsible third party after paying a claim.",
        [
            ("The insurer's right to recover from a responsible third party after paying the insured's claim.", True, "Correct. Subrogation prevents the insured from collecting twice for the same loss."),
            ("The insured's right to cancel the policy and receive a pro-rata premium refund.", False, "This describes the cancellation condition."),
            ("The insurer's right to inspect the insured's property before issuing a policy.", False, "This describes the inspection right, not subrogation."),
            ("The insured's obligation to pay the premium on time to keep coverage in force.", False, "This describes the premium payment condition."),
        ]
    ),
    (
        "All of the following make an insurance contract unique compared to other contracts EXCEPT:",
        "multiple_choice", "standard",
        "Insurance contracts are unique because they are aleatory, unilateral, and contracts of adhesion. They are NOT unique for requiring written signatures.",
        [
            ("Insurance contracts must always be signed in writing to be valid.", True, "Correct — this is NOT unique or necessarily true. Binders can create oral coverage."),
            ("Insurance contracts are aleatory — the exchange of value is unequal.", False, "Aleatory IS a unique characteristic of insurance contracts."),
            ("Insurance contracts are unilateral — only the insurer makes a legally enforceable promise.", False, "Unilateral IS a unique characteristic of insurance contracts."),
            ("Insurance contracts are contracts of adhesion — drafted by one party.", False, "Contract of adhesion IS a unique characteristic of insurance contracts."),
        ]
    ),
],

"property-fundamentals": [
    (
        "A homeowner's house is destroyed by fire. The insurer pays the cost to rebuild with new materials of like kind and quality. This is an example of:",
        "scenario", "standard",
        "Replacement cost coverage pays the cost to repair or replace damaged property with new materials of like kind and quality, without deducting for depreciation.",
        [
            ("Replacement cost coverage", True, "Correct. Replacement cost pays to rebuild without depreciation deduction."),
            ("Actual cash value coverage", False, "ACV = replacement cost minus depreciation. It would pay less than full rebuilding cost."),
            ("Agreed value coverage", False, "Agreed value is a predetermined amount agreed upon at policy inception."),
            ("Functional replacement cost", False, "Functional replacement cost replaces with less expensive but functionally equivalent materials."),
        ]
    ),
    (
        "Under an actual cash value policy, a 5-year-old roof (10-year life expectancy) is destroyed. The replacement cost is $10,000. What does the insurer pay before the deductible?",
        "scenario", "standard",
        "ACV = Replacement Cost - Depreciation. The roof is 50% through its life, so ACV = $10,000 - $5,000 = $5,000.",
        [
            ("$5,000", True, "Correct. The roof is 50% depreciated, so ACV = $10,000 x 50% = $5,000."),
            ("$10,000", False, "This would be the replacement cost value, not ACV."),
            ("$7,500", False, "This would reflect 25% depreciation, not 50%."),
            ("$0, because the roof was not new at the time of loss.", False, "ACV policies do pay claims — they just reduce payment for depreciation."),
        ]
    ),
    (
        "Which of the following perils would be covered under an open perils (special form) property policy but NOT under a basic form policy?",
        "multiple_choice", "standard",
        "Open perils covers all perils except those specifically excluded. Basic form only covers named perils. Theft is not on the basic form named-peril list but IS covered under open perils unless excluded.",
        [
            ("Theft", True, "Correct. Theft is not a basic form named peril but is covered under open perils unless excluded."),
            ("Fire", False, "Fire is covered under all forms — basic, broad, and special."),
            ("Lightning", False, "Lightning is a named peril covered under the basic form."),
            ("Windstorm", False, "Windstorm is a named peril covered under the basic form."),
        ]
    ),
    (
        "A building has a replacement cost of $200,000. The owner insures it for $120,000 under a policy with an 80% coinsurance requirement. A $40,000 partial loss occurs. How much does the insurer pay?",
        "scenario", "hard",
        "Coinsurance formula: (Amount carried / Amount required) x Loss. Required = $200,000 x 80% = $160,000. Paid = ($120,000 / $160,000) x $40,000 = $30,000.",
        [
            ("$30,000", True, "Correct. ($120,000 divided by $160,000) x $40,000 = $30,000. The owner bears 25% as a coinsurance penalty."),
            ("$40,000", False, "The full $40,000 would only be paid if the building were insured to the required amount."),
            ("$24,000", False, "This would result from an incorrect coinsurance calculation."),
            ("$120,000", False, "The policy limit is not the payment amount for a partial loss."),
        ]
    ),
    (
        "Under a property policy, 'proximate cause' refers to:",
        "multiple_choice", "standard",
        "Proximate cause is the dominant, efficient cause that sets a chain of events in motion resulting in a loss.",
        [
            ("The dominant cause that sets the chain of events leading to the loss in motion.", True, "Correct. The proximate cause determines whether the loss is covered under the policy."),
            ("The most recent event that contributed to the loss.", False, "The proximate cause is the dominant cause, not necessarily the most recent one."),
            ("Any contributing factor that played a role in the loss.", False, "This describes a contributing cause, not the proximate cause."),
            ("The cause identified by the insured on the claim form.", False, "Proximate cause is a legal determination, not self-reported."),
        ]
    ),
],

"casualty-fundamentals": [
    (
        "Under a liability policy, the duty to defend means:",
        "multiple_choice", "standard",
        "The duty to defend is broader than the duty to indemnify. The insurer must provide a legal defense even if the suit is groundless, false, or fraudulent.",
        [
            ("The insurer must provide a legal defense for the insured even if the claim is groundless or fraudulent.", True, "Correct. The duty to defend is triggered by allegations that could potentially be covered."),
            ("The insured must cooperate with the insurer's investigation of the claim.", False, "This describes the insured's duty to cooperate, not the insurer's duty to defend."),
            ("The insurer will pay damages only if the insured is found legally liable.", False, "This describes the duty to indemnify, which is narrower than the duty to defend."),
            ("The insured must defend themselves and seek reimbursement from the insurer.", False, "Under most liability policies, the insurer assumes the defense directly."),
        ]
    ),
    (
        "Which of the following is NOT a required element to prove negligence?",
        "multiple_choice", "standard",
        "The four elements of negligence are: duty, breach of duty, proximate cause, and damages. Intent is NOT an element — negligence is unintentional by definition.",
        [
            ("Intent to cause harm", True, "Correct — intent is NOT required. Negligence is by definition unintentional."),
            ("A legal duty owed to the injured party", False, "Duty is the first required element of negligence."),
            ("Actual damages suffered by the injured party", False, "Damages are required — without harm, there is no negligence claim."),
            ("A causal connection between the breach and the injury", False, "Proximate cause is a required element of negligence."),
        ]
    ),
    (
        "A customer slips on a wet floor in a grocery store and breaks their arm. The store's general liability policy covers this under which coverage part?",
        "scenario", "standard",
        "Premises and operations coverage under a CGL policy covers bodily injury arising from the insured's premises or ongoing operations.",
        [
            ("Premises and operations liability", True, "Correct. Slip and fall injuries on the insured's premises are covered under premises liability."),
            ("Products and completed operations liability", False, "This covers injuries caused by products sold or completed work, not slip and fall on premises."),
            ("Personal and advertising injury", False, "This covers offenses like libel, slander, and copyright infringement."),
            ("Medical payments only, with no liability coverage", False, "Medical payments is a no-fault coverage, but the primary coverage is premises liability."),
        ]
    ),
    (
        "Under a claims-made liability policy, coverage applies to:",
        "multiple_choice", "standard",
        "A claims-made policy covers claims first made (reported) during the policy period, regardless of when the injury occurred (subject to the retroactive date).",
        [
            ("Claims first reported during the policy period, subject to the retroactive date.", True, "Correct. Claims-made coverage is triggered by when the claim is reported, not when the injury occurred."),
            ("Injuries that occur during the policy period, regardless of when reported.", False, "This describes an occurrence policy, not a claims-made policy."),
            ("Only claims involving bodily injury, not property damage.", False, "Claims-made policies can cover both bodily injury and property damage."),
            ("Claims reported within 30 days after the policy expires.", False, "Extended reporting periods may extend the window, but only if purchased separately."),
        ]
    ),
    (
        "An insured is sued for $80,000. The insurer pays the $80,000 judgment AND $12,000 in defense costs. The policy limit is $100,000. How much of the limit remains?",
        "scenario", "standard",
        "Defense costs under a standard liability policy are supplementary payments paid in ADDITION to the policy limit, not deducted from it. The full $100,000 limit remains available for damages.",
        [
            ("$20,000 — defense costs do not erode the liability limit under standard policies.", True, "Correct. Supplementary payments including defense costs are outside and in addition to the limit."),
            ("$8,000 — both the judgment and defense costs reduce the available limit.", False, "Defense costs are supplementary payments outside the limit under standard liability policies."),
            ("$0 — the total of $92,000 exhausts the $100,000 limit.", False, "Defense costs do not reduce the liability limit under standard policies."),
            ("$100,000 — no payments reduce the limit until a final judgment.", False, "The $80,000 judgment does reduce the available limit; only defense costs are outside the limit."),
        ]
    ),
],

"personal-auto": [
    (
        "Under a Personal Auto Policy, which coverage pays for damage to the insured's own vehicle caused by collision with another car?",
        "multiple_choice", "standard",
        "Collision coverage pays for damage to the insured's vehicle caused by impact with another vehicle or object, or by rollover, regardless of fault.",
        [
            ("Collision coverage", True, "Correct. Collision covers damage to the insured's own vehicle from impact with another car or object."),
            ("Liability coverage", False, "Liability pays for damage the insured causes to others, not to their own vehicle."),
            ("Comprehensive coverage", False, "Comprehensive covers non-collision losses such as theft, fire, hail, and flood."),
            ("Uninsured motorist property damage", False, "UMPD covers the insured's vehicle when hit by an uninsured driver, not a general collision."),
        ]
    ),
    (
        "An insured is struck by a driver who has no auto insurance. Which PAP coverage pays for the insured's medical bills?",
        "scenario", "standard",
        "Uninsured motorist bodily injury (UMBI) coverage pays for the insured's injuries when caused by a driver who has no liability insurance.",
        [
            ("Uninsured motorist bodily injury coverage", True, "Correct. UMBI covers the insured's injuries caused by an at-fault uninsured driver."),
            ("Medical payments coverage", False, "Med Pay covers medical bills regardless of fault, but UMBI specifically addresses uninsured at-fault drivers."),
            ("Collision coverage", False, "Collision covers vehicle damage, not medical bills."),
            ("Personal injury protection", False, "PIP is a no-fault coverage available in PIP states, not specifically for uninsured driver situations."),
        ]
    ),
    (
        "A friend borrows the insured's car with permission and causes an accident. Under the PAP, which statement is correct?",
        "scenario", "standard",
        "Under the PAP, coverage follows the car. A permissive user driving with the named insured's permission is covered as an insured under the policy.",
        [
            ("The friend is covered as a permissive user under the named insured's policy.", True, "Correct. Coverage follows the vehicle — permissive users are covered under the owner's PAP."),
            ("The friend's own auto policy is the only policy that covers the accident.", False, "The vehicle owner's policy is primary; the driver's own policy may be excess."),
            ("There is no coverage because the named insured was not driving.", False, "Coverage follows the car and extends to permissive users."),
            ("The friend is covered only if they have their own auto insurance.", False, "Permission to use the vehicle triggers coverage under the owner's policy."),
        ]
    ),
    (
        "The split limits 25/50/25 on an auto liability policy mean:",
        "multiple_choice", "standard",
        "Split limits: per-person BI / per-occurrence BI / per-occurrence PD. 25/50/25 = $25,000 per person BI, $50,000 per occurrence BI, $25,000 per occurrence PD.",
        [
            ("$25,000 per person BI / $50,000 per occurrence BI / $25,000 per occurrence PD", True, "Correct. The three numbers represent per-person BI, per-occurrence BI, and per-occurrence PD limits."),
            ("$25,000 deductible / $50,000 collision limit / $25,000 comprehensive limit", False, "Split limits apply to liability coverage, not deductibles or physical damage."),
            ("$25,000 liability / $50,000 medical payments / $25,000 uninsured motorist", False, "Split limits describe a single liability limit structure, not three separate coverages."),
            ("$25,000 property damage / $50,000 bodily injury / $25,000 uninsured motorist", False, "The correct reading is BI per person / BI per occurrence / PD per occurrence."),
        ]
    ),
    (
        "Under the PAP, which of the following vehicles would NOT be covered?",
        "multiple_choice", "standard",
        "The PAP covers private passenger autos. Motorcycles have fewer than 4 wheels and are not covered under the standard PAP.",
        [
            ("A motorcycle owned by the named insured.", True, "Correct. Motorcycles are not covered under the standard PAP."),
            ("A newly purchased sedan reported to the insurer within 14 days.", False, "Newly acquired autos are covered under the PAP if reported within the required time frame."),
            ("A rental car used temporarily while the insured's car is being repaired.", False, "Non-owned autos used temporarily are covered under the PAP."),
            ("A trailer designed for use with a private passenger auto.", False, "Non-motorized trailers designed for use with covered autos are covered under the PAP."),
        ]
    ),
],

"homeowners": [
    (
        "Under a homeowners policy, Coverage A (Dwelling) covers:",
        "multiple_choice", "standard",
        "Coverage A covers the dwelling structure itself and structures attached to it. Detached structures, personal property, and liability are covered under other coverages.",
        [
            ("The dwelling structure and attached structures such as an attached garage.", True, "Correct. Coverage A covers the main dwelling and structures attached to it."),
            ("All personal property inside the home up to the policy limit.", False, "Personal property is covered under Coverage C."),
            ("Detached structures on the premises such as a detached garage.", False, "Detached structures are covered under Coverage B, typically at 10% of Coverage A."),
            ("Additional living expenses if the home is uninhabitable after a loss.", False, "Additional living expenses are covered under Coverage D."),
        ]
    ),
    (
        "A homeowner's policy has a $1,000 deductible. A fire causes $15,000 in damage. The next week, a separate windstorm causes $800 in damage. How much does the insurer pay for the windstorm loss?",
        "scenario", "standard",
        "The deductible applies per occurrence. The $800 windstorm loss is less than the $1,000 deductible, so the insurer pays nothing for that claim.",
        [
            ("$0 — the loss is less than the per-occurrence deductible.", True, "Correct. The $800 loss does not exceed the $1,000 deductible."),
            ("$800 — the deductible was already satisfied by the fire claim.", False, "Homeowners deductibles apply per occurrence, not once per year."),
            ("$200 — the amount exceeding half the deductible.", False, "The deductible is applied in full to each separate occurrence."),
            ("$1,000 — the insurer pays the deductible amount on each claim.", False, "The insurer pays the loss minus the deductible, not the deductible itself."),
        ]
    ),
    (
        "Which loss would be covered under an HO-3 open perils form for the dwelling?",
        "multiple_choice", "standard",
        "HO-3 covers the dwelling on an open perils basis — all perils except those specifically excluded. Flood and earthquake are excluded.",
        [
            ("Sudden accidental discharge of water from a burst pipe.", True, "Correct. Sudden and accidental water damage from plumbing is covered under HO-3 open perils."),
            ("Flood damage from an overflowing river.", False, "Flood is a standard exclusion; separate flood insurance is required."),
            ("Earthquake damage to the foundation.", False, "Earthquake is excluded; a separate endorsement is required."),
            ("Termite damage to the floor joists.", False, "Damage by insects and pests is excluded under homeowners policies."),
        ]
    ),
    (
        "Personal property under Coverage C of the homeowners policy is covered:",
        "multiple_choice", "standard",
        "Coverage C covers the named insured's personal property on a worldwide basis.",
        [
            ("On a worldwide basis, including property away from the residence premises.", True, "Correct. Coverage C follows the insured's personal property anywhere in the world."),
            ("Only while the property is located at the insured's residence premises.", False, "Coverage C extends beyond the premises to cover property worldwide."),
            ("Only for property owned by the named insured, not by family members.", False, "Coverage C also covers personal property owned by resident family members."),
            ("On an open perils basis, the same as Coverage A under HO-3.", False, "Under HO-3, personal property is covered on a named perils basis, not open perils."),
        ]
    ),
    (
        "A homeowner operates a small accounting business from a spare bedroom. Their HO-3 policy would:",
        "scenario", "standard",
        "Standard homeowners policies exclude business pursuits and business property. Business equipment used in a home business may have limited or no coverage without an endorsement.",
        [
            ("Provide limited or no coverage for business equipment without an endorsement.", True, "Correct. Business property has strict sublimits or exclusions under standard homeowners policies."),
            ("Cover all business equipment under Coverage C up to the policy limit.", False, "Business property has strict sublimits under homeowners policies."),
            ("Cover business liability arising from the home office under Coverage E.", False, "Business liability is excluded under standard homeowners policies."),
            ("Automatically extend full coverage to any business use of the home.", False, "Business pursuits and property require endorsements for proper coverage."),
        ]
    ),
],

"dwelling-policies": [
    (
        "A dwelling policy (DP) differs from a homeowners policy primarily because:",
        "multiple_choice", "standard",
        "Dwelling policies are designed for non-owner-occupied properties or owner-occupied dwellings that don't qualify for a homeowners policy.",
        [
            ("Dwelling policies are designed for tenant-occupied or non-owner-occupied residential properties.", True, "Correct. DPs are used for rental property and properties not eligible for a homeowners policy."),
            ("Dwelling policies cover both the structure and personal property automatically.", False, "Personal property and liability must be added by endorsement under a DP."),
            ("Dwelling policies include personal liability coverage as a standard feature.", False, "Personal liability is not included in basic dwelling policies."),
            ("Dwelling policies are only available for commercial rental properties.", False, "Dwelling policies apply to residential properties."),
        ]
    ),
    (
        "Under a DP-1 (basic form) dwelling policy, which peril is covered?",
        "multiple_choice", "standard",
        "The DP-1 basic form covers only fire, lightning, and internal explosion.",
        [
            ("Fire", True, "Correct. Fire is one of the few perils covered under the DP-1 basic form."),
            ("Theft", False, "Theft is not covered under the DP-1 basic form."),
            ("Windstorm", False, "Windstorm is added in the DP-2 broad form, not the DP-1."),
            ("Vandalism", False, "Vandalism is added in the DP-2 broad form, not the DP-1."),
        ]
    ),
    (
        "A landlord rents a house to a tenant. A fire destroys the tenant's personal belongings. Which policy covers the tenant's belongings?",
        "scenario", "standard",
        "The landlord's dwelling policy protects the structure. The tenant's personal property requires the tenant's own renters insurance (HO-4).",
        [
            ("The tenant's own renters insurance policy (HO-4).", True, "Correct. The landlord's DP does not cover the tenant's personal belongings."),
            ("The landlord's dwelling policy under Coverage C.", False, "The landlord's DP covers the structure, not the tenant's belongings."),
            ("The landlord's dwelling policy automatically extends to tenants.", False, "Dwelling policies do not cover tenants' personal property."),
            ("No coverage is available for tenant personal property.", False, "Tenants can purchase HO-4 renters insurance."),
        ]
    ),
    (
        "Under a dwelling policy, 'fair rental value' coverage pays:",
        "multiple_choice", "standard",
        "Fair rental value coverage compensates the landlord for lost rental income when a covered loss makes the property uninhabitable.",
        [
            ("The landlord for lost rental income while the property is uninhabitable after a covered loss.", True, "Correct. Fair rental value = the rent lost while covered repairs are made."),
            ("The tenant for additional rent paid for temporary housing after a covered loss.", False, "Additional living expenses for a tenant would be covered under their own HO-4 policy."),
            ("The insurer for the cost of renting replacement equipment during repairs.", False, "Fair rental value applies to lost rent, not equipment rental."),
            ("The landlord for market appreciation in rental rates during the repair period.", False, "Fair rental value is based on actual rental income lost, not market appreciation."),
        ]
    ),
    (
        "The DP-3 special form dwelling policy covers the dwelling structure on what basis?",
        "multiple_choice", "standard",
        "The DP-3 covers the dwelling structure on an open perils (all-risk) basis — all perils except those specifically excluded.",
        [
            ("Open perils — all perils except those specifically excluded.", True, "Correct. DP-3 covers the dwelling open perils, the broadest dwelling form available."),
            ("Named perils — only the perils specifically listed in the policy.", False, "Named perils describes the DP-1 and DP-2 forms, not the DP-3."),
            ("Fire and lightning only.", False, "Fire and lightning only describes the DP-1 basic form."),
            ("Replacement cost with no exclusions.", False, "Open perils does not mean no exclusions; flood and earthquake are still typically excluded."),
        ]
    ),
],

"commercial-property": [
    (
        "Under the Building and Personal Property (BPP) coverage form, which of the following is NOT covered?",
        "multiple_choice", "standard",
        "Land is never covered under a property insurance policy. Land cannot be destroyed and has no insurable value.",
        [
            ("Land on which the building sits.", True, "Correct — land is NOT covered. Land cannot be destroyed and has no insurable value."),
            ("The building owned by the named insured.", False, "The building is covered under the BPP form."),
            ("Business personal property such as furniture and equipment.", False, "Business personal property is covered under the BPP form."),
            ("Personal property of others in the insured's care, custody, or control.", False, "Personal property of others is covered under the BPP up to the stated limit."),
        ]
    ),
    (
        "A fire destroys a retail store's inventory. The store closes for three months while repairs are made. Which coverage pays for the lost income?",
        "scenario", "standard",
        "Business income coverage reimburses the insured for lost income and continuing expenses during the period of restoration after a covered loss.",
        [
            ("Business income (business interruption) coverage.", True, "Correct. Business income coverage pays for lost revenue and continuing expenses during restoration."),
            ("Extra expense coverage.", False, "Extra expense covers additional costs to continue operations, not lost income."),
            ("Building and personal property coverage.", False, "BPP covers physical property damage, not income loss."),
            ("Commercial general liability coverage.", False, "CGL covers third-party liability claims, not the insured's own income loss."),
        ]
    ),
    (
        "The coinsurance clause in a commercial property policy penalizes the insured for:",
        "multiple_choice", "standard",
        "The coinsurance clause requires the insured to carry coverage equal to a specified percentage of the property's value. If underinsured, the insured bears a proportionate share of any partial loss.",
        [
            ("Insuring the property for less than the required percentage of its value.", True, "Correct. Underinsurance triggers the coinsurance penalty, reducing claim payments proportionately."),
            ("Filing more than two claims in a single policy year.", False, "Claim frequency does not trigger a coinsurance penalty."),
            ("Failing to report a loss within the required time frame.", False, "Late notice may affect coverage, but it is not a coinsurance issue."),
            ("Purchasing coverage from more than one insurer for the same property.", False, "Multiple policies trigger other-insurance provisions, not coinsurance penalties."),
        ]
    ),
    (
        "The period of restoration for business income coverage begins:",
        "multiple_choice", "standard",
        "The period of restoration begins when the physical damage occurs and ends when the property is repaired or replaced with reasonable speed.",
        [
            ("When the physical damage occurs, and ends when the property is restored to use.", True, "Correct. The period of restoration ties to the actual property repair timeline."),
            ("When the insured submits a claim to the insurer.", False, "The period begins at the time of loss, not when the claim is filed."),
            ("30 days after the loss occurs.", False, "There is typically a 72-hour waiting period, not 30 days."),
            ("On the date the policy was issued.", False, "The period is triggered by a covered loss, not the policy issuance date."),
        ]
    ),
    (
        "A warehouse stores goods for multiple customers. Which commercial property coverage form is designed for this operation?",
        "multiple_choice", "standard",
        "The Legal Liability coverage form covers the warehouse operator's legal liability for damage to customers' goods in their care.",
        [
            ("Legal liability coverage form.", True, "Correct. Legal liability covers the bailee's liability for customers' goods."),
            ("Building and personal property form.", False, "The BPP is designed for the insured's own property, not goods held for others."),
            ("Business income form.", False, "Business income covers lost revenue, not liability for customers' property."),
            ("Extra expense form.", False, "Extra expense covers additional operational costs, not property of others."),
        ]
    ),
],

"commercial-general-liability": [
    (
        "A customer is injured by a product the insured manufactured and sold two years ago. Which CGL coverage part applies?",
        "scenario", "standard",
        "Products and completed operations coverage applies to bodily injury arising from products the insured has sold or distributed.",
        [
            ("Products and completed operations liability.", True, "Correct. Injury caused by a product after it leaves the insured's hands is a products liability claim."),
            ("Premises and operations liability.", False, "Premises and operations covers injuries on the insured's premises or from ongoing operations."),
            ("Personal and advertising injury.", False, "Personal and advertising injury covers offenses like libel, slander, and false arrest."),
            ("Medical payments only.", False, "The primary coverage part for products claims is products and completed operations."),
        ]
    ),
    (
        "A CGL policy has a $1,000,000 per occurrence limit and a $2,000,000 general aggregate. Three separate claims of $800,000 each occur in one year. How much does the policy pay in total?",
        "scenario", "hard",
        "The general aggregate caps total payments. After $2,000,000 is paid (first two claims), the third claim receives no payment.",
        [
            ("$2,000,000 — the general aggregate is exhausted after the first two claims.", True, "Correct. The aggregate limits total annual payments to $2,000,000."),
            ("$2,400,000 — each claim is paid up to the per-occurrence limit.", False, "The general aggregate caps total annual payments."),
            ("$1,000,000 — only the first claim is paid in full.", False, "The aggregate allows payment up to $2,000,000 total."),
            ("$3,000,000 — all three claims are paid in full.", False, "The $2,000,000 aggregate prevents payment beyond that total."),
        ]
    ),
    (
        "An advertising agency is sued for using a competitor's slogan without permission. Which CGL coverage part applies?",
        "scenario", "standard",
        "Personal and advertising injury coverage applies to offenses including copyright infringement and misappropriation of advertising ideas.",
        [
            ("Personal and advertising injury coverage.", True, "Correct. Using another's slogan constitutes an advertising injury."),
            ("Products and completed operations.", False, "This applies to bodily injury or property damage from products or completed work."),
            ("Premises and operations.", False, "This covers injuries on premises or from operations, not intellectual property claims."),
            ("Medical payments.", False, "Medical payments is a no-fault bodily injury coverage, not applicable to advertising claims."),
        ]
    ),
    (
        "Under a CGL policy, which of the following is typically EXCLUDED?",
        "multiple_choice", "standard",
        "The CGL excludes property damage to property in the insured's care, custody, or control.",
        [
            ("Property damage to property in the insured's care, custody, or control.", True, "Correct. The care, custody, and control exclusion removes coverage for the insured's responsibilities."),
            ("Bodily injury to a customer slipping on the insured's premises.", False, "Premises slip-and-fall is a standard covered exposure under the CGL."),
            ("Property damage caused by the insured's completed work.", False, "Completed operations property damage is covered under products/completed operations."),
            ("Personal injury arising from false arrest by the insured's security staff.", False, "False arrest is a covered personal injury offense under the CGL."),
        ]
    ),
    (
        "An occurrence-based CGL policy covers:",
        "multiple_choice", "standard",
        "An occurrence-based CGL covers injuries or damage that occur during the policy period, regardless of when the claim is reported.",
        [
            ("Injuries that occur during the policy period, regardless of when the claim is filed.", True, "Correct. Occurrence coverage is triggered by when the injury happens, not when reported."),
            ("Only claims filed during the policy period.", False, "Filing during the policy period is the trigger for claims-made coverage, not occurrence."),
            ("Injuries that occur AND are reported during the policy period.", False, "Occurrence coverage does not require reporting during the policy period."),
            ("Only injuries arising from the named insured's direct actions.", False, "The CGL covers the insured's liability broadly."),
        ]
    ),
],

"business-auto": [
    (
        "Under the BAP, Symbol 7 means the policy covers:",
        "multiple_choice", "standard",
        "Symbol 7 covers specifically described autos — only the vehicles listed on the declarations page.",
        [
            ("Only the specifically described autos listed on the declarations.", True, "Correct. Symbol 7 = specifically described autos only."),
            ("Any auto owned, hired, or borrowed by the insured.", False, "This describes Symbol 1 (any auto)."),
            ("Any owned auto of the private passenger type.", False, "This describes Symbol 3."),
            ("Any auto the insured does not own but uses in the business.", False, "This describes non-owned auto coverage."),
        ]
    ),
    (
        "An employee uses their personal vehicle to make deliveries for the employer. The employer's BAP should include which coverage to protect the employer?",
        "scenario", "standard",
        "Non-owned auto liability covers the employer's liability when employees use their personal vehicles for business purposes.",
        [
            ("Non-owned auto liability coverage.", True, "Correct. Non-owned auto protects the employer when employees use personal vehicles for business."),
            ("Hired auto coverage.", False, "Hired auto covers vehicles the business rents or leases, not employee-owned vehicles."),
            ("Symbol 1 coverage for any auto.", False, "Symbol 1 is broad coverage, but the specific exposure is non-owned autos."),
            ("Physical damage coverage on the employee's vehicle.", False, "The employer is not responsible for physical damage to the employee's personal vehicle."),
        ]
    ),
    (
        "A hired auto is best described as:",
        "multiple_choice", "standard",
        "A hired auto is a vehicle the insured leases, hires, rents, or borrows from a third party other than an employee.",
        [
            ("A vehicle the insured rents or leases from a rental agency for business use.", True, "Correct. Hired autos are rented, leased, or borrowed from third parties."),
            ("Any auto used by an employee for business purposes.", False, "Employee-owned vehicles used for business are non-owned autos, not hired autos."),
            ("A vehicle owned by the insured and assigned to a specific employee.", False, "Insured-owned vehicles are covered under owned auto symbols."),
            ("Any auto the insured purchases during the policy period.", False, "Newly acquired autos are covered under owned auto provisions."),
        ]
    ),
    (
        "A company vehicle is used by an employee for personal errands without permission. An accident occurs. Under Symbol 1 (any auto) BAP, this is most likely:",
        "scenario", "standard",
        "Symbol 1 covers any auto the named insured owns, hires, or borrows. Coverage for unauthorized personal use depends on policy language, but Symbol 1 is the broadest.",
        [
            ("Covered, because Symbol 1 covers any auto including personal use of company vehicles.", True, "Correct. Symbol 1 is broad enough to cover most uses of any auto."),
            ("Excluded because the employee was on personal time.", False, "Symbol 1 does not restrict coverage to business use only."),
            ("Covered only if the employee pays back the deductible.", False, "Deductibles are not a condition for coverage determination under Symbol 1."),
            ("Excluded under all BAP symbols because it was not business use.", False, "Symbol 1 does not require business use as a condition of coverage."),
        ]
    ),
    (
        "The BAP uninsured motorist coverage protects:",
        "multiple_choice", "standard",
        "Uninsured motorist coverage pays for bodily injury to insured persons caused by an at-fault driver with no liability insurance.",
        [
            ("Insured persons injured by an at-fault uninsured driver.", True, "Correct. UM coverage protects against injury caused by drivers with no liability insurance."),
            ("Damage to the insured's vehicles caused by uninsured drivers.", False, "This describes uninsured motorist property damage (UMPD)."),
            ("The employer's vehicles when no other coverage applies.", False, "Physical damage is covered under collision/comprehensive, not UM."),
            ("All employees driving company vehicles regardless of fault.", False, "UM only applies when an uninsured driver is at fault."),
        ]
    ),
],

"workers-compensation": [
    (
        "Workers compensation provides benefits to employees who are:",
        "multiple_choice", "standard",
        "Workers compensation provides benefits for work-related injuries — those arising out of and in the course of employment. It is a no-fault system.",
        [
            ("Injured or become ill as a result of their employment, regardless of fault.", True, "Correct. Workers comp is no-fault — the employee does not need to prove negligence."),
            ("Injured only when the employer is found negligent.", False, "Workers comp is no-fault — fault is irrelevant."),
            ("Injured on company premises only.", False, "Workers comp covers work-related injuries regardless of location, including business travel."),
            ("Full-time employees only, not part-time or seasonal workers.", False, "Workers comp generally covers all employees including part-time workers."),
        ]
    ),
    (
        "Under workers compensation, an injured employee's medical bills are paid:",
        "multiple_choice", "standard",
        "Workers compensation pays medical benefits in full with no deductible or copay from the employee.",
        [
            ("In full, with no deductible or copay required from the employee.", True, "Correct. Medical benefits under WC are 100% covered with no out-of-pocket cost."),
            ("Up to $1,000,000 lifetime maximum per injury.", False, "Most states do not impose a dollar cap on workers comp medical benefits."),
            ("Only after the employee satisfies a $500 deductible.", False, "There is no deductible for the employee under workers compensation."),
            ("Only for injuries treated within the first 30 days.", False, "Workers comp medical benefits continue for as long as medically necessary."),
        ]
    ),
    (
        "An employee is permanently and totally unable to return to work after a workplace accident. Which workers compensation benefit applies?",
        "scenario", "standard",
        "Permanent total disability (PTD) benefits replace a portion of lost wages for life or as defined by state law when an employee is permanently unable to work.",
        [
            ("Permanent total disability benefits.", True, "Correct. PTD benefits provide ongoing wage replacement for workers permanently unable to work."),
            ("Temporary total disability benefits.", False, "TTD applies while the worker is temporarily unable to work during recovery."),
            ("Permanent partial disability benefits.", False, "PPD applies when a worker has permanent impairment but can still work in some capacity."),
            ("Vocational rehabilitation benefits only.", False, "Vocational rehabilitation helps workers return to employment; PTD is the primary benefit here."),
        ]
    ),
    (
        "The employers liability (Part Two) of a workers compensation policy protects the employer from:",
        "multiple_choice", "standard",
        "Part Two covers the employer for lawsuits by employees that fall outside the workers compensation exclusive remedy — such as cases involving gross negligence.",
        [
            ("Lawsuits by employees alleging negligence outside the workers compensation system.", True, "Correct. Employers liability covers suits that fall outside the WC exclusive remedy doctrine."),
            ("The cost of workers compensation benefits paid to injured employees.", False, "Benefits are covered under Part One, not Part Two."),
            ("Claims by third parties injured on the employer's premises.", False, "Third-party premises liability is covered under a CGL policy."),
            ("OSHA fines and penalties for safety violations.", False, "Workers compensation does not cover government fines or penalties."),
        ]
    ),
    (
        "The 'exclusive remedy' doctrine in workers compensation means:",
        "multiple_choice", "standard",
        "The exclusive remedy doctrine means workers compensation is the only legal remedy for work-related injuries. Employees give up the right to sue the employer in tort in exchange for guaranteed benefits.",
        [
            ("Workers compensation is the sole remedy — employees cannot sue the employer in tort.", True, "Correct. Exclusive remedy protects employers from tort suits in exchange for guaranteed WC benefits."),
            ("Employers can choose either workers compensation or tort liability, but not both.", False, "The choice belongs to the system, not the employer."),
            ("Employees must exhaust workers compensation benefits before suing the employer.", False, "Exclusive remedy bars tort suits entirely."),
            ("Workers compensation only applies if no other insurance is available.", False, "WC applies as the primary remedy regardless of other coverage."),
        ]
    ),
],

"crime-bonds-specialty": [
    (
        "A commercial crime policy's employee dishonesty coverage protects the employer from:",
        "multiple_choice", "standard",
        "Employee dishonesty coverage covers the employer for direct financial loss caused by dishonest acts of employees, including theft and embezzlement.",
        [
            ("Financial loss caused by theft or embezzlement committed by employees.", True, "Correct. Employee dishonesty protects employers against losses from their own employees' criminal acts."),
            ("Theft of business property by outsiders during a burglary.", False, "Outside theft is covered under burglary/robbery coverage."),
            ("Errors made by employees in processing financial transactions.", False, "Errors and omissions are covered under professional liability, not crime policies."),
            ("Liability to customers caused by employee misconduct.", False, "Customer liability falls under a liability policy, not a crime policy."),
        ]
    ),
    (
        "A surety bond differs from insurance primarily because:",
        "multiple_choice", "standard",
        "A surety bond is a three-party agreement where the surety guarantees the principal will fulfill an obligation. If a claim is paid, the surety has the right to recover from the principal.",
        [
            ("The surety has the right to recover (indemnification) from the principal if a loss is paid.", True, "Correct. Suretyship is not true risk transfer — the principal is ultimately responsible."),
            ("Surety bonds cover accidental losses, while insurance covers intentional acts.", False, "Insurance covers accidental losses; surety bonds guarantee performance or honesty."),
            ("Surety bonds only cover property damage, not financial losses.", False, "Surety bonds cover non-performance of obligations, which often involves financial loss."),
            ("Surety bonds are bilateral contracts between two parties.", False, "Surety bonds are three-party agreements."),
        ]
    ),
    (
        "A contractor is required by a city to post a bond guaranteeing completion of a public works project. This is a:",
        "scenario", "standard",
        "A performance bond guarantees that a contractor will complete a project according to contract terms.",
        [
            ("Performance bond.", True, "Correct. A performance bond guarantees completion of a contract."),
            ("License and permit bond.", False, "A license and permit bond guarantees compliance with laws, not completion of a specific project."),
            ("Fidelity bond.", False, "A fidelity bond protects against employee dishonesty, not contractor non-performance."),
            ("Payment bond.", False, "A payment bond guarantees the contractor will pay subcontractors, not project completion."),
        ]
    ),
    (
        "Under a commercial crime policy, 'robbery' is defined as taking property by:",
        "multiple_choice", "standard",
        "Robbery involves force, violence, or threat against a person — distinguishing it from burglary (unlawful entry) and theft (simple taking).",
        [
            ("Force, violence, or threat of violence against a person.", True, "Correct. Robbery requires a threat or act of violence against a person present."),
            ("Unlawful entry into a premises with intent to commit theft.", False, "This is the definition of burglary, not robbery."),
            ("Dishonest acts committed by an employee over time.", False, "This describes embezzlement, covered under employee dishonesty."),
            ("Taking property without the use of force or breaking and entering.", False, "This describes theft, not robbery."),
        ]
    ),
    (
        "An ocean marine insurance policy covers which of the following?",
        "multiple_choice", "standard",
        "Ocean marine insurance covers goods transported over water (cargo), the vessel itself (hull), freight revenue, and maritime liability.",
        [
            ("Cargo transported by sea and the vessel (hull) carrying it.", True, "Correct. Ocean marine covers hull, cargo, freight, and maritime liability."),
            ("Goods transported by truck across state lines.", False, "Truck transport is covered under inland marine, not ocean marine."),
            ("Workers injured aboard a commercial fishing vessel.", False, "Maritime workers are covered under the Jones Act."),
            ("Damage to a marina from a hurricane.", False, "Marina property damage would be covered under commercial property."),
        ]
    ),
],

"ethics-producer-responsibilities": [
    (
        "An insurance producer has a fiduciary duty to their clients. This means the producer must:",
        "multiple_choice", "standard",
        "A fiduciary duty requires the producer to act in the client's best interest, not their own.",
        [
            ("Act in the client's best interest and handle client funds with the highest standard of care.", True, "Correct. Fiduciary duty means the producer's interests are subordinate to the client's."),
            ("Place all policies with the insurer that pays the highest commission.", False, "Placing policies for commission rather than client benefit violates fiduciary duty."),
            ("Recommend the most comprehensive and most expensive policy available.", False, "The best policy fits the client's needs and budget, not the most expensive."),
            ("Disclose only information that is favorable to the insurer.", False, "Producers must disclose material information to clients."),
        ]
    ),
    (
        "Twisting, as defined in insurance regulation, refers to:",
        "multiple_choice", "standard",
        "Twisting is using misrepresentation to induce an insured to drop an existing policy and replace it with a new one, to the detriment of the policyholder.",
        [
            ("Misrepresenting a policy to induce an insured to drop an existing policy and replace it with a new one.", True, "Correct. Twisting uses deceptive comparisons to persuade harmful replacement."),
            ("Offering a premium discount in exchange for a referral.", False, "Offering inducements not in the policy is rebating, not twisting."),
            ("Placing a policy with an unauthorized insurer for higher commission.", False, "Placing with unauthorized insurers violates surplus lines regulations."),
            ("Failing to disclose the producer's commission to the client.", False, "Non-disclosure of commissions may be an ethical violation but is not twisting."),
        ]
    ),
    (
        "A producer submits an application knowing the applicant omitted a prior DUI conviction. The producer is guilty of:",
        "scenario", "standard",
        "Knowingly submitting false or incomplete applications violates the producer's legal and ethical obligations.",
        [
            ("Misrepresentation and potentially fraud.", True, "Correct. Knowingly submitting incomplete applications violates the producer's obligations."),
            ("Nothing, because the applicant is solely responsible for accuracy.", False, "Producers are responsible for accuracy and cannot knowingly ignore material omissions."),
            ("Twisting, because they changed the coverage terms to benefit themselves.", False, "Twisting involves misrepresenting a policy to induce switching carriers."),
            ("Rebating, because they accepted compensation for the misleading application.", False, "Rebating involves returning a portion of the premium to the insured as an inducement."),
        ]
    ),
    (
        "A producer wants to sell insurance in State B but is only licensed in State A. The producer should:",
        "scenario", "standard",
        "Producers must be licensed in each state where they conduct insurance business.",
        [
            ("Apply for a non-resident license in State B before transacting business there.", True, "Correct. Non-resident licensing allows producers to legally operate in other states."),
            ("Proceed, because their home state license covers all states.", False, "Licensing is state-specific. A State A license has no authority in State B."),
            ("Use a licensed State B agent as a front.", False, "Using a licensed agent as a front to circumvent licensing is illegal."),
            ("Request a temporary exemption from the State B insurance department.", False, "Temporary exemptions are not a standard mechanism for unlicensed producers."),
        ]
    ),
    (
        "An insurance producer receives a premium payment from a client. The producer must:",
        "multiple_choice", "standard",
        "Premium funds are fiduciary funds and must be kept in a separate trust account, not commingled with personal or business funds.",
        [
            ("Deposit the funds in a separate trust account and remit to the insurer promptly.", True, "Correct. Premium funds must be kept separate from the producer's own money."),
            ("Hold the funds until the end of the month before remitting to the insurer.", False, "Holding premium funds beyond what is reasonably necessary is a misappropriation risk."),
            ("Deposit the funds in their business operating account for convenience.", False, "Commingling client premium funds with operating accounts is prohibited."),
            ("Use the funds for business expenses, provided they are repaid before policy expiration.", False, "Using client funds for any other purpose is misappropriation — a criminal offense."),
        ]
    ),
],

"exam-prep": [
    (
        "On the P&C licensing exam, when a question asks about 'the purpose of insurance,' the best answer is:",
        "multiple_choice", "standard",
        "The fundamental purpose of insurance is to restore the insured to their pre-loss financial condition through risk pooling.",
        [
            ("To restore the insured to their pre-loss financial condition through risk pooling.", True, "Correct. Indemnity and risk pooling are the foundational purposes of insurance."),
            ("To provide a profit opportunity for policyholders who file large claims.", False, "Insurance should not result in profit — this violates indemnity."),
            ("To guarantee that insurers earn a profit on every policy written.", False, "Insurer profitability is a business goal, not the purpose of insurance."),
            ("To encourage policyholders to take greater financial risks.", False, "Moral hazard is a problem to be managed, not a purpose."),
        ]
    ),
    (
        "An exam question states an insured 'suffered a direct physical loss.' The word 'direct' means:",
        "multiple_choice", "standard",
        "A direct loss is one immediately caused by the insured peril, without an intervening cause. An indirect loss flows from the direct loss, such as lost income after a fire.",
        [
            ("The loss was immediately and directly caused by the covered peril, with no intervening cause.", True, "Correct. Direct losses are the immediate result of the peril."),
            ("The loss was witnessed by the insured in person.", False, "Whether the insured witnessed the loss is irrelevant."),
            ("The loss was reported directly to the insurer without involving an agent.", False, "The claims reporting method does not define direct vs. indirect loss."),
            ("The loss is covered without any deductible.", False, "Direct loss has nothing to do with deductibles."),
        ]
    ),
    (
        "Which strategy is most effective when unsure of an answer on the P&C licensing exam?",
        "multiple_choice", "standard",
        "Eliminate clearly wrong answers first, then select the answer most consistent with the fundamental purpose of the coverage. Extreme answers are usually wrong.",
        [
            ("Eliminate obviously wrong choices, then select the answer most consistent with the purpose of insurance.", True, "Correct. Process of elimination combined with core principles is the most reliable strategy."),
            ("Choose the longest answer, as it is usually the most complete.", False, "Answer length is not a reliable indicator of correctness."),
            ("Select 'All of the above' whenever it appears.", False, "'All of the above' is not always correct."),
            ("Skip difficult questions and return only if time allows.", False, "There is no penalty for guessing; always answer every question."),
        ]
    ),
    (
        "An endorsement to a policy is best described as:",
        "multiple_choice", "standard",
        "An endorsement is a written modification attached to the policy that adds, removes, or changes coverage.",
        [
            ("A written modification attached to the policy that changes, adds, or removes coverage.", True, "Correct. Endorsements modify the standard policy and become part of the contract."),
            ("A verbal agreement between the insured and agent to change coverage.", False, "Verbal agreements are generally not binding; changes must be in writing."),
                       ("A separate policy issued alongside the primary policy.", False, "A separate policy is not an endorsement; it is a standalone contract."),
            ("A summary of coverage provided to the insured at renewal.", False, "A renewal summary is not an endorsement."),
        ]
    ),
    (
        "A coverage exclusion in an insurance policy:",
        "multiple_choice", "standard",
        "Exclusions remove specific perils, property, or situations from coverage that would otherwise be covered by the insuring agreement.",
        [
            ("Removes specific perils or situations from coverage otherwise provided by the insuring agreement.", True, "Correct. Exclusions narrow the broad coverage granted by the insuring agreement."),
            ("Expands coverage beyond the standard policy form.", False, "Expansions are added by endorsement, not exclusion."),
            ("Defines the terms used throughout the policy.", False, "Definitions are found in the definitions section of the policy."),
            ("Sets the premium the insured must pay for coverage.", False, "Premiums are set by the declarations page and underwriting, not exclusions."),
        ]
    ),
],

}  # end REAL_QUESTIONS


def main():
    create_all()
    db = SessionLocal()
    try:
        # Remove all existing questions and choices
        existing = db.scalars(select(Question)).all()
        deleted = 0
        for q in existing:
            for c in q.choices:
                db.delete(c)
            db.delete(q)
            deleted += 1
        db.flush()
        print(f"Deleted {deleted} existing questions.")

        loaded = 0
        for module_slug, questions in REAL_QUESTIONS.items():
            module = db.scalar(select(Module).where(Module.slug == module_slug))
            if not module:
                print(f"  WARNING: Module '{module_slug}' not found — skipping {len(questions)} questions.")
                continue

            # Find a lesson in this module to associate questions with (optional)
            lesson = db.scalar(select(Lesson).where(Lesson.module_id == module.id))

            for q_text, q_type, difficulty, explanation, choices in questions:
                q = Question(
                    module_id=module.id,
                    lesson_id=lesson.id if lesson else None,
                    question_text=q_text,
                    question_type=q_type,
                    difficulty=difficulty,
                    explanation=explanation,
                    is_active=True,
                )
                db.add(q)
                db.flush()

                for sort_order, (choice_text, is_correct, rationale) in enumerate(choices):
                    db.add(AnswerChoice(
                        question_id=q.id,
                        choice_text=choice_text,
                        is_correct=is_correct,
                        sort_order=sort_order,
                    ))
                loaded += 1

        db.commit()
        print(f"Loaded {loaded} real exam questions across {len(REAL_QUESTIONS)} modules.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
