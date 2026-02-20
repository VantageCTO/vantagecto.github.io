"""Generate static blog pages from the VantageCTO API.

Called by the GitHub Actions workflow after a blog post is published.
Templates are embedded here so they aren't publicly accessible on the site.
"""

import os
from datetime import datetime, timezone

import markdown
import requests

API_URL = os.environ["API_URL"]
SLUG = os.environ["POST_SLUG"]

# ---------------------------------------------------------------------------
# Embedded Templates
# ---------------------------------------------------------------------------

POST_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en" class="blog-page">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{{EXCERPT}}" />
  <meta property="og:title" content="{{TITLE}} — VantageCTO Blog" />
  <meta property="og:description" content="{{EXCERPT}}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://vantage-cto.com/blog/{{SLUG}}.html" />
  <meta name="twitter:card" content="summary" />
  <title>{{TITLE}} — VantageCTO Blog</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Outfit:wght@400;500;700;800&family=IBM+Plex+Mono:wght@300;400&display=swap" rel="stylesheet" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="stylesheet" href="/styles.css" />
  <link rel="canonical" href="https://vantage-cto.com/blog/{{SLUG}}.html" />
</head>
<body>

<nav id="navbar" class="scrolled" aria-label="Main navigation">
  <a class="logo" href="/">Vantage<span>CTO</span></a>
  <a class="nav-cta" href="/blog/">Blog</a>
</nav>

<main id="main-content">
  <div class="blog-header">
    <a href="/blog/" class="blog-back">&larr; BACK TO BLOG</a>
    <h1 class="blog-title">{{TITLE}}</h1>
    <div class="blog-meta">
      <span>{{AUTHOR}}</span>
      <span>{{DATE}}</span>
    </div>
  </div>
  <article class="blog-content">
    {{CONTENT}}
  </article>
</main>

<footer role="contentinfo">
  <p>&copy; 2026 <a href="/">VantageCTO</a> — All rights reserved.</p>
  <p>Built with conviction. <span style="color:var(--accent)">// blog</span></p>
</footer>

</body>
</html>
"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en" class="blog-page">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Insights for non-technical founders on startup strategy, technology decisions, and runway protection." />
  <meta property="og:title" content="Blog — VantageCTO" />
  <meta property="og:description" content="Insights for non-technical founders on startup strategy, technology decisions, and runway protection." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://vantage-cto.com/blog/" />
  <title>Blog — VantageCTO</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Outfit:wght@400;500;700;800&family=IBM+Plex+Mono:wght@300;400&display=swap" rel="stylesheet" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="stylesheet" href="/styles.css" />
  <link rel="canonical" href="https://vantage-cto.com/blog/" />
</head>
<body>

<nav id="navbar" class="scrolled" aria-label="Main navigation">
  <a class="logo" href="/">Vantage<span>CTO</span></a>
  <a class="nav-cta" href="/#waitlist">Join Waitlist</a>
</nav>

<main id="main-content">
  <div class="blog-index-header">
    <p class="section-label">// VantageCTO Blog</p>
    <h1 class="blog-index-title">Insights for Founders</h1>
    <p class="blog-index-sub">Strategic thinking before the spend. {{POST_COUNT}} articles.</p>
  </div>
  <div class="blog-list">
    {{POSTS}}
  </div>
</main>

<footer role="contentinfo">
  <p>&copy; 2026 <a href="/">VantageCTO</a> — All rights reserved.</p>
  <p>Built with conviction. <span style="color:var(--accent)">// blog</span></p>
</footer>

</body>
</html>
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def format_date(iso_str: str | None) -> str:
    if not iso_str:
        return ""
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return dt.strftime("%B %d, %Y")


def render_post(post: dict) -> str:
    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
    content_html = md.convert(post["content_markdown"])

    html = POST_TEMPLATE
    html = html.replace("{{TITLE}}", post["title"])
    html = html.replace("{{AUTHOR}}", post["author"])
    html = html.replace("{{DATE}}", format_date(post.get("published_at")))
    html = html.replace("{{CONTENT}}", content_html)
    html = html.replace("{{SLUG}}", post["slug"])
    html = html.replace("{{EXCERPT}}", post.get("excerpt") or "")
    return html


def render_sitemap(posts: list[dict]) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = """\
  <url>
    <loc>https://vantage-cto.com/</loc>
    <lastmod>2026-02-19</lastmod>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://vantage-cto.com/blog/</loc>
    <lastmod>{today}</lastmod>
    <priority>0.8</priority>
  </url>
""".format(today=today)

    for p in posts:
        pub_date = ""
        if p.get("published_at"):
            dt = datetime.fromisoformat(p["published_at"].replace("Z", "+00:00"))
            pub_date = dt.strftime("%Y-%m-%d")
        else:
            pub_date = today
        urls += f"""\
  <url>
    <loc>https://vantage-cto.com/blog/{p['slug']}.html</loc>
    <lastmod>{pub_date}</lastmod>
    <priority>0.6</priority>
  </url>
"""

    return f"""\
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>
"""


def render_index(posts: list[dict]) -> str:
    posts.sort(key=lambda p: p.get("published_at") or "", reverse=True)

    if not posts:
        listing_html = '<p class="blog-empty">No posts yet. Check back soon.</p>'
    else:
        listing_html = ""
        for p in posts:
            pub_date = format_date(p.get("published_at"))
            listing_html += f"""    <article class="blog-card">
      <a href="/blog/{p['slug']}.html">
        <h2 class="blog-card-title">{p['title']}</h2>
      </a>
      <div class="blog-card-meta">
        <span>{p['author']}</span>
        <span>{pub_date}</span>
      </div>
      <p class="blog-card-excerpt">{p.get('excerpt') or ''}</p>
      <a href="/blog/{p['slug']}.html" class="blog-card-link">Read more &rarr;</a>
    </article>
"""

    html = INDEX_TEMPLATE
    html = html.replace("{{POSTS}}", listing_html)
    html = html.replace("{{POST_COUNT}}", str(len(posts)))
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    # Fetch the published post
    resp = requests.get(f"{API_URL}/blog/{SLUG}")
    resp.raise_for_status()
    post = resp.json()

    # Generate individual post page
    os.makedirs("blog", exist_ok=True)
    post_html = render_post(post)
    with open(f"blog/{post['slug']}.html", "w") as f:
        f.write(post_html)
    print(f"Generated blog/{post['slug']}.html")

    # Regenerate blog index with all published posts
    resp = requests.get(f"{API_URL}/blog/")
    resp.raise_for_status()
    posts = resp.json()

    index_html = render_index(posts)
    with open("blog/index.html", "w") as f:
        f.write(index_html)
    print(f"Updated blog/index.html with {len(posts)} posts")

    # Regenerate sitemap with blog post URLs
    sitemap_xml = render_sitemap(posts)
    with open("sitemap.xml", "w") as f:
        f.write(sitemap_xml)
    print(f"Updated sitemap.xml with {len(posts)} blog posts")


if __name__ == "__main__":
    main()
