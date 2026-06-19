#!/usr/bin/env python3
"""
gap_modules_seed.py — Content Gap Modules
Adds 6 modules covering topics commonly tested on licensing exams
that weren't fully covered in the existing P&C / L&H course content.

Modules:
  1. Indexed Products (IUL + FIA)               — course='lh'
  2. Tax-Advantaged Health Accounts (FSA/HSA/HRA)— course='lh'
  3. Medicare Supplement / Medigap               — course='lh'
  4. Retirement Plans & Special Life Concepts    — course='lh'
  5. Cyber Liability Insurance                   — course='pc'
  6. Business Disability Income                  — course='lh'

Run from pc-license-prep-server-v2/:
    .venv/bin/python3 scripts/gap_modules_seed.py
Safe to re-run — skips existing slugs.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import select, text
from app.database import SessionLocal, create_all
from app.models import Module, Lesson, Term, Question, AnswerChoice


# ── MODULE 1: INDEXED PRODUCTS ────────────────────────────────────────────────

INDEXED_PRODUCTS_QUESTIONS = [
    ("A Fixed Indexed Annuity (FIA) credits interest based on:",
     "multiple_choice", "standard",
     "A Fixed Indexed Annuity credits interest linked to the performance of an external index (like the S&P 500) rather than a fixed rate. The annuity itself is not directly invested in the market — it is a fixed insurance product with index-linked crediting.",
     [("The performance of an external market index, subject to caps, floors, and participation rates", True, "Correct. FIAs link interest crediting to an index's performance, but the owner's principal is not directly invested in equities."),
      ("A fixed interest rate declared by the insurer each year", False, "A fixed rate product is a traditional fixed annuity, not an indexed annuity."),
      ("The actual investment return of an underlying portfolio of stocks", False, "Variable annuities invest in subaccounts directly in the market. FIAs are not invested in equities — they use index-linked crediting formulas."),
      ("The prime lending rate set by the Federal Reserve", False, "Prime rate is not an indexing basis for FIAs.")]),

    ("In an indexed annuity, the 'participation rate' refers to:",
     "multiple_choice", "standard",
     "The participation rate determines what percentage of the index's gain is credited to the annuity. For example, a 70% participation rate with an index gain of 10% results in a 7% credit to the annuity.",
     [("The percentage of the index gain that is credited to the annuity", True, "Correct. A participation rate of 80% on a 10% index gain would credit 8% to the annuity contract."),
      ("The percentage of premium that is invested in the stock market", False, "FIA premiums are not invested directly in the market; the participation rate refers to index gain crediting."),
      ("The percentage of the annuity's value that is surrender-charge-free each year", False, "Surrender-charge-free withdrawals are governed by a different provision — the free withdrawal amount."),
      ("The portion of the contract that participates in guaranteed minimum interest", False, "Guaranteed minimum interest is a separate feature of FIAs from the participation rate.")]),

    ("The 'cap rate' in a Fixed Indexed Annuity limits:",
     "multiple_choice", "standard",
     "The cap rate sets the maximum interest rate that can be credited in a given crediting period, regardless of how well the index performs. If the index gains 20% but the cap is 8%, only 8% is credited.",
     [("The maximum interest rate that can be credited regardless of index performance", True, "Correct. The cap rate is the ceiling on index-linked interest crediting in a given period."),
      ("The minimum interest rate that will be credited regardless of index performance", False, "The minimum crediting rate is the floor (typically 0%), not the cap rate."),
      ("The total amount of premium that can be deposited into the annuity", False, "Premium limits are not referred to as a cap rate."),
      ("The maximum surrender charge that can be applied to withdrawals", False, "Surrender charges are a separate concept from the cap rate.")]),

    ("The 'floor' in a Fixed Indexed Annuity guarantees:",
     "multiple_choice", "standard",
     "The floor is the minimum interest credit percentage — typically 0%. This means that even if the index declines, the annuity owner cannot lose principal due to negative index performance. The floor is a key consumer protection feature of FIAs.",
     [("A minimum interest credit of 0% — the owner cannot lose principal due to index declines", True, "Correct. The floor (typically 0%) protects the annuity owner from negative index returns. If the index loses 15%, the crediting rate is 0%, not -15%."),
      ("A guaranteed minimum death benefit for the owner's beneficiaries", False, "The floor refers to minimum index crediting, not death benefit guarantees."),
      ("The minimum withdrawal amount the owner must take each year", False, "Minimum withdrawals relate to required minimum distributions from qualified accounts, not the FIA floor."),
      ("A guaranteed minimum return equal to the 10-year Treasury rate", False, "The floor is not tied to Treasury rates; it is typically set at 0% by the insurer.")]),

    ("Indexed Universal Life (IUL) insurance differs from traditional Universal Life because IUL:",
     "multiple_choice", "standard",
     "IUL policies credit interest based on the performance of a stock market index rather than the insurer's declared current interest rate. IUL policies retain the flexible premium and adjustable death benefit features of traditional UL while adding index-linked crediting.",
     [("Credits interest linked to a stock market index rather than a declared fixed rate", True, "Correct. IUL uses index-linked crediting while retaining UL's flexible premium and adjustable death benefit features."),
      ("Invests the cash value directly in equity subaccounts chosen by the policyholder", False, "Variable life/VUL invests in subaccounts. IUL uses index-linked crediting formulas; the cash value is not directly invested in equities."),
      ("Provides a guaranteed fixed interest rate for the life of the policy", False, "A guaranteed fixed rate describes whole life or fixed UL, not IUL."),
      ("Has no surrender charges or free withdrawal limitations", False, "IUL policies typically have surrender charges during the early policy years.")]),

    ("A 'spread' or 'margin' in an indexed annuity works by:",
     "multiple_choice", "standard",
     "Some FIAs use a spread (also called margin or asset fee) instead of or in addition to a cap rate. The spread is subtracted from the index gain before crediting. For example, if the index gains 10% and the spread is 3%, the credited rate is 7%.",
     [("Subtracting a set percentage from the index gain before crediting interest to the contract", True, "Correct. A spread is deducted from the index return before crediting. If the index earns 8% and the spread is 2%, the owner is credited 6%."),
      ("Adding a guaranteed bonus percentage to any positive index return", False, "Adding a bonus describes an interest bonus feature, not a spread."),
      ("Investing the difference between premium paid and account value in equities", False, "FIAs do not invest in equities directly; the spread is a crediting formula element."),
      ("Guaranteeing that the credited rate will always be at least equal to the spread percentage", False, "The spread is deducted from gains, not a guaranteed minimum.")]),

    ("For suitability purposes, a Fixed Indexed Annuity is generally most appropriate for a client who:",
     "multiple_choice", "standard",
     "FIAs are suitable for clients who want principal protection (cannot lose to index declines) and some upside potential linked to market performance, but who do not need immediate access to funds and can accept crediting limitations like caps and participation rates.",
     [("Wants principal protection with some upside potential and does not need immediate liquidity", True, "Correct. FIAs are designed for clients who want protection from market losses while still benefiting from some market-linked growth, and who can commit funds for the surrender charge period."),
      ("Needs daily liquidity and access to all funds without any penalty", False, "FIAs have surrender charge periods that limit liquidity; they are not appropriate for clients needing immediate full access."),
      ("Wants the highest possible returns and is comfortable with full market risk", False, "Variable annuities or equity investments suit clients wanting maximum return with full market risk; FIAs limit both upside and downside."),
      ("Is seeking short-term savings over a 6-month horizon", False, "FIAs are long-term products with multi-year surrender charge periods; they are not appropriate for short-term savings.")]),

    ("When comparing an IUL policy to a Variable Universal Life (VUL) policy, which statement is correct?",
     "multiple_choice", "standard",
     "The key difference is investment risk: VUL subaccount values can decrease if markets decline, putting the policyholder's cash value at direct market risk. IUL uses index-linked crediting with a floor that prevents negative credits — the cash value cannot decline due to index performance.",
     [("IUL has a floor protecting against negative credits; VUL cash value can decline with market losses", True, "Correct. IUL's floor (typically 0%) prevents negative index-linked credits. VUL cash value is directly tied to subaccount performance and can decline."),
      ("VUL has a floor and IUL does not", False, "It is IUL that has a floor. VUL subaccounts are directly invested in the market with no floor protection."),
      ("Both IUL and VUL invest cash value directly in equity subaccounts", False, "Only VUL invests cash value directly in subaccounts. IUL uses index-linked crediting without direct equity investment."),
      ("IUL policies have no caps or participation rate limitations on interest crediting", False, "IUL policies do have caps, participation rates, or spreads that limit upside crediting.")]),

    ("The 'annual reset' (or 'annual point-to-point') crediting method in an indexed annuity means:",
     "multiple_choice", "standard",
     "With annual reset, the index gain is measured from the beginning to the end of each contract year. Any gain is locked in at year-end, and the next year starts fresh from the new index value — so prior losses are not carried forward.",
     [("The index starting point resets each year, locking in gains and eliminating prior year losses from future calculations", True, "Correct. Annual reset locks in gains each year and starts fresh, so a down year doesn't require 'recovery' before new gains are credited."),
      ("The contract automatically renews with new cap rates every year", False, "While cap rates may change at renewal, the annual reset specifically refers to the index measurement method."),
      ("The owner receives the index gain once per year in a cash distribution", False, "Annual reset is a crediting formula method, not a cash distribution schedule."),
      ("The insurer resets all fees and charges to zero at the start of each contract year", False, "Annual reset refers to the index measurement method, not fee resets.")]),

    ("A producer recommending a Fixed Indexed Annuity must disclose which of the following to the client?",
     "multiple_choice", "standard",
     "Suitability and best-interest standards require producers to disclose material product features that affect value and risk, including surrender charges, the indexing method, and any limitations on crediting such as caps and participation rates.",
     [("Surrender charges, the indexing method, cap rates, and participation rates", True, "Correct. Producers must disclose all material features of the FIA including surrender charges, crediting method, and crediting limitations."),
      ("Only the guaranteed minimum interest rate — other features are proprietary", False, "All material features including caps, participation rates, and surrender charges must be disclosed."),
      ("Only information that the client specifically asks about", False, "Best-interest and suitability standards require proactive disclosure of material information, not just reactive disclosure."),
      ("Nothing beyond the standard illustrations provided by the insurer", False, "Illustrations are important but producers have independent disclosure obligations under suitability rules.")]),

    ("An indexed annuity's 'point-to-point' crediting method measures index performance:",
     "multiple_choice", "standard",
     "Point-to-point crediting measures the index value at two specific dates — typically the contract anniversary dates — and credits interest based on the change between those two points.",
     [("From a starting index value to an ending index value over a defined crediting period", True, "Correct. Point-to-point measures the index at the start and end of the crediting period and credits the gain (subject to cap/participation rate/floor)."),
      ("Based on the highest index value achieved during the crediting period", False, "Measuring the highest value is the 'high water mark' or 'annual high' method, not standard point-to-point."),
      ("Using the average of daily index values throughout the crediting period", False, "Averaging daily values is the 'monthly average' or 'daily average' method, not point-to-point."),
      ("Only if the index is positive every single month during the period", False, "Point-to-point only looks at the start and end values; it does not require positive performance in every intervening month.")]),

    ("Which of the following is NOT a typical feature of an Indexed Universal Life (IUL) policy?",
     "multiple_choice", "standard",
     "IUL policies have flexible premiums, adjustable death benefits, index-linked crediting, and no direct market investment. They do not guarantee that cash value will grow to a specific target amount by a specified date.",
     [("A guaranteed cash value target amount that will be reached by a specific date", True, "Correct. IUL does not guarantee that cash value will reach a specific amount by a specific date. That is more characteristic of endowment products."),
      ("Flexible premium payments that can be adjusted by the policyholder", False, "Flexible premiums ARE a feature of IUL — this is a characteristic of UL-type products."),
      ("Interest crediting linked to a stock market index", False, "Index-linked crediting IS the defining feature of IUL."),
      ("A floor that prevents negative interest credits due to index declines", False, "A floor (typically 0%) IS a standard feature of IUL.")]),

    ("If an IUL policy's cash value is insufficient to cover the monthly cost of insurance, the policy will:",
     "multiple_choice", "standard",
     "Like all Universal Life policies, IUL will lapse if the cash value is insufficient to cover the monthly deductions (cost of insurance, expense charges). This can happen if premiums are too low, credited interest is minimal, or withdrawals deplete the cash value.",
     [("Lapse unless the policyholder makes an additional premium payment to cover the shortfall", True, "Correct. IUL — like all UL policies — will lapse if the cash value cannot cover the monthly deductions. The policyholder must fund the policy to keep it in force."),
      ("Automatically convert to term insurance at no additional cost", False, "Automatic conversion to term is not a standard IUL feature when cash value is depleted."),
      ("Maintain coverage with the insurer funding the shortfall as a loan", False, "The insurer does not fund coverage shortfalls as a loan. The policyholder must pay additional premiums."),
      ("Continue in force indefinitely using the credited index returns alone", False, "If cash value is insufficient to cover monthly charges, the policy will lapse regardless of future crediting expectations.")]),

    ("In comparing FIA and traditional fixed annuities for a conservative client, the FIA offers:",
     "multiple_choice", "standard",
     "Compared to a traditional fixed annuity, a FIA offers the potential for higher returns (when the index performs well) while maintaining principal protection via the floor. The trade-off is that upside is limited by caps and participation rates.",
     [("Potential for higher returns than a fixed annuity, while still protecting principal from market losses", True, "Correct. A FIA can credit more than a traditional fixed annuity when markets perform well, while the floor protects against negative credits."),
      ("Guaranteed returns higher than any fixed annuity regardless of market conditions", False, "FIA returns depend on index performance; they are not always higher than fixed annuities."),
      ("Unlimited upside potential equal to actual index returns with no crediting limitations", False, "FIAs have caps, participation rates, or spreads that limit upside potential."),
      ("Greater liquidity than a fixed annuity with shorter surrender charge periods", False, "FIAs typically have surrender charge periods similar to or longer than traditional fixed annuities.")]),

    ("Which regulatory body must a producer register with to sell Variable Universal Life (VUL) policies, unlike IUL policies?",
     "multiple_choice", "standard",
     "VUL is classified as a security because the policyholder bears the investment risk. Producers must hold a FINRA securities registration (Series 6 or Series 7) in addition to their state insurance license to sell VUL. IUL is a fixed insurance product and requires only a state insurance license.",
     [("FINRA — producers need a securities registration in addition to their insurance license", True, "Correct. VUL is a security requiring FINRA registration (Series 6 or 7). IUL is a fixed product requiring only a state insurance license."),
      ("The SEC only — state insurance licensing is not required for VUL", False, "Both state insurance licensing AND FINRA registration are required for VUL."),
      ("No additional registration — a standard insurance license covers both IUL and VUL", False, "VUL requires a securities registration (FINRA) that IUL does not require."),
      ("The state insurance department must approve each VUL producer individually", False, "State licensing through the standard exam process applies; FINRA handles the additional securities registration required for VUL.")]),

    ("The guaranteed minimum accumulation benefit (GMAB) rider on a FIA guarantees:",
     "multiple_choice", "standard",
     "A GMAB rider guarantees that after a specified holding period, the contract value will be at least a stated minimum — often the original premium or a percentage of it — regardless of how the index performed.",
     [("That the contract value will be at least a minimum amount after a specified holding period", True, "Correct. A GMAB guarantees a minimum account value after a defined period, protecting the owner if index-linked crediting results in minimal growth."),
      ("That the annuity will generate lifetime income payments regardless of account value", False, "Lifetime income guarantees are provided by GLWB (Guaranteed Lifetime Withdrawal Benefit) riders, not GMAB."),
      ("That the owner will always receive the full cap rate regardless of index performance", False, "The GMAB is a minimum value guarantee; it does not affect how the cap rate is applied."),
      ("That beneficiaries will receive the original premium as a death benefit regardless of withdrawals", False, "Death benefit protections are provided by specific death benefit riders, not GMAB.")]),

    ("A producer finds that a 72-year-old client with significant liquid assets and moderate risk tolerance is interested in a 10-year surrender period FIA primarily because the producer earns a higher commission. This is most likely:",
     "multiple_choice", "standard",
     "Recommending a long surrender period product primarily for the producer's commission benefit rather than the client's needs violates the best-interest standard. At age 72 with liquid assets, a 10-year surrender period may not serve the client's actual liquidity and estate planning needs.",
     [("A best-interest violation — the recommendation appears to benefit the producer rather than the client", True, "Correct. Recommending a product primarily for commission benefit rather than client suitability violates the best-interest standard."),
      ("Acceptable — producers are always entitled to recommend the highest-commission product available", False, "Producers are required to prioritize client interests over their own financial interests under best-interest standards."),
      ("Required — regulators mandate that producers recommend the highest-commission product in all cases", False, "Regulators require best-interest recommendations, not highest-commission recommendations."),
      ("Only problematic if the client has written about their concern in a suitability form", False, "The best-interest analysis is based on actual client needs, not just documented concerns.")]),

    ("Which of the following correctly describes the tax treatment of interest credited to a non-qualified Fixed Indexed Annuity?",
     "multiple_choice", "standard",
     "In a non-qualified annuity, credited interest grows tax-deferred — it is not taxed in the year credited. Taxes are owed when funds are withdrawn, at which point earnings are taxed as ordinary income (not capital gains). Withdrawals before age 59½ may also be subject to a 10% federal penalty.",
     [("Interest grows tax-deferred; withdrawals of earnings are taxed as ordinary income", True, "Correct. Non-qualified annuity interest grows tax-deferred and is taxed as ordinary income when withdrawn."),
      ("Interest is taxed as ordinary income in the year it is credited, like a savings account", False, "Annuity interest is not taxed in the year credited — that is the tax deferral advantage."),
      ("All withdrawals from a non-qualified FIA are completely tax-free", False, "Non-qualified annuity earnings are taxable on withdrawal; only Roth IRA distributions can be tax-free."),
      ("Interest is taxed as a long-term capital gain when withdrawn", False, "Annuity earnings are taxed as ordinary income, not capital gains, regardless of how long they accumulate.")]),

    ("The 'bonus' feature on some FIA contracts typically:",
     "multiple_choice", "standard",
     "Bonus annuities offer an upfront interest credit on premium (e.g., 5% bonus on deposit). However, bonuses typically come with trade-offs including longer surrender periods, lower cap rates, and the bonus may be subject to vesting schedules or recapture if the contract is surrendered early.",
     [("Credits additional interest upfront but often comes with trade-offs like longer surrender periods or lower caps", True, "Correct. Bonus features provide upfront value but producers must disclose the corresponding trade-offs, which are material to suitability."),
      ("Provides a guaranteed profit over any other non-bonus annuity with certainty", False, "Bonus annuities are not always superior; trade-offs must be evaluated in the context of the client's specific needs."),
      ("Eliminates all surrender charges for the life of the contract", False, "Bonus contracts typically have longer, not shorter, surrender charge periods."),
      ("Only applies if the client deposits more than $100,000 in premium", False, "Bonus features are a product design element, not universally tied to a minimum deposit amount.")]),

    ("In an IUL policy, the cost of insurance (COI) typically:",
     "multiple_choice", "standard",
     "In IUL (and all UL) policies, the cost of insurance increases with age and is deducted monthly from the policy's cash value. Older policyholders pay higher COI charges, which can strain the policy if cash value is not sufficient to cover rising charges.",
     [("Increases as the insured ages, deducted monthly from the policy's cash value", True, "Correct. COI increases with age in all UL-type policies including IUL. Monthly deductions from cash value cover the net amount at risk."),
      ("Is fixed for the life of the policy regardless of the insured's age", False, "Fixed insurance costs are a feature of whole life; UL and IUL have age-based COI that increases over time."),
      ("Is paid separately and does not reduce the policy's cash value", False, "COI is deducted directly from the IUL cash value, reducing it monthly."),
      ("Is waived entirely once the cash value exceeds the death benefit amount", False, "COI is not waived based on the relationship between cash value and death benefit.")]),

    ("A client surrenders a non-qualified FIA for $150,000 when their original premium was $100,000. The client must report:",
     "multiple_choice", "standard",
     "When a non-qualified annuity is surrendered, the owner must report the gain ($150,000 - $100,000 = $50,000) as ordinary income in the year of surrender. The original $100,000 of premium (basis) is not taxed again since it was contributed with after-tax dollars.",
     [("$50,000 of ordinary income — the gain over the original premium", True, "Correct. The $50,000 gain ($150,000 - $100,000 basis) is taxable as ordinary income. The original $100,000 premium is returned tax-free as it was after-tax money."),
      ("$150,000 of ordinary income — the full surrender value", False, "The return of original premium (basis) is not taxable. Only the $50,000 gain is taxable."),
      ("$0 — annuity surrenders are always tax-free", False, "Non-qualified annuity gains are taxable as ordinary income on surrender."),
      ("$50,000 of long-term capital gain taxed at reduced rates", False, "Annuity gains are taxed as ordinary income, not capital gains, regardless of how long they accumulated.")]),
]

# ── MODULE 2: TAX-ADVANTAGED HEALTH ACCOUNTS ──────────────────────────────────

TAX_HEALTH_ACCOUNTS_QUESTIONS = [
    ("A Health Savings Account (HSA) is only available to individuals who are enrolled in:",
     "multiple_choice", "standard",
     "HSA eligibility requires enrollment in a High Deductible Health Plan (HDHP). You cannot contribute to an HSA if you are covered by a non-HDHP health plan, enrolled in Medicare, or claimed as a dependent on another person's tax return.",
     [("A High Deductible Health Plan (HDHP) that meets IRS minimum deductible requirements", True, "Correct. Only HDHP enrollees are eligible to contribute to an HSA. The HDHP must meet IRS minimum deductible and maximum out-of-pocket requirements."),
      ("Any employer-sponsored health insurance plan", False, "HSA eligibility is limited to HDHP enrollees; enrollment in any health plan does not qualify."),
      ("Medicare Part A and Part B", False, "Medicare enrollment disqualifies individuals from contributing to an HSA."),
      ("A Preferred Provider Organization (PPO) plan regardless of deductible level", False, "A PPO can qualify as an HDHP if it meets IRS deductible minimums, but enrollment in any PPO alone does not qualify.")]),

    ("The primary tax advantage of a Health Savings Account (HSA) is:",
     "multiple_choice", "standard",
     "HSAs offer a triple tax advantage: contributions are tax-deductible (or pre-tax through payroll deduction), growth is tax-free, and withdrawals for qualified medical expenses are tax-free. This makes HSAs unique among tax-advantaged accounts.",
     [("Contributions are tax-deductible, growth is tax-free, and qualified withdrawals are tax-free", True, "Correct. HSAs have a triple tax advantage — one of the most powerful tax-advantaged vehicles available."),
      ("Contributions are made with after-tax dollars but qualified withdrawals are tax-free", False, "Roth accounts use after-tax contributions for tax-free withdrawals. HSA contributions are tax-deductible (pre-tax)."),
      ("Contributions are tax-deductible but all withdrawals are taxed as ordinary income", False, "Traditional IRA withdrawals are taxed; HSA qualified withdrawals are tax-free."),
      ("Only employer contributions to an HSA are tax-free — employee contributions are taxed", False, "Both employee and employer HSA contributions can be pre-tax or deductible.")]),

    ("Unused HSA funds at the end of the year:",
     "multiple_choice", "standard",
     "Unlike a Flexible Spending Account (FSA), HSA funds roll over indefinitely from year to year. There is no 'use it or lose it' rule for HSAs. Funds can accumulate and even be invested for long-term growth.",
     [("Roll over and accumulate indefinitely — there is no 'use it or lose it' rule for HSAs", True, "Correct. HSA funds are owned by the individual and roll over without limit — a key advantage over FSAs."),
      ("Are forfeited if not used within the plan year, similar to an FSA", False, "The 'use it or lose it' rule applies to FSAs, not HSAs. HSAs roll over indefinitely."),
      ("Must be withdrawn or rolled over into an IRA by age 65", False, "HSA funds do not need to be moved to an IRA. After age 65, withdrawals for non-medical purposes are penalty-free (though taxed as income)."),
      ("Are automatically used to pay next year's health insurance premiums", False, "HSA funds do not automatically pay premiums; the accountholder decides how to use the funds.")]),

    ("A Flexible Spending Account (FSA) differs from an HSA primarily in that an FSA:",
     "multiple_choice", "standard",
     "The key FSA-HSA difference: FSA funds are generally subject to a 'use it or lose it' rule (forfeited if unused by year-end, though some plans allow a grace period or $610 carryover). FSAs do not require HDHP enrollment and are employer-sponsored.",
     [("Is subject to a 'use it or lose it' rule and does not require enrollment in an HDHP", True, "Correct. FSAs have the 'use it or lose it' rule (forfeiture of unused funds), do not require HDHP enrollment, and are employer-sponsored."),
      ("Offers a triple tax advantage identical to an HSA", False, "FSAs offer tax advantages but the 'use it or lose it' rule and lack of rollover mean they are less flexible than HSAs."),
      ("Can be opened by self-employed individuals without employer sponsorship", False, "Health FSAs are employer-sponsored. Self-employed individuals cannot open a health FSA on their own."),
      ("Allows unlimited contribution rollovers from year to year", False, "FSAs have forfeiture rules or limited rollover. It is HSAs that roll over indefinitely.")]),

    ("A Health Reimbursement Arrangement (HRA) is:",
     "multiple_choice", "standard",
     "An HRA is funded exclusively by the employer — employees cannot contribute. The employer reimburses employees for qualified medical expenses tax-free. HRA funds not used in the year may roll over at the employer's discretion.",
     [("An employer-funded account that reimburses employees for qualified medical expenses tax-free", True, "Correct. HRAs are funded solely by the employer; employees cannot contribute. Reimbursements for qualified medical expenses are tax-free."),
      ("A joint employee-employer savings account similar to a 401(k)", False, "Only employers fund HRAs. There is no employee contribution component."),
      ("A type of health insurance plan with a high deductible", False, "HRAs are reimbursement accounts, not health insurance plans."),
      ("Available only to self-employed individuals with no employees", False, "HRAs are offered by employers to their employees; they are not limited to self-employed individuals.")]),

    ("Which of the following individuals is NOT eligible to contribute to an HSA?",
     "multiple_choice", "standard",
     "An individual enrolled in Medicare Part A or B is not eligible to make HSA contributions — even if they also have HDHP coverage. Other disqualifying conditions include being claimed as a dependent or having non-HDHP health coverage.",
     [("A person enrolled in Medicare Part A", True, "Correct. Medicare enrollment (Part A, Part B, or both) disqualifies an individual from making HSA contributions."),
      ("A person enrolled in an HDHP with a $2,000 annual deductible", False, "Enrollment in a qualifying HDHP makes a person eligible, not ineligible, for HSA contributions."),
      ("A person who receives employer contributions to an HSA on their behalf", False, "Receiving employer contributions does not disqualify someone from also making personal contributions."),
      ("A person who is a US citizen living and working abroad", False, "Citizenship status and location do not disqualify HSA contributions as long as the person meets eligibility requirements.")]),

    ("HSA withdrawals used for non-qualified medical expenses before age 65 are subject to:",
     "multiple_choice", "standard",
     "Non-qualified HSA withdrawals before age 65 are taxed as ordinary income AND subject to an additional 20% penalty. After age 65, non-qualified withdrawals are only subject to ordinary income tax (no penalty) — similar to a traditional IRA.",
     [("Ordinary income tax plus a 20% penalty tax", True, "Correct. Pre-65 non-qualified HSA withdrawals are taxed as income AND penalized 20%."),
      ("A 10% penalty only — no income tax applies", False, "Both income tax and a 20% penalty apply to pre-65 non-qualified withdrawals."),
      ("No tax or penalty — HSA withdrawals are always tax-free", False, "Only qualified medical expense withdrawals are tax-free. Non-qualified withdrawals are taxed and penalized."),
      ("A flat 15% tax regardless of the owner's income tax bracket", False, "The tax is ordinary income tax at the owner's marginal rate plus a 20% penalty.")]),

    ("For a self-employed individual, contributions to an HSA are:",
     "multiple_choice", "standard",
     "Self-employed individuals who are enrolled in an HDHP can make HSA contributions and deduct them as an above-the-line deduction on their personal income tax return — they do not need an employer to sponsor the HSA.",
     [("Deductible above the line on the individual's personal income tax return", True, "Correct. Self-employed HDHP enrollees can open and contribute to an HSA and deduct contributions on their personal return."),
      ("Not permitted — HSAs are only available through employer plans", False, "Self-employed individuals can open and fund their own HSAs if they have qualifying HDHP coverage."),
      ("Deductible only as a business expense, not a personal deduction", False, "HSA contributions by self-employed individuals are a personal above-the-line deduction, not a business expense."),
      ("Subject to self-employment tax in addition to income tax", False, "HSA contributions are pre-tax/deductible; they reduce taxable income and are not subject to self-employment tax.")]),

    ("A Dependent Care FSA (DCFSA) is used to pay for:",
     "multiple_choice", "standard",
     "A Dependent Care FSA reimburses eligible dependent care expenses such as daycare, after-school programs, and summer day camps for children under 13 or for other qualifying dependents who cannot care for themselves.",
     [("Childcare and other qualifying dependent care expenses, such as daycare for children under 13", True, "Correct. A DCFSA pays for qualifying dependent care expenses — not medical expenses. It is distinct from a health FSA."),
      ("The employee's own medical expenses and health insurance premiums", False, "A health FSA covers medical expenses; a DCFSA covers dependent care expenses — these are separate account types."),
      ("Long-term care insurance premiums for the employee's parents", False, "Long-term care premiums are not a qualifying expense for a DCFSA."),
      ("College tuition and educational expenses for dependent children", False, "Educational expenses are covered by 529 plans or Coverdell ESAs, not a DCFSA.")]),

    ("The IRS annual HSA contribution limit for self-only HDHP coverage in a typical year is:",
     "multiple_choice", "standard",
     "The IRS sets annual HSA contribution limits that are adjusted periodically for inflation. The self-only limit is approximately $4,150 (2024) and the family limit is approximately $8,300 (2024). Individuals age 55+ can make additional $1,000 catch-up contributions.",
     [("A set IRS limit adjusted annually for inflation, with a higher limit for family coverage", True, "Correct. HSA contribution limits are set and adjusted annually by the IRS, with higher limits for family HDHP coverage than self-only coverage."),
      ("There is no annual limit — any amount can be contributed to an HSA", False, "HSAs have annual contribution limits set by the IRS."),
      ("The same limit regardless of whether coverage is individual or family", False, "The family HDHP coverage limit is significantly higher than the self-only limit."),
      ("Limited to 50% of the annual HDHP deductible", False, "HSA limits are set by the IRS, not calculated as a percentage of the deductible.")]),

    ("Which account type is owned by the individual and portable if they change jobs?",
     "multiple_choice", "standard",
     "An HSA is owned by the individual — it is portable and stays with the person regardless of job changes or loss of HDHP coverage (though new contributions require HDHP enrollment). FSA funds are typically forfeited if employment ends mid-year, and HRAs are employer-owned.",
     [("HSA — it is individually owned and portable across employers", True, "Correct. The HSA belongs to the individual, not the employer. It is fully portable."),
      ("FSA — unused balances transfer to the new employer's FSA automatically", False, "FSA funds generally cannot transfer to a new employer's plan; unused balances are typically forfeited."),
      ("HRA — employees retain full HRA balances when changing jobs", False, "HRAs are employer-funded and employer-owned; balances typically do not transfer to a new employer."),
      ("All three — HSA, FSA, and HRA are all individually portable", False, "Only the HSA is individually owned and portable. FSAs and HRAs are employer-sponsored and not portable.")]),

    ("An employer contributes to an employee's HSA. For the employee, this contribution is:",
     "multiple_choice", "standard",
     "Employer HSA contributions are excluded from the employee's gross income — they are not subject to income tax, Social Security tax, or Medicare tax. This is a significant tax advantage for both employer and employee.",
     [("Excluded from the employee's gross income — not subject to income, SS, or Medicare tax", True, "Correct. Employer HSA contributions are excluded from gross income and exempt from payroll taxes."),
      ("Included in the employee's gross income and taxed as ordinary income", False, "Employer HSA contributions are excluded from income — they are a tax-free employer benefit."),
      ("Subject to Social Security and Medicare taxes but not income tax", False, "Employer HSA contributions are excluded from all payroll taxes as well as income tax."),
      ("Deductible by the employer but taxable to the employee as a fringe benefit", False, "Employer HSA contributions are deductible by the employer AND tax-free to the employee.")]),

    ("A Limited Purpose FSA (LPFSA) can be used alongside an HSA to pay for:",
     "multiple_choice", "standard",
     "A Limited Purpose FSA is a special FSA designed to be compatible with HSA eligibility. It covers only dental and vision expenses (not general medical), allowing the individual to preserve HSA funds for other qualified medical expenses.",
     [("Dental and vision expenses only, preserving HSA eligibility", True, "Correct. An LPFSA covers only dental and vision to allow combined use with an HSA without disqualifying the individual from HSA contributions."),
      ("All medical expenses including physician visits and prescriptions", False, "A general health FSA would disqualify HSA eligibility. The Limited Purpose FSA is restricted to dental and vision."),
      ("Long-term care insurance premiums and home health aide costs", False, "Long-term care expenses are not LPFSA-eligible expenses."),
      ("Over-the-counter medications without a prescription", False, "OTC medications can be purchased with a health FSA or HSA; the LPFSA specifically covers dental and vision.")]),

    ("Which of the following is a qualified medical expense for HSA purposes?",
     "multiple_choice", "standard",
     "Qualified medical expenses for HSAs include items defined by IRS Section 213(d): doctor visits, prescription drugs, dental care, vision care, and many other healthcare costs. Cosmetic surgery and gym memberships are not qualified unless for a specific medical condition.",
     [("Prescription eyeglasses and contact lenses", True, "Correct. Vision care expenses including prescription eyeglasses and contacts are qualified medical expenses for HSA purposes."),
      ("Gym membership for general fitness", False, "General fitness expenses are not qualified medical expenses unless prescribed for a specific medical condition."),
      ("Cosmetic surgery to improve appearance", False, "Cosmetic surgery that is not medically necessary is not a qualified HSA expense."),
      ("Health insurance premiums for a standard employer plan", False, "Health insurance premiums are generally not qualified HSA expenses, with limited exceptions (COBRA, Medicare premiums after 65, and long-term care insurance).")]),

    ("After age 65, an HSA owner who withdraws funds for non-medical expenses:",
     "multiple_choice", "standard",
     "After age 65, HSA owners can withdraw funds for any reason. Non-medical withdrawals are taxed as ordinary income but are NOT subject to the 20% penalty. This makes the HSA function like a traditional IRA after 65 for non-medical withdrawals.",
     [("Pays ordinary income tax but no penalty — similar to a traditional IRA withdrawal", True, "Correct. After 65, non-qualified HSA withdrawals are taxed as ordinary income but free of the 20% penalty."),
      ("Pays a 20% penalty in addition to ordinary income tax", False, "The 20% penalty only applies before age 65. After 65, only ordinary income tax applies."),
      ("Makes all HSA withdrawals completely tax-free regardless of purpose", False, "Tax-free treatment applies only to qualified medical expense withdrawals, even after 65."),
      ("Must roll the funds into an IRA to avoid penalties", False, "After 65, non-qualified withdrawals simply trigger ordinary income tax; no rollover is required or needed.")]),

    ("A Health Reimbursement Arrangement (HRA) can generally be paired with which type of health plan?",
     "multiple_choice", "standard",
     "Traditional HRAs (not Qualified Small Employer HRAs or Individual Coverage HRAs) can be paired with any employer-sponsored health plan, including non-HDHP plans, as long as the plan is group coverage.",
     [("Any employer-sponsored group health plan, including non-HDHP plans", True, "Correct. Traditional HRAs are flexible and can be offered alongside any group health plan, not just HDHPs."),
      ("Only a High Deductible Health Plan — HRAs require HDHP enrollment", False, "HDHP requirement applies to HSAs, not traditional HRAs."),
      ("Only Medicare Advantage plans for retirees", False, "Traditional HRAs are employer-sponsored for active employees; other HRA types may cover retirees."),
      ("Only plans with zero deductibles — HRAs cannot be paired with any deductible plan", False, "There is no zero-deductible requirement for pairing with an HRA.")]),

    ("The maximum FSA contribution limit is set by:",
     "multiple_choice", "standard",
     "The IRS sets the maximum annual FSA contribution limit, which is adjusted periodically for inflation. Employers may set lower limits but cannot exceed the IRS maximum. The 2024 health FSA limit is $3,200.",
     [("The IRS, with annual limits adjusted for inflation", True, "Correct. IRS sets FSA contribution limits. Employers may set lower limits but cannot exceed the IRS maximum."),
      ("Each employer independently with no IRS limitation", False, "The IRS sets a maximum limit; employers can go lower but not higher."),
      ("ERISA with fixed limits that never change regardless of inflation", False, "ERISA governs plan structure, but FSA dollar limits are set by the IRS and adjusted for inflation."),
      ("The employee's chosen contribution amount with no maximum", False, "FSAs have IRS-set annual contribution maximums.")]),

    ("Which of the following correctly describes an HSA investment option?",
     "multiple_choice", "standard",
     "Once the HSA cash balance reaches a threshold set by the administrator (often $1,000-$2,000), the accountholder can invest the excess in mutual funds, stocks, or other investments. Investment gains grow tax-free and can be withdrawn tax-free for qualified medical expenses.",
     [("HSA funds above a threshold can be invested in mutual funds with tax-free growth", True, "Correct. HSA investment options allow excess funds to be invested. Growth is tax-free, and qualified withdrawals remain tax-free."),
      ("HSA funds can only be held in an FDIC-insured savings account — no investment option exists", False, "Many HSA administrators offer investment options for funds above a minimum balance threshold."),
      ("Investment gains in an HSA are taxed as long-term capital gains", False, "HSA investment gains are tax-free as long as they are used for qualified medical expenses."),
      ("HSA funds must be fully invested in a federally mandated money market fund", False, "No federal mandate requires HSA investment in money market funds; investment options vary by administrator.")]),

    ("An employee who over-contributes to their HSA in a given year faces:",
     "multiple_choice", "standard",
     "HSA over-contributions (above the IRS annual limit) are subject to a 6% excise tax on the excess amount for each year the excess remains in the account. The employee should withdraw the excess and any attributable earnings before the tax filing deadline to avoid the tax.",
     [("A 6% excise tax on the excess contribution for each year it remains in the account", True, "Correct. Over-contributions to an HSA are subject to a 6% excise tax annually until the excess is withdrawn."),
      ("A 20% penalty and loss of all HSA tax benefits", False, "The penalty is 6%, not 20%. Tax benefits are not permanently lost."),
      ("No penalty — excess HSA contributions are simply returned without consequence", False, "Excess contributions are penalized at 6% annually if not corrected."),
      ("Ordinary income tax on the entire HSA balance for that year", False, "Only the excess contribution amount is subject to penalty; the rest of the HSA balance is unaffected.")]),

    ("When comparing FSA and HSA accounts for a client who is self-employed with HDHP coverage, which is the better option?",
     "multiple_choice", "standard",
     "Self-employed individuals can open and contribute to an HSA but generally cannot open a health FSA (FSAs require employer sponsorship). Additionally, the HSA's rollover feature and portability make it superior for self-employed individuals.",
     [("HSA — self-employed individuals cannot open a health FSA; HSA also has rollover and portability advantages", True, "Correct. Self-employed individuals with HDHP coverage should use an HSA since FSAs are employer-sponsored and not available to the self-employed for health expenses."),
      ("FSA — because self-employed individuals can open any type of FSA independently", False, "Health FSAs are employer-sponsored; self-employed individuals generally cannot open their own health FSA."),
      ("Both are equally suitable for self-employed HDHP enrollees", False, "Only HSAs are available to self-employed individuals for health expense savings."),
      ("Neither — self-employed individuals must use a Keogh plan for healthcare savings", False, "Keogh plans are retirement savings vehicles; HSAs are the appropriate vehicle for healthcare savings for self-employed HDHP enrollees.")]),

    ("A Qualified Small Employer Health Reimbursement Arrangement (QSEHRA) is designed for:",
     "multiple_choice", "standard",
     "A QSEHRA allows small employers (fewer than 50 full-time equivalent employees) who do not offer group health insurance to reimburse employees tax-free for individual health insurance premiums and qualified medical expenses.",
     [("Small employers with fewer than 50 FTE employees who do not offer group health coverage", True, "Correct. QSEHRAs are available only to small employers (fewer than 50 FTE) who do not offer group health plans, allowing them to reimburse individual health insurance premiums."),
      ("Large employers with over 500 employees as an alternative to group health plans", False, "QSEHRAs are for small employers with fewer than 50 FTE employees, not large employers."),
      ("Self-employed individuals with no employees to reimburse their own health costs", False, "QSEHRAs require at least one employee; they are not for sole proprietors with no employees."),
      ("Only non-profit organizations regardless of employer size", False, "QSEHRAs are available to all qualifying small employers, not limited to non-profits.")]),
]

# ── MODULE 3: MEDIGAP ─────────────────────────────────────────────────────────

MEDIGAP_QUESTIONS = [
    ("Medicare Supplement (Medigap) insurance is designed to cover:",
     "multiple_choice", "standard",
     "Medigap policies cover some of the cost-sharing gaps in Original Medicare (Part A and Part B), such as deductibles, coinsurance, and copayments. Medigap does not cover services not covered by Medicare.",
     [("Gaps in Original Medicare coverage such as deductibles, coinsurance, and copayments", True, "Correct. Medigap fills cost-sharing gaps in Original Medicare — it does not add new covered services."),
      ("Prescription drugs not covered by Medicare Part B", False, "Prescription drugs are covered by Medicare Part D, not Medigap."),
      ("Long-term custodial care in a nursing home", False, "Long-term custodial care is not covered by Medicare or Medigap. Long-term care insurance is a separate product."),
      ("Services covered by Medicare Advantage plans", False, "Medigap works with Original Medicare, not Medicare Advantage. Medigap cannot be used with Medicare Advantage.")]),

    ("Medigap plans are standardized by the federal government, meaning:",
     "multiple_choice", "standard",
     "Federal law requires that Medigap plans with the same letter designation offer identical benefits regardless of which insurance company sells them. The only difference between insurers for the same plan letter is price.",
     [("Every company selling Plan G must offer the same benefits — only the premium differs", True, "Correct. Medigap standardization means Plan G from Insurer A provides identical benefits to Plan G from Insurer B — only premiums differ."),
      ("Each insurance company can design its own Medigap benefits for each plan letter", False, "Standardization prohibits benefit variation; only premiums can differ between insurers for the same plan letter."),
      ("Medigap premiums are set by the federal government, so all companies charge the same amount", False, "Only benefits are standardized; premiums vary by insurer, location, and rating method."),
      ("Medigap plans are optional supplements that insurers can offer or decline to sell in any state", False, "While insurers choose which plan letters to offer, those they do offer must meet standardized benefit requirements.")]),

    ("During the Medigap Open Enrollment Period, an applicant aged 65 or older who is enrolled in Medicare Part B:",
     "multiple_choice", "standard",
     "The Medigap open enrollment period is a 6-month window beginning the month a person is both age 65 or older AND enrolled in Medicare Part B. During this period, insurers must accept applicants and cannot charge higher premiums for pre-existing conditions.",
     [("Cannot be denied coverage and cannot be charged higher premiums due to health status", True, "Correct. The open enrollment period guarantees issue rights — applicants cannot be turned down or charged extra for health conditions."),
      ("Must pass a medical underwriting exam before coverage is issued", False, "Medical underwriting is prohibited during the Medigap open enrollment period."),
      ("Can only purchase Plan A during the open enrollment period", False, "All standardized Medigap plans offered in the state can be purchased during open enrollment."),
      ("Is automatically enrolled in a Medigap plan by their Medicare carrier", False, "Medigap enrollment is voluntary; there is no automatic enrollment.")]),

    ("Medigap Plan G is one of the most comprehensive plans available because it covers:",
     "multiple_choice", "standard",
     "Medigap Plan G covers nearly all Medicare cost-sharing including the Part A deductible, Part A coinsurance, Part B coinsurance, Part B excess charges, skilled nursing facility coinsurance, and foreign travel emergency coverage. The only gap is the Part B deductible.",
     [("Nearly all Medicare cost-sharing except the Medicare Part B deductible", True, "Correct. Plan G is comprehensive, covering Part A deductible, Part B coinsurance, excess charges, and skilled nursing coinsurance — but not the Part B annual deductible."),
      ("Everything including the Part B deductible with no out-of-pocket costs to the enrollee", False, "Plan G does not cover the Part B deductible. Plan F (not available to new enrollees after 2019) covered the Part B deductible."),
      ("Only hospitalization costs under Part A — no Part B benefits are included", False, "Plan G provides extensive coverage for both Part A and Part B cost-sharing."),
      ("Prescription drug costs as a supplement to Medicare Part D", False, "Medigap does not cover prescription drugs; that is Medicare Part D's role.")]),

    ("Which Medigap plan is no longer available to newly eligible Medicare beneficiaries after January 1, 2020?",
     "multiple_choice", "standard",
     "The MACRA Act of 2015 prohibited the sale of first-dollar coverage Medigap plans (Plans C and F) to individuals who become newly eligible for Medicare on or after January 1, 2020. Those enrolled before 2020 can keep their Plan C or F.",
     [("Plan C and Plan F — they covered the Part B deductible, which is now prohibited for new enrollees", True, "Correct. Plans C and F (and High Deductible Plan F) cannot be sold to new Medicare eligibles after 2020 because they covered the Part B deductible."),
      ("Plan G — it was phased out due to its comprehensive coverage", False, "Plan G remains available and is one of the most popular Medigap plans. It is Plan C and F that were restricted."),
      ("Plan N — due to cost-sharing changes under the ACA", False, "Plan N remains available to all Medicare beneficiaries."),
      ("Plan A — the original basic plan was discontinued", False, "Plan A remains available as the base benefit Medigap plan.")]),

    ("A Medigap policy's guaranteed issue right allows an enrollee to purchase a Medigap plan without medical underwriting when:",
     "multiple_choice", "standard",
     "Guaranteed issue rights arise in specific triggering events: losing employer coverage, moving out of a Medicare Advantage plan's service area, Medicare Advantage plan being discontinued, or losing other forms of creditable coverage.",
     [("They lose other health coverage due to no fault of their own, such as losing employer group coverage", True, "Correct. Losing employer coverage or losing Medicare Advantage coverage triggers a guaranteed issue right to purchase Medigap without underwriting."),
      ("They simply decide they prefer a Medigap plan over their current coverage at any time", False, "Guaranteed issue rights are triggered by specific qualifying events — they are not available just because someone wants to switch."),
      ("They turn 70 years old regardless of their current coverage", False, "Age 70 is not a guaranteed issue triggering event."),
      ("They apply for Medigap during the annual Medicare Open Enrollment period (Oct 15 - Dec 7)", False, "The Medicare annual open enrollment period applies to Part D and Medicare Advantage, not Medigap guaranteed issue rights.")]),

    ("Medicare Supplement insurance does NOT cover which of the following?",
     "multiple_choice", "standard",
     "Medigap policies fill gaps in Medicare Parts A and B. They do not cover prescription drugs (Part D), dental, vision, hearing, long-term custodial care, or services not covered at all by Original Medicare.",
     [("Routine dental care and prescription drugs", True, "Correct. Medigap does not cover dental care, vision, hearing, prescription drugs, or long-term custodial care."),
      ("Medicare Part A hospital coinsurance", False, "Part A hospital coinsurance IS covered by most Medigap plans (including Plan A, the minimum benefit plan)."),
      ("Medicare Part B coinsurance for physician services", False, "Part B coinsurance IS covered by most comprehensive Medigap plans (e.g., Plans G and N)."),
      ("Emergency care received outside the United States", False, "Foreign travel emergency coverage IS included in several Medigap plans (Plans C, D, F, G, M, N).")]),

    ("Medigap premiums are determined by three rating methods. 'Community rated' Medigap means:",
     "multiple_choice", "standard",
     "Community rating charges everyone the same premium regardless of age. 'Issue-age rated' charges based on age when first enrolled. 'Attained-age rated' increases premiums as the policyholder ages and tends to be the least favorable over the long term for enrollees who keep their policy for many years.",
     [("Everyone in the community pays the same premium regardless of age", True, "Correct. Community rating is the most favorable for older enrollees — premiums do not increase based on age."),
      ("Premiums are based on the age when the policy was first purchased", False, "Age at purchase determines premiums under 'issue-age rated' plans, not community rating."),
      ("Premiums increase annually based on the policyholder's current age", False, "Premiums that increase with the policyholder's current age are 'attained-age rated.'"),
      ("Premiums are set by CMS and are the same for all plans nationally", False, "CMS does not set Medigap premiums; they are set by insurers using one of three rating methods.")]),

    ("A beneficiary enrolled in a Medicare Advantage (Part C) plan wants to switch to Original Medicare and a Medigap policy. What should the producer inform them?",
     "multiple_choice", "standard",
     "When leaving a Medicare Advantage plan after the open enrollment period, the beneficiary may not have guaranteed issue rights for Medigap. They could face medical underwriting unless they qualify for a special guaranteed issue right.",
     [("They may be subject to medical underwriting when applying for Medigap unless they have a guaranteed issue right", True, "Correct. Leaving Medicare Advantage outside of special circumstances may not trigger a guaranteed issue right, meaning the applicant could be denied or charged more for Medigap."),
      ("They are automatically guaranteed Medigap coverage whenever they leave a Medicare Advantage plan", False, "Only specific qualifying events trigger guaranteed issue rights. Simply choosing to leave Medicare Advantage may not qualify."),
      ("They can keep their Medicare Advantage benefits while adding Medigap coverage simultaneously", False, "Medigap cannot be used with Medicare Advantage plans. The beneficiary must fully disenroll from Medicare Advantage."),
      ("Medicare Advantage and Medigap can be combined to provide triple coverage", False, "Medigap policies cannot be used alongside Medicare Advantage plans.")]),

    ("Under federal law, Medigap insurance companies must provide which minimum benefit in all plans?",
     "multiple_choice", "standard",
     "All Medigap plans must provide at minimum: Medicare Part A coinsurance for days 61-90 and 91-150, an additional 365 days of hospital coverage after Medicare benefits are exhausted, and Medicare Part B coinsurance or copayments. These are the core Plan A benefits.",
     [("Medicare Part A hospital coinsurance and an additional 365 hospital days after Medicare exhausts", True, "Correct. Plan A benefits — including Part A coinsurance and 365 extra hospital days — are mandatory minimum benefits in all Medigap plans."),
      ("Full coverage of the Medicare Part B deductible", False, "The Part B deductible is NOT a required minimum benefit; it is covered only by Plans C and F (unavailable to new enrollees after 2020)."),
      ("Coverage for all outpatient prescription drugs", False, "Prescription drug coverage is not part of Medigap; it requires Medicare Part D."),
      ("Dental and vision benefits equivalent to Medicare Advantage", False, "Dental and vision are not Medigap benefits; they are supplemental benefits offered by some Medicare Advantage plans.")]),

    ("Which statement about Medigap Plan N is correct?",
     "multiple_choice", "standard",
     "Plan N covers most Medicare cost-sharing but requires copayments of up to $20 for some doctor office visits and up to $50 for emergency room visits that don't result in inpatient admission. It also does not cover Part B excess charges.",
     [("Plan N requires copayments for some office visits and does not cover Part B excess charges", True, "Correct. Plan N has cost-sharing through copayments and does not cover excess charges — this makes it less expensive than Plan G."),
      ("Plan N covers the Part B deductible and all excess charges with no copayments", False, "Plan N does not cover the Part B deductible and does not cover excess charges."),
      ("Plan N is only available to beneficiaries under age 70", False, "Medigap plans are generally available to all Medicare-eligible individuals; age 70 is not a cutoff."),
      ("Plan N covers prescription drugs as part of its supplemental benefits", False, "No Medigap plan covers prescription drugs.")]),

    ("A Medigap policy applicant who missed their open enrollment period applies at age 68. The insurer:",
     "multiple_choice", "standard",
     "Outside of the open enrollment period and guaranteed issue rights, insurers in most states can use medical underwriting to determine whether to accept or decline applicants and can charge higher premiums based on health status.",
     [("May use medical underwriting, potentially denying coverage or charging higher premiums", True, "Correct. Outside the open enrollment period and absent a guaranteed issue right, Medigap insurers can underwrite applicants."),
      ("Must accept the applicant at standard rates due to federal guaranteed issue protections", False, "Federal guaranteed issue protections apply only during the open enrollment period and specific qualifying events."),
      ("Must sell the applicant a Plan A at a minimum with no underwriting", False, "There is no federal requirement to guarantee any plan letter outside of open enrollment or qualifying events."),
      ("Cannot sell the applicant any Medigap policy after age 65 regardless of circumstances", False, "Medigap is available to applicants at any age; it is just that underwriting may apply outside the open enrollment period.")]),

    ("Medicare Part B 'excess charges' are:",
     "multiple_choice", "standard",
     "Medicare Part B excess charges occur when a provider does not accept Medicare assignment and charges more than the Medicare-approved amount. The excess can be up to 15% above the approved amount. Medigap plans F and G cover these excess charges.",
     [("The difference between what a non-assignment provider charges and Medicare's approved amount, up to 15%", True, "Correct. Excess charges are the additional amount non-participating providers can charge above Medicare's approved amount — up to 15%."),
      ("Charges for services Medicare considers medically unnecessary", False, "Medically unnecessary services are excluded from coverage entirely; that is different from excess charges."),
      ("Co-payments required for Medicare Part B outpatient services", False, "Part B coinsurance and copayments are different from excess charges."),
      ("Annual premium increases charged by Medicare for late Part B enrollment", False, "Late enrollment penalties are a different Medicare concept from excess charges.")]),

    ("Which of the following is NOT a standardized Medigap plan letter available to new Medicare enrollees?",
     "multiple_choice", "standard",
     "Following the MACRA Act, Plans C and F cannot be sold to new Medicare eligibles (those who became eligible on or after January 1, 2020). Plan E, H, I, and J were also previously discontinued. Plan G, N, and others remain available.",
     [("Plan F — it cannot be sold to new Medicare eligibles after January 1, 2020", True, "Correct. Plan F (which covered the Part B deductible) cannot be sold to individuals newly eligible for Medicare after January 1, 2020."),
      ("Plan G — it was replaced by a newer comprehensive plan", False, "Plan G remains available and is very popular for new Medicare enrollees."),
      ("Plan N — it was discontinued as part of Medicare reforms", False, "Plan N remains available to new Medicare enrollees."),
      ("Plan A — the basic plan was phased out as other plans expanded coverage", False, "Plan A remains available as the base minimum benefit Medigap plan.")]),

    ("A producer who sells Medigap to a Medicare beneficiary must provide:",
     "multiple_choice", "standard",
     "Federal law requires Medigap sellers to provide the applicant with a copy of the NAIC (National Association of Insurance Commissioners) Medigap shopper's guide and a comparison of available plans — this protects consumers in the purchase process.",
     [("A copy of the Medicare Supplement insurance shopper's guide before or at the time of sale", True, "Correct. Federal regulations require providing the Medicare Supplement insurance shopper's guide to help consumers compare plans."),
      ("Only the policy contract — no additional materials are federally required", False, "Federal regulations specifically require the shopper's guide for Medigap sales."),
      ("A full list of all Medicare Advantage plans available in the county", False, "Medigap producers are required to provide Medigap materials, not Medicare Advantage plan information."),
      ("Written approval from CMS before completing any Medigap sale", False, "CMS approval of individual Medigap sales is not required; producers must be licensed and provide required disclosures.")]),

    ("A Medicare beneficiary who enrolls in a Medigap policy must also be enrolled in:",
     "multiple_choice", "standard",
     "Medigap works as a supplement to Original Medicare (Part A and Part B). Enrollees must be covered by Medicare Part A and Part B for Medigap to function — Medigap pays secondary to Medicare's payment.",
     [("Medicare Part A and Part B (Original Medicare)", True, "Correct. Medigap supplements Original Medicare, so the beneficiary must have both Part A and Part B for the Medigap policy to coordinate benefits."),
      ("Medicare Part D for the Medigap policy to take effect", False, "Part D prescription coverage is separate and not required for Medigap enrollment."),
      ("A Medicare Advantage plan to receive full Medigap benefits", False, "Medigap CANNOT be used with Medicare Advantage. It works only with Original Medicare (Parts A and B)."),
      ("An employer-sponsored health plan as the primary payer", False, "Medigap does not require employer coverage; it is secondary to Original Medicare.")]),

    ("Which of the following individuals CANNOT be denied a Medigap policy in most states?",
     "multiple_choice", "standard",
     "During the 6-month Medigap open enrollment period (when a beneficiary is 65+ and newly enrolled in Part B), insurers cannot deny coverage or charge extra for pre-existing conditions. Outside this window, underwriting applies.",
     [("A 65-year-old newly enrolled in Medicare Part B within the last 6 months", True, "Correct. The open enrollment period guarantees issue rights — denial based on health status is prohibited."),
      ("A 72-year-old with end-stage renal disease who missed their open enrollment period", False, "End-stage renal disease and missing the open enrollment period may allow underwriting. ESRD has historically been an exclusion for Medigap."),
      ("A 68-year-old who voluntarily dropped a prior Medigap plan 3 years ago", False, "Voluntarily dropping prior coverage does not create a guaranteed issue right after the open enrollment period ends."),
      ("A 70-year-old applying for the first time who has always had employer group coverage", False, "Reaching a specific age alone does not guarantee issue rights outside of qualifying events and the open enrollment period.")]),

    ("The Medigap free look period allows a policyholder to return the policy within:",
     "multiple_choice", "standard",
     "Federal law requires Medigap policies to include a 30-day free look period. If the policyholder returns the policy within 30 days of receiving it, they receive a full premium refund.",
     [("30 days of receiving the policy for a full premium refund", True, "Correct. Medigap policies carry a 30-day free look period with full premium refund."),
      ("10 days of receiving the policy for a full premium refund", False, "The Medigap free look period is 30 days, not 10 days (though 10 days is the standard for many other insurance products)."),
      ("60 days of the policy effective date with no questions asked", False, "The free look period is 30 days, not 60 days."),
      ("Any time before the first claim is filed", False, "The free look right has a fixed time window (30 days); it does not extend until the first claim.")]),

    ("Medigap policies issued since 2010 include which standardized benefit in several plans?",
     "multiple_choice", "standard",
     "The 2010 Medigap standardization added preventive care benefits to some plans and adjusted the plan letters. Plans now also include a hospice care coinsurance benefit in all plans as a core minimum benefit.",
     [("Medicare Part A hospice coinsurance as a minimum benefit in all plans", True, "Correct. Since the 2010 standardization, all Medigap plans must include coverage for Medicare Part A hospice care coinsurance."),
      ("Coverage for prescription drugs in all plans regardless of Part D enrollment", False, "Medigap does not cover prescription drugs in any plan."),
      ("Routine dental care as part of the preventive care supplement", False, "Routine dental care is not a Medigap benefit."),
      ("A guaranteed no-premium-increase feature for the first 5 years", False, "No Medigap plan guarantees against premium increases.")]),

    ("When a Medicare beneficiary moves to a new state, their Medigap policy:",
     "multiple_choice", "standard",
     "Because Medigap plans are federally standardized, a Plan G in any state provides the same benefits as a Plan G in any other state. The policy follows the beneficiary when they move, and benefits do not change.",
     [("Remains valid and provides the same standardized benefits in the new state", True, "Correct. Medigap standardization means benefits are the same regardless of state. Moving does not invalidate the policy."),
      ("Automatically terminates upon relocation and must be reissued in the new state", False, "Medigap policies do not automatically terminate when a policyholder moves to a new state."),
      ("Changes its benefit structure to conform to the new state's regulations", False, "Federal standardization means Plan G in any state has identical benefits; benefits do not change upon relocation."),
      ("Must be updated within 30 days with the new state's insurance department", False, "Medigap policyholders are not required to re-register their policy with the new state's department.")]),

    ("A producer receives a request from a 63-year-old who wants to purchase a Medigap policy now to be ready when they turn 65. The producer should explain that:",
     "multiple_choice", "standard",
     "Medigap policies can only be sold to individuals who are enrolled in Medicare. Most people do not have Medicare until age 65 (or earlier due to disability). A 63-year-old without Medicare cannot purchase a Medigap policy.",
     [("Medigap is only available to Medicare beneficiaries — they cannot purchase it before Medicare enrollment", True, "Correct. Medigap supplements Medicare; it cannot be purchased without Medicare enrollment. The client should plan for enrollment at 65."),
      ("The client can purchase Medigap now and Medicare will be billed retroactively when they turn 65", False, "Medicare has no retroactive billing; Medigap requires active Medicare enrollment."),
      ("Any US resident over age 60 can purchase Medigap as supplemental coverage", False, "Medigap is specifically designed for Medicare beneficiaries; age 60 alone does not qualify."),
      ("The client can purchase Medigap now but benefits won't begin until Medicare enrollment", False, "Medigap cannot be sold to non-Medicare beneficiaries; the sale itself would be improper.")]),
]

# ── MODULE 4: RETIREMENT PLANS & SPECIAL LIFE CONCEPTS ───────────────────────

RETIREMENT_PLANS_QUESTIONS = [
    ("A Modified Endowment Contract (MEC) is created when a life insurance policy:",
     "multiple_choice", "standard",
     "A policy becomes a Modified Endowment Contract when it fails the 7-pay test — meaning the cumulative premiums paid in the first 7 years exceed the net level premium that would be required for a paid-up policy. Once a MEC, always a MEC.",
     [("Fails the 7-pay test by receiving more premium in 7 years than allowed by IRS limits", True, "Correct. The 7-pay test determines whether a policy is a MEC. Exceeding the cumulative 7-year limit triggers MEC status."),
      ("Has a cash value that exceeds the death benefit in any policy year", False, "Cash value exceeding death benefit triggers a different issue (policy termination/gain). MEC status is determined by the 7-pay test."),
      ("Is transferred to a new owner after the original insured dies", False, "Policy transfer at death does not create a MEC."),
      ("Has been in force for more than 20 years without a claim", False, "Policy longevity without a claim does not trigger MEC status.")]),

    ("The primary disadvantage of a Modified Endowment Contract (MEC) compared to a non-MEC life insurance policy is:",
     "multiple_choice", "standard",
     "Non-MEC life insurance allows tax-free access to cash value through loans and withdrawals up to basis. A MEC loses this tax advantage: pre-death withdrawals are taxed on an income-first basis (gains taxed first), and a 10% penalty applies before age 59½.",
     [("Withdrawals are taxed on a gain-first basis and subject to a 10% penalty before age 59½", True, "Correct. MEC withdrawals and loans are treated like annuity withdrawals: gains come out first and are taxed, and pre-59½ distributions face a 10% penalty."),
      ("The death benefit becomes taxable income to the beneficiary", False, "The death benefit of a MEC remains income-tax-free to beneficiaries — MEC status does not change this."),
      ("The policy cannot be used as collateral for a loan", False, "MEC policies can still be used as collateral; the tax treatment of distributions changes, not collateral use."),
      ("Premiums paid into a MEC are no longer deductible", False, "Life insurance premiums are generally not deductible regardless of MEC status.")]),

    ("In a traditional 401(k) plan, employee contributions are made with:",
     "multiple_choice", "standard",
     "Traditional 401(k) contributions are made on a pre-tax basis, reducing the employee's current taxable income. The contributions and their earnings grow tax-deferred and are taxed as ordinary income when withdrawn in retirement.",
     [("Pre-tax dollars, reducing taxable income now with taxes deferred until withdrawal", True, "Correct. Traditional 401(k) contributions reduce current taxable income. Taxes are paid on withdrawals in retirement."),
      ("After-tax dollars, with all withdrawals tax-free in retirement", False, "After-tax contributions for tax-free retirement withdrawals describe the Roth 401(k), not the traditional 401(k)."),
      ("After-tax dollars that also grow tax-deferred until retirement", False, "Traditional 401(k) uses pre-tax dollars; after-tax growth describes the non-deductible IRA."),
      ("Pre-tax dollars, with all growth tax-free and withdrawals never taxed", False, "Traditional 401(k) withdrawals are taxed as ordinary income. Tax-free withdrawals describe Roth accounts.")]),

    ("A Simplified Employee Pension (SEP-IRA) is particularly well-suited for:",
     "multiple_choice", "standard",
     "SEP-IRAs are simple, low-cost retirement plans ideal for self-employed individuals and small business owners. Contribution limits are much higher than a traditional IRA (up to 25% of compensation, capped at the IRS limit), and there is minimal administration.",
     [("Self-employed individuals and small business owners who want high contribution limits with minimal administration", True, "Correct. SEP-IRAs allow contributions up to 25% of compensation (or the IRS limit), with simple administration — ideal for the self-employed."),
      ("Large corporations with complex benefit structures", False, "SEP-IRAs are designed for simplicity; large corporations typically use 401(k) or defined benefit plans."),
      ("Employees who want to make their own contributions directly into the plan", False, "SEP-IRA contributions are made only by the employer; employees cannot contribute to their own SEP-IRA."),
      ("Government employees who are covered by a defined benefit pension", False, "Government employees typically have access to 457(b) plans; SEP-IRAs are for private sector self-employed and small businesses.")]),

    ("A SIMPLE IRA differs from a SEP-IRA primarily in that a SIMPLE IRA:",
     "multiple_choice", "standard",
     "A SIMPLE (Savings Incentive Match Plan for Employees) IRA allows both employer AND employee contributions. SEP-IRAs only allow employer contributions. SIMPLE IRAs are available to employers with 100 or fewer employees.",
     [("Allows both employer and employee contributions; SEP-IRAs are employer-contribution only", True, "Correct. The SIMPLE IRA allows employee salary deferrals plus employer matching contributions, while SEP-IRAs allow only employer contributions."),
      ("Has higher contribution limits than a SEP-IRA", False, "SEP-IRA limits (25% of compensation) are significantly higher than SIMPLE IRA limits, making SEP more attractive for high earners."),
      ("Is available only to nonprofit organizations", False, "SIMPLE IRAs are available to any small employer with 100 or fewer employees, not just nonprofits."),
      ("Does not allow employer matching contributions", False, "Employer matching or non-elective contributions are a required feature of the SIMPLE IRA.")]),

    ("A life settlement differs from a viatical settlement in that a life settlement involves:",
     "multiple_choice", "standard",
     "Viatical settlements involve terminally ill policyholders (typically with life expectancy under 2 years). Life settlements involve policyholders who are not terminally ill — they sell their policies for financial reasons such as no longer needing coverage or needing liquidity.",
     [("A policyholder who is not terminally ill selling their policy for liquidity or other reasons", True, "Correct. Life settlements are for policyholders who are not terminally ill. Viatical settlements are specifically for terminally or chronically ill individuals."),
      ("A terminally ill policyholder selling their policy for immediate cash", False, "Terminally ill policyholders use viatical settlements, not life settlements."),
      ("The insurer buying back the policy at its original face value", False, "The insurer is not the buyer in a life settlement; third-party investors purchase the policy."),
      ("A transfer of the policy as a charitable donation with no cash received", False, "A charitable gift of a policy is a donation, not a life settlement. Life settlements involve cash consideration.")]),

    ("Key person life insurance is purchased to protect a business against:",
     "multiple_choice", "standard",
     "Key person life insurance indemnifies the business for the financial loss resulting from the death of a key employee whose skills, relationships, or knowledge are critical to the business. The business is both the owner and beneficiary.",
     [("The financial loss resulting from the death of a critical employee whose skills are essential to the business", True, "Correct. Key person insurance reimburses the business for lost profits, recruitment and training costs, and other losses caused by the key person's death."),
      ("The key person's personal estate taxes and financial obligations", False, "Key person insurance protects the business, not the individual's personal estate."),
      ("Customer lawsuits arising from the key person's professional negligence", False, "Professional liability/E&O insurance covers negligence claims; key person insurance covers death-related financial loss."),
      ("Losses from natural disasters that disrupt business operations", False, "Business interruption insurance covers natural disaster losses; key person insurance specifically addresses the death of a key individual.")]),

    ("In a buy-sell agreement funded by life insurance, the purpose of the life insurance policy is to:",
     "multiple_choice", "standard",
     "A buy-sell agreement obligates surviving owners or the entity to purchase a deceased owner's interest. Life insurance provides the cash needed to complete the purchase — it funds the buyout so the survivor(s) can pay the deceased owner's estate for the business interest.",
     [("Provide the cash needed for the surviving owners or entity to buy out the deceased owner's interest", True, "Correct. Life insurance funds the buy-sell agreement — the death benefit provides the purchase price to buy the deceased owner's share from their estate."),
      ("Provide income replacement for the deceased owner's family after the business is sold", False, "Buy-sell insurance funds the business purchase; personal income replacement is a separate need addressed by personal life insurance."),
      ("Insure the business assets against fire, theft, and other property losses", False, "Business property insurance covers assets; key person and buy-sell life insurance covers ownership transition."),
      ("Reimburse the business for revenue lost during ownership transition", False, "Business interruption insurance covers revenue loss; buy-sell insurance funds the ownership transfer.")]),

    ("Required Minimum Distributions (RMDs) from traditional IRAs and 401(k)s must begin by:",
     "multiple_choice", "standard",
     "Under the SECURE 2.0 Act, the RMD starting age was increased to age 73 for individuals who turn 72 after December 31, 2022, and will increase to age 75 in 2033. Roth IRAs do not have RMDs during the owner's lifetime.",
     [("Age 73 for individuals subject to current IRS rules (age 75 starting in 2033)", True, "Correct. SECURE 2.0 raised the RMD age to 73 (and eventually 75 in 2033). Knowing the current RMD age is important for exam purposes."),
      ("Age 59½ — the same age as the penalty-free withdrawal age", False, "Age 59½ is when penalties for early withdrawals end, not when RMDs begin."),
      ("Age 65 — when Medicare eligibility begins", False, "Medicare eligibility age and RMD age are different. RMDs currently begin at 73."),
      ("Age 62 — the earliest Social Security eligibility age", False, "Social Security early eligibility and RMD age are different concepts.")]),

    ("A 'split-dollar life insurance' arrangement typically involves:",
     "multiple_choice", "standard",
     "Split-dollar life insurance is a cost-sharing arrangement between two parties — typically an employer and employee — where they split the premium costs and the policy benefits (death benefit and/or cash value) according to a negotiated agreement.",
     [("An employer and employee sharing the cost and benefits of a life insurance policy", True, "Correct. Split-dollar arrangements split both the premium costs and the policy benefits between the two parties, typically an employer and a key employee."),
      ("A life insurance policy with two equal beneficiaries who each receive 50% of the death benefit", False, "Multiple beneficiaries receiving equal shares is a beneficiary designation, not a split-dollar arrangement."),
      ("A policy that splits premiums between two separate insurance companies", False, "Split-dollar is an arrangement between the insured and another party, not between two insurers."),
      ("A term insurance policy that is renewed every year for half the original premium", False, "Annual renewable term and split-dollar are separate concepts.")]),

    ("In a cross-purchase buy-sell agreement with 4 business partners, each partner must own:",
     "multiple_choice", "standard",
     "In a cross-purchase buy-sell, each partner buys and owns a policy on each other partner. With 4 partners, each owns 3 policies (one on each other partner), for a total of 12 policies. This can be administratively cumbersome compared to an entity-purchase plan.",
     [("3 policies — one on each of the other partners, for a total of 12 policies among all partners", True, "Correct. Cross-purchase: each of 4 partners owns 3 policies = 12 total. This is why entity-purchase plans are often preferred for more than 2-3 owners."),
      ("1 policy on all other partners combined, for a total of 4 policies", False, "Each partner needs a separate policy on each other partner in a cross-purchase arrangement."),
      ("4 policies — one on each partner including themselves", False, "You cannot own a life insurance policy on yourself for buy-sell purposes; cross-purchase means each partner insures the others."),
      ("6 policies total — one policy per partner pair", False, "Six policies would be correct only if the policies were joint first-to-die; standard cross-purchase requires n × (n-1) policies.")]),

    ("A Roth IRA differs from a traditional IRA in that Roth IRA contributions are:",
     "multiple_choice", "standard",
     "Roth IRA contributions are made with after-tax dollars — no deduction — but qualified distributions in retirement are completely tax-free. Traditional IRA contributions may be deductible and are taxed on withdrawal.",
     [("Made with after-tax dollars, with qualified withdrawals completely tax-free in retirement", True, "Correct. Roth = after-tax contributions, tax-free qualified distributions. Traditional = pre-tax deductible contributions, taxable distributions."),
      ("Pre-tax, with taxes deferred until retirement withdrawals", False, "Pre-tax contributions with deferred taxes describe the traditional IRA, not Roth."),
      ("Limited to employer matching contributions only", False, "Roth IRA contributions are individual contributions; employer matching applies to employer-sponsored plans."),
      ("Exempt from annual IRS contribution limits", False, "Roth IRAs have the same annual contribution limits as traditional IRAs, set by the IRS.")]),

    ("A viatical settlement is tax-free to the viator (the terminally ill policyholder) when:",
     "multiple_choice", "standard",
     "Viatical settlement proceeds paid to a terminally ill or chronically ill individual are generally income-tax-free under the Health Insurance Portability and Accountability Act (HIPAA). The proceeds are treated like accelerated death benefits.",
     [("The viator is terminally ill (life expectancy of 24 months or less) or chronically ill", True, "Correct. HIPAA provides income-tax-free treatment for viatical settlement proceeds received by terminally or chronically ill individuals."),
      ("The proceeds are invested in a tax-qualified retirement account within 60 days", False, "There is no rollover rule for viatical proceeds; the tax-free treatment applies directly to qualifying individuals."),
      ("The policy has been in force for more than 10 years before the settlement", False, "Policy duration does not determine the tax treatment of viatical proceeds."),
      ("The settlement is completed through a licensed viatical settlement broker", False, "Tax treatment depends on the viator's health status, not whether a licensed broker facilitated the transaction.")]),

    ("Business overhead expense (BOE) disability insurance is designed to:",
     "multiple_choice", "standard",
     "BOE disability insurance covers the ongoing fixed overhead expenses of a business owner's practice or business when they are disabled — rent, employee salaries, utilities, equipment leases, etc. It does not replace the owner's personal income.",
     [("Pay the business owner's fixed overhead expenses when the owner is disabled", True, "Correct. BOE disability covers fixed business expenses (rent, staff, utilities) when the owner is too disabled to work — not personal income replacement."),
      ("Replace the business owner's personal income during disability", False, "Personal income replacement is provided by individual disability income insurance, not BOE insurance."),
      ("Pay the business owner's personal medical bills during disability", False, "Medical expenses are covered by health insurance; BOE covers business operating expenses."),
      ("Fund a disability buy-sell agreement between business partners", False, "Disability buy-sell coverage is a separate product; BOE covers ongoing business expenses.")]),

    ("Section 1035 exchanges allow a policyholder to:",
     "multiple_choice", "standard",
     "A 1035 exchange allows tax-free replacement of one insurance or annuity contract for another without triggering income tax on any accumulated gain — as long as the exchange meets IRS requirements.",
     [("Exchange one life insurance policy or annuity for another without current income tax on the gain", True, "Correct. IRC Section 1035 allows tax-free exchanges between like insurance contracts — the gain is preserved in the new contract but not currently taxed."),
      ("Withdraw cash value from a life insurance policy without any income tax", False, "1035 exchanges involve contract replacement, not cash withdrawals. Withdrawals above basis are taxable."),
      ("Convert a traditional IRA to a Roth IRA without tax consequences", False, "IRA conversions are governed by different IRS rules; 1035 exchanges apply to insurance contracts and annuities."),
      ("Transfer life insurance ownership to a family member tax-free at death", False, "1035 exchanges are for contract replacements during life; estate planning transfers at death use different mechanisms.")]),

    ("In a defined benefit pension plan, the retirement benefit is determined by:",
     "multiple_choice", "standard",
     "Defined benefit plans guarantee a specific monthly benefit at retirement, typically based on a formula using years of service and average final salary. The employer bears the investment risk and is responsible for funding the promised benefit.",
     [("A formula based on years of service and average salary — the employer bears the investment risk", True, "Correct. Defined benefit plans guarantee a formula-based retirement income. The employer funds the plan and bears investment risk."),
      ("The account balance at retirement, which depends on contributions and investment returns", False, "Account balance at retirement describes a defined contribution plan (like a 401k), not a defined benefit plan."),
      ("The employee's choice of investment options within the plan", False, "Employees do not choose investments in a defined benefit plan; the employer manages the pension fund."),
      ("The amount the employee contributed over their career", False, "Defined benefit plans are not based on employee contribution amounts; they are based on a formula.")]),

    ("A 'graded premium' whole life policy offers:",
     "multiple_choice", "standard",
     "Graded premium whole life starts with lower premiums in the early policy years that increase over time before leveling off at a fixed amount. This allows younger or lower-income buyers to start coverage with lower initial premiums.",
     [("Lower premiums in early years that increase over time before leveling off permanently", True, "Correct. Graded premium whole life starts low and increases, making early years more affordable. Eventually premiums level off."),
      ("Level premiums that remain the same for the life of the policy", False, "Level premiums describe standard whole life; graded premium starts low and increases."),
      ("Premiums that decrease as the policyholder ages and the cash value grows", False, "Premiums that decrease with age describe a policy with a reducing term rider, not standard graded premium whole life."),
      ("A single lump-sum premium paid at policy inception with no further payments", False, "A single lump-sum describes a single-premium policy; graded premium involves a series of increasing payments.")]),

    ("The 'transfer for value' rule can cause a life insurance death benefit to become taxable. This rule is triggered when:",
     "multiple_choice", "standard",
     "The transfer for value rule states that if a life insurance policy is transferred for valuable consideration (sold, not gifted), the death benefit in excess of the consideration paid may become taxable income to the new owner. Certain exceptions apply.",
     [("A life insurance policy is sold (transferred for valuable consideration) to a new owner", True, "Correct. Transferring a life insurance policy for cash or other valuable consideration triggers the transfer for value rule, potentially making the death benefit taxable."),
      ("The insured names a trust as beneficiary of the life insurance policy", False, "Naming a trust as beneficiary does not trigger the transfer for value rule."),
      ("The policy owner borrows against the cash value of the policy", False, "Policy loans do not constitute a transfer of ownership and do not trigger the transfer for value rule."),
      ("The policy lapses and is reinstated within the allowed reinstatement period", False, "Reinstatement of a lapsed policy does not trigger the transfer for value rule.")]),

    ("The 'corridor' requirement in a universal life policy ensures that:",
     "multiple_choice", "standard",
     "The IRS requires that life insurance policies maintain a minimum amount of pure insurance protection (the corridor) relative to the cash value. If the cash value grows too large relative to the death benefit, the policy must increase the death benefit to maintain the tax-favored insurance status.",
     [("The death benefit remains sufficiently larger than the cash value to qualify as life insurance", True, "Correct. The corridor test (or net single premium/guideline premium test) requires that the death benefit exceed the cash value by a specified percentage to maintain insurance contract tax status."),
      ("The premium remains the same even when the policy's cost of insurance increases", False, "The corridor refers to the death benefit-to-cash-value ratio, not premium stability."),
      ("The cash value always equals at least 10% of the death benefit", False, "The corridor requires the death benefit to exceed cash value, not the other way around."),
      ("The policy's investment returns are guaranteed at a minimum rate", False, "Guaranteed minimum interest rates are a feature of the policy, not the corridor requirement.")]),

    ("403(b) plans are retirement savings plans available to employees of:",
     "multiple_choice", "standard",
     "403(b) plans (also called tax-sheltered annuities or TSAs) are employer-sponsored retirement plans available to employees of public schools, non-profit organizations qualifying under IRC 501(c)(3), and certain ministers.",
     [("Public schools, tax-exempt non-profit organizations (501(c)(3)), and certain ministers", True, "Correct. 403(b) plans are the nonprofit and education sector equivalent of the for-profit 401(k) plan."),
      ("Any employer with more than 500 employees regardless of tax status", False, "403(b) eligibility is based on employer type (education/nonprofit), not size."),
      ("Only federal government employees and military personnel", False, "Federal employees use the Thrift Savings Plan (TSP); 403(b) is for nonprofit and education sector employees."),
      ("Only self-employed individuals with no employees", False, "Self-employed individuals use SEP-IRAs, SIMPLE IRAs, or Solo 401(k)s; 403(b) is for non-profit/education employees.")]),

    ("An insurable interest requirement for a key person life insurance policy means:",
     "multiple_choice", "standard",
     "The business must have an insurable interest in the key person — meaning the business stands to suffer a measurable financial loss from the key person's death. Fortunately, a business always has insurable interest in its key employees.",
     [("The business must stand to suffer financial loss from the key person's death", True, "Correct. Insurable interest for key person insurance requires a financial stake in the continued life of the insured. Businesses have insurable interest in employees whose death would cause financial harm."),
      ("The key employee must own at least 25% of the business to qualify for coverage", False, "Ownership percentage is not the insurable interest standard; financial dependence on the person's continued work is."),
      ("The policy cannot be issued if the key person is related to the business owner", False, "Family relationships do not eliminate insurable interest; what matters is financial dependency."),
      ("The IRS must pre-approve the amount of key person insurance the business carries", False, "IRS approval is not required for key person life insurance; the amount is a business decision based on estimated financial exposure.")]),
]

# ── MODULE 5: CYBER LIABILITY INSURANCE ──────────────────────────────────────

CYBER_LIABILITY_QUESTIONS = [
    ("First-party cyber liability coverage pays for:",
     "multiple_choice", "standard",
     "First-party cyber coverage pays for the policyholder's own losses from a cyber event, including data breach response costs, business interruption, ransomware payments, and crisis management — losses that directly impact the insured's own business.",
     [("The policyholder's own losses from a cyber event, such as breach response costs and ransomware payments", True, "Correct. First-party coverage pays for the insured's own direct losses — data breach notification, credit monitoring, business interruption, ransomware, etc."),
      ("Lawsuits filed by third parties whose data was compromised in a breach", False, "Third-party lawsuits are covered by third-party (liability) cyber coverage, not first-party coverage."),
      ("Regulatory fines for HIPAA violations by the policyholder's employees", False, "Regulatory fines may be covered by specific cyber liability endorsements; this is typically a third-party coverage element."),
      ("Other businesses' losses caused by a cyber attack on the policyholder's network", False, "Losses to other parties from your network breach would be third-party liability coverage.")]),

    ("Third-party cyber liability coverage pays for:",
     "multiple_choice", "standard",
     "Third-party cyber coverage protects the insured when a cyber event causes harm to customers, vendors, or other third parties, who then sue the insured. This includes data breach lawsuits, privacy violation claims, and network security failure claims.",
     [("Lawsuits and claims brought by customers or others whose data was compromised", True, "Correct. Third-party cyber coverage protects the insured from claims and lawsuits filed by those harmed by the insured's cyber security failure."),
      ("The cost of restoring the policyholder's own systems and data after an attack", False, "System restoration costs are first-party coverage; third-party covers claims by others."),
      ("The ransom payment required to restore access to encrypted systems", False, "Ransomware payments are a first-party coverage element."),
      ("The policyholder's own lost revenue during a network outage", False, "Business interruption/lost revenue is first-party coverage; third-party covers harm to others.")]),

    ("A ransomware attack that encrypts a company's files and demands payment would be covered by which type of cyber coverage?",
     "multiple_choice", "standard",
     "Ransomware is a first-party cyber coverage event — the insured's own systems are attacked, and the ransom payment and recovery costs are the insured's own losses. Some cyber policies have specific ransomware sublimits.",
     [("First-party cyber coverage, including ransomware payment and system restoration costs", True, "Correct. Ransomware is a first-party loss — the insured's own business is attacked and the ransom/recovery costs are direct losses to the policyholder."),
      ("Third-party cyber liability, as the hackers are a third party causing the loss", False, "The hackers are not the 'third party' in cyber insurance terminology. Third-party coverage is for claims by customers/vendors, not the attackers."),
      ("Commercial general liability — ransomware is a property damage claim", False, "Standard CGL policies typically exclude cyber events; ransomware is a cyber-specific coverage."),
      ("Workers' compensation — employees whose data is compromised can file claims", False, "Workers' compensation covers work-related injuries and illnesses; it does not cover cyber events.")]),

    ("A data breach involving personally identifiable information (PII) typically triggers costs that include:",
     "multiple_choice", "standard",
     "Data breach response costs typically include mandatory notifications to affected individuals, credit monitoring services, forensic investigation, public relations/crisis management, and potentially regulatory fines and legal defense.",
     [("Notification to affected individuals, credit monitoring, forensic investigation, and PR/crisis management", True, "Correct. All of these are standard data breach response costs that cyber insurance (first-party) is designed to cover."),
      ("Only the cost of mailing notification letters — other costs are excluded", False, "Modern cyber policies cover a broad range of breach response costs, not just notifications."),
      ("Replacement of all hardware equipment affected by the breach", False, "Hardware replacement may be covered for damage caused by a cyber event, but the listed costs are the primary breach response expenses."),
      ("Full settlement of all future lawsuits before they are filed", False, "Cyber coverage pays for covered claims as they arise; it does not pre-fund future settlements.")]),

    ("Business interruption coverage under a cyber policy pays for:",
     "multiple_choice", "standard",
     "Cyber business interruption coverage pays for lost income and extra expenses when a cyber event causes the insured's business to shut down or operate at reduced capacity. This is analogous to business interruption in a property policy but triggered by cyber events.",
     [("Lost revenue and extra expenses when a cyber attack disrupts business operations", True, "Correct. Cyber BI coverage pays for income lost and extra expenses incurred when a cyber event disrupts normal business operations."),
      ("The salaries of all employees during the system outage regardless of whether they work", False, "Payroll continuation may be part of BI, but the coverage is for lost income and extra expenses, not all payroll costs regardless of impact."),
      ("Any revenue the business might have earned if the cyber event hadn't occurred that year", False, "BI coverage is tied to the actual period of interruption from the specific covered event, not speculative future revenue."),
      ("The cost of hiring a new IT staff member to prevent future cyber events", False, "Future prevention costs are not covered by business interruption; BI covers losses from the current event.")]),

    ("Social engineering fraud in the cyber insurance context refers to:",
     "multiple_choice", "standard",
     "Social engineering attacks manipulate employees into taking actions that cause financial loss — such as transferring funds to a fraudulent account because an employee was tricked by a fake email from the 'CEO' (business email compromise/BEC).",
     [("Manipulating employees into transferring funds or revealing sensitive information through deception", True, "Correct. Social engineering fraud (including business email compromise) involves tricking employees rather than hacking systems — a significant and growing cause of cyber losses."),
      ("Installing malicious software on a company's computer systems", False, "Malware installation is a technical attack, not social engineering. Social engineering manipulates people, not systems."),
      ("Accessing systems through a technical vulnerability in software", False, "Technical vulnerability exploitation is hacking; social engineering manipulates people through deception."),
      ("Stealing physical computers or storage media from an office", False, "Physical theft is a property crime; social engineering is psychological manipulation causing financial transfer or data disclosure.")]),

    ("Cyber liability insurance typically EXCLUDES coverage for:",
     "multiple_choice", "standard",
     "Common cyber insurance exclusions include acts of war/nation-state attacks, pre-existing known vulnerabilities, bodily injury and property damage (covered by CGL), infrastructure failure, intentional acts by the insured, and sometimes future revenue loss beyond the restoration period.",
     [("Intentional acts by the insured and known pre-existing vulnerabilities not remediated", True, "Correct. Intentional acts and known unaddressed vulnerabilities are standard cyber policy exclusions."),
      ("All claims arising from employee negligence", False, "Employee negligence (phishing clicks, misconfigured systems) is typically covered; intentional acts by employees may be excluded."),
      ("Third-party claims from customers whose data was compromised", False, "Third-party claims from affected customers are a core covered cyber liability risk."),
      ("Business interruption lasting less than 8 hours", False, "While some policies have waiting periods, short-duration outages being excluded from all cyber policies is not a universal standard exclusion.")]),

    ("PCI DSS compliance failures exposed by a data breach can result in what type of covered cyber loss?",
     "multiple_choice", "standard",
     "When a merchant or service provider fails to comply with PCI DSS (Payment Card Industry Data Security Standard) and suffers a breach, they can face fines and assessments from payment card brands (Visa, Mastercard). Some cyber policies cover these PCI fines and penalties.",
     [("PCI fines and assessment penalties from payment card brands", True, "Correct. Cyber insurance can cover PCI DSS fines and assessments levied by payment card brands following a breach — a significant exposure for businesses handling card payments."),
      ("The cost of upgrading to PCI-compliant systems to prevent future breaches", False, "Proactive security improvements are not covered losses; they are preventive expenses."),
      ("Criminal fines imposed by the federal government for PCI non-compliance", False, "PCI is not a federal law; violations result in card brand fines, not federal criminal penalties."),
      ("Free credit monitoring for all US cardholders whose data was exposed", False, "Credit monitoring for affected cardholders would be a breach response cost — a different coverage element from PCI fines.")]),

    ("A company's cyber policy includes a '$10,000 retention.' This means:",
     "multiple_choice", "standard",
     "A retention in cyber insurance is equivalent to a deductible — the amount the insured pays out of pocket before insurance coverage kicks in.",
     [("The insured pays the first $10,000 of each covered cyber loss before insurance pays", True, "Correct. A retention is the cyber insurance equivalent of a deductible — the insured retains the first $10,000 of each loss."),
      ("The insurer retains $10,000 from each payment as an administrative fee", False, "The retention is the insured's out-of-pocket obligation, not an insurer fee."),
      ("Coverage is limited to $10,000 per occurrence regardless of actual loss", False, "$10,000 as a limit would cap coverage; a retention is the amount the insured pays before coverage begins."),
      ("The policy only covers losses exceeding $10,000 per month in aggregate", False, "Monthly aggregate retentions are unusual; a standard retention applies per occurrence.")]),

    ("Network security liability coverage responds when:",
     "multiple_choice", "standard",
     "Network security liability covers the insured's legal liability when their network security failure causes harm to third parties — including allowing malware to spread to others, failing to protect third-party data, or enabling a denial-of-service attack against others.",
     [("The insured's network security failure causes harm to third parties, such as spreading malware", True, "Correct. Network security liability responds to third-party claims resulting from the insured's failure to maintain adequate network security."),
      ("The insured's own network is attacked from an external source", False, "External attacks on the insured's own systems are first-party coverage; network security liability is about harm to third parties."),
      ("The insured purchases a new server and it fails within the warranty period", False, "Hardware warranty failures are equipment coverage matters, not network security liability."),
      ("An employee accidentally deletes important company files", False, "Accidental data deletion is a first-party coverage matter; network security liability covers harm to third parties from security failures.")]),

    ("Media liability coverage in a cyber policy covers:",
     "multiple_choice", "standard",
     "Media liability covers the insured for claims arising from digital content they publish online — copyright infringement, defamation, invasion of privacy, and similar intellectual property and content-related claims.",
     [("Copyright infringement, defamation, and privacy violations arising from the insured's online content", True, "Correct. Media liability covers claims related to content the insured publishes online — copyright, defamation, privacy violations in digital media."),
      ("Physical damage to media equipment like cameras and broadcasting hardware", False, "Physical equipment damage is property insurance; media liability covers legal claims from content."),
      ("Business interruption losses from a cyberattack on a media company", False, "Business interruption is a separate first-party coverage; media liability covers content-related legal claims."),
      ("Claims from employees who view inappropriate content on company devices", False, "Employee-related claims are HR/employment practices matters; media liability covers third-party content claims.")]),

    ("Which type of business is generally most exposed to cyber liability risk?",
     "multiple_choice", "standard",
     "Businesses that collect, store, and process large amounts of sensitive personal data (healthcare providers, retailers, financial institutions) face the greatest cyber liability exposure due to the volume of PII and the regulatory environment.",
     [("Healthcare providers and retailers who store large amounts of patient or customer personal data", True, "Correct. Businesses with large stores of sensitive PII — healthcare, retail, financial services — face the greatest cyber liability exposure."),
      ("Companies that only do business in person with no online presence", False, "Even companies without a web presence can face cyber risks through point-of-sale systems and employee devices."),
      ("Small businesses with fewer than 10 employees who use only paper records", False, "While paper-only businesses have lower cyber exposure, even small businesses face cyber risk if they use any digital systems."),
      ("Businesses located in rural areas away from major technology hubs", False, "Geographic location does not determine cyber liability exposure; the type of data handled is the primary factor.")]),

    ("An insured company is sued by customers after a hacker stole credit card information from the insured's database. This is a:",
     "multiple_choice", "standard",
     "Customer lawsuits arising from data stolen from the insured's systems are third-party cyber liability claims — the insured is being held legally responsible for harm caused to third parties by their security failure.",
     [("Third-party cyber liability claim covered by cyber liability insurance", True, "Correct. Customer lawsuits arising from stolen data are third-party liability claims — the insured's security failure caused harm to others."),
      ("First-party cyber claim because the insured's systems were attacked", False, "The attack on the insured's systems creates a first-party loss for the insured's own costs; the customer lawsuits are separate third-party claims."),
      ("Covered under the insured's commercial general liability policy", False, "Standard CGL policies typically exclude cyber events and data-related claims; cyber policies are designed to cover these."),
      ("Not covered — customer lawsuits from data breaches are universally excluded from all cyber policies", False, "Third-party data breach liability is a core covered risk in cyber insurance policies.")]),

    ("Cyber extortion coverage is triggered by:",
     "multiple_choice", "standard",
     "Cyber extortion coverage responds when a hacker threatens to disclose confidential data, destroy systems, or continue a denial-of-service attack unless the insured pays a ransom. The coverage pays both the ransom payment (if paid) and the costs of responding to the threat.",
     [("A threat to cause harm to the insured's systems or data unless a ransom is paid", True, "Correct. Cyber extortion coverage responds to demands for ransom payment under threat of cyber harm."),
      ("A customer threatening a lawsuit unless the insured pays to settle", False, "Customer threats of lawsuits are general liability matters; cyber extortion is specific to cyber-related ransom demands."),
      ("An employee threatening to leak confidential information unless given a raise", False, "Employee-related threats are employment practices and crime coverage matters, not cyber extortion."),
      ("A vendor threatening to terminate a contract unless terms are renegotiated", False, "Contract disputes are not cyber extortion events.")]),

    ("Systems failure coverage under a cyber policy is broader than traditional cyber coverage because it covers:",
     "multiple_choice", "standard",
     "Systems failure coverage extends cyber coverage to include non-malicious system failures — such as a software update causing a system crash or hardware failure causing data loss — not just cyber attacks.",
     [("Business interruption from non-malicious technical failures like software bugs or hardware crashes", True, "Correct. Systems failure coverage extends beyond cyber attacks to cover accidental/non-malicious technical failures that cause business interruption."),
      ("Only malicious hacking attacks that result in data theft", False, "Coverage limited to malicious attacks is standard cyber coverage; systems failure is broader."),
      ("Physical damage to servers from fire or water — standard property coverage", False, "Fire and water damage is covered by property insurance; systems failure covers electronic/software failures."),
      ("Employee theft of company hardware for personal use", False, "Employee theft is a crime coverage matter; systems failure covers technical failures not caused by theft.")]),

    ("When determining adequate cyber insurance limits for a client, a producer should consider:",
     "multiple_choice", "standard",
     "Adequate cyber limits should reflect the client's actual exposure: the volume and type of data held, regulatory environment, potential breach response costs, third-party liability exposure, and business interruption exposure.",
     [("The type and volume of sensitive data held, regulatory environment, and potential breach response costs", True, "Correct. Proper cyber limit analysis requires assessing data exposure, regulatory requirements, and the full scope of potential loss scenarios."),
      ("Only the client's annual revenue — cyber limits should equal 10% of revenue", False, "Revenue is one factor but not the sole determinant; data exposure and regulatory environment are equally important."),
      ("The cost of the client's current IT security software and hardware", False, "IT security investment affects risk quality but not the calculation of adequate insurance limits."),
      ("Only previous cyber claims history — no other factors are relevant", False, "Claims history is relevant but insufficient alone; cyber exposure analysis requires a comprehensive assessment of current risk factors.")]),

    ("A denial-of-service (DoS) attack that takes down a company's e-commerce website for 3 days would primarily trigger:",
     "multiple_choice", "standard",
     "A DoS attack is a cyber event that causes business interruption. The primary covered loss is the business interruption coverage for lost revenue and extra expenses during the 3-day outage.",
     [("First-party cyber business interruption coverage for lost revenue and extra expenses", True, "Correct. A DoS attack disrupting e-commerce operations causes business interruption — a first-party coverage trigger."),
      ("Third-party cyber liability coverage because the attack came from outside", False, "The source being external does not make it third-party coverage. Third-party coverage responds to claims by others; the DoS business interruption is the insured's own loss."),
      ("Product liability coverage for orders that couldn't be fulfilled during the outage", False, "Product liability covers injury/damage from products; business interruption coverage addresses the revenue loss from the system outage."),
      ("Commercial property coverage because the website was unavailable", False, "Websites are not physical property; DoS business interruption is a cyber coverage matter.")]),

    ("Cyber insurance typically requires insureds to maintain which of the following as a condition of coverage?",
     "multiple_choice", "standard",
     "Cyber insurers increasingly require minimum security controls as a condition of coverage — including multi-factor authentication, regular patching and updates, employee security training, and incident response planning.",
     [("Basic security controls such as multi-factor authentication and regular system patching", True, "Correct. Maintaining minimum security hygiene is increasingly required by cyber insurers as a condition of coverage."),
      ("Purchase of the most expensive available endpoint security software", False, "Insurers require adequate controls, not necessarily the most expensive software on the market."),
      ("Hiring a full-time cybersecurity professional on staff", False, "While strong security staffing is beneficial, hiring a full-time professional is not universally required by all cyber insurers."),
      ("Annual cyber liability training for all employees — failure voids coverage entirely", False, "Training is encouraged and some policies reward it with better terms, but failure to train does not universally void all cyber coverage.")]),

    ("A company's cyber policy has a $1 million limit with a $10,000 retention. A covered breach costs $800,000. The insurer pays:",
     "multiple_choice", "standard",
     "The insured pays the retention ($10,000) first, then the insurer pays the remainder up to the policy limit. $800,000 - $10,000 = $790,000 paid by the insurer.",
     [("$790,000 — the loss minus the $10,000 retention, within the $1 million limit", True, "Correct. Loss ($800,000) minus retention ($10,000) = $790,000 insurer payment. This is within the $1 million policy limit."),
      ("$800,000 — the insurer pays the full loss because it is within the limit", False, "The $10,000 retention is the insured's responsibility; the insurer pays $790,000, not $800,000."),
      ("$1,000,000 — the full policy limit regardless of actual loss", False, "Insurance pays actual covered losses minus the retention, not automatically the full limit."),
      ("$0 — the retention must be paid by the insured and then the insurer reimburses everything", False, "The insurer does not reimburse the retention; the insured pays the retention and the insurer pays the remainder.")]),

    ("Regulatory defense and penalties coverage under a cyber policy responds when:",
     "multiple_choice", "standard",
     "Following a data breach, regulatory agencies (FTC, state attorneys general, HHS/OCR for HIPAA) may investigate and impose fines and penalties. This cyber coverage element pays for defense costs and covered fines/penalties from such regulatory actions.",
     [("A government regulator investigates the insured following a data breach and imposes fines", True, "Correct. Regulatory defense and penalties coverage responds to government investigations and fines arising from a covered cyber event."),
      ("The insured voluntarily self-reports a data breach to regulators for a discount", False, "Self-reporting to earn a discount is a regulatory strategy; coverage responds to investigations and penalties, not the act of reporting."),
      ("An employee is personally fined for failing to follow the company's data security policies", False, "Personal employee fines are not covered by the company's cyber policy; coverage is for the company's own regulatory exposure."),
      ("The insured fails to purchase the most current version of their security software", False, "Failure to update software may affect coverage eligibility but is not itself a regulatory penalty coverage trigger.")]),
]

# ── MODULE 6: BUSINESS DISABILITY INCOME ─────────────────────────────────────

BUSINESS_DI_QUESTIONS = [
    ("Business Overhead Expense (BOE) disability insurance is designed to pay:",
     "multiple_choice", "standard",
     "BOE disability insurance covers the fixed overhead expenses of the insured's business during the owner's disability. It does NOT replace the owner's personal income — that's individual DI. BOE pays rent, utilities, employee salaries, and other fixed operating costs.",
     [("Fixed business overhead expenses (rent, employee salaries, utilities) when the owner is disabled", True, "Correct. BOE covers the business's ongoing fixed expenses so the owner can keep the business running during their disability."),
      ("The business owner's personal income replacement during disability", False, "Personal income replacement is the function of individual disability income insurance, not BOE."),
      ("The business owner's personal medical expenses during disability", False, "Medical expenses are covered by health insurance; BOE covers business operating expenses."),
      ("All variable and fixed business expenses without limit during disability", False, "BOE has a benefit limit and generally covers fixed overhead expenses, not all variable costs.")]),

    ("The benefit period for a Business Overhead Expense policy is typically:",
     "multiple_choice", "standard",
     "BOE policies are designed as short-term coverage to bridge the gap while the owner recovers or makes alternative arrangements (selling the business, finding a partner). Benefit periods are typically 12-24 months, much shorter than individual DI coverage.",
     [("12 to 24 months — shorter than individual DI policies", True, "Correct. BOE benefit periods are typically 12-24 months because the expectation is that the owner will either recover, sell the business, or make other arrangements."),
      ("To age 65, matching the benefit period of standard individual DI policies", False, "To-age-65 benefit periods are common in individual DI; BOE is typically much shorter at 12-24 months."),
      ("5 years — the standard short-term disability period", False, "5 years is a medium-term DI benefit period; BOE is typically 1-2 years."),
      ("Unlimited — BOE pays as long as the owner remains disabled", False, "BOE has a defined maximum benefit period, typically 1-2 years, not unlimited.")]),

    ("Which of the following is a covered expense under a typical BOE disability policy?",
     "multiple_choice", "standard",
     "BOE covers fixed overhead expenses the business continues to incur even when the owner is disabled: rent, employee salaries and benefits, utilities, equipment lease payments, professional dues, insurance premiums, and similar expenses.",
     [("Employee salaries for staff who continue working during the owner's disability", True, "Correct. Employee salaries are a fixed overhead expense that continues during the owner's disability and is covered by BOE."),
      ("The owner's personal mortgage payment on their home", False, "Personal home mortgage is a personal expense, not a business overhead expense. BOE only covers business expenses."),
      ("The cost of hiring a temporary replacement for the disabled owner", False, "Replacement salary is sometimes covered but is generally not a standard BOE benefit — the owner's personal income and replacement cost are separate from fixed overhead."),
      ("Profits the business would have earned if the owner had not been disabled", False, "Lost profits are not covered by BOE insurance. Lost income for the owner is covered by individual disability income insurance.")]),

    ("Key person disability insurance is purchased by:",
     "multiple_choice", "standard",
     "Key person disability insurance is purchased and owned by the business to protect against the financial loss caused by the disability of a critical employee. The business is the beneficiary and receives the benefit payments.",
     [("The business — with the business as owner and beneficiary of the policy", True, "Correct. Key person disability is purchased by the business, which owns the policy and receives the disability benefit to offset losses from the key person's inability to work."),
      ("The key employee personally — with their family as the beneficiary", False, "Personal disability insurance with family beneficiary describes an individual DI policy, not key person disability."),
      ("A third-party investor who speculates on the key person's health", False, "Third-party investment in others' disability insurance is not a legitimate key person disability structure."),
      ("The key person's employer-sponsored group disability plan as a supplement", False, "Key person disability is a separate business-purpose policy, not a supplement to the group plan.")]),

    ("Disability buy-sell insurance provides benefits that are used to:",
     "multiple_choice", "standard",
     "Disability buy-sell insurance funds a buy-sell agreement that is triggered by disability — when one owner becomes permanently disabled, the disability insurance provides the funds to allow the remaining owners to buy out the disabled owner's interest.",
     [("Fund the purchase of a disabled owner's business interest by the remaining owners", True, "Correct. Disability buy-sell insurance provides cash to buy out a permanently disabled owner's share of the business, similar to how life insurance funds a buy-sell at death."),
      ("Pay the disabled owner's personal living expenses during their disability", False, "Personal living expenses during disability are covered by individual disability income insurance."),
      ("Cover the business's overhead expenses while the disabled owner recovers", False, "Business overhead expenses are covered by BOE disability insurance; buy-sell DI funds ownership transitions."),
      ("Provide tax-free income to the disabled business owner's family", False, "Family income provision is a function of individual life and DI policies; buy-sell DI funds the business transfer.")]),

    ("The definition of disability most favorable to the insured in individual DI policies is:",
     "multiple_choice", "standard",
     "'Own-occupation' disability is the most favorable definition for the insured — it pays if the insured cannot perform the material and substantial duties of their own specific occupation, even if they could work in another occupation.",
     [("Own-occupation — unable to perform the duties of your own specific occupation", True, "Correct. Own-occupation is the most favorable definition because the insured can receive benefits even if they work in a different occupation."),
      ("Any-occupation — unable to perform any job for which they are reasonably suited", False, "Any-occupation is the least favorable definition because the insured must be unable to work in any suitable job to qualify for benefits."),
      ("Modified own-occupation — unable to perform their own occupation AND working in another", False, "Modified own-occupation is less favorable than true own-occupation because it reduces or eliminates benefits if the insured works in another occupation."),
      ("Income replacement — benefits paid only if income declines by more than 80%", False, "Income replacement definitions trigger on income loss rather than occupation definition; own-occupation is still more favorable for most professionals.")]),

    ("Group disability income insurance typically offers which benefit structure?",
     "multiple_choice", "standard",
     "Group DI typically replaces 60-70% of pre-disability income. This is intentional — replacing 100% would reduce the financial incentive to return to work. Group DI often uses 'any-occupation' definitions after an initial own-occupation period.",
     [("60-70% of pre-disability income with a transition from own-occupation to any-occupation definition", True, "Correct. Group DI typically replaces a percentage of income (not 100%) and often uses a definition that shifts from own-occupation to any-occupation after 2 years."),
      ("100% of pre-disability income to ensure no financial hardship to the employee", False, "100% replacement would reduce return-to-work incentives; group DI typically caps replacement at 60-70%."),
      ("A flat weekly benefit the same for all employees regardless of income", False, "Group DI benefits are typically a percentage of salary, not a flat dollar amount the same for all employees."),
      ("Benefits for the insured's entire lifetime if disability begins before age 40", False, "Group DI typically pays to age 65 or a defined benefit period; lifetime benefits are unusual in group plans.")]),

    ("Individual disability income insurance premiums paid by an individual (not through an employer) using after-tax dollars result in:",
     "multiple_choice", "standard",
     "When disability insurance premiums are paid with after-tax personal dollars, the benefits received are income-tax-free. This is a significant advantage for individually-owned DI policies compared to employer-paid group DI.",
     [("Tax-free disability benefit payments — benefits are not includable in income", True, "Correct. Individually-paid after-tax DI premiums result in tax-free benefit payments. You pay tax on the premium (already taxed) so benefits aren't taxed again."),
      ("Taxable disability benefit payments because premiums were deductible", False, "Individually-paid (non-deducted) after-tax premiums result in tax-free benefits, not taxable benefits."),
      ("A tax deduction for the individual in the year premiums are paid", False, "Individual disability insurance premiums are not deductible by employees paying them personally."),
      ("Benefits that are taxed at the long-term capital gain rate", False, "DI benefits are either fully taxable as ordinary income (employer-paid) or tax-free (after-tax individual premiums); capital gain rates do not apply.")]),

    ("A 'return of premium' rider on a disability income policy:",
     "multiple_choice", "standard",
     "A return of premium rider refunds a portion (typically 50-80%) of the premiums paid if the insured does not make any or makes minimal claims over a specified period. It increases the policy cost but provides some premium recovery if disability never occurs.",
     [("Refunds a portion of premiums paid if the insured has few or no claims over a specified period", True, "Correct. The return of premium rider partially refunds premiums if claims are below a threshold — it adds cost but provides premium recovery for claim-free periods."),
      ("Waives all future premiums if the insured becomes disabled", False, "Waiver of premium is a separate rider from return of premium. Waiver of premium waives future premiums during disability."),
      ("Returns the total benefit paid to the insurer if the insured recovers from disability", False, "Benefits paid for a valid disability are not returned; the rider returns premiums, not benefits."),
      ("Pays premiums on behalf of the insured's family members after the insured dies", False, "Premium continuation for family is not the function of a return of premium rider.")]),

    ("The elimination period in a disability income policy is most analogous to:",
     "multiple_choice", "standard",
     "The elimination period is the waiting period between the onset of disability and when benefits begin — it functions like a deductible in time rather than dollars. Longer elimination periods result in lower premiums.",
     [("A deductible — the insured must be disabled for this period before benefits begin", True, "Correct. The elimination period works like a time deductible — no benefits are paid during this waiting period, and longer periods reduce premium costs."),
      ("A grace period — the time after the disability to file a claim", False, "The grace period is the time to pay a premium before lapse; the elimination period is the waiting period at the start of disability."),
      ("A probationary period — the time after policy purchase before any coverage begins", False, "A probationary period may apply to pre-existing conditions; the elimination period applies at the onset of each disability."),
      ("A benefit period — the maximum time benefits will be paid", False, "The benefit period is the maximum duration of benefit payments; the elimination period is the initial waiting period.")]),

    ("Business overhead expense disability insurance benefits are typically:",
     "multiple_choice", "standard",
     "BOE benefits are generally deductible as a business expense when paid, and the benefit payments received are taxable income to the business — since the expenses being reimbursed are also deductible. This creates a wash in most cases.",
     [("Taxable income to the business when received, since the premiums were deductible", True, "Correct. BOE premiums are deductible as a business expense, making the benefits taxable when received — unlike individually-owned DI."),
      ("Always tax-free to the business — no tax is owed on BOE benefit payments", False, "BOE benefits are taxable because the premiums were deducted; there is no tax-free treatment for BOE benefits."),
      ("Deductible to the insured as a medical expense on their personal tax return", False, "BOE is a business policy; the tax treatment is at the business level, not the personal medical expense level."),
      ("Tax-free to the business only if the disability lasts longer than 12 months", False, "Tax treatment of BOE benefits is not based on disability duration; it is based on whether premiums were deducted.")]),

    ("For a self-employed physician who cannot perform surgery due to a back injury, the most appropriate disability coverage would be:",
     "multiple_choice", "standard",
     "A physician who cannot perform surgery needs own-occupation coverage specific to their specialty — not just inability to work in 'any' occupation. Without own-occupation coverage, they could be denied benefits if they could perform a less-demanding medical role.",
     [("Own-occupation DI coverage specific to their surgical specialty", True, "Correct. Own-occupation specialty coverage is essential for physicians — it pays if they cannot perform their specific surgical duties, even if they could work in another medical capacity."),
      ("Any-occupation DI since they can still do administrative medical work", False, "Any-occupation would deny benefits if the physician could work in any suitable capacity, including non-surgical medical roles."),
      ("Workers' compensation — back injuries are covered work-related injuries for self-employed physicians", False, "Workers' compensation generally applies to employees; self-employed physicians typically are not covered by workers' comp."),
      ("Social Security disability only — private DI is redundant for physicians", False, "Social Security disability has very strict standards and long waiting periods; private own-occupation DI is essential for high-income professionals.")]),

    ("A disability income policy's 'partial disability' benefit pays when:",
     "multiple_choice", "standard",
     "Partial disability benefits pay when the insured can perform some but not all of their occupational duties, or when their income is reduced due to disability. This addresses the common scenario where a disabled person can work part-time or in a reduced capacity.",
     [("The insured can work in a limited capacity but suffers reduced income due to disability", True, "Correct. Partial disability benefits address the situation where the insured can work but cannot earn their pre-disability income due to the disability."),
      ("The insured is expected to be disabled for less than 90 days", False, "Short-term disability is typically addressed by the elimination period; partial disability is about reduced capacity, not duration."),
      ("The insured refuses to return to work despite medical clearance", False, "Refusing to return to work after medical clearance would end disability benefits; partial disability benefits support return to work."),
      ("The insured is only partially at fault for the accident that caused their disability", False, "Partial fault for the cause of disability is not relevant to disability benefit eligibility; partial disability is about reduced work capacity.")]),

    ("Which of the following individuals would most benefit from purchasing disability buy-sell insurance?",
     "multiple_choice", "standard",
     "Disability buy-sell insurance is most valuable for business partners who have a mutual agreement that if one partner becomes permanently disabled, the others will buy out their interest. Without the insurance, the surviving partners may lack the cash to complete the buyout.",
     [("Two business partners with a buy-sell agreement who need to fund a buyout if one becomes disabled", True, "Correct. Business partners with a buy-sell agreement need disability buy-sell insurance to ensure they have the funds to execute the agreement if a partner is permanently disabled."),
      ("A sole proprietor with no partners who owns a retail store", False, "A sole proprietor has no buy-sell agreement to fund; other business disability coverages (BOE, individual DI) are more relevant."),
      ("An employee with a family who depends on their income", False, "Income-dependent family members are protected by individual disability income insurance, not disability buy-sell coverage."),
      ("A large publicly-traded company with thousands of shareholders", False, "Publicly-traded companies have different ownership transition mechanisms; disability buy-sell is designed for closely-held businesses with a small number of owners.")]),

    ("A group long-term disability plan with a 180-day elimination period and 24-month own-occupation definition would pay benefits to a disabled employee:",
     "multiple_choice", "standard",
     "With a 180-day elimination period, benefits begin after 6 months of disability. The 24-month own-occupation definition means benefits continue for up to 24 months if the employee cannot perform their own occupation — after that, many group plans shift to any-occupation.",
     [("Starting after 180 days, continuing for up to 24 months under the own-occupation definition", True, "Correct. The 180-day elimination period is served first; then benefits pay for up to 24 months under own-occupation before potentially transitioning to any-occupation."),
      ("Starting immediately — group plans waive elimination periods for work injuries", False, "The 180-day elimination period applies regardless of the cause of disability."),
      ("For the employee's entire lifetime if they are disabled before age 50", False, "A 24-month own-occupation benefit period limits coverage, not lifetime benefits."),
      ("Only if the employee cannot perform any occupation — own-occupation applies only to life insurance", False, "Own-occupation is a disability income insurance definition; the plan's 24-month own-occupation period applies as stated.")]),

    ("The 'waiver of premium' provision in a disability income policy means:",
     "multiple_choice", "standard",
     "The waiver of premium provision in DI policies waives the policyholder's obligation to pay premiums while they are disabled and receiving benefits. This ensures the policy stays in force without the financial burden of premiums during disability.",
     [("Premiums are waived while the insured is disabled and receiving disability benefits", True, "Correct. Waiver of premium prevents the policy from lapsing due to non-payment while the insured is disabled."),
      ("The insured receives a refund of all premiums paid before the disability began", False, "Return of premiums is a separate rider; waiver of premium only waives future premiums during disability."),
      ("The insurer waives the right to terminate the policy for any reason during disability", False, "Waiver of premium specifically waives the premium obligation; policy termination rights are a separate matter."),
      ("The insured can waive premiums anytime they wish for up to 6 months in any 3-year period", False, "Waiver of premium is triggered by disability, not at the insured's discretion.")]),

    ("An overhead expense disability policy's monthly benefit is limited to:",
     "multiple_choice", "standard",
     "BOE benefit amounts are based on the actual documented overhead expenses of the business, subject to the policy's monthly maximum. Benefits cannot exceed actual covered expenses incurred — it is an indemnity product.",
     [("The actual documented overhead expenses incurred, up to the policy's stated maximum", True, "Correct. BOE is an indemnity product — it pays actual covered overhead expenses up to the policy limit, not a set amount regardless of actual expenses."),
      ("A flat percentage of the business's annual gross revenue regardless of actual expenses", False, "BOE benefits are based on actual overhead expenses, not a revenue percentage."),
      ("The policy maximum regardless of actual overhead expenses incurred", False, "BOE pays actual expenses up to the maximum; it does not pay the maximum automatically."),
      ("Double the owner's monthly personal income to cover both business and personal needs", False, "BOE covers business expenses only; personal income replacement requires a separate individual DI policy.")]),

    ("A 'non-cancelable and guaranteed renewable' disability income policy means:",
     "multiple_choice", "standard",
     "Non-cancelable and guaranteed renewable (also called 'non-can') is the highest quality disability policy provision. The insurer cannot cancel the policy, cannot increase premiums, and must renew the policy as long as the insured pays the premiums — until the policy's expiration age.",
     [("The insurer cannot cancel the policy or raise premiums as long as premiums are paid on time", True, "Correct. Non-can policies give the insured the most protection — guaranteed continuation at the original premium rate."),
      ("The insurer can cancel the policy for health reasons but cannot raise premiums", False, "Non-cancelable means the insurer cannot cancel; guaranteed renewable also prevents premium increases."),
      ("The insured can cancel the policy anytime but the insurer cannot", False, "Non-cancelable refers to the insurer's inability to cancel; the insured always retains the right to cancel."),
      ("Premiums are guaranteed to decrease by 5% per year automatically", False, "Non-can guarantees premiums won't increase, not that they'll decrease.")]),

    ("When is a business owner's disability buy-sell agreement typically triggered?",
     "multiple_choice", "standard",
     "Disability buy-sell agreements are typically triggered after a waiting period (often 12-24 months) to ensure the disability is truly permanent. This prevents a forced buyout from a temporary disability that might resolve with treatment.",
     [("After a defined waiting period (typically 12-24 months) confirming permanent or long-term disability", True, "Correct. The waiting period before triggering the buy-sell agreement ensures the disability is long-term, preventing a forced buyout from a short-term disability."),
      ("Immediately upon any disability, even if expected to be short-term", False, "Immediate triggering would force buyouts for temporary disabilities; the waiting period ensures permanence."),
      ("Only if the disability is caused by a workplace accident covered by workers' compensation", False, "Disability buy-sell agreements cover any qualifying disability regardless of cause."),
      ("Only when the disabled partner's productivity drops below 25% of pre-disability levels", False, "The buy-sell trigger is typically based on disability duration, not productivity percentage.")]),

    ("A producer recommending individual disability income insurance to a self-employed attorney should emphasize which feature as most important?",
     "multiple_choice", "standard",
     "For a self-employed attorney, the own-occupation definition is most critical — it ensures they receive full benefits if they cannot practice law as an attorney, even if they could work in a different legal capacity (e.g., teaching law). Without own-occupation coverage, benefits could be denied.",
     [("Own-occupation definition — ensures benefits if unable to practice as an attorney", True, "Correct. Own-occupation is the most critical feature for professionals because it protects their specific career, not just general ability to work."),
      ("A short elimination period — to ensure benefits begin as quickly as possible", False, "While elimination period length matters, the definition of disability is more fundamental for a professional."),
      ("A return of premium rider — to recover costs if no claims are filed", False, "Return of premium adds cost and complexity; the definition of disability is the more critical feature for a self-employed professional."),
      ("A group plan through a bar association — individual coverage is inferior to group", False, "Group plans often use any-occupation definitions; individual own-occupation coverage is superior for professionals.")]),
]


# ── SEED FUNCTION ─────────────────────────────────────────────────────────────

GAP_MODULES = [
    {
        "slug": "gap-indexed-products",
        "title": "Indexed Products: IUL & Fixed Indexed Annuities",
        "description": (
            "Covers Indexed Universal Life (IUL) and Fixed Indexed Annuities (FIA) — "
            "how indexing works, participation rates, cap rates, floors, spreads, "
            "suitability, and tax treatment. High-frequency exam topics in both "
            "L&H licensing and continuing education."
        ),
        "course": "lh",
        "sort_order": 450,
        "questions": INDEXED_PRODUCTS_QUESTIONS,
    },
    {
        "slug": "gap-tax-health-accounts",
        "title": "Tax-Advantaged Health Accounts: HSA, FSA & HRA",
        "description": (
            "Covers Health Savings Accounts (HSA), Flexible Spending Accounts (FSA), "
            "and Health Reimbursement Arrangements (HRA) — eligibility requirements, "
            "contribution limits, rollover rules, tax treatment, and HDHP pairing. "
            "Tested on L&H licensing exams in every state."
        ),
        "course": "lh",
        "sort_order": 452,
        "questions": TAX_HEALTH_ACCOUNTS_QUESTIONS,
    },
    {
        "slug": "gap-medigap",
        "title": "Medicare Supplement Insurance (Medigap)",
        "description": (
            "Covers Medicare Supplement (Medigap) plans A through N — what Medicare "
            "doesn't cover, standardized plan benefits, open enrollment rules, "
            "guaranteed issue rights, the 2020 Plan C/F restrictions, rating methods, "
            "and producer requirements. Essential for any L&H producer."
        ),
        "course": "lh",
        "sort_order": 454,
        "questions": MEDIGAP_QUESTIONS,
    },
    {
        "slug": "gap-retirement-plans",
        "title": "Retirement Plans & Special Life Insurance Concepts",
        "description": (
            "Covers qualified retirement plans (401k, IRA, SEP-IRA, SIMPLE IRA, 403b), "
            "Modified Endowment Contracts (MEC), life and viatical settlements, "
            "key person insurance, buy-sell agreements, Section 1035 exchanges, "
            "and other advanced life insurance concepts tested on L&H exams."
        ),
        "course": "lh",
        "sort_order": 456,
        "questions": RETIREMENT_PLANS_QUESTIONS,
    },
    {
        "slug": "gap-cyber-liability",
        "title": "Cyber Liability Insurance",
        "description": (
            "Covers first-party and third-party cyber liability coverage, data breach "
            "response, ransomware, business interruption, social engineering fraud, "
            "media liability, regulatory defense, and cyber policy structure. "
            "An increasingly tested topic on P&C licensing exams."
        ),
        "course": "pc",
        "sort_order": 458,
        "questions": CYBER_LIABILITY_QUESTIONS,
    },
    {
        "slug": "gap-business-di",
        "title": "Business Disability Income Insurance",
        "description": (
            "Covers Business Overhead Expense (BOE) disability insurance, key person "
            "disability, disability buy-sell funding, group vs individual DI, "
            "own-occupation definitions, elimination periods, and non-cancelable "
            "provisions. Frequently tested on L&H licensing exams."
        ),
        "course": "lh",
        "sort_order": 460,
        "questions": BUSINESS_DI_QUESTIONS,
    },
]


def seed():
    create_all()
    db = SessionLocal()
    try:
        total_mods = total_q = 0

        for mod_def in GAP_MODULES:
            existing = db.scalar(
                select(Module).where(Module.slug == mod_def["slug"]))
            if existing:
                print(f"  SKIP (exists): {mod_def['slug']}")
                continue

            mod = Module(
                slug=mod_def["slug"],
                title=mod_def["title"],
                description=mod_def["description"],
                sort_order=mod_def["sort_order"],
                is_active=True,
            )
            db.add(mod)
            db.flush()
            db.execute(
                text("UPDATE modules SET course=:c WHERE id=:id"),
                {"c": mod_def["course"], "id": mod.id})
            total_mods += 1
            print(f"  MODULE: {mod.title} ({mod_def['course'].upper()})")

            for (q_text, q_type, difficulty, explanation, choices) in mod_def["questions"]:
                q = Question(
                    module_id=mod.id,
                    lesson_id=None,
                    question_text=q_text,
                    question_type=q_type,
                    difficulty=difficulty,
                    explanation=explanation,
                    is_active=True,
                )
                db.add(q)
                db.flush()
                for sort_i, (ct, correct, ce) in enumerate(choices, 1):
                    db.add(AnswerChoice(
                        question_id=q.id,
                        choice_text=ct,
                        is_correct=correct,
                        explanation=ce,
                        sort_order=sort_i,
                    ))
                total_q += 1

        db.commit()
        print(f"\n=== Gap modules complete: {total_mods} modules, "
              f"{total_q} questions ===")
        print("Modules added:")
        for m in GAP_MODULES:
            print(f"  [{m['course'].upper()}] {m['title']} "
                  f"({len(m['questions'])} questions)")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
