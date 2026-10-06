import test from 'node:test';
import assert from 'node:assert/strict';
import { planReducer, selectLessons } from '../examples/model.mjs';
test('Reducer rejects malformed/duplicate input and preserves immutable history', () => {
 const before=Object.freeze([{id:'a',title:'JSX',completed:false}].map(Object.freeze));
 const after=planReducer(before,{type:'toggled',id:'a'});
 assert.equal(before[0].completed,false);assert.equal(after[0].completed,true);
 assert.throws(()=>planReducer(before,{type:'added',lesson:{id:'a',title:'Duplicate'}}),/Unique/);
 assert.throws(()=>planReducer(before,{type:'added',lesson:{id:'b',title:'   '}}),/Title/);
 assert.throws(()=>planReducer(before,{type:'unknown'}),/Unknown/);
 const added=planReducer(before,{type:'added',lesson:{id:'b',title:'  State  '}});
 assert.equal(added[1].title,'State');assert.equal(added[0],before[0]);
 assert.equal(planReducer(added,{type:'removed',id:'a'}).length,1);
});
test('Filtering is derived, case-insensitive and does not overwrite canonical data', () => {
 const items=[{id:'a',title:'JSX',completed:false},{id:'b',title:'State',completed:true}];
 assert.deepEqual(selectLessons(items,' state ',false),[items[1]]);
 assert.deepEqual(selectLessons(items,'',true),[items[1]]);
 assert.deepEqual(selectLessons(items,'missing',false),[]);assert.equal(items.length,2);
});
