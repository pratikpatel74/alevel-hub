from lib import *
import math
D = {}

def hexring(cx, cy, r=26, cls="bx"):
    pts = [(cx + r * math.cos(math.radians(30 + 60 * i)), cy + r * math.sin(math.radians(30 + 60 * i))) for i in range(6)]
    return poly(pts, cls, closed=True)

# u01 condensation / hydrolysis
def glyco():
    b = []
    for x in (50, 190):
        b += [hexring(x, 70, 34), T(x, 128, "glucose", "tm", "m", size=12)]
    b += [T(88, 66, "OH", "ta", size=13), T(152, 66, "HO", "ta", "e", size=13)]
    b += [L(234, 70, 280, 70, "ln", "ah"), T(257, 28, "condensation", "", "m", size=12), T(257, 92, "− H₂O", "ta", "m", size=13)]
    b += [hexring(320, 70, 34), hexring(420, 70, 34), L(354, 70, 386, 70, "ac thick"), T(370, 62, "O", "ta", "m", size=14)]
    b += [T(370, 128, "1,4-glycosidic bond", "ta", "m", size=13), T(370, 146, "(maltose)", "tm", "m", size=12)]
    b += [L(280, 170, 234, 170, "ln", "ah"), T(257, 156, "hydrolysis", "", "m", size=12), T(257, 192, "+ H₂O", "ta", "m", size=13)]
    return svg(480, 204, b)
D["glycosidic"] = (glyco(), "u01", "Monosaccharides and disaccharides",
  "Two monosaccharides join by **condensation**: an OH from each reacts, water is released and a glycosidic bond forms. **Hydrolysis** is the reverse: water is used to break the bond.")

# u03 DNA ladder
def dna():
    b = []
    pairs = [("A", "T", 2), ("C", "G", 3), ("G", "C", 3), ("T", "A", 2), ("A", "T", 2)]
    x1, x2 = 120, 360
    b += [L(x1, 30, x1, 290, "ln thick"), L(x2, 30, x2, 290, "ln thick")]
    b += [L(100, 290, 100, 40, "ln", "ah"), T(100, 306, "5′ → 3′", "tm", "m", size=12), L(380, 40, 380, 280, "ln", "ah"), T(380, 26, "5′ → 3′", "tm", "m", size=12)]
    for i, (a, c, n) in enumerate(pairs):
        y = 56 + i * 52
        b += [C(x1, y, 7, "gf"), C(x2, y, 7, "gf")]
        b += [R(x1 + 10, y - 13, 60, 26, "at", rx=4), T(x1 + 40, y + 5, a, "ta", "m", size=14)]
        b += [R(x2 - 70, y - 13, 60, 26, "at", rx=4), T(x2 - 40, y + 5, c, "ta", "m", size=14)]
        for k in range(n):
            yy = y - (n - 1) * 4 + k * 8
            b.append(L(x1 + 74, yy, x2 - 74, yy, "lm"))
    b += [T(10, 150, "sugar-", "tg", size=12), T(10, 166, "phosphate", "tg", size=12), T(10, 182, "backbone", "tg", size=12)]
    b += [T(240, 320, "dashed lines = hydrogen bonds (A–T 2, C–G 3)", "tm", "m", size=12)]
    return svg(480, 330, b)
D["dna-structure"] = (dna(), "u03", "Nucleotides, DNA and RNA",
  "Two antiparallel strands, each with a sugar-phosphate backbone, held together by hydrogen bonds between complementary bases: A pairs with T (2 hydrogen bonds), C with G (3).")

# u04 ultracentrifugation
def fraction():
    b = []
    items = [("low speed", "nuclei", 40), ("medium", "mitochondria", 26), ("high", "ER, ribosomes", 14)]
    for i, (sp, pel, h) in enumerate(items):
        x = 50 + i * 150
        b += [P(f"M{x},40 L{x},210 Q{x},236 {x + 26},236 Q{x + 52},236 {x + 52},210 L{x + 52},40", "ln")]
        b += [f'<rect x="{x + 2}" y="70" width="48" height="{150 - h}" class="nt" stroke="none"/>']
        b += [P(f"M{x + 3},{226 - h} L{x + 49},{226 - h} L{x + 49},210 Q{x + 49},233 {x + 26},233 Q{x + 3},233 {x + 3},210 Z", "at")]
        b += [T(x + 26, 28, sp, "", "m", size=13), T(x + 26, 258, pel, "ta", "m", size=13), T(x + 26, 274, "pellet", "tm", "m", size=12)]
        if i < 2: b += [P(f"M{x + 56},80 C{x + 90},60 {x + 110},60 {x + 142},80", "ln", "ah"), T(x + 99, 56, "supernatant", "tm", "m", size=11)]
    return svg(480, 286, b)
