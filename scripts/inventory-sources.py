"""Inventory a local pinned react.dev checkout; never crawl external sites."""
import argparse,collections,hashlib,json,re,subprocess
from pathlib import Path
from curriculum import MODULES
parser=argparse.ArgumentParser();parser.add_argument('--source-root',default='../react-docs');args=parser.parse_args()
source=Path(args.source_root).resolve();root=Path(__file__).resolve().parents[1]
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
mapping=collections.defaultdict(list)
for m in MODULES:
 for route in m['paths']:mapping[route].append('react-sec-'+m['slug'])
entries=[]
for p in sorted((source/'src/content').rglob('*.md')):
 rel=p.relative_to(source/'src/content');route='/'+str(rel.with_suffix(''))
 if route.endswith('/index'):route=route[:-6]
 if route=='/index':route='/'
 text=p.read_text();title=re.search(r'^title:\s*(.+)',text,re.M)
 modules=mapping.get(route,[])
 status='lesson-source' if modules else 'reference-only' if str(rel).startswith(('learn/','reference/')) else 'site-or-history'
 if 'rsc-sandbox-test' in route:status='internal-source'
 entries.append({'path':str(p.relative_to(source)),'route':route,'url':'https://react.dev'+route,'title':title[1].strip('"') if title else rel.stem,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'coverage':status,'sections':modules,'review':'intro-and-structure-reviewed' if str(rel).startswith(('learn/','reference/')) else 'inventory-only'})
missing=sorted(set(mapping)-{e['route'] for e in entries})
if missing:raise SystemExit('Source routes not present: '+str(missing))
data={'repository':'https://github.com/reactjs/react.dev','commit':commit,'snapshotDate':'2026-10-06','scope':'Every Markdown content file in src/content of this snapshot; not every external link, redirect, image or archived documentation domain. Inventory does not imply full reading or lesson reproduction.','counts':dict(collections.Counter(e['coverage'] for e in entries)),'entries':entries}
(root/'docs/source-inventory.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
lines=['# React documentation coverage','',f'Snapshot: `{commit}`. {len(entries)} content files.','', 'Legend: lesson-source = linked primary reading for an authored skill; reference-only = indexed lookup/specialist or overview page; site-or-history = site/community/blog material outside the skill sequence; internal-source = repository test page. A source link does not mean every example or API option on that page is taught.','', '| Documentation | Coverage | Course sections |','| --- | --- | --- |']
for e in entries:lines.append('| ['+e['title'].replace('|','\\|')+']('+e['url']+') | '+e['coverage']+' | '+', '.join(e['sections'])+' |')
(root/'docs/COVERAGE.md').write_text('\n'.join(lines)+'\n')
print(len(entries),data['counts'])
