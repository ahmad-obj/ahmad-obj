from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'assets' / 'editorial'
PALETTE = {'#0B0B0A','#F1EEE7','#9B9993','#343432','#F04A2A'}
PANELS = ['00-cover.svg','01-automotive.svg','02-orchestration.svg','03-digit.svg','04-secondary.svg','05-stack.svg','06-end.svg']

class ReadmeV2Tests(unittest.TestCase):
    def test_all_panels_exist_and_are_static_accessible_svg(self):
        for name in PANELS:
            p = ASSET / name
            self.assertTrue(p.exists(), name)
            text = p.read_text()
            self.assertNotRegex(text, r'<(?:script|animate|animateTransform|animateMotion)\b')
            root = ET.parse(p).getroot()
            self.assertEqual(root.attrib.get('viewBox','').split()[:3], ['0','0','1200'])
            titles = [e for e in root.iter() if e.tag.endswith('title')]
            self.assertTrue(titles and ''.join(titles[0].itertext()).strip())

    def test_palette_is_locked(self):
        colors=set()
        for name in PANELS:
            colors.update(re.findall(r'#[0-9A-Fa-f]{6}', (ASSET/name).read_text()))
        self.assertTrue(colors <= PALETTE, colors - PALETTE)

    def test_required_project_copy_is_present(self):
        auto=(ASSET/'01-automotive.svg').read_text()
        orch=(ASSET/'02-orchestration.svg').read_text()
        digit=(ASSET/'03-digit.svg').read_text()
        self.assertIn('3D AUTOMOTIVE', auto); self.assertIn('THREE.JS', auto)
        self.assertIn('MULTIMODEL', orch); self.assertIn('LANGGRAPH', orch)
        self.assertIn('AI DIGIT', digit); self.assertIn('PYTORCH', digit); self.assertIn('28×28', digit)

    def test_panels_have_distinct_composition_markers(self):
        expected={'01-automotive.svg':'composition-diagonal','02-orchestration.svg':'composition-route','03-digit.svg':'composition-crop'}
        for name,marker in expected.items():
            self.assertIn(marker,(ASSET/name).read_text())

    def test_secondary_stack_and_end_are_minimal(self):
        secondary=(ASSET/'04-secondary.svg').read_text()
        stack=(ASSET/'05-stack.svg').read_text()
        end=(ASSET/'06-end.svg').read_text()
        for s in ['SIXTY-FOUR','WEBERAISE','SCOUT EMAIL']: self.assertIn(s, secondary)
        for s in ['PYTHON','C++','TYPESCRIPT','THREE.JS','WEBGL','PYTORCH','LANGGRAPH','LINUX']: self.assertIn(s, stack)
        self.assertIn('MUHAMMAD AHMAD',end)
        self.assertLess(end.count('<text'),8)

class ReadmeCompositionTests(unittest.TestCase):
    def test_readme_uses_editorial_sequence_and_real_links(self):
        readme=(ROOT/'README.md').read_text()
        order=['00-cover.svg','01-automotive.svg','02-orchestration.svg','03-digit.svg','04-secondary.svg','05-stack.svg','06-end.svg']
        positions=[readme.index(name) for name in order]
        self.assertEqual(positions,sorted(positions))
        for url in [
            'https://github.com/ahmad-obj/3dcarweb',
            'https://github.com/ahmad-obj/multimodel-orchestration',
            'https://github.com/ahmad-obj/AI-digit-recognizer',
            'https://github.com/ahmad-obj/Chess',
            'https://github.com/ahmad-obj/Weberaise',
            'https://github.com/ahmad-obj/scout-email',
        ]: self.assertIn(url,readme)
        self.assertIn('artifacts/audit-reality/03-hero.png',readme)
        self.assertNotIn('geometric-system.svg',readme)
        self.assertNotIn('github-readme-stats',readme)
        self.assertNotIn('shields.io',readme)

    def test_readme_identity_copy_is_concise(self):
        readme=(ROOT/'README.md').read_text()
        for s in ['Muhammad Ahmad','Computer Science @ FAST-NUCES','Portfolio','LinkedIn','Email']:
            self.assertIn(s,readme)

if __name__=='__main__': unittest.main()
