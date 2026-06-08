#!/usr/bin/env python3
"""
load_lesson_content.py
Run from pc-license-prep-server-v2/ directory:
    .venv/bin/python3 scripts/load_lesson_content.py

Replaces auto-generated stub lesson content with real exam-focused prose.
Only updates lessons whose body is currently a stub (< 300 chars).
Safe to re-run — won't overwrite real content.

Priority order: Insurance Basics → Insurance Contracts → Property Fundamentals
→ Casualty Fundamentals → Ethics and Producer Responsibilities
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_all
from app.models import Lesson, Module
from sqlalchemy import select

# Keyed by lesson slug. Content is (body, summary, example, memory_tip).
LESSON_CONTENT = {

# ═══════════════════════════════════════════════════════════════════════
# MODULE 1 — INSURANCE BASICS
# ═══════════════════════════════════════════════════════════════════════

"what-is-insurance": (
    """Insurance is a financial arrangement in which one party (the insured) pays a relatively small, certain amount of money (the premium) to another party (the insurer) in exchange for a promise to pay a larger, uncertain amount if a specified loss occurs. At its core, insurance is a mechanism for transferring risk — the insured trades the possibility of a large, unpredictable loss for the certainty of a small, known premium payment.

The fundamental principle underlying all insurance is indemnity: the idea that insurance should restore the insured to their pre-loss financial position, but not put them in a better position. An insured should not profit from a loss. If a homeowner's $200,000 house burns down, the insurer pays enough to rebuild that house — not a profit. This principle prevents insurance from becoming a tool for speculation or fraud.

Insurance works because of risk pooling. Thousands of policyholders each pay premiums into a common fund. Most will never suffer a major loss in a given year, but those who do are compensated from that pooled fund. No single person has to bear the full financial impact of a catastrophic event alone. The insurer functions as the administrator of this pool, collecting premiums, investing the reserves, and paying claims.

For the exam, always connect insurance to three core ideas: risk transfer (the insured shifts financial responsibility to the insurer), indemnity (no profit from a loss), and risk pooling (many pay so few can collect). Questions will often test whether you understand that insurance is not a guarantee against loss itself — it is a financial remedy after a loss occurs.""",
    "Insurance transfers financial risk from an insured to an insurer through premium payments.",
    "A homeowner pays $1,200 per year in premiums. When a fire causes $80,000 in damage, the insurer pays — the small certain cost protected against the large uncertain loss.",
    "Remember the three pillars: Transfer (risk moves to insurer), Indemnity (restore, not enrich), Pooling (many fund the few)."
),

"risk-peril-hazard": (
    """Three terms appear constantly on the P&C exam and are frequently confused: risk, peril, and hazard. Understanding the difference between them is essential.

Risk is the possibility of financial loss. It is the uncertainty about whether a loss will occur and how large it will be. When an underwriter evaluates a property, they are assessing the risk — the overall likelihood and potential severity of a claim. Risk is the broadest concept of the three.

A peril is the direct cause of a loss. Fire, theft, windstorm, flood, and collision are all perils — they are the events that actually trigger the damage or loss. When you look at a named perils policy, you are looking at a list of perils that the policy covers. The exam will ask you to identify which peril caused a specific loss, because coverage depends on whether that peril is in the policy.

A hazard is a condition that increases the probability or severity of a loss from a given peril. Hazards come in three types that the exam tests heavily. A physical hazard is a tangible condition — faulty wiring increases fire risk, a slippery floor increases fall risk. A moral hazard arises from the character or dishonesty of the insured — someone who might intentionally cause a loss to collect insurance proceeds. A morale hazard (note the different spelling) arises from indifference — the insured becomes careless about preventing losses because they know they are insured.

The exam commonly presents a scenario and asks whether it illustrates a peril, a physical hazard, a moral hazard, or a morale hazard. Use this test: did it cause the loss (peril)? Is it a physical condition that makes loss more likely (physical hazard)? Does it involve dishonesty or intent (moral hazard)? Does it involve carelessness or indifference (morale hazard)?""",
    "Risk is the possibility of loss; a peril is the direct cause; a hazard is a condition that increases likelihood or severity.",
    "A gas station's faulty underground tanks (physical hazard) increase the risk of a fuel leak (risk). If the leak ignites and causes a fire, the fire is the peril that triggers the insurance claim.",
    "Peril = the event. Hazard = the condition. Risk = the overall possibility. 'PHR' — Peril Happens, Risk remains, Hazard raises it."
),

"risk-management": (
    """Risk management is the systematic process of identifying, analyzing, and responding to potential losses. Before insurance existed, individuals and businesses had to rely entirely on their own resources to handle unexpected losses. Modern risk management offers five strategies, all of which appear on the P&C exam.

