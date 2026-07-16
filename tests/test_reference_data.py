import unittest
from pathlib import Path

from tools_data import SOURCE_RETRIEVED, TOOLS


ROOT = Path(__file__).resolve().parents[1]


class ReferenceDataTests(unittest.TestCase):
    def test_every_tool_exposes_dated_authoritative_sources(self):
        self.assertEqual(SOURCE_RETRIEVED, '2026-07-16')
        for slug, tool in TOOLS.items():
            with self.subTest(tool=slug):
                self.assertTrue(tool.get('authorities'))
                for source in tool['authorities']:
                    self.assertTrue(source['url'].startswith('https://'))
                    self.assertEqual(source['retrieved'], SOURCE_RETRIEVED)
                    self.assertTrue(source['title'])
                    self.assertTrue(source['version'])

    def test_form_drafter_refuses_unconfirmed_legacy_examples(self):
        prompt = TOOLS['form-drafter']['system_prompt']
        self.assertIn('CAPF 2A, CAPF 24, CAPF 31, and CAPF 60-80 are not present', prompt)
        self.assertIn('FORM NOT CONFIRMED', prompt)
        self.assertNotIn('Application for and Approval of Civil Air Patrol Activity', prompt)
        self.assertNotIn('Mission Information Form', prompt)
        self.assertNotIn('Application for Senior Member Membership', prompt)

    def test_specialty_track_uses_current_guides_without_sqtr_claims(self):
        prompt = TOOLS['specialty-track']['system_prompt']
        self.assertIn('CAP Pamphlet 70-1 Operations Officer', prompt)
        self.assertIn('CAP Pamphlet 214 Communications Officer', prompt)
        self.assertIn('CAP Pamphlet 60-11 Cadet Programs Officer', prompt)
        self.assertIn('Do not call specialty-track requirements SQTRs', prompt)
        self.assertNotIn('CAPP 207', prompt)
        self.assertNotIn('CAPP 217', prompt)
        self.assertNotIn('AXIS', prompt)

    def test_sui_prompt_uses_current_regulation_map(self):
        prompt = TOOLS['sui-prep']['system_prompt']
        self.assertIn('CAPR 20-3, dated 18 May 2026', prompt)
        self.assertIn('CAPR 30-1 Organization', prompt)
        self.assertIn('CAPR 1-1 Ethics Policy', prompt)
        self.assertIn('CAPR 60-2 Cadet Protection Program', prompt)
        self.assertIn('Never cite CAPR 20-1 for organization', prompt)

    def test_deploy_workflow_tracks_reference_data(self):
        workflow = (ROOT / '.github/workflows/deploy.yml').read_text()
        self.assertIn("- 'tools_data.py'", workflow)


if __name__ == '__main__':
    unittest.main()