D["ultracentrifugation"] = (fraction(), "u04", "Cell fractionation and ultracentrifugation",
  "The homogenate is spun at increasing speeds. Each time the densest organelles form a pellet, and the supernatant is poured into a new tube and spun faster: nuclei first, then mitochondria, then ER and ribosomes.")

# u05 cell cycle
def cycle():
    b = []
    cx, cy, r = 140, 150, 110
    segs = [("G1", 0, 140, "at"), ("S", 140, 230, "gt"), ("G2", 230, 310, "at"), ("M", 310, 350, "nt"), ("C", 350, 360, "nt")]
    def arc(a1, a2, cls):
        p1 = (cx + r * math.sin(math.radians(a1)), cy - r * math.cos(math.radians(a1)))
        p2 = (cx + r * math.sin(math.radians(a2)), cy - r * math.cos(math.radians(a2)))
        large = 1 if a2 - a1 > 180 else 0
        return f'<path d="M{f(cx)},{f(cy)} L{f(p1[0])},{f(p1[1])} A{r},{r} 0 {large} 1 {f(p2[0])},{f(p2[1])} Z" class="{cls}"/>'
    for n, a1, a2, cls in segs: b.append(arc(a1, a2, cls))
    def lab(a, s, cls="", rr=70, size=14):
        return T(cx + rr * math.sin(math.radians(a)), cy - rr * math.cos(math.radians(a)) + 5, s, cls, "m", size=size)
    b += [lab(70, "G1", "ta"), lab(185, "S", "tg"), lab(270, "G2", "ta"), lab(330, "M", "", 128, 14), lab(356, "C", "", 128, 13)]
    b += [T(280, 50, "Interphase", "", size=14), T(280, 68, "(most of the cycle)", "tm", size=12)]
    b += [T(280, 94, "G1: growth, organelles made", "tm", size=12), T(280, 112, "S: DNA replicates", "tg", size=12), T(280, 130, "G2: more growth, checks", "tm", size=12)]
    b += [T(280, 170, "M: mitosis (nucleus divides)", "", size=12), T(280, 188, "C: cytokinesis", "", size=12)]
    return svg(480, 280, b)
D["cell-cycle"] = (cycle(), "u05", "The cell cycle",
  "Most of the cycle is interphase. DNA replicates in the S phase, so each chromosome has two sister chromatids before mitosis begins. Mitosis and cytokinesis are a small slice at the end.")

# u07 primary vs secondary response
def immune():
    p = Plot(60, 30, 390, 210, (0, 60), (0, 10))
    b = p.axes("", "antibody concentration") + [T(p.X(60), p.Y(0) + 20, "time / days", "tm", "e", size=12)]
    def resp(t0, peak, rise, fall, h):
        return lambda t: 0 if t < t0 else h * (1 - math.exp(-(t - t0) / rise)) * math.exp(-max(0, t - t0 - peak) / fall)
    f1 = resp(4, 8, 3, 8, 2.5); f2 = resp(32, 6, 1.2, 14, 9)
    b += [p.curve(lambda t: f1(t) + f2(t), 0, 60, n=300, cls="ac")]
    b += [L(p.X(0), p.Y(0), p.X(0), p.Y(0), "ln")]
    b += [L(p.X(2), p.Y(0) + 30, p.X(2), p.Y(0) + 6, "gl", "ag"), T(p.X(2), p.Y(0) + 46, "1st exposure", "tg", "start", size=12)]
    b += [L(p.X(30), p.Y(0) + 30, p.X(30), p.Y(0) + 6, "gl", "ag"), T(p.X(30), p.Y(0) + 46, "2nd exposure", "tg", "m", size=12)]
    b += [T(p.X(12), p.Y(3.6), "primary: slow, small", "", "m", size=13)]
    b += [T(p.X(48), p.Y(9.6), "secondary: fast, large", "", "m", size=13), T(p.X(48), p.Y(9.6) + 16, "(memory cells)", "tm", "m", size=12)]
    return svg(470, 300, b)
D["immune-response"] = (immune(), "u07", "Humoral response: B lymphocytes and antibodies",
  "The first exposure gives a slow, small primary response, usually with symptoms. Memory cells made then divide rapidly into plasma cells on a second exposure, so far more antibody is made far faster, usually before symptoms appear.")