Avoidance means eliminating the activity that creates the risk entirely. A company that decides not to manufacture a product because of potential liability has avoided that risk. Avoidance is the most complete risk management strategy, but it is often impractical — avoiding all risk would mean doing nothing.

Reduction (also called loss control) means taking steps to lower either the frequency or the severity of potential losses without eliminating the activity. Installing smoke detectors reduces the severity of fire losses. Requiring employees to wear hard hats reduces the frequency of head injuries. Reduction does not eliminate risk — it manages it.

Retention means accepting the financial consequences of a loss. Self-insurance, deductibles, and simply going without insurance are all forms of retention. Retention makes sense when losses are predictable, small enough to absorb, or when the cost of transfer (premium) exceeds the expected loss value.

Sharing involves spreading risk among multiple parties, such as co-insurance arrangements or risk retention groups where multiple businesses pool their exposures.

Transfer shifts the financial responsibility for a loss to another party. Purchasing insurance is the most common form of risk transfer — the insured pays a premium and transfers the potential loss to the insurer. Contractual risk transfer (hold harmless agreements) is another form.

For the exam, be prepared to classify a described action into one of these five categories. The most commonly tested distinction is between reduction (changing how an activity is done to lower risk) and avoidance (stopping the activity altogether).
""",
    "Risk management offers five strategies: avoidance, reduction, retention, sharing, and transfer.",
    "A restaurant installs a fire suppression system (reduction), buys a $500 deductible property policy (retention of small losses plus transfer of large ones), and requires a hold harmless agreement from event caterers (contractual transfer).",
    "ARRST — Avoidance, Reduction, Retention, Sharing, Transfer. Think of risk management as a spectrum from 'don't do it' to 'pay someone else if it happens.'"
),

"law-of-large-numbers": (
    """The Law of Large Numbers is a statistical principle that forms the mathematical foundation of insurance. It states that as the number of similar, independent exposure units in a group increases, the actual loss results will more closely approach the expected (predicted) loss results.

In practical terms: if an insurer covers 100 houses, it cannot predict with confidence which one will burn down, or whether any will. But if it covers 100,000 similar houses, it can predict with high accuracy that approximately 2% will suffer significant fire losses in a given year — because actual experience converges on statistical probability as the sample size grows.

This predictability is what allows insurers to set accurate premiums. If an insurer can reliably predict that 200 of 10,000 insured homes will have claims averaging $25,000 each, it knows it needs to collect roughly $500,000 in aggregate premium from that group, plus administrative costs and profit margin. This is the actuarial foundation of insurance pricing.

Three conditions make the Law of Large Numbers work in insurance. First, the exposures must be similar — insuring 10,000 identical suburban homes is more predictable than insuring 10,000 wildly different properties. Second, the exposures should be independent — one loss should not increase the likelihood of other losses (catastrophic events like hurricanes violate this). Third, the sample must be large enough — the larger the pool, the more reliable the prediction.

The exam uses the Law of Large Numbers to explain why insurers prefer large books of business, why diversification across geographies matters, and why catastrophic events strain insurer finances (they cause many losses simultaneously, violating the independence requirement).
""",
    "The Law of Large Numbers allows insurers to predict losses accurately by pooling a large number of similar, independent risks.",
    "An insurer covering 50,000 similar homes can predict with confidence that about 1,000 will have water damage claims averaging $8,000 each — totaling $8 million in expected losses — far more accurately than it could predict a single home's outcome.",
    "Bigger pool = more predictable results. Like flipping a coin: 10 flips might be 8 heads, but 10,000 flips will be close to 5,000 heads. The law only works when risks are similar and independent."
),

"insurable-interest": (
    """Insurable interest is one of the most fundamental requirements for a valid insurance contract. It means that the person purchasing insurance must face a real financial loss if the insured event occurs. Without insurable interest, insurance becomes gambling — a bet on whether a loss will happen.

For property insurance, insurable interest must exist at the time of the loss. The insured must have a financial stake in the property at the time it is damaged or destroyed. A homeowner has insurable interest in their home because they would suffer a financial loss if it burned. A mortgage lender has insurable interest in the property securing the loan. A tenant has insurable interest in their personal belongings but not in the building itself (unless they have a leasehold interest).

For life insurance, insurable interest must exist at the time the policy is purchased. Spouses have insurable interest in each other. Business partners have insurable interest in each other's lives (key person insurance). Creditors have insurable interest in debtors up to the amount of the debt. A stranger has no insurable interest in another stranger's life — purchasing such a policy would be a wagering contract.

The insurable interest requirement serves two important purposes. First, it prevents wagering — people should not be able to profit from someone else's misfortune unless they have a genuine financial stake. Second, it reduces moral hazard — an insured with a real financial interest in the property is motivated to protect it, not destroy it.

