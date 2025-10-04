import os
from datetime import datetime

POSTS_DIR = "blog/posts"
INDEX_FILE = "blog/index.html"
CSS_FILE = "style.css"
INCLUDE_PARTICLES = True  # Toggle triangles background

def format_title(filename):
    try:
        parts = filename.split("-", 3)
        if len(parts) < 4:
            raise ValueError
        return parts[3].replace(".html", "").replace("-", " ").title()
    except Exception:
        return filename.replace(".html", "")

def extract_date(filename):
    try:
        year, month, day, _ = filename.split("-", 3)
        return datetime(int(year), int(month), int(day))
    except Exception:
        return None

posts = []
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".html"):
        date = extract_date(filename)
        title = format_title(filename)
        posts.append({
            "file": filename,
            "title": title,
            "date": date
        })
        if not date:
            print(f"Warning: '{filename}' does not follow YYYY-MM-DD-title.html format.")

posts.sort(key=lambda p: p["date"] or datetime.min, reverse=True)

for post in posts:
    post_path = os.path.join(POSTS_DIR, post["file"])
    with open(post_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure CSS link
    if f'href="{CSS_FILE}"' not in content:
        content = f'<link rel="stylesheet" href="../{CSS_FILE}">\n{content}'

    # Add auto date
    if post["date"]:
        date_line = f'<p><em>Posted on {post["date"].strftime("%B %d, %Y")}</em></p>\n'
        if date_line not in content:
            content = date_line + content

    # Back-to-home link
    back_link = '<p><a href="../index.html">← Back to blog homepage</a></p>\n'
    if back_link not in content:
        content += "\n" + back_link

    # Wrap post content in container
    if 'class="post-content"' not in content:
        content = f'<div class="post-content">\n{content}\n</div>'

    # Build full HTML with particles outside the post container
    if INCLUDE_PARTICLES:
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{format_title(post["file"])}</title>
  <link rel="stylesheet" href="../{CSS_FILE}">
</head>
<body>
  <!-- Particles container -->
  <div id="tsparticles"></div>

  {content}

  <!-- tsParticles script -->
  <script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>
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
  </script>
</body>
</html>
"""
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(full_html)
    else:
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(content)

# Build blog index
html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>My Blog</title>
  <link rel="stylesheet" href="{CSS_FILE}">
</head>
<body>
  <header>
    <h1>My Blog</h1>
  </header>
  <main>
    <ul>
"""

for post in posts:
    date_str = post["date"].strftime("%Y-%m-%d") if post["date"] else "Unknown"
    html += f'      <li><a href="posts/{post["file"]}">{post["title"]}</a> <small>({date_str})</small></li>\n'

html += """    </ul>
  </main>
</body>
</html>
"""

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Blog index updated with {len(posts)} posts.")
