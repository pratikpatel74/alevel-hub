from lib import *
import math
D = {}

# 1. Heart and double circulation
def heart():
    b = []
    b += [R(150, 8, 180, 40, "bx"), T(240, 33, "Lungs", "", "m")]
    b += [R(150, 336, 180, 40, "bx"), T(240, 361, "Body cells", "", "m")]
    # chambers (person's right side drawn on the left)
    b += [R(60, 112, 110, 78, "bx"), T(115, 156, "RA", "", "m")]
    b += [R(60, 198, 170, 104, "bx"), T(115, 255, "RV", "", "m")]
    b += [R(310, 112, 110, 78, "bx"), T(365, 156, "LA", "", "m")]
    b += [R(250, 198, 170, 104, "at", extra=' stroke-width="4.5"'), T(365, 255, "LV", "ta", "m")]
    b += [L(240, 112, 240, 302, "ln thick"), T(240, 322, "septum", "tm", "m")]
    # deoxygenated route (gold)
    b += [poly([(150, 356), (30, 356), (30, 150), (58, 150)], "gl", "ag")]
    b += [T(22, 262, "vena cava", "tg", "m", rot=-90)]
    b += [L(115, 176, 115, 222, "gl", "ag")]
    b += [poly([(200, 230), (200, 52)], "gl", "ag"), T(193, 80, "pulmonary", "tg", "e", size=13), T(193, 96, "artery", "tg", "e", size=13)]
    # oxygenated route (accent)
    b += [poly([(395, 280), (395, 356), (334, 356)], "ac", "aa")]
    b += [T(403, 330, "aorta", "ta", size=13)]
    b += [poly([(330, 28), (365, 28), (365, 108)], "ac", "aa")]
    b += [T(373, 50, "pulmonary vein", "ta", size=13)]
    b += [L(365, 176, 365, 222, "ac", "aa")]
    # valves: short bars where blood leaves each chamber
    for x1, x2, y in [(95, 135, 194), (345, 385, 194), (186, 214, 200), (381, 409, 314)]:
        b.append(L(x1, y, x2, y, "ln", extra=' stroke-width="3" stroke-dasharray="6 5"'))
    return svg(480, 384, b)
D["heart"] = (heart(), "u10", "The heart and the cardiac cycle",
  "Drawn as if facing the person, so the right side of the heart is on the left. **Gold**: deoxygenated blood, body → vena cava → RA → RV → pulmonary artery → lungs. **Accent**: oxygenated blood, lungs → pulmonary vein → LA → LV → aorta → body. Dashed bars are the valves. The left ventricle wall is thickest because it pumps blood round the whole body.")

# 2. Oxygen dissociation curves
def odc():
    p = Plot(70, 30, 370, 250, (0, 14), (0, 100))
    S = lambda P50: (lambda x: 100 * x**2.7 / (x**2.7 + P50**2.7))
    b = p.axes("pO₂ / kPa", "% saturation")
    for x in (0, 2, 4, 6, 8, 10, 12, 14): b += p.xtick(x, str(x))
    for y in (0, 50, 100): b += p.ytick(y, str(y))
    b += [L(p.X(4), p.Y(0), p.X(4), p.Y(100), "lm"), T(p.X(4) + 6, p.Y(6), "respiring tissue", "tm", size=12)]
    b += [p.curve(S(2.3), 0, 14, cls="gl"), p.curve(S(3.4), 0, 14, cls="ln thick" if False else "ln"), p.curve(S(4.8), 0, 14, cls="ac")]
    for i, (cls, tcls, lab) in enumerate([("gl", "tg", "higher affinity (fetal)"), ("ln", "", "adult"), ("ac", "ta", "more CO₂ (Bohr effect)")]):
        y = p.Y(40 - i * 11)
        b += [L(p.X(6.2), y - 4, p.X(7.2), y - 4, cls), T(p.X(7.5), y + 1, lab, tcls, size=13)]
    return svg(470, 320, b)
D["odc"] = (odc(), "u10", "Oxygen dissociation curves",
  "At the pO₂ of respiring tissue (dashed line), the right-shifted curve is much lower, so haemoglobin with **lower affinity has unloaded more O₂**. A left-shifted curve loads O₂ at low pO₂, which suits a fetus or an animal in low-oxygen mud.")

