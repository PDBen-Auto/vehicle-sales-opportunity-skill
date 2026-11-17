import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('site_builder',ROOT/'tools/build_site.py')
site=importlib.util.module_from_spec(spec);spec.loader.exec_module(site)

class PublicSiteTests(unittest.TestCase):
    def test_site_preserves_case_and_required_navigation(self):
        with tempfile.TemporaryDirectory()as tmp:
            output=Path(tmp)/'site';result=site.build(output)
            self.assertEqual(result['status'],'pass')
            self.assertEqual((output/'cases/utv-atv/index.html').read_bytes(),(ROOT/'cases/utv-atv/输出/北美UTV保有量研究-20261117.html').read_bytes())
            self.assertTrue((output/'cases/utv-atv/北美UTV车型保有量保守情景-20261117.xlsx').is_file())
            for rel in ['demo/dashboard.html','multitype-demo/dashboard.html','cases/utv-atv/data/snapshots/cpsc-5177.json']:
                self.assertTrue((output/rel).is_file(),rel)
            self.assertFalse((output/'.git').exists())
            self.assertFalse((output/'过程').exists())
            self.assertIn('cases/utv-atv/',(output/'index.html').read_text(encoding='utf-8'))
            with self.assertRaises(ValueError):site.build(output)

if __name__=='__main__':unittest.main()
