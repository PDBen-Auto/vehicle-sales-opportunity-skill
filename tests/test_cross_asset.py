import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_workflow import builder,SKILL,fixture

class CrossAssetTests(unittest.TestCase):
    def multi(self):return json.loads((SKILL/'assets/demo-multitype.json').read_text(encoding='utf-8'))
    def test_all_five_asset_types_and_metrics_separate(self):
        a,o,q=builder.analyze(self.multi(),'a'*64)
        self.assertEqual({r['assetType']for r in a['series']},{'automobile','motorcycle','utv','atv','boat'})
        rows=[r for r in a['series']if r['seriesId']=='demo.explorer']
        self.assertEqual(len(rows),5)
        self.assertEqual(len({i['id']for i in o['items']}),len(o['items']))
        retail=next(r for r in rows if r['assetType']=='utv'and r['metricKind']=='retail_sales')
        wholesale=next(r for r in rows if r['assetType']=='utv'and r['metricKind']=='wholesale')
        self.assertEqual(retail['currentUnits'],1680)
        self.assertEqual(wholesale['currentUnits'],4200)
        segments=[s for s in a['segments']if s['assetType']=='utv']
        self.assertEqual({s['currentUnits']for s in segments},{1680,4200})
    def test_v1_defaults_preserved(self):
        a,_,_=builder.analyze(fixture(),'a'*64)
        self.assertTrue(all(r['assetType']=='automobile'and r['metricKind']=='retail_sales'for r in a['series']))
    def test_bad_type_and_metric_rejected(self):
        for key,value in [('assetType','engine'),('metricKind','recall_units'),('metricKind','vio')]:
            with self.subTest(key=key,value=value):
                d=fixture();d['records'][0][key]=value
                with self.assertRaises(ValueError):builder.validate(d)
    def test_registration_isolated_from_sales(self):
        d=fixture();extra=[]
        for r in d['records']:
            r=copy.deepcopy(r);r['metricKind']='new_registrations';extra.append(r)
        d['records']+=extra
        a,_,q=builder.analyze(d,'a'*64)
        self.assertEqual(q['seriesCount'],18)
        self.assertEqual(q['pairedSeries'],16)
        self.assertEqual({r['metricKind']for r in a['series']},{'retail_sales','new_registrations'})
    def test_markdown_never_adds_asset_types_or_metric_kinds(self):
        a,o,_=builder.analyze(self.multi(),'a'*64)
        report=builder.markdown_report(a,o)
        self.assertIn('US / utv / retail_sales',report)
        self.assertIn('US / utv / wholesale',report)
        self.assertIn('US / boat / retail_sales',report)

if __name__=='__main__':unittest.main()
