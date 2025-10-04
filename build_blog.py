import os
from datetime import datetime

POSTS_DIR = "blog/posts"
INDEX_FILE = "blog/index.html"
CSS_FILE = "style.css"

def format_title(filename):
    """Convert filename to a human-readable title."""
    try:
        parts = filename.split("-", 3)
        if len(parts) < 4:
            raise ValueError
        return parts[3].replace(".html", "").replace("-", " ").title()
    except Exception:
        return filename.replace(".html", "")

def extract_date(filename):
    """Extract date from filename."""
    try:
        year, month, day, _ = filename.split("-", 3)
        return datetime(int(year), int(month), int(day))
    except Exception:
        return None

# Collect posts
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

# Sort posts newest first
posts.sort(key=lambda p: p["date"] or datetime.min, reverse=True)

# Ensure each post has CSS link and auto date
for post in posts:
    post_path = os.path.join(POSTS_DIR, post["file"])
    with open(post_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Prepend CSS link if missing
    if f'href="{CSS_FILE}"' not in content:
        content = f'<link rel="stylesheet" href="../{CSS_FILE}">\n{content}'

    # Prepend date if missing
    if post["date"]:
        date_line = f'<p><em>Posted on {post["date"].strftime("%B %d, %Y")}</em></p>\n'
        if date_line not in content:
            content = date_line + content

    # Write back updated post
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(content)

# Build index.html
html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>DevLog</title>
  <link rel="stylesheet" href="{CSS_FILE}">
</head>
<body>
  <header>
    <h1>DevLog</h1>
    <nav>
      <a href="../index.html">Home</a>
    </nav>
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

# Write index.html
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Blog index updated with {len(posts)} posts.")


