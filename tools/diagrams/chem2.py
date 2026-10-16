from lib import *
import math
D = {}

def swatch(x, y, w, h, colour, rx=4):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" style="fill:{colour};stroke:var(--border-hi);stroke-width:1.2"/>'

def curly(d, cls="ac", mk="aa"):
    return P(d, cls, mk)

def dots(x, y, horiz=True):
    return [C(x - 4 if horiz else x, y if horiz else y - 4, 2, "cf"), C(x + 4 if horiz else x, y if horiz else y + 4, 2, "cf")]

# u01 TOF mass spectrometer
def tof():
    b = []
    b += [R(20, 70, 440, 90, "bx", rx=10)]
    stages = [(20, 110, "ionisation", "M + H⁺ → MH⁺"), (110, 200, "acceleration", "same KE"), (200, 380, "ion drift", "light ions faster"), (380, 460, "detection", "current ∝ abundance")]
    for x1, x2, n, d in stages:
        b += [T((x1 + x2) / 2, 56, n, "", "m", size=13), T((x1 + x2) / 2, 184, d, "tm", "m", size=11)]
    b += [L(110, 70, 110, 160, "lm"), L(200, 70, 200, 160, "lm"), L(380, 70, 380, 160, "lm")]
    b += [L(140, 80, 140, 150, "ln thick"), L(170, 80, 170, 150, "ln thick"), T(140, 96, "+", "", "m", size=13), T(170, 96, "−", "", "m", size=13)]
    b += [R(440, 82, 14, 66, "at", rx=3)]
    b += [C(270, 130, 9, "gt"), L(286, 130, 320, 130, "gl", "ag"), T(270, 150, "heavy", "tg", "m", size=11)]
    b += [C(340, 100, 5, "af"), L(352, 100, 432, 100, "ac", "aa"), T(340, 90, "light", "ta", "m", size=11)]
    b += [C(55, 115, 6, "af"), C(72, 120, 8, "gt"), L(210, 115, 250, 115, "ln", "ah")]
    b += [T(240, 214, "½mv² = KE, so smaller m → larger v → shorter time t = d ÷ v", "tm", "m", size=12)]
    return svg(480, 224, b)
D["tof"] = (tof(), "u01", "Time-of-flight (TOF) mass spectrometry",
  "The four stages. An electric field gives every ion the same kinetic energy, so lighter ions move faster through the drift region and reach the detector first. Each ion gains an electron at the detector, making a current.")

# u02 mole map
def molemap():
    b = []
    b += [C(240, 140, 46, "at"), T(240, 136, "moles", "ta", "m", size=16), T(240, 156, "n", "ta", "m", size=14)]
    nodes = [(80, 40, "mass (g)", "n = m ÷ Mr"), (400, 40, "number of particles", "N = n × 6.022 × 10²³"), (80, 240, "solution", "n = c × V (V in dm³)"), (400, 240, "gas", "pV = nRT (Pa, m³, K)")]
    for x, y, n, eq in nodes:
        b += [R(x - 72, y - 22, 144, 44, "bx"), T(x, y - 3, n, "", "m", size=13), T(x, y + 14, eq, "tm", "m", size=11)]
        dx, dy = 240 - x, 140 - y; d = math.hypot(dx, dy)
        x1, y1 = x + dx / d * 60, y + dy / d * 30
        x2, y2 = 240 - dx / d * 50, 140 - dy / d * 50
        b.append(L(x1, y1, x2, y2, "ln", "ah", start=True))
    return svg(480, 280, b)
D["mole-map"] = (molemap(), "u02", "Relative masses and the mole",
  "Moles are the hub: convert whatever you're given into moles, use the mole ratio from the balanced equation, then convert back. Remember the unit traps: dm³ for solutions, m³ and Pa for the gas equation.")

# u06 approach to equilibrium
def equil():
    p = Plot(60, 30, 380, 200, (0, 10), (0, 1.1))
    b = p.axes("", "concentration") + [T(p.X(10), p.Y(0) + 20, "time", "tm", "e", size=12)]
    teq = 4.5
    b += [p.curve(lambda t: 0.35 + 0.65 * math.exp(-t / 1.4), 0, 10, cls="ac"), p.curve(lambda t: 0.6 * (1 - math.exp(-t / 1.4)), 0, 10, cls="gl")]
    b += [L(p.X(teq), p.Y(0), p.X(teq), p.Y(1.05), "lm"), T(p.X(teq) + 6, p.Y(1.0), "equilibrium reached", "tm", size=12)]
    b += [T(p.X(9.8), p.Y(0.35) + 18, "reactants", "ta", "e", size=13), T(p.X(9.8), p.Y(0.6) - 8, "products", "tg", "e", size=13)]
    b += [T(p.X(7.2), p.Y(0.84), "constant, but not equal", "", "m", size=13)]
    return svg(470, 270, b)
D["equilibrium"] = (equil(), "u06", "Dynamic equilibrium",
  "In a closed system the forward rate falls and the reverse rate rises until they are equal. From then on concentrations stay constant, but they are usually not equal, and both reactions keep going.")