# u09 co-transport in the ileum
def ileum():
    b = []
    b += [R(140, 40, 200, 200, "bx", rx=10), T(240, 30, "epithelial cell", "tm", "m", size=12)]
    b += [T(70, 30, "lumen", "", "m", size=13), T(410, 30, "blood", "", "m", size=13)]
    b += [T(240, 150, "low Na⁺", "tm", "m", size=13), T(240, 168, "high glucose", "tm", "m", size=13)]
    # pump on blood side
    b += [C(340, 90, 16, "gt"), T(340, 95, "ATP", "tg", "m", size=11)]
    b += [L(300, 84, 380, 84, "gl", "ag"), T(386, 88, "3Na⁺ out", "tg", size=12), L(380, 100, 300, 100, "gl", "ag"), T(386, 110, "2K⁺ in", "tg", size=12)]
    b += [T(340, 128, "Na⁺/K⁺ pump", "tm", "m", size=11)]
    # co-transporter
    b += [R(128, 74, 24, 52, "at", rx=6)]
    b += [L(60, 90, 200, 90, "ac", "aa"), T(56, 94, "Na⁺", "ta", "e", size=13), L(60, 112, 200, 112, "ac", "aa"), T(56, 116, "glucose", "ta", "e", size=13)]
    b += [T(140, 144, "co-transporter", "tm", "m", size=11)]
    # facilitated diffusion out
    b += [R(328, 186, 24, 36, "nt", rx=6), L(290, 204, 400, 204, "ln", "ah"), T(406, 208, "glucose", "", size=13), T(340, 238, "facilitated diffusion", "tm", "m", size=11)]
    return svg(480, 252, b)
D["co-transport"] = (ileum(), "u09", "Absorption in the ileum",
  "The Na⁺/K⁺ pump uses ATP to keep Na⁺ low inside the cell. Na⁺ then diffuses in from the lumen through a co-transporter, carrying glucose (or amino acids) against its gradient. Glucose leaves into the blood by facilitated diffusion.")

# u11 mass flow
def massflow():
    b = []
    b += [R(20, 40, 100, 70, "at"), T(70, 30, "source (leaf)", "ta", "m", size=13)]
    b += [R(360, 40, 100, 70, "bx"), T(410, 30, "sink (root)", "", "m", size=13)]
    b += [R(140, 60, 200, 30, "nt", rx=4), T(240, 108, "phloem sieve tube", "tm", "m", size=12)]
    b += [L(150, 75, 330, 75, "ac thick", "aa")]
    b += [R(140, 160, 200, 24, "bx", rx=4), T(240, 177, "xylem", "tm", "m", size=12)]
    b += [L(120, 66, 150, 66, "gl", "ag"), T(70, 128, "sucrose actively", "tg", "m", size=12), T(70, 144, "loaded (ATP)", "tg", "m", size=12)]
    b += [L(170, 158, 170, 94, "ln", "ah"), T(176, 132, "H₂O in by", "", size=12), T(176, 148, "osmosis", "", size=12)]
    b += [L(310, 94, 310, 158, "ln", "ah"), T(316, 132, "H₂O out", "", size=12)]
    b += [L(330, 66, 360, 66, "gl", "ag"), T(410, 128, "sucrose unloaded:", "tg", "m", size=12), T(410, 144, "used or stored", "tg", "m", size=12)]
    b += [T(144, 52, "high pressure", "ta", size=12), T(336, 52, "low pressure", "tm", "e", size=12)]
    return svg(480, 200, b)
D["mass-flow"] = (massflow(), "u11", "Mass flow hypothesis",
  "At the source, sucrose is actively loaded into the sieve tube, lowering water potential, so water enters from the xylem by osmosis and pressure rises. At the sink, sucrose is removed and water leaves. The pressure gradient pushes sap from source to sink.")

