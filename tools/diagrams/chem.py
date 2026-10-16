from lib import *
import math
D = {}

def mbf(a): return lambda E: E * math.exp(-E / a) / a**2

# 1. Maxwell–Boltzmann at two temperatures
def mb_temp():
    p = Plot(50, 30, 400, 220, (0, 8), (0, 0.4))
    b = p.axes("", "number of molecules") + [T(p.X(8), p.Y(0) + 20, "energy", "tm", "e", size=12)]
    Ea = 4.2
    b += [p.area(mbf(1.5), Ea, 8, cls="at"), p.area(mbf(1.0), Ea, 8, cls="gt")]
    b += [p.curve(mbf(1.0), 0, 8, cls="ln"), p.curve(mbf(1.5), 0, 8, cls="ac")]
    b += [L(p.X(Ea), p.Y(0), p.X(Ea), p.Y(0.3), "lm"), T(p.X(Ea) + 4, p.Y(0.3) + 4, "Eₐ", "", size=15)]
    b += [T(p.X(1.3), p.Y(0.37), "lower T", "", size=13), T(p.X(2.1), p.Y(0.255), "higher T", "ta", size=13)]
    b += [T(p.X(5.0), p.Y(0.17), "molecules with E ≥ Eₐ", "tm", size=12), L(p.X(5.4), p.Y(0.155), p.X(5.1), p.Y(0.03), "lm")]
    return svg(470, 300, b)
D["mb-temperature"] = (mb_temp(), "u05", "Effect of temperature",
  "At the higher temperature the peak is lower and further right, but the area under the curve (the number of molecules) is the same. The shaded tail beyond Eₐ is much larger, so many more collisions per second have enough energy to react.")

# 2. Maxwell–Boltzmann with a catalyst
def mb_cat():
    p = Plot(50, 30, 400, 220, (0, 8), (0, 0.4))
    b = p.axes("", "number of molecules") + [T(p.X(8), p.Y(0) + 20, "energy", "tm", "e", size=12)]
    Ea, Ec = 4.6, 2.8
    b += [p.area(mbf(1.0), Ec, 8, cls="at"), p.curve(mbf(1.0), 0, 8, cls="ln")]
    b += [L(p.X(Ea), p.Y(0), p.X(Ea), p.Y(0.28), "lm"), T(p.X(Ea) + 4, p.Y(0.28) + 4, "Eₐ without catalyst", "tm", size=12)]
    b += [L(p.X(Ec), p.Y(0), p.X(Ec), p.Y(0.33), "ac"), T(p.X(Ec) + 4, p.Y(0.33) + 4, "Eₐ with catalyst", "ta", size=13)]
    return svg(470, 300, b)
D["mb-catalyst"] = (mb_cat(), "u05", "Catalysts",
  "A catalyst doesn't change the curve. It provides a route with a lower Eₐ, so a much bigger share of the molecules (shaded) now has enough energy to react.")

# 3. Energy profile (exothermic)
def profile():
    b = []
    x0, y0 = 60, 30
    b += [L(x0, 270, x0, y0 - 8, "ln", "ah"), T(x0 + 8, y0 - 4, "enthalpy", "tm", size=12), L(x0, 270, 460, 270, "ln", "ah"), T(460, 292, "progress of reaction", "tm", "e", size=12)]
    yr, yp, ytop = 150, 230, 60
    b.append(P(f"M80,{yr} L150,{yr} C200,{yr} 210,{ytop} 250,{ytop} C290,{ytop} 300,{yp} 350,{yp} L440,{yp}", "ac"))
    b += [T(80, yr - 10, "reactants", "", size=13), T(395, yp + 22, "products", "", "m", size=13)]
    b += [L(150, yr, 270, yr, "lm"), L(250, yr, 250, ytop + 3, "ln", "ah"), T(242, 112, "Eₐ", "", "e", size=15)]
    b += [L(300, yr, 450, yr, "lm"), L(440, yr, 440, yp - 3, "gl", "ag"), T(432, 186, "ΔH", "tg", "e", size=15), T(432, 204, "(negative)", "tg", "e", size=12)]
    return svg(480, 300, b)
