"""
MiroFish — Unit Economics & Scale Model (v2)
============================================
Bottom-up model for an automated fresh-meal vending machine ("Rice Bowl Machine")
at a ₹129 price point in India.

v2 CHANGES vs v1 (v1 was materially over-optimistic):
  * Food cost rebuilt bottom-up at ₹41.60/meal, not guessed at ₹24.
  * Throughput assumptions re-anchored to the only public Indian benchmark:
    Daalchini FY22 = ₹12 Cr revenue / ~850 machines = ₹1.4 L per machine per year
    (≈₹387/day ≈ 3 meals/day at ₹129). v1 assumed 120-180 meals/day.
  * Fixed cost bug fixed (maintenance/insurance were per-meal; now per-machine-year).
  * Added "max supportable capex" analysis — the number that decides if the
    machine can exist at all.
  * Added explicit KILL CRITERIA.

Run:  python3 model/financial_model.py
Out:  model/outputs/*.csv
Deps: Python 3.8+, standard library only.
"""

import csv
import os
from dataclasses import dataclass, asdict

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")

# =============================================================================
# 1. BOTTOM-UP MEAL COST
# =============================================================================

# A 400g cooked rice bowl: 220g cooked rice + 140g dal + 40g tadka/garnish.
INGREDIENTS = [
    # item,                       qty,     unit_price, note
    ("Rice (raw)",                0.154,   55.0,  "khichdi/sona masoori wholesale, ₹55/kg"),
    ("Dal / legume (raw)",        0.120,  120.0,  "toor/moong wholesale, ₹110-130/kg"),
    ("Oil + ghee",                0.010,  150.0,  "₹150/kg blended"),
    ("Spice blend (masala)",      0.008,  400.0,  "whole-spice blend, ₹350-450/kg"),
    ("Fresh onion/tomato/ginger", 0.050,   80.0,  "₹80/kg"),
    ("Packaging (bowl/lid/cutlery/bag/label)", 1.0, 10.0, "PP bowl + seal + cutlery + carry bag"),
]


def meal_cost_build():
    rows, total = [], 0.0
    for name, qty, price, note in INGREDIENTS:
        if name.startswith("Packaging"):
            cost = price
        else:
            cost = qty * price
        total += cost
        rows.append({"component": name, "cost_inr": round(cost, 2), "note": note})
    return rows, total


INGREDIENT_ROWS, RAW_FOOD_COST = meal_cost_build()
# ₹41.60 at 129 = 32% of price. Benchmark: a good QSR runs 28-32% food cost.
# So ₹129 is a defensible price. It is NOT the problem with this business.


# =============================================================================
# 2. ASSUMPTIONS
# =============================================================================

@dataclass
class Assumptions:
    price: float = 129.0

    food_cost: float = RAW_FOOD_COST
    waste_pct_of_food: float = 0.15          # held-food model; 8-10% if made-to-order
    energy_per_meal: float = 7.50            # ~1.0 kWh @ ₹7.5 (Haryana LT commercial)
    payment_pct: float = 0.018               # UPI/card MDR blend
    promo_per_meal: float = 3.0
    site_commission_pct: float = 0.03

    # Per-machine-year fixed costs
    route_labour: float = 150_000.0          # 1 tech @ ₹22.5L/yr ÷ 15 machines
    maintenance_pct_capex: float = 0.12      # 16 augers, 3 chambers, boiler, seals
    insurance_software_iot: float = 50_000.0
    interventions_per_month: float = 2.0
    cost_per_intervention: float = 800.0
    depreciation_years: float = 5.0

    availability_steady: float = 0.92
    availability_year1: float = 0.85

    def var_cost(self):
        food = self.food_cost * (1 + self.waste_pct_of_food)
        return (food + self.energy_per_meal + self.price * self.payment_pct
                + self.promo_per_meal + self.price * self.site_commission_pct)

    def contribution(self):
        return self.price - self.var_cost()


@dataclass
class SiteType:
    name: str
    rent_per_year: float
    operating_days: int
    assumed_meals_per_day: float
    capex: float
    repeat_intensity: str
    note: str