# u07 oxidation states number line
def oxline():
    b = []
    x0, x1 = 40, 440
    X = lambda v: x0 + (v + 1) / 8 * (x1 - x0)
    b += [L(x0 - 10, 100, x1 + 10, 100, "ln")]
    for v in range(-1, 8): b += [L(X(v), 94, X(v), 106, "ln"), T(X(v), 124, ("+" if v > 0 else "") + str(v).replace("-", "−"), "tm", "m", size=12)]
    sp = [(-1, "Cl⁻"), (0, "Cl₂"), (1, "ClO⁻"), (5, "ClO₃⁻"), (7, "ClO₄⁻")]
    for v, s in sp: b += [C(X(v), 100, 6, "af"), T(X(v), 80, s, "ta", "m", size=14)]
    b += [L(80, 160, 400, 160, "ac", "aa"), T(240, 152, "oxidation: loses electrons, state goes up", "ta", "m", size=12)]
    b += [L(400, 190, 80, 190, "gl", "ag"), T(240, 212, "reduction: gains electrons, state goes down", "tg", "m", size=12)]
    b += [T(240, 30, "oxidation states of chlorine", "", "m", size=13)]
    return svg(480, 224, b)
D["oxidation-states"] = (oxline(), "u07", "Oxidation states",
  "Chlorine can take many oxidation states. Moving right (more positive) is oxidation; moving left is reduction. In Cl₂ + 2NaOH → NaCl + NaClO + H₂O, chlorine goes both ways at once (0 → −1 and 0 → +1): disproportionation.")

# u09 Group 2 solubility
def g2sol():
    b = []
    el = ["Mg", "Ca", "Sr", "Ba"]
    b += [T(130, 26, "hydroxides M(OH)₂", "ta", "m", size=13), T(350, 26, "sulfates MSO₄", "tg", "m", size=13)]
    for i, e in enumerate(el):
        y = 50 + i * 40
        b += [T(240, y + 18, e, "", "m", size=14)]
        w1 = 30 + i * 50; w2 = 180 - i * 50
        b += [R(220 - w1, y + 4, w1, 20, "at", rx=3), R(260, y + 4, w2, 20, "gt", rx=3)]
    b += [T(130, 228, "more soluble down the group", "ta", "m", size=12), T(350, 228, "less soluble down the group", "tg", "m", size=12)]
    b += [T(184, 70, "Mg(OH)₂ sparingly soluble", "tm", "e", size=11), T(460, 194, "BaSO₄ insoluble", "tm", "e", size=11)]
    return svg(480, 240, b)
D["g2-solubility"] = (g2sol(), "u09", "Solubility",
  "The two trends run in opposite directions (bar length shows relative solubility, not to scale). Insoluble BaSO₄ is the basis of the sulfate test and of barium meals.")

# u10 halide test
def halide():
    b = []
    cols = [("Cl⁻", "#f5f5f4", "white", "dissolves", "dissolves"), ("Br⁻", "#efe2bd", "cream", "no change", "dissolves"), ("I⁻", "#f2d14b", "yellow", "no change", "no change")]
    b += [T(16, 96, "AgNO₃ (after", "", size=12), T(16, 112, "dilute HNO₃)", "", size=12), T(16, 166, "dilute NH₃", "", size=12), T(16, 216, "conc. NH₃", "", size=12)]
    for i, (ion, col, name, dil, conc) in enumerate(cols):
        x = 190 + i * 100
        b += [T(x, 40, ion, "", "m", size=16)]
        b += [swatch(x - 34, 72, 68, 34, col), T(x, 124, name, "tm", "m", size=12)]
        b += [T(x, 166, dil, "ta" if dil == "dissolves" else "tm", "m", size=12), T(x, 216, conc, "ta" if conc == "dissolves" else "tm", "m", size=12)]
    b += [L(130, 140, 460, 140, "lm"), L(130, 190, 460, 190, "lm")]
    return svg(480, 232, b)
D["halide-test"] = (halide(), "u10", "Silver nitrate test for halide ions",
  "Acidify with dilute nitric acid first (removes carbonate), then add silver nitrate. The precipitate colours are hard to tell apart, so confirm with ammonia: only AgCl dissolves in dilute NH₃; AgBr needs concentrated; AgI never dissolves.")

# u11 E/Z isomers
def ez():
    b = []
    def isomer(cx, top_right, lab, cls):
        o = [L(cx - 30, 100, cx + 30, 100, "ln"), L(cx - 30, 108, cx + 30, 108, "ln"), T(cx - 34, 109, "C", "", "e", size=15), T(cx + 34, 109, "C", "", size=15)]
        o += [L(cx - 46, 96, cx - 70, 64, "ln"), T(cx - 76, 58, "CH₃", "ta", "m", size=14)]
        o += [L(cx - 46, 112, cx - 70, 144, "ln"), T(cx - 76, 162, "H", "", "m", size=14)]
        if top_right == "CH3":
            o += [L(cx + 46, 96, cx + 70, 64, "ln"), T(cx + 76, 58, "CH₃", "ta", "m", size=14), L(cx + 46, 112, cx + 70, 144, "ln"), T(cx + 76, 162, "H", "", "m", size=14)]
        else:
            o += [L(cx + 46, 96, cx + 70, 64, "ln"), T(cx + 76, 58, "H", "", "m", size=14), L(cx + 46, 112, cx + 70, 144, "ln"), T(cx + 76, 162, "CH₃", "ta", "m", size=14)]
        o += [T(cx, 200, lab, cls, "m", size=15)]
        return o
    b += isomer(120, "CH3", "Z-but-2-ene", "ta") + isomer(360, "H", "E-but-2-ene", "tg")
    b += [T(120, 220, "CH₃ groups on the same side", "tm", "m", size=12), T(360, 220, "CH₃ groups on opposite sides", "tm", "m", size=12)]
    b += [T(240, 24, "no rotation about C=C", "tm", "m", size=12)]
    return svg(480, 232, b)
