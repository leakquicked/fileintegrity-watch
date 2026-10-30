import tempfile, unittest
from pathlib import Path
from integrity_watch import build_manifest, verify_manifest

class IntegrityTests(unittest.TestCase):
    def test_detects_change(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); f=root/"a.txt"; f.write_text("one")
            manifest=build_manifest(root,["a.txt"])
            m=root/"manifest.json"
            import json
            m.write_text(json.dumps(manifest))
            self.assertEqual(verify_manifest(m)["problems"],[])
            f.write_text("two")
            self.assertEqual(verify_manifest(m)["problems"][0]["status"],"changed")
if __name__ == "__main__": unittest.main()