# Rent = all-in occupancy cost for ~35 sq ft (base + CAM + utility), benchmarked to
# Anarock mall leasing (kiosks ~₹618/sq ft/mo India avg) and Gurugram office rents.
SITES = [
    SiteType("Captive office ≥800 staff (free space)", 60_000, 250, 55, 1_500_000,
             "Very high", "Same person, 4-5x/week. The only genuinely good site."),
    SiteType("Paid kiosk, Grade A office park", 480_000, 250, 45, 1_500_000,
             "High", "Rent is 8x the captive case for the same demand."),
    SiteType("Hospital (private, lobby)", 300_000, 365, 50, 1_500_000,
             "Medium-high", "Attendants eat 3x/day; captive but price-sensitive."),
    SiteType("Airport (terminal)", 1_200_000, 365, 60, 1_500_000,
             "None", "One-off travellers. No repeat, brutal concession fee."),
    SiteType("Metro station (DMRC)", 480_000, 365, 40, 1_500_000,
             "Low", "4-hour peak; commuters carry bags, rarely eat a bowl standing."),
    SiteType("Shopping mall food court", 720_000, 365, 45, 1_500_000,
             "Low", "Weekend-heavy. Competes with 20 hot QSRs at same price."),
    SiteType("Highway wayside", 240_000, 365, 30, 1_500_000,
             "Very low", "Travellers want a sit-down break. Wrong occasion entirely."),
]


# =============================================================================
# 3. CORE ENGINE
# =============================================================================

def machine_pnl(a, site, meals_per_day, availability=None, capex=None):
    availability = a.availability_steady if availability is None else availability
    capex = site.capex if capex is None else capex

    eff = meals_per_day * availability
    meals_yr = eff * site.operating_days
    revenue = meals_yr * a.price

    var = a.var_cost() * meals_yr
    contribution = revenue - var

    fixed = (site.rent_per_year + a.route_labour
             + a.maintenance_pct_capex * capex + a.insurance_software_iot
             + a.interventions_per_month * 12 * a.cost_per_intervention)

    ebitda = contribution - fixed
    dep = capex / a.depreciation_years
    payback = capex / ebitda if ebitda > 0 else float("inf")

    return {
        "site": site.name,
        "meals_per_day": meals_per_day,
        "meals_per_year": round(meals_yr),
        "revenue_lakh": round(revenue / 1e5, 1),
        "contribution_lakh": round(contribution / 1e5, 1),
        "contribution_per_meal": round(a.contribution(), 2),
        "fixed_lakh": round(fixed / 1e5, 1),
        "ebitda_lakh": round(ebitda / 1e5, 1),
        "ebitda_margin_pct": round(100 * ebitda / revenue, 1) if revenue else 0.0,
        "ebit_lakh": round((ebitda - dep) / 1e5, 1),
        "capex_lakh": round(capex / 1e5, 1),
        "payback_years": round(payback, 2) if payback != float("inf") else -1,
        "revenue_to_capex": round(revenue / capex, 2) if capex else 0,
    }


def breakeven_meals(a, site, availability=None, capex=None):
    availability = a.availability_steady if availability is None else availability
    capex = site.capex if capex is None else capex
    fixed = (site.rent_per_year + a.route_labour
             + a.maintenance_pct_capex * capex + a.insurance_software_iot
             + a.interventions_per_month * 12 * a.cost_per_intervention)
    return fixed / (a.contribution() * availability * site.operating_days)


def max_supportable_capex(a, site, meals_per_day, payback_years=3.0,
                          availability=None):
    """
    Invert the P&L: at a given throughput, what is the most we can spend on the
    machine and still recover it in `payback_years`? Maintenance scales with capex,
    so solve algebraically.

      EBITDA = C - (rent + labour + ins + intr) - m*capex
      want capex / EBITDA = P
      => capex = P * (K - m*capex)   where K = C - (rent+labour+ins+intr)
      => capex(1 + P*m) = P*K
    """
    availability = a.availability_steady if availability is None else availability
    meals_yr = meals_per_day * availability * site.operating_days
    C = a.contribution() * meals_yr
    K = C - (site.rent_per_year + a.route_labour + a.insurance_software_iot
             + a.interventions_per_month * 12 * a.cost_per_intervention)
    if K <= 0:
        return -1.0
    m = a.maintenance_pct_capex
    return payback_years * K / (1 + payback_years * m)


# =============================================================================
# 4. REPORTS
# =============================================================================

def write_csv(path, rows):
    os.makedirs(OUT, exist_ok=True)
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"    → {os.path.basename(path)} ({len(rows)} rows)")


def r_meal_cost():
    print("\n[1] BOTTOM-UP COST OF ONE 400g RICE BOWL")
    print(f"    {'component':<42}{'₹':>8}")
    for r in INGREDIENT_ROWS:
        print(f"    {r['component']:<42}{r['cost_inr']:>8.2f}")
    print(f"    {'TOTAL RAW FOOD + PACK':<42}{RAW_FOOD_COST:>8.2f}"
          f"   ({RAW_FOOD_COST/129*100:.0f}% of ₹129)")
    print("    Benchmark: healthy QSR food cost is 28-32% of price. ₹129 is fine.")
    write_csv(f"{OUT}/meal_cost_build.csv", INGREDIENT_ROWS)


