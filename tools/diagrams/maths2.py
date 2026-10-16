from lib import *
import math
D = {}

# u02 discriminant
def disc():
    b = []
    cases = [("b² − 4ac > 0", "two real roots", lambda x: x * x - 1.5, "ac", 2.2), ("b² − 4ac = 0", "one repeated root", lambda x: x * x, "ln", 2.0), ("b² − 4ac < 0", "no real roots", lambda x: x * x + 1, "gl", 1.73)]
    for i, (t, d, fn, cls, dom) in enumerate(cases):
        p = Plot(14 + i * 156, 40, 136, 150, (-2.2, 2.2), (-2, 4))
        b += [L(p.x0, p.Y(0), p.x0 + p.w, p.Y(0), "ln"), p.curve(fn, -dom, dom, cls=cls)]
        b += [T(p.x0 + p.w / 2, 24, t, "", "m", size=13), T(p.x0 + p.w / 2, 214, d, "tm", "m", size=12)]
        if i == 0: b += [C(p.X(-math.sqrt(1.5)), p.Y(0), 4, "af"), C(p.X(math.sqrt(1.5)), p.Y(0), 4, "af")]
        if i == 1: b += [C(p.X(0), p.Y(0), 4, "cf")]
    return svg(480, 226, b)
D["discriminant"] = (disc(), "u02", "The discriminant",
  "The discriminant b² − 4ac tells you how many times the graph of y = ax² + bx + c meets the x-axis: twice (positive), touching once (zero) or not at all (negative).")

# u05 Pascal's triangle
def pascal():
    b = []
    for n in range(6):
        y = 30 + n * 38
        b.append(T(30, y + 5, f"n = {n}", "tm", size=12))
        for k in range(n + 1):
            x = 260 + (k - n / 2) * 52
            v = math.comb(n, k)
            cls = "at" if n == 4 else "bx"
            b += [C(x, y, 17, cls), T(x, y + 5, str(v), "ta" if n == 4 else "", "m", size=14)]
    b += [T(240, 262, "(a + b)⁴ = a⁴ + 4a³b + 6a²b² + 4ab³ + b⁴", "ta", "m", size=14), T(240, 282, "each number = sum of the two above; row n gives nC0 … nCn", "tm", "m", size=12)]
    return svg(480, 292, b)
D["pascal"] = (pascal(), "u05", "Pascal's triangle and nCr",
  "Each entry is the sum of the two above it. Row n gives the binomial coefficients nCr, so row 4 gives the coefficients of (a + b)⁴.")

# u07 exponential and log graphs
def explog():
    p = Plot(50, 20, 380, 300, (-3, 5), (-3, 5))
    b = p.axes("x", "y", xat=0, yat=0)
    b += [L(p.X(-3), p.Y(-3), p.X(5), p.Y(5), "lm"), T(p.X(4.4), p.Y(4.9), "y = x", "tm", "e", size=12)]
    b += [p.curve(math.exp, -3, math.log(5), cls="ac"), p.curve(math.log, math.exp(-3), 5, cls="gl")]
    b += [T(p.X(1.3), p.Y(4.6), "y = eˣ", "ta", "e", size=14), T(p.X(4.9), p.Y(1.0), "y = ln x", "tg", "e", size=14)]
    b += [C(p.X(0), p.Y(1), 3.5, "af"), T(p.X(0) - 6, p.Y(1) - 6, "(0, 1)", "ta", "e", size=12), C(p.X(1), p.Y(0), 3.5, "gf"), T(p.X(1) + 6, p.Y(0) + 18, "(1, 0)", "tg", size=12)]
    return svg(470, 336, b)
D["exp-log-graphs"] = (explog(), "u07", "Logarithms",
  "y = ln x is the inverse of y = eˣ, so its graph is the reflection in y = x. eˣ is always positive and passes through (0, 1); ln x is only defined for x > 0 and passes through (1, 0).")

# u10 vectors
def vectors():
    b = []
    O, A, B = (60, 260), (180, 80), (400, 180)
    b += [C(*O, 3.5, "cf"), T(O[0] - 8, O[1] + 16, "O", "", "e", size=14), T(A[0] - 8, A[1] - 8, "A", "", "e", size=14), T(B[0] + 8, B[1] + 6, "B", "", size=14)]
    b += [L(*O, *A, "ac", "aa"), T(100, 160, "a", "ta", "e", size=16)]
    b += [L(*O, *B, "ac", "aa"), T(240, 240, "b", "ta", "m", size=16)]
    b += [L(*A, *B, "gl", "ag"), T(300, 112, "AB = b − a", "tg", size=15)]
    M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    b += [C(*M, 4, "gf"), T(M[0] - 10, M[1] + 22, "M", "tg", "e", size=13), L(*O, *M, "lm", "am")]
    return svg(480, 290, b)