# 3. Nephron
def nephron():
    b = []
    b += [L(10, 140, 470, 140, "lm"), T(470, 132, "cortex", "tm", "e", size=13), T(470, 158, "medulla", "tm", "e", size=13)]
    b += [T(10, 380, "ψ lowest", "tm", size=12), T(10, 364, "deepest:", "tm", size=12)]
    b += [C(62, 70, 30, "ln"), C(62, 70, 15, "at"), T(62, 22, "Bowman's capsule", "tm", "m", size=12), T(62, 120, "glomerulus", "ta", "m", size=12)]
    b += [P("M92,70 C105,50 115,50 125,70 S145,90 155,70 S175,50 190,66 L200,76", "ln thick")]
    b += [T(145, 40, "PCT", "", "m")]
    b += [P("M200,76 L200,330 Q200,352 220,352 Q240,352 240,330 L240,96", "ln thick")]
    b += [P("M240,96 C255,76 265,76 275,96 S295,116 305,96 S325,76 340,92 L380,92", "ln thick"), T(300, 72, "DCT", "", "m")]
    b += [L(380, 40, 380, 390, "ln thick", "ah"), T(392, 52, "collecting", "", size=13), T(392, 68, "duct", "", size=13)]
    b += [L(380, 40, 380, 92, "ln thick")]
    # flows
    b += [L(196, 210, 160, 210, "ac", "aa"), L(196, 270, 160, 270, "ac", "aa"), T(155, 215, "H₂O", "ta", "e", size=13), T(155, 275, "H₂O", "ta", "e", size=13)]
    b += [L(244, 190, 286, 190, "gl", "ag"), L(244, 250, 286, 250, "gl", "ag"), T(292, 195, "Na⁺ Cl⁻", "tg", size=13), T(292, 255, "Na⁺ Cl⁻", "tg", size=13)]
    b += [L(384, 230, 420, 230, "ac", "aa"), L(384, 300, 420, 300, "ac", "aa"), T(424, 235, "H₂O", "ta", size=13), T(424, 305, "H₂O", "ta", size=13), T(424, 320, "(ADH)", "tm", size=12)]
    b += [T(220, 378, "loop of Henle", "", "m", size=13)]
    b += [T(250, 160, "impermeable", "tm", size=12), T(250, 174, "to water", "tm", size=12)]
    return svg(480, 400, b)
D["nephron"] = (nephron(), "u24", "Loop of Henle",
  "The ascending limb pumps Na⁺ and Cl⁻ into the medulla but lets no water out, so the medulla's water potential falls, most of all at the bottom. Water then leaves the descending limb and the collecting duct by osmosis. ADH inserts aquaporins in the collecting duct, so more water leaves.")

# 4. Sarcomere relaxed vs contracted
def sarc(y, zl, zr, label):
    b = [T(10, y - 30, label, "", size=13)]
    for z in (zl, zr): b.append(L(z, y - 22, z, y + 42, "ln thick"))
    for dy in (-12, 0, 32, 44 - 24):
        pass
    for dy in (-12, 32):
        b.append(L(zl, y + dy, zl + 150, y + dy, "ln"))
        b.append(L(zr, y + dy, zr - 150, y + dy, "ln"))
    b.append(R(140, y - 4, 200, 26, "at", rx=4))
    return b
def sarcomere():
    b = []
    b += sarc(60, 40, 440, "Relaxed")
    b += sarc(230, 90, 390, "Contracted")
    # brackets
    def br(x1, x2, y, lab, cls="tm"):
        return [L(x1, y, x2, y, "ln" if cls != "ta" else "ac"), L(x1, y - 5, x1, y + 5, "ln" if cls != "ta" else "ac"), L(x2, y - 5, x2, y + 5, "ln" if cls != "ta" else "ac"), T((x1 + x2) / 2, y + 18, lab, cls, "m", size=13)]
    b += br(140, 340, 122, "A-band", "ta") + br(40, 140, 122, "½ I-band") + br(190, 290, 22 - 2, "H-zone")
    b += br(140, 340, 292, "A-band (same length)", "ta") + br(90, 140, 292, "½ I")
    b += [T(240, 196, "H-zone gone", "tm", "m", size=12)]
    b += [T(440, 26, "Z-line", "tm", "m", size=12), T(240, 330, "actin = thin lines, myosin = tinted bar", "tm", "m", size=12)]
    return svg(480, 340, b)
D["sarcomere"] = (sarcomere(), "u22", "Sarcomere structure",
  "When the muscle contracts, actin slides over myosin towards the centre. The Z-lines move closer, so the sarcomere, I-band and H-zone all shorten. The **A-band stays the same length**, because it is the length of the myosin filaments.")

