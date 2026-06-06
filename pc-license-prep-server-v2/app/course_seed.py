from __future__ import annotations

# P&C License Prep Academy — Enriched Course Seed
# State-neutral general Property & Casualty exam preparation.
# 14 modules | 15-18 terms each | 3-4 lessons each | 3 seed questions per module.
#
# Shape: DEFAULT_COURSE = {"modules": [{slug,title,description,sort_order,lessons,terms,questions}]}

RAW_MODULES = [

  # ── 1. Insurance Basics ──────────────────────────────────────────────
  ('insurance-basics', 'Insurance Basics',
   'Core language and concepts every P&C candidate needs first.',
   [
     ('what-is-insurance', 'What Is Insurance?',
      'Insurance is a contractual arrangement that transfers the financial risk of covered losses '
      'from an insured to an insurer in exchange for premium. The insurer promises to pay covered '
      'losses per the policy terms. The fundamental goal is indemnity: restoring the insured to '
      'the same financial position as before the loss, no better and no worse. Insurance relies '
      'on pooling: many insureds pay premium so funds are available to pay the few who suffer '
      'losses.'),
     ('risk-management', 'Risk and Risk Management Methods',
      'Risk is the possibility of financial loss. The five risk management methods are avoidance '
      '(eliminating the activity), reduction (lowering frequency or severity), retention '
      '(accepting the loss), sharing (dividing risk among parties), and transfer (shifting risk '
      'to another, as with insurance). Insurance is a transfer method. Risk retention is not '
      'necessarily bad; businesses intentionally retain minor losses through deductibles.'),
     ('peril-hazard', 'Peril and Hazard',
      'A peril is the cause of loss — fire, theft, wind, hail, collision. A hazard increases '
      'the chance or severity of loss. Physical hazards are tangible conditions such as faulty '
      'wiring. Moral hazard is dishonesty that increases the chance of loss to profit from '
      'insurance (arson). Morale hazard is carelessness from knowing a loss will be covered '
      '(leaving a car unlocked because it is insured).'),
     ('insurable-interest', 'Insurable Interest and Indemnity',
      'Insurable interest is the financial stake a person must have in insured property. Without '
      'it, a policy is unenforceable and becomes a wagering contract. For property, insurable '
      'interest must exist at the time of loss. Indemnity limits recovery to the actual financial '
      'loss; the insured should not profit from a loss.'),
   ],
   [
     ('Risk', 'The chance a loss could happen.', 'The uncertainty or possibility of financial loss.', 'A fire could destroy a warehouse.'),
     ('Peril', 'The cause of loss.', 'A cause of loss such as fire, theft, wind, hail, explosion, or collision.', 'Lightning strikes and burns a house; lightning is the peril.'),
     ('Physical Hazard', 'A physical condition that increases loss chance.', 'A tangible condition that increases the frequency or severity of loss.', 'Faulty wiring increases the chance of fire.'),
     ('Moral Hazard', 'Intentional dishonesty to profit from insurance.', 'A hazard arising from the dishonest character of an insured that increases the chance of loss.', 'An insured burns a failing business to collect insurance proceeds.'),
     ('Morale Hazard', 'Carelessness because insurance exists.', 'A hazard created by the indifference of an insured who knows a loss will be covered.', 'Leaving valuables in an unlocked car because theft is covered.'),
     ('Premium', 'The price paid for insurance.', 'The amount charged by the insurer in exchange for the promise to pay covered losses.', 'An insured pays $1,200 per year for homeowners coverage.'),
     ('Insurable Interest', 'A financial stake in the insured item.', 'A financial or ownership interest in the subject of insurance such that a loss causes financial harm.', 'A homeowner has insurable interest in their dwelling.'),
     ('Indemnity', 'Restoring the insured to pre-loss position.', 'The principle limiting recovery to actual financial loss, preventing profit from insurance.', 'An insured collects ACV for a destroyed vehicle, not more.'),
     ('Subrogation', 'Insurer takes the insured\'s right to collect from a third party.', 'The right of an insurer, after paying a loss, to stand in the insured\'s place and recover from a negligent third party.', 'An insurer pays a fire loss, then sues the negligent neighbor who caused it.'),
     ('Law of Large Numbers', 'Bigger pools make losses more predictable.', 'The principle that the larger the group of similar risks, the more closely actual losses match predicted losses.', 'Insurers use large driver pools to accurately predict auto claims.'),
     ('Adverse Selection', 'Higher-risk people buy more insurance.', 'The tendency for those most likely to have losses to seek insurance more aggressively.', 'People with serious health conditions seek more life insurance.'),
     ('Underwriting', 'Selecting and pricing risks.', 'The process of evaluating applications, selecting acceptable risks, and determining appropriate premium.', 'An underwriter reviews a home inspection before issuing a policy.'),
     ('Risk Transfer', 'Shifting financial risk to another party.', 'A risk management method in which financial responsibility for a loss is moved to another party, such as an insurer.', 'Buying insurance transfers fire risk to the insurer.'),
     ('Risk Retention', 'Keeping and paying for losses yourself.', 'Accepting the financial consequences of a loss, intentionally or unintentionally.', 'A business pays the first $1,000 of each loss through a deductible.'),
     ('Self-Insurance', 'Setting aside funds to pay your own losses.', 'A formal program in which a business retains risk and sets aside reserves to pay its own losses rather than buying commercial insurance.', 'A large corporation self-insures its workers compensation exposure.'),
     ('Utmost Good Faith', 'Both parties must be fully honest.', 'The duty of each party to an insurance contract to disclose all material facts honestly and completely.', 'An applicant must disclose prior losses on an application.'),
     ('Concealment', 'Hiding a material fact.', 'The intentional failure to disclose a material fact on an application, which may make a policy voidable.', 'Failing to disclose a prior arson conviction.'),
     ('Representation', 'A statement made on an application.', 'A statement made by an applicant in connection with an insurance application; must be substantially true.', 'Stating the home is owner-occupied on the application.'),
   ]),

  # ── 2. Insurance Contracts ───────────────────────────────────────────
  ('insurance-contracts', 'Insurance Contracts',
   'How insurance policies are legally structured and interpreted.',
   [
     ('policy-sections', 'The Six Parts of an Insurance Policy',
      'Most policies contain six sections. Declarations: names the insured, policy period, limits, '
      'premium. Definitions: explains terms used in the policy. Insuring Agreement: states what '
      'the insurer promises to cover. Conditions: list the duties of each party. Exclusions: '
      'remove certain causes, property, or situations. Endorsements: attached forms that add, '
      'remove, or modify coverage.'),
     ('contract-characteristics', 'Legal Characteristics of Insurance Contracts',
      'Insurance contracts are contracts of adhesion (written by the insurer; ambiguities favor '
      'the insured), aleatory (unequal exchange depending on uncertain events), conditional '
      '(insured must meet conditions to collect), unilateral (only the insurer makes an '
      'enforceable promise), and personal (coverage follows the insured, not property, and '
      'cannot be assigned without insurer consent).'),
     ('valid-contract', 'Elements of a Valid Insurance Contract',
      'A valid contract requires offer and acceptance, consideration (premium and promise to '
      'pay), competent parties, and legal purpose. Insurance also requires insurable interest '
      'and utmost good faith. Without all elements, the contract may be void or voidable.'),
     ('binders-cancellation', 'Binders, Cancellation, and Nonrenewal',
      'A binder is temporary insurance evidence providing coverage while a policy is being '
      'issued. A certificate of insurance is evidence of coverage issued to a third party. '
      'Cancellation ends a policy before expiration; most states require advance notice (10 '
      'days for nonpayment, 30 days for other reasons). Nonrenewal is the decision not to '
      'continue a policy at expiration, also requiring advance notice.'),
   ],
   [
     ('Declarations', 'The summary page of the policy.', 'The policy section listing the named insured, policy period, limits, premium, deductibles, and covered property or exposures.', 'The dec page shows the dwelling limit and annual premium.'),
     ('Insuring Agreement', 'The insurer\'s promise to pay.', 'The section stating what the insurer agrees to cover and under what circumstances.', 'The insuring agreement promises to pay for direct physical loss by covered perils.'),
     ('Conditions', 'Rules both parties must follow.', 'Provisions setting out the duties of the insured and insurer, including notice of loss, proof of loss, and cooperation.', 'The insured must give prompt notice of a loss under policy conditions.'),
     ('Exclusions', 'What the policy does not cover.', 'Provisions that limit or remove coverage for certain perils, property, persons, or situations.', 'A flood exclusion removes coverage for rising water damage.'),
     ('Endorsement', 'A form that changes the policy.', 'A written form attached to a policy that adds, removes, or modifies coverage; also called a rider.', 'A jewelry endorsement schedules a specific ring for additional coverage.'),
     ('Contract of Adhesion', 'Take it or leave it — insurer writes it.', 'A contract drafted by one party and accepted or rejected as written; ambiguities are interpreted against the drafter (insurer).', 'Courts interpret unclear policy language in favor of the insured.'),
     ('Aleatory Contract', 'One side may pay far more than the other.', 'A contract in which the values exchanged are unequal and depend on an uncertain event.', 'The insurer may pay $300,000 after the insured paid only $1,500 in premium.'),
     ('Conditional Contract', 'Coverage depends on meeting requirements.', 'A contract in which the insurer\'s obligation to pay depends on the insured fulfilling certain duties.', 'The insurer can deny a claim if the insured fails to give timely notice of loss.'),
     ('Unilateral Contract', 'Only the insurer makes a binding promise.', 'A contract in which only the insurer makes an enforceable promise to pay; the insured may cancel at any time.', 'The insured may cancel at any time; only the insurer is bound to pay covered losses.'),
     ('Consideration', 'What each side gives to make the contract binding.', 'The value exchanged: the insured\'s premium payment and the insurer\'s promise to pay covered losses.', 'Premium paid and the policy promise together form consideration.'),
     ('Binder', 'Temporary proof of insurance.', 'A temporary contract, oral or written, providing coverage until a formal policy is issued or the application is declined.', 'An agent binds auto coverage by phone while the policy is being written.'),
     ('Certificate of Insurance', 'Proof of coverage given to a third party.', 'A document issued to a third party as evidence that an insurance policy exists; does not grant rights under the policy.', 'A contractor provides a certificate to a property owner before starting work.'),
     ('Named Insured', 'The person listed on the dec page.', 'The individual or entity identified by name on the declarations page as the primary insured.', 'The company listed on the declarations page is the named insured.'),
     ('Assignment', 'Transferring policy rights to another person.', 'The transfer of rights under a policy to another party; most property policies require insurer consent.', 'A homeowner cannot assign a homeowners policy to a buyer without insurer approval.'),
     ('Cancellation', 'Ending the policy before expiration.', 'The termination of a policy before its expiration date; insurers must provide advance notice required by state law.', 'An insurer cancels a policy for nonpayment with 10 days\' notice.'),
     ('Nonrenewal', 'Choosing not to continue at expiration.', 'The insurer\'s decision not to offer to renew a policy at expiration; advance notice is required under most state laws.', 'An insurer sends nonrenewal notice 60 days before the policy expires.'),
     ('Valued Policy', 'Pays a set amount regardless of actual loss.', 'A policy paying a stated amount upon total loss without applying the indemnity principle.', 'A valued policy pays $200,000 face amount upon total loss of the dwelling.'),
     ('Warranty', 'An absolute promise by the insured.', 'A statement guaranteed to be true; breach may void the policy even if unrelated to the loss.', 'An insured warrants that a burglar alarm is operational at all times.'),
   ]),

  # ── 3. Property Insurance Fundamentals ──────────────────────────────
  ('property-fundamentals', 'Property Insurance Fundamentals',
   'First-party property concepts, valuation methods, and coinsurance.',
   [
     ('direct-vs-indirect-loss', 'Direct and Indirect Loss',
      'A direct loss is immediate physical damage to covered property from a covered peril. An '
      'indirect (consequential) loss is a financial loss resulting from the direct loss, such as '
      'loss of use, additional living expenses, fair rental value, or business income. Property '
      'policies cover direct losses by default; indirect losses require specific coverage.'),
     ('valuation', 'Replacement Cost vs Actual Cash Value',
      'Replacement cost (RC) pays to repair or replace damaged property with new property of '
      'like kind and quality without deducting depreciation. Actual cash value (ACV) is '
      'replacement cost minus depreciation. Most homeowners policies pay ACV for personal '
      'property and RC for the dwelling when coinsurance is met. An RC endorsement on contents '
      'eliminates the depreciation deduction.'),
     ('coinsurance', 'Coinsurance and the Coinsurance Penalty',
      'Coinsurance requires the insured to carry insurance equal to a stated percentage (often '
      '80%) of the property\'s value. If less is carried, the insured becomes a co-insurer and '
      'shares in losses. Formula: (Amount carried ÷ Amount required) × Loss = Maximum recovery. '
      'Example: $120,000 carried on a $200,000 building with 80% requirement yields '
      '$160,000 required; the insured collects only 75% of any loss.'),
     ('deductibles', 'Deductibles and Other Property Provisions',
      'A deductible is the insured\'s share of each loss before the insurer pays. Deductibles '
      'reduce premium and deter small claims. Vacancy (typically 60+ days with no occupants and '
      'little or no contents) can suspend certain coverages. The pair and set clause limits '
      'recovery to the difference in value of a set when one item is damaged.'),
   ],
   [
     ('Replacement Cost', 'Cost to replace with new, same quality.', 'The cost to repair or replace damaged property with new property of like kind and quality without deduction for depreciation.', 'Replacing a 5-year-old roof at today\'s cost with no depreciation deduction.'),
     ('Actual Cash Value', 'Replacement cost minus depreciation.', 'A valuation method calculated as replacement cost less depreciation due to age and wear.', 'A 10-year-old HVAC unit has depreciation deducted before payment.'),
     ('Depreciation', 'Loss of value due to age and use.', 'The decrease in property value caused by age, wear, obsolescence, or physical deterioration.', 'A roof loses value each year as it ages.'),
     ('Direct Loss', 'Physical damage to the insured property.', 'Physical damage to covered property directly caused by a covered peril.', 'Fire burns the kitchen cabinets.'),
     ('Indirect Loss', 'Financial loss resulting from direct damage.', 'A consequential financial loss resulting from direct physical damage, such as loss of use or business income.', 'Hotel costs while a fire-damaged home is being repaired.'),
     ('Business Income', 'Lost revenue during business interruption.', 'Coverage replacing net income and continuing expenses when a business suspends operations due to covered direct physical loss.', 'A restaurant covered for business income recovers lost revenue during fire repair.'),
     ('Extra Expense', 'Extra costs to stay operational after a loss.', 'Coverage for additional costs incurred to continue operations or minimize the period of suspension after a covered loss.', 'Renting temporary space to keep a business running after a fire.'),
     ('Coinsurance', 'A requirement to carry insurance equal to a percentage of value.', 'A policy provision requiring the insured to carry insurance equal to a specified percentage of value or share in losses.', 'An 80% coinsurance clause requires $160,000 on a $200,000 building.'),
     ('Coinsurance Penalty', 'The insured\'s share of loss for underinsuring.', 'The reduction in claim payment when an insured carries less than the required coinsurance amount.', 'Carrying $120,000 when $160,000 is required results in collecting only 75% of any loss.'),
     ('Deductible', 'The insured\'s share of each loss.', 'The amount the insured must pay before the insurer pays; reduces premium and discourages small claims.', 'A $1,000 deductible means the insured pays the first $1,000 of each loss.'),
     ('Agreed Value', 'A provision that waives coinsurance.', 'A policy condition under which the insurer agrees the amount of insurance is sufficient; the coinsurance clause is suspended.', 'An agreed value endorsement eliminates the coinsurance penalty for the policy period.'),
     ('Blanket Insurance', 'One limit covering multiple items or locations.', 'A policy insuring multiple items, locations, or classes of property under a single limit.', 'A blanket policy covers all five business locations under one $2 million limit.'),
     ('Specific Insurance', 'Separate limits for each item or location.', 'A policy assigning a separate amount of insurance to each specific item or location.', 'Each building is insured for its own stated limit under a specific policy.'),
     ('Debris Removal', 'Coverage for removing damaged property after a loss.', 'Coverage for the reasonable cost to remove debris of covered property after a covered peril.', 'Removing charred wood and rubble after a fire.'),
     ('Pair and Set Clause', 'Limits recovery for one item in a pair.', 'A provision limiting recovery when one item of a pair or set is lost to the difference in value of the set before and after the loss.', 'One earring is stolen; the insurer pays the value difference of the pair, not a replacement earring.'),
     ('Functional Replacement Cost', 'Replace with equally functional but less expensive material.', 'A valuation method paying the cost to replace property with less expensive but functionally equivalent modern materials.', 'Replacing ornate plaster molding with flat drywall at lower cost.'),
     ('Vacancy', 'No occupants and minimal contents.', 'A condition in which a building has no people and little or no personal property; most policies suspend certain coverages after 60 days.', 'A commercial building empty for 90 days triggers the vacancy clause.'),
     ('Subrogation', 'Insurer\'s right to recover from a responsible third party.', 'After paying a covered loss, the insurer steps into the insured\'s shoes to recover from a negligent third party who caused the loss.', 'An insurer pays a roof loss caused by a contractor\'s negligence, then sues the contractor.'),
   ]),
  # ── 4. Casualty Insurance Fundamentals ──────────────────────────────
  ('casualty-fundamentals', 'Casualty Insurance Fundamentals',
   'Liability, negligence, damages, and third-party coverage concepts.',
   [
     ('liability-basics', 'Liability Insurance Basics',
      'Liability insurance is third-party coverage: it pays others for damages the insured '
      'becomes legally obligated to pay. Liability policies typically include a duty to defend '
      '(paying defense costs) and a duty to indemnify (paying damages up to the limit). '
      'Defense costs are often paid in addition to the limit, or within the limit, depending '
      'on the policy. Most policies pay defense even for groundless or fraudulent claims.'),
     ('negligence', 'Negligence and Its Four Elements',
      'Negligence is the failure to exercise the care a reasonably prudent person would use '
      'under similar circumstances. The four elements are: (1) Duty — the defendant owed a '
      'legal duty of care; (2) Breach — the defendant breached that duty; (3) Proximate Cause '
      '— the breach directly caused the injury; (4) Damages — actual harm resulted. All four '
      'must be present for a negligence claim to succeed.'),
     ('defenses', 'Defenses to Negligence Claims',
      'Contributory negligence (rare) bars recovery if the plaintiff was at all negligent. '
      'Comparative negligence reduces recovery by the plaintiff\'s percentage of fault. '
      'Assumption of risk applies when the plaintiff knowingly accepted a known danger. '
      'Statutes of limitations require claims to be filed within a specified time period.'),
     ('policy-structures', 'Occurrence vs Claims-Made Coverage',
      'An occurrence policy covers losses that happen during the policy period, regardless '
      'of when the claim is filed. A claims-made policy covers claims first made during the '
      'policy period for events after the retroactive date. Tail coverage (extended reporting '
      'period) extends the time to report after a claims-made policy ends.'),
   ],
   [
     ('Bodily Injury', 'Physical injury or death of a person.', 'Physical injury, sickness, disease, or death of any person for which the insured may be liable.', 'A customer slips on a wet floor and breaks a wrist.'),
     ('Property Damage', 'Physical damage to someone else\'s property.', 'Physical injury to or destruction of tangible property, including loss of use of that property.', 'A contractor accidentally breaks a client\'s window.'),
     ('Personal Injury', 'Non-physical harm such as defamation or false arrest.', 'Injury arising from offenses such as false arrest, malicious prosecution, wrongful eviction, defamation, or invasion of privacy.', 'A store falsely accuses a customer of shoplifting, damaging their reputation.'),
     ('Advertising Injury', 'Injury from advertising activities.', 'Injury arising from offenses in advertising, such as libel, slander, copyright infringement, or misappropriation of advertising ideas.', 'A company uses a competitor\'s slogan without permission in its advertising.'),
     ('Negligence', 'Failure to exercise reasonable care.', 'The failure to act as a reasonably prudent person would under similar circumstances, resulting in harm to another.', 'A driver runs a stop sign and injures a pedestrian.'),
     ('Duty', 'The legal obligation to act with care.', 'The first element of negligence; a legal obligation owed by the defendant to the plaintiff to act or refrain from acting in a certain way.', 'A store owner has a duty to keep aisles free of hazards.'),
     ('Proximate Cause', 'The primary cause that leads to a loss.', 'The efficient, dominant cause setting in motion a chain of events leading to a loss; the direct cause.', 'A drunk driver running a red light is the proximate cause of an accident.'),
     ('Strict Liability', 'Liability without proof of negligence.', 'Legal responsibility imposed regardless of fault; applies to inherently dangerous activities or defective products.', 'A manufacturer is strictly liable for a defective product even without negligence.'),
     ('Vicarious Liability', 'Responsibility for another\'s actions.', 'Legal responsibility for the negligent acts of another because of their relationship, such as employer-employee.', 'An employer is vicariously liable for an employee\'s negligent acts in the course of employment.'),
     ('Respondeat Superior', 'Employer is responsible for employees\' work acts.', 'The doctrine holding an employer liable for the wrongful acts of an employee within the scope of employment.', 'A delivery driver causes an accident while working; the employer faces liability.'),
     ('Comparative Negligence', 'Each party\'s fault reduces their recovery.', 'A doctrine reducing a plaintiff\'s damages by their percentage of fault; under pure form, even a mostly at-fault plaintiff may recover.', 'A plaintiff 30% at fault in a $100,000 loss recovers only $70,000.'),
     ('Contributory Negligence', 'Any fault by plaintiff bars recovery entirely.', 'Used in few states; completely bars a plaintiff from recovering if they were at all negligent.', 'A jaywalking pedestrian recovers nothing even if the driver was primarily at fault.'),
     ('Assumption of Risk', 'Voluntary acceptance of a known danger.', 'A defense to negligence in which the plaintiff knowingly and voluntarily accepted a known risk.', 'A spectator at a baseball game assumes the risk of being struck by a foul ball.'),
     ('Occurrence Policy', 'Covers events that happen during the policy period.', 'A liability policy covering claims from occurrences during the policy period, regardless of when the claim is filed.', 'An occurrence policy written in Year 1 covers a loss that happened in Year 1 even if claimed in Year 5.'),
     ('Claims-Made Policy', 'Covers claims first reported during the policy period.', 'A liability policy covering claims first made during the policy period, provided the occurrence happened after the retroactive date.', 'A professional liability claims-made policy covers a claim reported this year for an error made last year, if after the retroactive date.'),
     ('Retroactive Date', 'The earliest date a claims-made policy will cover.', 'The date before which occurrences are excluded from coverage under a claims-made policy.', 'A policy with a January 1, 2023 retroactive date does not cover acts from 2022.'),
     ('Extended Reporting Period', 'Extra time to report after a claims-made policy ends.', 'Tail coverage; extends the period to report claims after a claims-made policy expires or is canceled.', 'A doctor buys a 3-year tail after retiring to cover future claims from past work.'),
     ('Damages', 'Money awarded to compensate an injured party.', 'Monetary compensation a court awards for losses suffered; may be compensatory (actual losses) or punitive (punishment).', 'A jury awards $50,000 in compensatory damages for medical bills and lost wages.'),
   ]),

  # ── 5. Personal Auto Insurance ───────────────────────────────────────
  ('personal-auto', 'Personal Auto Insurance',
   'Coverages, definitions, and key concepts of the Personal Auto Policy.',
   [
     ('pap-structure', 'Personal Auto Policy Structure',
      'The PAP has six parts: Part A (Liability), Part B (Medical Payments), Part C '
      '(Uninsured Motorists), Part D (Damage to Your Auto), Part E (Duties After Loss), '
      'and Part F (General Provisions). The declarations page identifies the named insured, '
      'covered autos, policy period, coverages, and limits.'),
     ('liability', 'Part A — Liability Coverage',
      'Part A pays for bodily injury or property damage the insured becomes legally responsible '
      'for in an auto accident, and pays defense costs. Coverage applies to the named insured, '
      'spouse, family members using covered autos, and others using covered autos with '
      'permission. Split limits express liability as per-person/per-accident/property damage. '
      'A combined single limit (CSL) applies one amount to all damages from one accident.'),
     ('physical-damage', 'Part D — Physical Damage Coverage',
      'Collision covers upset or impact with another vehicle or object. Other Than Collision '
      '(comprehensive) covers non-collision losses including theft, fire, hail, vandalism, '
      'flood, and animal contact. Both include a deductible. Without Part D, the insured\'s '
      'own vehicle has no physical damage coverage.'),
     ('um-uim', 'Part C — Uninsured and Underinsured Motorist Coverage',
      'Uninsured Motorist (UM) pays for the insured\'s bodily injury caused by a driver '
      'with no liability insurance or a hit-and-run driver. Underinsured Motorist (UIM) '
      'applies when the at-fault driver\'s limits are insufficient. Part B Medical Payments '
      'covers medical expenses for the insured and passengers regardless of fault.'),
   ],
   [
     ('Named Insured', 'The person listed on the dec page.', 'The individual identified on the declarations page as the primary policyholder; receives full policy rights.', 'The person who purchased the policy and is named on the dec page.'),
     ('Family Member', 'A relative living in the insured\'s household.', 'A person related by blood, marriage, or adoption living in the named insured\'s household.', 'A spouse and a child living at home are family members.'),
     ('Permissive Use', 'Using a covered auto with the owner\'s permission.', 'Use of a covered auto with express or implied consent of the named insured; the driver is covered under the owner\'s policy.', 'A friend borrowing the insured\'s car with permission is covered under permissive use.'),
     ('Owned Auto', 'A vehicle owned by the named insured.', 'A vehicle described on the declarations page, a newly acquired vehicle, a trailer owned by the named insured, or a temporary substitute vehicle.', 'The insured\'s pickup truck listed on the dec page is an owned auto.'),
     ('Non-Owned Auto', 'A vehicle the insured uses but does not own.', 'A vehicle the named insured or family member does not own and uses on a temporary basis.', 'An insured rents a car on vacation; the rental is a non-owned auto.'),
     ('Collision', 'Upset or impact with another vehicle or object.', 'Physical damage coverage for the insured\'s vehicle from collision with another vehicle or object, or from upset.', 'The insured backs into a light pole; collision covers the damage.'),
     ('Other Than Collision', 'Physical damage from non-collision causes.', 'Physical damage coverage for losses other than collision, including theft, fire, flood, vandalism, hail, and animal contact; also called comprehensive.', 'A hailstorm damages the insured\'s car; OTC coverage pays.'),
     ('Split Limits', 'Separate limits for BI per person, BI per accident, and PD.', 'A liability limit structure expressed as three numbers: per-person BI / per-accident BI / property damage.', 'A 100/300/100 policy pays up to $100,000 per person, $300,000 per accident for BI, and $100,000 for PD.'),
     ('Combined Single Limit', 'One limit for all damages in one accident.', 'A single liability limit applying to the total of bodily injury and property damage from one accident.', 'A $300,000 CSL may pay any combination of BI and PD up to $300,000 per accident.'),
     ('Uninsured Motorist', 'Coverage when the at-fault driver has no insurance.', 'Coverage paying for the insured\'s bodily injury caused by a driver with no liability insurance or a hit-and-run driver.', 'The insured is injured by an uninsured driver; UM coverage pays.'),
     ('Underinsured Motorist', 'Coverage when the at-fault driver\'s limits are too low.', 'Coverage paying when the at-fault driver\'s liability limits are insufficient to cover the insured\'s damages.', 'An at-fault driver has $25,000 in liability; the insured\'s $100,000 in damages triggers UIM.'),
     ('Medical Payments', 'Medical cost coverage regardless of fault.', 'Part B of the PAP; pays reasonable medical expenses for the insured and passengers injured in an auto accident regardless of fault.', 'The insured\'s passenger is injured; medical payments covers their hospital bill.'),
     ('Newly Acquired Auto', 'A vehicle the insured buys during the policy period.', 'A vehicle acquired by the named insured during the policy period; covered automatically for a defined period subject to notification requirements.', 'An insured buys a second vehicle mid-policy; it is automatically covered for up to 14 days.'),
     ('Financial Responsibility Law', 'State law requiring proof of ability to pay.', 'A state law requiring drivers to demonstrate financial ability to pay for auto accident damages, typically through minimum liability insurance.', 'Most states require at least $25,000 in liability coverage under financial responsibility laws.'),
     ('Personal Injury Protection', 'No-fault medical and income coverage.', 'Required in no-fault states; pays the insured\'s medical expenses, lost wages, and other costs regardless of fault.', 'A no-fault state requires PIP; the insured\'s own insurer pays medical bills even if another driver caused the accident.'),
     ('Stacking', 'Combining coverage from multiple policies or vehicles.', 'The practice of combining limits from multiple auto policies or vehicles to increase coverage; allowed in some states, prohibited in others.', 'An insured with two vehicles and $100,000 UM each may stack for $200,000 in permitted states.'),
     ('Gap Coverage', 'Covers the difference between ACV and loan balance.', 'Coverage paying the difference between the insurer\'s ACV payment for a totaled vehicle and the outstanding loan balance.', 'A new car worth $28,000 ACV has a $33,000 loan; gap coverage pays the $5,000 difference.'),
   ]),

  # ── 6. Homeowners Insurance ──────────────────────────────────────────
  ('homeowners', 'Homeowners Insurance',
   'HO policy forms, coverage parts, and key provisions.',
   [
     ('ho-forms', 'Homeowners Policy Forms',
      'HO-3 (Special Form) is the most common: open perils on the dwelling, named perils on '
      'contents. HO-2 (Broad Form): named perils on both. HO-5 (Comprehensive): open perils on '
      'both. HO-4 (Renters): personal property only, for tenants. HO-6 (Condo): unit interior '
      'and personal property. HO-8 (Modified): for older homes where RC exceeds market value.'),
     ('coverage-parts', 'The Six Coverage Parts',
      'Coverage A — Dwelling: main structure. Coverage B — Other Structures: detached garages, '
      'fences, sheds (typically 10% of A). Coverage C — Personal Property: belongings '
      '(typically 50-70% of A). Coverage D — Loss of Use/ALE (typically 20-30% of A). '
      'Coverage E — Personal Liability. Coverage F — Medical Payments to Others.'),
     ('perils', 'Named Perils vs Open Perils and Exclusions',
      'Named perils policies cover only the listed perils. Open perils (all-risk) policies '
      'cover all causes except those specifically excluded. Common exclusions: flood, earthquake, '
      'ordinance/law, sewer backup, wear and tear, intentional acts. Endorsements can add back '
      'certain excluded perils for additional premium.'),
     ('provisions', 'Important Homeowners Provisions',
      'The mortgagee clause requires the insurer to pay the lender even if the insured\'s claim '
      'is denied for the insured\'s own acts. Inflation guard automatically increases Coverage A '
      'limits. Personal property sublimits apply to jewelry, firearms, money, and silverware. '
      'Scheduled endorsements increase these sublimits. Coverage A must be maintained at the '
      'required percentage of RC to collect full replacement cost on losses.'),
   ],
   [
     ('HO-3', 'The most common homeowners form.', 'ISO form providing open perils on the dwelling and named perils on personal property.', 'The HO-3 is the standard form used by most homeowners.'),
     ('HO-4', 'Renters insurance.', 'ISO form for tenants providing named perils coverage for personal property only; does not cover the building.', 'A renter buys HO-4 to cover their belongings but not the landlord\'s structure.'),
     ('HO-5', 'Comprehensive form — open perils on everything.', 'ISO form providing open perils coverage for both the dwelling and personal property; the broadest homeowners form.', 'An HO-5 policyholder has open perils on both the house and its contents.'),
     ('HO-6', 'Condo unit owners form.', 'ISO form for condo owners covering the interior of the unit and personal property.', 'A condo owner insures the interior walls, fixtures, and belongings with an HO-6.'),
     ('HO-8', 'Modified coverage for older homes.', 'ISO form for older homes where RC substantially exceeds market value; pays functional replacement cost rather than full RC.', 'An older home with high RC but low market value may be insured on an HO-8.'),
     ('Coverage A', 'Dwelling coverage.', 'Homeowners coverage for the main residential structure and attached structures.', 'The main house and attached patio cover are Coverage A.'),
     ('Coverage B', 'Other structures coverage.', 'Homeowners coverage for structures separated from the dwelling by clear space; typically 10% of Coverage A.', 'A detached garage and backyard fence are Coverage B.'),
     ('Coverage C', 'Personal property coverage.', 'Homeowners coverage for personal belongings owned or used by an insured; worldwide subject to limits and conditions.', 'Furniture, clothing, and electronics are Coverage C.'),
     ('Coverage D', 'Loss of use or additional living expenses.', 'Homeowners coverage paying additional living expenses when the insured residence is uninhabitable due to a covered loss.', 'Hotel and restaurant costs while the home is repaired after a fire are Coverage D.'),
     ('Coverage E', 'Personal liability coverage.', 'Homeowners coverage paying for damages the insured becomes legally obligated to pay for BI or PD occurring on the premises or due to personal activities.', 'A guest slips on an icy porch; Coverage E pays the resulting judgment.'),
     ('Coverage F', 'Medical payments to others.', 'Homeowners coverage paying reasonable medical expenses for persons injured on the insured location, regardless of fault.', 'A child cuts their hand on the insured\'s fence; Coverage F pays the medical bill without a lawsuit.'),
     ('Named Perils', 'Coverage for only the listed perils.', 'A coverage basis insuring only against causes of loss that are named in the policy; the insured must prove a listed peril caused the loss.', 'HO-4 personal property coverage lists fire, theft, vandalism, and other specific perils.'),
     ('Open Perils', 'Coverage for all causes except those excluded.', 'Also called all-risk or special form; covers all causes of loss except those specifically excluded.', 'HO-3 dwelling coverage is open perils; anything not excluded is covered.'),
     ('Mortgagee Clause', 'Protects the lender\'s interest.', 'A provision requiring the insurer to pay the lender even if the insured\'s claim is denied for the insured\'s own acts.', 'If the insured commits arson, the insurer still pays the mortgagee bank for its interest.'),
     ('Additional Living Expense', 'Extra costs when home is uninhabitable.', 'The necessary increase in living expenses to maintain normal standard of living when the insured residence is uninhabitable due to a covered loss.', 'Hotel bills and restaurant meals while the home is repaired are ALE.'),
     ('Scheduled Personal Property', 'Listed high-value items at a stated amount.', 'An endorsement listing specific valuable items with individual agreed values; eliminates sublimits and may broaden coverage.', 'A $15,000 diamond ring is scheduled for its full appraised value.'),
     ('Inflation Guard', 'Automatic increase in Coverage A limits.', 'A provision or endorsement automatically increasing Coverage A limits periodically to keep pace with construction cost inflation.', 'An inflation guard endorsement increases Coverage A by 4% per year.'),
     ('Ordinance or Law', 'Extra rebuilding costs required by building codes.', 'Coverage for additional cost to repair or rebuild to meet current building codes after a covered loss.', 'After a fire, local code requires updated electrical panels; ordinance or law coverage pays the extra cost.'),
   ]),

  # ── 7. Commercial Property ───────────────────────────────────────────
  ('commercial-property', 'Commercial Property Insurance',
   'Commercial property forms, causes of loss, and key provisions.',
   [
     ('bpp-structure', 'Building and Personal Property Coverage Form',
      'The BPP covers three categories: Building (owned structures and fixtures), Business '
      'Personal Property (contents the named insured owns), and Personal Property of Others '
      '(property of customers or others in the insured\'s care, custody, or control). Each '
      'category may be insured separately or under a blanket limit.'),
     ('causes-of-loss', 'Causes of Loss Forms',
      'The Basic Form covers 11 named perils including fire, lightning, explosion, windstorm, '
      'and smoke. The Broad Form adds collapse, plumbing water damage, and falling objects. '
      'The Special Form (open perils) covers all direct physical loss except specifically '
      'excluded perils. Common exclusions: flood, earthquake, war, governmental action.'),
     ('business-income', 'Business Income and Extra Expense',
      'Business Income reimburses net income lost and continuing expenses when operations '
      'are suspended due to covered physical damage. The restoration period is the time '
      'needed to repair or replace damaged property. Extra Expense pays additional costs to '
      'continue operations. Extended business income continues coverage after restoration '
      'to account for rebuilding a customer base.'),
     ('commercial-provisions', 'Coinsurance, Deductibles, and Other Provisions',
      'Commercial property coinsurance typically requires 80%, 90%, or 100% of value at '
      'the time of loss. Agreed value suspends coinsurance. Peak season endorsements increase '
      'limits during high-inventory periods. Builders risk covers buildings under construction. '
      'Reporting forms require periodic premium reports for fluctuating inventory values.'),
   ],
   [
     ('Building', 'The structure owned by the insured.', 'Under a commercial property policy, the covered building includes the structure, permanently installed fixtures, and machinery used to service the building.', 'The insured\'s owned warehouse is the building.'),
     ('Business Personal Property', 'Contents and equipment owned by the business.', 'Movable property owned by the named insured used in the business, including furniture, fixtures, machinery, equipment, and inventory.', 'Desks, computers, and merchandise inventory are business personal property.'),
     ('Personal Property of Others', 'Property of customers in the insured\'s care.', 'Property belonging to others that the named insured has in its care, custody, or control.', 'A repair shop covers customers\' items left for service as personal property of others.'),
     ('Business Income', 'Lost revenue during business interruption.', 'Coverage replacing net income and continuing expenses when operations are suspended due to covered physical loss.', 'A fire closes a restaurant for two months; business income pays lost revenue and ongoing rent.'),
     ('Extra Expense', 'Additional costs to stay operational after a loss.', 'Coverage for extra costs incurred to continue operations or reduce the period of suspension following a covered loss.', 'Renting temporary equipment to keep the business running after flood damage.'),
     ('Causes of Loss — Basic Form', 'Eleven named perils for commercial property.', 'The most limited commercial property causes of loss form, covering fire, lightning, explosion, windstorm, hail, smoke, aircraft, vehicles, riot, vandalism, and sprinkler leakage.', 'A fire destroys a warehouse; the basic form covers it as a named peril.'),
     ('Causes of Loss — Broad Form', 'Basic perils plus collapse and water damage.', 'Commercial property causes of loss adding collapse, falling objects, water damage from plumbing, and weight of ice or snow to the basic form perils.', 'A burst pipe floods an office; broad form covers water damage from plumbing.'),
     ('Causes of Loss — Special Form', 'Open perils for commercial property.', 'The most comprehensive commercial property causes of loss form, covering all direct physical loss except specifically excluded perils.', 'A mystery cause damages merchandise; special form covers it because it is not excluded.'),
     ('Restoration Period', 'Time to repair after a covered loss.', 'The period beginning when covered property is damaged and ending when it is or could reasonably be repaired; defines the business income coverage period.', 'A factory requiring three months to rebuild has a three-month restoration period.'),
     ('Builders Risk', 'Coverage for buildings under construction.', 'A specialized property policy covering a building while it is under construction.', 'A new warehouse under construction is covered by a builders risk policy.'),
     ('Blanket Coverage', 'One limit covering multiple items or locations.', 'A structure applying a single limit of insurance to two or more items, classes of property, or locations.', 'A $5 million blanket limit covers buildings at all three company locations.'),
     ('Reporting Form', 'Coverage with periodic value reports for fluctuating inventory.', 'A commercial property form requiring the insured to periodically report property values; premium is adjusted based on actual values.', 'A retailer with seasonal inventory uses a reporting form to match premium to actual value.'),
     ('Agreed Value', 'Suspends the coinsurance clause.', 'A commercial property option in which the insurer agrees the stated amount of insurance is sufficient; the coinsurance clause is suspended.', 'An agreed value endorsement eliminates coinsurance penalties for the policy year.'),
     ('Peak Season Endorsement', 'Increases limits during high-inventory periods.', 'An endorsement temporarily increasing coverage limits during periods when inventory values are highest.', 'A toy retailer increases inventory limits from October through December with a peak season endorsement.'),
     ('Ordinance or Law', 'Covers extra rebuilding costs required by codes.', 'Coverage for additional cost to repair, rebuild, or demolish to comply with current building codes after a covered loss.', 'After a partial fire loss, code requires the entire building to be brought to current standards; ordinance or law pays the extra cost.'),
     ('Leasehold Interest', 'Value of a favorable lease lost due to a covered loss.', 'Coverage for a tenant\'s financial interest in a below-market lease that is terminated due to a covered property loss.', 'A tenant with below-market rent loses the lease after a covered fire; leasehold interest coverage pays the value of the lease advantage.'),
   ]),

  # ── 8. Commercial General Liability ─────────────────────────────────
  ('commercial-general-liability', 'Commercial General Liability (CGL)',
   'CGL coverage parts, triggers, limits, and key provisions.',
   [
     ('cgl-parts', 'CGL Coverage A, B, and C',
      'Coverage A — Bodily Injury and Property Damage: pays for BI or PD the insured is '
      'legally liable for. Coverage B — Personal and Advertising Injury: pays for non-physical '
      'injuries such as libel, slander, false arrest, or copyright infringement. Coverage C '
      '— Medical Payments: pays reasonable medical expenses for persons injured on the '
      'insured\'s premises, regardless of fault.'),
     ('cgl-triggers', 'CGL Liability Triggers',
      'The standard CGL is occurrence-based: it covers occurrences happening during the '
      'policy period regardless of when claims are filed. Products-Completed Operations '
      'coverage applies after a product leaves the insured\'s possession or after a job is '
      'completed. Claims-made CGL policies require the claim to be made during the policy '
      'period. Contractual liability assumed in an insured contract is also covered.'),
     ('cgl-limits', 'CGL Limits of Insurance',
      'Each Occurrence Limit: maximum for all damages from one occurrence. General Aggregate: '
      'maximum for all Coverage A claims in the policy period (excluding products). '
      'Products-Completed Operations Aggregate: separate aggregate for products and completed '
      'work. Coverage B has a per-offense limit. Coverage C has a per-person limit.'),
     ('cgl-exclusions', 'CGL Key Exclusions and Endorsements',
      'The CGL excludes: expected/intended injury, auto liability, workers compensation, '
      'employers liability, most pollution, professional services, and liquor liability for '
      'alcohol sellers. The Liquor Liability exclusion applies when liquor is sold. An '
      'Additional Insured endorsement extends Coverage A and B to a third party.'),
   ],
   [
     ('Coverage A', 'Bodily injury and property damage liability.', 'CGL Coverage A pays damages the insured is legally obligated to pay for bodily injury or property damage caused by an occurrence.', 'A customer slips on a wet floor; CGL Coverage A covers the resulting lawsuit.'),
     ('Coverage B', 'Personal and advertising injury liability.', 'CGL Coverage B pays for offenses such as libel, slander, false arrest, wrongful eviction, invasion of privacy, and copyright infringement.', 'A company\'s advertisement falsely implies a competitor is dishonest; Coverage B applies.'),
     ('Coverage C', 'Medical payments to injured visitors.', 'CGL Coverage C pays reasonable medical expenses for third parties injured on the insured\'s premises, without a legal liability determination.', 'A visitor is cut on exposed wiring; Coverage C pays their medical bills.'),
     ('Each Occurrence Limit', 'Maximum paid for a single occurrence.', 'The most the CGL insurer will pay for all damages from any one occurrence.', 'The $1 million each occurrence limit is the cap for all claims from one accident.'),
     ('General Aggregate Limit', 'Maximum for all Coverage A claims in a policy year.', 'The most the CGL insurer will pay for all Coverage A losses during the policy period, exclusive of products-completed operations.', 'Once $2 million in Coverage A claims are paid, the general aggregate is exhausted.'),
     ('Products-Completed Operations', 'Liability for products after delivery and completed work.', 'CGL coverage for BI or PD arising from the insured\'s products after they are sold or from work after it is completed.', 'A completed deck collapses and injures someone a year later; products-completed operations coverage applies.'),
     ('Premises and Operations', 'Liability for on-premises activities and ongoing work.', 'CGL coverage for BI or PD arising from ownership, maintenance, or use of the insured\'s premises or ongoing operations.', 'A store visitor is injured by a falling display while the store is open.'),
     ('Contractual Liability', 'Liability assumed from a written contract.', 'CGL coverage for liability assumed in an insured contract, such as a hold harmless or indemnification clause in a lease or construction agreement.', 'A tenant agrees to hold the landlord harmless for injury on premises; the CGL covers this assumed liability.'),
     ('Additional Insured', 'A third party added to the policy.', 'A person or organization added to a CGL policy by endorsement who receives certain coverage; does not receive all rights of a named insured.', 'A property owner requires a contractor\'s CGL policy to list the owner as an additional insured.'),
     ('Liquor Liability Exclusion', 'Removes coverage for alcohol-related claims.', 'A CGL exclusion removing coverage for claims arising from selling, serving, or furnishing alcoholic beverages by an insured in the business of doing so.', 'A bar must buy a separate liquor liability policy because the CGL excludes this exposure.'),
     ('Pollution Exclusion', 'Removes coverage for most pollution-related losses.', 'A CGL exclusion eliminating coverage for BI or PD from the discharge or escape of pollutants.', 'A chemical manufacturer is excluded from CGL coverage for gradual groundwater contamination.'),
     ('Insured Contract', 'A contract in which assumed liability is covered.', 'A contract for which the CGL provides contractual liability coverage, typically including lease agreements and construction contracts.', 'A lease requiring the tenant to indemnify the landlord is an insured contract under the CGL.'),
     ('Personal and Advertising Injury', 'Non-physical harm from specific offenses.', 'CGL Coverage B injury from offenses such as false arrest, malicious prosecution, wrongful eviction, libel, slander, invasion of privacy, or copyright infringement in advertising.', 'A magazine article falsely accuses a business of fraud; Coverage B applies.'),
     ('Fire Damage Legal Liability', 'Coverage for fire damage to rented premises.', 'A CGL sublimit paying for fire damage to premises rented to the named insured when the insured is legally liable.', 'A tenant\'s negligence causes a fire damaging the landlord\'s building; fire damage legal liability pays up to the sublimit.'),
     ('Products Aggregate', 'Separate maximum for products and completed work claims.', 'A separate aggregate limit applying only to products and completed operations coverage; renews each policy year.', 'Products-completed operations claims draw from the $2 million products aggregate, not the general aggregate.'),
     ('Occurrence', 'An accident or repeated exposure causing injury or damage.', 'Under the CGL, an accident including continuous or repeated exposure to the same harmful conditions, resulting in BI or PD.', 'Long-term chemical exposure over multiple policy years may be treated as one occurrence.'),
   ]),

  # ── Business Auto Insurance ─────────────────────────────────────
  ('business-auto',
   'Business Auto Insurance',
   'Commercial auto symbols, liability, and physical damage for business fleets.',
   [
     ('bap-covered-autos',
      'Business Auto Covered Auto Symbols',
      'The Business Auto Policy uses numbered symbols on the declarations page to define '
      'which autos are covered for each coverage. Symbol 1 means any auto. Symbol 7 means '
      'specifically described autos. Symbol 8 means hired autos only. Symbol 9 means '
      'non-owned autos only. The symbol controls coverage — not every auto qualifies for '
      'every coverage part.'),
     ('bap-liability',
      'BAP Liability and Physical Damage',
      'Business auto liability covers bodily injury and property damage the insured is legally '
      'responsible for from accidents involving covered autos. Physical damage covers the autos '
      'themselves: collision (impact or upset) and comprehensive/other than collision (theft, '
      'fire, hail). Medical payments and uninsured motorist coverage are optional.'),
     ('hired-nonowned',
      'Hired and Non-Owned Auto Liability',
      'Hired auto covers vehicles the business rents or borrows. Non-owned auto covers '
      'employee-owned vehicles used for business. Both protect the business, not the employee. '
      'Employees still need their own personal auto policy for their own protection.'),
   ],
   [
     ('Covered Auto Symbol', 'A code defining which autos are covered.', 'A numerical symbol on the BAP declarations defining which vehicles qualify for a given coverage.', 'Symbol 7 means only specifically described autos are covered.'),
     ('Symbol 1', 'Any auto — broadest BAP coverage.', 'A BAP symbol meaning all autos owned, hired, borrowed, or non-owned are covered for that coverage.', 'Symbol 1 for liability covers any auto used in the business.'),
     ('Symbol 7', 'Only specifically listed autos.', 'A BAP symbol meaning only autos described on the declarations page are covered.', 'Five delivery vans listed by VIN on the dec page are the only covered autos under Symbol 7.'),
     ('Symbol 8', 'Hired autos only.', 'A BAP symbol meaning only autos the insured rents, leases, hires, or borrows are covered.', 'A company adds Symbol 8 for hired auto liability when renting vehicles for sales trips.'),
     ('Symbol 9', 'Non-owned autos only.', 'A BAP symbol meaning only autos employees or partners own and use for business are covered.', 'Symbol 9 covers an employee who uses their personal car to make client deliveries.'),
     ('Hired Auto', 'A vehicle rented or leased by the business.', 'Under the BAP, an auto the named insured leases, hires, rents, or borrows for use in the business.', 'A company rents a cargo van for a trade show; the rental is a hired auto.'),
     ('Non-Owned Auto', 'An employee-owned vehicle used for business.', 'Under the BAP, an auto the insured does not own but is used in business operations.', 'A salesperson uses their personal car to visit clients; it is a non-owned auto.'),
     ('BAP Liability', 'Covers BI and PD from covered autos.', 'Business auto liability paying for bodily injury and property damage the insured is legally responsible for from accidents involving covered autos.', 'A delivery driver causes an accident; BAP liability covers the injured third party.'),
     ('Collision', 'Impact or upset of a covered auto.', 'BAP physical damage coverage for the insured auto caused by collision with another vehicle or object, or by the vehicle overturning.', 'A company truck backs into a loading dock; collision covers the damage.'),
     ('Comprehensive', 'Non-collision physical damage to a covered auto.', 'BAP physical damage coverage for losses other than collision, including theft, fire, hail, vandalism, and animal contact.', 'A company van is stolen; comprehensive coverage pays for the loss.'),
     ('Drive Other Car Endorsement', 'Extends BAP coverage to named executives.', 'A BAP endorsement extending coverage to a named individual who does not own a personal auto and regularly uses vehicles not on the BAP.', 'A fleet-only executive with no personal auto is covered by the DOC endorsement when driving a rental.'),
     ('Fellow Employee Exclusion', 'Removes coverage for injuries to co-workers.', 'A BAP exclusion eliminating liability coverage for bodily injury to a fellow employee of the insured occurring in the course of employment.', 'A driver injures a coworker in a work vehicle; the BAP fellow employee exclusion may apply.'),
     ('MCS-90 Endorsement', 'Required for federally regulated motor carriers.', 'A mandatory endorsement for federally regulated interstate motor carriers requiring the insurer to pay covered losses even if the carrier failed to comply with policy conditions.', 'A trucking company in interstate commerce must attach an MCS-90 to their BAP.'),
     ('Garagekeepers Coverage', 'Covers customer vehicles left with the business.', 'A coverage for repair shops, dealers, and storage facilities paying for physical damage to customer vehicles in the insured care, custody, or control.', 'A customer car is damaged in a fire at the body shop; garagekeepers coverage pays.'),
     ('Garage Coverage Form', 'Covers auto dealers and service operations.', 'A specialized commercial auto form for auto dealers, service stations, and garekeepers combining auto liability, garagekeepers, and other coverages.', 'A car dealership uses the garage coverage form to cover both liability and customer vehicles on the lot.'),
   ]),

  # ── 10. Workers Compensation ──────────────────────────────────────────
  ('workers-compensation', 'Workers Compensation',
   'The workers compensation system, statutory benefits, and employers liability.',
   [
     ('wc-system', 'Purpose and Structure of Workers Compensation',
      'Workers compensation (WC) is a no-fault statutory system providing benefits to employees '
      'injured in the course of employment. The employee gives up the right to sue the employer '
      'in exchange for guaranteed benefits — the exclusive remedy doctrine. Most states require '
      'WC coverage or approved self-insurance. A few monopolistic state fund states require '
      'purchase from the state fund only.'),
     ('wc-benefits', 'Statutory Benefits',
      'WC benefits include: medical (all necessary treatment, no dollar limit in most states), '
      'disability income (income replacement during disability), death benefits (burial and '
      'survivor income), and rehabilitation (vocational or physical rehabilitation). Disability '
      'is classified as temporary total, permanent total, temporary partial, or permanent partial.'),
     ('employers-liability', 'Part Two — Employers Liability',
      'The WC policy has two parts. Part One — Workers Compensation: pays statutory benefits '
      'without limit. Part Two — Employers Liability: covers the employer for certain employee '
      'lawsuits falling outside the WC system, such as loss of consortium suits by a spouse '
      'or suits by employees in non-covered states. Part Two has specific limits.'),
     ('wc-rating', 'Experience Rating and Classification',
      'WC premium is based on a class code for the type of work and the payroll. Experience '
      'rating adjusts premium based on actual loss history versus the class average. The '
      'experience modification factor (MOD) is multiplied by standard premium: 1.00 is '
      'average, below 1.00 is a credit, above 1.00 is a debit.'),
   ],
   [
     ('Exclusive Remedy', 'WC is the employee\'s only remedy against the employer.', 'The legal doctrine making WC the sole remedy an employee may seek from their employer for a work-related injury; the employee cannot sue the employer in tort.', 'An employee injured on a forklift collects WC benefits and cannot sue the employer for negligence.'),
     ('Course of Employment', 'Injury must happen while performing job duties.', 'A requirement that a WC injury or illness occur while the employee is performing duties arising out of and in the course of employment.', 'A delivery driver injured while making deliveries is covered; a personal errand injury is not.'),
     ('Medical Benefits', 'WC pays all necessary medical care.', 'Coverage for all reasonable and necessary medical treatment for a work-related injury or occupational disease, typically without a dollar or time limit.', 'All surgeries, therapy, and prescriptions related to a work injury are paid by WC medical benefits.'),
     ('Temporary Total Disability', 'Completely unable to work temporarily.', 'A WC disability classification for an employee completely unable to work temporarily; typically pays two-thirds of pre-injury wages.', 'An employee with a broken leg who cannot work for eight weeks receives TTD benefits.'),
     ('Permanent Total Disability', 'Permanently unable to work at any job.', 'A WC disability classification for an employee permanently and totally unable to perform any gainful employment due to a work-related injury.', 'An employee who loses both hands may be classified as permanently totally disabled.'),
     ('Temporary Partial Disability', 'Can work at reduced capacity temporarily.', 'A WC classification for an employee who can perform some work at reduced capacity temporarily; pays a portion of the wage difference.', 'An injured employee returns to light duty at lower pay; TPD benefits cover part of the wage reduction.'),
     ('Permanent Partial Disability', 'Permanent impairment but can still work.', 'A WC classification for an employee with a permanent impairment who can still perform some work; may be scheduled (specific body parts) or non-scheduled.', 'An employee loses a finger; a scheduled benefit is paid for the specific loss.'),
     ('Death Benefits', 'Payments to survivors when a worker is killed.', 'WC benefits paid to surviving dependents of a worker killed in a work-related accident; typically includes burial expenses and ongoing income replacement.', 'The spouse and children of a worker killed on a construction site receive death benefits.'),
     ('Vocational Rehabilitation', 'Training to help an injured worker return to work.', 'A WC benefit providing retraining or education to help an injured employee return to suitable employment when unable to return to their previous position.', 'A worker who can no longer perform physical labor is trained for an office position.'),
     ('Employers Liability', 'Covers lawsuits by employees outside the WC system.', 'Part Two of the WC policy; covers the employer for employee suits falling outside the WC exclusive remedy, such as loss of consortium claims.', 'A worker\'s spouse sues the employer for loss of consortium; Part Two covers the defense and damages.'),
     ('Experience Modification Factor', 'A multiplier adjusting WC premium based on loss history.', 'A number applied to WC standard premium reflecting the insured\'s actual loss experience compared to the class average; less than 1.00 is a credit, more than 1.00 is a debit.', 'A manufacturer with a MOD of 0.85 pays 15% less than standard WC premium.'),
     ('Occupational Disease', 'An illness caused by working conditions.', 'A disease arising out of and in the course of employment, caused by conditions specific to the type of work; covered by workers compensation.', 'A miner who develops black lung disease from coal dust has an occupational disease covered by WC.'),
     ('Second Injury Fund', 'Pays when a pre-existing condition combines with a new work injury.', 'A state-administered fund paying for additional disability when a pre-existing condition combines with a new work injury to cause greater total disability.', 'A worker with one eye loses the other at work; the employer pays for the eye loss; the second injury fund pays for total blindness.'),
     ('Monopolistic State Fund', 'States where WC must be bought from the state.', 'A state WC system requiring employers to purchase coverage from the state fund; private insurance is not permitted for the required coverage.', 'Some states require all employers to buy WC from the monopolistic state fund.'),
     ('USL&H Act', 'Federal WC for maritime workers.', 'The United States Longshoremen\'s and Harbor Workers\' Compensation Act; provides WC-like benefits to maritime workers not covered by state WC laws.', 'A dock worker injured while loading cargo may have benefits under USL&H.'),
     ('Waiver of Subrogation', 'Insurer gives up the right to recover from a third party.', 'An agreement, often required by contract, in which the WC insurer waives its subrogation rights against a third party.', 'A general contractor requires subcontractors to include a waiver of subrogation on their WC policies.'),
   ]),

  # ── 10. Specialty Coverages ──────────────────────────────────────────
  ('crime-bonds-specialty', 'Crime, Bonds, and Specialty Coverages',
   'Crime, bonds, inland marine, and other specialty P&C coverages.',
   [
     ('commercial-crime', 'Commercial Crime Coverage',
      'Commercial crime coverage protects businesses from dishonest acts. Employee Theft '
      'covers theft by employees. Forgery or Alteration covers forged financial instruments. '
      'Theft, Disappearance, and Destruction covers money and securities losses. Computer '
      'Fraud covers theft using a computer. Crime coverage is not included in the CGL; a '
      'separate crime policy or endorsement is needed.'),
     ('surety', 'Surety Bonds',
      'A surety bond is a three-party agreement: Principal (who must perform), Obligee '
      '(who requires the guarantee), and Surety (who guarantees performance). If the '
      'principal fails, the surety pays the obligee and expects reimbursement from the '
      'principal. Common types: Performance Bonds (guarantee completion), Payment Bonds '
      '(guarantee payment to subcontractors), License and Permit Bonds, Court Bonds.'),
     ('inland-marine', 'Inland Marine Coverage',
      'Inland marine covers property in transit over land and movable or specialized property. '
      'Floater policies follow items wherever they go. Common coverages: Contractors Equipment, '
      'Motor Truck Cargo, Installation Floater, Accounts Receivable, Valuable Papers, and '
      'Electronic Data Processing. Personal articles floaters cover jewelry, fine arts, and '
      'other scheduled personal property.'),
     ('ocean-marine', 'Ocean Marine Coverage',
      'Ocean marine covers ships (Hull), cargo (Cargo), and liability (Protection and '
      'Indemnity/P&I). The Warehouse-to-Warehouse clause covers cargo from origin to '
      'destination. General Average requires all cargo owners to share in sacrificial losses '
      'made to save the vessel. Particular Average is a partial loss affecting only one party.'),
   ],
   [
     ('Employee Theft', 'Coverage for stealing by employees.', 'Commercial crime coverage for direct loss from theft by an employee.', 'A bookkeeper embezzles funds; employee theft coverage pays.'),
     ('Forgery or Alteration', 'Coverage for forged or changed financial instruments.', 'Commercial crime coverage for loss from forged signatures or altered financial instruments such as checks.', 'A forged company check clears the bank; forgery coverage reimburses the loss.'),
     ('Computer Fraud', 'Theft using a computer or network.', 'Commercial crime coverage for loss of money or property transferred based on fraudulent computer instructions.', 'Hackers trick an employee into wiring funds to a fraudulent account; computer fraud coverage applies.'),
     ('Fidelity Bond', 'Guarantees employee honesty.', 'A bond protecting an employer against losses from dishonest acts by employees.', 'A bank buys a fidelity bond to protect against teller theft.'),
     ('Surety Bond', 'A three-party guarantee of performance.', 'A bond in which the surety guarantees to the obligee that the principal will fulfill an obligation; the surety has the right to recover from the principal.', 'A construction company obtains a surety bond so the project owner is protected if construction is not completed.'),
     ('Principal', 'The party who must perform in a surety bond.', 'In a surety bond, the party required to perform an obligation and whose performance is guaranteed by the surety.', 'The contractor who must complete the building project is the principal.'),
     ('Obligee', 'The party who requires the performance guarantee.', 'In a surety bond, the party who benefits from the bond and to whom the principal owes the obligation.', 'The project owner requiring the performance bond is the obligee.'),
     ('Performance Bond', 'Guarantees a contractor completes a project.', 'A surety bond guaranteeing the principal will complete a construction project; if not, the surety pays the obligee for completion costs.', 'A municipality requires a performance bond before awarding a road paving contract.'),
     ('Payment Bond', 'Guarantees subcontractors and suppliers are paid.', 'A surety bond guaranteeing the principal will pay subcontractors, laborers, and material suppliers on the project.', 'If the general contractor fails to pay, the payment bond surety pays the subcontractors.'),
     ('Inland Marine', 'Coverage for property in transit or specialized movable property.', 'A broad category covering property in transit over land, property with no fixed location, and certain specialty property.', 'A florist\'s delivery truck contents and a museum\'s traveling exhibit are inland marine risks.'),
     ('Floater Policy', 'Coverage following property wherever it goes.', 'An inland marine policy covering movable property wherever it is located, not just at a fixed address.', 'A personal articles floater covers a diamond ring at home, on vacation, or anywhere worldwide.'),
     ('Contractors Equipment', 'Coverage for construction equipment and tools.', 'An inland marine coverage for mobile equipment used by contractors, such as backhoes, cranes, and portable tools.', 'A landscaper\'s trailer, mower, and tools are covered under a contractors equipment floater.'),
     ('Motor Truck Cargo', 'Covers goods being transported by truck.', 'An inland marine policy covering the cargo of a trucking company while in transit.', 'A trucking company carries motor truck cargo coverage to protect shipments in their trailers.'),
     ('Hull Coverage', 'Covers physical damage to a vessel.', 'Ocean marine coverage for direct physical damage to a ship or vessel.', 'A cargo ship damaged in a storm collects under hull coverage.'),
     ('Protection and Indemnity', 'Ocean marine liability coverage.', 'Ocean marine liability coverage protecting shipowners against liability for crew injuries, damage to other vessels or cargo, and third-party claims.', 'A cargo ship that collides with another faces liability covered by P&I insurance.'),
     ('General Average', 'All cargo owners share in a deliberate sacrifice.', 'A maritime principle requiring all cargo owners to share proportionally in a deliberate sacrifice made to save the common voyage.', 'Cargo is jettisoned to save a sinking ship; all cargo owners contribute to compensate the owner whose cargo was lost.'),
   ]),

  # ── 11. Dwelling Policies ─────────────────────────────────────────────
  ('dwelling-policies', 'Dwelling Policies',
   'DP forms, rental property coverage, and differences from homeowners.',
   [
     ('dp-purpose', 'Purpose of Dwelling Policies',
      'Dwelling policies (DP forms) cover residential structures not qualifying for homeowners '
      'insurance: rental properties, seasonal homes, older dwellings, and properties with '
      'substandard construction. Unlike homeowners policies, DP forms do not automatically '
      'include personal liability. Fair Rental Value coverage is available as an add-on.'),
     ('dp-forms', 'DP-1, DP-2, and DP-3',
      'DP-1 (Basic Form): covers fire, lightning, and internal explosion; extended coverage '
      'may be added by endorsement. DP-2 (Broad Form): adds more named perils including '
      'falling objects and plumbing water damage. DP-3 (Special Form): open perils on the '
      'dwelling, named perils on personal property; the most comprehensive dwelling form.'),
     ('dp-provisions', 'Key Dwelling Policy Provisions',
      'DP policies cover the dwelling structure and may include other private structures, '
      'personal property, and fair rental value. Liability is not included by default. '
      'Vacancy provisions suspend certain coverages after 60 days. DP policies pay ACV '
      'by default unless a replacement cost endorsement is added.'),
   ],
   [
     ('DP-1', 'Basic dwelling form.', 'The most basic ISO dwelling form, covering fire, lightning, and internal explosion; additional perils may be added by endorsement.', 'A landlord buys DP-1; lightning damage to the roof is covered.'),
     ('DP-2', 'Broad named perils dwelling form.', 'An ISO dwelling form with broader named perils than DP-1, adding falling objects, weight of ice and snow, and plumbing water damage.', 'A burst pipe floods a rental property; DP-2 covers the water damage.'),
     ('DP-3', 'Special form dwelling — open perils on the structure.', 'The most comprehensive ISO dwelling form; open perils on the dwelling, named perils on personal property.', 'A mystery cause damages the rental dwelling; DP-3 covers it because the cause is not excluded.'),
     ('Fair Rental Value', 'Lost rental income when the dwelling is uninhabitable.', 'Coverage under a dwelling policy for loss of rental income when the dwelling is uninhabitable due to a covered peril.', 'A fire makes a rental home uninhabitable for three months; fair rental value pays the lost rent.'),
     ('Extended Coverage', 'Additional named perils for dwelling policies.', 'An endorsement adding windstorm, hail, explosion, riot, aircraft, vehicles, smoke, and volcanic action to basic fire and lightning coverage.', 'A DP-1 with extended coverage now covers hurricane wind damage.'),
     ('Actual Cash Value', 'DP default valuation: RC minus depreciation.', 'The default valuation method for dwelling policies; replacement cost less depreciation.', 'A 15-year-old roof on a rental is damaged; ACV is paid after deducting depreciation.'),
     ('Personal Liability', 'Liability not automatically included in DP forms.', 'Coverage for the landlord\'s liability to third parties; not included in standard dwelling policies and must be added by endorsement.', 'A tenant\'s guest is injured on rental property steps; the landlord needs personal liability coverage endorsed onto the DP form.'),
     ('Vacancy Clause', 'Limits or suspends coverage after extended vacancy.', 'A policy provision reducing or suspending certain coverages when a building has been vacant beyond a specified period, typically 60 days.', 'A rental empty between tenants for 70 days may have vandalism coverage suspended.'),
     ('Landlord', 'The owner of rental property.', 'The property owner who rents a dwelling to tenants; the named insured on a dwelling policy for the rental.', 'The landlord insures the building under a DP-3; tenants insure their belongings under a renters policy.'),
     ('Tenant', 'The person renting the dwelling.', 'A person or entity occupying the insured dwelling under a rental agreement; not typically a named insured on the landlord\'s DP policy.', 'The tenant\'s personal belongings are not covered by the landlord\'s DP policy; the tenant needs a renters policy.'),
   ]),

  # ── 12. Ethics and Producer Responsibilities ─────────────────────────
  ('ethics-producer-responsibilities', 'Ethics and Producer Responsibilities',
   'Producer authority, duties, unfair practices, and licensing obligations.',
   [
     ('producer-authority', 'Types of Producer Authority',
      'Express authority is explicitly granted in the agency agreement. Implied authority is '
      'not expressly stated but reasonably necessary to carry out express authority (such as '
      'issuing binders). Apparent authority arises when the insurer\'s conduct leads a third '
      'party to reasonably believe the agent has authority, even if that authority was not '
      'actually granted. The insurer can be bound by an agent\'s apparent authority.'),
     ('producer-types', 'Types of Producers',
      'An independent agent represents multiple insurers and owns the book of business. A '
      'captive or exclusive agent represents only one insurer; the insurer owns the book. '
      'A direct writer sells through employees, not independent agents. A broker represents '
      'the insured, not the insurer. A managing general agent (MGA) has broader authority '
      'including the ability to bind coverage and issue policies.'),
     ('unfair-practices', 'Unfair Trade Practices',
      'Misrepresentation: false or misleading statements about a policy. Twisting: using '
      'misrepresentation to induce policy replacement. Churning: twisting within the same '
      'company. Rebating: giving the insured something of value not in the policy as an '
      'inducement (prohibited in most states). False advertising and unfair discrimination '
      'are also prohibited. Violations may result in license suspension or revocation.'),
     ('producer-duties', 'Producer Duties and Licensing',
      'Producers have a fiduciary duty to handle premium responsibly; premium must be '
      'remitted promptly and never commingled with personal funds. E&O insurance protects '
      'producers against negligence claims. Continuing education (CE) is required for '
      'license renewal in most states. State departments of insurance regulate producers '
      'through market conduct examinations.'),
   ],
   [
     ('Express Authority', 'Authority explicitly written in the agency agreement.', 'Specific authority granted in writing to an agent by the insurer, defining what the agent may and may not do.', 'The agency agreement states the agent may bind policies up to $500,000; that is express authority.'),
     ('Implied Authority', 'Authority reasonably necessary to carry out express authority.', 'Authority not explicitly stated but reasonably inferred as necessary to perform the agent\'s expressed duties.', 'An agent with authority to sell policies has implied authority to issue a binder, even if not expressly stated.'),
     ('Apparent Authority', 'Authority a third party reasonably believes exists.', 'Authority arising when the insurer\'s conduct leads a third party to believe the agent has authority, even if not actually granted.', 'If an insurer allows an agent to use insurer stationery, a customer may reasonably believe the agent has broad authority.'),
     ('Independent Agent', 'Represents multiple insurers and owns the business.', 'A producer representing more than one insurer, placing business with multiple companies, and retaining ownership of renewal rights.', 'An independent agent shops clients among several insurers for the best coverage and rate.'),
     ('Captive Agent', 'Represents only one insurer.', 'A producer appointed by and representing only one insurance company; the insurer typically owns the expirations.', 'A captive agent writes only one company\'s policies and cannot place business elsewhere.'),
     ('Broker', 'Represents the insured, not the insurer.', 'A producer acting on behalf of the insured to find coverage; legally the insured\'s representative.', 'A broker shops the insured\'s commercial risks to multiple markets on behalf of the client.'),
     ('Misrepresentation', 'A false or misleading statement.', 'Making a false, misleading, or incomplete statement about a policy, coverage, or insurer; an unfair trade practice.', 'Telling a prospect that a policy covers flood when it does not is misrepresentation.'),
     ('Twisting', 'Using deception to replace a policy.', 'Inducing a policyholder to replace existing coverage through misrepresentation or incomplete comparison.', 'Exaggerating the flaws of an existing policy to convince a client to switch is twisting.'),
     ('Churning', 'Replacing a policy within the same company for commission.', 'The replacement of a policyholder\'s existing policy with a new policy from the same insurer using misrepresentation, primarily to generate commissions.', 'Convincing a client to replace their policy with a new one from the same company to earn a commission is churning.'),
     ('Rebating', 'Giving something of value as an inducement to buy.', 'Returning part of the premium or giving any valuable consideration not in the policy as an inducement to purchase; illegal in most states.', 'Offering a client a gift card for signing up for a new policy is rebating.'),
     ('Fiduciary Duty', 'Duty to handle money and client affairs responsibly.', 'The obligation of a producer to act in the client\'s best interest and handle premium funds with care, trust, and honesty.', 'An agent who collects premium must remit it promptly and never use it for personal expenses.'),
     ('Errors and Omissions', 'Professional liability coverage for producers.', 'Insurance protecting a producer against claims from negligent acts, errors, or omissions in professional insurance services.', 'A producer who fails to obtain required coverage faces an E&O claim; E&O coverage pays defense and damages.'),
     ('Unfair Discrimination', 'Treating similar risks differently without justification.', 'Making distinctions in rates, coverage, or services among similarly situated insureds without actuarial justification.', 'Charging different premiums based on race or religion rather than actuarial factors is unfair discrimination.'),
     ('Binding Authority', 'The agent\'s power to put coverage in force immediately.', 'The authority granted to a producer to initiate insurance coverage on behalf of the insurer before a formal policy is issued.', 'An agent with binding authority confirms auto coverage by phone so a client can drive off the lot.'),
     ('Market Conduct Examination', 'State review of insurer and agent practices.', 'An examination by the state department of insurance reviewing business practices of insurers and producers for compliance with insurance laws.', 'A state DOI examines an agency\'s claims handling and rating practices.'),
     ('License Suspension', 'Temporary loss of the license to sell insurance.', 'A disciplinary action temporarily removing a producer\'s license to sell, solicit, or negotiate insurance.', 'A producer convicted of rebating may have their license suspended for six months.'),
   ]),

  # ── 13. Exam Strategy ─────────────────────────────────────────────────
  ('exam-prep', 'Exam Strategy and Final Review',
   'Question types, elimination techniques, and study planning for the P&C exam.',
   [
     ('reading-questions', 'Reading Exam Questions Carefully',
      'Read the complete question stem before looking at answer choices. Identify the '
      'coverage type (property, liability, auto, etc.) and specific concept being tested. '
      'Watch for qualifier words: except, not, never, always, first, best, and most likely. '
      'Exception questions ("All of the following EXCEPT") require finding the false statement. '
      'Scenario questions embed a concept in a story — identify the concept first.'),
     ('elimination', 'Using Elimination to Choose the Best Answer',
      'Cross out factually wrong answers first. Then eliminate answers not addressing what '
      'the question asks. Between remaining answers, choose the one most directly supported '
      'by course material. On licensing exams, the best answer is usually the most '
      'straightforward application of the rule. If two seem correct, one is usually '
      'more specific or complete.'),
     ('study-plan', 'Building a Study Plan',
      'Start with Insurance Basics, then Contracts, then property and casualty topics, then '
      'personal and commercial lines, and finally ethics and exam strategy. Review every '
      'missed question until you understand why the correct answer is correct. Study terms '
      'using flashcards before attempting quiz questions on that topic. Take timed practice '
      'exams in the final week. Focus extra time on topics where quiz scores are below 80%.'),
   ],
   [
     ('Qualifier Word', 'A word that changes what the question is asking.', 'A word such as except, not, never, always, first, best, or most likely that modifies the question and must be identified before choosing an answer.', 'The word EXCEPT means find the false statement, not the true one.'),
     ('Exception Question', 'A question asking which statement is false.', 'A format using EXCEPT, NOT, or FALSE that requires identifying the one incorrect or inapplicable option among the choices.', '"All of the following are parts of an insurance policy EXCEPT" — find the one that is not a part.'),
     ('Scenario Question', 'A question presenting a story to identify a concept.', 'A question presenting a factual situation and asking the candidate to identify the applicable concept, coverage, or rule.', 'A question describes a flooded store and asks what type of loss applies; the answer is indirect loss.'),
     ('Elimination', 'Crossing out wrong answers to find the best one.', 'A strategy removing clearly wrong or inapplicable choices first, increasing the probability of selecting the correct answer.', 'If three choices involve homeowners and the question is about auto, eliminate the homeowners answers first.'),
     ('Best Answer', 'The most accurate choice for the specific question.', 'The answer that most directly and accurately addresses what the question is asking, even if other choices contain true statements that do not answer the question.', 'A question asks who pays first in a no-fault accident; the best answer is the insured\'s own insurer.'),
     ('Coverage Type Identification', 'Determining which branch of insurance a question covers.', 'The first step in answering an exam question; identifying which type or coverage part the question addresses before looking at answer choices.', 'Spotting a slip-and-fall question tells you it is a casualty/liability question, not property.'),
     ('Mistake Bank', 'Reviewing missed questions to identify weak areas.', 'The set of incorrectly answered questions; reviewing these focuses study time on topics where understanding is weakest.', 'A candidate who repeatedly misses coinsurance questions should review the property fundamentals module.'),
     ('Distractor', 'A wrong answer designed to seem plausible.', 'An incorrect answer choice written to seem reasonable to a candidate who does not know the material well.', 'On a coinsurance question, "deductible" may appear as a distractor for candidates who confuse the two.'),
     ('Timing', 'Managing time during the actual exam.', 'Allocating a specific amount of time per question and moving on if stuck, returning to skipped questions at the end.', 'On a 150-question exam with 2 hours, allow about 48 seconds per question.'),
     ('Readiness Score', 'An estimate of exam preparedness.', 'A score indicating how prepared a candidate is based on quiz results, lesson completion, and mistake bank analysis.', 'A candidate with 90% lesson completion and 85% quiz accuracy has a high readiness score.'),
   ]),
]


