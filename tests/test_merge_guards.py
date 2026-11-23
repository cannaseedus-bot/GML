import sys, unittest, tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'core'))
from gml2 import parse
from assemble import load_directory
from registry import load_registry, validate_document, RegistryError
from extension import owns_document
ROOT=Path(__file__).resolve().parents[1]
class TestMergeGuards(unittest.TestCase):
 def test_f14_other_schema_not_validated_by_tensor(self):
  with tempfile.TemporaryDirectory() as d:
   (Path(d)/'other.gml').write_text('graph [ schema "aiml-gml/1" graph_id "aiml/other" contract "pattern" ]')
   (Path(d)/'tensor.gml').write_text((ROOT/'contracts/col_a.gml').read_text())
   docs=load_directory(d)
   self.assertEqual(len(docs),2)
   self.assertFalse(owns_document(load_registry().extension, docs['aiml/other']))
 def test_m2_data_typo_rejected(self):
  doc=parse((ROOT/'contracts/col_a.gml').read_text().replace('value 1.0','vaule 1.0'))
  with self.assertRaisesRegex(RegistryError,'unregistered field: data.vaule'): validate_document(doc,load_registry())
 def test_m2_graph_typo_rejected(self):
  doc=parse((ROOT/'contracts/assembled.gml').read_text().replace('directed 1','directde 1'))
  with self.assertRaisesRegex(RegistryError,'unregistered field: graph.directde'): validate_document(doc,load_registry())
 def test_m2_unknown_coverage_rejected(self):
  doc=parse((ROOT/'contracts/assembled.gml').read_text().replace('coverage_policy "complete"','coverage_policy "invalid"'))
  with self.assertRaisesRegex(RegistryError,'graph.coverage_policy enum mismatch'): validate_document(doc,load_registry())