# 5. Action potential
def ap():
    p = Plot(70, 24, 380, 260, (0, 5), (-90, 50))
    b = p.axes("time / ms", "membrane potential / mV", yat=-90)
    for y in (-90, -70, -55, 0, 40): b += p.ytick(y, str(y).replace("-", "−"))
    for x in range(0, 6): b += p.xtick(x, str(x), yat=-90)
    b += [L(p.X(0), p.Y(-55), p.X(5), p.Y(-55), "lm"), T(p.X(5), p.Y(-55) - 6, "threshold", "tm", "e", size=12)]
    pts = [(0, -70), (1.0, -70)]
    d = (f"M{p.X(0)},{p.Y(-70)} L{p.X(1)},{p.Y(-70)} C{p.X(1.2)},{p.Y(-70)} {p.X(1.25)},{p.Y(-58)} {p.X(1.35)},{p.Y(-55)} "
         f"C{p.X(1.5)},{p.Y(-40)} {p.X(1.6)},{p.Y(40)} {p.X(1.8)},{p.Y(40)} C{p.X(2.0)},{p.Y(40)} {p.X(2.4)},{p.Y(-80)} {p.X(2.8)},{p.Y(-82)} "
         f"C{p.X(3.3)},{p.Y(-83)} {p.X(3.8)},{p.Y(-70)} {p.X(4.4)},{p.Y(-70)} L{p.X(5)},{p.Y(-70)}")
    b.append(P(d, "ac"))
    b += [T(p.X(0.1), p.Y(-64), "resting", "tm", size=12)]
    b += [T(p.X(1.4), p.Y(16), "Na⁺ in", "ta", "e", size=13), T(p.X(1.4), p.Y(2), "depolarisation", "tm", "e", size=12)]
    b += [T(p.X(2.3), p.Y(16), "K⁺ out", "tg", size=13), T(p.X(2.3), p.Y(2), "repolarisation", "tm", size=12)]
    b += [T(p.X(3.0), p.Y(-88) + 0, "", "tm")]
    b += [T(p.X(3.3), p.Y(-76) + 20, "hyperpolarisation", "tm", "m", size=12)]
    return svg(470, 320, b)
D["action-potential"] = (ap(), "u21", "Action potential",
  "Once the membrane reaches about −55 mV, voltage-gated Na⁺ channels open and Na⁺ rushes in (to about +40 mV). Then Na⁺ channels close and K⁺ channels open, so K⁺ leaves. K⁺ channels are slow to close, so the potential dips below −70 mV before the pump restores it.")

# 6. Cholinergic synapse
def synapse():
    b = []
    b += [P("M150,10 L150,120 Q150,170 240,170 Q330,170 330,120 L330,10", "ln thick"), T(240, 30, "presynaptic knob", "tm", "m", size=12)]
    for x, y in [(200, 90), (235, 110), (275, 95), (215, 140), (262, 140)]:
        b.append(C(x, y, 12, "at"))
    b += [L(120, 205, 360, 205, "ln thick"), T(200, 240, "postsynaptic membrane", "tm", "m", size=12)]
    for x in (190, 240, 290): b.append(R(x - 10, 205, 20, 12, "gt", rx=2))
    b += [T(240, 193, "", "")]
    # steps
    b += [L(70, 62, 146, 62, "gl", "ag"), T(60, 84, "① Ca²⁺ in", "tg", size=13)]
    b += [T(345, 80, "② vesicles fuse,", "", size=13), T(345, 96, "ACh released", "", size=13)]
    b += [L(290, 172, 290, 198, "ac", "aa"), T(345, 186, "③ ACh crosses", "", size=13)]
    b += [L(290, 220, 290, 262, "ac", "aa"), T(345, 270, "④ Na⁺ in:", "", size=13), T(345, 286, "depolarises", "", size=13)]
    b += [T(10, 270, "⑤ enzyme", "tm", size=13), T(10, 286, "breaks down ACh", "tm", size=12)]
    b += [T(10, 190, "cleft", "tm", size=12), L(48, 186, 115, 186, "lm")]
    b += [L(70, 34, 140, 34, "ln", "ah"), T(10, 38, "impulse", "tm", size=12)]
    return svg(480, 300, b)
