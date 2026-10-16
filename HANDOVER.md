# A-level Study Hubs: handover notes

Read this first if the conversation has been compacted or a new session is picking the work up. Last updated: 16 Oct 2026, 18:30.

## Golden rules

1. **Pratik's Mac folders are the master copy** (table below). Claude's cloud workspace (`/home/claude/...`, `/mnt/user-data/...`) is temporary and gets wiped between sessions. Never rebuild from a cloud copy you didn't just fetch.
2. **Before editing, fetch the current files from the Mac** with `device_stage_files`, or `device_list_dir` to check mtimes first. Edit the fetched copy, rebuild, then write back with `device_commit_files`, passing `expectedMtimeMs` so newer edits aren't overwritten.
3. **One chat per repo at a time.** Two sessions working on the same repo left a stale `.git/HEAD.lock` on 16 Oct. If git says a lock file exists, check `pgrep -l git`, then run `rm -f .git/HEAD.lock .git/index.lock`.
4. **Finance has its own context doc:** `~/Documents/Projects/finance-hub/FINANCE_HUB_CONTEXT.md`. Read it before touching Finance.
5. **Pratik wants short answers** and fully literal, copy-paste terminal commands.

## What exists

Four revision sites plus a landing page. All are static, self-contained `index.html` files hosted on Netlify. Each one auto-deploys when its GitHub repo's `main` branch is pushed.

| Site | Live URL | GitHub repo | Folder on Pratik's Mac |
|---|---|---|---|
| Landing page | https://alevel-study-hubs.netlify.app/ | pratikpatel74/alevel-hub | ~/Documents/Projects/alevel-hub |
| Biology (AQA 7402) | https://aqa-alevel-biology.netlify.app/ | pratikpatel74/alevel-biology | ~/Documents/Projects/alevel-biology |
| Chemistry (AQA 7405) | https://aqa-alevel-chemistry.netlify.app/ | pratikpatel74/alevel-chemistry | ~/Documents/Projects/alevel-chemistry |
| Maths (AQA 7357) | https://aqa-alevel-maths.netlify.app/ | pratikpatel74/alevel-maths | ~/Documents/Projects/alevel-maths |
| Finance (LIBF Unit 1) | https://alevel-finance-hub.netlify.app/ | pratikpatel74/finance-hub | ~/Documents/Projects/finance-hub |

Size of each hub:
- **Biology:** 31 topics, 682 questions, 12 required practicals.
- **Chemistry:** 34 topics, 748 questions, 12 required practicals.
- **Maths:** 35 topics, 770 questions, worked examples in every topic, no practicals.
- **Finance:** 6 topics, 132 questions. It's an older, separate design with one HTML file per quiz and Word summaries. It was built in a different session.

