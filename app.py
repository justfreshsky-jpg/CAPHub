"""
CAPHub — Flask app: landing page, /wings dashboard, /tools roadmap MVPs.

Uses the shared Fresh Sky privacy and provider controls. The /tools/<slug> routes
ship the documented roadmap items: form drafter, specialty-track coach,
SUI prep checklist. Stateless, with a restricted U.S. provider chain.
"""
import logging
import os

from flask import Response, Flask, jsonify, render_template, request

from tools_data import TOOLS as _TOOLS, get_tool as _get_tool, all_slugs as _all_slugs

app = Flask(__name__)

_logger = logging.getLogger(__name__)


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
<p><em>Last updated 2026-07-16</em></p>
<h2>What we collect</h2>
<p>Fresh Sky AI for Civil Air Patrol is a stateless tool. We do <strong>not</strong> require accounts. We do <strong>not</strong> store the text or voice input you submit. We do <strong>not</strong> upload member rosters, patient data, or any personally identifying information.</p>
<h2>What we send to AI providers</h2>
<p>The text or voice transcript you submit is sent through the configured restricted U.S. AI provider pool. Provider availability can change. The shared privacy layer rejects several common identifier patterns before provider calls, but automated screening is not a substitute for removing identifying information. Do not submit PII, member rosters, payment data, or sensitive operational details.</p>
<h2>What gets logged</h2>
<p>Standard request metadata (IP address, timestamp, response code) is logged by Google Cloud Run for operational purposes (debugging, abuse prevention) and rotated automatically per Google retention defaults. We do not associate logs with individual users.</p>
<h2>Cookies</h2>
<p>A Flask session cookie is set to remember ephemeral state during your visit. It expires when you close the browser. No third-party tracking, no advertising cookies.</p>
<h2>Children</h2>
<p>Some of our tools (e.g. CAPStudy) are designed to be used by minors aged 12+. We do not collect any personally identifying information from anyone, including minors. Parents/guardians of cadets aged 12-17 may use the tool freely.</p>
<h2>Contact</h2>
<p>Questions: <a href="https://www.freshskyai.com/contact">Fresh Sky contact page</a>. Operator: Fresh Sky LLC, Somerset County, NJ.</p>
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
<p>Questions: <a href="https://www.freshskyai.com/contact">Fresh Sky contact page</a>.</p>
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
    extras = ''.join(
        f'  <url><loc>https://cap.freshskyai.com/tools/{s}</loc>'
        f'<changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
        for s in _all_slugs()
    )
    # All 52 per-wing detail pages
    wing_codes = [c.lower() for _, ws in _CAP_REGIONS for c, _ in ws]
    wing_urls = ''.join(
        f'  <url><loc>https://cap.freshskyai.com/wing/{c}</loc>'
        f'<changefreq>monthly</changefreq><priority>0.5</priority></url>\n'
        for c in wing_codes
    )
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url><loc>https://cap.freshskyai.com/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
        '  <url><loc>https://cap.freshskyai.com/wings</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
        '  <url><loc>https://cap.freshskyai.com/tools</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
        + extras + wing_urls +
        '</urlset>\n',
        mimetype='application/xml',
    )


# ─── CAP Wings dashboard ────────────────────────────────────────────────
# Single listing page for all 52 CAP wings (50 states + DC + Puerto Rico),
# grouped by the 8 CAP regions. Each wing links to its CAP-managed .cap.gov
# site plus the Fresh Sky CAP tools that work for
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


# Lookup helper for /wing/<code> routing
_WING_BY_CODE = {code: (region, name) for region, wings in _CAP_REGIONS for code, name in wings}


@app.route('/wing/<code>')
def _wing_detail(code):
    code = code.upper()
    info = _WING_BY_CODE.get(code)
    if not info:
        return Response('Wing not found', status=404, mimetype='text/plain')
    region, name = info
    slug = code.lower()
    cap_url = f'https://www.{slug}wg.cap.gov'
    body = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>{name} ({code}) — Fresh Sky AI for Civil Air Patrol</title>