D["synapse"] = (synapse(), "u21", "Cholinergic synapses",
  "The order to learn: ① the impulse opens Ca²⁺ channels and Ca²⁺ enters the knob; ② vesicles fuse with the membrane and release ACh; ③ ACh diffuses across the cleft; ④ it binds to receptors (gold), Na⁺ channels open and the postsynaptic membrane depolarises; ⑤ acetylcholinesterase breaks ACh down.")

# 7. Inhibitors
def inhib():
    p = Plot(60, 30, 380, 230, (0, 10), (0, 1.1))
    mm = lambda V, K: (lambda s: V * s / (K + s))
    b = p.axes("substrate concentration", "rate")
    b += [p.curve(mm(1.0, 0.8), 0, 10, cls="ln"), p.curve(mm(1.0, 3.2), 0, 10, cls="ac"), p.curve(mm(0.55, 0.8), 0, 10, cls="gl")]
    b += [L(p.X(0), p.Y(1.0), p.X(10), p.Y(1.0), "lm"), T(p.X(10), p.Y(1.0) - 6, "maximum rate", "tm", "e", size=12)]
    for i, (cls, tcls, lab) in enumerate([("ln", "", "no inhibitor"), ("ac", "ta", "competitive: catches up"), ("gl", "tg", "non-competitive: lower max")]):
        y = p.Y(0.30 - i * 0.11)
        b += [L(p.X(3.4), y - 4, p.X(4.2), y - 4, cls), T(p.X(4.5), y + 1, lab, tcls, size=13)]
    return svg(470, 300, b)
D["inhibitors"] = (inhib(), "u02", "Inhibitors",
  "Adding more substrate outcompetes a **competitive** inhibitor, so the rate eventually reaches the same maximum. A **non-competitive** inhibitor changes the active site's shape, so the affected enzymes can't work however much substrate there is: the maximum rate is lower.")

# 8. Fluid mosaic
def mosaic():
    b = []
    xs = [x for x in range(28, 470, 18)]
    skip = lambda x: 150 <= x <= 200 or 300 <= x <= 335
    for x in xs:
        if skip(x): continue
        b += [C(x, 70, 7, "at"), L(x - 2, 77, x - 2, 108, "ln"), L(x + 2, 77, x + 2, 108, "ln")]
        b += [C(x, 150, 7, "at"), L(x - 2, 143, x - 2, 112, "ln"), L(x + 2, 143, x + 2, 112, "ln")]
    b += [R(148, 54, 22, 112, "gt", rx=8), R(180, 54, 22, 112, "gt", rx=8), T(176, 190, "channel protein", "tg", "m", size=13), L(175, 62, 175, 158, "lm")]
    b += [R(300, 50, 38, 120, "gt", rx=14), T(319, 190, "carrier protein", "tg", "m", size=12)]
    b += [P("M100,62 L100,36 M100,44 L88,26 M100,44 L112,26 M100,36 L100,18", "ac")]
    b += [T(100, 12, "glycoprotein / glycolipid", "ta", "m", size=12)]
    b += [R(253, 84, 10, 22, "bx", rx=3), L(258, 84, 258, 76, "lm"), T(258, 216, "cholesterol", "tm", "m", size=12), L(258, 200, 258, 110, "lm")]
    b += [T(470, 46, "hydrophilic heads", "tm", "e", size=12), L(440, 50, 442, 62, "lm")]
    b += [T(470, 222, "hydrophobic tails", "tm", "e", size=12), L(440, 208, 442, 120, "lm")]
    return svg(480, 232, b)
D["fluid-mosaic"] = (mosaic(), "u06", "Fluid-mosaic model",
  "A bilayer of phospholipids with proteins scattered through it. Ions and polar molecules need **channel or carrier proteins** to get past the hydrophobic tails. Cholesterol sits between phospholipids and makes the membrane less fluid. Glycoproteins and glycolipids act as receptors and antigens.")