def r_margin_stack(a):
    print("\n[2] CONTRIBUTION PER MEAL")
    print(f"    Price                                  {a.price:>8.2f}")
    print(f"    Food (incl. {a.waste_pct_of_food:.0%} waste)              {-a.food_cost*(1+a.waste_pct_of_food):>8.2f}")
    print(f"    Energy                                 {-a.energy_per_meal:>8.2f}")
    print(f"    Payment MDR                            {-a.price*a.payment_pct:>8.2f}")
    print(f"    Promo / discount                       {-a.promo_per_meal:>8.2f}")
    print(f"    Site commission                        {-a.price*a.site_commission_pct:>8.2f}")
    print(f"    {'CONTRIBUTION':<38}{a.contribution():>8.2f}"
          f"   ({a.contribution()/a.price*100:.0f}% margin)")
    print("    The bowl is a healthy product. The problem is downstream of this line.")
    rows = [{"line": "price", "inr": a.price},
            {"line": "food_incl_waste", "inr": round(-a.food_cost*(1+a.waste_pct_of_food), 2)},
            {"line": "energy", "inr": -a.energy_per_meal},
            {"line": "payment_mdr", "inr": round(-a.price*a.payment_pct, 2)},
            {"line": "promo", "inr": -a.promo_per_meal},
            {"line": "site_commission", "inr": round(-a.price*a.site_commission_pct, 2)},
            {"line": "contribution", "inr": round(a.contribution(), 2)},
            {"line": "contribution_margin_pct", "inr": round(100*a.contribution()/a.price, 1)}]
    write_csv(f"{OUT}/contribution_stack.csv", rows)


def r_breakeven(a):
    print("\n[3] BREAK-EVEN THROUGHPUT VS WHAT SITES ACTUALLY DELIVER")
    print(f"    {'site':<38}{'rent':>8}{'BE/d':>7}{'plan/d':>8}{'verdict':>12}")
    rows = []
    for s in SITES:
        be = breakeven_meals(a, s)
        plan = s.assumed_meals_per_day
        ratio = plan / be
        v = ("PASS" if ratio >= 1.5 else
             "MARGINAL" if ratio >= 1.0 else "FAILS")
        print(f"    {s.name[:38]:<38}{s.rent_per_year/1e5:>7.1f}L{be:>7.0f}"
              f"{plan:>8.0f}{v:>12}")
        rows.append({"site": s.name,
                     "rent_lakh": round(s.rent_per_year/1e5, 1),
                     "operating_days": s.operating_days,
                     "breakeven_meals_per_day": round(be, 1),
                     "assumed_meals_per_day": plan,
                     "headroom_x": round(ratio, 2),
                     "repeat_intensity": s.repeat_intensity,
                     "verdict": v, "note": s.note})
    write_csv(f"{OUT}/breakeven_by_site.csv", rows)


def r_site_pnl(a):
    print("\n[4] PER-MACHINE P&L AT ASSUMED THROUGHPUT (₹15L capex)")
    print(f"    {'site':<38}{'rev':>7}{'EBITDA':>8}{'mgn':>6}{'payback':>9}{'rev/capex':>10}")
    rows = []
    for s in SITES:
        p = machine_pnl(a, s, s.assumed_meals_per_day)
        pb = f"{p['payback_years']:.1f}y" if p["payback_years"] > 0 else "never"
        print(f"    {s.name[:38]:<38}{p['revenue_lakh']:>6.1f}L"
              f"{p['ebitda_lakh']:>7.1f}L{p['ebitda_margin_pct']:>5.0f}%"
              f"{pb:>9}{p['revenue_to_capex']:>9.1f}x")
        rows.append(p)
    write_csv(f"{OUT}/per_machine_pnl.csv", rows)


