# Flight 001 — Physics and numerical results (independent toy calculations)

Run: python3 model.py --milestones; python3 model.py --cycle 132
Tests: python3 -m unittest discover -s tests -v

## 1. Exact arithmetic [MATH under assumptions A]
After n completed cycles (300 seconds/cycle):
- N(n) = 2^n
- M(n) = 0.05 * 2^n kg
- t = 300 n seconds
- At 1 h (n=12): 4,096 objects; 204.8 kg
- At 2 h (n=24): 16,777,216 objects; 838,860.8 kg
- New 50 g rest-mass energy equivalent m c^2 = approx 4.4938e15 J (average 1.4979e13 W over first 300 s). This does NOT imply that this energy becomes local heat or an explosion.

## 2. Independent threshold table [MODEL]
Columns: condition | first cycle | time since start
- 10 L uniform-density occupancy exceeded | 8 | 00:40
- Earth mass (5.9722e24 kg) exceeded | 87 | 07:15
- Solar mass (1.98847e30 kg) exceeded | 105 | 08:45
- Uniform sphere R <= Schwarzschild radius | 132 | 11:00
- Uniform sphere radius R > c*t in Minkowski space | 148 | 12:20

Conventions: first event when the strict inequality is satisfied, except compactness threshold uses R <= Rs. Report is a chain of **different conditional comparisons**, NOT a history of a physically plausible evolving object. In particular the flat-light-cone scenario ignores severe self-gravity well before n=148. These thresholds cannot all hold in one self-consistent classical model.

## 3. Uniform sphere & Newtonian compression [MODEL C]
At effective density rho = 1000 kg/m^3:
- V = M/rho
- R = (3 M / (4 pi rho))^(1/3)
- Newtonian uniform self-gravitating sphere central pressure:
  p_center = (2 pi / 3) G rho^2 R^2
Representative results:
- n=48, 4 h: R≈1.50 km, p≈314 Pa
- n=60, 5 h: R≈23.96 km, p≈80,276 Pa
- n=66, 5h30: R≈95.86 km, p≈1.28 MPa
- n=72, 6h: R≈383.42 km, p≈20.6 MPa
Caution: pressure comparison is NOT a material-failure time. The real object is not uniform-density hydrostatic fluid under exponential creation. Oxygen-poor surroundings also do not guarantee chemical combustion.

## 4. Schwarzschild compactness [MODEL C, NOT dynamic GR]
Rs = 2GM/c^2, applicable as an important scale in spherically symmetric GR. At n=132, M≈2.7223e38 kg (~136.9 million solar masses); R≈4.0205e11 m; Rs≈4.0432e11 m.
Crossing the algebraic ratio Rs/R=1 under an imposed constant rho **does not** calculate when a realistic black hole forms. To determine that requires spacetime-dependent stress-energy, expansion/transport, pressure/temperature, and GR evolution; ordinary hydrostatic Newtonian pressure is invalid by this regime.
References: NASA GSFC https://imagine.gsfc.nasa.gov/science/objects/black_holes2.html ; OpenStax https://openstax.org/books/astronomy/pages/24-5-black-holes

## 5. Flat spacetime causal-volume contradiction [MODEL D; finite initial radius]
Local propagation from one origin cannot populate events outside its future light cone at t. Bound occupied volume (without overlapping finite-volume copies) by a ball of radius **r0 + c*t** in flat space, where r0 = (3 m0/(4πρ))^(1/3) is the spherical-equivalent initial object radius. If all copies have fixed volume v0 = 0.05/1000 m^3, required ball radius grows as R(n) ~ 2^(n/3), whereas ct grows linearly in n. At n=147 (12h15): R≈86.0 AU vs (r0+ct)≈88.38 AU. At n=148 (12h20): R≈108.35 AU vs (r0+ct)≈88.98 AU. Default r0 is tiny relative to astronomical distances; crossing cycle stays n=148.
This shows the *assumptions* are jointly incompatible indefinitely. It does NOT prove a physical explosion or describe an expanding FRW universe. Curved spacetime, strong gravity and nonlocal fictional replication invalidate this simple construction.
NASA cosmology overview: https://science.nasa.gov/universe/overview/

## 6. Event-horizon to r=0 test-particle proper time [MODEL E]
Fixed Schwarzschild mass M, freely falling test particle starting at rest at infinity (specific energy 1): from horizon to r=0 its remaining proper time is 4GM/(3c^3). For M = 100 million solar masses, about 657 s (~10.95 min). Two complete 300 s intervals fit **if the cycle timer starts afresh at horizon passage**; up to **three scheduled births** can occur if the clock's phase at crossing is 270 s (births at +30 s, +330 s, +630 s). Phase and survivability are unspecified.
Different infall initial conditions yield different proper times. The probe is NOT a simulation of a multiplying extended food object. **An inward light signal emitted outside can cross the future event horizon and meet an infaller inside**; only outbound signals from inside cannot reach distant observers. Sol reported an illustrative meeting at ≈206 s of infaller proper time, not independently reproduced here.

## 7. Unsolved physical closure
Heat generation requires velocities, material properties and a specified replication process. Creation of rest mass requires accounting for a source or explicit new physics. State transitions after fragmentation, ingestion, phase change, or event-horizon crossing are undefined. Do not claim any single termination mechanism as proved.


## 8. Local parent-child placement bound [MODEL G, reported by Sol; unit-tested arithmetic]
Assume each parent is fixed in position, each birth may place its child center no farther than **one full bun diameter** (2r0) from the parent, all buns remain full nonoverlapping spheres, and the very first center is at the origin. After n generations the outermost surface is contained in a sphere of radius \`(2n+1)r0\`. A best-case volume upper bound for count is \`(2n+1)^3\`, already overly generous because it ignores packing gaps.
At n=14, 16,384 <= 29³=24,389; at n=15, 32,768 > 31³=29,791. Thus this **specific fixed-parent local-placement model** is inconsistent by 75 minutes, even with empty space outside the reachable shell. This is neither a claim about canonical magic nor a theorem for freely moving parents or long-distance placement.

## 9. Model compatibility warning [MATH/MODEL separation]
The flat-space constraint uses a Minkowski background with bounded local creation; the compactness indicator uses large self-gravity. It would be physically inconsistent to treat both as simultaneous accurate predictions. Under a substantially evolving mass-energy budget, background spacetime cannot simply remain Minkowski. The fixed Schwarzschild geodesic calculation presumes an unchanging background, and is not valid unchanged while huge new mass is created.