On the exam, insurable interest questions typically involve identifying whether a described party has a legitimate financial interest. Common scenarios include banks (yes, as mortgage holders), tenants (yes, for their personal property; no, for the building), and strangers (no, for another person's property or life).
""",
    "Insurable interest requires that the insured face genuine financial loss if the insured event occurs.",
    "A bank holding a $300,000 mortgage on a house has insurable interest in that house up to the outstanding loan balance. The homeowner has insurable interest in the full value of the home.",
    "No stake, no coverage. Ask: 'Would this person lose money if the loss occurred?' Yes = insurable interest. No = no insurable interest, no valid policy."
),

"types-of-insurers": (
    """Insurance is provided through several different types of organizations, each with a distinct ownership structure, regulatory status, and business model. The P&C exam tests your ability to distinguish between them.

Stock insurance companies are owned by shareholders. Shareholders invest capital, and the company operates to generate profit for them. Policyholders are customers, not owners. Stock companies issue non-participating policies — policyholders do not share in the company's profits or losses.

Mutual insurance companies are owned by their policyholders. There are no outside shareholders. Policyholders may receive dividends when the company performs well — these are called participating policies. Mutual company dividends are considered a return of premium (not taxable income) because they represent a refund of excess premium paid.

Reciprocal insurers (also called reciprocal exchanges or interinsurance exchanges) are groups of individuals or businesses that agree to insure each other. Each member is both an insured and an insurer of the others. A third party called an attorney-in-fact manages the exchange and handles the administrative functions.

Lloyd's of London is not an insurance company but a marketplace where individual underwriters (called Names or syndicates) accept portions of insurance risks. Lloyd's specializes in unusual and hard-to-place risks. It is not a U.S. domestic insurer.

Risk retention groups are groups of businesses in the same industry that pool their liability risks together. They are regulated under federal law (the Liability Risk Retention Act) and can operate across state lines with minimal state regulation.

The exam often asks about the source of an insurer's capital (shareholders for stock, policyholders for mutual), whether dividends are guaranteed (they are never guaranteed — they are discretionary), and the role of the attorney-in-fact in a reciprocal exchange.
""",
    "Insurers are organized as stock companies (shareholder-owned), mutual companies (policyholder-owned), or reciprocal exchanges (members insure each other).",
    "A policyholder at State Farm (a mutual company) may receive a dividend check at year-end if the company's experience was favorable — this is a return of excess premium, not investment income.",
    "Stock = shareholders own it. Mutual = policyholders own it. Reciprocal = members own each other's risk. Lloyd's = a market, not a company."
),

"insurance-regulation": (
    """Insurance in the United States is regulated primarily at the state level. This is a foundational principle established by the McCarran-Ferguson Act of 1945, which affirmed that the states have the primary authority to regulate the business of insurance. Federal regulation exists but is limited.

Each state has an Insurance Department (or Division of Insurance) headed by an Insurance Commissioner (elected in some states, appointed in others). The commissioner's office performs several critical functions: licensing insurers and producers, approving policy forms and rates, examining insurer solvency, investigating consumer complaints, and enforcing insurance laws.

The primary purpose of insurance regulation is to protect consumers and maintain insurer solvency. Regulators want to ensure that insurers can pay claims when they come due. They require insurers to maintain minimum capital and surplus, file annual financial statements, and submit to periodic financial examinations.

State guaranty funds protect policyholders if an admitted insurer becomes insolvent. Each state has a guaranty fund that pays covered claims up to statutory limits when a licensed (admitted) insurer fails. Guaranty funds do not cover surplus lines (non-admitted) insurers.

For the exam, key regulation points include: states (not federal government) regulate insurance; the Insurance Commissioner enforces state insurance laws; admitted insurers are licensed by the state and covered by the guaranty fund; non-admitted (surplus lines) insurers are not covered by the guaranty fund; insurance rates must be adequate (enough to pay claims), not excessive (not too high), and not unfairly discriminatory (not based on protected characteristics unrelated to risk).
""",
    "Insurance is primarily regulated at the state level by the Insurance Commissioner to protect consumers and ensure insurer solvency.",
    "When a licensed insurer becomes insolvent and cannot pay claims, the state guaranty fund steps in to pay covered claims up to the statutory limit — protecting policyholders who did nothing wrong.",
    "State regulation. Commissioner enforces. Guaranty fund protects admitted insurer policyholders. Remember: admitted = state-licensed = guaranty fund covered."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 2 — INSURANCE CONTRACTS
# ═══════════════════════════════════════════════════════════════════════

"main-policy-sections": (
    """Every insurance policy is organized into standard sections, and the exam expects you to know what each section contains. Understanding this structure helps you navigate any policy to find the relevant language.

The Declarations page (often called the 'dec page') is the face page of the policy. It contains the policy-specific information: the named insured's name and address, the policy period (effective and expiration dates), the covered property or vehicles, the coverage limits, deductibles, premiums, and the names of any additional insureds or loss payees. The dec page is the most personalized section — it is different for every policyholder.

The Insuring Agreement is the heart of the policy — it is the insurer's promise. It broadly states what the insurer agrees to do: pay for covered losses, defend the insured against covered claims, etc. Insuring agreements are either broad (covering all losses except those excluded) or narrow (covering only listed perils).

Exclusions are the limitations and restrictions on coverage. They specify what the policy does NOT cover. Common exclusions include intentional acts, flood, earthquake, and war. Exclusions are critically important on the exam — a covered peril can still result in a denied claim if an exclusion applies.

Conditions are the obligations both parties must meet for the policy to be valid and for coverage to apply. Common conditions include the insured's duty to pay premiums, give timely notice of loss, cooperate in the investigation, submit to examination under oath, and protect property from further damage after a loss.

Definitions clarify the specific meaning of terms used throughout the policy. Because insurance policies use technical language, defined terms (usually in quotation marks or bold) have specific meanings that may differ from everyday usage.

Miscellaneous provisions (sometimes called 'other conditions') address items like cancellation and nonrenewal, assignment of the policy, liberalization, and other administrative matters.
""",
    "Every insurance policy contains declarations, insuring agreement, exclusions, conditions, definitions, and miscellaneous provisions.",
    "After a house fire, the insured checks the declarations for their coverage limit ($250,000), the insuring agreement to confirm fire is covered, the exclusions to make sure no exception applies, and the conditions to confirm they gave proper notice.",
    "DICE-M: Declarations (who/what/when/how much), Insuring agreement (the promise), Conditions (obligations), Exclusions (what's NOT covered), Miscellaneous (the rest)."
),

"parts-of-an-insurance-policy": (
    """Building on the basic policy structure, certain components of a policy deserve deeper examination because they appear frequently in exam scenarios.

The named insured is the person or entity specifically identified on the declarations page. The named insured has the broadest rights under the policy — they can cancel the policy, receive premium refunds, and are owed the duties of notice. Spouses of individual named insureds are often automatically treated as named insureds under personal lines policies.

Additional insureds are parties added to the policy who have a limited insured status — typically they are protected against liability arising from the named insured's operations but may not have all the rights of the named insured. Additional insureds are common in commercial policies (landlords added to tenant policies, general contractors added to subcontractor policies).

Loss payees and mortgageholders have an interest in property insurance proceeds. A bank holding a mortgage is typically listed as a mortgageholder — if the property is damaged, the bank has a right to be named in the insurance check to protect its collateral.

Endorsements (also called riders or forms) are written modifications to the policy that change, add, or remove coverage. An endorsement becomes part of the policy and overrides conflicting policy language. Endorsements are used to customize a standard policy for an individual insured's needs.

A binder is a temporary insurance contract that provides coverage immediately while the formal policy is being prepared. Binders are legally binding even before the policy is issued. They typically expire when the formal policy is delivered.

Certificates of insurance are documents that summarize the coverage in effect for a named insured. They are used as proof of insurance (for landlords, lenders, or contract requirements) but do not themselves constitute the insurance policy and generally cannot be used to expand coverage.
""",
    "Insurance policies identify the named insured, additional insureds, loss payees, and can be modified by endorsements.",
    "A general contractor requires all subcontractors to name the GC as an additional insured on their CGL policies. This way, if a sub's employee injures a third party, the GC has some protection under the sub's policy.",
    "Named insured = full rights. Additional insured = limited protection. Loss payee = right to proceeds. Endorsement = modifies the policy. Binder = temporary coverage."
),

"valid-contract": (
    """For an insurance policy to be legally enforceable, it must meet the same basic requirements as any valid contract, plus one additional requirement unique to insurance.

The four standard requirements for any valid contract are: (1) Offer and acceptance — one party makes an offer and the other accepts it on the same terms. In insurance, the application is the offer; the policy is the acceptance. (2) Consideration — both parties must give something of value. The insured gives the premium; the insurer gives the promise of coverage. (3) Legal purpose — the contract must be for a lawful purpose. A policy insuring an illegal activity is not enforceable. (4) Competent parties — both parties must have the legal capacity to contract. Minors and mentally incapacitated individuals generally cannot enter binding contracts.

The fifth requirement unique to insurance is insurable interest — the applicant must have a genuine financial stake in the insured person or property. Without insurable interest, the contract is a wagering agreement and is void.

A void contract has no legal effect from the beginning — it is as if the contract never existed. A voidable contract is valid but can be cancelled by one of the parties under certain circumstances. Insurance fraud, for example, makes a policy voidable at the insurer's option.

For the exam, remember that misrepresentation (a false statement of fact on the application) and concealment (withholding material information) can make a policy voidable. A material misrepresentation is one that would have affected the insurer's decision to issue the policy or the premium charged. Immaterial misrepresentations (minor, inconsequential errors) generally do not void coverage.
""",
    "A valid insurance contract requires offer and acceptance, consideration, legal purpose, competent parties, and insurable interest.",
    "An applicant states they have no prior losses when they had a major fire claim two years ago. This material misrepresentation gives the insurer grounds to void the policy — the insurer would not have issued coverage on the same terms had it known the truth.",
    "CALICO: Consideration, Acceptance, Legal purpose, Insurable interest, Competent parties, Offer. Five for any contract; insurable interest is the insurance-specific add-on."
),

"contract-characteristics": (
    """Insurance contracts have several unique legal characteristics that set them apart from ordinary commercial contracts. The exam tests each of these characteristics regularly.

Aleatory means the exchange of values is unequal and depends on chance. The insured may pay $800 in annual premium and never file a claim — or may pay $800 and receive $300,000 after a total loss. The outcome is uncertain for both parties. Most commercial contracts involve an equal exchange of value; insurance does not.

Unilateral means only one party (the insurer) makes a legally enforceable promise. The insured promises to pay premium, but if they stop paying, the policy simply lapses — the insured cannot be sued for non-payment. The insurer, however, is legally bound to pay covered claims once the contract is in force.

Conditional means the insurer's duty to pay is conditional on the insured meeting certain obligations — paying the premium, giving timely notice of loss, cooperating in the investigation, protecting property from further damage, and so on. The insurer is not required to pay if the insured materially breaches these conditions.

Contract of adhesion means the policy is drafted entirely by the insurer; the insured can only accept or reject it as written — they cannot negotiate individual terms. Because the insured had no say in the drafting, courts resolve any ambiguity in policy language in favor of the insured (the non-drafting party). This principle is called contra proferentem.

Personal means the policy is a contract with a specific person or entity — it cannot be assigned (transferred) to another party without the insurer's consent. This matters because the insurer evaluated the specific risk presented by the original insured.
""",
    "Insurance contracts are aleatory, unilateral, conditional, contracts of adhesion, and personal.",
    "A homeowner sells their house without telling their insurer. The buyer cannot simply take over the seller's homeowners policy — because the policy is personal to the original insured. The buyer needs their own policy.",
    "AUCAP: Aleatory (unequal exchange), Unilateral (one party promises), Conditional (conditions must be met), Adhesion (take it or leave it), Personal (specific to the insured)."
),

"policy-conditions": (
    """Policy conditions are the obligations that both the insured and the insurer must fulfill for the insurance contract to operate properly. Conditions are not coverage provisions — they are procedural requirements. Failing to meet a condition can result in a denied claim even if the loss would otherwise be covered.

The insured's most important conditions include: prompt notice of loss (the insured must notify the insurer as soon as reasonably possible after a covered loss); cooperation (the insured must assist in the investigation, attend hearings and trials if requested, and not voluntarily make payments or admit liability without the insurer's consent); proof of loss (a formal, often sworn statement describing the loss, the property affected, and the amount claimed); protection of property from further damage (after a loss, the insured must take reasonable steps to protect remaining property); and examination under oath (the insurer may require the insured to answer questions under oath about the loss).

