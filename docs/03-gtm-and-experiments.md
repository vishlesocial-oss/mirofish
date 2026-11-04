# MiroFish — Go-To-Market and the First 18 Months

The engineering plan is in `02-engineering-review.md`. This document is about the part that actually decides the outcome: **who pays, for what, and how you find out cheaply that they won't.**

---

## 1. The core reframe

Your brief targets seven location types at once. The analysis (`01-unicorn-analysis.md` §5.2) shows four of them are structurally unprofitable and one is a concession-fee trap.

**Ship to two: offices and hospitals. Both captive. Both repeating. Both with an employer/administrator who has a budget and a duty of care.**

Everything else is a distraction until you have 30 sites.

---

## 2. Who actually pays

This is the most important table in the document, because it changes your sales motion, your pricing, and your cash cycle.

| Model | Who pays | Price realised | Volume | Cash cycle | Works? |
|---|---|---|---|---|---|
| **A. Pure walk-up** | Employee, ad hoc | ₹129 | Low, volatile | Instant | Weak — this is the Daalchini trap |
| **B. Employer subsidy** | Employer ₹49 + employee ₹80 | ₹129 | **High, contracted** | Monthly invoice | **Yes — this is the unlock** |
| **C. Prepaid meal pack** | Employee, bulk buy | ₹119 (10-pack) | Medium, committed | Upfront | Good — improves cash |
| **D. Full canteen replacement** | Employer, per-head contract | ₹110–125 | Very high, guaranteed | Monthly | Best economics, hardest sale |

### Why B is the unlock

- **Tax:** from FY 2026-27 the meal-perquisite exemption is **₹200/meal (₹1,05,600/yr)**. A ₹129 subsidised meal is *inside* the exemption. Employer cost is a deductible business expense, employee benefit is tax-free, and neither side pays tax on it. This is new and it is a genuine reason for an HR head to take your call.
- **Volume:** a subsidised meal roughly doubles uptake. At ₹129 unsubsidised you compete with a ₹60 office canteen. At ₹80 effective you don't.
- **Predictability:** contracted headcount converts your worst problem (forecast) into a signed number.
- **Sales:** one signature gets you 800–3,000 potential customers at one address. Compare that to 3,000 individual walk-ups.

### The economics of a subsidy deal

Employer pays ₹49 × 22 days × 60% uptake of 800 staff = **₹5.2 L/year** to them — less than a coffee machine contract at many Indian offices, and it is tax-advantaged. You get ₹129 realised on every bowl with contracted volume. **The subsidy is not a discount; it is payment for demand certainty**, and it is the cheapest customer acquisition in the business.

---

## 3. Segment prioritisation

| Segment | Site count (NCR est.) | Deal size | Sales cycle | Priority |
|---|---|---|---|---|
| **IT/ITES & GCC campuses, 800+ staff** | ~400 | ₹15–40 L/yr | 3–6 months | **1** |
| **Private hospitals, 150+ beds** | ~250 | ₹12–25 L/yr | 4–8 months | **2** |
| Manufacturing plants (captive, 1,000+ workers) | ~150 | ₹20–50 L/yr | 6–9 months | 3 |
| Co-working (WeWork/Awfis) | ~80 | ₹4–8 L/yr | 1–2 months | 4 — fast, small, good for learning |
| Universities/campuses | ~60 | ₹20–60 L/yr | 9–12 months (tender) | 5 |
| **Malls, metros, airports, highways** | — | — | — | **Do not enter** |

**Start with co-working for speed of learning, and IT campuses for size.** Co-working gets you a live machine in 6 weeks and teaches you about real humans. IT campuses pay the bills.

---

## 4. The first 30 sites — concrete

Do not build a sales organisation. Do this yourself:

1. **Make a list of 120 buildings** within a 12 km radius of your workshop, with ≥800 employees. You can build this from LinkedIn company pages + Google Maps in two days. **Radius matters more than prestige** — route density is the whole economics.
2. **Find the person who owns the canteen contract**, not the CEO. Titles: Admin Head, Facilities Manager, Employee Experience, HR Operations, Admin. They have a budget line called "employee welfare" and a problem called "the canteen is bad and people complain."
3. **Lead with the problem they already have**, not your technology: *"Your canteen serves 400 people in 45 minutes and the food is cold by the time the last person eats. We install a unit that serves a hot ₹129 bowl in 3 minutes, and we subsidise it with you at ₹49."* Never lead with "robotic kitchen" or "AI vision."
4. **Offer a 60-day paid pilot** at ₹1.5 L, with a written success metric (meals/day, repeat rate, uptime). Free pilots destroy your credibility and your cash.
5. **Target: 30 signed sites in 12 months.** At 45 meals/day that is a ₹58 Cr annualised run-rate and the proof you need for a Series A.

