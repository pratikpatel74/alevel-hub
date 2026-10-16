from lib import *
import math
D = {}

# 1. Transformations
def transf():
    p = Plot(40, 20, 400, 260, (-4, 5), (-1, 9))
    b = p.axes("x", "y", xat=0, yat=0)
    f0 = lambda x: x * x / 2
    b += [p.curve(f0, -4, 4, cls="ln"), p.curve(lambda x: f0(x) + 3, -3.4, 3.4, cls="ac"), p.curve(lambda x: f0(x - 2), -1.8, 5, cls="gl")]
    b += legend([("ln", "", "y = f(x)"), ("ac", "ta", "y = f(x) + 3"), ("gl", "tg", "y = f(x − 2)")], 40, 316, row=True, spacing=140)
    b += [L(p.X(0), p.Y(0), p.X(0), p.Y(3) + 3, "ac", "aa"), L(p.X(0), p.Y(0) - 10, p.X(2) - 3, p.Y(0) - 10, "gl", "ag")]
    b += [T(p.X(-0.15), p.Y(1.6), "up 3", "ta", "e", size=12), T(p.X(1), p.Y(0) + 18, "right 2", "tg", "m", size=12)]
    return svg(470, 326, b)
D["transformations"] = (transf(), "u03", "Transformations of y = f(x)",
  "Adding outside the function moves the graph **up**: f(x) + 3 is 3 units up. Changing x inside moves it **sideways the opposite way** to the sign: f(x − 2) is 2 units to the right.")

# 2. Circle
def circle():
    b = []
    cx, cy, r = 220, 160, 110
    b += [L(30, 290, 450, 290, "ln", "ah"), L(40, 300, 40, 12, "ln", "ah"), T(450, 282, "x", "tm", "e"), T(48, 20, "y", "tm")]
    b += [C(cx, cy, r, "ac"), C(cx, cy, 3.5, "cf"), T(cx - 8, cy + 20, "(a, b)", "", "e", size=14)]
    a = math.radians(40); px, py = cx + r * math.cos(a), cy - r * math.sin(a)
    b += [L(cx, cy, px, py, "ln"), T((cx + px) / 2 - 10, (cy + py) / 2 - 8, "r", "", "e", size=16), C(px, py, 3.5, "cf")]
    dx, dy = -math.sin(a), -math.cos(a)
    b += [L(px - 70 * dx, py - 70 * dy, px + 90 * dx, py + 90 * dy, "gl"), T(px + 10, py - 50, "tangent ⟂ radius", "tg", size=13)]
    b += [T(cx, 300 - 4, "", ""), T(450, 262, "(x − a)² + (y − b)² = r²", "", "e", size=15)]
    return svg(470, 310, b)
D["circle"] = (circle(), "u04", "Circles",
  "A circle with centre (a, b) and radius r has equation (x − a)² + (y − b)² = r². The tangent at any point is perpendicular to the radius there, so its gradient is −1 ÷ (gradient of the radius).")

# 3. sin and cos
def trig():
    p = Plot(50, 20, 400, 200, (0, 360), (-1.3, 1.3))
    b = p.axes("x°", "y", yat=0)
    for x in (90, 180, 270, 360): b += p.xtick(x, str(x), yat=-1.3)
    for y in (-1, 1): b += p.ytick(y, str(y).replace("-", "−"))
    b += [L(p.X(0), p.Y(1), p.X(360), p.Y(1), "lm"), L(p.X(0), p.Y(-1), p.X(360), p.Y(-1), "lm")]
    b += [p.curve(lambda x: math.sin(math.radians(x)), 0, 360, cls="ac"), p.curve(lambda x: math.cos(math.radians(x)), 0, 360, cls="gl")]
    b += legend([("ac", "ta", "y = sin x"), ("gl", "tg", "y = cos x")], 60, 270, row=True, spacing=140)
    for x in (90, 180, 270, 360): b.append(L(p.X(x), p.Y(-1.3), p.X(x), p.Y(1.3), "lm", extra=' stroke-opacity="0.35"'))
    return svg(470, 282, b)
D["trig-graphs"] = (trig(), "u06", "Exact values and graphs",
  "Both graphs repeat every 360° and stay between −1 and 1. cos x is sin x shifted 90° to the left. Use the symmetry to find second solutions: sin x = sin(180° − x) and cos x = cos(360° − x).")