The examination under oath provision is particularly important on the exam. The insurer has the right to question the insured under oath — refusing to submit to an examination under oath can result in denial of the claim.

Appraisal is a condition that addresses disputes over the amount of a loss (not whether the loss is covered). If the insured and insurer disagree on the value of a covered loss, either party can invoke appraisal: each side selects an appraiser, and the two appraisers select an umpire. If the appraisers disagree, the umpire casts the deciding vote. The appraisal award is binding.

Subrogation is the insurer's right to recover from a responsible third party after paying a claim. Once the insurer pays the insured, it steps into the insured's legal shoes and can sue the responsible party. The insured cannot do anything to impair the insurer's subrogation rights — signing a release of the responsible party before the insurer pays can void coverage.
""",
    "Policy conditions define the obligations both parties must meet — including notice of loss, cooperation, proof of loss, and protection of property.",
    "After a car hits an insured's fence, the insured must notify the insurer promptly, file a proof of loss, cooperate with the claims investigation, and NOT sign a release with the driver before the insurer investigates — doing so could waive the insurer's subrogation rights.",
    "Think of conditions as the rules of the claims game: notify promptly, cooperate fully, prove your loss, and protect what's left. Breaking the rules can cost you coverage."
),

"cancellation-nonrenewal": (
    """Insurance policies can be ended before their natural expiration date (cancellation) or simply not continued at expiration (nonrenewal). Both are heavily regulated to protect policyholders from abrupt loss of coverage.