D["vectors"] = (vectors(), "u10", "Position vectors and geometry",
  "With position vectors a and b, the vector from A to B is b − a (go back along a, then along b). The midpoint M of AB has position vector a + ½(b − a) = ½(a + b).")

# u11 box plot
def boxplot():
    b = []
    X = lambda v: 40 + v * 4
    q = dict(mn=12, q1=34, med=46, q3=58, mx=80, out=98)
    y = 90
    b += [L(X(0), 160, X(100) + 8, 160, "ln", "ah")]
    for v in range(0, 101, 20): b += [L(X(v), 160, X(v), 166), T(X(v), 182, str(v), "tm", "m", size=12)]
    b += [L(X(q["mn"]), y, X(q["q1"]), y, "ln"), L(X(q["q3"]), y, X(q["mx"]), y, "ln"), L(X(q["mn"]), y - 12, X(q["mn"]), y + 12, "ln"), L(X(q["mx"]), y - 12, X(q["mx"]), y + 12, "ln")]
    b += [R(X(q["q1"]), y - 24, X(q["q3"]) - X(q["q1"]), 48, "at", rx=2), L(X(q["med"]), y - 24, X(q["med"]), y + 24, "ac thick")]
    b += [T(X(q["out"]), y + 5, "×", "", "m", size=16), T(X(q["out"]), y - 14, "outlier", "tm", "m", size=11)]
    for k, lab in (("mn", "min"), ("q1", "Q₁"), ("med", "median"), ("q3", "Q₃"), ("mx", "max")):
        b.append(T(X(q[k]), y - 32 if k in ("q1", "med", "q3") else y - 18, lab, "ta" if k == "med" else "tm", "m", size=12))
    b += [L(X(q["q1"]), 132, X(q["q3"]), 132, "ln", "ah", start=True), T(X(46), 148, "IQR = Q₃ − Q₁ = 24", "", "m", size=12)]
    b += [T(240, 212, "outlier rule: more than 1.5 × IQR beyond a quartile (58 + 36 = 94)", "tm", "m", size=12)]
    return svg(480, 222, b)
D["box-plot"] = (boxplot(), "u11", "Diagrams",
  "A box plot shows the median, the quartiles and the spread. Here IQR = 24, so any value above 58 + 1.5 × 24 = 94 is an outlier; the whisker stops at the largest value that isn't one.")

# u12 Venn diagram
def venn():
    b = []
    b += [R(30, 20, 420, 220, "bx", rx=8), T(440, 40, "S", "tm", "e", size=14)]
    b += [C(190, 130, 80, "at"), C(290, 130, 80, "at"), T(150, 134, "0.3", "", "m", size=16), T(240, 134, "0.2", "ta", "m", size=16), T(330, 134, "0.25", "", "m", size=16), T(410, 220, "0.25", "tm", "m", size=14)]
    b += [T(130, 60, "A", "", "m", size=16), T(350, 60, "B", "", "m", size=16)]
    b += [T(240, 262, "P(A ∪ B) = 0.3 + 0.2 + 0.25 = 0.75;  P(A ∩ B) = 0.2", "", "m", size=13)]
    return svg(480, 274, b)
D["venn"] = (venn(), "u12", "Diagrams",
  "The overlap is P(A ∩ B) = 0.2. P(A) = 0.5 and P(B) = 0.45, and P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = 0.75. All four regions add up to 1. Since 0.5 × 0.45 ≠ 0.2, A and B aren't independent.")

