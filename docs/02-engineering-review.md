# MiroFish — Engineering Design Review

**Input:** Subsystem brief dated Nov 2026 (3 subsystems, ~21 hoppers, steam + PID, 3 chambers)
**Purpose:** Convert the brief into a buildable, costed architecture. Every change is justified by either cost, reliability, or food quality — not preference.

---

## 1. Summary of recommended changes

| # | In your brief | Recommendation | Why |
|---|---|---|---|
| 1 | ~21 hoppers (8 main + 8 masala + 4 tadka + oil + ghee) | **10 hoppers** (4 ingredient + 3 recipe blends + oil + ghee + water) | Cuts ~11 motors, 11 failure modes, and ~₹3–4 L of BOM. Blends are *better* for consistency than individual spices. |
| 2 | Steam boiler + PID cooktop | **Induction PID only.** Steam confined to CIP cleaning. | Removes pressure vessel, scale/water treatment, certification burden, and a service tech who can handle a boiler. |
| 3 | Overnight pre-soak cycle | **Delete.** Cook from dry, made to order. | Removes 12 hours of warm standing water (bacterial incubator) and a whole valve/drain subsystem. |
| 4 | Customer pre-orders "for the next day" | **Made to order, ≤3 min cycle.** | Removes forecast risk, waste, and holding-time quality loss. |
| 5 | 3 holding chambers, dispense from hold | **2 holding chambers** (rice, dal) + **tadka cooked fresh at dispense** | Holding is where quality dies. Keep only what must be held. |
| 6 | 500–1,000 meals/day per unit | **150–250 meals/day per unit**, or a 5–7 unit cluster | One 15 kg rice hopper physically maxes at 98 meals (see §3). |
| 7 | AI vision camera "to ensure food is properly cooked" | **Keep, but change the job.** Use it for *portion verification and spill detection*, not doneness. | Doneness is solved by recipe + PID + load cell. Vision is the expensive, unreliable way to do it. |
| 8 | Manual leftover collection or drain flush | **Weigh the holding chamber at every dispense.** | Delta = waste. This single metric turns the machine into a data business. |
| 9 | 2–3 patents on core tech | **2 narrow claims max** (tadka dispense sequence; anti-bridging micro-dose). FTO search first. | Core space is prior art since 2014 (WO2016030906A1). See memo §8. |

---

## 2. Revised hopper architecture (21 → 10)

### The reduction logic

You do not need 8 masala hoppers for a 6–10 item menu. **A dish's identity is in a blend, not in individual spices.** A sambar, a tadka, and a biryani masala are three powders, not twenty-one.

| Hopper | Contents | Dose/meal | Why it stays |
|---|---|---|---|
| H1 | Rice (or alternate grain) | 154 g | Base |
| H2 | Dal / legume A | 120 g | Base |
| H3 | Dal / legume B *(optional, can be merged with H2)* | — | Menu breadth |
| H4 | Fresh component (dehydrated onion/tomato or IQF) | 50 g | Flavour backbone |
| H5 | **Masala Blend A** (e.g. sambar-style) | 8 g | Recipe identity |
| H6 | **Masala Blend B** (e.g. Punjabi dal-style) | 8 g | Recipe identity |
| H7 | **Masala Blend C** (e.g. biryani/pulao) | 8 g | Recipe identity |
| H8 | Oil | 8 g | Cooking medium |
| H9 | Ghee | 2 g | Tadka finish — **quality-critical** |
| H10 | Water (metered, not a hopper — a flow-metered line) | 300 ml | Cooking + cleaning |

**Result: 9 physical hoppers + 1 metered water line.** Down from ~21.

### What you lose, and why it is acceptable

You lose the ability to let a customer dial individual spices up or down. That customisation is a *demo feature*, not a purchase driver — nobody chooses a lunch spot because they can adjust the cumin. You keep the ability to run **more** dishes, because 3 blends × 3 bases = 9 combinations, which is a full menu.

### Why this also helps food safety

Every hopper is a pest ingress point (20 lids on an unattended machine is 20 vulnerabilities) and a moisture-bridging risk. Halving the count roughly halves your contamination surface and your cleaning labour.

---

## 3. Throughput and capacity — the constraint you have to design around