D["ez-isomers"] = (ez(), "u11", "Stereoisomerism: E/Z",
  "The C=C can't rotate, so the groups are fixed in place. On each carbon the higher-priority group (higher atomic number: C beats H) is compared. Same side = Z (zusammen); opposite sides = E (entgegen).")

# u12 fractionating column
def column():
    b = []
    b += [P("M180,30 L300,30 L300,320 L180,320 Z", "bx")]
    fr = [("refinery gases", 50), ("petrol", 95), ("naphtha", 140), ("kerosene", 185), ("diesel", 230), ("fuel oil", 275)]
    for n, y in fr:
        b += [L(300, y, 340, y, "ln", "ah"), T(346, y + 5, n, "", size=13), L(186, y + 20, 294, y + 20, "lm")]
    b += [L(120, 345, 180, 310, "ln", "ah"), T(116, 350, "crude oil", "", "e", size=13), T(116, 366, "vapour", "", "e", size=13)]
    b += [L(150, 300, 150, 50, "gl", "ag"), T(142, 60, "cooler", "tg", "e", size=12), T(142, 300, "hotter", "tg", "e", size=12)]
    b += [T(240, 22, "", "")]
    b += [T(20, 110, "short chains", "tm", size=12), T(20, 126, "(lower boiling", "tm", size=12), T(20, 142, "points) rise higher", "tm", size=12)]
    return svg(480, 372, b)
D["fractional-distillation"] = (column(), "u12", "Fractional distillation",
  "The column is hotter at the bottom. Vapour rises and each fraction condenses where the temperature falls below its boiling point. Short chains (weak van der Waals forces, low boiling points) come off near the top.")

# u14 electrophilic addition mechanism
def eadd():
    b = []
    b += [T(30, 114, "H₂C", "", size=16), L(70, 106, 110, 106, "ln"), L(70, 114, 110, 114, "ln"), T(114, 114, "CH₂", "", size=16)]
    b += [T(118, 66, "H", "", size=16), L(132, 60, 160, 42, "ln"), T(164, 42, "Br", "", size=16), T(108, 60, "δ+", "ta", "e", size=11), T(190, 34, "δ−", "ta", size=11)]
    b += [curly("M90,102 C90,76 104,70 116,66")]
    b += [curly("M146,52 C150,30 170,24 178,30")]
    b += [L(200, 110, 236, 110, "ln", "ah")]
    b += [T(246, 114, "H₃C–CH₂", "", size=16), T(318, 102, "+", "ta", size=14), T(290, 180, "Br⁻", "", size=16), C(300, 158, 2, "cf"), C(308, 158, 2, "cf")]
    b += [curly("M300,154 C300,138 310,126 312,118")]
    b += [T(262, 148, "carbocation", "tm", "e", size=11)]
    b += [L(350, 110, 386, 110, "ln", "ah"), T(392, 114, "CH₃CH₂Br", "", size=16)]
    b += [T(30, 214, "① C=C electrons attack H; H–Br breaks heterolytically", "tm", size=12), T(30, 232, "② Br⁻ lone pair attacks the carbocation", "tm", size=12)]
    return svg(480, 244, b)
D["electrophilic-addition"] = (eadd(), "u14", "Electrophilic addition",
  "Ethene with HBr. The electron-rich C=C attacks the δ+ hydrogen, and the H–Br bond breaks so both electrons go to Br. This leaves a carbocation, which the Br⁻ ion then attacks. Draw the arrows from bonds or lone pairs.")

# u15 oxidation pathways
def alcox():
    b = []
    box = lambda x, y, w, s, cls="bx", tc="": [R(x - w / 2, y - 18, w, 36, cls), T(x, y + 5, s, tc, "m", size=13)]
    b += box(70, 40, 120, "1° alcohol") + box(240, 40, 110, "aldehyde") + box(410, 40, 120, "carboxylic acid", "at", "ta")
    b += [L(130, 40, 184, 40, "ln", "ah"), T(157, 72, "distil", "tm", "m", size=12), L(296, 40, 349, 40, "ln", "ah"), T(322, 72, "reflux", "tm", "m", size=12)]
    b += box(70, 130, 120, "2° alcohol") + box(240, 130, 110, "ketone", "at", "ta")
    b += [L(130, 130, 184, 130, "ln", "ah"), T(157, 160, "reflux", "tm", "m", size=12)]
    b += box(70, 220, 120, "3° alcohol") + [T(240, 225, "✗ not oxidised (stays orange)", "tg", "start" if False else "m", size=13)]
    b += [L(130, 220, 154, 220, "lm")]
    b += [T(240, 270, "K₂Cr₂O₇ / H₂SO₄: orange Cr₂O₇²⁻ → green Cr³⁺", "", "m", size=13)]
    return svg(480, 282, b)