D["energy-profile"] = (profile(), "u04", "Enthalpy change",
  "In an exothermic reaction the products have less enthalpy than the reactants, so ΔH is negative (energy is released). Eₐ is the energy barrier between reactants and the top of the hump.")

# 4. First ionisation energy across Period 3
def ie():
    el = ["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"]
    v = [496, 738, 578, 787, 1012, 1000, 1251, 1521]
    p = Plot(70, 30, 370, 220, (0.5, 8.5), (0, 1600))
    b = p.axes("", "1st IE / kJ mol⁻¹")
    for y in (0, 400, 800, 1200, 1600): b += p.ytick(y, str(y))
    for i, e in enumerate(el): b += p.xtick(i + 1, e)
    b.append(poly([p.pt(i + 1, x) for i, x in enumerate(v)], "ac"))
    for i, x in enumerate(v): b.append(C(p.X(i + 1), p.Y(x), 4, "af"))
    b += [T(p.X(3), p.Y(578) + 22, "dip: 3p", "tg", "m", size=13), T(p.X(6) + 6, p.Y(1000) + 24, "dip: paired 3p", "tg", "m", size=13)]
    return svg(470, 290, b)
D["ie-period3"] = (ie(), "u08", "First ionisation energy across Period 3",
  "First ionisation energy rises across Period 3 as nuclear charge increases with similar shielding. It dips at Al (electron removed from 3p, higher in energy than 3s) and at S (electron removed from a paired 3p orbital, where repulsion helps).")

# 5. Melting points across Period 3
def mp():
    el = ["Na", "Mg", "Al", "Si", "P₄", "S₈", "Cl₂", "Ar"]
    v = [371, 923, 933, 1687, 317, 388, 172, 84]
    kind = ["at", "at", "at", "gt", "bx", "bx", "bx", "bx"]
    p = Plot(70, 64, 380, 200, (0.4, 8.6), (0, 1800))
    b = p.axes("", "melting point / K")
    for y in (0, 600, 1200, 1800): b += p.ytick(y, str(y))
    for i, (e, x, k) in enumerate(zip(el, v, kind)):
        X = p.X(i + 1)
        b += [R(X - 16, p.Y(x), 32, p.Y(0) - p.Y(x), k, rx=3), T(X, p.Y(0) + 20, e, "tm", "m")]
    for x, k, t, lab in [(70, "at", "ta", "metallic"), (170, "gt", "tg", "macromolecular"), (330, "bx", "tm", "simple molecular")]:
        b += [R(x, 12, 14, 14, k, rx=3), T(x + 20, 24, lab, t, size=13)]
    return svg(470, 300, b)
D["mp-period3"] = (mp(), "u08", "Melting point across Period 3",
  "Melting point depends on structure. Metallic bonding strengthens from Na to Al; silicon is macromolecular, so it is highest; P₄, S₈, Cl₂ and Ar are simple molecular, and their order follows the number of electrons (van der Waals forces).")

