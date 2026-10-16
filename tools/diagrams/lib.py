"""Tiny helpers for hand-built, theme-aware SVG diagrams.
Classes are styled by the hub template (.fig ...): ln line, lm dashed muted, bx box,
ac accent line, gl gold line, at/gt tinted fills, af/gf/cf/mf solid fills, tm muted text,
ta accent text, tg gold text, gap (background-coloured stroke to make a line crossing)."""
import math

def svg(w, h, body):
    defs = ('<defs>'
            '<marker id="ah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="cf"/></marker>'
            '<marker id="aa" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="af"/></marker>'
            '<marker id="ag" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="gf"/></marker>'
            '<marker id="am" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="mf"/></marker>'
            '</defs>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">{defs}{"".join(body)}</svg>\n'

def f(v): return f"{v:.1f}".rstrip("0").rstrip(".")

def T(x, y, s, cls="", a="start", rot=None, size=None):
    c = f' class="{cls}"' if cls else ""
    an = "" if a == "start" else f' text-anchor="{"middle" if a=="m" else "end"}"'
    r = f' transform="rotate({rot} {f(x)} {f(y)})"' if rot is not None else ""
    sz = f' font-size="{size}"' if size else ""
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{f(x)}" y="{f(y)}"{c}{an}{r}{sz}>{s}</text>'

def L(x1, y1, x2, y2, cls="ln", arrow=None, start=False, extra=""):
    m = ""
    if arrow: m = f' marker-end="url(#{arrow})"' + (f' marker-start="url(#{arrow})"' if start else "")
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" class="{cls}"{m}{extra}/>'

def P(d, cls="ln", arrow=None, extra=""):
    m = f' marker-end="url(#{arrow})"' if arrow else ""
    return f'<path d="{d}" class="{cls}"{m}{extra}/>'

def poly(pts, cls="ln", arrow=None, closed=False):
    d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + (" Z" if closed else "")
    return P(d, cls, arrow)

def R(x, y, w, h, cls="bx", rx=6, extra=""):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" class="{cls}"{extra}/>'

def C(x, y, r, cls="ln"):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" class="{cls}"/>'

class Plot:
    """Maps data coords to a pixel box (x0,y0 = top-left of plot area)."""
    def __init__(s, x0, y0, w, h, xr, yr):
        s.x0, s.y0, s.w, s.h, s.xr, s.yr = x0, y0, w, h, xr, yr
    def X(s, x): return s.x0 + (x - s.xr[0]) / (s.xr[1] - s.xr[0]) * s.w
    def Y(s, y): return s.y0 + s.h - (y - s.yr[0]) / (s.yr[1] - s.yr[0]) * s.h
    def pt(s, x, y): return (s.X(x), s.Y(y))
    def curve(s, fn, a, b, n=160, cls="ln", arrow=None):
        pts = [s.pt(a + (b - a) * i / n, fn(a + (b - a) * i / n)) for i in range(n + 1)]
        return poly(pts, cls, arrow)
    def area(s, fn, a, b, base=0, cls="at", n=120):
        pts = [s.pt(a, base)] + [s.pt(a + (b - a) * i / n, fn(a + (b - a) * i / n)) for i in range(n + 1)] + [s.pt(b, base)]
        d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + " Z"
        return f'<path d="{d}" class="{cls}" stroke="none"/>'
    def axes(s, xlab="", ylab="", xat=None, yat=None, origin_label=None):
        xa = s.Y(yat if yat is not None else s.yr[0])
        ya = s.X(xat if xat is not None else s.xr[0])
        out = [L(s.x0, xa, s.x0 + s.w + 8, xa, "ln", "ah"), L(ya, s.y0 + s.h, ya, s.y0 - 8, "ln", "ah")]
        if xlab: out.append(T(s.x0 + s.w + 8, xa - 8, xlab, "tm", "e"))
        if ylab: out.append(T(ya + 8, s.y0 - 4, ylab, "tm"))
        if origin_label: out.append(T(ya - 6, xa + 16, origin_label, "tm", "e"))
        return out
    def xtick(s, x, lab, yat=None):
        y = s.Y(yat if yat is not None else s.yr[0])
        return [L(s.X(x), y, s.X(x), y + 5), T(s.X(x), y + 20, lab, "tm", "m")]
    def ytick(s, y, lab, xat=None):
        x = s.X(xat if xat is not None else s.xr[0])
        return [L(x - 5, s.Y(y), x, s.Y(y)), T(x - 9, s.Y(y) + 5, lab, "tm", "e")]

def legend(items, x, y, gap=24, size=13, row=False, spacing=150):
    """items: (line class, text class, label). Vertical list, or one row if row=True."""
    out = []
    for i, (lc, tc, lab) in enumerate(items):
        X, Y = (x + i * spacing, y) if row else (x, y + i * gap)
        out += [L(X, Y - 4, X + 22, Y - 4, lc), T(X + 28, Y + 1, lab, tc, size=size)]
    return out