D["alcohol-oxidation"] = (alcox(), "u15", "Oxidation with acidified potassium dichromate(VI)",
  "Primary alcohols give an aldehyde if you distil it off as it forms, or a carboxylic acid if you heat under reflux. Secondary alcohols give ketones. Tertiary alcohols have no H on the C–OH carbon, so they aren't oxidised.")

# u16 IR spectrum
def ir():
    p = Plot(50, 30, 400, 200, (4000, 500), (0, 115))
    b = [L(p.X(4000), p.Y(0), p.X(500) + 8, p.Y(0), "ln", "ah"), L(p.X(4000), p.Y(0), p.X(4000), p.Y(115) - 8, "ln", "ah"), T(p.X(4000) + 8, p.Y(115) - 4, "transmittance %", "tm", size=12)]
    for w in (4000, 3000, 2000, 1500, 1000, 500): b += p.xtick(w, str(w))
    b += [T(p.X(500), p.Y(0) + 38, "wavenumber / cm⁻¹", "tm", "e", size=12)]
    b += [f'<rect x="{f(p.X(1500))}" y="{f(p.Y(100))}" width="{f(p.X(500) - p.X(1500))}" height="{f(p.Y(0) - p.Y(100))}" class="nt" stroke="none"/>', T(p.X(1000), p.Y(106), "fingerprint region", "tm", "m", size=12)]
    def spec(w):
        t = 92
        t -= 55 * math.exp(-((w - 2950) / 330) ** 2)
        t -= 80 * math.exp(-((w - 1710) / 28) ** 2)
        t -= 40 * math.exp(-((w - 1280) / 35) ** 2)
        for c, h in ((1420, 30), (940, 35), (1050, 25), (700, 30), (620, 25)): t -= h * math.exp(-((w - c) / 18) ** 2)
        return max(5, t)
    b.append(p.curve(spec, 4000, 500, n=600, cls="ln"))
    b += [T(p.X(2950), p.Y(30), "O–H (acid)", "ta", "m", size=13), T(p.X(2950), p.Y(30) + 16, "very broad", "ta", "m", size=11)]
    b += [T(p.X(1760), p.Y(14), "C=O 1710", "tg", "e", size=13)]
    return svg(480, 282, b)
D["ir-spectrum"] = (ir(), "u16", "Infrared spectroscopy",
  "A sketch of the IR spectrum of ethanoic acid. The very broad O–H (acid) absorption at 2500–3000 cm⁻¹ plus the sharp C=O at about 1710 cm⁻¹ show a carboxylic acid. Below 1500 cm⁻¹ is the fingerprint region, matched against a database.")

# u19 Kp worked flow
def kp():
    n1, n2, P = 0.60, 0.80, 100
    tot = n1 + n2; x1, x2 = n1 / tot, n2 / tot; p1, p2 = x1 * P, x2 * P; K = p2 ** 2 / p1
    b = []
    steps = [("equilibrium moles", f"N₂O₄ {n1:.2f}, NO₂ {n2:.2f}", f"total {tot:.2f} mol"),
             ("mole fractions", f"N₂O₄ {x1:.3f}, NO₂ {x2:.3f}", "(add up to 1)"),
             ("partial pressures", f"N₂O₄ {p1:.1f} kPa, NO₂ {p2:.1f} kPa", f"(× total {P} kPa)"),
             ("Kp = (pNO₂)² ÷ pN₂O₄", f"= {p2:.1f}² ÷ {p1:.1f} = {K:.0f} kPa", "")]
    for i, (h, a, c) in enumerate(steps):
        y = 14 + i * 74
        b += [R(30, y, 420, 56, "at" if i == 3 else "bx"), T(46, y + 22, h, "ta" if i == 3 else "", size=14), T(46, y + 42, a + ("  " + c if c else ""), "tm", size=12)]
        if i < 3: b.append(L(240, y + 58, 240, y + 72, "ln", "ah"))
    return svg(480, 310, b), K
_k = kp()
D["kp-steps"] = (_k[0], "u19", "Kp",
  f"Worked example for N₂O₄ ⇌ 2NO₂ at a total pressure of 100 kPa. Always go moles → mole fractions → partial pressures → Kp, using equilibrium amounts, not starting ones. Kp ≈ {_k[1]:.0f} kPa.")