Your own ratio: 10 kg rice feeds 65 people = 154 g raw rice per meal. A 15 kg rice hopper therefore holds **98 meals**.

| Target meals/day | Rice hopper refills/day | Interval in a 4-hour peak |
|---|---|---|
| 200 | 2.1 | every 117 min |
| 500 | 5.1 | every 47 min |
| 1,000 | 10.3 | every 23 min |

**Decision required (pick one, do not defer):**

- **(A) Accept 150–250 meals/day per unit.** Serve high-volume sites with a **cluster of 5–7 identical units** behind one counter, sharing one refill visit. *Recommended.* Keeps hoppers small, hygienic, and cheap; adds redundancy (if one unit is down, you still serve); scales linearly with demand.
- **(B) Redesign as a continuous bulk-feed.** ~60 kg rice bin with a level sensor and a vacuum/gravity feed. Serves 400+/day but adds bulk, a new pest-control problem, a new mechanism, and ~₹2 L of cost. Only justified for airport/campus-scale fixed installations.

**Do not** design a single unit for 1,000 meals/day and assume refills. Refilling every 23 minutes is a staffed kitchen, which defeats the entire premise.

### Cycle time budget (target ≤3 min, made to order)

| Step | Time | Notes |
|---|---|---|
| Payment + order confirm | 5 s | UPI |
| Dispense rice + water to chamber | 20 s | Auger + flow meter |
| Dal dispense | 15 s | |
| Cook rice (induction, pressure-assisted) | 90–110 s | Pre-validated recipe |
| Cook dal (induction, pressure-assisted) | 100–120 s | Runs **in parallel** with rice |
| Tadka: oil + ghee heat, blend dispense, 20 s bloom | 35 s | Last, for aroma |
| Dispense + tadka-on-top | 25 s | 3 nozzles |
| **Total (parallel cook)** | **~3 min** | Serial would be ~4.5 min |

**The parallel-cook architecture is what buys you the 3 minutes.** This is the strongest argument for your 3-chamber design — keep it, but for parallelism, not for holding.

---

## 4. The tadka system — your one genuinely novel mechanism

This is where I would put your engineering effort and your IP budget.

### The insight

A tadka is not a flavour ingredient, it is a **thermal-aromatic event**: fat heated to 160–180°C, spices added for 15–30 seconds, volatile compounds released and immediately poured over the dish. The aroma compounds (cuminaldehyde from jeera, allicin from garlic, thiosulfinates from onion) are volatile — they degrade within **20–40 minutes** of being held hot. A tadka made at 10am and held at 65°C until 1pm is a *different chemical product* from one made 30 seconds before serving.

**No existing vending machine does this.** It is a real, defensible, perceptible quality differentiator — and it is a *process* claim, which is far easier to defend than an apparatus claim.

### Mechanism sketch

```
        ┌──────────────────────────────┐
        │  Tadka cup (60ml, SS, PID)   │  ← ghee/oil from H8/H9
        │   induction coil beneath     │  ← blend from H5/H6/H7
        └───────────┬──────────────────┘
                    │  3-axis tilt (servo)
                    ▼
        ┌──────────────────────────────┐
        │  Bowl under dispense nozzle  │
        │  (rice bed + dal, already    │
        │   dispensed and levelled)    │
        └──────────────────────────────┘
```

Sequence: heat cup to 175°C (PID, ~20 s) → dispense 8 g blend into hot fat → hold 15 s (bloom) → **tilt cup and pour over the bowl** in one continuous motion, moving so the pour spreads rather than pools.

### Why this is patentable where the rest isn't

- The prior art (WO2016030906A1, US10595660B2) covers *cooking* and *dispensing*. It does not cover **timed thermal finishing at the point of dispensing**.
- It is a narrow, specific, mechanical claim — the kind that survives examination.
- It is also a **trade secret** you can keep: nobody can copy the timing and temperature profile by looking at your machine.

### Cost

Roughly **₹18–25 k** at volume: a small induction coil, a servo tilt mechanism (you already need servos elsewhere), and a 60 ml SS cup. It is the cheapest quality differentiator available to you. **Build this first.**

---

## 5. Cleaning — the thing most likely to actually fail

Your brief says steam-cleans chambers, holding chambers, and nozzles at day end. That is necessary but not sufficient, and it is the subsystem I would prototype first, because **cleaning failure is the #1 reason automated food equipment dies in the field.**

