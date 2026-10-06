const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs');
const {JSDOM}=require('jsdom');
test('Rendered capstone supports validation, add, complete, search and remove',async()=>{
 const dom=new JSDOM('<div id="root"></div>',{url:'http://localhost'});
 global.window=dom.window;global.document=dom.window.document;global.HTMLElement=dom.window.HTMLElement;global.FormData=dom.window.FormData;global.IS_REACT_ACT_ENVIRONMENT=true;
 const React=require('react'),{createRoot}=require('react-dom/client');
 fs.mkdirSync('tests/.generated',{recursive:true});
 require('esbuild').buildSync({entryPoints:['examples/App.jsx'],bundle:true,platform:'node',format:'cjs',jsx:'automatic',external:['react','react/jsx-runtime'],outfile:'tests/.generated/App.cjs'});
 const App=require('./.generated/App.cjs').default,root=createRoot(document.getElementById('root'));
 const act=React.act;await act(async()=>root.render(React.createElement(App)));
 const submit=async()=>act(async()=>document.querySelector('form').dispatchEvent(new dom.window.Event('submit',{bubbles:true,cancelable:true})));
 document.querySelector('input[name=title]').value='   ';await submit();assert.match(document.querySelector('[role=alert]').textContent,/Enter/);
 document.querySelector('input[name=title]').value='Learn JSX';await submit();assert.equal(document.querySelectorAll('li').length,1);assert.equal(document.querySelector('[role=alert]'),null);
 await act(async()=>document.querySelector('li input').click());assert.match(document.querySelector('[role=status]').textContent,/1 of 1/);
 // Drive React's controlled onChange through a native input event.
 const search=document.querySelector('input[id]');const setter=Object.getOwnPropertyDescriptor(dom.window.HTMLInputElement.prototype,'value').set;
 await act(async()=>{setter.call(search,'missing');search.dispatchEvent(new dom.window.Event('input',{bubbles:true}));});assert.match(document.body.textContent,/No matching/);
 await act(async()=>{setter.call(search,'');search.dispatchEvent(new dom.window.Event('input',{bubbles:true}));});assert.equal(document.querySelectorAll('li').length,1);
 await act(async()=>document.querySelector('li button').click());assert.match(document.body.textContent,/Add your first/);
 await act(async()=>root.unmount());dom.window.close();delete global.IS_REACT_ACT_ENVIRONMENT;
});