# u12 translation
def translation():
    b = []
    codons = ["AUG", "GCA", "UUC", "GGU", "UAA"]
    for i, c in enumerate(codons):
        x = 40 + i * 84
        b += [R(x, 200, 76, 26, "bx", rx=3), T(x + 38, 218, c, "", "m", size=14)]
    b += [T(20, 244, "mRNA", "tm", size=12), T(460, 244, "stop", "tm", "e", size=12)]
    b += [P("M110,190 L110,120 Q110,100 130,100 L300,100 Q320,100 320,120 L320,190", "lm"), T(215, 92, "ribosome", "tm", "m", size=12)]
    for i, (ac, aa) in enumerate([("CGU", "Ala"), ("AAG", "Phe")]):
        x = 124 + 84 + (i - 1) * 84 + 0
        x = 124 + i * 84 + 84 - 84
    for i, (ac, aa) in enumerate([("CGU", "Ala"), ("AAG", "Phe")]):
        x = 124 + (i + 1) * 84 - 84 + 0
        xx = 40 + (i + 1) * 84
        b += [R(xx + 6, 160, 64, 26, "at", rx=3), T(xx + 38, 178, ac, "ta", "m", size=14), L(xx + 38, 160, xx + 38, 140, "ln")]
        b += [C(xx + 38, 128, 13, "gt"), T(xx + 38, 133, aa, "tg", "m", size=11)]
    b += [L(175, 128, 233, 128, "gl", extra=' stroke-width="3"')]
    b += [C(120, 60, 13, "gt"), T(120, 65, "Met", "tg", "m", size=11), L(120, 73, 160, 117, "gl", extra=' stroke-width="3"')]
    b += [T(300, 140, "peptide bond", "tg", size=12), L(296, 136, 214, 130, "lm")]
    b += [T(360, 170, "tRNA anticodon", "ta", size=12), T(360, 186, "pairs with codon", "ta", size=12)]
    b += [L(30, 270, 120, 270, "ln", "ah"), T(128, 274, "ribosome moves one codon at a time", "tm", size=12)]
    return svg(480, 284, b)
D["translation"] = (translation(), "u12", "Translation",
  "tRNA molecules with complementary anticodons bring amino acids to the ribosome, two at a time. A peptide bond forms between neighbouring amino acids (using ATP), the ribosome moves on one codon, and this repeats until a stop codon.")

# u13 meiosis
def meiosis():
    b = []
    def chrom(x, y, cls, double=True, h=26):
        o = [L(x, y - h / 2, x, y + h / 2, cls + " thick")]
        if double: o.append(L(x + 7, y - h / 2, x + 7, y + h / 2, cls + " thick"))
        return o
    def cell(cx, cy, r, items):
        o = [C(cx, cy, r, "bx")]
        for dx, cls, d, h in items: o += chrom(cx + dx, cy, cls, d, h)
        return o
    b += cell(80, 140, 52, [(-26, "ac", True, 34), (-10, "gl", True, 34), (8, "ac", True, 20), (22, "gl", True, 20)])
    b += [T(80, 210, "diploid parent", "tm", "m", size=12), T(80, 226, "(after replication)", "tm", "m", size=12)]
    b += [L(140, 140, 176, 90, "ln", "ah"), L(140, 140, 176, 190, "ln", "ah"), T(170, 146, "I", "", size=14)]
    b += cell(220, 80, 38, [(-14, "ac", True, 34), (6, "gl", True, 20)])
    b += cell(220, 200, 38, [(-14, "gl", True, 34), (6, "ac", True, 20)])
    b += [T(220, 268, "homologous pairs separate", "tm", "m", size=12)]
    for i, (cy, a, c) in enumerate([(80, "ac", "gl"), (200, "gl", "ac")]):
        for j, dy in enumerate((-30, 30)):
            y = cy + dy * 0.9
            b += [L(262, cy, 330, y, "ln", "ah")]
            b += cell(360, y, 22, [(-8, a, False, 30), (6, c, False, 18)])
    b += [T(296, 30, "II", "", "m", size=14), T(390, 268, "chromatids separate:", "tm", "m", size=12), T(390, 284, "4 haploid cells", "tm", "m", size=12)]
    b += [T(400, 82, "", "")]
    return svg(480, 292, b)
D["meiosis"] = (meiosis(), "u13", "Meiosis",
  "Accent and gold show chromosomes from each parent. In **meiosis I** homologous pairs separate, halving the chromosome number; which way each pair lines up is random (independent segregation). In **meiosis II** sister chromatids separate, giving four haploid cells.")