Separate project, not covered here: the Pre-Dentistry hub (repo `pratikpatel74/pre-dentistry-study-guide`, folder `~/Documents/Projects/pre-dentistry-study-guide`, https://pre-dentistry-hub.netlify.app/), built in the Finance style.

## How a hub is built

Each subject repo has this layout:

```
index.html          # the built site (this is what Netlify serves)
netlify.toml        # publish = "."
.gitignore          # .agents/ (created by the Netlify CLI)
README.md
src/
  build.py          # validates content and writes ../index.html
  template.html     # page shell, CSS and JS; DATA is injected at __DATA__
  content/
    site.yaml       # meta (subject, code, title, storage prefix, texts) + plan (sections per year)
    practicals.yaml # list of required practicals ([] for Maths)
    u01.yaml ...    # one file per topic
  diagrams/         # SVG diagrams, referenced by fig: in topic files
```

To rebuild after editing content:

```bash
cd ~/Documents/Projects/alevel-<subject>/src
pip3 install pyyaml
python3 build.py
```

`build.py` refuses to build if a topic doesn't have exactly 22 questions with 4 options each, a valid answer index, an explanation, and no duplicates. It also flags answer positions skewed towards one letter.

### Topic file format (`uNN.yaml`)

```yaml
id: "3.1a"          # used in URLs: #s-<id> (summary), #q-<id> (quiz)
order: 1            # sort order
year: 1             # 1 or 2 (Chemistry and Maths need this; Biology infers it from the plan)
section: "3.1"      # must match a plan code in site.yaml
spec: "3.1.1–3.1.3"
title: "..."
desc: "..."
practicals: [1]     # required practical numbers
summary:
  - h: "Heading"
    p: ["bullet with **bold** and `formula`", "..."]
    fig: heart       # optional: shows src/diagrams/heart.svg under this section
    cap: "Caption"   # required when fig is set
pitfalls: ["..."]
examples:           # Maths only, top-level: {q, steps: [...], a}
questions:
  - q: "..."
    o: ["A", "B", "C", "D"]
    a: 1            # index of the correct option (0-3)
    e: "Explanation shown after answering"
```

### One shared template (since 16 Oct)

`src/template.html` and `src/build.py` are **identical in all three subject repos**. Everything subject-specific lives in `content/site.yaml`:

- `meta`: subject, code, title, storage `prefix`, `rpBlurb`, `rpIntro`, and optionally `heroSub`, `banner` (shown when there are no practicals), and `secColors` (maps section codes like `P` to colour slots 1–8).
- `plan`: the sections per year.

Topic files can also use `badge` (Maths spec letters) and top-level `examples` (worked examples). If you change the template or build script, copy the same file into all three repos and bump `TEMPLATE_VERSION` in `build.py`.

Every template must start with `<!doctype html>` and a `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` tag. The Claude artifact previews add that tag automatically, but Netlify serves the file as it is. Without the tag, phones render the page at desktop width, so cards don't stack (fixed 16 Oct).

On the hub page, every hub's top bar has a "← All subjects" link to the landing page.

### Diagrams

- SVG files live in `src/diagrams/<name>.svg`. A summary section shows one with `fig: <name>` and `cap: "<caption>"` in its `uNN.yaml`. `build.py` inlines the SVG, checks it (needs a `viewBox`, no scripts or styles, caption required), prefixes its ids and adds an `aria-label`.
- Diagrams don't hard-code colours. They use classes styled by the template (`ln` text colour, `ac` section accent, `gl` gold, `at`/`gt` tinted fills, `tm` muted text and so on), so they follow light/dark mode and each section's colour.
- Writing SVGs to the Mac with `device_commit_files` injects a C2PA `<metadata>` block into each file. `build.py` strips it, but clean the files too (remove `<metadata>…</metadata>` and the `xmlns:c2pa` attribute) so the repo stays tidy.
- They are generated by Python scripts in `alevel-hub/tools/diagrams/` (see its README). Edit the script, then run `apply.py` for that subject and rebuild.
- 16 Oct: Biology 34, Chemistry 36, Maths 31 (101 in total). Every topic has at least one, except Maths proof/indices/surds, partial fractions, differentiation techniques and integration techniques, where a picture adds little. Generated by `bio.py`/`bio2.py`, `chem.py`/`chem2.py`, `maths.py`/`maths2.py`. Examples: heart, oxygen dissociation, nephron, sarcomere, action potential, synapse; Maxwell–Boltzmann, Born–Haber, titration curve, cell, NMR splitting, VSEPR shapes; transformations, tangents and normals, critical region, normal curve, projectile, inclined plane, ladder.

### Practical videos

- Each practical in `practicals.yaml` can have a `videos:` list. Each entry has `yt` (the 11-character YouTube id), `title` and `by` (channel). `build.py` checks these.
- The page shows a thumbnail with a play button. Clicking it loads the video from `youtube-nocookie.com`, so YouTube isn't contacted until someone presses play. There's also a "Watch on YouTube" link.
- 16 Oct: all 24 practicals have one (Chemistry RP1 and RP7 have two, for parts a and b): 26 videos in total. Biology: all from Miss Estruch. Chemistry: mostly Dr de Bruin's Classroom, plus The Chem Tutor, Malmesbury Education, Tailored Tutors, St Peter's School, LPGS Chemistry, Mr Carver and Mr Murray-Green.
- Every video was checked as live and embeddable with `https://noembed.com/embed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D<id>` via WebFetch (YouTube's own oEmbed gets cached wrongly by WebFetch, and the cloud shell can't reach YouTube). A title like "OUTDATED" means pick another. Videos can be removed by their owners, so re-check now and then.
- The list lives in `alevel-hub/tools/videos/videos.py`; `addvids.py <practicals.yaml> bio|chem` writes it into the yaml.

### Quiz features (all hubs)

- **Questions:** each attempt draws 10 random questions from the pool of 22.
- **Retrying:** "Retry missed" re-asks only the questions answered wrongly.
- **Timer:** optional, 60 s per question.
- **Keyboard:** 1–4 to answer, Enter for the next question.
- **Saved progress:** score badges, the timer setting and the theme are stored in `localStorage`, separately per site.

## How to deploy changes

Claude **can't push to Pratik's GitHub from the cloud session**, because pushes are refused for this account. The working method is:

1. Fetch the repo's `src/` (and `index.html`) from the Mac with `device_stage_files`. Files land in `/mnt/user-data/uploads/<folder>/`. Copy them into `/mnt/user-data/outputs/alevel-<subject>/` keeping the repo layout, then edit and run `python3 build.py` inside `src/`.
2. Write the changed files to the Mac with the device tools (`device_commit_files` into `~/Documents/Projects/...`). This only works when the Mac is linked and online; `~/Documents/Projects` has been granted before.
3. If the Mac is offline, send a zip with SendUserFile instead.
4. Give Pratik copy-paste commands. He prefers fully literal CLI commands.

```bash
cd ~/Documents/Projects/alevel-<subject>
git add .
git commit -m "<message>"
git push
```

Netlify picks up the push automatically for all five sites. They were connected through the Netlify web portal, and Finance was linked for auto-deploy on 16 Oct. If a push doesn't deploy, check that the site is linked under Site configuration → Build & deploy → Continuous deployment.

After deploying, the live URL can be checked with WebFetch, but it only sees the page title, because the content is built by JavaScript. The cloud shell can't reach netlify.app (the proxy refuses the connection). For real checks, render the local `index.html` with Playwright (Chromium is preinstalled; use `devices['iPhone 13']` for mobile), or ask Pratik to check on his phone.

## Status log

- **Live:** all four hubs and the landing page are deployed and verified.
- **Deployed 15 Oct, 20:26:** the "← All subjects" link on the Biology, Chemistry and Maths hubs, the Maths hero-text fix (it now mentions worked examples instead of required practicals), and this handover file.
- **16 Oct:**
  - Added the mobile viewport fix to Biology, Chemistry and Maths.
  - Added a "← All subjects" link to the Finance hub top bar.
  - Linked Finance to GitHub for auto-deploy in Netlify.
  - All four hubs now auto-deploy on push.
  - Full accuracy read-through of Biology and Chemistry (see Accuracy notes).
  - Unified the three templates into one shared template and build script.
  - Added SVG diagram support and 101 diagrams across the three hubs (40 first, then 61 more so every topic has one).
  - Added embedded tutorial videos to all 24 required practicals (template v3).
  - **Deployed 16 Oct, ~10:50:** Biology `68db971`, Chemistry `290ca10`, Maths `cbec57d`, landing page repo `6eadea5`. All four repos clean after the push.
- **Finance hub fixes** are being handled by Pratik in a separate chat. Known issues:
  - Section 75 is credited to the Consumer Rights Act 2015; it should be the Consumer Credit Act 1974.
  - Minimum payment figures don't match between the summary (3–5% or £25) and the quiz (£10 or 1–2%).
  - The Topic 6 name differs: "Borrowing Products" on the hub, "Credit & Debt" on the quiz.

## Accuracy notes

- All content is original. It is written against the AQA specifications, not copied from paid resources.
- An automated check compared each answer key with its explanation. The flagged questions were reviewed by hand, and the Maths numerical answers were recalculated.
- **Full read-through, 16 Oct:** every Biology and Chemistry question, summary, pitfall and practical was read and calculations re-run. Fixes:
  - Chemistry: two questions had a second correct option (ethyl ethanoate NMR ratio "3:3:2"; butane also has 2 ¹³C peaks). Wrong C₃H₈ precise mass (44.0626 → 44.0624). Wrong argon explanation (it has more electrons, not fewer; the point is it's monatomic). Wording fixes in u01, u03 and u06.
  - Biology: transpiration question didn't match its answers. Clearer monoclonal antibody answer. Codominance example changed to roan cattle.
- The content hasn't had expert review. Pratik was advised to spot-check topics against a textbook or teacher.

## Claude preview artifacts (private, claude.ai)

- Biology: https://claude.ai/artifact/EPkA6U2ryAsfv3o4MTf4UY
- Chemistry: https://claude.ai/artifact/TiYRgDe5fhexrSjJkG37MT
- Maths: https://claude.ai/artifact/1wv8ifHF6zezkrLnacmwab

These are previews only and out of date (published before the "All subjects" link, the shared template and the diagrams). The Netlify sites are the real ones; republish a preview only if Pratik asks.

## Possible next steps (only if Pratik asks)

- **More diagrams:** a second diagram for the busiest topics, or the four skipped Maths topics (use `tools/diagrams`).
- **Practice questions:** add exam-style long-answer questions with mark schemes.
- **Progress page:** add a page on the landing site summarising scores. This would need the scores in one place, because `localStorage` is per site.
- **Finance redesign:** move Finance to the same design as the AQA hubs.