# u22 Period 3 oxides
def oxides():
    b = []
    ox = ["Na₂O", "MgO", "Al₂O₃", "SiO₂", "P₄O₁₀", "SO₂"]
    ph = ["14", "9", "7 (insol.)", "7 (insol.)", "0", "2–3"]
    kind = ["at", "at", "nt", "gt", "gt", "gt"]
    for i, (o, h, k) in enumerate(zip(ox, ph, kind)):
        x = 50 + i * 76
        b += [R(x - 34, 60, 68, 44, k, rx=6), T(x, 87, o, "", "m", size=13), T(x, 132, h, "tm", "m", size=12)]
    b += [T(14, 132, "pH", "tm", size=12)]
    b += [T(88, 40, "ionic, basic", "ta", "m", size=13), T(202, 40, "amphoteric", "", "m", size=13), T(354, 40, "covalent, acidic", "tg", "m", size=13)]
    b += [L(20, 160, 460, 160, "ln", "ah"), T(240, 182, "ionic → covalent across the period; basic → acidic", "tm", "m", size=12)]
    b += [T(202, 210, "Al₂O₃ reacts with acids and bases", "tm", "m", size=11)]
    return svg(480, 222, b)
D["period3-oxides"] = (oxides(), "u22", "Oxides with water",
  "Across Period 3 the oxides change from ionic and basic (O²⁻ makes OH⁻ in water) to covalent and acidic. Al₂O₃ is amphoteric. Al₂O₃ and SiO₂ don't dissolve, so water stays at pH 7, but SiO₂ is still classed as acidic because it reacts with bases.")

# u23 d-orbital splitting and colour
def colour():
    b = []
    b += [T(120, 30, "free ion", "tm", "m", size=12), T(340, 30, "in a complex", "tm", "m", size=12)]
    for i in range(5): b.append(L(70 + i * 22, 130, 86 + i * 22, 130, "ln thick"))
    for i in range(2): b.append(L(330 + i * 26, 70, 348 + i * 26, 70, "ln thick"))
    for i in range(3): b.append(L(318 + i * 26, 170, 336 + i * 26, 170, "ln thick"))
    b += [L(182, 130, 300, 70, "lm"), L(182, 130, 300, 170, "lm")]
    b += [L(420, 166, 420, 76, "ac", "aa"), T(428, 125, "ΔE = hν", "ta", size=14)]
    b += [C(327, 165, 3, "cf"), L(327, 162, 340, 78, "gl", "ag"), C(340, 74, 3, "gf")]
    b += [T(240, 220, "light of energy ΔE is absorbed (an electron is promoted);", "tm", "m", size=12), T(240, 238, "the colour seen is the complementary colour, transmitted", "tm", "m", size=12)]
    return svg(480, 250, b)
D["d-splitting"] = (colour(), "u23", "Colour",
  "Ligands split the d orbitals into two energy levels. An electron absorbs visible light of exactly ΔE = hν to jump up; we see the remaining (complementary) colours. Changing the ligand, co-ordination number or oxidation state changes ΔE, so the colour changes.")

# u24 aqua ions with NaOH / NH3 / Na2CO3
def aqua():
    b = []
    ions = ["Cu²⁺", "Fe²⁺", "Fe³⁺", "Al³⁺"]
    cols = [["#4f8fe0", "#4f8fe0", "#4f8fe0", "#3fa7a0"], ["#5a7d3a", "#5a7d3a", "#5a7d3a", "#5a7d3a"], ["#8b4a1f", "#8b4a1f", "#8b4a1f", "#8b4a1f"], ["#f5f5f4", None, "#f5f5f4", "#f5f5f4"]]
    excess = [["", "", "deep blue solution", ""], ["", "", "", ""], ["", "", "", "+ CO₂ fizz"], ["", "dissolves", "", "+ CO₂ fizz"]]
    heads = [("NaOH", ""), ("excess", "NaOH"), ("excess", "NH₃"), ("Na₂CO₃", "")]
    for j, (h1, h2) in enumerate(heads): b += [T(150 + j * 92, 18 if h2 else 26, h1, "", "m", size=12), T(150 + j * 92, 33, h2, "", "m", size=12)]
    for i, ion in enumerate(ions):
        y = 44 + i * 58
        b.append(T(30, y + 26, ion, "", "m", size=15))
        for j in range(4):
            x = 150 + j * 92
            c = cols[i][j]
            if (i, j) == (0, 2): c = "#1f3fa8"
            if c: b.append(swatch(x - 30, y + 4, 60, 30, c))
            else: b.append(R(x - 30, y + 4, 60, 30, "lm", rx=4))
            if excess[i][j]: b.append(T(x, y + 50, excess[i][j], "tm", "m", size=10))
    b.append(T(240, 290, "Fe(OH)₂ (green) slowly turns brown in air", "tm", "m", size=11))
    return svg(480, 300, b)
D["aqua-ions"] = (aqua(), "u24", "Reactions with NaOH and NH₃ (hydrolysis)",
  "Swatches show the precipitate colours (an empty box means it dissolved). Only Al(OH)₃ dissolves in excess NaOH (amphoteric). Only Cu(OH)₂ dissolves in excess NH₃, giving deep blue [Cu(NH₃)₄(H₂O)₂]²⁺. The 3+ ions are acidic enough to give a hydroxide and CO₂ with carbonate; Cu²⁺ and Fe²⁺ give carbonates.")