# 9. Counter-current vs parallel flow
def cc():
    b = []
    def row(y, title, water, blood, rev):
        o = [T(10, y - 34, title, "", size=14)]
        o += [L(60, y - 14, 440, y - 14, "ln", "ah"), T(30, y - 9, "water", "tm", "m", size=12)]
        if rev: o += [L(440, y + 46, 60, y + 46, "ac", "aa")]
        else: o += [L(60, y + 46, 440, y + 46, "ac", "aa")]
        o += [T(30, y + 51, "blood", "ta", "m", size=12)]
        for i, (w, bl) in enumerate(zip(water, blood)):
            x = 90 + i * 80
            o += [R(x - 26, y - 4, 52, 22, "bx", rx=4), T(x, y + 12, f"{w}%", "", "m", size=13)]
            o += [R(x - 26, y + 22, 52, 22, "at", rx=4), T(x, y + 38, f"{bl}%", "ta", "m", size=13)]
        return o
    b += row(56, "Counter-current (fish gills): water always richer in O₂", [90, 75, 60, 45, 30], [80, 65, 50, 35, 20], True)
    b += row(196, "Parallel flow: levels meet halfway, diffusion stops", [90, 70, 58, 52, 50], [10, 30, 42, 48, 50], False)
    return svg(480, 270, b)
D["counter-current"] = (cc(), "u08", "Fish",
  "Numbers are % O₂ saturation along a lamella. In counter-current flow, blood meets water that is always a little richer in oxygen, so O₂ diffuses in along the **whole length** and blood leaves at 80%. With parallel flow, the two equalise at 50% and diffusion stops.")

# 10. Calvin cycle
def calvin():
    b = []
    b += [R(180, 20, 120, 46, "at"), T(240, 49, "RuBP (5C)", "ta", "m")]
    b += [R(330, 180, 130, 46, "bx"), T(395, 209, "2 × GP (3C)", "", "m")]
    b += [R(20, 180, 130, 46, "bx"), T(85, 209, "TP (3C)", "", "m")]
    b += [P("M300,52 C380,60 400,110 398,176", "ln", "ah"), T(400, 100, "+ CO₂", "tg", size=14), T(400, 118, "rubisco", "tm", size=12)]
    b += [P("M330,212 L156,212", "ln", "ah"), T(243, 200, "reduced using", "tm", "m", size=12), T(243, 232, "reduced NADP + ATP", "tm", "m", size=12)]
    b += [P("M85,178 C80,110 110,58 176,46", "ln", "ah"), T(240, 112, "5 of every 6 TP", "tm", "m", size=12), T(240, 128, "regenerate RuBP", "tm", "m", size=12), T(240, 144, "(uses ATP)", "tm", "m", size=12)]
    b += [L(85, 228, 85, 270, "gl", "ag"), T(95, 262, "1 in 6 TP → glucose, starch,", "tg", size=13), T(95, 278, "amino acids, lipids", "tg", size=13)]
    return svg(480, 290, b)
D["calvin-cycle"] = (calvin(), "u16", "Light-independent reaction (Calvin cycle)",
  "CO₂ joins RuBP (catalysed by rubisco), giving two GP. GP is reduced to TP using reduced NADP and ATP from the light-dependent reaction. Most TP regenerates RuBP so the cycle continues; the rest makes useful organic molecules. Six turns make one glucose.")

# 11. Respiration overview
def resp():
    b = []
    stages = [("Glycolysis", "cytoplasm", "2 ATP (net), 2 reduced NAD"),
              ("Link reaction", "matrix", "CO₂, reduced NAD"),
              ("Krebs cycle", "matrix", "CO₂, reduced NAD and FAD, ATP"),
              ("Oxidative phosphorylation", "inner membrane", "most ATP; O₂ + H⁺ + e⁻ → H₂O")]
    mids = ["glucose", "2 pyruvate", "acetylcoenzyme A", "reduced NAD and FAD"]
    y = 14
    for i, (n, loc, out) in enumerate(stages):
        b += [T(105, y + 14, mids[i], "tm", "m", size=12), L(105, y + 20, 105, y + 40, "ln", "ah")]
        y += 44
        cls = "at" if i == 3 else "bx"
        b += [R(10, y, 190, 46, cls), T(105, y + 22, n, "ta" if i == 3 else "", "m", size=12 if i == 3 else 14), T(105, y + 38, loc, "tm", "m", size=12)]
        b += [L(204, y + 23, 222, y + 23, "lm", "am"), T(228, y + 28, out, "", size=13)]
        y += 56
    return svg(480, y + 4, b)
D["respiration"] = (resp(), "u17", "Glycolysis (cytoplasm)",
  "The four stages of aerobic respiration, where each happens, and what each makes. Without oxygen, only glycolysis runs, so pyruvate is turned into lactate or ethanol to regenerate NAD.")

