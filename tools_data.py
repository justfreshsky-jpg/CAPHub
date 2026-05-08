"""
CAP tool definitions for /tools/<slug> routes on cap.freshskyai.com.

Each tool is a single LLM-driven worksheet — one form, one prompt,
one result page. Stateless. Free for CAP members + squadrons. Public-
domain content, not affiliated with Civil Air Patrol Inc.
"""
from __future__ import annotations

TOOLS: dict[str, dict] = {

    'form-drafter': {
        'title':       'CAP Form Drafter',
        'tagline':     'Draft commonly-used CAP forms (CAPF 2A activity, CAPF 24 SAR mission report, CAPF 31 application narrative, CAPF 60-80 incident report, etc.)',
        'icon':        '📋',
        'fields': [
            ('form',     'Which CAPF form (e.g. "CAPF 2A activity proposal")', 'input'),
            ('context',  'Activity / mission / situation details — who, what, when, where, why',  'textarea'),
            ('audience', 'Who reads this (squadron commander, group, wing, IC) — affects tone',   'input'),
        ],
        'system_prompt': (
            "You are a CAP staff officer helping draft Civil Air Patrol forms (CAPF series). "
            "Given a form name + the activity / situation context, produce: (1) IDENTIFY THE "
            "FORM — confirm the canonical form number (e.g. CAPF 2A 'Application for and "
            "Approval of Civil Air Patrol Activity', CAPF 24 'Mission Information Form', "
            "CAPF 31 'Application for Senior Member Membership', CAPF 60-80 'Incident "
            "Report'). If unsure, say 'verify the current form on capmembers.com'. (2) "
            "STRUCTURED DRAFT — produce a draft narrative organized by the form's section "
            "headings (per the form's own instructions). Use plain CAP-correct vocabulary "
            "(squadron / group / wing / region; senior member / cadet; encampment / SAREX / "
            "AT / IACE; SQTR / CAPT / SET; etc.). (3) WHAT'S MISSING — call out fields the "
            "user didn't provide enough info for; do not guess. (4) ROUTING — typical "
            "approval chain for that form (Sq/CC → Gp/CC → Wg/CC etc.). (5) DISCLAIMER — "
            "this is a draft based on the user-supplied details only. Always verify against "
            "the current form, current CAP regulation, and your AHJ's instructions before "
            "submission. Forms and procedures change."
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
        'system_prompt': (
            "You are a CAP Senior-Member specialty-track coach. Given a track + current "
            "rating + time budget, produce a realistic 6-month plan: (1) WHERE YOU ARE — "
            "interpret current progress and identify the very next requirement on the SQTR "
            "(Specialty Qualification Training Record) for the user's rating level. (2) "
            "MILESTONES — the next 3 SQTR line items in priority order, with realistic "
            "timing given their hours/month. Reference the CAPP series pamphlet for that "
            "track (e.g. CAPP 207 Operations, CAPP 217 Comm, CAPP 50-2 Cadet Programs "
            "etc.) — note the operator should verify current pamphlet numbers because CAP "
            "renumbers. (3) STUDY RESOURCES — only ones that are free + canonical: CAP "
            "regulations on capmembers.com, eServices Learning Management System (LMS), "
            "AXIS academy. Don't invent course names. (4) MENTOR / OJT — what they should "
            "ask their squadron CC or specialty-track mentor for; what counts as on-the-"
            "job training for this track. (5) RATING CHECKPOINTS — what they need to "
            "demonstrate to claim the next rating; reference the SQTR signoff process and "
            "the OPR / 2nd-O signature requirements. (6) DISCLAIMER — this is a planning "
            "aid based on the operator's understanding of CAP PD; current SQTRs and "
            "regulations on capmembers.com are authoritative. Verify before claiming any "
            "rating progress."
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
        'system_prompt': (
            "You are a CAP unit-inspection coach helping a squadron / group prepare for "
            "a Subordinate Unit Inspection (SUI). Given the unit + timeline + worry-list, "
            "produce a prioritized prep plan: (1) THE BIG SIX inspection compliance areas "
            "for any CAP unit: Operations + Membership / PD + Logistics / Communications + "
            "Safety + Public Affairs + Finance / Admin. Spend more text on the user's "
            "worry areas; lighter on the strength areas. (2) DOCUMENTS TO PULL — for each "
            "area, the canonical document set inspectors expect (Operating Instructions, "
            "minutes / rosters / PD records, inventory, property accountability, finance "
            "ledger and audit, safety briefings log, etc.). Reference current CAPRs by "
            "name + number where well-known (CAPR 20-1 series, 60-1 / 60-3, 39-2, 1-2 "
            "Code of Ethics, 173 finance, etc.) and tell the user to verify the current "
            "version on capmembers.com. (3) WHAT INSPECTORS ACTUALLY LOOK AT — beyond "
            "documents: cadet protection currency, member records currency, recent "
            "promotions documented, awards routed, safety-down day held, IS-100 / 200 / "
            "700 / 800 currency for relevant members, currency of OPR/Performance "
            "Reports. (4) WEEK-BY-WEEK PLAN — given the timeline the user provided, what "
            "to fix first, what to defer if there's not enough time, what to fully "
            "document vs delegate. (5) RED FLAGS to fix BEFORE the inspector walks in: "
            "expired CAPR-required currencies, missing safety briefings, finance audit "
            "gaps, members with overdue cadet protection. (6) DISCLAIMER — this is a "
            "prep aid; the SUI inspector's actual checklist (and the current CAPRs) are "
            "authoritative. Coordinate with your group / wing inspection officer + DCS / "
            "DC for current expectations."
        ),
    },
}


def get_tool(slug: str) -> dict | None:
    return TOOLS.get(slug)


def all_slugs() -> list[str]:
    return list(TOOLS.keys())