### The specific failure mode

Starch (rice) + protein (dal) + hot fat (tadka) forms a **tenacious film** on stainless steel. It polymerises with heat. Steam alone softens it but does not remove it from corners, seams, and nozzle bores. Once it builds, it:
- harbours bacteria despite the surface looking clean,
- reduces heat transfer on the cook surface,
- clogs the 3 nozzles (the narrowest points in your system),
- blinds capacitive level sensors.

### Recommended CIP sequence (per cycle, not per day)

| Step | Action | Duration |
|---|---|---|
| 1 | Scrape/flush: water at 60°C, 2 L, through chamber and nozzles | 40 s |
| 2 | Alkaline wash: food-grade NaOH 0.5%, 70°C, recirculated | 90 s |
| 3 | Rinse: potable water, 2 L | 30 s |
| 4 | **Steam sanitise** chamber + nozzle bore (this is where your boiler earns its place) | 45 s |
| 5 | Air purge + dry | 30 s |
| **Total** | | **~4 min** |

Note what this does: **it puts the steam where steam is genuinely valuable** — sanitising and reaching the nozzle bores — while removing it from the cooking path where it was costing you a pressure vessel.

### Non-negotiables

- **Nozzle bore ≥8 mm.** Anything smaller will clog with a grain of rice. Design the nozzle for the worst case, not the average.
- **No sharp internal corners** anywhere food touches. Fully welded, radiused, drainable.
- **Drain must have a strainer and a trap**, and must be inspectable without tools.
- **Daily deep clean is still required** — a 15-minute attended clean per machine per day. Budget for it in labour. "No manual intervention" is a marketing claim; "no manual intervention *during service*" is an engineering target.
- **Log every clean cycle and every temperature excursion.** This is your food-safety defence and, later, your regulatory asset.

**Cleaning is also the strongest argument for the cluster model (§3A).** One technician cleaning 6 units in one room is 6x more efficient than driving to 6 sites. Route density is economics.

---

## 6. Instrumentation — what to keep, what to cut

| Instrument | Keep? | Revised job |
|---|---|---|
| **Load cells (all hoppers)** | **Yes — core** | Portion accuracy AND **inventory tracking AND waste measurement**. This is your most valuable sensor: it makes the machine honest. |
| **Load cell (holding/dispense)** | **Yes — add** | Cooked-in minus dispensed-out = waste. Without this you cannot manage your largest variable cost. |
| **AI vision camera** | **Yes, but re-scoped** | Not doneness. Use for: (a) bowl-present confirmation, (b) spill detection, (c) nozzle obstruction detection, (d) portion fill-level. Cheaper models, simpler model, more reliable. |
| **Thermal probe / IR per chamber** | **Yes** | Core food-safety evidence: prove ≥75°C core. Log it. |
| **Capacitive level sensors** | **Yes, but** | They foul. Use load cells as primary and levels as backup, not the reverse. |
| **Gas/vapour sensor** | Optional | Nice for detecting burning, but adds cost and calibration burden. Defer to v2. |
| **Pressure/flow sensor on water** | **Yes** | Needed because you have a water line into a food machine — leak detection is a legal and insurance matter. |

**Cut:** separate doneness-vision model, per-hopper humidity sensors (use a desiccant cartridge with a scheduled replacement instead — mechanical, cheap, reliable), and any sensor whose failure produces a silent wrong answer rather than a visible fault.

### Design principle
Every sensor should fail **loudly**. A load cell that drifts silently is worse than no load cell, because it makes the machine confidently wrong. Add a nightly self-check: dispense a known test weight, verify, log.

---

## 7. Bill of materials — target cost

At **100 units** (not pilot, not 5,000). These are engineering estimates to be replaced by quotes.