# u13 binomial distribution
def binom():
    n, pr = 10, 0.3
    P = [math.comb(n, k) * pr**k * (1 - pr)**(n - k) for k in range(n + 1)]
    p = Plot(50, 30, 390, 190, (-0.7, 10.7), (0, 0.3))
    b = p.axes("x", "P(X = x)")
    for k in range(n + 1):
        b.append(R(p.X(k) - 12, p.Y(P[k]), 24, p.Y(0) - p.Y(P[k]), "at" if k == 3 else "bx", rx=2))
        b.append(T(p.X(k), p.Y(0) + 18, str(k), "tm", "m", size=12))
    for y in (0.1, 0.2, 0.3): b += p.ytick(y, f"{y:.1f}")
    b += [L(p.X(3), p.Y(0.29), p.X(3), p.Y(P[3]), "lm"), T(p.X(3) + 6, p.Y(0.285), "mean np = 3", "ta", size=13)]
    b += [T(p.X(10.5), p.Y(0.22), "X ~ B(10, 0.3)", "", "e", size=14), T(p.X(10.5), p.Y(0.22) + 18, f"P(X = 3) = {P[3]:.4f}", "tm", "e", size=12)]
    return svg(470, 260, b), P[3]
_b = binom()
D["binomial"] = (_b[0], "u13", "Binomial model",
  f"X ~ B(10, 0.3): 10 independent trials, each with P(success) = 0.3. The most likely value is 3, which is also the mean np. P(X = 3) = 10C3 × 0.3³ × 0.7⁷ = {_b[1]:.4f}.")

# u17 modulus graph
def modulus():
    p = Plot(50, 20, 380, 260, (-1, 5), (-4, 6))
    b = p.axes("x", "y", xat=0, yat=0)
    b += [p.curve(lambda x: 2 * x - 4, -0.2, 5, cls="lm")]
    b += [p.curve(lambda x: abs(2 * x - 4), -1, 5, cls="ac")]
    b += [C(p.X(2), p.Y(0), 4, "af"), T(p.X(2) + 10, p.Y(0) + 20, "(2, 0)", "ta", size=12)]
    b += [T(p.X(0) + 8, p.Y(4) + 4, "(0, 4)", "ta", size=12), T(p.X(4.4), p.Y(5.6), "y = |2x − 4|", "ta", "e", size=14), T(p.X(1.2), p.Y(-3), "y = 2x − 4", "tm", size=13)]
    b += [T(p.X(1.6), p.Y(-1.2), "reflected up", "tm", "e", size=11)]
    return svg(470, 300, b)
D["modulus"] = (modulus(), "u17", "Modulus",
  "To sketch y = |f(x)|, draw y = f(x) and reflect any part below the x-axis up into it. Here the V has its vertex at (2, 0). To solve |2x − 4| = k, find where a horizontal line meets both arms.")

# u19 geometric series convergence
def geo():
    p = Plot(50, 30, 390, 200, (0.4, 8.6), (0, 2.2))
    b = p.axes("n", "Sₙ")
    S = 0
    for n in range(1, 9):
        S += 0.5 ** (n - 1)
        b += [R(p.X(n) - 14, p.Y(S), 28, p.Y(0) - p.Y(S), "at", rx=2), T(p.X(n), p.Y(0) + 18, str(n), "tm", "m", size=12)]
    b += [L(p.X(0.4), p.Y(2), p.X(8.6), p.Y(2), "ac"), T(p.X(8.6), p.Y(2) - 8, "S∞ = a ÷ (1 − r) = 2", "ta", "e", size=13)]
    b += [T(p.X(3), p.Y(2) - 8, "1 + ½ + ¼ + …", "", "m", size=14)]
    for y in (1, 2): b += p.ytick(y, str(y))
    return svg(470, 260, b)
D["geometric-series"] = (geo(), "u19", "Geometric sequences and series",
  "With a = 1 and r = ½, each term halves, so the partial sums Sₙ get ever closer to 2 without reaching it. A geometric series converges only when |r| < 1, and then S∞ = a ÷ (1 − r).")

# u20 radians: sector
def sector():
    b = []
    cx, cy, r = 120, 220, 180
    th = 1.0
    ex, ey = cx + r * math.cos(th), cy - r * math.sin(th)
    b += [f'<path d="M{cx},{cy} L{cx + r},{cy} A{r},{r} 0 0 0 {f(ex)},{f(ey)} Z" class="at"/>']
    b += [P(f"M{cx + r},{cy} A{r},{r} 0 0 0 {f(ex)},{f(ey)}", "ac thick")]
    b += [P(f"M{cx + 40},{cy} A40,40 0 0 0 {f(cx + 40 * math.cos(th))},{f(cy - 40 * math.sin(th))}", "ln"), T(cx + 50, cy - 16, "θ", "", size=15)]
    b += [T(cx + r / 2, cy + 20, "r", "", "m", size=15), T(cx + 70, cy - 110, "r", "", "e", size=15)]
    b += [T(cx + r * math.cos(th / 2) + 12, cy - r * math.sin(th / 2), "arc s = rθ", "ta", size=14)]
    b += [T(330, 30, "θ in radians", "", size=14), T(330, 52, "area = ½r²θ", "", size=14), T(330, 74, "π rad = 180°", "tm", size=13), T(330, 94, "1 rad ≈ 57.3°", "tm", size=13)]
    b += [T(cx + 70, cy - 40, "½r²θ", "ta", "m", size=13)]
    return svg(480, 240, b)