# 12. Tissue fluid
def tfluid():
    b = []
    b += [R(96, 110, 288, 44, "bx", rx=22), T(8, 137, "arteriole", "tm", size=13), T(472, 137, "venule", "tm", "e", size=13)]
    b += [L(160, 140, 330, 140, "ln", "ah"), T(240, 128, "blood flow", "tm", "m", size=12)]
    for x in (125, 175): b += [L(x, 108, x, 64, "ac", "aa"), L(x, 156, x, 204, "ac", "aa")]
    for x in (310, 355): b += [L(x, 64, x, 106, "gl", "ag"), L(x, 202, x, 158, "gl", "ag")]
    b += [T(130, 30, "high hydrostatic pressure", "ta", "m", size=13), T(130, 46, "pushes fluid out", "ta", "m", size=12)]
    b += [T(350, 30, "water returns by osmosis:", "tg", "m", size=13), T(350, 46, "plasma proteins keep ψ low", "tg", "m", size=12)]
    b += [T(240, 236, "tissue fluid around cells", "tm", "m", size=12), T(240, 252, "excess drains into lymph", "tm", "m", size=12)]
    return svg(480, 262, b)
D["tissue-fluid"] = (tfluid(), "u10", "Tissue fluid",
  "At the arteriole end, hydrostatic pressure is high enough to force water and small molecules out. Large plasma proteins stay in the blood, so by the venule end, where pressure has fallen, water moves back in by osmosis. Excess tissue fluid drains into the lymph.")

# 13. Types of selection
def selection():
    b = []
    g = lambda m, s: (lambda x: math.exp(-((x - m) / s) ** 2 / 2))
    panels = [("Stabilising", lambda x: g(0, 1)(x), lambda x: 1.3 * g(0, 0.6)(x)),
              ("Directional", lambda x: g(0, 1)(x), lambda x: g(1.3, 1)(x)),
              ("Disruptive", lambda x: g(0, 1)(x), lambda x: 0.8 * g(-1.6, 0.6)(x) + 0.8 * g(1.6, 0.6)(x))]
    for i, (n, before, after) in enumerate(panels):
        p = Plot(16 + i * 156, 40, 136, 120, (-3.2, 3.2), (0, 1.4))
        b += [L(p.x0, p.Y(0), p.x0 + p.w, p.Y(0), "ln"), T(p.x0 + p.w / 2, 26, n, "", "m", size=14)]
        b += [p.curve(before, -3.2, 3.2, cls="lm"), p.curve(after, -3.2, 3.2, cls="ac")]
        b += [T(p.x0 + p.w / 2, p.Y(0) + 20, "phenotype", "tm", "m", size=12)]
    b += [L(30, 202, 60, 202, "lm"), T(66, 207, "before", "tm", size=12), L(140, 202, 170, 202, "ac"), T(176, 207, "after selection", "ta", size=12)]
    return svg(480, 216, b)
D["selection"] = (selection(), "u27", "Natural selection and evolution",
  "Stabilising selection favours the mean, so the range narrows. Directional selection favours one extreme, so the mean shifts. Disruptive selection favours both extremes, which can split a population into two groups.")

# 14. PCR
def pcr():
    p = Plot(70, 30, 380, 210, (0, 6), (40, 110))
    b = p.axes("time", "temperature / °C", yat=40)
    for y in (55, 72, 95): b += p.ytick(y, str(y))
    pts = []
    for c in range(2):
        o = c * 3
        pts += [(o, 95), (o + 0.9, 95), (o + 1.0, 55), (o + 1.9, 55), (o + 2.0, 72), (o + 2.9, 72), (o + 3.0, 95)]
    b.append(poly([p.pt(x, y) for x, y in pts[:-1]], "ac"))
    for o in (0, 3):
        b += [T(p.X(o + 0.45), p.Y(95) - 8, "separate", "ta", "m", size=12), T(p.X(o + 1.45), p.Y(55) + 18, "anneal", "ta", "m", size=12), T(p.X(o + 2.45), p.Y(72) - 8, "extend", "ta", "m", size=12)]
    b += [L(p.X(0), p.Y(42) + 0, p.X(3), p.Y(42), "lm"), T(p.X(1.5), p.Y(42) - 6, "one cycle: DNA doubles", "tm", "m", size=12)]
    return svg(470, 270, b)
D["pcr"] = (pcr(), "u31", "PCR (in vitro amplification)",
  "Each PCR cycle has three temperatures: 95 °C breaks the hydrogen bonds so the strands separate, 55 °C lets primers anneal, and 72 °C is the best temperature for Taq polymerase to join nucleotides. Each cycle doubles the DNA.")
