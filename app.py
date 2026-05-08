"""
CAPHub — minimal Flask app serving the static landing page.

Standalone (no freshsky_common dependency). One route serving the
umbrella site for Fresh Sky AI's free Civil Air Patrol tools.
"""
import os

from flask import Response, Flask, jsonify, render_template

app = Flask(__name__)


@app.after_request
def _security_headers(resp):
    resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
    resp.headers.setdefault('X-Frame-Options', 'DENY')
    resp.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
    resp.headers.setdefault('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
    return resp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    return jsonify(status='ok')


_PRIVACY_HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Privacy — Fresh Sky AI for Civil Air Patrol</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:system-ui,sans-serif;max-width:760px;margin:40px auto;padding:0 20px;line-height:1.6;color:#0f172a}h1{margin-bottom:.5em}h2{margin-top:1.5em;font-size:1.1rem}a{color:#1e3a8a}</style>
</head><body>
<a href="/">← Back to Fresh Sky AI for Civil Air Patrol</a>
<h1>Privacy Policy — Fresh Sky AI for Civil Air Patrol</h1>
<p><em>Last updated 2026-05-07</em></p>
<h2>What we collect</h2>
<p>Fresh Sky AI for Civil Air Patrol is a stateless tool. We do <strong>not</strong> require accounts. We do <strong>not</strong> store the text or voice input you submit. We do <strong>not</strong> upload member rosters, patient data, or any personally identifying information.</p>
<h2>What we send to AI providers</h2>
<p>The text or voice transcript you submit is sent to one of several US/EU-jurisdiction LLM providers (Groq, Cerebras, Mistral, HuggingFace via Together, Sambanova, Cloudflare Workers AI, or Google Gemini) for processing. None of these providers train on inputs from our paid-tier API calls (Gemini's free tier may; we do not pass PII).</p>
<h2>What gets logged</h2>
<p>Standard request metadata (IP address, timestamp, response code) is logged by Google Cloud Run for operational purposes (debugging, abuse prevention) and rotated automatically per Google retention defaults. We do not associate logs with individual users.</p>
<h2>Cookies</h2>
<p>A Flask session cookie is set to remember ephemeral state during your visit. It expires when you close the browser. No third-party tracking, no advertising cookies.</p>
<h2>Children</h2>
<p>Some of our tools (e.g. CAPStudy) are designed to be used by minors aged 12+. We do not collect any personally identifying information from anyone, including minors. Parents/guardians of cadets aged 12-17 may use the tool freely.</p>
<h2>Contact</h2>
<p>Questions: <a href="mailto:admin@freshskyllc.com">admin@freshskyllc.com</a>. Operator: Fresh Sky LLC, Somerset County, NJ.</p>
</body></html>"""

_TERMS_HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Terms of Use — Fresh Sky AI for Civil Air Patrol</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:system-ui,sans-serif;max-width:760px;margin:40px auto;padding:0 20px;line-height:1.6;color:#0f172a}h1{margin-bottom:.5em}h2{margin-top:1.5em;font-size:1.1rem}a{color:#1e3a8a}</style>
</head><body>
<a href="/">← Back to Fresh Sky AI for Civil Air Patrol</a>
<h1>Terms of Use — Fresh Sky AI for Civil Air Patrol</h1>
<p><em>Last updated 2026-05-07</em></p>
<h2>What this is</h2>
<p>Fresh Sky AI for Civil Air Patrol is a free volunteer-built tool offered by Fresh Sky LLC for use by U.S. Civil Air Patrol members and squadrons. No charge. No contract. No license required.</p>
<h2>What this is not</h2>
<p>Fresh Sky AI for Civil Air Patrol is <strong>not</strong> affiliated with any government agency, military service, or official entity. Output is AI-generated and intended as a draft or study aid only — the human user is responsible for verifying accuracy against authoritative current sources before acting on or filing anything.</p>
<h2>Use at your own discretion</h2>
<p>You agree to use the tool in good faith. Do not submit personally identifying information (PII) about third parties, patient health information (PHI), or classified/sensitive operational details. The tool is not designed to handle such data and we do not warrant against any misuse.</p>
<h2>No warranty</h2>
<p>The tool is provided "as is" without warranty of any kind. Fresh Sky LLC disclaims all liability for damages arising from use or misuse of the output.</p>
<h2>Changes</h2>
<p>We may update or discontinue the tool without notice. If a tool is retired, this URL will redirect or be retired in tandem.</p>
<h2>Contact</h2>
<p>Questions: <a href="mailto:admin@freshskyllc.com">admin@freshskyllc.com</a>.</p>
</body></html>"""


@app.route('/robots.txt')
def _robots():
    return Response(
        "User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /metrics\nDisallow: /health\n"
        "Sitemap: https://cap.freshskyai.com/sitemap.xml\n",
        mimetype='text/plain',
    )


@app.route('/sitemap.xml')
def _sitemap():
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url><loc>https://cap.freshskyai.com/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
        '  <url><loc>https://cap.freshskyai.com/wings</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
        '</urlset>\n',
        mimetype='application/xml',
    )


# ─── CAP Wings dashboard ────────────────────────────────────────────────
# Single listing page for all 52 CAP wings (50 states + DC + Puerto Rico),
# grouped by the 8 CAP regions. Each wing links to gocivilairpatrol.com
# (the canonical wing page) plus the Fresh Sky CAP tools that work for
# that wing's members. Pure information architecture — no internal data
# we don't have access to. Free for CAP audience.
_CAP_REGIONS = [
    ('Great Lakes Region', [
        ('IL', 'Illinois Wing'), ('IN', 'Indiana Wing'),
        ('KY', 'Kentucky Wing'), ('MI', 'Michigan Wing'),
        ('OH', 'Ohio Wing'),     ('WI', 'Wisconsin Wing'),
    ]),
    ('Middle East Region', [
        ('DC', 'National Capital Wing'), ('DE', 'Delaware Wing'),
        ('MD', 'Maryland Wing'),         ('NC', 'North Carolina Wing'),
        ('SC', 'South Carolina Wing'),   ('VA', 'Virginia Wing'),
        ('WV', 'West Virginia Wing'),
    ]),
    ('North Central Region', [
        ('IA', 'Iowa Wing'),     ('KS', 'Kansas Wing'),
        ('MN', 'Minnesota Wing'),('MO', 'Missouri Wing'),
        ('NE', 'Nebraska Wing'), ('ND', 'North Dakota Wing'),
        ('SD', 'South Dakota Wing'),
    ]),
    ('Northeast Region', [
        ('CT', 'Connecticut Wing'),  ('ME', 'Maine Wing'),
        ('MA', 'Massachusetts Wing'),('NH', 'New Hampshire Wing'),
        ('NJ', 'New Jersey Wing'),   ('NY', 'New York Wing'),
        ('PA', 'Pennsylvania Wing'), ('RI', 'Rhode Island Wing'),
        ('VT', 'Vermont Wing'),
    ]),
    ('Pacific Region', [
        ('AK', 'Alaska Wing'), ('CA', 'California Wing'),
        ('HI', 'Hawaii Wing'), ('NV', 'Nevada Wing'),
        ('OR', 'Oregon Wing'), ('WA', 'Washington Wing'),
    ]),
    ('Rocky Mountain Region', [
        ('CO', 'Colorado Wing'), ('ID', 'Idaho Wing'),
        ('MT', 'Montana Wing'),  ('UT', 'Utah Wing'),
        ('WY', 'Wyoming Wing'),
    ]),
    ('Southeast Region', [
        ('AL', 'Alabama Wing'), ('FL', 'Florida Wing'),
        ('GA', 'Georgia Wing'), ('MS', 'Mississippi Wing'),
        ('PR', 'Puerto Rico Wing'), ('TN', 'Tennessee Wing'),
    ]),
    ('Southwest Region', [
        ('AR', 'Arkansas Wing'), ('AZ', 'Arizona Wing'),
        ('LA', 'Louisiana Wing'),('NM', 'New Mexico Wing'),
        ('OK', 'Oklahoma Wing'), ('TX', 'Texas Wing'),
    ]),
]


@app.route('/wings')
def _wings():
    rows_html = []
    total_wings = 0
    for region_name, wings in _CAP_REGIONS:
        wing_cards = []
        for code, name in wings:
            total_wings += 1
            slug = code.lower()
            # Canonical wing URL pattern on gocivilairpatrol.com
            cap_url = f'https://www.{slug}wg.cap.gov'
            wing_cards.append(
                f'<li class="wing"><strong>{name}</strong>'
                f'<span class="code">{code}</span>'
                f'<a class="extlink" href="{cap_url}" target="_blank" rel="noopener">'
                f'{slug}wg.cap.gov ↗</a></li>'
            )
        rows_html.append(
            f'<section class="region"><h2>{region_name}</h2>'
            f'<ul class="wings">{"".join(wing_cards)}</ul></section>'
        )

    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CAP Wing dashboard — Fresh Sky AI for Civil Air Patrol</title>
<meta name="description" content="All 52 Civil Air Patrol wings — 50 states plus DC and Puerto Rico — grouped by the 8 CAP regions. Plus free Fresh Sky AI tools for CAP members and squadrons.">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="canonical" href="https://cap.freshskyai.com/wings">
<link rel="icon" type="image/png" href="/static/favicon.png">
<style>
  *,*::before,*::after{{box-sizing:border-box}}
  body{{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#0f172a;background:#f8fafc;line-height:1.55}}
  nav{{display:flex;align-items:center;justify-content:space-between;padding:1rem 1.6rem;background:#fff;border-bottom:1px solid #e5e7eb}}
  nav a{{color:#1e3a8a;text-decoration:none}}
  nav a.brand{{font-weight:800}}
  main{{max-width:980px;margin:0 auto;padding:2.5rem 1.4rem 4rem}}
  h1{{font-size:1.9rem;margin:0 0 .4rem;font-weight:800}}
  .lede{{color:#64748b;margin:0 0 2rem;font-size:1.05rem}}
  .tools{{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:1.2rem 1.4rem;margin:0 0 2.5rem}}
  .tools h3{{margin:0 0 .6rem;font-size:.92rem;text-transform:uppercase;letter-spacing:.06em;color:#64748b}}
  .tools ul{{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:.5rem}}
  .tools li a{{display:inline-block;padding:.5rem .9rem;background:#1e3a8a;color:#fff;border-radius:8px;font-size:.92rem;text-decoration:none;font-weight:600}}
  .tools li a:hover{{background:#1e40af}}
  section.region{{margin-bottom:2rem}}
  section.region h2{{font-size:1.05rem;font-weight:700;color:#1e3a8a;margin:0 0 .8rem;padding-bottom:.3rem;border-bottom:2px solid #fbbf24;display:inline-block}}
  ul.wings{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.5rem}}
  li.wing{{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:.7rem .9rem;display:flex;align-items:center;gap:.6rem;transition:border-color .15s}}
  li.wing:hover{{border-color:#1e3a8a}}
  li.wing .code{{background:#1e3a8a;color:#fff;font-size:.7rem;font-weight:700;padding:.15rem .5rem;border-radius:4px;margin-right:auto}}
  li.wing strong{{font-size:.9rem}}
  li.wing a.extlink{{font-size:.78rem;color:#64748b;text-decoration:none}}
  li.wing a.extlink:hover{{color:#1e3a8a;text-decoration:underline}}
  .footer-note{{color:#94a3b8;font-size:.82rem;margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid #e5e7eb;text-align:center}}
</style>
</head>
<body>

<nav>
  <a class="brand" href="/">🛩️ Fresh Sky AI for CAP</a>
  <a href="/">← Home</a>
</nav>

<main>
  <h1>CAP Wing dashboard</h1>
  <p class="lede">All <strong>{total_wings}</strong> Civil Air Patrol wings — 50 states plus DC (National Capital Wing) and Puerto Rico — grouped by the 8 CAP regions. Click any wing to visit its official site at gocivilairpatrol.com.</p>

  <div class="tools">
    <h3>Free tools for any wing's members + squadrons</h3>
    <ul>
      <li><a href="https://capr.freshskyai.com" target="_blank" rel="noopener">CAPR Search — Q&A over CAPRs/CAPPs</a></li>
      <li><a href="https://capstudy.freshskyai.com" target="_blank" rel="noopener">CAPStudy — cadet AT prep quizzes</a></li>
      <li><a href="https://capmeeting.freshskyai.com" target="_blank" rel="noopener">CAPMeeting — squadron meeting builder</a></li>
    </ul>
  </div>

  {''.join(rows_html)}

  <p class="footer-note">
    Public-domain regulation content. Not affiliated with or endorsed by Civil Air Patrol Inc.<br>
    Always free for CAP members + squadrons. <a href="https://www.freshskyai.com/support" target="_blank" rel="noopener">Support the project</a> if these tools help you.
  </p>
</main>

</body></html>"""
    return Response(body, mimetype='text/html')


@app.route('/privacy')
def _privacy():
    return Response(_PRIVACY_HTML, mimetype='text/html')


@app.route('/terms')
def _terms():
    return Response(_TERMS_HTML, mimetype='text/html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