# u25 enantiomers
def enant():
    b = []
    def tetra(cx, mirror):
        s = -1 if mirror else 1
        o = [T(cx, 125, "C", "", "m", size=17)]
        o += [L(cx, 108, cx, 64, "ln"), T(cx, 56, "H", "", "m", size=15)]
        o += [poly([(cx + s * 10, 128), (cx + s * 52, 150), (cx + s * 46, 160)], "cf", closed=True), T(cx + s * 70, 168, "OH", "ta", "m", size=15)]
        for k in range(5):
            t = (k + 1) / 6
            xa, ya = cx - s * (8 + t * 40), 128 + t * 24
            o.append(L(xa - s * 0, ya - t * 6, xa, ya + t * 6, "ln"))
        o += [T(cx - s * 66, 172, "CH₃", "", "m", size=15)]
        o += [L(cx, 132, cx, 180, "ln"), T(cx, 200, "C₂H₅", "", "m", size=15)]
        return o
    b += tetra(130, False) + tetra(350, True)
    b += [L(240, 30, 240, 220, "lm"), T(240, 240, "mirror", "tm", "m", size=12)]
    b += [T(240, 22, "butan-2-ol", "", "m", size=13)]
    return svg(480, 250, b)
D["enantiomers"] = (enant(), "u25", "Chirality",
  "Butan-2-ol: the central carbon has four different groups (H, OH, CH₃, C₂H₅), so it is chiral. The two enantiomers are mirror images that can't be superimposed. Wedge = towards you; hashed = away.")

# u26 nucleophilic addition mechanism
def nadd():
    b = []
    b += [T(30, 100, "H₃C", "", size=16), L(70, 95, 96, 95, "ln"), T(100, 101, "C", "", size=16), T(106, 128, "H", "", size=15), L(106, 104, 106, 112, "ln")]
    b += [L(114, 88, 140, 66, "ln"), L(119, 93, 145, 71, "ln"), T(146, 64, "O", "", size=16), T(166, 58, "δ−", "ta", size=11), T(100, 82, "δ+", "ta", "e", size=11)]
    b += [T(40, 170, "⁻:CN", "", size=16), curly("M60,154 C70,130 88,120 100,108")]
    b += [curly("M128,76 C132,52 150,44 156,50")]
    b += [L(200, 100, 236, 100, "ln", "ah")]
    b += [T(250, 104, "CH₃–C(H)(CN)–O⁻", "", size=15), T(300, 160, "H⁺", "", size=16), curly("M384,98 C400,130 360,170 318,160")]
    b += [L(250, 200, 286, 200, "ln", "ah"), T(296, 205, "CH₃CH(OH)CN", "", size=15)]
    b += [T(30, 232, "racemic: CN⁻ attacks the planar C=O from either side", "tm", size=12)]
    return svg(480, 244, b)
D["nucleophilic-addition"] = (nadd(), "u26", "Nucleophilic addition of HCN",
  "Ethanal with KCN then acid. CN⁻ attacks the δ+ carbon and the C=O π electrons move onto oxygen, giving an O⁻ intermediate, which picks up H⁺. The C=O is planar, so attack from either side is equally likely: a racemic mixture forms.")

# u27 addition–elimination
def addelim():
    b = []
    b += [T(20, 104, "H₃C", "", size=16), L(58, 99, 84, 99, "ln"), T(88, 105, "C", "", size=16)]
    b += [L(100, 92, 124, 70, "ln"), L(105, 97, 129, 75, "ln"), T(130, 68, "O", "", size=16)]
    b += [L(100, 110, 124, 132, "ln"), T(126, 146, "Cl", "", size=16)]
    b += [T(28, 176, "H₂O", "", size=16), C(44, 158, 2, "cf"), C(52, 158, 2, "cf"), curly("M50,154 C60,134 76,122 88,112")]
    b += [curly("M114,80 C118,56 136,50 140,56")]
    b += [L(170, 104, 204, 104, "ln", "ah"), T(187, 124, "addition", "tm", "m", size=11)]
    cx = 270
    b += [T(cx - 14, 108, "H₃C–", "", "e", size=15), T(cx, 108, "C", "", size=16), L(cx + 14, 102, cx + 36, 102, "ln"), T(cx + 40, 108, "O⁻", "", size=16)]
    b += [L(cx + 6, 112, cx + 6, 136, "ln"), T(cx - 2, 154, "Cl", "", size=16), L(cx + 6, 92, cx + 6, 72, "ln"), T(cx - 6, 66, "⁺OH₂", "", size=15)]
    b += [curly(f"M{cx + 52},96 C{cx + 52},74 {cx + 30},74 {cx + 20},96")]
    b += [curly(f"M{cx + 14},122 C{cx + 34},132 {cx + 36},148 {cx + 22},152")]
    b += [L(346, 104, 378, 104, "ln", "ah"), T(362, 124, "elimination", "tm", "m", size=11)]
    b += [T(388, 100, "CH₃COOH", "", size=15), T(388, 144, "+ HCl", "", size=15)]
    b += [T(20, 214, "① lone pair adds to the δ+ carbon; C=O opens", "tm", size=12), T(20, 232, "② C=O reforms, Cl⁻ leaves, then H⁺ is lost (HCl)", "tm", size=12)]
    return svg(480, 244, b)
