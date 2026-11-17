"""Snapshot byte provenance must survive platform-specific text defaults."""
import hashlib,importlib.util,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('case_reproduce',ROOT/'cases/utv-atv/reproduce.py')
case=importlib.util.module_from_spec(spec);spec.loader.exec_module(case)

class PortabilityTests(unittest.TestCase):
    def test_rewrite_keeps_source_checksum_for_lf_and_crlf(self):
        with tempfile.TemporaryDirectory()as tmp:
            work=Path(tmp)
            for index,newline in enumerate([b'\n',b'\r\n']):
                source=work/f'input-{index}.json'
                content=b'{'+newline+b'  "quantity": 34000'+newline+b'}'
                source.write_bytes(content)
                script=work/f'builder-{index}.py'
                script.write_text('from pathlib import Path\np=Path('+repr(str(source))+')\np.write_text(p.read_text(encoding="utf-8"),encoding="utf-8")\n',encoding='utf-8')
                expected=hashlib.sha256(content).hexdigest()
                case.run_frozen_builder(script)
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),expected)

if __name__=='__main__':unittest.main()
