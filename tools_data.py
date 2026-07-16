"""
CAP tool definitions for /tools/<slug> routes on cap.freshskyai.com.

Each tool is a single LLM-driven worksheet — one form, one prompt,
one result page. Stateless. Free for CAP members + squadrons. Uses publicly
available publication references; not affiliated with Civil Air Patrol Inc.
"""
from __future__ import annotations

SOURCE_RETRIEVED = '2026-07-16'
CAP_PUBLICATIONS_URL = (
    'https://www.gocivilairpatrol.com/members/publications/'
    'indexes-regulations-and-manuals-1700'
)
CAP_FORMS_URL = 'https://www.gocivilairpatrol.com/members/publications/forms/'
CAP_PAMPHLETS_URL = (
    'https://www.gocivilairpatrol.com/members/publications/pamphlets-1702/'
)
CAP_SUI_URL = (
    'https://www.gocivilairpatrol.com/members/cap-national-hq/'
    'inspector-general/sui/'
)

TOOLS: dict[str, dict] = {

    'form-drafter': {
        'title':       'CAP Form Drafter',
        'tagline':     'Draft text for a current CAP form after confirming the form in CAP NHQ\'s official forms library.',
        'icon':        '📋',
        'fields': [
            ('form',     'Which current CAPF form (for example, "CAPF 12 — Application for Senior Membership")', 'input'),
            ('context',  'Activity / mission / situation details — who, what, when, where, why',  'textarea'),
            ('audience', 'Who reads this (squadron commander, group, wing, IC) — affects tone',   'input'),
        ],
        'authorities': [
            {
                'title': 'CAP NHQ Forms Library',
                'version': 'Current public forms index',
                'url': CAP_FORMS_URL,
                'retrieved': SOURCE_RETRIEVED,
            },
        ],
        'system_prompt': (
            "You are a CAP staff-writing assistant. The authoritative source is the current "
            "CAP NHQ Forms Library, retrieved 2026-07-16. Confirmed current examples are: "
            "CAPF 12 'Application for Senior Membership' (Sep 2025); CAPF 15 "
            "'Application for Cadet Membership in Civil Air Patrol' (Oct 2022); CAPF 23 "
            "'Recommendation for Benchmark Candidate' (Apr 2017); CAPF 70-1 'Pre-flight "
            "Risk Assessment Worksheet' (Oct 2025); CAPF 160 'Deliberate Risk Assessment "
            "Worksheet' (Apr 2022); and CAPF 160S 'Real Time Risk Assessment Worksheet' "
            "(Apr 2022). CAPF 37 is available only through Operational Resource Management "
            "and CAPF 101 only through Ops Qual; do not fabricate either. CAPF 2A, CAPF 24, CAPF 31, and "
            "CAPF 60-80 are not present in that current public index. Never invent, infer, "
            "silently renumber, or claim a title for a form that is not confirmed here. If "
            "the requested form is not one of these confirmed examples, start with "
            "'FORM NOT CONFIRMED' and direct the user to the official Forms Library before "
            "drafting against any section headings. For a confirmed form, produce: (1) "
            "FORM AND VERSION — number, title, and listed revision date. (2) DRAFT TEXT — "
            "use only facts the user supplied and organize it by clearly described purpose; "
            "do not pretend to reproduce fields or instructions you were not given. (3) "
            "MISSING INFORMATION — identify gaps without guessing. (4) ROUTING TO VERIFY — "
            "tell the user to follow the current form, governing publication, and unit/wing "
            "instructions; do not invent an approval chain. (5) DISCLAIMER — this is a "
            "draft only and must be checked against the current official form before use."
        ),
    },

    'specialty-track': {
        'title':       'Specialty Track Coach',
        'tagline':     "Plan your way through a CAP senior-member specialty track — Technician → Senior → Master.",
        'icon':        '🎯',
        'fields': [
            ('track',     'Specialty track (Aerospace Education / Operations / Communications / Cadet Programs / Personnel / Public Affairs / Safety / Stan-Eval / Logistics / etc.)', 'input'),
            ('current',   'Current rating (none / Tech / Sr / Master) and what you have completed so far',  'textarea'),
            ('time',      'Approximate hours per month you can devote',                                       'input'),
            ('focus',     'Personal goal (PD progression / squadron need / leadership prep / instructor)',    'textarea'),
        ],
        'authorities': [
            {
                'title': 'CAP NHQ Pamphlets Library',
                'version': 'Current public pamphlet index',
                'url': CAP_PAMPHLETS_URL,
                'retrieved': SOURCE_RETRIEVED,
            },
            {
                'title': 'CAPR 40-1 — Civil Air Patrol Senior Member Education & Training Program',
                'version': '24 May 2021',
                'url': CAP_PUBLICATIONS_URL,
                'retrieved': SOURCE_RETRIEVED,
            },
        ],
        'system_prompt': (
            "You are a CAP Senior-Member specialty-track coach. Given a track + current "
            "rating + time budget, produce a realistic 6-month plan: (1) WHERE YOU ARE — "
            "summarize the user's stated progress without claiming an exact unmet task. "
            "(2) CURRENT GUIDE — identify a guide only when it matches this verified "
            "2026-07-16 CAP NHQ index snapshot: CAP Pamphlet 70-1 Operations Officer "
            "(17 Oct 2025), CAP Pamphlet 214 Communications Officer, CAP Pamphlet 60-11 "
            "Cadet Programs Officer (Jun 2026), CAP Pamphlet 200 Personnel Officer "
            "(30 Apr 2026), CAP Pamphlet 201 Public Affairs Officer, CAP Pamphlet 202 "
            "Financial Management Officer, CAP Pamphlet 206 Logistics Officer, CAP "
            "Pamphlet 212 Standardization/Evaluation Officer, or CAP Pamphlet 40-160 "
            "Safety Officer. If the track is not in this list, say the guide number is not "
            "confirmed and link the current Pamphlets Library; do not guess. (3) MILESTONES "
            "— propose three practical study/OJT milestones, but never label them official "
            "requirements or quote task numbers unless the user supplies the current guide. "
            "Do not call specialty-track requirements SQTRs; SQTR terminology is used for "
            "operational qualifications. (4) RESOURCES — use the official publication "
            "library and current member-learning area in eServices without inventing a "
            "platform name or course. (5) MENTOR CHECK — list questions for the unit "
            "commander, education and training officer, and specialty-track mentor. (6) "
            "DISCLAIMER — the current specialty-track guide, CAPR 40-1, eServices record, "
            "and approving authority are controlling."
        ),
    },

    'sui-prep': {
        'title':       'SUI Prep Checklist',
        'tagline':     "Subordinate Unit Inspection prep — what to gather, what to fix, what inspectors actually look at.",
        'icon':        '✅',
        'fields': [
            ('unit',      'Unit type (squadron / group / wing) and approximate size',                      'input'),
            ('weeks',     'Weeks remaining until the SUI',                                                  'input'),
            ('strengths', 'Areas where you feel solid (CAPR-compliant, well-documented)',                   'textarea'),
            ('worries',   'Areas where you suspect issues (out-of-date OIs, missing PD records, finance, safety logs, etc.)', 'textarea'),
        ],
        'authorities': [
            {
                'title': 'CAPR 20-3 — Inspections and Compliance Analyses Implementation Guide',
                'version': '18 May 2026',
                'url': CAP_PUBLICATIONS_URL,
                'retrieved': SOURCE_RETRIEVED,
            },
            {
                'title': 'CAP NHQ SUI Information',
                'version': 'Current public SUI information page',
                'url': CAP_SUI_URL,
                'retrieved': SOURCE_RETRIEVED,
            },
        ],
        'system_prompt': (
            "You are a CAP unit-inspection coach helping a squadron / group prepare for "
            "a Subordinate Unit Inspection (SUI). Given the unit + timeline + worry-list, "
            "produce a prioritized prep plan grounded in CAPR 20-3, dated 18 May 2026, and "
            "the current SUI worksheets/checklists available through CAP systems. (1) "
            "SCOPE FIRST — tell the user to obtain the exact current worksheet for the "
            "unit and inspection cycle; do not assert a universal set of graded areas. "
            "(2) DOCUMENTS TO PULL — suggest evidence only for applicable functions and "
            "label every item 'confirm against the current worksheet.' (3) CURRENT "
            "PUBLICATION MAP — use only well-supported references: CAPR 1-1 Ethics Policy; "
            "CAPR 30-1 Organization; CAPR 39-2 Membership; CAPR 40-1 Senior Member "
            "Education & Training; CAPR 60-1 Cadet Program Management; CAPR 60-2 Cadet "
            "Protection Program; CAPR 100-1/100-3 Communications; CAPR 130-2 Aircraft "
            "Maintenance; CAPR 132-1 Vehicle Management; CAPR 160-1 Safety; CAPR 173-1 "
            "Financial Procedures; CAPR 174-1 Property Management; and CAPR 190-1 Public "
            "Affairs. Never cite CAPR 20-1 for organization, CAPR 1-2 for ethics, or CAPR "
            "60-3 for emergency services. (4) WEEK-BY-WEEK PLAN — prioritize missing "
            "required evidence and overdue corrective actions; never suggest backdating, "
            "fabricating records, or marking an item complete without evidence. (5) "
            "UNKNOWN OR CONTROLLED MATERIAL — say 'not confirmed from the public index' "
            "and refer the user to the assigned inspector or current eServices worksheet. "
            "(6) DISCLAIMER — CAPR 20-3, the current worksheet, and the assigned inspection "
            "team are authoritative."
        ),
    },
}


def get_tool(slug: str) -> dict | None:
    return TOOLS.get(slug)


def all_slugs() -> list[str]:
    return list(TOOLS.keys())