D["addition-elimination"] = (addelim(), "u27", "Acyl chlorides and acid anhydrides",
  "Ethanoyl chloride with water. Addition: the lone pair on water's O attacks the δ+ carbon and the C=O opens. Elimination: the C=O reforms, Cl⁻ leaves, and H⁺ is lost, giving HCl. Alcohols, ammonia and amines react the same way.")

# u28 nitration mechanism
def nitration():
    b = []
    def benz(cx, cy, full=True, plus=False):
        r = 30
        pts = [(cx + r * math.cos(math.radians(90 + 60 * i)), cy - r * math.sin(math.radians(90 + 60 * i))) for i in range(6)]
        o = [poly(pts, "ln", closed=True)]
        if full: o.append(C(cx, cy, 17, "ln"))
        else:
            o.append(P(f"M{f(cx - 15)},{f(cy - 8)} A17,17 0 1 0 {f(cx + 15)},{f(cy - 8)}", "ln"))
            o.append(T(cx, cy + 6, "+", "", "m", size=14))
        return o
    b += benz(70, 120)
    b += [T(130, 66, "NO₂⁺", "", size=15), curly("M84,108 C96,88 110,76 128,70")]
    b += [L(170, 120, 200, 120, "ln", "ah")]
    b += benz(260, 120, full=False)
    b += [L(260, 90, 246, 66, "ln"), T(240, 62, "H", "", "e", size=14), L(260, 90, 276, 66, "ln"), T(278, 62, "NO₂", "", size=14)]
    b += [curly("M252,78 C252,92 256,98 258,104")]
    b += [L(316, 120, 346, 120, "ln", "ah")]
    b += benz(400, 120) + [L(400, 90, 400, 66, "ln"), T(400, 58, "NO₂", "", "m", size=14), T(440, 168, "+ H⁺", "", size=14)]
    b += [T(30, 200, "① ring electrons attack NO₂⁺ (delocalisation partly lost)", "tm", size=12), T(30, 218, "② C–H electrons return to the ring; H⁺ leaves", "tm", size=12)]
    b += [T(70, 180, "benzene", "tm", "m", size=11), T(260, 180, "intermediate", "tm", "m", size=11)]
    return svg(480, 230, b)
D["nitration"] = (nitration(), "u28", "Electrophilic substitution",
  "Nitration of benzene. The delocalised electrons attack the NO₂⁺ electrophile, giving an intermediate with a horseshoe (part of the ring) and a + charge; H and NO₂ are on the same carbon. Losing H⁺ restores the stable delocalised ring.")

# u29 base strength
def bases():
    b = []
    items = [("CH₃CH₂–NH₂", "ethylamine", "ethyl group pushes electrons onto N", "strongest", "ta", "at"),
             ("H–NH₂", "ammonia", "reference", "", "", "bx"),
             ("C₆H₅–NH₂", "phenylamine", "N lone pair delocalised into the ring", "weakest", "tg", "gt")]
    for i, (f_, n, why, rank, tc, cls) in enumerate(items):
        y = 20 + i * 76
        b += [R(20, y, 440, 58, cls), T(40, y + 26, f_, tc, size=16), T(40, y + 46, n, "tm", size=12), T(440, y + 24, rank, tc, "e", size=13), T(440, y + 44, why, "tm", "e", size=12)]
    b += [L(468, 30, 468, 220, "ln", "ah")]
    return svg(480, 248, b)
D["base-strength"] = (bases(), "u29", "Base properties",
  "Base strength depends on how available the lone pair on nitrogen is to accept H⁺. Alkyl groups push electron density onto N (stronger base). In phenylamine the lone pair is delocalised into the benzene ring (weaker base).")

# u30 condensation polymerisation
def condpoly():
    b = []
    b += [T(20, 40, "HOOC(CH₂)₄COOH", "", size=15), T(270, 40, "H₂N(CH₂)₆NH₂", "", size=15)]
    b += [T(20, 62, "dicarboxylic acid", "tm", size=12), T(270, 62, "diamine", "tm", size=12), T(236, 44, "+", "", "m", size=16)]
    b += [L(240, 80, 240, 116, "ln", "ah"), T(250, 102, "− H₂O for every link", "ta", size=12)]
    b += [T(240, 150, "–[ CO(CH₂)₄CO–NH(CH₂)₆NH ]ₙ–", "", "m", size=16)]
    b += [R(222, 130, 54, 30, "lm", rx=4), T(249, 180, "amide link", "ta", "m", size=13)]
    b += [T(240, 214, "e.g. hexanedioic acid + hexane-1,6-diamine → nylon-6,6", "tm", "m", size=12)]
    return svg(480, 226, b)
D["condensation-polymer"] = (condpoly(), "u30", "Condensation polymers",
  "Each monomer has two functional groups, so chains grow in both directions. Every amide (–CONH–) or ester (–COO–) link that forms releases a small molecule, usually water. The repeat unit contains one of each monomer.")