### The objection you will hear most

*"We already have a canteen contractor."* — Correct, and true at every site. Your answers, in order:
- You are not replacing the canteen, you are serving the 30% who don't eat there (they go out, or skip, or order Swiggy).
- You are 24/7; the canteen is 12:30–14:30.
- You report per-meal consumption data the canteen never gives them.
- **And critically:** if the facility manager is a Sodexo/Compass-type contractor, offer *them* the operator model (see §6) instead of competing. Convert the gatekeeper into the channel.

---

## 5. What people actually do vs. what they say

The single most useful thing you can build in the next 90 days is not a machine. It is an **observation log**. Every automated-food company that died was confident about behaviour it had not measured.

Hypotheses to test, with the number that kills each:

| # | Hypothesis | Test | Kill if |
|---|---|---|---|
| H1 | People will pay ₹129 for a machine-cooked bowl | Manual counter, fixed price, 8 weeks | <25 bowls/day |
| H2 | They will repeat | Track individual repeat purchases | <40% buy twice in 10 days |
| H3 | Freshness/no-manual-intervention matters to them | A/B copy: "cooked after you pay" vs "chef-prepared" | No difference in conversion |
| H4 | They will accept a 3-minute wait | Measure abandonment at 0 / 90 / 180 s queue | >20% abandon at 3 min |
| H5 | Employers will pay ₹49 | 10 conversations with Admin Heads; ask for a signed pilot | <3 of 10 say yes |
| H6 | Tadka-on-top is perceptible | Blind triangle test, 30 eaters, tadka-now vs tadka-2h-ago | <60% correctly identify |
| H7 | Pre-order works | Offer pre-order to 100 people | <5% use it → delete the feature |

**H7 is the one that saves you the most money.** If pre-order fails — and the strong prior is that it will — you delete an entire subsystem, the pre-soak cycle, and the forecast problem, for the cost of one experiment.

**H6 costs ₹25,000 and tells you whether your only differentiated feature is real.** Run it first. Blind triangle test with 30 people in an office canteen, tadka poured 20 seconds before serving vs 2 hours before. If they cannot tell the difference, do not spend a rupee on the tadka module and do not file the patent.

---

## 6. The model that scales: sell the system, not the meals

By month 18–24, your constraint will not be demand or technology. It will be **capital**: every new machine is ₹9–13 L of your balance sheet, and at 500 machines that is ₹50 Cr+ of hardware you have to fund before you earn a rupee of depreciation back.

Three ways out, in ascending order of attractiveness:

### Option 1 — Franchise/operator (fastest to scale)
You sell the machine (₹13 L, 30% margin), the consumable ingredient kits (40% margin), and the software subscription (₹4,000/month). The operator — a regional entrepreneur, a canteen contractor, a facility-management company — owns the asset and takes the volume risk. You take a per-meal royalty of ₹8–12.

- **Your revenue:** ₹13 L + ₹4.8 L/yr + kit margin + royalty
- **Your capex:** ~zero
- **Risk:** quality control, brand dilution, and operators who underperform

This is how Daalchini reached 2,000 kiosks on $6.73M. The capex sits on someone else's balance sheet. It is not glamorous, and it is how you get to scale without raising ₹500 Cr.

### Option 2 — Sell to the canteen contractors
Sodexo, Compass, Elior and their Indian equivalents already own the site relationships you are fighting for, and they are all under margin pressure on labour. Sell *them* a machine that removes 2 kitchen staff per site. You become a supplier to the incumbent instead of a competitor to it — a much easier sale, and it converts the gatekeeper problem into a channel.

### Option 3 — Own the sites (best economics, worst capital)
Operate everything yourself. Highest margin, highest control, and requires ₹50 Cr+ of hardware capital. Only viable after a Series B.

**Recommended sequence: own the first 30 (prove it), franchise the next 200 (scale it), supply contractors in parallel (hedge it).**

---

## 7. Brand and menu — the things that actually make people come back

The machine is the how. This is the what, and it is what they judge you on.

**One dish, three variants, done perfectly.** Not forty SKUs. Indian food history is unambiguous — biryani, momos, chai, dosa, vada pav. Narrow menus win because they let you perfect one thing and simplify the machine that makes it.

Suggested opening menu (all at ₹129, all ~450–550 kcal, all vegetarian to start — this halves your cold chain, allergen, and food-safety complexity):

