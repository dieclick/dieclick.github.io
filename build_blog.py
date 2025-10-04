#!/usr/bin/env python3
import os, re, shutil
from datetime import datetime

POSTS_DIR = "blog/posts"
INDEX_FILE = "blog/index.html"
CSS_FILE = "style.css"

# determine css href relative to a post in blog/posts/
if os.path.exists(os.path.join("blog", CSS_FILE)):
    CSS_HREF = "../" + CSS_FILE
elif os.path.exists(CSS_FILE):
    CSS_HREF = "/" + CSS_FILE
else:
    CSS_HREF = "../" + CSS_FILE  # fallback; adjust if needed

CSS_LINK = f'<link rel="stylesheet" href="{CSS_HREF}">'

PARTICLES_SCRIPT = """<script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>
<script>
window.addEventListener('DOMContentLoaded', function() {{
  tsParticles.load("tsparticles", {{
    fullScreen: {{ enable: true, zIndex: -1 }},
    particles: {{
      number: {{ value: 80 }},
      color: {{ value: "#ffffff" }},
      shape: {{ type: "circle" }},
      opacity: {{ value: 0.2 }},
      size: {{ value: 2 }},
      links: {{ enable: true, distance: 120, color: "#ffffff", opacity: 0.4, width: 1 }},
      move: {{ enable: true, speed: 0.5, direction: "none", outModes: {{ default: "bounce" }} }}
    }},
    interactivity: {{
      events: {{
        onHover: {{ enable: true, mode: "repulse" }},
        onClick: {{ enable: true, mode: "push" }}
      }},
      modes: {{ repulse: {{ distance: 50 }}, push: {{ quantity: 2 }} }}
    }},
    detectRetina: true
  }});
}});
</script>"""

def format_title(filename):
    try:
        return filename.split("-", 3)[3].replace(".html", "").replace("-", " ").title()
    except Exception:
        return filename.replace(".html", "")

def extract_date(filename):
    try:
        y, m, d, _ = filename.split("-", 3)
        return datetime(int(y), int(m), int(d))
    except Exception:
        return None

os.makedirs(POSTS_DIR, exist_ok=True)

processed = []
for fname in sorted(os.listdir(POSTS_DIR)):
    if not fname.lower().endswith(".html"):
        continue
    path = os.path.join(POSTS_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    # backup original (so you can compare)
    bak = path + ".bak"
    shutil.copyfile(path, bak)

    date = extract_date(fname)
    title = format_title(fname)
    lower = original.lower()

    changed = False
    notes = []

    if "<html" in lower and "<body" in lower:
        # Full-HTML post: inject where appropriate
        # Inject CSS link into head if missing
        head_match = re.search(r"(<head[^>]*>)(.*?)(</head>)", original, re.S|re.I)
        if head_match:
            head_inner = head_match.group(2)
            if CSS_HREF not in head_inner:
                new_head = head_match.group(1) + head_inner + "\n  " + CSS_LINK + head_match.group(3)
                original = original[:head_match.start()] + new_head + original[head_match.end():]
                changed = True
                notes.append("css-injected-in-head")
        else:
            # no <head>, add one after <html>
            original = re.sub(r"(<html[^>]*>)", r"\1\n<head>\n  " + CSS_LINK + "\n</head>", original, count=1, flags=re.I)
            changed = True
            notes.append("head-inserted")

        # Insert particles container at start of <body> if missing
        if "<div id=\"tsparticles\"" not in original.lower():
            original = re.sub(r"(<body[^>]*>)", r"\1\n  <div id=\"tsparticles\"></div>", original, count=1, flags=re.I)
            changed = True
            notes.append("particles-div-inserted")

        # Ensure date line near top of body (if not present)
        if date and "posted on" not in original.lower():
            # insert after particles div (if present) or after <body>
            original = re.sub(r"(<div id=\"tsparticles\"[^>]*>\s*</div>\s*)", r"\1\n  <p><em>Posted on " + date.strftime("%B %d, %Y") + "</em></p>\n", original, count=1, flags=re.I)
            changed = True
            notes.append("date-inserted")

        # Ensure back link before </body>
        if "back to blog homepage" not in original.lower():
            original = re.sub(r"(</body\s*>)", r'  <p><a href="../index.html">← Back to blog homepage</a></p>\n' + PARTICLES_SCRIPT + r"\1", original, count=1, flags=re.I)
            changed = True
            notes.append("backlink-and-script-inserted")
        else:
            # ensure script exists
            if "tsparticles.bundle.min.js" not in original.lower():
                original = re.sub(r"(</body\s*>)", PARTICLES_SCRIPT + r"\1", original, count=1, flags=re.I)
                changed = True
                notes.append("script-inserted")
    else:
        # Raw content: build full HTML wrapper
        date_html = f'<p><em>Posted on {date.strftime("%B %d, %Y")}</em></p>\n' if date else ""
        content = date_html + original.strip() + "\n"
        # ensure backlink
        if "back to blog homepage" not in content.lower():
            content += '\n<p><a href="../index.html">← Back to blog homepage</a></p>\n'
        full = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  {CSS_LINK}
</head>
<body>
  <div id="tsparticles"></div>
  <div class="post-content">
{content}
  </div>

  {PARTICLES_SCRIPT}
</body>
</html>
"""
        original = full
        changed = True
        notes.append("wrapped-raw-content")

    # write back only if changed
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(original)
    print(f"[{ 'UPDATED' if changed else 'SKIPPED' }] {fname}  -> {', '.join(notes)}")
    processed.append({"file": fname, "title": title, "date": date.strftime("%Y-%m-%d") if date else "Unknown", "changed": changed})

# Build index from processed files (use filenames for date)
posts = sorted(processed, key=lambda p: p["date"] or "0000-00-00", reverse=True)

index_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>DEVlog</title>
  {css}
</head>
<body>
  <div id="tsparticles"></div>
  <header><h1>PainLogs</h1></header>
  <main><ul>
""".format(css=CSS_LINK)

for p in posts:
    index_html += f'    <li><a href="posts/{p["file"]}">{p["title"]}</a> <small>({p["date"]})</small></li>\n'

index_html += """  </ul></main>

{script}
</body>
</html>
""".format(script=PARTICLES_SCRIPT)

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(index_html)

print(f"\nDone — index + {len(processed)} posts processed. Inspect the .bak files in blog/posts/ to compare originals.")