# 4. Tangent and normal
def tn():
    p = Plot(40, 20, 400, 260, (-1, 4), (-1, 6))
    b = p.axes("x", "y", xat=0, yat=0)
    fx = lambda x: 0.5 * x * x
    b.append(p.curve(fx, -1, 3.4, cls="ln"))
    x0 = 2; y0 = fx(x0); m = x0
    b += [p.curve(lambda x: y0 + m * (x - x0), 0.6, 3.4, cls="ac"), p.curve(lambda x: y0 - (x - x0) / m, -0.6, 4, cls="gl")]
    b += [C(p.X(x0), p.Y(y0), 4, "cf"), T(p.X(x0) + 8, p.Y(y0) + 22, "(2, 2)", "", size=13)]
    b += [T(p.X(2.6), p.Y(4.6), "tangent, gradient 2", "ta", "e", size=13), T(p.X(4), p.Y(1.0) + 24, "normal, gradient −½", "tg", "e", size=13)]
    b += [T(p.X(-0.9), p.Y(5.6), "y = ½x²", "", size=13)]
    return svg(470, 300, b)
D["tangent-normal"] = (tn(), "u08", "Tangents and normals",
  "For y = ½x², dy/dx = x, so at (2, 2) the tangent has gradient 2. The normal is perpendicular, so its gradient is −1 ÷ 2 = −½. Then use y − y₁ = m(x − x₁).")

# 5. Area above and below the axis
def area():
    p = Plot(40, 20, 400, 240, (-0.5, 4.5), (-2.5, 3.5))
    fx = lambda x: x * (x - 3) * (x - 4) / 2
    b = [p.area(fx, 0, 3, cls="at"), p.area(fx, 3, 4, cls="gt")]
    b += p.axes("x", "y", xat=0, yat=0)
    b.append(p.curve(fx, -0.3, 4.4, cls="ln"))
    for x in (3, 4): b.append(T(p.X(x), p.Y(0) + 18, str(x), "tm", "m"))
    b += [T(p.X(1.3), p.Y(0.9), "integral positive", "ta", "m", size=13), T(p.X(3.5), p.Y(-1.3) + 6, "integral", "tg", "m", size=12), T(p.X(3.5), p.Y(-1.3) + 20, "negative", "tg", "m", size=12)]
    return svg(470, 290, b)
D["area-under-curve"] = (area(), "u09", "Areas",
  "An integral counts area below the x-axis as negative. When a curve crosses the axis, integrate each part separately (here 0 to 3, then 3 to 4) and add the sizes of the areas.")

# 6. Critical region for a binomial test
def crit():
    n, pr = 20, 0.5
    P = [math.comb(n, k) * pr**k * (1 - pr)**(n - k) for k in range(n + 1)]
    cum = lambda k: sum(P[:k + 1])
    p = Plot(50, 30, 400, 200, (-0.7, 20.7), (0, 0.19))
    b = p.axes("x", "P(X = x)")
    for k in range(n + 1):
        cls = "at" if cum(k) <= 0.05 else "bx"
        b.append(R(p.X(k) - 7, p.Y(P[k]), 14, p.Y(0) - p.Y(P[k]), cls, rx=2))
    for k in (0, 5, 10, 15, 20): b.append(T(p.X(k), p.Y(0) + 18, str(k), "tm", "m"))
    b += [L(p.X(-0.4), p.Y(0) + 32, p.X(5.4), p.Y(0) + 32, "ac"), T(p.X(2.5), p.Y(0) + 50, "critical region X ≤ 5", "ta", "m", size=13)]
    b += [T(p.X(13), p.Y(0.17), f"P(X ≤ 5) = {cum(5):.4f} ✓", "", size=12), T(p.X(13), p.Y(0.17) + 18, f"P(X ≤ 6) = {cum(6):.4f} ✗", "tm", size=12), T(p.X(13), p.Y(0.17) + 36, "(5% level)", "tm", size=12)]
    return svg(470, 290, b), cum(5), cum(6)
_c = crit()
D["critical-region"] = (_c[0], "u14", "Critical regions",
  f"X ~ B(20, 0.5), testing H₁: p < 0.5 at the 5% level. P(X ≤ 5) = {_c[1]:.4f} is below 0.05 but P(X ≤ 6) = {_c[2]:.4f} isn't, so the critical region is X ≤ 5. The actual significance level is {_c[1] * 100:.2f}%.")