<meta name="description" content="Fresh Sky AI free tools for {name} ({code}) members and squadrons. Part of {region}.">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="canonical" href="https://cap.freshskyai.com/wing/{slug}">
<link rel="icon" type="image/png" href="/static/favicon.png">
<style>
*,*::before,*::after{{box-sizing:border-box}}
body{{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#0f172a;background:#f8fafc;line-height:1.6}}
nav{{display:flex;align-items:center;justify-content:space-between;padding:1rem 1.6rem;background:#fff;border-bottom:1px solid #e5e7eb}}
nav a{{color:#1e3a8a;text-decoration:none;font-weight:600}}
main{{max-width:760px;margin:0 auto;padding:2.5rem 1.4rem 4rem}}
.crumb{{color:#64748b;font-size:.85rem;margin:0 0 1rem}}
.crumb a{{color:#1e3a8a;text-decoration:none}}
h1{{font-size:1.9rem;margin:0 0 .4rem;font-weight:800}}
.region{{color:#64748b;font-size:.95rem;margin:0 0 1.6rem}}
.code{{display:inline-block;background:#1e3a8a;color:#fff;font-size:.78rem;font-weight:700;padding:.2rem .55rem;border-radius:5px;margin-right:.4rem;vertical-align:middle}}
.cta{{display:inline-block;padding:.85rem 1.4rem;background:#1e3a8a;color:#fff;border-radius:8px;text-decoration:none;font-weight:700;margin:0 .5rem .5rem 0}}
.cta.alt{{background:#fff;color:#1e3a8a;border:1px solid #1e3a8a}}
section{{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:1.4rem;margin:1.4rem 0}}
section h2{{font-size:1.05rem;margin:0 0 .6rem;color:#1e3a8a}}
section ul{{padding-left:1.2rem;margin:0}}
.foot{{color:#94a3b8;font-size:.82rem;margin-top:2rem;padding-top:1.2rem;border-top:1px solid #e5e7eb;text-align:center}}
</style>
</head>
<body>

<nav>
  <a href="/">🛩️ Fresh Sky AI for CAP</a>
  <a href="/wings" style="color:#64748b;font-weight:400">← All wings</a>
</nav>

<main>
  <p class="crumb"><a href="/">Home</a> &nbsp;›&nbsp; <a href="/wings">Wings</a> &nbsp;›&nbsp; {name}</p>
  <h1><span class="code">{code}</span>{name}</h1>
  <p class="region">{region}</p>

  <a class="cta" href="{cap_url}" target="_blank" rel="noopener">Visit {slug}wg.cap.gov →</a>
  <a class="cta alt" href="/tools">Try Fresh Sky CAP tools →</a>

  <section>
    <h2>Free tools for {code} members + squadrons</h2>
    <ul>
      <li><a href="https://capr.freshskyai.com" target="_blank" rel="noopener">CAPR Search</a> — Q&amp;A over CAPRs / CAPPs</li>
      <li><a href="https://capstudy.freshskyai.com" target="_blank" rel="noopener">CAPStudy</a> — cadet Achievement Test prep</li>
      <li><a href="https://capmeeting.freshskyai.com" target="_blank" rel="noopener">CAPMeeting</a> — squadron meeting agenda builder</li>
      <li><a href="/tools/form-drafter">CAP Form Drafter</a> — drafts of common CAPFs from your activity context</li>
      <li><a href="/tools/specialty-track">Specialty Track Coach</a> — 6-month plan for your senior-member track</li>
      <li><a href="/tools/sui-prep">SUI Prep Checklist</a> — Subordinate Unit Inspection prep</li>
    </ul>
  </section>

  <section>
    <h2>Where the canonical info lives</h2>
    <ul>
      <li><strong>{name} official site</strong> — <a href="{cap_url}" target="_blank" rel="noopener">{cap_url}</a> (wing CC, encampment, group / squadron locator, events)</li>
      <li><strong>National CAP</strong> — <a href="https://www.gocivilairpatrol.com" target="_blank" rel="noopener">gocivilairpatrol.com</a></li>
      <li><strong>Member resources</strong> — <a href="https://www.gocivilairpatrol.com/members" target="_blank" rel="noopener">CAP NHQ member resources</a> (publications and links to member systems)</li>
    </ul>
  </section>

  <p class="foot">
    Information architecture only — Fresh Sky AI doesn't have access to {code}-internal data
    (rosters, eServices status, etc.). For wing-internal info, sign in at the wing site.
    Always free for CAP members + squadrons.
  </p>
</main>

</body></html>"""
    return Response(body, mimetype='text/html')


@app.route('/wings')
def _wings():
    rows_html = []
    total_wings = 0
    for region_name, wings in _CAP_REGIONS:
        wing_cards = []
        for code, name in wings:
            total_wings += 1
            slug = code.lower()
            # CAP-managed wing sites use the <wing>wg.cap.gov pattern.
            cap_url = f'https://www.{slug}wg.cap.gov'
            wing_cards.append(
                f'<li class="wing"><a href="/wing/{slug}" class="winglink">'
                f'<strong>{name}</strong></a>'
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
  li.wing a.winglink{{text-decoration:none;color:#0f172a;flex:1 0 auto}}
  li.wing a.winglink:hover strong{{color:#1e3a8a;text-decoration:underline}}
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
  <p class="lede">All <strong>{total_wings}</strong> Civil Air Patrol wings — 50 states plus DC (National Capital Wing) and Puerto Rico — grouped by the 8 CAP regions. Click any wing to visit its CAP-managed <code>.cap.gov</code> site.</p>

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
    Uses publicly available CAP publication references. Not affiliated with or endorsed by Civil Air Patrol Inc.<br>
    Always free for CAP members + squadrons.
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


# Provider calls are centralized in the privacy-restricted shared chain.

from freshsky_common.llm import LLMChain, install_provider_metrics  # noqa: E402

_SHARED_LLM = LLMChain(privacy_profile="us_public")
install_provider_metrics(app)


def _llm_shared(system, user):
    return _SHARED_LLM.complete(system=system, user=user) or None


_PROVIDERS_TOOLS = [('shared', _llm_shared)]


def _llm_call(system: str, user: str) -> str:
    last_err = None
    for name, fn in _PROVIDERS_TOOLS:
        try:
            out = fn(system, user)
            if out:
                return out.strip()
        except Exception as e:
            last_err = e
            _logger.warning('Provider %s failed: %s', name, e)
    raise RuntimeError(f'All providers failed: {last_err}')


# ─── /tools index + per-tool routes ─────────────────────────────────────

@app.route('/tools')
def _tools_index():
    return render_template('tools_index.html', slugs=_all_slugs(), tools=_TOOLS)


@app.route('/tools/<slug>', methods=['GET', 'POST'])
def _tools_run(slug):
    tool = _get_tool(slug)
    if not tool:
        return Response('Tool not found', status=404, mimetype='text/plain')
    result = None
    error = None
    submitted = {}
    if request.method == 'POST':
        for field_key, _label, _kind in tool['fields']:
            submitted[field_key] = (request.form.get(field_key) or '').strip()[:4000]
        if not any(v for v in submitted.values()):
            error = 'Please fill in at least one field.'
        else:
            user_msg = '\n\n'.join(f'{k}:\n{v}' for k, v in submitted.items() if v)
            try:
                result = _llm_call(tool['system_prompt'], user_msg)
            except Exception as e:
                _logger.exception('LLM error for %s', slug)
                error = ('All AI providers are currently unreachable. '
                         f'Please try again in a minute. ({type(e).__name__})')
    return render_template(
        'tools_run.html',
        slug=slug, tool=tool, submitted=submitted, result=result, error=error,
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