D["radians"] = (sector(), "u20", "Radians",
  "One radian is the angle where the arc length equals the radius. With θ in radians, arc length s = rθ and sector area = ½r²θ. Convert using π radians = 180°.")

# u21 R and alpha triangle
def ralpha():
    b = []
    A, B, Cc = (60, 220), (360, 220), (360, 60)
    b += [poly([A, B, Cc], "at", closed=True)]
    b += [R(344, 204, 16, 16, "lm", rx=0)]
    b += [T(210, 244, "R cos α = a  (here a = 4)", "", "m", size=13), T(372, 145, "R sin α = b", "", size=13), T(372, 163, "(here b = 3)", "tm", size=12), T(196, 126, "R", "ta", "e", size=16)]
    b += [P(f"M{A[0] + 60},{A[1]} A60,60 0 0 0 {f(A[0] + 60 * math.cos(math.atan(160 / 300)))},{f(A[1] - 60 * math.sin(math.atan(160 / 300)))}", "ln"), T(A[0] + 70, A[1] - 10, "α", "", size=15)]
    b += [T(20, 28, "4 sin θ + 3 cos θ = R sin(θ + α)", "", size=14), T(20, 48, "R = √(4² + 3²) = 5, tan α = 3 ÷ 4, α ≈ 36.9°", "tm", size=12)]
    return svg(480, 256, b)
D["r-alpha"] = (ralpha(), "u21", "R cos(θ ± α) and R sin(θ ± α)",
  "Expanding R sin(θ + α) = R sin θ cos α + R cos θ sin α and matching with 4 sin θ + 3 cos θ gives R cos α = 4 and R sin α = 3. These are the sides of a right-angled triangle, so R = 5 and tan α = 3 ÷ 4.")

# u22 parametric curve
def param():
    p = Plot(60, 20, 360, 260, (-0.5, 9.5), (-6.5, 6.5))
    b = p.axes("x", "y", xat=0, yat=0)
    pts = [p.pt(t * t, 2 * t) for t in [i / 40 for i in range(-120, 121)]]
    b.append(poly(pts, "ac"))
    for t in (-3, -2, -1, 0, 1, 2, 3):
        dy = -8 if t > 0 else (16 if t < 0 else 5)
        if abs(t) == 1: dx_, dy, an = 10, (20 if t > 0 else -10), "start"
        elif t == 0: dx_, dy, an = -10, -8, "e"
        else: dx_, dy, an = -8, dy, "e"
        b += [C(p.X(t * t), p.Y(2 * t), 4, "af"), T(p.X(t * t) + dx_, p.Y(2 * t) + dy, f"t = {t}".replace("-", "−"), "tm", an, size=11)]
    b += [T(p.X(1.0), p.Y(6.1), "x = t², y = 2t", "", size=14), T(p.X(1.0), p.Y(6.1) + 18, "Cartesian: y² = 4x", "ta", size=13)]
    return svg(470, 300, b)
D["parametric"] = (param(), "u22", "Parametric equations",
  "Each value of the parameter t gives one point (t², 2t). Eliminating t (t = y ÷ 2, so x = y² ÷ 4) gives the Cartesian equation y² = 4x.")