Cancellation during the policy period can be initiated by either the insured or the insurer, but the rules differ. The insured can typically cancel at any time by notifying the insurer; they receive a pro rata return of unearned premium (the exact unearned portion). The insurer faces more restrictions — particularly after the policy has been in force for 60 days.

During the first 60 days of a new policy, insurers generally can cancel for any underwriting reason with proper notice. After 60 days, most states restrict insurer cancellation to specific reasons: nonpayment of premium, material misrepresentation in the application, substantial increase in risk, or fraud.

Notice requirements for cancellation are state-specific but typically require written notice delivered to the insured's last known address. Common notice periods are 10 days for nonpayment of premium and 30 days for other reasons. Some states require 45 or 60 days for nonrenewal.

Nonrenewal occurs when the insurer declines to continue the policy at expiration. Insurers typically must provide advance written notice (30-60 days before expiration) and must have a legitimate reason. They cannot nonrenew solely because the insured filed a claim, in many states.

Return premium rules differ by who cancels: pro rata applies when the insurer cancels (full unearned premium returned); short rate applies when the insured cancels (a penalty is taken — the insured receives less than the full unearned premium to compensate the insurer for policy acquisition costs).
""",
    "Policies can be cancelled mid-term or nonrenewed at expiration, with different notice requirements and return premium calculations depending on who initiates.",
    "An insured cancels their homeowners policy after 6 months of a one-year $1,200 policy. Using short rate, they might receive only $540 instead of the pro rata $600 — the $60 difference is the short rate penalty for early cancellation.",
    "Who cancels = who gets penalized. Insured cancels early = short rate (penalty). Insurer cancels = pro rata (full return). Nonrenewal = notice required 30-60 days before expiration."
),

"other-insurance": (
    """When more than one insurance policy covers the same loss, the 'other insurance' provisions in each policy determine how the loss is shared between the insurers. This prevents the insured from collecting more than 100% of the loss.

