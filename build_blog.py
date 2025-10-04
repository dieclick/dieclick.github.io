import os
from datetime import datetime

POSTS_DIR = "blog/posts"
INDEX_FILE = "blog/index.html"

posts = []
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".html"):
        try:
            year, month, day, rest = filename.split("-", 3)
            date = datetime(int(year), int(month), int(day))
            title = rest.replace(".html", "").replace("-", " ").title()
        except Exception:
            date = None
            title = filename.replace(".html", "")

        posts.append({
            "file": filename,
            "title": title,
            "date": date.strftime("%Y-%m-%d") if date else "Unknown"
        })

posts.sort(key=lambda p: p["date"], reverse=True)

# Build HTML
html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>My Blog</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <h1>My Blog</h1>
    <nav>
      <a href="../index.html">Home</a> | 
      <a href="../projects/">Projects</a>
    </nav>
  </header>
  <main>
    <ul>
"""

for post in posts:
    html += f'      <li><a href="posts/{post["file"]}">{post["title"]}</a> <small>({post["date"]})</small></li>\n'

html += """    </ul>
  </main>
</body>
</html>
"""

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Blog index updated with {len(posts)} posts.")
