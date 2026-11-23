import unittest
from host_gate import tests,signatures,compare,gate

def run_result(text,rc=1): return {'stdout':'','stderr':text,'exit_code':rc,'timed_out':False}
def snap(text,rc=1):
 r=run_result(text,rc)
 return {'suite':{'run':r,'summary':tests(r),'signatures':signatures(r)},'base_health':run_result('',0),'extension_summary':run_result('',0)}
class HostGateTests(unittest.TestCase):
 def test_named_recovery(self):
  before=snap('test_schema (tests.test_registry.Case) ... ERROR\nRan 1 tests\nFAILED (errors=1)\nschema mismatch')
  after=snap('test_schema (tests.test_registry.Case) ... ok\nRan 1 tests\nOK',0)
  d=compare(before,after)
  self.assertIn('tests.test_registry.Case.test_schema',d['recovered_by_name'])
  self.assertEqual(d['signature_counts']['F14']['after'],0)
 def test_missing_not_recovered(self):
  d=compare(snap('test_schema (tests.Case) ... ERROR'),snap('Ran 0 tests\nOK',0))
  self.assertFalse(d['recovered_by_name'])
 def test_no_merge_authority(self):
  g=gate(snap('Ran 0 tests\nOK',0),None)
  self.assertEqual(g['decision'],'REVIEW_REQUIRED')
  self.assertEqual(g['checks']['M5_main_merge_authorized'],'BLOCKED')
 def test_signatures(self):
  s=signatures(run_result('schema mismatch\nbad digests 9\ndata.vaule unregistered field'))
  self.assertTrue(s['F14']);self.assertTrue(s['M2']);self.assertTrue(s['M6'])
if __name__=='__main__': unittest.main()