| Variant | Base | Blend | Fresh finish |
|---|---|---|---|
| Ghar ki Dal-Chawal | Rice + toor dal | Cumin-ginger tadka blend | Ghee tadka, fresh coriander |
| Sambar Rice | Rice + toor/moong | Sambar blend | Ghee + curry leaf tadka |
| Pulao Bowl | Rice + moong dal | Whole-spice pulao blend | Fried onion + ghee |

**Naming matters more than you think.** "Home-made chef style" (your phrase) is a good instinct but vague. The claim that will actually sell is narrower and provable: **"Cooked after you pay."** It is true, it is verifiable, it is the exact opposite of a canteen's promise, and it directly attacks the held-food quality problem your competitors have.

**Nutrition transparency is a moat.** Publish calories, protein, and sodium per bowl. Nobody in Indian canteen food does this, and it is precisely what your target customer (health-aware professional, 25–38) says they want. It is also free to produce — you already know every gram that went in because you weigh it.

---

## 8. 18-month plan with gates and spend

| Phase | Months | Spend | Build | Evidence required to proceed |
|---|---|---|---|---|
| **0. Demand** | 0–3 | ₹18 L | Manual counter, one office, 400 bowls/week | ≥25 bowls/day; ≥40% repeat in 10 days |
| **1. Modules** | 4–9 | ₹55 L | Tadka module, 1 chamber, CIP, dispense | Tadka blind test ≥60%; CIP leaves no film; 3-min cook holds texture |
| **2. Alpha** | 10–15 | ₹95 L | 1 integrated unit, 10 hoppers, induction only | ≥85% uptime over 500 cycles; BOM ≤₹13 L at 10 units |
| **3. Proof** | 16–18 | ₹1.2 Cr | 3 units, 3 sites, 1 route | ≥45 meals/day; cleaning ≤10 min by non-specialist; service labour <1.5 hrs/day/machine |

**Cumulative: ₹2.9 Cr to reach a defensible Series A.** Not ₹3 Cr to build a machine — ₹2.9 Cr to build a *company with evidence*.

Note the shape: **two-thirds of the spend happens after you have proof that people want the food.** That is the entire discipline. If Phase 0 fails, you have spent ₹18 L, not ₹3 Cr.

---

## 9. Team — the first 8 hires

| Role | When | Why it is this early |
|---|---|---|
| **Food lead / chef** (from a QSR or cloud kitchen, not a hotel) | Month 0 | Recipe *reproducibility* is the product. A hotel chef will fight the machine; a QSR chef will engineer for it. |
| Mechanical design engineer (food equipment background) | Month 1 | Hoppers, augers, CIP. This is the hardest hire to get right. |
| Embedded/firmware engineer | Month 3 | Closed-loop dispense, load cells, thermal control. |
| Ops lead (ex-vending or ex-QSR area manager) | Month 6 | Route economics, service SLAs. Hiring this late is the most common scaling failure. |
| Field service technician ×2 | Month 12 | Learn by doing before you write the manual. |
| B2B sales (ex-corporate catering or facilities) | Month 10 | Sells to Admin Heads, not consumers. |
| Supplier/manufacturing engineer | Month 15 | Takes BOM from ₹13 L to ₹9 L; this hire pays for itself. |

**Deliberately not hiring early:** a CTO, a growth marketer, or a large engineering team. The binding constraint is *evidence*, not headcount.

---

## 10. Risks and how you would know early

| Risk | Early signal | Mitigation |
|---|---|---|
| Demand below 25/day | Phase 0 week 3 | Stop. Do not build. |
| Tadka difference imperceptible | ₹25k blind test, week 4 | Drop the feature, drop the patent, re-plan differentiation |
| Cleaning film | Phase 1 CIP test, week 20 | This kills the thesis. Prototype it before anything else. |
| BOM >₹15 L at 100 units | Month 12 quotes | Cut hoppers further; drop to 2 chambers |
| Employer won't subsidise | 10 conversations, month 2 | Fall back to prepaid packs; accept lower volume |
| Facility managers block you | First 5 site attempts | Convert to operator model |
| A funded competitor bundles it free | Ongoing | Your defence is site contracts and recipe blends, not hardware |
| Food-safety incident | Any single event | This is existential. Over-invest in logging and CIP. |
| GST makes ₹129 realised ₹122.86 | Confirm before pricing | Model it now, not after launch |

---

## 11. The one-line strategy

> **Win 30 office buildings with a subsidised ₹129 bowl that is cooked after you pay, prove 45 meals/day and 85% uptime, cut the machine from ₹13 L to ₹9 L, then franchise the system instead of funding the hardware.**

If you can say that sentence to an investor with 12 months of data behind it, you can raise. If you build the machine first and go looking for sites, you will join a long list of well-engineered companies that could not find enough people to eat.