# u24 concavity and inflection
def concave():
    p = Plot(50, 20, 380, 260, (-2.6, 2.6), (-3.5, 3.5))
    fx = lambda x: x**3 - 3 * x
    b = p.axes("x", "y", xat=0, yat=0)
    b += [p.curve(fx, -2.15, 0, cls="gl"), p.curve(fx, 0, 2.15, cls="ac")]
    b += [C(p.X(-1), p.Y(2), 4, "cf"), T(p.X(-1), p.Y(2) - 10, "max: f″ < 0", "", "m", size=12)]
    b += [C(p.X(1), p.Y(-2), 4, "cf"), T(p.X(1), p.Y(-2) + 22, "min: f″ > 0", "", "m", size=12)]
    b += [C(p.X(0), p.Y(0), 4, "cf"), T(p.X(0) + 12, p.Y(0) + 18, "inflection: f″ = 0", "", size=12)]
    b += [T(p.X(-2.5), p.Y(3.1), "concave (f″ < 0)", "tg", size=13), T(p.X(2.55), p.Y(-3.1), "convex (f″ > 0)", "ta", "e", size=13)]
    return svg(470, 300, b)
D["concavity"] = (concave(), "u24", "Second derivatives, concavity and inflection",
  "y = x³ − 3x. Where f″(x) < 0 the curve is concave (gold) and where f″(x) > 0 it is convex (accent). At the point of inflection f″(x) = 0 and changes sign. Here f″(x) = 6x, so the inflection is at x = 0.")

# u26 limit of a sum
def riemann():
    p = Plot(50, 20, 380, 240, (0, 4.4), (0, 5))
    fx = lambda x: 1 + x * x / 4
    b = p.axes("x", "y")
    dx = 0.5
    for i in range(8):
        x = 0.5 + i * dx
        if x >= 4: break
        b.append(R(p.X(x), p.Y(fx(x)), p.X(x + dx) - p.X(x), p.Y(0) - p.Y(fx(x)), "at", rx=0))
    b += [p.curve(fx, 0, 4.3, cls="ln")]
    b += [L(p.X(2.5), p.Y(0) + 12, p.X(3.0), p.Y(0) + 12, "ln", "ah", start=True), T(p.X(2.75), p.Y(0) + 30, "δx", "", "m", size=13)]
    b += [T(p.X(0.5), p.Y(0) + 20, "a", "", "m", size=13), T(p.X(4), p.Y(0) + 20, "b", "", "m", size=13)]
    b += [T(p.X(0.2), p.Y(4.6), "Σ y δx → ∫ y dx as δx → 0", "", size=14)]
    return svg(470, 296, b)
D["limit-of-sum"] = (riemann(), "u26", "Integration as the limit of a sum",
  "The area under a curve is approximated by thin rectangles of width δx and height y. As δx → 0 the total Σ y δx becomes the exact area, written ∫ y dx from a to b.")

# u28 3D vector
def vec3d():
    b = []
    O = (170, 200)
    ax = {"x": (-0.55, 0.35), "y": (1, 0), "z": (0, -1)}
    S = 150
    def P3(x, y, z):
        return (O[0] + S * (x * ax["x"][0] + y * ax["y"][0] + z * ax["z"][0]), O[1] + S * (x * ax["x"][1] + y * ax["y"][1] + z * ax["z"][1]))
    for k, lab in (("x", "x (i)"), ("y", "y (j)"), ("z", "z (k)")):
        e = P3(*(1.1 if k == c else 0 for c in "xyz"))
        b += [L(*O, *e, "ln", "ah"), T(e[0] + (8 if k != "x" else -6), e[1] + (14 if k == "x" else -4), lab, "tm", "e" if k == "x" else "start", size=13)]
    p = (0.8, 1.0, 0.7)
    Pp = P3(*p); base = P3(p[0], p[1], 0); bx_ = P3(p[0], 0, 0); by_ = P3(0, p[1], 0)
    b += [L(*base, *Pp, "lm"), L(*bx_, *base, "lm"), L(*by_, *base, "lm")]
    b += [L(*O, *Pp, "ac", "aa"), C(*Pp, 4, "af"), T(Pp[0] + 8, Pp[1] - 6, "P(3, 4, 2)", "ta", size=14)]
    b += [T(300, 40, "OP = 3i + 4j + 2k", "", size=14), T(300, 60, "|OP| = √(3² + 4² + 2²) = √29", "tm", size=12)]
    return svg(480, 284, b)
D["vectors-3d"] = (vec3d(), "u28", "3D vectors",
  "A point in 3D is reached by moving along x, then y, then z. Its position vector is 3i + 4j + 2k and its distance from the origin is √(3² + 4² + 2²) = √29.")

