const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const esbuild = require('esbuild');
const raw = JSON.parse(fs.readFileSync('course.json', 'utf8'));
const LMS = vm.runInNewContext(fs.readFileSync('lms-runtime.js', 'utf8') + '; LMS', { URL, crypto: require('node:crypto').webcrypto });
test('Offline data agrees and the authored skills path is complete', () => {
  const html = fs.readFileSync('index.html', 'utf8');
  assert.deepEqual(JSON.parse(html.match(/<script id="lms-course-data" type="application\/json">([\s\S]*?)<\/script>/)[1]), raw);
  const course = LMS.validate(raw);
  assert.equal(course.sections.length, 35);
  assert.equal(LMS.flatten(course.sections).length, 70);
  assert.deepEqual(Array.from(LMS.ready(course)), []);
  let sectionQuestions=0;
  const allPrompts=[];
  for (const section of course.sections) {
    assert.equal(section.children[0].slides.length, 5);
    assert.ok(section.studyGuide.summary.length > 20);
    assert.ok(section.children[0].sources.length > 0);
    assert.equal(section.children[1].skill, section.studyGuide.title.replace(' study guide',''));
    for (const q of section.children[1].questions) { sectionQuestions++; allPrompts.push(q.prompt); }
  }
  assert.equal(sectionQuestions,105);
  assert.equal(course.finalQuiz.questions.length,35);
  for(const q of course.finalQuiz.questions) assert.ok(!allPrompts.includes(q.prompt),'Final questions must be fresh scenarios');
});
test('Source inventory resolves all linked routes and retains honest coverage', () => {
  const inventory=JSON.parse(fs.readFileSync('docs/source-inventory.json','utf8'));
  assert.equal(inventory.entries.length,225);
  const urls=new Set(inventory.entries.map(e=>e.url));
  for(const section of raw.sections) for(const source of section.sources) assert.ok(urls.has(source.url),source.url);
  assert.ok(inventory.counts['reference-only']>0);
  assert.ok(inventory.counts['site-or-history']>0);
  assert.equal(inventory.commit,'046f17d04295ba047bb5739026b4ac3110f17028');
});
test('All 35 authored examples parse as JSX or TSX; sketches are not claimed executable', () => {
  for(const section of raw.sections) {
    const body=section.children[0].slides[1].body;
    const code=body.match(/```jsx\n([\s\S]*?)```/)[1];
    assert.doesNotThrow(()=>esbuild.transformSync(code,{loader:section.id.endsWith('typescript')?'tsx':'jsx',jsx:'automatic'}),section.title);
  }
});
test('Code escapes HTML, source URLs are restricted, and guides retain attribution and notes', () => {
  assert.ok(LMS.prose('```jsx\n<img src=x onerror=alert(1)>\n```').includes('&lt;img'));
  const changed=JSON.parse(JSON.stringify(raw));changed.sections[0].children[0].sources.push({title:'Unsafe',url:'javascript:alert(1)'});
  assert.ok(!LMS.validate(changed).sections[0].children[0].sources.some(s=>s.title==='Unsafe'));
  const section=LMS.validate(raw).sections[0];
  const guide=LMS.studyGuide(section,{[section.children[0].id]:{notes:'Document host responsibilities.'}});
  for(const phrase of ['Document host responsibilities.','## Sources','CC BY 4.0','Compare your solution','Practice before']) assert.ok(guide.includes(phrase));
  assert.ok(!guide.includes('TypeScript contributors'));
});