def _build_course() -> dict:
    course: dict = {"modules": []}
    for idx, (slug, title, description, lessons, terms) in enumerate(RAW_MODULES, start=1):
        module: dict = {
            "slug": slug, "title": title, "description": description,
            "sort_order": idx, "lessons": [], "terms": [], "questions": [],
        }
        lesson_slugs = []
        for lesson_idx, (lesson_slug, lesson_title, body) in enumerate(lessons, start=1):
            sentences = [s.strip() for s in body.split(".") if s.strip()]
            summary = sentences[0] + "." if sentences else body[:120]
            lesson_slugs.append(lesson_slug)
            module["lessons"].append({
                "slug": lesson_slug, "title": lesson_title, "summary": summary, "body": body,
                "example": (f"On the exam: a question about {lesson_title.lower()} may describe "
                            f"a scenario and ask you to identify the correct term or coverage."),
                "memory_tip": (f"For {lesson_title}: focus on the key distinction that separates "
                               f"this concept from similar ones — that distinction is what the exam tests."),
                "audio_script": f"{lesson_title}. {body}",
                "estimated_minutes": 8, "sort_order": lesson_idx, "is_active": True,
            })
        for term, plain, exam_def, example in terms:
            module["terms"].append({
                "term": term, "plain_english_definition": plain,
                "exam_definition": exam_def, "example": example,
            })
        if terms:
            t0, t1, t2 = terms[0], terms[min(1, len(terms)-1)], terms[min(5, len(terms)-1)]
            module["questions"].extend([
                {
                    "lesson_slug": lesson_slugs[0] if lesson_slugs else "",
                    "question_text": f"Which of the following best describes {t0[0]}?",
                    "question_type": "multiple_choice", "difficulty": "standard",
                    "explanation": t0[2], "is_active": True,
                    "choices": [
                        {"choice_text": t0[1], "is_correct": True, "explanation": f"Correct. {t0[2]}", "sort_order": 1},
                        {"choice_text": "A policy exclusion that removes coverage automatically.", "is_correct": False, "explanation": "An exclusion removes coverage; this does not describe the term.", "sort_order": 2},
                        {"choice_text": "A state-specific regulation that varies by jurisdiction.", "is_correct": False, "explanation": "This is a general P&C concept, not a state-specific rule.", "sort_order": 3},
                        {"choice_text": "A premium discount for maintaining continuous coverage.", "is_correct": False, "explanation": "Premium discounts are a separate concept.", "sort_order": 4},
                    ],
                },
                {
                    "lesson_slug": lesson_slugs[min(1, len(lesson_slugs)-1)] if lesson_slugs else "",
                    "question_text": f"A candidate reads: '{t2[3]}' — which term does this describe?",
                    "question_type": "scenario", "difficulty": "standard",
                    "explanation": t2[2], "is_active": True,
                    "choices": [
                        {"choice_text": t2[0], "is_correct": True, "explanation": f"Correct. {t2[2]}", "sort_order": 2},
                        {"choice_text": terms[min(3, len(terms)-1)][0], "is_correct": False, "explanation": "The scenario does not describe this concept.", "sort_order": 1},
                        {"choice_text": "A policy cancellation provision.", "is_correct": False, "explanation": "The scenario does not involve cancellation.", "sort_order": 3},
                        {"choice_text": "A premium financing agreement.", "is_correct": False, "explanation": "The scenario does not involve premium financing.", "sort_order": 4},
                    ],
                },
                {
                    "lesson_slug": lesson_slugs[0] if lesson_slugs else "",
                    "question_text": f"All of the following statements about {t1[0]} are true EXCEPT:",
                    "question_type": "exception", "difficulty": "hard",
                    "explanation": t1[2], "is_active": True,
                    "choices": [
                        {"choice_text": f"It means: {t1[1]}", "is_correct": False, "explanation": "This is a true statement.", "sort_order": 1},
                        {"choice_text": f"The exam definition: {t1[2][:80]}...", "is_correct": False, "explanation": "This is a true statement.", "sort_order": 2},
                        {"choice_text": "It automatically applies without conditions or exclusions.", "is_correct": True, "explanation": "This is false. All insurance concepts apply subject to policy terms, conditions, and exclusions.", "sort_order": 3},
                        {"choice_text": f"Example: {t1[3][:60]}...", "is_correct": False, "explanation": "This is a true example.", "sort_order": 4},
                    ],
                },
            ])
        course["modules"].append(module)
    return course


DEFAULT_COURSE = _build_course()