The primary rule is that an insured should never profit from having multiple policies. If two policies both covered a $50,000 loss in full, the insured would collect $100,000 — a $50,000 windfall. Other insurance provisions prevent this.

Pro rata liability is the most common approach in property insurance. Each insurer pays its proportionate share of the loss based on the ratio of its policy limit to the total insurance in force. Example: Policy A has $200,000 in coverage; Policy B has $100,000. Total coverage is $300,000. A $60,000 loss occurs. Policy A pays 2/3 ($40,000); Policy B pays 1/3 ($20,000).

Primary and excess arrangements specify which policy responds first (primary) and which responds only after the primary is exhausted (excess). Umbrella and excess liability policies are classic examples of excess coverage. The primary policy pays first up to its limit; the excess policy then pays amounts above that.

Contribution by equal shares is used in some liability policies. Each insurer pays an equal share of the loss until either the loss is paid or one policy reaches its limit.

For the exam, know that other insurance provisions exist to prevent double recovery. Pro rata is the most common approach for property coverage. When policies conflict on other insurance language, the analysis can become complex — but the key principle is always that the insured recovers their actual loss, not more.
""",
    "When multiple policies cover the same loss, other insurance provisions ensure the insured recovers actual losses without profit, using pro rata, primary/excess, or contribution arrangements.",
    "A landlord has both a commercial property policy ($500,000 limit) and a separate inland marine policy ($100,000 limit) that both cover the same business equipment. A $60,000 loss occurs. Pro rata: the CP policy pays 5/6 ($50,000) and the inland marine pays 1/6 ($10,000).",
    "Other insurance = no double recovery. Pro rata = each pays its share proportional to limits. Primary/excess = first one pays, then the other. The insured always gets the loss — never more."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 3 — PROPERTY FUNDAMENTALS (selected high-priority lessons)
# ═══════════════════════════════════════════════════════════════════════

"property-valuation": (
    """How an insurer values a loss at the time of claim is one of the most tested concepts in property insurance. Two primary valuation methods appear on every P&C exam.

Actual cash value (ACV) is defined as replacement cost minus depreciation. It represents the fair market value of the item at the time of loss — what you could have sold it for just before it was destroyed. ACV reflects the fact that a 10-year-old roof is not worth as much as a brand-new one. When an insurer pays ACV on a $15,000 roof that is 5 years into a 15-year expected lifespan, it pays $15,000 × (10/15) = $10,000 — reflecting 5/15 depreciation.

Replacement cost value (RCV) pays what it actually costs to repair or replace the damaged property with new materials of like kind and quality, without deducting for depreciation. An RCV policy on a 10-year-old roof pays what a new roof costs today. RCV policies typically cost more in premium because they expose the insurer to higher claim payments.

The difference between ACV and RCV matters enormously at claim time. A homeowner with an ACV policy on an old roof may receive far less than they need to actually replace it. For this reason, many insurers offer replacement cost endorsements that upgrade ACV policies.

Two less-common valuation methods also appear on the exam. Agreed value (or stated value) fixes the settlement amount at policy inception — the insurer and insured agree on the value, and that amount is paid on a total loss without further negotiation. Functional replacement cost replaces with materials that are functionally equivalent but less expensive — used for older buildings where exact reproduction would be impractical.

