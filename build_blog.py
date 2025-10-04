import os
from datetime import datetime

POSTS_DIR = "blog/posts"
INDEX_FILE = "blog/index.html"
CSS_FILE = "style.css"

PARTICLES_SCRIPT = """
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>
<script>
window.addEventListener('DOMContentLoaded', function() {
  tsParticles.load("tsparticles", {
    fullScreen: { enable: true, zIndex: -1 },
    particles: {
      number: { value: 80 },
      color: { value: "#ffffff" },
      shape: { type: "circle" },
      opacity: { value: 0.2 },
      size: { value: 2 },
      links: { enable: true, distance: 120, color: "#ffffff", opacity: 0.4, width: 1 },
      move: { enable: true, speed: 0.5, direction: "none", outModes: { default: "bounce" } }
    },
    interactivity: {
      events: {
        onHover: { enable: true, mode: "repulse" },
        onClick: { enable: true, mode: "push" }
      },
      modes: { repulse: { distance: 50 }, push: { quantity: 2 } }
    },
    detectRetina: true
  });
});
</script>
"""

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

posts = []

for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".html"):
        post_path = os.path.join(POSTS_DIR, filename)
        date = extract_date(filename)
        title = format_title(filename)

        posts.append({"file": filename, "title": title, "date": date})

        with open(post_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Prepend date automatically
        date_html = ""
        if date:
            date_html = f'<p><em>Posted on {date.strftime("%B %d, %Y")}</em></p>\n'
        content = date_html + content

        # Wrap in post-content
        if 'class="post-content"' not in content:
            content = f'<div class="post-content">\n{content}\n</div>'

        # Add back-to-home link if missing
        back_link = '<p><a href="../index.html">← Back to blog homepage</a></p>\n'
        if back_link not in content:
            content += "\n" + back_link

        # Build full HTML with particles
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="../{CSS_FILE}">
</head>
<body>
  <div id="tsparticles"></div>
  {content}
  {PARTICLES_SCRIPT}
</body>
</html>
"""

        # Overwrite the post file
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(full_html)

# Rebuild index.html
html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>DEVlog</title>
  <link rel="stylesheet" href="{CSS_FILE}">
</head>
<body>
  <div id="tsparticles"></div>
  <header>
    <h1>DevLog</h1>
  </header>
  <main>
    <ul>
"""

for post in sorted(posts, key=lambda p: p["date"] or datetime.min, reverse=True):
    date_str = post["date"].strftime("%Y-%m-%d") if post["date"] else "Unknown"
    html += f'      <li><a href="posts/{post["file"]}">{post["title"]}</a> <small>({date_str})</small></li>\n'

html += f"""    </ul>
  </main>
  {PARTICLES_SCRIPT}
</body>
</html>
"""

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated {len(posts)} posts and index with dates, back links, and particles background.")
