# A-level Study Hubs: handover notes

Read this first if the conversation has been compacted or a new session is picking the work up. Last updated: 15 Oct 2026.

## What exists

Four revision sites plus a landing page. All are static, self-contained `index.html` files hosted on Netlify. Each one auto-deploys when its GitHub repo's `main` branch is pushed.

| Site | Live URL | GitHub repo | Folder on Pratik's Mac |
|---|---|---|---|
| Landing page | https://alevel-study-hubs.netlify.app/ | pratikpatel74/alevel-hub | ~/Documents/Projects/alevel-hub |
| Biology (AQA 7402) | https://aqa-alevel-biology.netlify.app/ | pratikpatel74/alevel-biology | ~/Documents/Projects/alevel-biology |
| Chemistry (AQA 7405) | https://aqa-alevel-chemistry.netlify.app/ | pratikpatel74/alevel-chemistry | ~/Documents/Projects/alevel-chemistry |
| Maths (AQA 7357) | https://aqa-alevel-maths.netlify.app/ | pratikpatel74/alevel-maths | ~/Documents/Projects/alevel-maths |
| Finance (LIBF Unit 1) | https://alevel-finance-hub.netlify.app/ | pratikpatel74/finance-hub | ~/Desktop/finance-hub |

Size of each hub:
- **Biology:** 31 topics, 682 questions, 12 required practicals.
- **Chemistry:** 34 topics, 748 questions, 12 required practicals.
- **Maths:** 35 topics, 770 questions, worked examples in every topic, no practicals.
- **Finance:** 6 topics, 132 questions. It's an older, separate design with one HTML file per quiz and Word summaries. It was built in a different session.

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
pitfalls: ["..."]
examples:           # Maths only, top-level: {q, steps: [...], a}
questions:
  - q: "..."
    o: ["A", "B", "C", "D"]
    a: 1            # index of the correct option (0-3)
    e: "Explanation shown after answering"
```

### The templates differ slightly

- **Biology:** the original template. Subject text is hard-coded in it ("AQA 7402", "bio_" storage prefix, and the plan list inside `build.py`).
- **Chemistry:** a generic version. It reads subject, code, prefix and texts from `site.yaml` `meta`, and the plan from `site.yaml`.
- **Maths:** an extended version of the generic template. It supports `badge` (spec letters on cards), top-level `examples` (worked examples), `meta.secColors`, `meta.banner` and `meta.heroSub`. Section codes are `P`, `S` and `M`.

Every template must start with `<!doctype html>` and a `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` tag. The Claude artifact previews add that tag automatically, but Netlify serves the file as it is. Without the tag, phones render the page at desktop width, so cards don't stack (fixed 16 Oct).

On the hub page, every hub's top bar has a "← All subjects" link to the landing page.

### Quiz features (all hubs)

- **Questions:** each attempt draws 10 random questions from the pool of 22.
- **Retrying:** "Retry missed" re-asks only the questions answered wrongly.
- **Timer:** optional, 60 s per question.
- **Keyboard:** 1–4 to answer, Enter for the next question.
- **Saved progress:** score badges, the timer setting and the theme are stored in `localStorage`, separately per site.

## How to deploy changes

Claude **can't push to Pratik's GitHub from the cloud session**, because pushes are refused for this account. The working method is:

1. Build in the cloud workspace, and stage outputs under `/mnt/user-data/outputs/alevel-<subject>/`.
2. Write the files to the Mac with the device tools (`device_commit_files` into `~/Documents/Projects/...`). This only works when the Mac is linked and online; `~/Documents/Projects` has been granted before.
3. If the Mac is offline, send a zip with SendUserFile instead.
4. Give Pratik copy-paste commands. He prefers fully literal CLI commands.

```bash
cd ~/Documents/Projects/alevel-<subject>
git add .
git commit -m "<message>"
git push
```

Netlify picks up the push automatically. Netlify sites were connected through the Netlify web portal.

After deploying, verify the live URL with WebFetch.

## Current status (15 Oct 2026, 20:30)

- **Live:** all four hubs and the landing page are deployed and verified.
- **Deployed 15 Oct, 20:26:** the "← All subjects" link on the Biology, Chemistry and Maths hubs, the Maths hero-text fix (it now mentions worked examples instead of required practicals), and this handover file.
- **Finance hub fixes** are being handled by Pratik in a separate chat. Known issues:
  - Section 75 is credited to the Consumer Rights Act 2015; it should be the Consumer Credit Act 1974.
  - Minimum payment figures don't match between the summary (3–5% or £25) and the quiz (£10 or 1–2%).
  - The Topic 6 name differs: "Borrowing Products" on the hub, "Credit & Debt" on the quiz.

## Accuracy notes

- All content is original. It is written against the AQA specifications, not copied from paid resources.
- An automated check compared each answer key with its explanation. The flagged questions were reviewed by hand, and the Maths numerical answers were recalculated.
- The content hasn't had expert review. Pratik was advised to spot-check topics against a textbook or teacher.

## Claude preview artifacts (private, claude.ai)

- Biology: https://claude.ai/artifact/EPkA6U2ryAsfv3o4MTf4UY
- Chemistry: https://claude.ai/artifact/TiYRgDe5fhexrSjJkG37MT
- Maths: https://claude.ai/artifact/1wv8ifHF6zezkrLnacmwab

These are previews only. The Netlify sites are the real ones. The previews were published before the "All subjects" link was added.

## Possible next steps (only if Pratik asks)

- **Shared template:** unify the three templates into one, with all subject text in `site.yaml`.
- **Practice questions:** add exam-style long-answer questions with mark schemes.
- **Progress page:** add a page on the landing site summarising scores. This would need the scores in one place, because `localStorage` is per site.
- **Finance redesign:** move Finance to the same design as the AQA hubs.