For the exam, always be able to calculate ACV given replacement cost and age/life expectancy, and understand that RCV is always greater than or equal to ACV (since ACV deducts depreciation).
""",
    "Property losses are valued using actual cash value (replacement cost minus depreciation) or replacement cost (full new cost without depreciation deduction).",
    "A 6-year-old water heater with a 12-year life expectancy is destroyed. Replacement cost is $900. ACV = $900 × (6/12) = $450. An ACV policy pays $450; an RCV policy pays $900.",
    "ACV = RC minus depreciation. RCV = full new cost. ACV = fair market value. RCV = new for old. Remember: 'ACV ages the asset; RCV renews it.'"
),

"coinsurance": (
    """The coinsurance clause is one of the most calculation-intensive concepts on the P&C exam. It exists to encourage property owners to insure their property to its full (or near-full) value, rather than underinsuring to save on premium.

Most commercial property policies have an 80% coinsurance requirement. This means the insured must carry coverage equal to at least 80% of the property's replacement cost value. If the insured carries less than 80%, they become a co-insurer — meaning they share proportionately in any loss.

The coinsurance formula is: Payment = (Amount of Insurance Carried ÷ Amount Required) × Loss Amount.

Example: A building has a replacement cost of $500,000. The 80% coinsurance requirement means coverage should be at least $400,000. The insured only carries $300,000. A $100,000 partial loss occurs. Payment = ($300,000 ÷ $400,000) × $100,000 = 0.75 × $100,000 = $75,000. The insured bears the remaining $25,000 as a coinsurance penalty.

Key points for the exam: the coinsurance penalty only applies to partial losses (not total losses, since the policy limit caps payment regardless). The penalty is calculated as a ratio of carried to required insurance, not as the coinsurance percentage. If the insured carries the required amount or more, the full loss is paid (up to the policy limit). The agreed value endorsement suspends the coinsurance clause entirely.

A common trap question: the coinsurance calculation uses the replacement cost at the time of loss, not at the time the policy was issued. If property values increase and the insured doesn't update their coverage limits, they may find themselves penalized at claim time.
""",
    "The coinsurance clause requires insuring property to a minimum percentage of its value; underinsurance results in a proportional reduction in claim payments.",
    "A $200,000 building with 80% coinsurance should be insured for at least $160,000. Insured for $120,000 and suffers a $40,000 loss: pays ($120,000 ÷ $160,000) × $40,000 = $30,000. The insured bears $10,000 as a coinsurance penalty.",
    "Formula: (Carried ÷ Required) × Loss = Payment. Required = Property Value × Coinsurance %. Carry enough and get full payment; carry less and become your own co-insurer."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 4 — CASUALTY FUNDAMENTALS (selected high-priority lessons)
# ═══════════════════════════════════════════════════════════════════════

"negligence": (
    """Negligence is the legal foundation of most liability insurance claims. Understanding its four required elements is essential for the P&C exam.

To prove negligence, the injured party (plaintiff) must establish all four elements. First, the defendant owed a legal duty of care to the plaintiff. The nature of this duty depends on the relationship — a property owner owes a higher duty to invited guests than to trespassers. Second, the defendant breached that duty by failing to act as a reasonable person would under the circumstances. Third, the breach was the proximate cause of the harm — meaning it was the direct, dominant cause that set the chain of events in motion. Fourth, the plaintiff suffered actual damages — measurable injury or loss.

If any one of these four elements is missing, there is no negligence claim. No duty means no liability. No breach means no negligence. No causation means the defendant is not responsible even if negligent. No damages means there is nothing to compensate.

Two doctrines modify negligence in different states. In contributory negligence states (a minority), any fault by the plaintiff — even 1% — bars recovery completely. In comparative negligence states (most states), the plaintiff's recovery is reduced by their percentage of fault. Pure comparative negligence allows recovery regardless of the plaintiff's fault percentage; modified comparative negligence bars recovery if the plaintiff is 50% or 51% at fault (depending on the state).

Vicarious liability is another important concept: employers are liable for the negligent acts of employees acting within the scope of employment (respondeat superior). This is why businesses need general liability insurance — they can be held responsible for employee conduct even if they were not personally negligent.
""",
    "Negligence requires proving duty, breach, proximate causation, and actual damages — all four must be present for liability to attach.",
    "A store owner fails to clean up a spill (breach of duty to maintain safe premises). A customer slips and breaks their arm (actual damages). The spill was the direct cause (proximate cause). The owner is liable for the customer's medical bills and lost wages.",
    "DBCD: Duty, Breach, Causation, Damages. All four required. Miss one = no negligence. Comparative negligence reduces recovery by fault %; contributory negligence bars it entirely."
),

# ═══════════════════════════════════════════════════════════════════════
# MODULE 13 — ETHICS AND PRODUCER RESPONSIBILITIES
# ═══════════════════════════════════════════════════════════════════════

"producer-licensing": (
    """Insurance producers (agents and brokers) must be licensed in each state where they transact insurance business. Licensing ensures that producers have demonstrated basic competency and are subject to ongoing regulatory oversight.