def r_volume_reality(a):
    print("\n[5] THE CENTRAL QUESTION: CAN ANYONE HIT THESE VOLUMES?")
    daalchini_rev = 12e7 / 850
    print(f"    Public benchmark — Daalchini FY22, ~850 machines, ₹12 Cr revenue:")
    print(f"      ₹{daalchini_rev/1e5:.1f}L per machine per year "
          f"= ₹{daalchini_rev/365:.0f}/day")
    print(f"      = {daalchini_rev/365/129:.1f} meals/day at ₹129 "
          f"(or {daalchini_rev/365/50:.1f} transactions at ₹50)")
    print(f"    India's largest vending operator runs at ~3-8 transactions/day/machine.")
    print(f"    This model needs ~{breakeven_meals(a, SITES[0]):.0f} meals/day just to break even.")
    print("    → The gap is not 20%. It is 5-10x. THAT is the business risk.")
    rows = [{"metric": "daalchini_rev_per_machine_year", "value": round(daalchini_rev),
             "unit": "INR"},
            {"metric": "implied_meals_per_day_at_129", "value": round(daalchini_rev/365/129, 1),
             "unit": "meals"},
            {"metric": "model_breakeven_meals_day_captive_office",
             "value": round(breakeven_meals(a, SITES[0]), 1), "unit": "meals"},
            {"metric": "gap_multiple",
             "value": round(breakeven_meals(a, SITES[0]) / (daalchini_rev/365/129), 1),
             "unit": "x"}]
    write_csv(f"{OUT}/volume_reality.csv", rows)


def r_max_capex(a):
    print("\n[6] MAX SUPPORTABLE MACHINE COST (3-year payback)")
    print("    This is the sentence that decides the company.")
    print(f"    {'meals/day':>10}{'captive office':>18}{'paid kiosk':>14}{'mall':>12}")
    rows = []
    for m in (20, 30, 40, 50, 60, 80, 100):
        vals = []
        row = {"meals_per_day": m}
        for label, s in (("office", SITES[0]), ("kiosk", SITES[1]), ("mall", SITES[5])):
            c = max_supportable_capex(a, s, m)
            row[f"{label}_max_capex_lakh"] = (round(c/1e5, 1) if c > 0 else None)
            if c <= 0:
                vals.append("—")
            elif c < 1e5:
                vals.append(f"₹{c/1e3:.0f}k")
            else:
                vals.append(f"₹{c/1e5:.0f}L")
        print(f"    {m:>10}{vals[0]:>18}{vals[1]:>14}{vals[2]:>12}")
        rows.append(row)
    write_csv(f"{OUT}/max_supportable_capex.csv", rows)
    print("    Your spec implies a ₹10-15L machine. That needs 45-60 meals/day")
    print("    at a captive office, or ~65+ in a paid kiosk. Below that the machine")
    print("    cannot pay for itself and no amount of capital fixes it.")


def r_scale(a, meals=55):
    print(f"\n[7] SCALE PATH (assuming {meals} meals/day — optimistic but defensible)")
    rev_per_machine = a.price * meals * a.availability_steady * 312
    capex_per_machine = 1_100_000          # at 500+ cumulative units
    wc_per_machine = 60_000                # spares, kitchen float, refunds, buffer
    print(f"    Revenue per machine per year: ₹{rev_per_machine/1e5:.1f}L")
    print(f"    {'revenue target':>16}{'machines':>11}{'machine capex':>16}{'total capital':>16}")
    rows = []
    for target, label in ((1e8, "₹10 Cr"), (2.5e9, "₹250 Cr"), (1e10, "₹1,000 Cr")):
        n = target / rev_per_machine
        capex = n * capex_per_machine
        wc = n * wc_per_machine
        total = capex + wc
        print(f"    {label:>16}{n:>11.0f}{'₹'+str(round(capex/1e7, 1))+' Cr':>16}"
              f"{'₹'+str(round(total/1e7, 1))+' Cr':>16}")
        rows.append({"revenue_target_cr": round(target/1e7),
                     "revenue_per_machine_lakh": round(rev_per_machine/1e5, 1),
                     "machines_required": round(n),
                     "machine_capex_cr": round(capex/1e7, 1),
                     "working_capital_cr": round(wc/1e7, 2),
                     "total_capital_cr": round(total/1e7, 1)})
    write_csv(f"{OUT}/scale_path.csv", rows)
    n_big = 1e10 / rev_per_machine
    print(f"    ₹1,000 Cr revenue needs ~{n_big:,.0f} machines and "
          f"~₹{n_big*capex_per_machine/1e7:,.0f} Cr of machine capital.")
    print("    That is an infrastructure-financing problem, not a startup.")


