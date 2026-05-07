# CAPHub

Static landing page for Fresh Sky AI's free Civil Air Patrol tools. Live at <https://cap.freshskyai.com>.

The umbrella site that:
- Tells the volunteer-CAP-member-and-engineer pitch
- Links to live tools (CAPR Search, CAPStudy, CAPMeeting)
- Lists the roadmap
- Is the canonical URL to send to a CC, training officer, or wing staff

Standalone Flask app, no `freshsky_common` dependency. The whole thing is one route serving an HTML template.