# 7. Velocity–time graph
def vt():
    p = Plot(50, 30, 370, 220, (0, 10), (0, 12))
    b = [p.area(lambda t: 4 * t if t < 2.5 else (10 if t < 7 else 10 - 10 * (t - 7) / 3), 0, 10, cls="at")]
    b += p.axes("", "v / m s⁻¹") + [T(p.X(10) + 14, p.Y(0) + 5, "t / s", "tm", size=12)]
    b.append(poly([p.pt(0, 0), p.pt(2.5, 10), p.pt(7, 10), p.pt(10, 0)], "ac"))
    for x, lab in ((2.5, "2.5"), (7, "7"), (10, "10")): b += p.xtick(x, lab)
    b += p.ytick(10, "10")
    b += [T(p.X(0.3), p.Y(10.9), "gradient = acceleration", "", size=12)]
    b += [T(p.X(4.8), p.Y(4.8), "area = displacement", "ta", "m", size=13), T(p.X(4.8), p.Y(4.8) + 18, "= 72.5 m", "ta", "m", size=13)]
    b += [T(p.X(8.75), p.Y(7.6), "deceleration", "", size=12)]
    return svg(470, 270, b)
D["vt-graph"] = (vt(), "u15", "Motion graphs",
  "On a velocity–time graph, the gradient is the acceleration and the area under the graph is the displacement. Here: ½ × 2.5 × 10 + 4.5 × 10 + ½ × 3 × 10 = 12.5 + 45 + 15 = 72.5 m.")

# 8. Connected particles over a pulley
def pulley():
    b = []
    b += [R(20, 150, 300, 16, "bx", rx=2), T(30, 190, "smooth table", "tm", size=12)]
    b += [R(120, 104, 60, 46, "at", rx=4), T(150, 132, "A (m₁)", "ta", "m", size=14)]
    b += [C(340, 150, 18, "bx"), L(180, 128, 338, 132, "ln"), L(358, 150, 358, 220, "ln")]
    b += [R(330, 220, 56, 46, "gt", rx=4), T(358, 248, "B (m₂)", "tg", "m", size=13)]
    b += [L(184, 120, 240, 120, "ln", "ah"), T(214, 112, "T", "", "m", size=15)]
    b += [L(372, 214, 372, 172, "ln", "ah"), T(380, 196, "T", "", size=15)]
    b += [L(358, 268, 358, 316, "gl", "ag"), T(366, 306, "m₂g", "tg", size=14)]
    b += [L(150, 168, 150, 212, "lm", "am"), T(158, 206, "m₁g", "tm", size=13), L(150, 102, 150, 60, "lm", "am"), T(158, 70, "R", "tm", size=13)]
    b += [L(410, 230, 410, 270, "ac", "aa"), T(418, 254, "a", "ta", size=15), L(190, 92, 240, 92, "ac", "aa"), T(250, 96, "a", "ta", size=15)]
    b += [T(20, 30, "A: T = m₁a", "", size=14), T(20, 50, "B: m₂g − T = m₂a", "", size=14)]
    return svg(470, 326, b)
D["pulley"] = (pulley(), "u16", "Connected particles",
  "Both particles have the same acceleration a, and the light inextensible string has the same tension T throughout. Write F = ma for each particle separately, in its own direction of motion, then solve the two equations together.")

# 9. Newton–Raphson
def nr():
    p = Plot(40, 20, 400, 240, (0, 3.2), (-2.5, 12))
    fx = lambda x: x**3 - 2 * x - 2
    dfx = lambda x: 3 * x * x - 2
    b = p.axes("x", "y", xat=0, yat=0)
    b.append(p.curve(fx, 0.3, 2.75, cls="ln"))
    x0 = 2.6; x1 = x0 - fx(x0) / dfx(x0)
    b += [L(p.X(x0), p.Y(0), p.X(x0), p.Y(fx(x0)), "lm"), C(p.X(x0), p.Y(fx(x0)), 4, "cf")]
    b += [p.curve(lambda x: fx(x0) + dfx(x0) * (x - x0), x1 - 0.1, x0 + 0.1, cls="ac")]
    b += [C(p.X(x1), p.Y(0), 4, "af"), T(p.X(x0), p.Y(0) + 20, "x₀", "", "m", size=14), T(p.X(x1) - 6, p.Y(0) + 20, "x₁", "ta", "m", size=14)]
    root = 1.7693
    b += [C(p.X(root), p.Y(0), 4, "gf"), T(p.X(root) - 8, p.Y(0) - 10, "root", "tg", "e", size=13)]
    b += [T(p.X(0.15), p.Y(10.5), "x₁ = x₀ − f(x₀) ÷ f′(x₀)", "", size=15), T(p.X(x0) + 8, p.Y(fx(x0)) + 14, "tangent at x₀", "ta", size=12)]
    return svg(470, 290, b), x1