def r_scenarios(a):
    print("\n[8] SCENARIO STACK — 500-machine network, year 3")
    scen = [
        ("BEAR  churn 30%/yr, 25 meals/d, 82% uptime, ₹11L capex", 25, 0.82, 1_100_000, 400_000),
        ("BASE  45 meals/d, 90% uptime, ₹9L capex at volume",        45, 0.90,   900_000, 350_000),
        ("BULL  70 meals/d, 94% uptime, ₹7L capex at scale",         70, 0.94,   700_000, 300_000),
    ]
    rows = []
    for name, m, avail, capex, rent in scen:
        s = SiteType("network", rent, 320, m, capex, "", "")
        p = machine_pnl(a, s, m, availability=avail, capex=capex)
        rev = p["revenue_lakh"] * 500 / 100
        eb = p["ebitda_lakh"] * 500 / 100
        print(f"    {name:<58} rev ₹{rev:>5.0f} Cr  EBITDA ₹{eb:>5.0f} Cr")
        rows.append({"scenario": name, "meals_per_day": m, "uptime": avail,
                     "capex_lakh": capex/1e5,
                     "network_revenue_cr": round(rev, 1),
                     "network_ebitda_cr": round(eb, 1),
                     "ebitda_margin_pct": p["ebitda_margin_pct"]})
    write_csv(f"{OUT}/scenarios.csv", rows)


def r_capacity():
    print("\n[9] HOPPER CAPACITY vs YOUR STATED 500-1,000 MEALS/DAY")
    raw_kg_per_meal = 10.0 / 65
    hopper = 15.0
    max_meals = hopper / raw_kg_per_meal
    print(f"    Your own ratio (10 kg rice → 65 people) = {raw_kg_per_meal*1000:.0f} g raw rice/person")
    print(f"    One 15 kg rice hopper therefore tops out at {max_meals:.0f} meals.")
    rows = []
    for t in (200, 500, 1000):
        refills = t / max_meals
        mins = 240 / refills
        print(f"    {t:>5} meals/day → {refills:>4.1f} refills/day, "
              f"one every {mins:>5.0f} min during a 4-hour peak")
        rows.append({"meals_per_day": t, "refills_per_day": round(refills, 1),
                     "minutes_between_refills_in_peak": round(mins)})
    write_csv(f"{OUT}/hopper_capacity.csv", rows)
    print("    → A single 15 kg rice hopper CANNOT serve 500/day. Either the hopper")
    print("      becomes a continuous feed (new mechanism, new patent, new cost) or")
    print("      the '500-1,000 meals/day' target is a 5-10 machine cluster, not one unit.")


def r_kill_criteria():
    print("\n[10] KILL CRITERIA — stop before you spend ₹3 Cr finding these out")
    crit = [
        ("Pilot ≥25 meals/day in a captive office for 8 weeks", "CAC/pull problem"),
        ("Uptime ≥85% over 500 consecutive meal cycles", "Reliability unsolved"),
        ("Food cost ≤₹45/meal at scale", "Unit economics unsolved"),
        ("Per-meal cycle ≤3 min with zero interventions", "Throughput unsolved"),
        ("80%+ of eaters repeat within 2 weeks", "Product/market fit unsolved"),
        ("Cleaning cycle <10 min, no manual scrub", "Ops model unsolved"),
        ("Machine BOM at 100 units ≤₹18L", "Manufacturing unsolved"),
    ]
    rows = []
    for c, fails in crit:
        print(f"    [ ] {c:<58} if missed → {fails}")
        rows.append({"criterion": c, "if_missed_means": fails})
    write_csv(f"{OUT}/kill_criteria.csv", rows)


def main():
    a = Assumptions()
    os.makedirs(OUT, exist_ok=True)
    print("=" * 78)
    print("MIROFISH — UNIT ECONOMICS MODEL v2")
    print(f"Price ₹{a.price:.0f}/bowl   Food ₹{a.food_cost:.2f}   "
          f"Contribution ₹{a.contribution():.2f}")
    print("=" * 78)

    r_meal_cost()
    r_margin_stack(a)
    r_breakeven(a)
    r_site_pnl(a)
    r_volume_reality(a)
    r_max_capex(a)
    r_scale(a)
    r_scenarios(a)
    r_capacity()
    r_kill_criteria()

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    be = breakeven_meals(a, SITES[0])
    print(f"  The product is sound: ₹{RAW_FOOD_COST:.0f} food cost, "
          f"{a.contribution()/a.price*100:.0f}% contribution margin at ₹129.")
    print(f"  The machine is the risk: it needs ~{be:.0f} meals/day to pay back,")
    print(f"  and no Indian vending operator publicly exceeds ~8 at ₹129 terms.")
    print(f"  Unicorn: possible, but NOT as a vending machine story.")
    print(f"  It has to be a captive-density food brand that happens to use machines.")
    print(f"\n  Outputs → {OUT}/")


if __name__ == "__main__":
    main()
