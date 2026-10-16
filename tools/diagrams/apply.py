"""Write diagrams into a repo and attach them to summary sections.
Usage: python3 apply.py <module> <repo src dir>"""
import sys, importlib, json, re, os
sys.path.insert(0, os.path.dirname(__file__))
mod = importlib.import_module(sys.argv[1])
src = sys.argv[2]
os.makedirs(f"{src}/diagrams", exist_ok=True)
for name, (svgtext, unit, heading, cap) in mod.D.items():
    open(f"{src}/diagrams/{name}.svg", "w").write(svgtext)
    path = f"{src}/content/{unit}.yaml"
    lines = open(path).read().split("\n")
    # drop any earlier fig/cap for this heading, then insert fresh
    out, i, done = [], 0, False
    while i < len(lines):
        ln = lines[i]
        out.append(ln)
        if ln == f'  - h: {json.dumps(heading, ensure_ascii=False)}':
            j = i + 1
            while j < len(lines) and (lines[j].startswith("    fig:") or lines[j].startswith("    cap:")): j += 1
            out.append(f"    fig: {name}")
            out.append(f"    cap: {json.dumps(cap, ensure_ascii=False)}")
            i = j; done = True; continue
        i += 1
    if not done: sys.exit(f"heading not found: {unit} {heading}")
    open(path, "w").write("\n".join(out))
print(f"applied {len(mod.D)} diagrams to {src}")