# u29 tree diagram
def tree():
    b = []
    S = (30, 140)
    A, A_ = (170, 70), (170, 210)
    b += [C(*S, 4, "cf"), L(*S, *A, "ln"), L(*S, *A_, "ln"), T(95, 92, "0.3", "", "e", size=13), T(95, 200, "0.7", "", "e", size=13)]
    b += [T(A[0] + 10, A[1] + 5, "R", "", size=15), T(A_[0] + 10, A_[1] + 5, "R′", "", size=15)]
    leaves = [(A, (330, 34), "L", "0.9", True), (A, (330, 106), "L′", "0.1", False), (A_, (330, 174), "L", "0.4", True), (A_, (330, 246), "L′", "0.6", False)]
    for st, en, lab, pr, hl in leaves:
        s0 = (st[0] + 30, st[1])
        b += [L(*s0, *en, "ac" if lab == "L" else "ln"), T((s0[0] + en[0]) / 2, (s0[1] + en[1]) / 2 - 6, pr, "ta" if lab == "L" else "", "m", size=13), T(en[0] + 8, en[1] + 5, lab, "", size=15)]
    b += [T(380, 39, "0.27", "ta", size=13), T(380, 111, "0.03", "tm", size=13), T(380, 179, "0.28", "ta", size=13), T(380, 251, "0.42", "tm", size=13)]
    b += [T(240, 284, "P(L) = 0.27 + 0.28 = 0.55;  P(R | L) = 0.27 ÷ 0.55 ≈ 0.491", "", "m", size=13)]
    return svg(480, 296, b)
D["tree-diagram"] = (tree(), "u29", "Tree diagrams",
  "R = it rains (0.3), L = late. The second branches are conditional probabilities, e.g. P(L | R) = 0.9. Multiply along branches, add the outcomes you want: P(L) = 0.55. Then P(R | L) = P(R ∩ L) ÷ P(L).")

# u31 correlation scatter panels
def scatter():
    import random
    rnd = random.Random(7)
    b = []
    panels = [("positive", 1), ("negative", -1), ("none", 0)]
    for i, (n, sgn) in enumerate(panels):
        p = Plot(14 + i * 156, 30, 136, 136, (0, 10), (0, 10))
        b += [L(p.x0, p.Y(0), p.x0 + p.w, p.Y(0), "ln"), L(p.x0, p.Y(0), p.x0, p.y0, "ln"), T(p.x0 + p.w / 2, 20, n, "", "m", size=13)]
        for _ in range(22):
            x = rnd.uniform(0.5, 9.5)
            y = (5 + sgn * (x - 5) * 0.8 + rnd.gauss(0, 1.1)) if sgn else rnd.uniform(0.5, 9.5)
            y = max(0.3, min(9.7, y))
            b.append(C(p.X(x), p.Y(y), 3.2, "af"))
        r = {1: "r close to +1", -1: "r close to −1", 0: "r close to 0"}[sgn]
        b.append(T(p.x0 + p.w / 2, 190, r, "tm", "m", size=12))
    b += [T(240, 214, "correlation doesn't prove causation", "tm", "m", size=12)]
    return svg(480, 224, b)
D["correlation"] = (scatter(), "u31", "Correlation",
  "The product moment correlation coefficient r measures how close the points are to a straight line: near +1 or −1 is strong linear correlation, near 0 is none. Test H₀: ρ = 0 against the critical value for your sample size.")

# u33 calculus chain
def chain():
    b = []
    rows = [("displacement s", "s = t³ − 6t²", 40), ("velocity v", "v = ds/dt = 3t² − 12t", 130), ("acceleration a", "a = dv/dt = 6t − 12", 220)]
    for n, eq, y in rows:
        b += [R(120, y - 22, 240, 50, "bx"), T(240, y - 1, n, "", "m", size=14), T(240, y + 18, eq, "tm", "m", size=12)]
    for y in (68, 158):
        b += [L(120, y, 120, y + 40, "ac", "aa"), T(112, y + 26, "differentiate", "ta", "e", size=12)]
        b += [L(360, y + 40, 360, y, "gl", "ag"), T(368, y + 26, "integrate", "tg", size=12), T(368, y + 42, "(+ c)", "tg", size=11)]
    b += [T(240, 276, "at rest: v = 0 → t = 0 or t = 4", "", "m", size=13)]
    return svg(480, 288, b)
D["kinematics-calculus"] = (chain(), "u33", "Calculus in kinematics",
  "When acceleration isn't constant, suvat doesn't apply. Differentiate to go from displacement to velocity to acceleration; integrate (adding a constant, found from initial conditions) to go back.")
