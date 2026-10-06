"""Regenerate the static course from original authored curriculum. No network."""
import json,re
from pathlib import Path
from curriculum import MODULES
ROOT=Path(__file__).resolve().parents[1]
def source(path): return {'title':path.rsplit('/',1)[-1].replace('-',' ').title() or 'React documentation','url':'https://react.dev'+path}
def question(row,id,shift):
    prompt,correct,a,b,explanation=row
    options=[correct,a,b];options=options[shift:]+options[:shift]
    return {'id':id,'prompt':prompt,'options':options,'answer':options.index(correct),'explanation':explanation}
sections=[]
for i,m in enumerate(MODULES):
    sid='react-sec-'+m['slug'];lid='react-lesson-'+m['slug'];sources=[source(p) for p in m['paths']]
    def slide(kind,title,body): return {'id':lid+'-'+kind,'title':title,'body':body}
    language='css' if m['slug']=='activity-motion' else 'tsx' if m['slug']=='typescript' else 'jsx'
    solution=m['solution']
    if solution.startswith(('function ','export ','const ','type ','/*')):solution='```'+language+'\n'+solution+'\n```'
    lesson={'id':lid,'type':'slides','title':m['title'],'minutes':30,'objectives':[m['goal']],'sources':sources,'slides':[
      slide('concept',m['title'],'YOUR GOAL\n'+m['goal']+'\n\n'+m['concept']),
      slide('example','Read and reason about the example','```jsx\n'+m['example']+'\n```\n\nRead the surrounding explanation before copying. Snippets may require the imports, helpers or host identified in their comments. Server/framework examples are architecture sketches, not executable browser lessons.'),
      slide('practice','Practice before opening the solution',m['practice']+'\n\nExplain your prediction, implement the change, then compare behavior. Use your chosen React project; this LMS displays code but does not execute or grade it.'),
      slide('solution','Compare your solution',solution),
      slide('takeaway','Retain and apply the skill',m['takeaway']+'\n\nSELF CHECK\nCan you explain the model, identify a failure case and demonstrate the task without copying? Complete the section quiz next. Practical exercises are self-assessed; use the capstone rubric for application evidence.') ]}
    quiz={'id':sid+'-quiz','type':'quiz','title':'Skill check · '+m['title'],'skill':m['title'],'sources':sources,'questions':[question(q,sid+'-q'+str(j+1),(i+j)%3) for j,q in enumerate(m['questions'][:3])]}
    sections.append({'id':sid,'type':'section','title':f'{i+1:02} · '+m['title'],'sources':sources,'studyGuide':{'title':m['title']+' study guide','summary':m['goal'],'takeaways':[m['takeaway'],m['concept']]},'children':[lesson,quiz]})
old=json.loads((ROOT/'course.json').read_text())
course={'schemaVersion':1,'id':'react-skills-complete-v1','title':'React skills','description':'An independent skills path based on the official react.dev snapshot: components, state, escape hatches, modern APIs, server integration, compiler, testing and a capstone. JavaScript and HTML/CSS familiarity are prerequisites. Specialist and historical material is indexed separately.','sections':sections,'finalQuiz':{'id':'react-final-skills','type':'quiz','title':'Final assessment · Apply React judgment','skill':'Integrated React judgment','sources':[source('/learn'),source('/reference/react')],'questions':[question(m['questions'][3],'react-final-q'+str(i+1),(i+1)%3) for i,m in enumerate(MODULES)]},'settings':{**old['settings'],'passScore':80,'allowRetakes':True,'unlockAll':True,'sequential':True,'requireLessons':True,'showLessonDetails':False}}
(ROOT/'course.json').write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n')
html=(ROOT/'index.html').read_text();embedded=json.dumps(course,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
html=re.sub(r'(<script id="lms-course-data" type="application/json">).*?(</script>)',lambda m:m[1]+embedded+m[2],html,flags=re.S)
html=re.sub(r'<title>.*?</title>','<title>React skills</title>',html,count=1)
(ROOT/'index.html').write_text(html)
print(f'{len(sections)} sections, {len(sections)*5} slides, {len(sections)*3} section questions, {len(sections)} final questions')