_n = nr()
D["newton-raphson"] = (_n[0], "u27", "Newton–Raphson",
  f"f(x) = x³ − 2x − 2. Start at x₀ = 2.6, follow the tangent down to the x-axis to get x₁ = {_n[1]:.3f}, then repeat from x₁. It fails if f′(x) is close to 0 near the starting point (the tangent is nearly flat).")

# 10. Normal distribution
def normal():
    p = Plot(30, 30, 420, 200, (-3.6, 3.6), (0, 0.45))
    phi = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    b = [p.area(phi, -2, 2, cls="nt"), p.area(phi, -1, 1, cls="at")]
    b += [L(p.X(-3.6), p.Y(0), p.X(3.6), p.Y(0), "ln"), p.curve(phi, -3.6, 3.6, cls="ln")]
    for z, lab in ((-2, "μ − 2σ"), (-1, "μ − σ"), (0, "μ"), (1, "μ + σ"), (2, "μ + 2σ")): b.append(T(p.X(z), p.Y(0) + 20, lab, "tm", "m", size=12))
    b += [T(p.X(0), p.Y(0.17), "68%", "ta", "m", size=15), T(p.X(-2.6), p.Y(0.2), "95% between", "tm", "m", size=12), T(p.X(-2.6), p.Y(0.2) + 16, "μ − 2σ and μ + 2σ", "tm", "m", size=12)]
    b += [L(p.X(0), p.Y(0), p.X(0), p.Y(phi(0)), "lm")]
    return svg(480, 260, b)
D["normal-curve"] = (normal(), "u30", "Properties",
  "The normal curve is symmetrical about the mean μ. About 68% of values lie within 1 standard deviation of the mean and about 95% within 2. Points of inflection are at μ ± σ.")

# 11. Projectile
def proj():
    p = Plot(80, 30, 370, 210, (0, 10), (0, 4.6))
    fx = lambda x: x * (10 - x) * 0.16
    b = [L(p.X(0), p.Y(0), p.X(10) + 10, p.Y(0), "ln"), p.curve(fx, 0, 10, cls="lm")]
    b += [L(p.X(0), p.Y(0), p.X(1.6), p.Y(0) - 92, "ac", "aa"), T(p.X(1.6) + 6, p.Y(0) - 92, "U", "ta", size=16)]
    b += [L(p.X(0), p.Y(0) + 2, p.X(1.6), p.Y(0) + 2, "gl", "ag"), T(p.X(0.8), p.Y(0) + 20, "U cos θ", "tg", "m", size=13)]
    b += [L(p.X(0) - 2, p.Y(0), p.X(0) - 2, p.Y(0) - 92, "gl", "ag"), T(p.X(0) - 8, p.Y(0) - 46, "U sin θ", "tg", "e", size=13)]
    b += [P(f"M{f(p.X(0) + 30)},{f(p.Y(0))} A30,30 0 0 0 {f(p.X(0) + 30 * math.cos(math.atan(92 / (p.X(1.6) - p.X(0)))))},{f(p.Y(0) - 30 * math.sin(math.atan(92 / (p.X(1.6) - p.X(0)))))}", "ln"), T(p.X(0) + 36, p.Y(0) - 10, "θ", "", size=14)]
    b += [L(p.X(5), p.Y(0), p.X(5), p.Y(fx(5)), "lm"), T(p.X(5) + 6, p.Y(1.7), "max height:", "tm", size=12), T(p.X(5) + 6, p.Y(1.7) + 16, "vertical v = 0", "tm", size=12)]
    b += [L(p.X(0), p.Y(0) + 34, p.X(10), p.Y(0) + 34, "ln", "ah", start=True), T(p.X(5), p.Y(0) + 50, "range: vertical displacement = 0", "tm", "m", size=12)]
    return svg(470, 300, b)