# u14 antibiotic resistance
def resistance():
    b = []
    import random
    rnd = random.Random(4)
    def pop(x0, n_res, total, alive=True):
        o = []; k = 0
        cells = [(x0 + 12 + (i % 6) * 16, 70 + (i // 6) * 16) for i in range(total)]
        res = set(rnd.sample(range(total), n_res))
        for i, (x, y) in enumerate(cells):
            o.append(C(x, y, 5.5, "af" if i in res else "nt"))
        return o
    b += pop(10, 2, 30) + [T(58, 50, "random mutation", "", "m", size=12), T(58, 172, "2 resistant", "ta", "m", size=12)]
    b += [L(116, 110, 150, 110, "ln", "ah"), T(133, 98, "drug", "tm", "m", size=11)]
    b += [C(178 + (0 % 6) * 16, 70, 5.5, "af"), C(178 + 3 * 16, 86, 5.5, "af")]
    b += [T(214, 50, "survivors", "", "m", size=12), T(214, 172, "others die", "tm", "m", size=12)]
    b += [L(272, 110, 306, 110, "ln", "ah"), T(289, 98, "divide", "tm", "m", size=11)]
    b += pop(316, 27, 30) + [T(364, 50, "next generations", "", "m", size=12), T(364, 172, "mostly resistant", "ta", "m", size=12)]
    return svg(430, 186, b)
D["antibiotic-resistance"] = (resistance(), "u14", "Antibiotic resistance",
  "Resistance starts as a chance mutation in a few bacteria (accent). The antibiotic kills the rest, so resistant bacteria survive, divide by binary fission and pass the allele on. Over generations the resistance allele becomes common.")

# u15 classification
def classify():
    b = []
    ranks = [("Domain", "Eukarya"), ("Kingdom", "Animalia"), ("Phylum", "Chordata"), ("Class", "Mammalia"), ("Order", "Primates"), ("Family", "Hominidae"), ("Genus", "Homo"), ("Species", "sapiens")]
    for i, (r, ex) in enumerate(ranks):
        x, y = 10 + i * 14, 10 + i * 34
        w, h = 460 - i * 28, 300 - i * 34
        b.append(R(x, y, w, h, "at" if i >= 6 else "bx", rx=8))
        b += [T(x + 10, y + 22, r, "ta" if i >= 6 else "", size=13), T(x + w - 10, y + 22, ex, "tm", "e", size=13)]
    return svg(480, 312, b)
D["classification"] = (classify(), "u15", "Classification",
  "Each group sits entirely inside a larger one, with no overlap (a hierarchy). Humans as the example: the binomial name is genus + species, Homo sapiens.")

# u18 energy flow
def energy():
    b = []
    b += [R(20, 40, 120, 50, "at"), T(80, 62, "GPP", "ta", "m", size=15), T(80, 80, "producers", "tm", "m", size=12)]
    b += [L(140, 65, 200, 65, "ln", "ah"), R(200, 40, 100, 50, "at"), T(250, 70, "NPP", "ta", "m", size=15)]
    b += [L(80, 90, 80, 130, "lm", "am"), T(80, 146, "R (respiration)", "tm", "m", size=12)]
    b += [L(300, 65, 350, 65, "ln", "ah"), T(325, 56, "I", "", "m", size=14), R(350, 40, 110, 50, "bx"), T(405, 62, "consumer", "", "m", size=13), T(405, 80, "N = I − (F + R)", "tm", "m", size=12)]
    b += [L(380, 90, 380, 130, "lm", "am"), T(380, 146, "F (faeces, urine)", "tm", "m", size=12)]
    b += [L(440, 90, 440, 170, "lm", "am"), T(440, 186, "R (heat)", "tm", "e", size=12)]
    b += [L(250, 90, 250, 170, "lm", "am"), T(250, 186, "not eaten (roots, bark)", "tm", "m", size=12)]
    b += [T(240, 222, "NPP = GPP − R", "", "m", size=14)]
    return svg(480, 234, b)
D["energy-flow"] = (energy(), "u18", "Net production of consumers",
  "Energy flows from plant biomass to consumers, and some is lost at every step: plant respiration (GPP → NPP), parts not eaten, faeces and urine, and the consumer's own respiration. Only N is left for the next trophic level.")

# u19 nitrogen cycle
def ncycle():
    b = []
    nodes = {"N2": (240, 30, "N₂ in air"), "NH4": (90, 150, "NH₄⁺"), "NO2": (240, 240, "NO₂⁻"), "NO3": (390, 150, "NO₃⁻"), "org": (240, 150, "proteins in plants/animals")}
    for k, (x, y, s) in nodes.items():
        w = 210 if k == "org" else 96
        b += [R(x - w / 2, y - 18, w, 36, "at" if k == "org" else "bx"), T(x, y + 5, s, "ta" if k == "org" else "", "m", size=13)]
    def ar(p1, p2, lab, lx, ly, a="m", cls="ln", mk="ah", tc="tm"):
        return [L(*p1, *p2, cls, mk), T(lx, ly, lab, tc, a, size=12)]
    b += ar((200, 48), (110, 130), "fixation", 132, 80, "e")
    b += ar((110, 170), (210, 228), "nitrification", 150, 220, "e")
    b += ar((290, 228), (370, 170), "nitrification", 332, 220)
    b += ar((370, 130), (280, 48), "denitrification", 350, 80, "start", "gl", "ag", "tg")
    b += ar((340, 150), (347, 150), "", 0, 0)
    b += ar((342, 160), (345, 160), "", 0, 0)
    b += [L(342, 150, 346, 150, "ln", "ah")]
    b += [P("M342,150 L346,150", "ln", "ah")]
    b += [T(360, 196, "absorbed", "tm", "m", size=11)]
    b += [L(135, 140, 138, 140, "ln")]
    b += [T(160, 112, "ammonification", "tm", "m", size=11), L(134, 150, 138, 150, "ln", "ah", start=False)]
    b += [T(240, 290, "waterlogged (anaerobic) soil favours denitrification", "tg", "m", size=12)]
    return svg(480, 300, b)
def ncycle2():
    b = []
    box = lambda x, y, w, s, cls="bx", tc="": [R(x - w / 2, y - 18, w, 36, cls), T(x, y + 5, s, tc, "m", size=13)]
    b += box(240, 30, 110, "N₂ (air)")
    b += box(240, 130, 200, "organic N in living things", "at", "ta")
    b += box(80, 250, 90, "NH₄⁺")
    b += box(240, 250, 84, "NO₂⁻")
    b += box(400, 250, 90, "NO₃⁻")
    lab = lambda x, y, s, c="tm", a="m": T(x, y, s, c, a, size=12)
    b += [poly([(185, 30), (50, 30), (50, 230)], "ln", "ah"), lab(58, 90, "fixation", "", "start")]
    b += [L(150, 148, 100, 230, "ln", "ah"), lab(132, 200, "ammonification", "tm", "start")]
    b += [L(125, 250, 196, 250, "ln", "ah"), lab(160, 280, "nitrification")]
    b += [L(282, 250, 353, 250, "ln", "ah"), lab(318, 280, "nitrification")]
    b += [L(400, 230, 330, 150, "ln", "ah"), lab(374, 196, "absorbed", "tm", "start")]
    b += [poly([(440, 232), (440, 30), (297, 30)], "gl", "ag"), lab(432, 80, "denitrification", "tg", "e")]
    return svg(480, 292, b)
D["nitrogen-cycle"] = (ncycle2(), "u19", "The nitrogen cycle",
  "Saprobionts turn organic nitrogen into ammonium (ammonification); nitrifying bacteria oxidise it to nitrite then nitrate (needs O₂); plants absorb nitrate. Nitrogen-fixing bacteria turn N₂ into ammonium; denitrifying bacteria (gold) return nitrate to N₂ in anaerobic soil.")

# u20 heart conduction
def conduction():
    b = []
    b += [P("M120,40 Q60,40 60,110 L60,180 Q60,300 240,330 Q420,300 420,180 L420,110 Q420,40 360,40 Z", "bx")]
    b += [L(60, 130, 420, 130, "lm"), T(410, 122, "atria", "tm", "e", size=12), T(410, 150, "ventricles", "tm", "e", size=12)]
    b += [L(240, 130, 240, 318, "ln"), T(250, 220, "septum", "tm", size=11)]
    b += [C(110, 70, 10, "gf"), T(126, 64, "① SAN", "tg", size=13), T(126, 80, "pacemaker", "tm", size=11)]
    b += [P("M110,70 Q160,90 230,124", "gl", "ag"), P("M110,70 Q70,100 74,124", "gl", "ag")]
    b += [C(240, 128, 9, "af"), T(254, 120, "② AVN: delay", "ta", size=13)]
    b += [L(240, 138, 240, 290, "ac thick"), T(214, 200, "③ bundle", "ta", "e", size=12), T(214, 216, "of His", "ta", "e", size=12)]
    b += [P("M240,300 Q160,300 120,250 L90,180", "ac", "aa"), P("M240,300 Q320,300 360,250 L390,180", "ac", "aa")]
    b += [T(252, 246, "④ Purkyne tissue", "ta", size=12)]
    b += [T(240, 350, "a non-conducting layer separates atria and ventricles", "tm", "m", size=11)]
    return svg(480, 360, b)
D["heart-conduction"] = (conduction(), "u20", "Control of heart rate",
  "① The SAN starts a wave of excitation that spreads across the atria, so they contract. ② The AVN delays it so the atria finish emptying. ③ The bundle of His carries it down the septum to the apex, then ④ Purkyne tissue carries it up the ventricle walls, so they contract from the bottom up.")

# u23 blood glucose feedback
def glucose():
    b = []
    b += [R(170, 140, 140, 40, "bx"), T(240, 165, "normal glucose", "", "m", size=13)]
    b += [R(170, 20, 140, 36, "at"), T(240, 43, "glucose rises", "ta", "m", size=13)]
    b += [R(170, 264, 140, 36, "gt"), T(240, 287, "glucose falls", "tg", "m", size=13)]
    b += [L(240, 138, 240, 60, "lm", "am"), L(240, 182, 240, 260, "lm", "am"), T(232, 105, "after a meal", "tm", "e", size=11), T(250, 225, "exercise, fasting", "tm", size=11)]
    b += [P("M312,38 L444,38 L444,150 L314,156", "ac", "aa"), T(322, 70, "β cells: insulin", "ta", size=12), T(322, 88, "cells take up", "tm", size=11), T(322, 102, "glucose;", "tm", size=11), T(322, 116, "glycogenesis", "tm", size=11)]
    b += [P("M168,282 L60,282 L60,170 L166,164", "gl", "ag"), T(70, 200, "α cells: glucagon", "tg", size=12), T(70, 218, "glycogenolysis,", "tm", size=11), T(70, 232, "gluconeogenesis", "tm", size=11)]
    return svg(480, 310, b)
D["glucose-feedback"] = (glucose(), "u23", "Insulin: lowering blood glucose",
  "Negative feedback with two separate mechanisms. A rise is detected by β cells, which secrete insulin: cells take up more glucose and the liver makes glycogen. A fall is detected by α cells, which secrete glucagon: the liver breaks down glycogen and makes new glucose.")

# u25 sex linkage Punnett square
def punnett():
    b = []
    x0, y0, s = 160, 60, 96
    b += [T(x0 + s, y0 - 34, "father XᴴY", "", "m", size=13), T(x0 - 50, y0 + s, "mother", "", "m", size=13), T(x0 - 50, y0 + s + 16, "XᴴXʰ", "", "m", size=13)]
    gam_f, gam_m = ["Xᴴ", "Y"], ["Xᴴ", "Xʰ"]
    for i, g in enumerate(gam_f): b += [C(x0 + s / 2 + i * s, y0 - 12, 14, "bx"), T(x0 + s / 2 + i * s, y0 - 7, g, "", "m", size=12)]
    for j, g in enumerate(gam_m): b += [C(x0 - 14, y0 + s / 2 + j * s, 14, "bx"), T(x0 - 14, y0 + s / 2 + j * s + 5, g, "", "m", size=12)]
    cells = [[("XᴴXᴴ", "girl", "bx", ""), ("XᴴY", "boy", "bx", "")], [("XᴴXʰ", "carrier girl", "gt", "tg"), ("XʰY", "affected boy", "at", "ta")]]
    for j in range(2):
        for i in range(2):
            g, d, cls, tc = cells[j][i]
            x, y = x0 + i * s + 4, y0 + 4 + j * s
            b += [R(x, y, s - 8, s - 8, cls, rx=6), T(x + (s - 8) / 2, y + 36, g, tc, "m", size=15), T(x + (s - 8) / 2, y + 56, d, "tm", "m", size=11)]
    b += [T(256, 290, "half of sons affected; no daughters affected", "", "m", size=13)]
    return svg(480, 302, b)
D["sex-linkage"] = (punnett(), "u25", "Sex linkage",
  "Haemophilia: carrier mother × unaffected father. Each son gets his X from his mother, so each son has a 0.5 chance of being affected. Daughters get the father's Xᴴ, so they are unaffected (half are carriers).")

# u26 Hardy–Weinberg square
def hw():
    b = []
    p, q = 0.7, 0.3
    x0, y0, S = 150, 40, 220
    a, c = S * p, S * q
    b += [R(x0, y0, a, a, "at", rx=0), R(x0 + a, y0, c, a, "gt", rx=0), R(x0, y0 + a, a, c, "gt", rx=0), R(x0 + a, y0 + a, c, c, "nt", rx=0)]
    b += [T(x0 + a / 2, y0 + a / 2 + 5, "p² = 0.49", "ta", "m", size=15), T(x0 + a + c / 2, y0 + a / 2 + 5, "pq", "tg", "m", size=14), T(x0 + a / 2, y0 + a + c / 2 + 5, "pq", "tg", "m", size=14), T(x0 + a + c / 2, y0 + a + c / 2 + 5, "q²", "", "m", size=14)]
    b += [T(x0 + a / 2, y0 - 10, "p = 0.7 (A)", "", "m", size=13), T(x0 + a + c / 2, y0 - 10, "q = 0.3 (a)", "", "m", size=13)]
    b += [T(x0 - 10, y0 + a / 2, "p", "", "e", size=13), T(x0 - 10, y0 + a + c / 2, "q", "", "e", size=13)]
    b += [T(390, 120, "AA: p² = 0.49", "ta", size=13), T(390, 140, "Aa: 2pq = 0.42", "tg", size=13), T(390, 160, "aa: q² = 0.09", "", size=13), T(390, 186, "total = 1", "tm", size=12)]
    return svg(500, 274, b)
D["hardy-weinberg"] = (hw(), "u26", "Hardy–Weinberg principle",
  "Why p² + 2pq + q² = 1: the square's sides are the allele frequencies p and q (p + q = 1). Its four regions are the genotype frequencies, with two pq regions for heterozygotes. Example: q = 0.3, so 9% are aa.")

# u28 succession
def succession():
    b = []
    stages = ["bare rock", "lichens", "mosses", "grasses", "shrubs", "woodland"]
    p = Plot(40, 40, 420, 170, (0, 5.4), (0, 1))
    b += [L(p.X(0), p.Y(0), p.X(5.4) + 8, p.Y(0), "ln", "ah"), T(p.X(5), p.Y(0) + 40, "time →", "tm", "e", size=12)]
    for i, s in enumerate(stages):
        b += [T(p.X(i), p.Y(0) + 20, s, "tm" if i not in (1, 5) else ("ta" if i == 5 else "tg"), "m", size=12)]
    b += [p.curve(lambda t: 0.08 + 0.17 * t, 0, 5, cls="ac"), T(p.X(3.3), p.Y(0.86), "biodiversity, biomass", "ta", "e", size=12)]
    b += [p.curve(lambda t: 0.02 + 0.6 * (1 - math.exp(-t / 2)), 0, 5, cls="gl"), T(p.X(5), p.Y(0.45), "soil depth", "tg", "e", size=12)]
    return svg(480, 254, b)
D["succession"] = (succession(), "u28", "Succession",
  "Pioneer species such as lichens colonise bare rock and start to make soil. Each stage changes the abiotic conditions so new species can survive and outcompete the earlier ones, until a stable climax community forms. Biodiversity and biomass generally increase.")

# u29 stem cell potency
def potency():
    b = []
    lv = [("Totipotent", "zygote, very early embryo", "any cell, including placenta"),
          ("Pluripotent", "embryo", "almost any body cell"),
          ("Multipotent", "adult, e.g. bone marrow", "a few related types"),
          ("Unipotent", "adult tissue", "one type, e.g. cardiomyocytes")]
    for i, (n, where, what) in enumerate(lv):
        w = 460 - i * 46; x = 240 - w / 2; y = 20 + i * 62
        b += [R(x, y, w, 50, "at" if i == 0 else "bx", rx=8), T(240, y + 21, n, "ta" if i == 0 else "", "m", size=14), T(240, y + 39, f"{where} → {what}", "tm", "m", size=11)]
    return svg(480, 268, b)
D["stem-cell-potency"] = (potency(), "u29", "Stem cells",
  "The range of cell types a stem cell can become narrows as development goes on, from totipotent (anything, including placenta) to unipotent (one type). iPS cells are made by turning unipotent adult cells back into pluripotent ones with transcription factors.")

# u30 epigenetics
def epi():
    b = []
    b += [T(120, 24, "gene ON", "ta", "m", size=14)]
    for x in (50, 120, 190):
        b += [C(x, 100, 20, "nt"), C(x, 72, 5, "af"), T(x, 62, "Ac", "ta", "m", size=11)]
    b += [P("M20,132 Q50,150 85,124 Q120,96 155,124 Q190,150 220,124", "ac")]
    b += [T(120, 160, "acetylated histones:", "tm", "m", size=12), T(120, 176, "DNA loose, TFs bind", "tm", "m", size=12)]
    b += [L(232, 100, 268, 100, "ln", "ah"), L(268, 116, 232, 116, "ln", "ah")]
    b += [T(370, 24, "gene OFF", "tg", "m", size=14)]
    for x in (330, 370, 410):
        b += [C(x, 100, 20, "gt")]
    b += [P("M290,100 Q310,70 330,80 Q350,130 370,120 Q390,70 410,80 Q430,130 450,100", "gl")]
    for x in (318, 384, 438): b += [C(x, 70, 5, "gf"), T(x, 58, "CH₃", "tg", "m", size=10)]
    b += [T(370, 160, "deacetylated + methylated:", "tm", "m", size=12), T(370, 176, "DNA tight, TFs can't bind", "tm", "m", size=12)]
    return svg(480, 188, b)
D["epigenetics"] = (epi(), "u30", "Epigenetics",
  "Neither change alters the base sequence. **Acetylated histones** hold DNA loosely, so transcription factors can reach the promoter and the gene is on. **Less acetylation** and **more methylation** of DNA condense the chromatin and block transcription factors, so the gene is off.")
