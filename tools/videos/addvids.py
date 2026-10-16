import sys, re, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from videos import BIO, CHEM
path, which = sys.argv[1], sys.argv[2]
V = BIO if which == 'bio' else CHEM
lines = open(path).read().split('\n'); out = []; n = None; done = set()
for ln in lines:
    if ln.startswith('  videos:') or ln.startswith('    - yt:') or ln.startswith('      title:') or ln.startswith('      by:'):
        continue  # idempotent: drop old video lines
    out.append(ln)
    m = re.match(r'- n: (\d+)$', ln)
    if m: n = int(m.group(1))
    if ln.startswith('  title:') and n in V:
        out.append('  videos:')
        for yt, t, by in V[n]:
            out += [f'    - yt: "{yt}"', f'      title: {json.dumps(t, ensure_ascii=False)}', f'      by: {json.dumps(by, ensure_ascii=False)}']
        done.add(n)
assert done == set(V), (done, set(V))
open(path, 'w').write('\n'.join(out)); print(path, 'videos added to', len(done))