# 6. VSEPR shapes
def vsepr():
    b = []
    def lp(x, y, ang):
        a = math.radians(ang); cx, cy = x + 30 * math.cos(a), y - 30 * math.sin(a)
        return [f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="11" ry="6" transform="rotate({f(-ang)} {f(cx)} {f(cy)})" class="gt"/>']
    def bond(x, y, ang, L_=46):
        a = math.radians(ang); return L(x + 13 * math.cos(a), y - 13 * math.sin(a), x + L_ * math.cos(a), y - L_ * math.sin(a), "ln")
    cells = [
        ("linear", "180°", [0, 180], [], "2 bonding pairs"),
        ("trigonal planar", "120°", [90, 210, 330], [], "3 bonding pairs"),
        ("tetrahedral", "109.5°", [90, 200, 260, 340], [], "4 bonding pairs"),
        ("pyramidal", "107°", [200, 270, 340], [90], "3 bonding, 1 lone pair"),
        ("bent", "104.5°", [218, 322], [60, 120], "2 bonding, 2 lone pairs"),
        ("octahedral", "90°", [0, 90, 180, 270, 225, 45], [], "6 bonding pairs"),
    ]
    for i, (n, ang, bonds, lps, sub) in enumerate(cells):
        cx, cy = 80 + (i % 3) * 160, 70 + (i // 3) * 186
        for a in bonds: b.append(bond(cx, cy, a))
        for a in lps: b += lp(cx, cy, a)
        b.append(C(cx, cy, 13, "at"))
        for a in bonds:
            r = math.radians(a); b.append(C(cx + 54 * math.cos(r), cy - 54 * math.sin(r), 7, "bx"))
        b += [T(cx, cy + 80, f"{n} · {ang}", "", "m", size=14), T(cx, cy + 98, sub, "tm", "m", size=12)]
    return svg(480, 376, b)
D["vsepr"] = (vsepr(), "u03", "Shapes of molecules (VSEPR)",
  "Count the electron pairs round the central atom. Lone pairs (gold) repel more than bonding pairs, so each lone pair closes the bond angle by about 2.5°: 109.5° (CH₄) → 107° (NH₃) → 104.5° (H₂O). Shapes are drawn flat; the tetrahedral and octahedral ones are 3D.")

# 7. Titration curve: weak acid + strong base
def titr():
    Ka, Ca, Va, Cb = 1.74e-5, 0.100, 25.0, 0.100
    def pH(vb):
        n_a, n_b, V = Ca * Va, Cb * vb, Va + vb
        Ct, Na = n_a / V, n_b / V
        lo, hi = -14.5, 0.5
        for _ in range(80):
            m = (lo + hi) / 2; H = 10**m
            g = H + Na - 1e-14 / H - Ct * Ka / (Ka + H)
            if g > 0: hi = m
            else: lo = m
        return -m
    p = Plot(60, 30, 390, 230, (0, 40), (0, 14))
    b = p.axes("", "pH") + [T(p.X(40), p.Y(0) + 38, "volume of NaOH added / cm³", "tm", "e", size=12)]
    for y in (0, 7, 14): b += p.ytick(y, str(y))
    for x in (0, 12.5, 25, 40): b += p.xtick(x, f"{x:g}")
    b += [f'<rect x="{f(p.X(0))}" y="{f(p.Y(10))}" width="{f(p.w)}" height="{f(p.Y(8.2) - p.Y(10))}" class="at" stroke="none"/>',
          f'<rect x="{f(p.X(0))}" y="{f(p.Y(4.4))}" width="{f(p.w)}" height="{f(p.Y(3.1) - p.Y(4.4))}" class="gt" stroke="none"/>']
    b += [T(p.X(0) + 6, p.Y(9.1) + 5, "phenolphthalein 8.2–10 ✓", "ta", size=12), T(p.X(40) - 6, p.Y(3.75) + 5, "methyl orange 3.1–4.4 ✗", "tg", "e", size=12)]
    pts = [p.pt(v, pH(v)) for v in [i * 0.1 for i in range(401)]]
    b.append(poly(pts, "ln"))
    pk = pH(12.5)
    b += [C(p.X(12.5), p.Y(pk), 4, "cf"), T(p.X(12.5) + 8, p.Y(pk) + 20, f"pH = pKa = {pk:.2f}", "", size=13)]
    b += [L(p.X(12.5), p.Y(pk), p.X(12.5), p.Y(0), "lm"), L(p.X(25), p.Y(pH(25)), p.X(25), p.Y(0), "lm")]
    b += [T(p.X(26), p.Y(6), f"equivalence: pH {pH(25):.1f}", "", size=13)]
    return svg(480, 310, b), pk, pH(25)
_t = titr()
D["titration"] = (_t[0], "u21", "Titration curves and indicators",
  f"25.0 cm³ of 0.100 mol dm⁻³ ethanoic acid (Ka = 1.74 × 10⁻⁵) titrated with 0.100 mol dm⁻³ NaOH. The vertical section sits above pH 7, so phenolphthalein changes colour inside it but methyl orange doesn't. Halfway to equivalence (12.5 cm³), pH = pKa = {_t[1]:.2f}.")

# 8. Born–Haber cycle for NaCl
def bh():
    p = Plot(20, 30, 440, 340, (0, 1), (-430, 740))
    Y = p.Y
    b = []
    def bar(y, x1, x2): return L(x1, Y(y), x2, Y(y), "ln thick")
    b += [bar(0, 190, 270), T(276, Y(0) + 5, "Na(s) + ½Cl₂(g)", "", size=13)]
    b += [bar(107, 190, 270), T(276, Y(107) + 5, "Na(g) + ½Cl₂(g)", "", size=13)]
    b += [bar(229, 190, 270), T(276, Y(229) + 5, "Na(g) + Cl(g)", "", size=13)]
    b += [bar(725, 190, 450), T(190, Y(725) - 9, "Na⁺(g) + Cl(g) + e⁻", "", size=13)]
    b += [bar(376, 400, 450), T(394, Y(376) + 5, "Na⁺(g) + Cl⁻(g)", "", "e", size=13)]
    b += [bar(-411, 160, 450), T(305, Y(-411) + 22, "NaCl(s)", "", "m", size=13)]
    def up(y1, y2, lab):
        return [L(225, Y(y1), 225, Y(y2) + 2, "ln", "ah"), T(217, (Y(y1) + Y(y2)) / 2 + 5, lab, "tm", "e", size=12)]
    b += up(0, 107, "+107 atomise Na") + up(107, 229, "+122 atomise Cl") + up(229, 725, "+496 1st IE of Na")
    b += [L(425, Y(725), 425, Y(376) - 2, "ln", "ah"), T(417, Y(550) + 5, "−349 EA of Cl", "tm", "e", size=12)]
    b += [L(425, Y(376), 425, Y(-411) - 2, "ac", "aa"), T(417, Y(-200), "−787", "ta", "e", size=13), T(417, Y(-200) + 16, "lattice formation", "ta", "e", size=12)]
    b += [L(175, Y(0), 175, Y(-411) - 2, "gl", "ag"), T(167, Y(-200), "ΔfH", "tg", "e", size=13), T(167, Y(-200) + 16, "−411", "tg", "e", size=13)]
    return svg(480, 400, b)
D["born-haber"] = (bh(), "u17", "Born–Haber cycles",
  "Born–Haber cycle for NaCl, in kJ mol⁻¹, roughly to scale. Going up is endothermic and going down is exothermic. Both routes from the elements to NaCl(s) give the same total (Hess's law): 107 + 122 + 496 − 349 − 787 = −411 = ΔfH.")

# 9. Zn/Cu cell
def cell():
    b = []
    for x, lab, ion, sign in [(40, "Zn", "Zn²⁺(aq)", "−"), (300, "Cu", "Cu²⁺(aq)", "+")]:
        b += [P(f"M{x},120 L{x},260 Q{x},280 {x + 20},280 L{x + 120},280 Q{x + 140},280 {x + 140},260 L{x + 140},120", "ln")]
        b += [L(x + 6, 180, x + 134, 180, "lm"), T(x + 70, 268, ion, "tm", "m", size=13)]
        b += [R(x + 58, 80, 24, 150, "gt" if lab == "Zn" else "at", rx=2)]
    b += [T(102, 66, "Zn (−)", "", "e", size=14), T(378, 66, "Cu (+)", "", size=14)]
    b += [P("M110,80 L110,24 L370,24 L370,80", "ln"), C(240, 24, 18, "bx"), T(240, 29, "V", "", "m", size=14), T(240, 62, "1.10 V", "", "m", size=13)]
    b += [L(140, 10, 200, 10, "ac", "aa"), T(132, 14, "e⁻", "ta", "e", size=14)]
    b += [P("M150,200 L150,150 Q150,130 170,130 L310,130 Q330,130 330,150 L330,200", "ln", extra=' stroke-width="10" stroke-opacity="0.25"'), T(240, 120, "salt bridge (KNO₃)", "tm", "m", size=12)]
    b += [T(110, 312, "Zn → Zn²⁺ + 2e⁻ (oxidation)", "tg", "m", size=12), T(370, 312, "Cu²⁺ + 2e⁻ → Cu (reduction)", "ta", "m", size=12)]
    return svg(480, 324, b)
D["cell"] = (cell(), "u20", "Cells and EMF",
  "Zinc has the more negative E⦵, so it is oxidised and electrons flow through the wire from Zn to Cu. The salt bridge lets ions move to balance the charge. EMF = E(right) − E(left) = 0.34 − (−0.76) = +1.10 V. Written: Zn | Zn²⁺ || Cu²⁺ | Cu.")

# 10. Rate vs concentration for orders 0, 1, 2
def orders():
    p = Plot(60, 30, 300, 220, (0, 1), (0, 1.1))
    b = p.axes("", "rate") + [T(p.X(1), p.Y(0) + 20, "concentration", "tm", "e", size=12)]
    b += [p.curve(lambda c: 0.35, 0, 1, cls="gl"), p.curve(lambda c: 0.75 * c, 0, 1, cls="ln"), p.curve(lambda c: c * c, 0, 1, cls="ac")]
    b += [T(p.X(1) + 8, p.Y(0.35) + 5, "zero order", "tg", size=13), T(p.X(1) + 8, p.Y(0.75) + 5, "first order", "", size=13), T(p.X(1) + 8, p.Y(1.0) + 5, "second order", "ta", size=13)]
    return svg(480, 290, b)
D["rate-orders"] = (orders(), "u18", "Finding orders",
  "On a rate–concentration graph, zero order is flat (rate doesn't depend on concentration), first order is a straight line through the origin, and second order is a curve: doubling concentration quadruples the rate.")

# 11. Nucleophilic substitution mechanism
def sn():
    b = []
    b += [T(30, 118, "HO⁻", "", size=18), C(46, 96, 2.2, "cf"), C(54, 96, 2.2, "cf")]
    cx, cy = 220, 112
    b += [T(cx, cy + 6, "C", "", "m", size=18), T(cx + 6, cy - 18, "δ+", "ta", size=12)]
    b += [L(cx, cy - 12, cx, cy - 44, "ln"), T(cx, cy - 50, "H", "", "m", size=15)]
    b += [L(cx - 10, cy + 10, cx - 34, cy + 34, "ln"), T(cx - 42, cy + 50, "H", "", "m", size=15)]
    b += [L(cx, cy + 12, cx, cy + 40, "ln"), T(cx, cy + 58, "CH₃", "", "m", size=15)]
    b += [L(cx + 12, cy, cx + 58, cy, "ln"), T(cx + 64, cy + 6, "Br", "", size=18), T(cx + 90, cy - 12, "δ−", "ta", size=12)]
    b += [P(f"M52,90 C90,50 160,60 {cx - 14},{cy - 4}", "ac", "aa")]
    b += [P(f"M{cx + 34},{cy - 4} C{cx + 40},{cy - 40} {cx + 76},{cy - 40} {cx + 80},{cy - 16}", "ac", "aa")]
    b += [L(330, 112, 362, 112, "ln", "ah"), T(368, 106, "CH₃CH₂OH", "", size=15), T(368, 130, "+ Br⁻", "", size=15)]
    b += [T(30, 200, "① lone pair on OH⁻ attacks the δ+ carbon", "tm", size=12), T(30, 218, "② C–Br bond breaks; both electrons go to Br", "tm", size=12)]
    return svg(480, 228, b)
D["sn-mechanism"] = (sn(), "u13", "Nucleophilic substitution",
  "Bromoethane with hydroxide ions. The first curly arrow goes from the lone pair on OH⁻ to the δ+ carbon; the second goes from the C–Br bond to Br, which leaves as Br⁻. Each curly arrow means a pair of electrons moving.")

# 12. TLC plate
def tlc():
    b = []
    b += [R(150, 20, 150, 250, "bx", rx=4)]
    b += [L(158, 230, 292, 230, "ln", extra=' stroke-dasharray="2 4"'), T(310, 235, "origin (pencil)", "tm", size=12)]
    b += [L(158, 50, 292, 50, "lm"), T(310, 55, "solvent front", "tm", size=12)]
    b += [f'<rect x="130" y="250" width="190" height="34" class="at" stroke="none"/>', T(326, 274, "solvent below origin", "tm", size=12)]
    b += [C(200, 230, 5, "mf"), C(200, 150, 8, "af"), C(250, 230, 5, "mf"), C(250, 100, 8, "gf"), C(250, 190, 7, "af")]
    b += [L(120, 230, 120, 152, "ac", "aa"), T(112, 196, "a", "ta", "e", size=15)]
    b += [L(90, 230, 90, 52, "ln", "ah"), T(82, 146, "b", "", "e", size=15)]
    b += [T(360, 140, "Rf = a ÷ b", "", size=15), T(360, 160, "(always below 1)", "tm", size=12)]
    return svg(480, 292, b)
D["tlc"] = (tlc(), "u34", "Thin-layer chromatography (TLC)",
  "Measure both distances from the origin. Rf = distance moved by the spot (a) ÷ distance moved by the solvent front (b). The second sample here contains at least two substances.")

# 13. 1H NMR of chloroethane
def nmr():
    p = Plot(30, 40, 420, 190, (10, 0), (0, 1.2))
    b = [L(p.X(10), p.Y(0), p.X(0) + 8, p.Y(0), "ln")]
    for d in range(0, 11, 2): b += p.xtick(d, str(d))
    b += [T(p.X(5), p.Y(0) + 40, "chemical shift δ / ppm", "tm", "m", size=12)]
    def multiplet(c, ws, h, cls):
        out = []; n = len(ws); sp = 0.07
        for i, w in enumerate(ws):
            x = c + (i - (n - 1) / 2) * sp
            out.append(L(p.X(x), p.Y(0), p.X(x), p.Y(h * w / max(ws)), cls))
        return out
    b += multiplet(3.57, [1, 3, 3, 1], 0.75, "ac")
    b += multiplet(1.48, [1, 2, 1], 1.05, "gl")
    b += [L(p.X(0), p.Y(0), p.X(0), p.Y(0.25), "ln"), T(p.X(0), p.Y(0.25) - 6, "TMS", "tm", "m", size=12)]
    b += [T(p.X(3.57), p.Y(0.75) - 30, "CH₂: quartet", "ta", "m", size=13), T(p.X(3.57), p.Y(0.75) - 12, "2H, next to CH₃", "tm", "m", size=12)]
    b += [T(p.X(1.48), p.Y(1.05) - 26, "CH₃: triplet", "tg", "m", size=13), T(p.X(1.48), p.Y(1.05) - 8, "3H, next to CH₂", "tm", "m", size=12)]
    return svg(480, 290, b)
D["nmr-ethyl"] = (nmr(), "u33", "Splitting (n + 1 rule)",
  "¹H NMR of chloroethane, CH₃CH₂Cl. The CH₂ has 3 neighbouring H, so it splits into 3 + 1 = 4 (quartet); the CH₃ has 2 neighbours, so it's a triplet. The CH₂ is next to Cl, so it is further downfield (higher δ). δ runs from right to left.")
