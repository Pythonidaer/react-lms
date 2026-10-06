const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
let playwright;try{playwright=require('playwright');}catch{playwright=require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright'));}
const course=JSON.parse(fs.readFileSync('course.json','utf8'));
(async()=>{
 let launch={headless:true};
 if(process.env.LMS_CHROMIUM_PACKAGE){const {default:chromium}=await import(path.resolve(process.env.LMS_CHROMIUM_PACKAGE,'build/index.js'));launch={...launch,args:chromium.args,executablePath:process.env.LMS_CHROMIUM_EXECUTABLE||await chromium.executablePath()};}
 const browser=await playwright.chromium.launch(launch),page=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));fs.mkdirSync('test-results',{recursive:true});
 const base=process.env.LMS_TEST_URL||'http://localhost:8000';await page.goto(base);
 const item=id=>page.locator(`[data-lms=open][data-id="${id}"]`);
 const toggle=page.locator('header [data-lms=outline]');
 async function outline(){if(!(await page.locator('#lms-outline').isVisible()))await toggle.click();}
 async function open(n){await outline();const details=page.locator('details[data-lms-section]').filter({has:item(n.id)}).first();if(await details.count()&&await details.getAttribute('open')===null)await details.locator('summary').click();await item(n.id).click();}
 const next=page.locator('[data-lms=slide-next]'),complete=page.locator('[data-lms=complete]'),guide=page.locator('[data-lms=guide]');
 assert.equal(await complete.isDisabled(),true);assert.equal(await guide.isDisabled(),true);
 await page.locator('header [data-view=report]').click();assert.equal(await page.locator('#lms-average-grade').innerText(),'—');assert.ok((await page.locator('.lms-report-heading').innerText()).includes('YOUR RESULTS'));
 await page.locator('header [data-view=settings]').click();await page.locator('#lms-unlock-all').uncheck();await page.locator('header [data-view=learn]').click();
 await page.locator('[data-lms-notes]').fill('Separate React from the application host.');
 assert.equal(await item(course.sections[0].children[1].id).isDisabled(),true);
 for(let si=0;si<course.sections.length;si++){
  const section=course.sections[si];
  await open(section.children[0]);
  await next.click();
  for(const width of [1440,768,390]){
   await page.setViewportSize({width,height:1000});
   if(width===390&&await page.locator('#lms-outline').isVisible())await toggle.click();
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true,`${section.id} page overflow at ${width}`);
   assert.equal(await page.locator('#lms-main').evaluate(el=>el.scrollWidth<=el.clientWidth+1),true,`${section.id} main overflow at ${width}`);
  }
  await page.setViewportSize({width:1440,height:1000});
  for(let i=0;i<3;i++)await next.click();await complete.click();
  await open(section.children[1]);
  if(si===0){
   for(const q of section.children[1].questions)await page.locator(`input[name="q-${q.id}"][value="${(q.answer+1)%q.options.length}"]`).check();
   await page.locator('#lms-quiz button[type=submit]').click();assert.equal(await guide.isDisabled(),true);
  }
  for(const q of section.children[1].questions)await page.locator(`input[name="q-${q.id}"][value="${q.answer}"]`).check();
  await page.locator('#lms-quiz button[type=submit]').click();assert.equal(await guide.isEnabled(),true);
  if(si===0){const promise=page.waitForEvent('download');await guide.click();const download=await promise;await download.saveAs('test-results/section-guide.md');const text=fs.readFileSync('test-results/section-guide.md','utf8');assert.ok(text.includes('Separate React from the application host.'));assert.ok(text.includes('CC BY 4.0'));}
 }
 await open(course.finalQuiz);for(const q of course.finalQuiz.questions)await page.locator(`input[name="q-${q.id}"][value="${q.answer}"]`).check();await page.locator('#lms-quiz button[type=submit]').click();
 await page.reload();assert.ok((await item(course.finalQuiz.id).innerText()).includes('Passed'));
 await page.locator('header [data-view=report]').click();assert.equal(await page.locator('#lms-average-grade').innerText(),'100%');assert.equal(await page.locator('tbody tr').count(),36);
 await toggle.click();assert.equal(await page.locator('#lms-outline').isVisible(),false);await page.reload();assert.equal(await page.locator('#lms-outline').isVisible(),false);
 for(const width of [1440,768,390]){await page.setViewportSize({width,height:1000});assert.equal(await page.locator('#lms-main').evaluate(el=>el.scrollWidth<=el.clientWidth+1),true,`Report overflow at ${width}`);await page.screenshot({path:`test-results/report-${width}.png`});}
 await page.setViewportSize({width:1440,height:1000});await toggle.click();const asideTop=await page.locator('#lms-outline').evaluate(el=>el.getBoundingClientRect().top);await page.locator('#lms-main').evaluate(el=>el.scrollTop=el.scrollHeight);assert.equal(await page.locator('#lms-outline').evaluate(el=>el.getBoundingClientRect().top),asideTop);
 // Content changes invalidate their own completion and dependent sequential items.
 await page.addInitScript(()=>document.addEventListener('DOMContentLoaded',()=>{const data=document.querySelector('#lms-course-data'),raw=JSON.parse(data.textContent);raw.sections[0].children[0].slides[0].body+='\nUpdated explanation.';data.textContent=JSON.stringify(raw);}));
 await page.evaluate(()=>location.hash='learn');await page.reload();await open(course.sections[0].children[0]);assert.equal(await guide.isDisabled(),true);assert.equal(await item(course.sections[0].children[1].id).isDisabled(),true);
 assert.deepEqual(errors,[]);await browser.close();console.log('Browser checks passed: all 70 lesson/quiz items, final, failure/retake, guide notes/attribution, persistence/invalidation, sidebar and independent scrolling, reports and 390/768/1440px layouts.');
})().catch(e=>{console.error(e);process.exit(1);});