| Subsystem | ₹ at 100 units | Notes |
|---|---|---|
| SS 304 enclosure + frame + panels | 1,80,000 | 35 sq ft footprint, food-grade, radiused |
| Hopper assembly ×9 (SS, airlock, auger, motor) | 2,70,000 | ₹30k each — the single biggest line |
| Auger drive motors + gearboxes ×9 | 90,000 | ₹10k each |
| Cooking chambers ×3 (induction + vessel + stirrer) | 1,35,000 | ₹45k each |
| **Tadka module (cup + mini induction + tilt servo)** | **22,000** | **Your differentiator — ringfence it** |
| Holding chambers ×2 (heated, insulated, load-celled) | 70,000 | |
| Dispensing: 3 nozzles + 3 servos + bowl handling | 55,000 | Bore ≥8 mm |
| Water system: pump, flow meter, filter, valves, drain | 30,000 | No boiler |
| CIP system: pump, tank, dosing, spray balls | 45,000 | Replaces boiler |
| Electronics: controller, 9× load cells, 3× thermal, drivers | 85,000 | |
| Display + UPI terminal + printer-less receipt | 32,000 | |
| Refrigeration (fresh component H4 only) | 28,000 | |
| Wiring, harness, contactors, safety interlocks | 55,000 | |
| Assembly, test, calibration, QA | 60,000 | |
| **BOM TOTAL** | **₹11.57 L** | |
| Margin/contingency 15% | 1.74 L | |
| **Machine cost at 100 units** | **~₹13.3 L** | |

At **500 units** expect **₹8–10 L** through volume pricing and value engineering (§2 hopper reduction is worth ~₹2.5 L of this).

At **pilot (first 5 units)** expect **₹28–35 L each** — NRE, jigs, tooling, engineering hours and rework are unamortised. **Do not confuse this with the production cost.** Founders who do, under-raise by a factor of two and run out of money exactly when it matters.

---

## 8. What to build first (ordered by information per rupee)

| Priority | Build | Cost | What it settles |
|---|---|---|---|
| 1 | **Tadka module** | ₹25 k | Is the aroma difference real and perceptible? If not, the entire differentiation thesis collapses — find out for ₹25k |
| 2 | **One chamber + one hopper + 3 min cook** | ₹1.5 L | Can you actually cook dal to good texture in 110 s? |
| 3 | **CIP on that one chamber** | ₹60 k | Does the film come off? If not, stop everything |
| 4 | **Dispense + tadka-on-top in a fake bowl** | ₹40 k | Does it plate appetisingly? This is what sells the bowl |
| 5 | **Load cell waste tracking** | ₹30 k | Can you run the machine at ≤10% waste? |
| 6 | Full integration, 1 unit | ₹8–12 L | Uptime, serviceability, real BOM |

**Total to answer the top five existential questions: ~₹3 L and 4 months.** That is one-twentieth of what a full prototype would cost, and it retires most of the risk.

---

## 9. Non-obvious engineering notes

1. **Dal is the hard one, not rice.** Dal foams during cooking and that foam carries starch into your chamber lid, vents, and sensors. Rice is forgiving. Add an antifoam dosing point or a headspace design that handles foam, or your first failure will be a jammed lid on the dal chamber.

2. **Augers ratchet on masala blends.** Fine powder compacts into the auger root and then releases in a slug. Fix with a *stepped* auger, a flexible silicone flight edge, and a dispense-by-weight closed loop rather than dispense-by-time. This is your second patent candidate.

3. **Steam + electronics in one 35 sq ft box is a corrosion problem.** Even with steam confined to CIP, humidity will find your control board. Pot the boards, positive-pressure the electronics bay, or you will be replacing controllers at 8% per year.

4. **Bowl handling is underrated.** A bowl sitting 4 mm off-centre spills. Your 3 nozzles need to hit a 120 mm target consistently after 10,000 cycles of thermal expansion. Design a *bowl-present positive-detent nest*, not an optical check.

5. **You cannot service this with a general-purpose technician.** 9 hoppers + 3 chambers + CIP + induction + controls is a two-day training course, minimum. Your route labour assumption (₹1.5 L/machine/year) assumes 15 machines per technician and that the technician can actually fix things. Test that in phase 3, not after you have 200 machines.

6. **Design for 2 persons to lift it.** A 35 sq ft food machine is heavy. If it cannot be moved through a standard office lift and door, your addressable sites collapse to ground-floor-corridor sites. **Check this before you finalise dimensions** — it is the kind of constraint that destroys a go-to-market plan.

7. **Power.** 3 induction hobs + CIP heater + holding = **3–4 kW peak**. Most office kiosk points are 1–2 kW. Budget for a dedicated 16A circuit per machine, and confirm it with the site before signing. This is a real installation cost and a real reason a site says no.