To obtain a P&C producer license, an applicant typically must complete a pre-licensing education course (the number of hours varies by state), pass a state licensing examination, submit an application with a background check, and pay the required fees. Some states require fingerprinting. Once licensed, producers must complete continuing education (CE) credits during each renewal period to maintain their license.

There is an important distinction between agents and brokers. An agent represents the insurer — they have authority granted by the insurer to bind coverage and act on the insurer's behalf. A broker represents the insured — they shop the market on the insured's behalf but typically cannot bind coverage themselves (they must contact the insurer or agent to bind). In practice, many producers act as both agents and brokers in different transactions.

Non-resident licensing allows a producer licensed in their home state to obtain licenses in other states through a simplified process. Most states participate in reciprocal licensing arrangements that streamline this process.

Producers can lose their license for a variety of violations, including misrepresentation, fraud, misappropriation of premiums, providing false information on a license application, felony conviction, and unfair trade practices like twisting and rebating. The insurance department can suspend, revoke, or refuse to renew a license and impose fines.

For the exam, know that producers must be licensed in each state where they do business, that continuing education is required for renewal, and that the most serious violations (fraud, misappropriation) result in license revocation and potential criminal prosecution.
""",
    "Insurance producers must be licensed in each state where they transact business, passing a state exam and maintaining CE credits for renewal.",
    "A licensed California agent who wants to also sell insurance to clients in Nevada must obtain a non-resident Nevada license — their California license gives them no authority in Nevada.",
    "Licensed per state. Pass the exam. Complete CE to renew. Agent = insurer's representative. Broker = insured's representative. Violations = suspension, revocation, or criminal charges."
),

"ethics-fiduciary": (
    """Insurance producers occupy a position of trust. Many of their obligations are fiduciary — meaning the producer's interests must be subordinated to the client's. Understanding these ethical obligations is heavily tested because they form the ethical backbone of the entire insurance profession.

A producer's fiduciary duties include acting in the client's best interest when recommending coverage, disclosing conflicts of interest, maintaining confidentiality of client information, and handling client funds with the highest standard of care.

Premium funds are the clearest example of fiduciary responsibility. When an insured pays a premium to a producer, those funds belong to the insured (and ultimately the insurer) — not the producer. Producers must maintain client premium funds in a separate, dedicated trust account. Commingling premium funds with personal or operating accounts is prohibited. Using premium funds for personal expenses — even temporarily — constitutes misappropriation, which is both a license violation and a crime.

Unfair trade practices are prohibited behaviors that harm consumers or competitors. The exam focuses on five key practices. Misrepresentation involves making false statements about policy benefits, terms, or an insurer's financial condition. Twisting involves using misrepresentation to induce a policyholder to drop an existing policy and replace it with another. Rebating involves offering or giving anything of value as an inducement to purchase insurance. Churning (internal replacement) involves replacing a policyholder's coverage within the same company unnecessarily for the producer's benefit. Defamation involves making false statements that harm a competitor's reputation.

The exam will present scenarios and ask you to identify which unfair trade practice is described. The key distinctions: twisting uses false information to induce replacement; rebating involves giving value as an inducement; misrepresentation is any false statement about a policy.
""",
    "Producers have fiduciary duties to clients — acting in their best interest, keeping premium funds in trust, and avoiding unfair trade practices like twisting and rebating.",
    "A producer convinces a client to drop their existing whole life policy and buy a new one by falsely claiming the existing policy has no cash value — this is twisting, an unfair trade practice that can result in license revocation.",
    "Fiduciary = client first. Premium funds in trust always. Twisting = lie to replace. Rebating = give value to induce. Misrepresentation = any false statement. All are illegal."
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

            # Only update if the current body is a stub (< 300 chars)
            current_len = len(lesson.body or "")
            if current_len >= 300:
                print(f"  SKIP (already has content, {current_len} chars): {slug}")
                skipped += 1
                continue

            lesson.body = body.strip()
            lesson.summary = summary.strip()
            lesson.example = example.strip()
            lesson.memory_tip = memory_tip.strip()
            updated += 1
            print(f"  UPDATED ({len(body)} chars): {slug}")

        db.commit()
        print(f"\nDone: {updated} lessons updated, {skipped} skipped (already have content), {not_found} not found.")
        print("Re-run after adding more content without risk of overwriting real content.")
    finally:
        db.close()


if __name__ == "__main__":
    load_content()