# u31 amino acid forms with pH
def aminoph():
    b = []
    forms = [("H₃N⁺–CHR–COOH", "low pH (acid)", "overall +", "ac"), ("H₃N⁺–CHR–COO⁻", "isoelectric point", "zwitterion, no overall charge", "ln"), ("H₂N–CHR–COO⁻", "high pH (alkali)", "overall −", "gl")]
    for i, (fm, cond, ch, cls) in enumerate(forms):
        y = 30 + i * 80
        b += [R(80, y, 320, 54, "at" if i == 0 else ("gt" if i == 2 else "bx")), T(240, y + 24, fm, "", "m", size=16), T(240, y + 44, f"{cond}: {ch}", "tm", "m", size=12)]
    b += [L(410, 84, 410, 110, "ln", "ah"), T(418, 102, "+OH⁻", "", size=12), L(410, 164, 410, 190, "ln", "ah"), T(418, 182, "+OH⁻", "", size=12)]
    b += [L(70, 110, 70, 84, "ln", "ah"), T(62, 102, "+H⁺", "", "e", size=12), L(70, 190, 70, 164, "ln", "ah"), T(62, 182, "+H⁺", "", "e", size=12)]
    return svg(480, 280, b)
D["amino-acid-ph"] = (aminoph(), "u31", "Amino acids",
  "In acid, the COO⁻ group picks up H⁺, so the amino acid is positive. In alkali, the NH₃⁺ loses H⁺, so it is negative. At the isoelectric point it is a zwitterion with no overall charge, which is why amino acids have high melting points.")

# u32 synthesis map
def synth():
    b = []
    pos = {"alkane": (65, 34), "halo": (240, 34), "alkene": (415, 34), "nitrile": (65, 144), "alcohol": (240, 144), "ketone": (415, 144),
           "amine": (65, 254), "aldehyde": (240, 254), "acid": (415, 254), "hydroxy": (240, 364), "ester": (415, 364)}
    names = {"alkane": "alkane", "halo": "halogenoalkane", "alkene": "alkene", "nitrile": "nitrile", "alcohol": "1°/2° alcohol", "ketone": "ketone",
             "amine": "primary amine", "aldehyde": "aldehyde", "acid": "carboxylic acid", "hydroxy": "hydroxynitrile", "ester": "ester"}
    HW = 58
    hw = lambda k: 68 if k == "halo" else HW
    for k, (x, y) in pos.items():
        b += [R(x - hw(k), y - 16, 2 * hw(k), 32, "at" if k in ("halo", "alcohol") else "bx"), T(x, y + 5, names[k], "ta" if k in ("halo", "alcohol") else "", "m", size=11)]
    def ar(a, c, off=(0, 0)):
        x1, y1 = pos[a]; x2, y2 = pos[c]
        dx, dy = x2 - x1, y2 - y1
        if abs(dy) < 1: s_ = (x1 + hw(a) * (1 if dx > 0 else -1), y1 + off[1]); e = (x2 - (hw(c) + 2) * (1 if dx > 0 else -1), y2 + off[1])
        elif abs(dx) < 1: s_ = (x1 + off[0], y1 + 16 * (1 if dy > 0 else -1)); e = (x2 + off[0], y2 - 18 * (1 if dy > 0 else -1))
        else:
            d = math.hypot(dx, dy); s_ = (x1 + dx / d * 46, y1 + dy / d * 22); e = (x2 - dx / d * 52, y2 - dy / d * 24)
        return [L(*s_, *e, "ln", "ah")]
    lab = lambda x, y, t, a="m": T(x, y, t, "tm", a, size=10)
    b += ar("alkane", "halo") + [lab(148, 24, "Cl₂, UV")]
    b += ar("alkene", "halo", (0, -6)) + [lab(340, 20, "HBr")] + ar("halo", "alkene", (0, 6)) + [lab(300, 66, "KOH, ethanol")]
    b += ar("halo", "nitrile") + [lab(126, 92, "KCN, ethanol", "e")]
    b += ar("halo", "alcohol") + [lab(246, 94, "NaOH(aq)", "start")]
    b += ar("alkene", "alcohol") + [lab(340, 104, "steam, H₃PO₄", "start")]
    b += ar("nitrile", "amine") + [lab(71, 204, "LiAlH₄", "start")]
    b += ar("alcohol", "aldehyde", (-6, 0)) + [lab(228, 196, "Cr₂O₇²⁻/H⁺, distil", "e")] + ar("aldehyde", "alcohol", (6, 0)) + [lab(252, 196, "NaBH₄", "start")]
    b += ar("alcohol", "ketone") + [lab(332, 168, "Cr₂O₇²⁻/H⁺ (2°)")]
    b += ar("aldehyde", "acid") + [lab(327, 284, "Cr₂O₇²⁻/H⁺, reflux")]
    b += ar("acid", "ester") + [lab(405, 306, "alcohol,", "e"), lab(405, 320, "conc. H₂SO₄", "e")]
    b += ar("aldehyde", "hydroxy") + [lab(246, 314, "KCN, then H⁺", "start")]
    return svg(480, 386, b)
D["synthesis-map"] = (synth(), "u32", "Key aliphatic interconversions",
  "The main aliphatic routes with their reagents. Learn the conditions as well as the reagents: aqueous NaOH gives an alcohol but ethanolic KOH gives an alkene. Only the CN⁻ steps add a carbon atom to the chain.")