D["projectile"] = (proj(), "u32", "Resolving the initial velocity",
  "Split U into U cos θ (horizontal, constant: no acceleration) and U sin θ (vertical, acceleration g downwards). At maximum height the vertical velocity is 0; at the end of the range the vertical displacement is 0.")

# 12. Inclined plane
def incline():
    b = []
    th = math.radians(28)
    A, Bx = (30, 290), (440, 290)
    top = (440, 290 - 410 * math.tan(th))
    b += [poly([A, Bx, top], "bx", closed=True)]
    b += [P(f"M{A[0] + 60},{A[1]} A60,60 0 0 0 {f(A[0] + 60 * math.cos(th))},{f(A[1] - 60 * math.sin(th))}", "ln"), T(A[0] + 72, A[1] - 10, "θ", "", size=15)]
    u = (math.cos(th), -math.sin(th))     # up the slope
    n = (-math.sin(th), -math.cos(th))    # out of the slope
    c = (250, 290 - 220 * math.tan(th))
    w, h = 70, 42
    add = lambda p, v, k: (p[0] + v[0] * k, p[1] + v[1] * k)
    p0, p1 = add(c, u, -w / 2), add(c, u, w / 2)
    b.append(poly([p0, p1, add(p1, n, h), add(p0, n, h)], "at", closed=True))
    g = add(c, n, h / 2)
    def arrow(v, k, cls, mk, lab, tcls, dx=6, dy=0, anchor="start", size=14):
        e = add(g, v, k)
        return [L(g[0], g[1], e[0], e[1], cls, mk), T(e[0] + dx, e[1] + dy, lab, tcls, anchor, size=size)]
    b += arrow((0, 1), 112, "ln", "ah", "mg", "", 8, 6)
    b += arrow(n, 96, "ac", "aa", "R", "ta", 6, 0)
    b += arrow(u, 96, "gl", "ag", "F (friction)", "tg", 6, 0)
    b += arrow((-u[0], -u[1]), 74, "lm", "am", "mg sin θ", "tm", -8, 16, "e", 13)
    b += arrow((-n[0], -n[1]), 64, "lm", "am", "mg cos θ", "tm", 8, 16, "start", 13)
    return svg(480, 300, b)
D["inclined-plane"] = (incline(), "u34", "Inclined planes",
  "Resolve parallel and perpendicular to the slope. Perpendicular: R = mg cos θ. Parallel: the weight component mg sin θ acts down the slope; friction acts up the slope if the particle would slide down. Limiting friction: F = μR.")

# 13. Ladder
def ladder():
    b = []
    b += [L(30, 300, 450, 300, "ln thick"), L(400, 300, 400, 20, "ln thick"), T(408, 34, "smooth wall", "tm", size=12), T(40, 318, "rough ground", "tm", size=12)]
    fx, fy, tx, ty = 170, 300, 400, 60
    b += [L(fx, fy, tx, ty, "ln", extra=' stroke-width="7" stroke-linecap="round"')]
    mx, my = (fx + tx) / 2, (fy + ty) / 2
    b += [L(mx, my, mx, my + 80, "gl", "ag"), T(mx + 8, my + 78, "W", "tg", size=15), C(mx, my, 4, "gf")]
    b += [L(tx, ty, tx - 80, ty, "ac", "aa"), T(tx - 84, ty - 8, "S", "ta", "e", size=15)]
    b += [L(fx, fy, fx, fy - 90, "ac", "aa"), T(fx - 8, fy - 92, "R", "ta", "e", size=15)]
    b += [L(fx, fy - 6, fx + 80, fy - 6, "ac", "aa"), T(fx + 86, fy - 10, "F", "ta", size=15)]
    ang = math.atan2(fy - ty, tx - fx)
    b += [P(f"M{fx + 46},{fy} A46,46 0 0 0 {f(fx + 46 * math.cos(ang))},{f(fy - 46 * math.sin(ang))}", "ln"), T(fx + 54, fy - 14, "θ", "", size=14)]
    b += [T(30, 40, "Resolve: F = S, R = W", "", size=14), T(30, 60, "Moments about the foot:", "", size=14), T(30, 80, "W × (L/2) cos θ = S × L sin θ", "", size=14)]
    return svg(480, 330, b)
D["ladder"] = (ladder(), "u35", "Tilting and ladders",
  "A uniform ladder of length L against a smooth wall: the wall gives only a horizontal reaction S, the ground gives a normal reaction R and friction F towards the wall. Take moments about the foot to remove R and F from the equation.")
