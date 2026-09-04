import os
from datetime import datetime

POSTS_DIR = "blog/posts"
INDEX_FILE = "blog/index.html"

os.makedirs(POSTS_DIR, exist_ok=True)

posts = []

for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".html"):
        filepath = os.path.join(POSTS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            year, month, day, rest = filename.split("-", 3)
            date = datetime(int(year), int(month), int(day))
            title = rest.replace(".html", "").replace("-", " ").title()
        except Exception:
            date = None
            title = filename.replace(".html", "")

        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div id="tsparticles"></div>
  <div class="post-content">
    <p><em>Posted on {date.strftime("%B %d, %Y") if date else "Unknown"}</em></p>
    {content}
    <p><a href="../index.html">← Back to blog homepage</a></p>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>
  <script>
    tsParticles.load("tsparticles", {{
      fullScreen: {{ enable: true, zIndex: -1 }},
      particles: {{
        number: {{ value: 80 }},
        color: {{ value: "#ffffff" }},
        shape: {{ type: "circle" }},
        opacity: {{ value: 0.2 }},
        size: {{ value: 2 }},
        links: {{
          enable: true,
          distance: 120,
          color: "#ffffff",
          opacity: 0.4,
          width: 1
        }},
        move: {{
          enable: true,
          speed: 0.5,
          direction: "none",
          outModes: {{ default: "bounce" }}
        }}
      }},
      interactivity: {{
        events: {{
          onHover: {{ enable: true, mode: "repulse" }},
          onClick: {{ enable: true, mode: "push" }}
        }},
        modes: {{
          repulse: {{ distance: 50 }},
          push: {{ quantity: 2 }}
        }}
      }},
      detectRetina: true
    }});
  </script>
  <script data-goatcounter="https://dieclick.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
</body>
</html>"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_html)

        posts.append({
            "file": filename,
            "title": title,
            "date": date.strftime("%Y-%m-%d") if date else "Unknown"
        })

posts.sort(key=lambda p: p["date"], reverse=True)
html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>DEVlog</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div id="tsparticles"></div>
  <header><h1>Painlogs</h1></header>
  <main><ul>
"""
for post in posts:
    html += f'    <li><a href="posts/{post["file"]}">{post["title"]}</a> <small>({post["date"]})</small></li>\n'
html += """  </ul></main>

  <script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>
  <script>
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
      detectRetina: true
    });
  </script>
  <script data-goatcounter="https://dieclick.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Blog index and {len(posts)} posts updated.")