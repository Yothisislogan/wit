#!/usr/bin/env python3
"""
load_questions_batch2.py
Run from pc-license-prep-server-v2/ directory:
    .venv/bin/python3 scripts/load_questions_batch2.py

Adds 70 additional real P&C licensing exam questions (5 per module, 14 modules).
Does NOT delete existing questions — appends to the current bank.
All questions cover different concepts from batch 1.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_all
from app.models import Module, Lesson, Question, AnswerChoice
from sqlalchemy import select

BATCH2_QUESTIONS = {

"insurance-basics": [
    (
        "Which of the following best illustrates the concept of 'insurable interest'?",
        "multiple_choice", "standard",
        "Insurable interest means the policyholder would suffer a direct financial loss if the insured property is damaged or the insured person dies. It must exist at the time of application for life insurance and at the time of loss for property insurance.",
        [
            ("A homeowner insuring their own house against fire.", True, "Correct. The homeowner has a direct financial interest in the house — they would suffer a loss if it burned down."),
            ("A neighbor insuring the house next door hoping it burns down.", False, "This describes a wagering contract, not insurable interest. The neighbor would profit, not suffer a loss."),
            ("An investor buying a life insurance policy on a stranger.", False, "Insurable interest requires a financial relationship — strangers have no insurable interest in each other."),
            ("A tenant insuring the landlord's building for its full value.", False, "A tenant may insure their personal property but not the landlord's building, since they don't own it."),
        ]
    ),
    (
        "A peril is best defined as:",
        "multiple_choice", "standard",
        "A peril is the direct cause of loss — the event that triggers the insurance claim. Examples include fire, theft, and windstorm. A hazard increases the likelihood or severity of a peril occurring.",
        [
            ("The direct cause of a loss, such as fire, theft, or windstorm.", True, "Correct. A peril is the event that directly causes the loss."),
            ("A condition that increases the chance or severity of a loss.", False, "This describes a hazard, not a peril."),
            ("The financial amount the insured must pay before coverage applies.", False, "This describes a deductible, not a peril."),
            ("The maximum amount an insurer will pay for a covered loss.", False, "This describes a policy limit, not a peril."),
        ]
    ),
    (
        "A moral hazard in insurance refers to:",
        "multiple_choice", "standard",
        "A moral hazard arises from the character or dishonesty of the insured — the tendency to be less careful about preventing losses, or even to cause losses intentionally, because insurance will cover them.",
        [
            ("The tendency of an insured to be less careful or act dishonestly because they are insured.", True, "Correct. Moral hazard stems from the insured's character or behavior after obtaining insurance."),
            ("A physical condition of the property that increases the likelihood of loss.", False, "Physical conditions describe physical hazards, not moral hazards."),
            ("The legal requirement that an insured have a financial stake in the insured item.", False, "This describes insurable interest, not a moral hazard."),
            ("The transfer of risk from the insured to the insurer through a premium payment.", False, "This describes the mechanism of insurance, not a moral hazard."),
        ]
    ),
    (
        "Under the principle of utmost good faith, an insurance applicant is required to:",
        "multiple_choice", "standard",
        "Utmost good faith (uberrimae fidei) requires both parties to an insurance contract to disclose all material facts honestly. The applicant must volunteer all information that would affect the insurer's decision to insure or the premium charged.",
        [
            ("Disclose all material facts that would affect the insurer's decision, even if not asked.", True, "Correct. Utmost good faith goes beyond answering questions — it requires volunteering material information."),
            ("Answer only the specific questions asked on the application form.", False, "This falls short of utmost good faith, which requires disclosure of all material facts."),
            ("Provide proof of loss within 60 days of any covered loss.", False, "This describes a policy condition, not utmost good faith at application."),
            ("Pay the premium on time to keep the policy in force.", False, "Premium payment is a policy condition, not the duty of utmost good faith."),
        ]
    ),
    (
        "The concept of 'adverse selection' means that:",
        "multiple_choice", "standard",
        "Adverse selection occurs when people with higher-than-average risk are more likely to seek insurance than those with lower risk. This skews the insured pool toward worse risks, potentially making the insurer's loss predictions inaccurate.",
        [
            ("People with higher risk are more likely to seek insurance than those with lower risk.", True, "Correct. Adverse selection skews the insured pool toward worse-than-average risks."),
            ("Insurers select only the best risks and refuse all others.", False, "This describes underwriting, not adverse selection."),
            ("The insured selects the coverage options that are most favorable to them.", False, "Policy selection by the insured is not adverse selection in the insurance sense."),
            ("An insurer charges higher premiums to offset expected losses.", False, "This describes risk-based pricing, not adverse selection."),
        ]
    ),
],

"insurance-contracts": [
    (
        "A binder in insurance is best described as:",
        "multiple_choice", "standard",
        "A binder is a temporary agreement that provides insurance coverage immediately while the formal policy is being prepared. It is a legally binding contract even though the full policy has not yet been issued.",
        [
            ("A temporary agreement providing immediate insurance coverage while the policy is being issued.", True, "Correct. A binder creates enforceable coverage before the formal policy is delivered."),
            ("A written endorsement that permanently modifies the policy.", False, "An endorsement modifies an existing policy; a binder provides temporary coverage."),
            ("A document listing all exclusions that apply to the policy.", False, "Exclusions are listed in the policy itself, not in a binder."),
            ("A summary of coverage mailed to the insured after the policy is issued.", False, "This describes a certificate of insurance or declarations page, not a binder."),
        ]
    ),
    (
        "Under a property insurance policy, the 'other insurance' clause with pro rata liability means:",
        "multiple_choice", "standard",
        "Pro rata liability means each insurer pays its proportionate share of a loss based on the ratio of its policy limit to the total insurance covering the property. This prevents the insured from collecting more than the actual loss.",
        [
            ("Each insurer pays its proportionate share of the loss based on its policy limit relative to total coverage.", True, "Correct. Pro rata prevents double recovery by splitting the loss proportionally among insurers."),
            ("The first insurer to receive the claim pays the entire loss.", False, "This describes a primary/excess arrangement, not pro rata."),
            ("The insurer with the highest limit pays first, then the others contribute.", False, "This describes a layered excess program, not pro rata liability."),
            ("The insured must choose which policy will respond to each claim.", False, "The insured cannot choose which insurer pays; pro rata divides the loss automatically."),
        ]
    ),
    (
        "The 'reasonable expectations' doctrine in insurance law holds that:",
        "multiple_choice", "standard",
        "The reasonable expectations doctrine provides that courts will honor the reasonable expectations of policyholders regarding coverage, even if the technical policy language would deny the claim, when those expectations were created by the insurer's marketing or conduct.",
        [
            ("Courts may honor what a policyholder reasonably expected to be covered, even if policy language is ambiguous.", True, "Correct. The doctrine protects policyholders when ambiguous language or insurer conduct created reasonable coverage expectations."),
            ("Insurers can deny all claims that exceed the policyholder's reasonable expectation of loss.", False, "This is not what the doctrine means — it protects policyholders, not insurers."),
            ("Policyholders must read the full policy before coverage is enforceable.", False, "Requiring full reading before coverage is not the reasonable expectations doctrine."),
            ("Claims must be reported within a reasonable time to be covered.", False, "This describes a notice condition, not the reasonable expectations doctrine."),
        ]
    ),
    (
        "A 'warranty' in an insurance contract differs from a 'representation' because:",
        "multiple_choice", "standard",
        "A warranty is a statement guaranteed to be absolutely true — any breach voids the policy regardless of materiality. A representation is a statement believed to be true; only material misrepresentations void the policy.",
        [
            ("A warranty must be strictly true or the policy is void; a representation only voids the policy if materially false.", True, "Correct. Warranties require strict compliance; representations require only substantial truth."),
            ("A warranty is made after the policy is issued; a representation is made at application.", False, "Both may be made at application; the difference is the standard of truth required."),
            ("A warranty covers additional perils; a representation limits coverage.", False, "Warranties and representations are statements, not coverage provisions."),
            ("A warranty is made by the insurer; a representation is made by the insured.", False, "Both warranties and representations are typically made by the insured at application."),
        ]
    ),
    (
        "The doctrine of waiver in insurance means:",
        "multiple_choice", "standard",
        "Waiver is the voluntary relinquishment of a known right. In insurance, if an insurer knowingly accepts a premium or takes action inconsistent with enforcing a policy condition, it may have waived its right to deny a claim based on that condition.",
        [
            ("An insurer voluntarily gives up a known right, such as the right to deny a claim for a known violation.", True, "Correct. Waiver prevents an insurer from later asserting a right it voluntarily surrendered."),
            ("The insured gives up the right to sue the insurer after accepting a partial payment.", False, "This could describe a release, not a waiver by the insurer."),
            ("The insurer waives the deductible as a goodwill gesture on small claims.", False, "While possible, this is a specific application of waiver, not the full definition of the doctrine."),
            ("The insured waives their right to subrogation against a family member.", False, "This describes a waiver of subrogation, a specific endorsement, not the general doctrine."),
        ]
    ),
],

"property-fundamentals": [
    (
        "Under a standard property policy, which of the following would be considered a 'direct loss'?",
        "multiple_choice", "standard",
        "A direct loss results immediately from the covered peril. Indirect (consequential) losses flow from the direct loss. Fire burning down a building is a direct loss; the resulting lost rental income is indirect.",
        [
            ("A fire destroys the insured building.", True, "Correct. The fire directly causes the physical damage — this is the direct loss."),
            ("Lost rental income while the building is being repaired after a fire.", False, "Lost rental income is a consequential (indirect) loss flowing from the fire damage."),
            ("Additional living expenses while the insured stays in a hotel after a fire.", False, "Additional living expenses are a consequential loss, not a direct loss."),
            ("The cost of a temporary generator while power is out after a windstorm.", False, "Extra expenses resulting from a covered loss are indirect losses."),
        ]
    ),
    (
        "A 'valued policy' differs from an 'open policy' in that:",
        "multiple_choice", "standard",
        "A valued policy pays a predetermined agreed amount upon total loss, regardless of the property's actual value at the time of loss. An open policy pays the actual cash value or replacement cost at the time of loss.",
        [
            ("A valued policy pays a pre-agreed amount on total loss; an open policy pays actual value at time of loss.", True, "Correct. Valued policies fix the payout in advance; open policies determine value at the time of loss."),
            ("A valued policy covers more perils than an open policy.", False, "The type of perils covered is unrelated to whether a policy is valued or open."),
            ("An open policy has no coverage limit; a valued policy has a maximum payout.", False, "Open policies have limits; valued policies fix the payout — the distinction is when value is determined."),
            ("A valued policy covers only real property; an open policy covers personal property.", False, "Both types of policies can cover real or personal property."),
        ]
    ),
    (
        "Under an 'agreed value' endorsement to a commercial property policy:",
        "multiple_choice", "standard",
        "The agreed value endorsement suspends the coinsurance clause. The insurer and insured agree in advance on the property's value, and the insurer will pay that amount on a total loss without applying a coinsurance penalty.",
        [
            ("The coinsurance clause is suspended, and the insurer pays the agreed amount on total loss.", True, "Correct. Agreed value eliminates the coinsurance penalty by fixing the insured value in advance."),
            ("The insurer agrees to pay replacement cost regardless of the deductible.", False, "Agreed value is about eliminating coinsurance, not about deductibles or replacement cost."),
            ("The insured agrees to accept actual cash value instead of replacement cost.", False, "Agreed value is not related to ACV vs. replacement cost valuation."),
            ("Both parties agree to use arbitration to settle all disputes.", False, "Arbitration is a dispute resolution method, not what agreed value refers to."),
        ]
    ),
    (
        "Inland marine insurance is designed primarily to cover:",
        "multiple_choice", "standard",
        "Inland marine insurance covers property in transit over land, property held by bailees, and certain types of mobile or floating property. It is broader and more flexible than standard property forms.",
        [
            ("Property in transit over land and mobile property that moves between locations.", True, "Correct. Inland marine covers goods in transit, contractor's equipment, and similar mobile property."),
            ("Only goods transported by ship on inland waterways.", False, "Ocean marine covers water transport; inland marine covers land-based transit and mobile property."),
            ("Buildings and structures at a fixed location.", False, "Fixed-location buildings are covered under commercial property or homeowners policies."),
            ("Only property owned by common carriers such as trucking companies.", False, "Inland marine covers the property being shipped as well as the carrier's liability."),
        ]
    ),
    (
        "A 'concurrent causation' situation in property insurance occurs when:",
        "multiple_choice", "standard",
        "Concurrent causation occurs when both a covered peril and an excluded peril contribute to a single loss. Courts have historically required insurers to pay when a covered peril was even a partial cause, leading to anti-concurrent causation language in modern policies.",
        [
            ("A covered peril and an excluded peril both contribute to the same loss.", True, "Correct. Concurrent causation creates coverage disputes when covered and excluded perils combine to cause a loss."),
            ("Two separate covered perils each cause independent losses in the same policy period.", False, "Separate losses from separate covered perils are straightforward; no causation dispute exists."),
            ("The insured causes a loss both accidentally and intentionally.", False, "This describes intent, not concurrent causation between covered and excluded perils."),
            ("The same property is covered by two policies simultaneously.", False, "Dual coverage creates 'other insurance' issues, not concurrent causation."),
        ]
    ),
],

"casualty-fundamentals": [
    (
        "Under a liability policy, 'occurrence' is typically defined as:",
        "multiple_choice", "standard",
        "An occurrence under a liability policy is an accident, including continuous or repeated exposure to substantially the same harmful conditions. This is broader than a single event — it can include gradual damage over time.",
        [
            ("An accident, including continuous or repeated exposure to substantially the same harmful conditions.", True, "Correct. The occurrence definition includes both sudden accidents and gradual exposures."),
            ("Any event that results in a covered claim being filed against the insured.", False, "An occurrence is defined by the event itself, not by whether a claim is filed."),
            ("A single discrete event that causes immediate and obvious bodily injury.", False, "Occurrences also include gradual exposure, not just single discrete events."),
            ("Any act or omission by the insured that violates a law or regulation.", False, "Legal violations may or may not be occurrences; the definition focuses on accidental harm."),
        ]
    ),
    (
        "The 'separation of insureds' clause in a liability policy means:",
        "multiple_choice", "standard",
        "The separation of insureds clause (also called severability of interests) means the policy applies separately to each insured, as if each were the only insured. A claim by one insured against another may therefore be covered.",
        [
            ("The policy applies separately to each insured as if they were the only insured under the policy.", True, "Correct. Severability of interests allows each insured to be treated independently for coverage purposes."),
            ("The insurer can separate covered and excluded portions of a claim and pay only the covered part.", False, "This describes allocation of covered vs. excluded loss, not separation of insureds."),
            ("Multiple insureds under one policy must file separate claims with separate deductibles.", False, "Separation of insureds is about independent coverage, not separate deductibles per insured."),
            ("The named insured and additional insureds have completely separate policy limits.", False, "They typically share limits; separation of insureds is about the coverage analysis, not separate limits."),
        ]
    ),
    (
        "Under an umbrella liability policy, the 'retained limit' refers to:",
        "multiple_choice", "standard",
        "The retained limit in an umbrella policy is the amount the insured must pay out of pocket for losses covered by the umbrella but NOT covered by underlying insurance. It is similar to a self-insured retention (SIR).",
        [
            ("The amount the insured pays for losses covered by the umbrella but not by underlying insurance.", True, "Correct. The retained limit functions like a deductible for coverage gaps not filled by underlying policies."),
            ("The maximum amount the umbrella insurer will pay over the policy period.", False, "This describes the aggregate limit, not the retained limit."),
            ("The portion of the underlying policy limits the insured must maintain.", False, "Maintenance of underlying limits is a condition of umbrella coverage, but it is not called the retained limit."),
            ("The premium the insured retains by choosing a higher deductible.", False, "Premium savings from deductibles are unrelated to the retained limit concept."),
        ]
    ),
    (
        "Comparative negligence differs from contributory negligence in that:",
        "multiple_choice", "standard",
        "Under contributory negligence, any fault by the plaintiff bars recovery entirely. Under comparative negligence, the plaintiff's damages are reduced proportionally by their percentage of fault — they can still recover even if partially at fault.",
        [
            ("Comparative negligence reduces the plaintiff's recovery proportionally; contributory negligence bars recovery entirely.", True, "Correct. Comparative negligence is more plaintiff-friendly — partial fault reduces but does not eliminate recovery."),
            ("Comparative negligence only applies to property damage; contributory negligence applies to bodily injury.", False, "Both doctrines apply to all types of negligence claims, not specific damage types."),
            ("Under comparative negligence, the defendant pays the full amount regardless of the plaintiff's fault.", False, "Under comparative negligence, the defendant's payment is reduced by the plaintiff's share of fault."),
            ("Contributory negligence is used in most states; comparative negligence is a minority rule.", False, "The reverse is true — most states use comparative negligence; contributory negligence is rare."),
        ]
    ),
    (
        "A 'claims-made' policy with a retroactive date of January 1, 2020 and a policy period of 2024 would cover:",
        "scenario", "standard",
        "A claims-made policy covers claims made during the policy period for incidents that occurred after the retroactive date. An incident in 2019 is before the retroactive date and not covered even if the claim is made in 2024.",
        [
            ("A claim made in 2024 for an incident that occurred in 2022.", True, "Correct. The incident (2022) is after the retroactive date (2020) and the claim is made during the policy period (2024)."),
            ("A claim made in 2025 for an incident that occurred in 2023.", False, "The claim is made after the policy period ended (2024) and without an extended reporting period, it is not covered."),
            ("A claim made in 2024 for an incident that occurred in 2019.", False, "The incident predates the retroactive date (January 1, 2020) and is not covered."),
            ("A claim made in 2023 for an incident that occurred in 2021.", False, "The claim is made before the current policy period (2024) — it would need to have been reported during the prior policy period."),
        ]
    ),
],

"personal-auto": [
    (
        "Under the PAP, 'medical payments coverage' differs from 'personal injury protection (PIP)' in that:",
        "multiple_choice", "standard",
        "Medical payments coverage pays medical bills for the insured and passengers regardless of fault, but only medical expenses. PIP (in no-fault states) also pays lost wages, replacement services, and funeral expenses in addition to medical bills.",
        [
            ("Med Pay covers medical expenses only; PIP also covers lost wages and other expenses.", True, "Correct. PIP is broader than Med Pay — it covers economic losses beyond medical bills."),
            ("Med Pay applies only to the named insured; PIP covers all passengers.", False, "Both Med Pay and PIP cover the named insured and passengers in the vehicle."),
            ("PIP is available in all states; Med Pay is only in no-fault states.", False, "PIP is available in no-fault states; Med Pay is available in most states."),
            ("Med Pay requires a finding of fault; PIP pays regardless of fault.", False, "Both Med Pay and PIP are no-fault coverages that pay regardless of who caused the accident."),
        ]
    ),
    (
        "Under the PAP, 'comprehensive coverage' pays for damage to the insured vehicle caused by:",
        "multiple_choice", "standard",
        "Comprehensive (also called other-than-collision or OTC) covers damage from perils other than collision — including theft, fire, hail, flood, vandalism, falling objects, and animal strikes.",
        [
            ("Theft, fire, hail, flood, vandalism, and animal strikes.", True, "Correct. Comprehensive covers all non-collision physical damage perils."),
            ("Collision with another vehicle or stationary object.", False, "Collision with other vehicles or objects is covered under collision coverage, not comprehensive."),
            ("Mechanical breakdown and wear-and-tear.", False, "Mechanical breakdown is not covered under any standard auto policy coverage."),
            ("Damage caused by an uninsured driver running a red light.", False, "Damage caused by an identified at-fault uninsured driver is covered under UMPD or collision, not comprehensive."),
        ]
    ),
    (
        "The PAP 'named insured' is defined as the person named on the declarations page. Who else qualifies as an 'insured' under the liability section?",
        "multiple_choice", "standard",
        "Under the PAP liability section, insureds include the named insured, spouse, resident relatives, and any person using a covered auto with the named insured's permission.",
        [
            ("The named insured, spouse, resident relatives, and permissive users of covered autos.", True, "Correct. All four categories are insureds under the PAP liability section."),
            ("Only the named insured and their spouse listed on the declarations.", False, "Resident relatives and permissive users are also insured under the liability section."),
            ("Any licensed driver in the household regardless of permission.", False, "Drivers must use the vehicle with permission to qualify as an insured."),
            ("Only drivers listed on the policy by name.", False, "Permissive users are insured even if not specifically named on the policy."),
        ]
    ),
    (
        "A driver is involved in a hit-and-run accident and the other driver flees. The driver's PAP would respond under which coverage?",
        "scenario", "standard",
        "A hit-and-run driver qualifies as an uninsured motorist because they cannot be identified. Uninsured motorist coverage (UMBI and UMPD where available) responds to hit-and-run accidents.",
        [
            ("Uninsured motorist coverage, because an unidentified hit-and-run driver qualifies as an uninsured motorist.", True, "Correct. Most PAP uninsured motorist provisions treat hit-and-run drivers as uninsured motorists."),
            ("Collision coverage only, because the damage was caused by physical impact.", False, "While collision would also cover the vehicle damage, UM coverage responds to the liability exposure."),
            ("Comprehensive coverage, because the other driver fled the scene.", False, "Comprehensive covers non-collision perils; a hit-and-run is a collision situation."),
            ("No coverage, because the at-fault driver cannot be identified.", False, "Uninsured motorist coverage is specifically designed for situations where the at-fault driver is unidentified."),
        ]
    ),
    (
        "Under the PAP, the 'duty to cooperate' condition requires the insured to:",
        "multiple_choice", "standard",
        "The duty to cooperate requires the insured to assist the insurer in investigating and defending claims — providing statements, attending proceedings, and not voluntarily making payments or admitting liability without the insurer's consent.",
        [
            ("Assist in investigation, provide statements, and not admit liability without the insurer's consent.", True, "Correct. The cooperation condition requires active assistance and prohibits unilateral admissions."),
            ("Pay all claims directly and seek reimbursement from the insurer.", False, "Insureds should not pay claims independently — this could waive coverage."),
            ("Notify the insurer within 24 hours of any accident.", False, "Prompt notice is required, but the specific duty to cooperate goes beyond just notification."),
            ("Accept any settlement offer the insurer negotiates on their behalf.", False, "While the insurer controls the defense, the insured retains rights regarding certain settlement terms."),
        ]
    ),
],

"homeowners": [
    (
        "Under the homeowners policy, Coverage E (Personal Liability) covers the insured for:",
        "multiple_choice", "standard",
        "Coverage E covers the insured's legal liability for bodily injury or property damage to others caused by an occurrence. It pays damages the insured is legally obligated to pay and provides a defense.",
        [
            ("Legal liability for bodily injury or property damage to others caused by an occurrence.", True, "Correct. Coverage E is third-party liability coverage for the insured's legal obligations."),
            ("Medical bills for the named insured and family members injured at home.", False, "Medical bills for the named insured and household members are covered under health insurance, not Coverage E."),
            ("Damage to the insured's own personal property from a covered peril.", False, "Damage to the insured's own property is covered under Coverages A, B, and C, not E."),
            ("Lost income if the insured cannot work due to injuries sustained at home.", False, "Lost income is not covered under the homeowners policy."),
        ]
    ),
    (
        "Under Coverage F (Medical Payments to Others) in a homeowners policy, payments are made:",
        "multiple_choice", "standard",
        "Coverage F pays medical expenses for guests injured on the insured's premises, regardless of fault. It is a goodwill coverage that does not require a finding of negligence — it cannot be used by the insured or household members.",
        [
            ("Regardless of fault, for medical expenses of guests injured on the insured's premises.", True, "Correct. Med Pay to others is no-fault and applies to guests, not household members."),
            ("Only when the insured is found legally negligent.", False, "Coverage F pays without regard to fault — that is its defining feature."),
            ("For medical expenses of the named insured and household members.", False, "Coverage F covers guests and invitees, not household members."),
            ("For any injury that occurs anywhere in the world.", False, "Coverage F is limited to injuries on or arising from the insured premises, with some extensions."),
        ]
    ),
    (
        "A scheduled personal property endorsement to a homeowners policy is used to:",
        "multiple_choice", "standard",
        "A scheduled personal property endorsement (also called a floater or rider) provides broader coverage and higher limits for specific high-value items such as jewelry, fine art, firearms, or silverware that would be inadequately covered under the base policy.",
        [
            ("Provide broader coverage and higher limits for specific high-value items like jewelry or art.", True, "Correct. Scheduling items provides open-perils coverage and eliminates sublimits for those specific items."),
            ("Add replacement cost coverage to all personal property under Coverage C.", False, "A replacement cost endorsement handles all personal property; scheduling applies to specific items."),
            ("Reduce the premium by identifying items the insured does not need covered.", False, "Scheduling items typically increases the premium because it provides broader coverage."),
            ("Transfer coverage for listed items to a separate commercial property policy.", False, "Scheduled items remain under the homeowners policy with enhanced terms."),
        ]
    ),
    (
        "Under the homeowners policy, which of the following is covered under Coverage B (Other Structures)?",
        "multiple_choice", "standard",
        "Coverage B covers structures on the residence premises that are separated from the dwelling by clear space — such as a detached garage, fence, or storage shed. Coverage is typically 10% of Coverage A.",
        [
            ("A detached garage used exclusively for personal purposes.", True, "Correct. A detached garage is the classic example of an other structure covered under Coverage B."),
            ("A fence separating the insured's property from a neighbor's used for a home business.", False, "Structures used for business purposes are excluded from Coverage B."),
            ("An attached sunroom that shares a wall with the main dwelling.", False, "Attached structures are part of the dwelling under Coverage A, not Coverage B."),
            ("A tool shed rented to a neighbor for storage.", False, "Structures rented to others (except garages) are excluded from Coverage B."),
        ]
    ),
    (
        "The homeowners policy excludes which of the following losses?",
        "multiple_choice", "standard",
        "Earth movement (including earthquake, landslide, and subsidence) is a standard exclusion under homeowners policies. Separate earthquake insurance is required.",
        [
            ("Damage caused by earthquake or earth movement.", True, "Correct. Earth movement is a standard exclusion; separate earthquake coverage is required."),
            ("Fire damage to the dwelling caused by a lightning strike.", False, "Fire is a covered peril under all homeowners forms, including fire caused by lightning."),
            ("Theft of personal property from an insured's vehicle.", False, "Theft of personal property from a vehicle is covered under Coverage C, subject to sublimits."),
            ("Vandalism to a vehicle parked in the insured's driveway.", False, "Vandalism to the dwelling and structures is covered; vehicle vandalism is a PAP matter."),
        ]
    ),
],

"dwelling-policies": [
    (
        "Which dwelling policy form provides the broadest coverage for the dwelling structure?",
        "multiple_choice", "standard",
        "The DP-3 special form covers the dwelling structure on an open perils (all-risk) basis, making it the broadest of the three dwelling forms. DP-1 is most restrictive (fire only), DP-2 is broader (named perils).",
        [
            ("DP-3 (special form), which covers the dwelling on an open perils basis.", True, "Correct. DP-3 is the broadest form, covering all perils except those specifically excluded."),
            ("DP-1 (basic form), which covers the widest range of perils.", False, "DP-1 is the most restrictive form, covering only fire, lightning, and internal explosion."),
            ("DP-2 (broad form), which is broader than DP-3.", False, "DP-2 is a named perils form; DP-3 (open perils) is broader."),
            ("All three DP forms provide identical coverage for the dwelling structure.", False, "The three forms differ significantly in the breadth of perils covered."),
        ]
    ),
    (
        "Under a DP-3 dwelling policy, personal property (if covered) is insured on what basis?",
        "multiple_choice", "standard",
        "Under DP-3, the dwelling is covered on open perils but personal property is covered on a named perils basis — only the perils specifically listed in the policy. This is an important distinction from homeowners HO-3.",
        [
            ("Named perils — only perils specifically listed in the policy.", True, "Correct. Under DP-3, personal property has named perils coverage even though the dwelling has open perils."),
            ("Open perils — all perils except those specifically excluded.", False, "Open perils applies to the dwelling under DP-3, but personal property is on a named perils basis."),
            ("Actual cash value only, with no peril restrictions.", False, "The valuation method (ACV vs. RC) is separate from whether coverage is open or named perils."),
            ("The same open perils basis as the dwelling structure.", False, "Personal property under DP-3 is named perils, not open perils."),
        ]
    ),
    (
        "An owner-occupied dwelling that does not qualify for a homeowners policy because it is in poor condition would most likely be insured under:",
        "scenario", "standard",
        "Dwelling policies are used for properties that don't qualify for homeowners policies, including those in poor condition, vacant properties, and properties owned by investors or landlords.",
        [
            ("A dwelling policy (DP form).", True, "Correct. Dwelling policies cover properties ineligible for homeowners policies, including substandard condition dwellings."),
            ("A commercial property policy.", False, "Commercial property policies cover non-residential or commercial structures, not owner-occupied homes."),
            ("A renters insurance policy (HO-4).", False, "HO-4 is for tenants, not property owners."),
            ("A mobile home policy.", False, "Mobile home policies are specific to manufactured housing, not conventional dwellings in poor condition."),
        ]
    ),
    (
        "Under a dwelling policy, 'additional living expense' coverage pays:",
        "multiple_choice", "standard",
        "Additional living expense coverage (also called loss of use) pays the extra costs the insured incurs to maintain their normal standard of living while their home is being repaired after a covered loss.",
        [
            ("Extra costs incurred by the insured to maintain their normal standard of living during repairs.", True, "Correct. ALE pays only the extra expense above what the insured would normally spend."),
            ("The full cost of the insured's temporary housing, regardless of normal living costs.", False, "ALE pays only the additional expense above normal — if rent was $1,000 and hotel is $1,500, ALE pays $500."),
            ("Lost rental income for the landlord while the property is being repaired.", False, "Lost rental income is covered under 'fair rental value,' not additional living expense."),
            ("All living expenses including food and utilities during the repair period.", False, "ALE covers only the additional (extra) costs, not normal living expenses the insured would incur anyway."),
        ]
    ),
    (
        "A dwelling policy can be written to cover a property on a replacement cost basis if:",
        "multiple_choice", "standard",
        "Replacement cost coverage on a dwelling policy typically requires that the property be insured to at least 80% of its replacement cost value. Otherwise, the policy defaults to actual cash value.",
        [
            ("The property is insured to at least 80% of its replacement cost value.", True, "Correct. Meeting the 80% coinsurance requirement enables replacement cost settlement under most dwelling policies."),
            ("The insured pays an additional premium regardless of the insured amount.", False, "Meeting the replacement cost threshold is required, not just paying extra premium."),
            ("The property is less than 10 years old at the time of policy issuance.", False, "Property age is not the determining factor for replacement cost eligibility."),
            ("The insured has never filed a prior claim on the property.", False, "Prior claims history does not determine replacement cost eligibility."),
        ]
    ),
],

"commercial-property": [
    (
        "Under a commercial property policy, 'extra expense' coverage pays for:",
        "multiple_choice", "standard",
        "Extra expense coverage pays the additional costs above normal operating expenses that a business incurs to continue operating after a covered loss. It is often used by businesses that cannot afford to shut down, like newspapers or hospitals.",
        [
            ("Additional costs above normal to continue operations after a covered loss.", True, "Correct. Extra expense covers costs like renting temporary space or equipment to keep the business running."),
            ("Lost income during the period the business is unable to operate.", False, "Lost income is covered under business income (business interruption) coverage, not extra expense."),
            ("Expenses to rebuild the damaged property faster than normal.", False, "Expediting expenses may be covered, but extra expense broadly covers all additional operating costs."),
            ("The cost of replacing inventory lost in a covered loss.", False, "Inventory is covered under the building and personal property form, not extra expense."),
        ]
    ),
    (
        "A commercial property policy is issued with a blanket limit covering multiple buildings. This differs from a specific limit policy because:",
        "multiple_choice", "standard",
        "A blanket limit covers multiple buildings or locations under a single combined limit. A specific limit assigns a separate limit to each building or location. Blanket coverage provides more flexibility but typically requires meeting an 80% or 90% coinsurance requirement on the total value.",
        [
            ("A blanket limit applies to all covered buildings combined; a specific limit applies separately to each.", True, "Correct. Blanket coverage pools the limit across all locations; specific coverage assigns limits per location."),
            ("A blanket policy covers more perils than a specific policy.", False, "Blanket vs. specific refers to how limits are structured, not which perils are covered."),
            ("A specific limit policy does not require coinsurance; a blanket policy does.", False, "Both types may have coinsurance requirements; blanket policies typically require higher coinsurance percentages."),
            ("A blanket policy only covers property at the primary location listed on the declarations.", False, "A blanket policy is specifically designed to cover multiple locations under one limit."),
        ]
    ),
    (
        "Under commercial property coverage, 'business personal property' includes all of the following EXCEPT:",
        "multiple_choice", "standard",
        "Business personal property includes furniture, fixtures, equipment, inventory, and improvements made by tenants. It does NOT include accounts receivable, which requires a separate inland marine coverage.",
        [
            ("Accounts receivable records.", True, "Correct. Accounts receivable are covered under a separate inland marine form, not standard BPP."),
            ("Furniture and fixtures used in the business.", False, "Furniture and fixtures are covered under business personal property."),
            ("Stock (inventory) held for sale.", False, "Inventory held for sale is covered under business personal property."),
            ("Leasehold improvements made by a tenant to the building.", False, "Tenant improvements and betterments are covered under business personal property."),
        ]
    ),
    (
        "The 'ordinance or law' exclusion in a commercial property policy means:",
        "multiple_choice", "standard",
        "The ordinance or law exclusion excludes the increased cost of rebuilding to current building codes after a covered loss. If a 1960s building must be rebuilt to current codes (requiring sprinklers, handicap access, etc.), the extra cost is excluded unless an ordinance or law endorsement is purchased.",
        [
            ("Increased costs to rebuild in compliance with current building codes are excluded without an endorsement.", True, "Correct. Standard policies exclude the extra cost of code upgrades; an endorsement is needed for coverage."),
            ("The policy excludes losses caused by violations of local ordinances by the insured.", False, "Ordinance violations may be excluded under other provisions, but the ordinance or law exclusion specifically addresses code-upgrade costs."),
            ("Coverage is excluded for any building constructed before local zoning laws were enacted.", False, "Pre-code construction is not the basis of the ordinance or law exclusion."),
            ("The insurer can deny claims based on any local law the insured has violated.", False, "The exclusion is specifically about additional rebuilding costs from code compliance, not about all law violations."),
        ]
    ),
    (
        "Under the commercial property cause of loss forms, which form provides the broadest coverage?",
        "multiple_choice", "standard",
        "The special cause of loss form provides open perils coverage — all causes of loss are covered unless specifically excluded. Basic and broad forms cover only specifically named perils.",
        [
            ("Special cause of loss form — open perils coverage.", True, "Correct. The special form covers all causes of loss except those specifically excluded."),
            ("Basic cause of loss form — covers the most common perils.", False, "The basic form is the most restrictive, covering only a short list of named perils."),
            ("Broad cause of loss form — covers more perils than the special form.", False, "The broad form is more comprehensive than basic but less comprehensive than special."),
            ("All three forms provide identical coverage for commercial buildings.", False, "The three forms differ significantly — basic has the fewest covered perils, special has the most."),
        ]
    ),
],

"commercial-general-liability": [
    (
        "Under a CGL policy, 'personal and advertising injury' coverage includes which of the following offenses?",
        "multiple_choice", "standard",
        "Personal and advertising injury covers offenses including libel, slander, false arrest, malicious prosecution, wrongful eviction, invasion of privacy, copyright infringement, and misappropriation of advertising ideas.",
        [
            ("Libel and slander committed in the course of advertising the insured's products.", True, "Correct. Libel and slander are classic personal and advertising injury offenses."),
            ("Bodily injury caused by the insured's advertising activities.", False, "Bodily injury from advertising activities falls under bodily injury liability, not personal and advertising injury."),
            ("Property damage caused by the insured's completed advertising materials.", False, "Property damage is covered under the bodily injury and property damage liability section, not personal and advertising injury."),
            ("Workers compensation claims filed by employees involved in advertising.", False, "Workers compensation is a separate coverage; CGL excludes employee injury claims."),
        ]
    ),
    (
        "A CGL policy excludes coverage for bodily injury to employees of the insured arising out of their employment. This is because:",
        "multiple_choice", "standard",
        "The CGL excludes employee bodily injury because this exposure is covered under workers compensation insurance. The CGL is designed for third-party (non-employee) liability.",
        [
            ("Employee injuries are covered under workers compensation, which is a separate mandatory coverage.", True, "Correct. Workers comp is the exclusive remedy for employee injuries; the CGL is for third-party claims."),
            ("The CGL only covers property damage, not bodily injury to any person.", False, "The CGL covers both bodily injury and property damage to third parties."),
            ("Employee injuries are always the employee's own fault and therefore uninsurable.", False, "Workers comp covers employees regardless of fault; it is simply a different coverage."),
            ("The policy only covers incidents that occur off the insured's premises.", False, "The CGL covers both on-premises and off-premises occurrences."),
        ]
    ),
    (
        "Under a CGL policy, the 'products-completed operations hazard' includes:",
        "multiple_choice", "standard",
        "The products-completed operations hazard includes bodily injury or property damage occurring away from the insured's premises and arising from the insured's product or work that has been completed.",
        [
            ("Bodily injury arising from the insured's product after it has left the insured's control.", True, "Correct. Once a product leaves the insured's possession, it falls under the products-completed operations hazard."),
            ("Injury occurring on the insured's premises from a product manufactured there.", False, "On-premises injuries from manufacturing fall under premises and operations, not products-completed operations."),
            ("Only damage caused by products the insured manufactures, not those it distributes.", False, "The hazard covers both manufactured and distributed products."),
            ("Completed operations coverage expires once the insured stops selling the product.", False, "Completed operations coverage extends for a specified period after work is completed or products are sold."),
        ]
    ),
    (
        "A contractor finishes building a deck in June. In September, the deck collapses and injures the homeowner. Under the contractor's CGL, this claim falls under:",
        "scenario", "standard",
        "Once the contractor's work is complete and accepted, any injury arising from it falls under the completed operations portion of the products-completed operations coverage.",
        [
            ("Completed operations coverage, because the work was finished and accepted before the injury.", True, "Correct. Injuries from completed work after it is turned over are completed operations claims."),
            ("Premises and operations, because the injury occurred at a construction site.", False, "The work was completed and the premises were no longer a construction site when the injury occurred."),
            ("Personal and advertising injury, because the homeowner may sue for misrepresentation.", False, "Personal and advertising injury covers specific offenses like libel, not workmanship claims."),
            ("No coverage, because the policy excludes damage to the insured's work.", False, "Bodily injury to the homeowner is covered; the 'your work' exclusion applies to property damage to the work itself."),
        ]
    ),
    (
        "The CGL's 'fire legal liability' coverage protects the insured for:",
        "multiple_choice", "standard",
        "Fire legal liability (also called damage to premises rented to you) covers the named insured's liability for fire damage to a premises they rent. The CGL generally excludes property damage to property in the insured's care, but carves out an exception for fire damage to rented premises.",
        [
            ("Fire damage caused by the insured to a premises they rent from another party.", True, "Correct. Fire legal liability covers the insured's liability for fire damage to their rented space."),
            ("Fire damage to the insured's own property caused by a third party.", False, "Fire legal liability covers the insured's liability for damage to others' property, not the insured's own property."),
            ("All property damage caused by fire on the insured's premises.", False, "Fire legal liability is specifically for damage to rented premises, not all fire damage."),
            ("Injuries to firefighters responding to a fire on the insured's premises.", False, "Bodily injury to third parties is covered under the main bodily injury liability section, not specifically under fire legal liability."),
        ]
    ),
],

"business-auto": [
    (
        "Under the BAP, 'covered autos' are determined by:",
        "multiple_choice", "standard",
        "Covered autos under the BAP are determined by numerical symbols on the declarations page. Each symbol defines which vehicles are covered — from Symbol 1 (any auto) to Symbol 9 (non-owned autos only).",
        [
            ("Numerical symbols on the declarations page that define which vehicles are covered.", True, "Correct. BAP symbols (1-9) precisely define the scope of covered autos for each coverage."),
            ("A list of vehicle VINs attached as an endorsement to the policy.", False, "Symbol 7 (specifically described autos) uses a schedule of VINs, but symbols broadly define coverage."),
            ("The vehicle's use — only autos used primarily for business are covered.", False, "Coverage is determined by symbols, not by whether the vehicle is primarily used for business."),
            ("The weight of the vehicle — only vehicles under 10,000 pounds GVW are covered.", False, "Vehicle weight is not the determining factor for BAP covered auto status."),
        ]
    ),
    (
        "Under the BAP, 'drive other car' (DOC) coverage is important for:",
        "multiple_choice", "standard",
        "Drive other car coverage provides personal auto-type coverage for company executives or employees who are provided with a company car and therefore do not own a personal auto. Without DOC, they have no coverage when driving a rented or borrowed vehicle.",
        [
            ("Executives provided with a company car who have no personal auto policy of their own.", True, "Correct. DOC fills the gap for individuals who rely entirely on a company-provided vehicle and have no personal policy."),
            ("Employees who drive their personal vehicles for company business.", False, "Employee personal vehicle use is covered under non-owned auto liability."),
            ("Vehicles the company rents for occasional business use.", False, "Rented vehicles are covered under hired auto coverage, not DOC."),
            ("All employees who are listed as additional insureds on the BAP.", False, "DOC is specifically for individuals who would otherwise have no personal auto coverage."),
        ]
    ),
    (
        "A trucking company's BAP would typically be written on which symbol?",
        "multiple_choice", "standard",
        "Trucking and motor carrier operations typically use Symbol 1 (any auto) or Symbol 7 (specifically described autos) depending on the fleet. Symbol 9 (non-owned autos) would be inadequate for a trucking company.",
        [
            ("Symbol 1 (any auto) to cover all owned, hired, and borrowed vehicles.", True, "Correct. Symbol 1 provides the broadest coverage and is appropriate for trucking operations."),
            ("Symbol 9 (non-owned autos only) to reduce premium costs.", False, "Symbol 9 covers only non-owned autos — a trucking company needs coverage for its own fleet."),
            ("Symbol 3 (private passenger autos only) for all company drivers.", False, "Symbol 3 covers only passenger cars; trucking companies operate commercial trucks."),
            ("Symbol 5 (owned autos subject to no-fault) for all vehicles.", False, "Symbol 5 is limited to no-fault states and specific auto types, inappropriate for a general trucking operation."),
        ]
    ),
    (
        "Under the BAP physical damage coverage, 'specified causes of loss' is similar to which personal auto coverage?",
        "multiple_choice", "standard",
        "Specified causes of loss under the BAP covers a named list of perils (fire, lightning, theft, windstorm, hail, earthquake, flood, and a few others). This is similar to comprehensive coverage in the PAP but is a named perils form rather than open perils.",
        [
            ("Comprehensive coverage in the PAP, but on a named perils rather than open perils basis.", True, "Correct. Specified causes of loss covers selected non-collision perils, similar to but narrower than comprehensive."),
            ("Collision coverage in the PAP, covering impact with other objects.", False, "Collision coverage is a separate BAP physical damage option, not similar to specified causes of loss."),
            ("Medical payments coverage in the PAP, covering injuries to vehicle occupants.", False, "Medical payments is a liability-adjacent coverage; specified causes of loss is physical damage coverage."),
            ("Uninsured motorist coverage in the PAP, covering damage from uninsured drivers.", False, "UM is a liability coverage; specified causes of loss is physical damage coverage."),
        ]
    ),
    (
        "An employer may be vicariously liable for an employee's auto accident under the doctrine of:",
        "multiple_choice", "standard",
        "Respondeat superior is the doctrine that holds employers liable for the negligent acts of employees acting within the scope of their employment. This is why employers need BAP coverage for employee-driven vehicles.",
        [
            ("Respondeat superior — employers are liable for employees acting within the scope of employment.", True, "Correct. Respondeat superior makes the employer vicariously liable for employee negligence on the job."),
            ("Res ipsa loquitur — the accident speaks for itself and implies negligence.", False, "Res ipsa loquitur is an evidentiary doctrine, not the basis for employer liability."),
            ("Subrogation — the employer recovers from the employee after paying the claim.", False, "Subrogation is the right to recover from responsible parties, not a basis for imposing liability."),
            ("Estoppel — the employer is prevented from denying liability after accepting the employee's work.", False, "Estoppel prevents a party from asserting a position inconsistent with prior conduct; it is not the basis of employer vehicle liability."),
        ]
    ),
],

"workers-compensation": [
    (
        "Which of the following is NOT a benefit provided by workers compensation insurance?",
        "multiple_choice", "standard",
        "Workers compensation provides medical benefits, disability income (TTD, PPD, TPD, PTD), vocational rehabilitation, and death benefits. It does NOT cover pain and suffering — that is available only through a tort lawsuit, which WC's exclusive remedy doctrine generally bars.",
        [
            ("Compensation for pain and suffering.", True, "Correct. Workers comp does not pay for pain and suffering — only for economic losses."),
            ("Medical treatment for work-related injuries.", False, "Medical benefits are a core WC benefit."),
            ("Partial wage replacement during temporary total disability.", False, "TTD wage replacement is a core WC benefit."),
            ("Death benefits for dependents of a fatally injured worker.", False, "Death benefits for eligible dependents are a core WC benefit."),
        ]
    ),
    (
        "Under workers compensation, 'temporary partial disability' (TPD) benefits apply when:",
        "scenario", "standard",
        "Temporary partial disability (TPD) benefits apply when an injured worker can return to work in a limited capacity at reduced wages during recovery. TPD supplements the difference between pre-injury wages and current reduced wages.",
        [
            ("The worker returns to light-duty work at a reduced wage while still recovering.", True, "Correct. TPD supplements the wage difference when a partially recovered worker earns less than before the injury."),
            ("The worker is completely unable to work for a period but will eventually fully recover.", False, "This describes temporary total disability (TTD), not TPD."),
            ("The worker has a permanent impairment but can still perform some type of work.", False, "Permanent impairment with continued work capacity describes permanent partial disability (PPD)."),
            ("The worker is permanently and totally unable to perform any work.", False, "This describes permanent total disability (PTD)."),
        ]
    ),
    (
        "A workers compensation policy's experience modification factor (mod) above 1.0 means:",
        "multiple_choice", "standard",
        "An experience modification factor (EMR or mod) above 1.0 means the employer has had worse-than-average losses for their industry, resulting in a premium surcharge. A mod below 1.0 means better-than-average experience and a premium credit.",
        [
            ("The employer has worse-than-average loss experience and pays a premium surcharge.", True, "Correct. A mod > 1.0 increases the premium; a mod < 1.0 decreases it."),
            ("The employer qualifies for a premium discount due to favorable loss history.", False, "A premium discount requires a mod below 1.0, not above."),
            ("The employer's coverage limits exceed the standard state benefit levels.", False, "Coverage limits are not what the experience mod measures."),
            ("The insurer will pay more than 100% of covered losses under the policy.", False, "The mod adjusts premiums, not the benefit levels paid to injured workers."),
        ]
    ),
    (
        "Under workers compensation, the 'going and coming rule' generally means:",
        "multiple_choice", "standard",
        "The going and coming rule states that injuries sustained while commuting to or from work are generally NOT covered by workers compensation, because the employee is not yet 'in the course of employment.' Exceptions exist for traveling employees and those running errands for the employer.",
        [
            ("Injuries during the ordinary commute to and from work are generally NOT covered.", True, "Correct. The going and coming rule excludes commuting injuries from WC coverage in most cases."),
            ("Injuries at work are covered only if the employee is going toward their workstation, not leaving.", False, "Coverage applies throughout the workday, not just when going to the workstation."),
            ("All injuries occurring outside the employer's premises are excluded from coverage.", False, "WC covers off-premises injuries that occur during work activities, such as deliveries and business travel."),
            ("Employees must be going to or coming from a work-related meeting to be covered.", False, "The rule applies to ordinary commuting; the exception is when the employee is on a work errand."),
        ]
    ),
    (
        "A workers compensation policy written on a 'monopolistic state fund' basis means:",
        "multiple_choice", "standard",
        "Some states (such as Ohio, Washington, Wyoming, and North Dakota) operate monopolistic state funds, meaning employers must purchase workers compensation exclusively from the state fund — private insurance is not permitted.",
        [
            ("Workers compensation must be purchased from the state fund; private insurers are not permitted.", True, "Correct. Monopolistic states require WC to be purchased from the state fund exclusively."),
            ("The state sets uniform premium rates but allows private insurers to compete.", False, "Uniform rates with private competition describes a competitive state fund, not a monopolistic one."),
            ("Employers in the state are exempt from workers compensation requirements.", False, "Monopolistic states require WC coverage; they just require it from the state fund."),
            ("The state fund provides unlimited coverage with no policy limits.", False, "State fund coverage is governed by state statutes with defined benefit schedules."),
        ]
    ),
],

"crime-bonds-specialty": [
    (
        "Under a commercial crime policy, 'forgery or alteration' coverage protects against:",
        "multiple_choice", "standard",
        "Forgery or alteration coverage protects businesses against losses from checks, drafts, promissory notes, or similar instruments that are forged or altered — including losses from accepting forged checks from customers.",
        [
            ("Losses from forged or altered checks and financial instruments.", True, "Correct. Forgery coverage responds when the insured suffers a financial loss from forged instruments."),
            ("Theft of blank check stock before it can be used.", False, "Theft of blank checks is covered under theft or employee dishonesty, not forgery."),
            ("Computer fraud that results in unauthorized electronic funds transfers.", False, "Computer fraud is a separate crime coverage, not forgery or alteration."),
            ("Counterfeit currency accepted by the insured in the course of business.", False, "Counterfeit money acceptance is a separate coverage called 'counterfeit money' under crime policies."),
        ]
    ),
    (
        "A fidelity bond that covers all employees without naming them individually is called a:",
        "multiple_choice", "standard",
        "A blanket fidelity bond covers all employees as a group without individually naming them. A scheduled bond covers specifically named employees or positions.",
        [
            ("Blanket fidelity bond.", True, "Correct. A blanket bond covers all employees; a scheduled bond names specific employees or positions."),
            ("Scheduled fidelity bond.", False, "A scheduled bond names specific employees; it does not cover all employees automatically."),
            ("Performance bond.", False, "A performance bond guarantees contract completion, not employee honesty."),
            ("Commercial surety bond.", False, "Commercial surety bonds guarantee obligations to third parties, not employee dishonesty."),
        ]
    ),
    (
        "An 'indemnity bond' (also called a lost instrument bond) is used to:",
        "multiple_choice", "standard",
        "An indemnity or lost instrument bond provides protection to a company that reissues a lost, stolen, or destroyed stock certificate, bond, or similar instrument. The bond protects against loss if the original instrument turns up and is presented by someone else.",
        [
            ("Protect a company that reissues a lost or destroyed financial instrument.", True, "Correct. Lost instrument bonds allow reissuance by indemnifying the issuing company against double payment."),
            ("Guarantee that a contractor will pay their subcontractors.", False, "Payment bonds guarantee payment to subcontractors, not lost instrument replacement."),
            ("Cover employee theft discovered after the bond period has expired.", False, "Discovery bonds address late discovery; they don't relate to lost instrument reissuance."),
            ("Ensure that a licensed professional completes their services.", False, "Professional license bonds guarantee compliance with laws, not service completion."),
        ]
    ),
    (
        "Under a contract bond, the 'obligee' is defined as:",
        "multiple_choice", "standard",
        "In a surety bond, there are three parties: the principal (who must perform), the obligee (who requires the bond/performance), and the surety (who guarantees performance). The obligee is the party protected by the bond.",
        [
            ("The party who requires the bond and is protected if the principal fails to perform.", True, "Correct. The obligee is typically the project owner or government entity requiring the bond."),
            ("The surety company that issues the bond and guarantees performance.", False, "The surety is the guarantor, not the obligee."),
            ("The contractor who purchases the bond to guarantee their own performance.", False, "The contractor is the principal, not the obligee."),
            ("The insurance agent who places the bond with the surety company.", False, "The agent facilitates the bond but is not a party to the three-party surety relationship."),
        ]
    ),
    (
        "Aviation insurance differs from standard property and liability coverage primarily because:",
        "multiple_choice", "standard",
        "Aviation insurance is a specialty line that combines hull (physical damage to the aircraft) and liability coverages in a single policy. It requires specialized underwriting due to the unique risks and high values involved.",
        [
            ("It combines aircraft hull (physical damage) and aviation liability coverage in a single specialty policy.", True, "Correct. Aviation policies are comprehensive specialty policies combining hull and liability coverage."),
            ("Aviation insurance is written exclusively by Lloyd's of London.", False, "While Lloyd's is a major aviation insurer, domestic insurers also write aviation coverage."),
            ("Aviation policies cover only commercial airlines, not private aircraft.", False, "Aviation insurance covers private, corporate, and commercial aircraft."),
            ("Aviation liability coverage is identical to general liability coverage.", False, "Aviation liability has unique features including passenger liability, ground handling, and hangarkeeper's liability."),
        ]
    ),
],

"ethics-producer-responsibilities": [
    (
        "Rebating in insurance is defined as:",
        "multiple_choice", "standard",
        "Rebating is the practice of offering or giving something of value — such as a return of premium, gift, or special favor — as an inducement to purchase insurance. Rebating is illegal in most states because it creates unfair discrimination among policyholders.",
        [
            ("Offering or returning a portion of the premium or other inducement to purchase insurance.", True, "Correct. Rebating is illegal because it gives some buyers an unfair advantage over others."),
            ("Misrepresenting a competitor's policy to induce the insured to switch carriers.", False, "This describes twisting, not rebating."),
            ("Placing coverage with an insurer not authorized to do business in the state.", False, "This describes a violation of surplus lines regulations, not rebating."),
            ("Charging different premiums to different insureds based on risk factors.", False, "Risk-based pricing is legal underwriting; rebating involves illegal inducements."),
        ]
    ),
    (
        "A 'cease and desist order' issued by a state insurance department means:",
        "multiple_choice", "standard",
        "A cease and desist order is a regulatory action requiring a producer or insurer to stop engaging in a specific practice that violates insurance laws. Failure to comply can result in license suspension or revocation.",
        [
            ("The producer must immediately stop the specified unlawful practice.", True, "Correct. A cease and desist order is a regulatory directive to halt illegal activity."),
            ("The producer's license is immediately revoked without a hearing.", False, "A cease and desist order stops a practice; license revocation is a separate, more severe action."),
            ("The producer must pay restitution to all affected policyholders.", False, "Restitution may be required, but it is a separate requirement from a cease and desist order."),
            ("The producer is permanently banned from the insurance industry.", False, "Permanent bans require formal license revocation proceedings, not just a cease and desist order."),
        ]
    ),
    (
        "Under the concept of 'apparent authority,' a producer may bind an insurer even if they lack actual authority when:",
        "multiple_choice", "standard",
        "Apparent authority exists when the insurer's conduct leads a reasonable third party to believe the producer has authority. The insurer may be bound by the producer's actions even if the producer exceeded their actual authority.",
        [
            ("The insurer's conduct reasonably leads the policyholder to believe the producer has authority.", True, "Correct. Apparent authority is created by the principal's conduct, not the agent's claims."),
            ("The producer verbally claims to have authority granted by the insurer.", False, "A producer's own claim of authority does not create apparent authority — the insurer's conduct must create the appearance."),
            ("The producer has written authority from the policyholder to represent them.", False, "Authority from the policyholder would make the producer the policyholder's agent, not the insurer's agent."),
            ("The producer has been in business for more than five years.", False, "Length of experience does not create apparent authority."),
        ]
    ),
    (
        "When a producer is found guilty of insurance fraud, the MOST likely consequence is:",
        "multiple_choice", "standard",
        "Insurance fraud is a serious crime that results in license revocation and can result in criminal prosecution, fines, and imprisonment. The insurance department will revoke the producer's license.",
        [
            ("License revocation and possible criminal prosecution.", True, "Correct. Insurance fraud is both a regulatory violation (license revocation) and a crime (criminal prosecution)."),
            ("A written warning from the state insurance department.", False, "Insurance fraud is far more serious than a warning — it triggers revocation and criminal referral."),
            ("A mandatory continuing education requirement.", False, "CE requirements address knowledge gaps, not fraudulent conduct."),
            ("A temporary 30-day license suspension.", False, "Fraud results in revocation, not a temporary suspension."),
        ]
    ),
    (
        "A producer who places insurance with an unauthorized (non-admitted) insurer without complying with surplus lines regulations is subject to:",
        "multiple_choice", "standard",
        "Surplus lines insurance must be placed through a licensed surplus lines broker with specific regulatory requirements (documenting that coverage was unavailable from admitted carriers, filing taxes, etc.). Bypassing these requirements violates insurance law.",
        [
            ("License suspension or revocation and possible fines.", True, "Correct. Placing with an unauthorized insurer outside surplus lines procedures is an illegal act."),
            ("No penalty, because non-admitted insurers are legal in all states.", False, "Non-admitted insurers can operate, but only through proper surplus lines procedures."),
            ("A requirement to refund the commission earned on the placement.", False, "While commission refund may be ordered, the primary penalty is license action."),
            ("Mandatory binding arbitration with the insured.", False, "Arbitration is a dispute resolution method, not a regulatory penalty for unauthorized placement."),
        ]
    ),
],

"exam-prep": [
    (
        "On a P&C licensing exam, when a question uses the word 'EXCEPT' or 'NOT,' the best approach is to:",
        "multiple_choice", "standard",
        "Exception questions ask you to identify the one item that does NOT fit the category. The correct answer is the statement that is false, while the three wrong answers are all true statements.",
        [
            ("Identify the one choice that does NOT fit — the correct answer is the false or inapplicable statement.", True, "Correct. EXCEPT/NOT questions flip the logic — you are looking for the one that doesn't belong."),
            ("Choose the answer that most completely describes the concept.", False, "Choosing the most complete answer applies to positive questions, not EXCEPT/NOT questions."),
            ("Select the answer that seems most extreme or unusual.", False, "Extremes are often wrong on positive questions but are not a reliable strategy for EXCEPT questions."),
            ("Skip the question because EXCEPT questions are always trick questions.", False, "EXCEPT questions are standard exam format — skip nothing and never leave a question unanswered."),
        ]
    ),
    (
        "A P&C exam question describes an insurance scenario and asks 'which coverage applies?' The best strategy is to:",
        "multiple_choice", "standard",
        "Scenario questions require you to identify the trigger — what happened, who is affected, and what type of claim is being made. Match the event to the coverage designed to respond to that type of claim.",
        [
            ("Identify the triggering event, who is harmed, and match it to the coverage designed for that claim.", True, "Correct. Scenario questions test whether you can connect a fact pattern to the correct coverage part."),
            ("Choose the coverage with the highest limit, as it is most likely to pay the claim.", False, "Coverage limits don't determine which coverage applies — the triggering event does."),
            ("Select the coverage named in the question, even if the scenario suggests otherwise.", False, "Always analyze the scenario facts, not just the terms used in the question."),
            ("Choose 'all of the above' when multiple coverages seem to apply.", False, "Usually only one primary coverage applies; read carefully to identify the most appropriate one."),
        ]
    ),
    (
        "The P&C exam is likely to test which of the following concepts most heavily?",
        "multiple_choice", "standard",
        "State P&C licensing exams consistently emphasize fundamental principles, policy structure, and how common coverages work. Rare specialty lines and obscure endorsements are tested less frequently.",
        [
            ("Fundamental principles, standard policy structures, and how common coverages pay claims.", True, "Correct. Core concepts — indemnity, insurable interest, standard coverage triggers — dominate the exam."),
            ("Obscure endorsements and specialty lines that rarely appear in practice.", False, "The exam focuses on principles and standard coverages, not rare specialty items."),
            ("Premium calculation formulas and actuarial rating methods.", False, "Actuarial calculations are not on the producer licensing exam."),
            ("The specific laws of every state regarding cancellation and renewal.", False, "State-specific laws vary and are tested as broad principles, not state-by-state rules."),
        ]
    ),
    (
        "When studying for the P&C exam, 'spaced repetition' is effective because:",
        "multiple_choice", "standard",
        "Spaced repetition involves reviewing material at increasing intervals over time. It strengthens long-term memory more effectively than cramming because it forces active recall at the point just before forgetting.",
        [
            ("Reviewing material at increasing intervals forces active recall and strengthens long-term memory.", True, "Correct. Spaced repetition is one of the most evidence-supported study strategies for exam preparation."),
            ("Studying everything the night before concentrates the material in short-term memory.", False, "Cramming produces short-term retention but poor performance on exams days later."),
            ("Reading the same material multiple times in one session maximizes retention.", False, "Massed repetition (re-reading) is less effective than spaced retrieval practice."),
            ("Taking the exam immediately after studying eliminates the need for review.", False, "Without review over time, material is quickly forgotten regardless of initial study quality."),
        ]
    ),
    (
        "A P&C exam question asks about a 'surplus lines' policy. The key fact to remember is that surplus lines insurers:",
        "multiple_choice", "standard",
        "Surplus lines insurers are non-admitted carriers that are not licensed in the state but may write coverage for risks that admitted insurers will not cover. They are not covered by the state guaranty fund.",
        [
            ("Are not covered by the state guaranty fund if they become insolvent.", True, "Correct. The guaranty fund only protects policyholders of admitted (licensed) insurers."),
            ("Are licensed and admitted in every state where they do business.", False, "Surplus lines insurers are non-admitted — they are not licensed in the state of placement."),
            ("Can only write coverage for personal lines risks like homeowners and auto.", False, "Surplus lines typically covers unusual, high-risk, or specialty commercial risks."),
            ("Are regulated more strictly than admitted carriers in every state.", False, "Surplus lines carriers are less regulated in the placement state — that is why they are used for unusual risks."),
        ]
    ),
],

}


def load_batch2():
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

        # Safety check — don't add if already have a large bank
        from sqlalchemy import func
        existing_count = db.scalar(select(func.count()).select_from(Question))
        if existing_count and existing_count > 100:
            print(f"WARNING: DB already has {existing_count} questions. "
                  f"Run purge_bad_questions.py first if needed.")
            print("Proceeding to append batch 2 questions...")

        loaded = 0
        for module_slug, questions in BATCH2_QUESTIONS.items():
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
        total = db.scalar(select(func.count()).select_from(Question))
        print(f"Loaded {loaded} batch-2 questions.")
        print(f"Total questions in DB: {total}")
    finally:
        db.close()


if __name__ == "__main__":
    load_batch2()
