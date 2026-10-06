"""Original skills curriculum; source routes are pinned by docs/source-inventory.json."""
MODULES=[]
def M(slug,title,paths,goal,concept,example,practice,solution,takeaway,questions):
    MODULES.append(dict(slug=slug,title=title,paths=paths.split(),goal=goal,concept=concept,example=example,practice=practice,solution=solution,takeaway=takeaway,questions=questions))
# Each question: applied prompt, correct choice, two distractors, explanation.
M('orientation','Plan and run a React project','/learn /learn/installation /learn/creating-a-react-app /learn/build-a-react-app-from-scratch /learn/add-react-to-an-existing-project /learn/editor-setup /learn/react-developer-tools',
'Choose a project setup and distinguish the React library from its host tools.',
'React describes UI from data using components. A framework adds routing, data loading and rendering conventions; a build tool transforms JSX and bundles modules. The official setup guide favors frameworks for new production apps, while a from-scratch build is useful for learning or unusual constraints. Create React App is deprecated. Existing sites can adopt React in one region rather than replacing everything. Learn JavaScript functions, modules, arrays and asynchronous code first. Use browser and React developer tools to inspect the actual component tree.',
'''import { createRoot } from 'react-dom/client';
function App() { return <h1>Reading studio</h1>; }
const container = document.getElementById('root');
if (!container) throw new Error('Missing root container');
createRoot(container).render(<App />);''',
'Choose between a full application and a React widget inside an existing site. List what your host supplies: routing, build commands, asset paths and deployment. Mount one heading in a dedicated root. Change its text and inspect the component in React DevTools.',
'For a widget, keep the existing page and mount React in a dedicated element. For an application, evaluate the documented framework options. Use the host’s development/build commands; do not expect React itself to provide a router. The root in the example owns only its container. A successful local render is separate from a successful production build.',
'React is the UI library; document the runtime, build tool and framework separately.',[
('Which tool supplies application routing by default?','Your chosen framework or router','React useState','JSX itself','React core does not prescribe a router.'),
('Where can React be introduced in an existing website?','A dedicated interactive region','Only after rewriting every page','Only on a new domain','Incremental adoption can preserve the existing site.'),
('What should you use for a new setup decision?','The current installation guide','A Create React App tutorial by default','Only the number of GitHub stars','The documentation explains supported setup choices and tradeoffs.'),
('A production build works but nested URLs fail on refresh. What needs investigation?','Host routing and deployment configuration','Whether component names are capitalized','Whether useState exists','Deployment paths and routing are responsibilities beyond React core.')])
M('components','Describe UI with components and JSX','/learn/your-first-component /learn/importing-and-exporting-components /learn/writing-markup-with-jsx /learn/javascript-in-jsx-with-curly-braces /reference/react/createElement /reference/react/Fragment',
'Write a reusable component with valid JSX and module exports.',
'A function component returns a description of UI. Capitalized JSX tags refer to components; lowercase tags refer to host elements. JSX is JavaScript syntax transformed by tooling, not an HTML string. Return one parent or Fragment, close tags, and use className. Curly braces embed expressions, including attributes; they cannot contain arbitrary statements. Import names according to named versus default exports. Declare components at module scope so their identity stays stable. createElement is the non-JSX equivalent; a Fragment groups children without a wrapper DOM element.',
'''export function LessonCard({ title, minutes }) {
  return (
    <article className="lesson-card">
      <h2>{title}</h2>
      <p>{minutes} minutes</p>
    </article>
  );
}''',
'Create two LessonCards with different titles. Add a Fragment around a heading and the cards. Fix an unclosed img and a class attribute copied from HTML. Explain why you use <LessonCard /> instead of calling LessonCard directly.',
'''export default function Library() {
  return <>
    <h1>My learning plan</h1>
    <LessonCard title="Components" minutes={15} />
    <LessonCard title="State" minutes={20} />
    <img src="/cover.png" alt="Notebook cover" className="cover" />
  </>;
}
// React calls components through JSX and manages their identity.''',
'JSX describes UI; components are stable, reusable functions that React calls.',[
('How do you group siblings without another DOM wrapper?','A Fragment','An unclosed div','A quoted HTML string','Fragments group children without adding a host node.'),
('Which expression passes a numeric prop?','minutes={15}','minutes="15"','minutes="{15}"','Braces evaluate JavaScript; quoted attributes are strings.'),
('Where should a reusable component normally be declared?','At module scope','Inside another component on every render','Inside a click handler only','Nested declarations can change identity and reset child state.'),
('Your named export LessonCard cannot be imported as a default export. What fixes it?','Use a named import or change the export intentionally','Change className to class','Call the function during render','Import syntax must agree with the module export.')])
M('props','Design props and composition','/learn/passing-props-to-a-component /learn/understanding-your-ui-as-a-tree /reference/rules/react-calls-components-and-hooks',
'Design a component contract using props, children and callbacks.',
'Props carry read-only inputs from parents. Destructure them, supply appropriate defaults, and compose content with children. A callback prop lets a child request a change while the parent owns the data. Props are snapshots for a render, not a mutable storage object. Rendering a tree of components differs from a module dependency tree. Composition can avoid unnecessary configuration props: a panel can accept any children. React must call components and Hooks itself; calling a component as an ordinary function bypasses its identity and can break Hook ordering.',
'''function Panel({ title, children }) {
  return <section><h2>{title}</h2>{children}</section>;
}
function Plan({ onAdd }) {
  return <Panel title="Practice">
    <button onClick={onAdd}>Add exercise</button>
  </Panel>;
}''',
'Add a default panel title. Make a parent own the add behavior. Explain why assigning a new value to props.title cannot update the parent’s data.',
'''function Panel({ title = 'Study panel', children }) {
  return <section><h2>{title}</h2>{children}</section>;
}
function App() {
  function handleAdd() { console.log('Parent received add request'); }
  return <Plan onAdd={handleAdd} />;
}
// To change UI, update parent state rather than mutating props.''',
'Keep inputs read-only; pass behavior through callbacks and content through composition.',[
('Which component should change a value passed as a prop?','The owner of that state','The child by mutating props','The browser by changing JSX','The child requests updates; the state owner applies them.'),
('What is children useful for?','Composing arbitrary nested content','Replacing every event handler','Automatically fetching data','children represents content nested inside a component tag.'),
('Does a module import tree equal the rendered component tree?','No, they describe different relationships','Always','Only if every file uses JSX','Imports describe code dependencies; the render tree describes UI instances.'),
('A panel needs a heading and varied content. Which contract stays flexible?','A title prop plus children','One boolean for every possible child layout','A prop that mutates parent data','Composition supports varied content without a flag explosion.')])
M('lists','Render conditions and stable lists','/learn/conditional-rendering /learn/rendering-lists',
'Render filtered lists without losing item identity or showing accidental zeros.',
'Use JavaScript conditions to choose elements. A component can return null to render nothing. With &&, React can render the left-hand value when it is falsy: 0 && <Badge /> yields a visible zero, so compare counts explicitly. map transforms data to UI and filter selects entries. Keys must be stable and unique among siblings. Use domain IDs rather than array indices for lists that reorder, insert or delete. key is consumed by React and is not available as a normal prop; pass an ID separately if a child needs it.',
'''function ReadingList({ items }) {
  const visible = items.filter(item => !item.archived);
  return <>
    {visible.length > 0 && <p>{visible.length} active lessons</p>}
    <ul>{visible.map(item => <li key={item.id}>{item.title}</li>)}</ul>
  </>;
}''',
'Render a completed badge only when completedCount is positive. Reorder a list containing editable rows. Describe why index keys can associate an input’s state with the wrong row.',
'''function Row({ item }) { return <li>{item.title}</li>; }
function Items({ items, completedCount }) {
  return <>
    {completedCount > 0 && <span>Completed: {completedCount}</span>}
    <ul>{items.map(item => <Row key={item.id} item={item} />)}</ul>
  </>;
}
// Keep each ID fixed across reorder operations.''',
'Use explicit boolean conditions and data-owned keys to preserve item identity.',[
('Which key works for a reorderable list?','A stable item ID','Math.random() during render','Its current index','Stable IDs preserve the association between data and component state.'),
('Why can count && <Badge /> show 0?','The expression evaluates to the number 0','React converts every false value to 0','Badge adds it automatically','Use count > 0 to produce a boolean condition.'),
('Can a child read key from its props?','No; pass a separate ID if needed','Yes, always','Only after an Effect','React reserves key for identity.'),
('After sorting editable rows, notes move to another item. What should you inspect first?','Whether keys are stable IDs','Whether the heading uses h2','Whether the list has a border','Index keys can reuse state for the wrong data item.')])
M('purity','Understand render, commit and purity','/learn/render-and-commit /learn/keeping-components-pure /reference/rules/components-and-hooks-must-be-pure /reference/react/StrictMode',
'Keep rendering repeatable and put side effects at the correct boundary.',
'A state update requests rendering. React calls components to calculate output, then commits required DOM changes. A render may be repeated or abandoned, so render must not mutate external objects, start subscriptions or send purchases. Local mutation of a freshly created value is fine; changing existing props or state is not. Event handlers perform user-driven work; Effects synchronize with external systems after commit. StrictMode adds development checks, including extra render and Effect/ref setup-cleanup cycles. Fix impurity or missing cleanup rather than disabling those checks. Production does not run those development checks.',
'''function Summary({ lessons }) {
  const titles = lessons.map(lesson => lesson.title);
  return <p>{titles.join(', ')}</p>;
}
// Avoid: lessons.push(...) or a network POST in this function.''',
'A render function increments a module-level counter and sends analytics. Explain what repeated rendering does. Move user-triggered logging into a handler; decide whether page-view synchronization needs an Effect.',
'''function StartButton({ lessonId }) {
  function handleStart() {
    console.log('Start requested', lessonId);
  }
  return <button onClick={handleStart}>Start lesson</button>;
}
// Page-view tracking is separate from purchases and should tolerate
// setup/cleanup behavior. Do not treat render counts as user actions.''',
'Render calculates UI; commits and external effects have separate responsibilities.',[
('What must remain safe when React repeats a render?','Calculating JSX from current inputs','Charging a credit card','Mutating a shared lesson array','Pure rendering can be repeated without external changes.'),
('What does StrictMode add?','Development checks for unsafe behavior','Double execution of all production clicks','Automatic server authentication','It exposes impurity and cleanup problems during development.'),
('Is pushing into a brand-new local array during render forbidden?','No, if it is local to that calculation','Yes, all mutation is forbidden','Only if it holds strings','Local construction differs from mutating persistent inputs.'),
('A purchase fires twice while testing rendering. What is the architectural fix?','Trigger the purchase from the intended user action','Remove StrictMode to hide it','Put the purchase in a JSX expression','A non-idempotent transaction does not belong in render.')])
M('events','Handle events and accessible controls','/learn/responding-to-events /reference/react-dom/components/common /reference/react-dom/components/input /reference/react/useId',
'Wire user actions with semantic elements, labels and explicit event behavior.',
'Pass a handler function rather than calling it in JSX. Use semantic button elements for actions; they provide keyboard behavior that a clickable div lacks. preventDefault stops a browser default, while stopPropagation stops event travel; they solve different problems. Label form controls and use useId for reusable accessibility relationships, not for list keys. React event handlers receive an event object, and event.currentTarget refers to the element whose handler is running. Keep behavior named around intent, such as onArchive, instead of forcing parents to know DOM details.',
'''import { useId } from 'react';
function Search({ query, onQueryChange }) {
  const id = useId();
  return <div>
    <label htmlFor={id}>Search lessons</label>
    <input id={id} value={query}
      onChange={event => onQueryChange(event.currentTarget.value)} />
  </div>;
}''',
'Implement a submit handler that prevents navigation and receives the search value. Add a clear button that does not submit the form. Explain why useId is unsuitable for domain item keys.',
'''function SearchForm({ onSearch }) {
  function submit(event) {
    event.preventDefault();
    onSearch(new FormData(event.currentTarget).get('query'));
  }
  return <form onSubmit={submit}>
    <label>Query <input name="query" /></label>
    <button type="submit">Search</button>
    <button type="reset">Clear</button>
  </form>;
}''',
'Use semantic controls, stable labels and handlers that express user intent.',[
('Which JSX passes a handler without executing it during render?','onClick={handleSave}','onClick={handleSave()}','onClick="handleSave"','React invokes the function when the event occurs.'),
('What stops a form’s default navigation?','event.preventDefault()','event.stopPropagation()','useId()','Preventing default and stopping propagation are distinct.'),
('What is useId designed for?','Accessibility ID relationships','Generating stable database keys','Replacing all DOM events','Data IDs should identify items; useId associates related markup.'),
('A clickable div is unreachable by keyboard. What is the direct improvement?','Use a button for the action','Add only a hover color','Hide it from assistive technology','Semantic controls supply expected interaction behavior.')])
M('state','Model local state and snapshots','/learn/state-a-components-memory /learn/state-as-a-snapshot /learn/queueing-a-series-of-state-updates /reference/react/useState',
'Predict state updates using snapshots, batching and updater functions.',
'useState gives the current render’s value and a setter requesting another render. A local variable does not persist or trigger rendering. Each component instance has its own state. Calling a setter does not change the value captured by the current handler, even in delayed callbacks. React batches updates; when several updates depend on earlier queued values, pass a pure updater such as n => n + 1. Setting the same value can skip rendering. Do not call ordinary Hooks inside conditions, loops or handlers. Initialization runs for the initial state; an initializer function can defer expensive work.',
'''import { useState } from 'react';
function PracticeCounter() {
  const [count, setCount] = useState(0);
  function addThree() {
    setCount(n => n + 1);
    setCount(n => n + 1);
    setCount(n => n + 1);
  }
  return <button onClick={addThree}>Completed: {count}</button>;
}''',
'Predict three calls to setCount(count + 1), then compare with three updater calls. Add a reset button. Explain why an alert immediately after a setter still sees the old snapshot.',
'''function Counter() {
  const [count, setCount] = useState(0);
  return <>
    <p>{count}</p>
    <button onClick={() => { setCount(n => n + 3); }}>Add three</button>
    <button onClick={() => setCount(0)}>Reset</button>
  </>;
}
// Repeated setCount(count + 1) requests the same replacement value.
// The handler retains its render's count until another render occurs.''',
'State is a render snapshot; use functional updates when the next value depends on queued state.',[
('Three setCount(count + 1) calls from count 0 usually produce what?','1','3','An automatic exception','Each replacement uses the same captured count.'),
('Which update safely depends on the previous queued value?','setCount(n => n + 1)','count++','setCount = count + 1','The updater receives the pending state.'),
('Does setting state immediately change the current handler’s variable?','No','Yes','Only when the handler is async','A render snapshot remains fixed for that handler.'),
('A delayed callback reads an earlier selection. Which concept explains it?','The callback captured a previous render snapshot','State is global across tabs','React always rereads all variables','Closures retain values from the render that created them.')])
M('immutability','Update objects and arrays safely','/learn/updating-objects-in-state /learn/updating-arrays-in-state /reference/rules/components-and-hooks-must-be-pure',
'Create new state values while preserving unchanged objects.',
'Treat existing state as read-only. Copy every changed level of a nested object; object spread is shallow. Use map to replace an item, filter to remove one and spread to add one. Copy an array before sorting or reversing. A copied array still points to its existing objects, so mutating an item inside it remains a state mutation. Keeping unchanged references makes updates easier to reason about and supports performance optimizations. Libraries can simplify immutable updates, but the underlying ownership rule remains.',
'''function completeLesson(lessons, id) {
  return lessons.map(lesson => lesson.id === id
    ? { ...lesson, completed: true }
    : lesson);
}
const before = [{ id: 'a', title: 'JSX', completed: false }];
const after = completeLesson(before, 'a');
// before[0].completed remains false.''',
'Implement removeLesson and renameLesson. Sort titles without changing the original array. Confirm that an unchanged item retains the same object reference.',
'''export function removeLesson(lessons, id) {
  return lessons.filter(lesson => lesson.id !== id);
}
export function renameLesson(lessons, id, title) {
  return lessons.map(lesson => lesson.id === id ? { ...lesson, title } : lesson);
}
export function sortedLessons(lessons) {
  return [...lessons].sort((a, b) => a.title.localeCompare(b.title));
}''',
'Copy the changed path and reuse untouched values; shallow copies do not make nested mutation safe.',[
('Which removes an item without mutating the array?','filter','splice on the original','pop on the original','filter produces a new array.'),
('Does [...items] clone each object inside it?','No','Yes, deeply','Only if IDs are strings','It copies the array while retaining element references.'),
('How should nested settings.theme be updated?','Copy settings and its changed theme object','Mutate theme then set the same settings','Only copy an unrelated array','Every changed level needs a new value.'),
('Sorting state unexpectedly changes another view’s order. What fixes the shared mutation?','Sort a copied array','Force a rerender after sorting','Change the list key to a random number','sort mutates its array; copy before using it.')])
M('state-design','Choose state structure and ownership','/learn/reacting-to-input-with-state /learn/choosing-the-state-structure /learn/sharing-state-between-components /learn/thinking-in-react',
'Find minimal state and lift it to the closest shared owner.',
'Start from visible UI states: empty, editing, submitting, success and error. Avoid contradictory booleans that allow impossible combinations. Store the minimal inputs needed to derive everything else; filtered lists and totals often belong in render rather than state. Prefer IDs over duplicated selected objects so updates stay consistent. Lift shared state to the nearest common parent and make child inputs controlled through value and callback props. Thinking in React begins with a static component hierarchy, then adds minimal state and its owner.',
'''function filterLessons(lessons, query, onlyCompleted) {
  return lessons.filter(lesson =>
    lesson.title.toLowerCase().includes(query.toLowerCase()) &&
    (!onlyCompleted || lesson.completed));
}
// State: query and onlyCompleted. Visible lessons are derived.''',
'Design a searchable study catalog with a count and list. Identify the state owner. Replace isLoading and isSuccess with a status value. Explain why storing selectedLesson duplicates data.',
'''function Catalog({ lessons }) {
  const [query, setQuery] = useState('');
  const visible = filterLessons(lessons, query, false);
  return <>
    <label>Search <input value={query} onChange={e => setQuery(e.currentTarget.value)} /></label>
    <p>{visible.length} matches</p>
    <ul>{visible.map(item => <li key={item.id}>{item.title}</li>)}</ul>
  </>;
}
// Keep selectedId, and derive lessons.find(item => item.id === selectedId).
// A request status could be 'idle' | 'pending' | 'success' | 'error'.''',
'Keep state minimal, valid and owned where all dependent components can use it.',[
('Where should state shared by two sibling controls live?','Their closest common owner','In duplicated state in each sibling','In a global variable by default','Lifting state gives siblings one source of truth.'),
('Which is usually derived rather than stored separately?','A filtered list from items and query','The user’s query text','The selected item ID','Duplicated derived state can fall out of sync.'),
('What avoids loading=true and success=true together?','A single request status','More unrelated booleans','A random list key','A status model excludes contradictory combinations.'),
('A selected item shows an old title after renaming. Which structure avoids the duplication?','Store selectedId and look up the current item','Copy the whole selected object again','Run an Effect after every render','An ID points to the current canonical data.')])
M('identity','Preserve and reset component state','/learn/preserving-and-resetting-state /learn/tutorial-tic-tac-toe',
'Use tree position, component type and keys to control state identity.',
'React associates state with a position in the rendered tree, taking component type and keys into account. Rendering the same type in the same position can preserve state despite different props. Changing a key can intentionally reset a form for a new entity. Moving component declarations into render can recreate their type and unexpectedly reset state. Keys are meaningful within their parent, not globally. The tic-tac-toe tutorial combines lifted state, immutable history and derived outcomes; time travel comes from storing past snapshots, not mutating a shared board.',
'''function LessonEditor({ lesson }) {
  return <Draft key={lesson.id} initialTitle={lesson.title} />;
}
function Draft({ initialTitle }) {
  const [title, setTitle] = useState(initialTitle);
  return <input aria-label="Draft title" value={title}
    onChange={e => setTitle(e.currentTarget.value)} />;
}''',
'Predict whether changing initialTitle alone resets Draft. Explain why switching lesson.id does. Design a three-entry immutable history and a selected history index.',
'''function addSnapshot(history, selectedIndex, nextBoard) {
  return [...history.slice(0, selectedIndex + 1), nextBoard];
}
// Changing props does not re-run useState initialization.
// A new key creates a new Draft identity and resets local state.
// Keep Draft at module scope. Derive the current board from history[index].''',
'Preserve state through stable identity; reset it deliberately with a new key.',[
('What can intentionally reset a form for another entity?','A changed entity key','A new label string alone','Mutating props','A new key gives the form a new identity.'),
('Does useState(initialTitle) reinitialize whenever initialTitle changes?','No','Yes','Only in development','Initialization applies to a component identity’s initial state.'),
('What supports time travel without overwriting past boards?','Immutable history snapshots','One shared mutated array','Random keys on every square','Each snapshot preserves a past value.'),
('A child loses typed text whenever its parent renders. What declaration should you inspect?','A child component defined inside the parent function','A label htmlFor','A stable data key','Recreating the component type can reset its state.')])
M('reducers','Centralize transitions with reducers','/learn/extracting-state-logic-into-a-reducer /reference/react/useReducer',
'Write pure state transitions using semantic actions.',
'A reducer calculates next state from previous state and an action. Events dispatch facts such as lessonAdded rather than directly duplicating update logic. Reducers run during render and must be pure: no fetch, storage writes, ID generation or state mutation. Create IDs in the event layer and include them in actions. Return new state values for changed paths. Unknown actions should have an intentional policy, often throwing during development. A reducer is useful when many events affect a related model; it does not automatically make the state global.',
'''export function reducer(state, action) {
  switch (action.type) {
    case 'added': return [...state, action.lesson];
    case 'removed': return state.filter(item => item.id !== action.id);
    default: throw new Error('Unknown action: ' + action.type);
  }
}''',
'Add a completed action to the reducer. Dispatch an added action from a button while generating its ID outside the reducer. Test that the original input array is unchanged.',
'''export function completeReducer(state, action) {
  switch (action.type) {
    case 'completed':
      return state.map(item => item.id === action.id ? { ...item, completed: true } : item);
    default: return reducer(state, action);
  }
}
// In an event handler:
// dispatch({ type: 'added', lesson: { id: crypto.randomUUID(), title, completed: false } });''',
'Reducers describe predictable transitions; events handle external work and generate action data.',[
('Which belongs inside a reducer?','Calculating a new array from state and action','Saving to a database','Generating a random ID on every call','Reducers must be pure and repeatable.'),
('What does dispatch carry?','An action describing the requested transition','A direct mutation of all components','A DOM node by necessity','Actions encode intent or facts for the reducer.'),
('Does useReducer automatically share state globally?','No','Yes','Only with async actions','The reducer state belongs to the component using it.'),
('Two reducer calls for the same inputs create different IDs. What should move?','ID generation into the event layer','The switch into an Effect','All state into refs','Random values inside the reducer break deterministic transitions.')])
M('context','Scale state with context and reducers','/learn/passing-data-deeply-with-context /learn/scaling-up-with-reducer-and-context /reference/react/createContext /reference/react/useContext',
'Share a model through a scoped provider without hiding ownership.',
'Context lets descendants read a value from the nearest matching provider, reducing prop threading. It is a transport mechanism, not storage by itself: a stateful provider still owns updates. Context defaults are fallbacks when no provider exists, not automatically updating state. In React 19 a context can be rendered as its own provider with value. Split state and dispatch contexts when useful; consumers of a changing value rerender even if memoized. Keep context definitions at module scope. Choose the smallest sensible provider scope; not every local input belongs in shared context.',
'''import { createContext, useContext, useReducer } from 'react';
const PlanContext = createContext(null);
function PlanProvider({ children }) {
  const [lessons, dispatch] = useReducer(reducer, []);
  return <PlanContext value={{ lessons, dispatch }}>{children}</PlanContext>;
}
function usePlan() {
  const value = useContext(PlanContext);
  if (!value) throw new Error('PlanProvider is required');
  return value;
}''',
'Place a provider around a catalog and summary, leaving an unrelated footer outside it. Explain which provider wins when nested. Separate lessons and dispatch contexts in a larger application.',
'''const LessonsContext = createContext(null);
const DispatchContext = createContext(null);
function Provider({ children }) {
  const [lessons, dispatch] = useReducer(reducer, []);
  return <LessonsContext value={lessons}>
    <DispatchContext value={dispatch}>{children}</DispatchContext>
  </LessonsContext>;
}
// A consumer reads the closest provider above it, not a provider it returns.''',
'Context transports a scoped value; keep its state owner and update contract explicit.',[
('Which context provider does a consumer read?','The nearest matching provider above it','The last provider in the source file','Every provider merged together','Provider lookup follows the render tree.'),
('What does a default context value represent?','A fallback when no provider is found','A global mutable state store','An automatic subscription to localStorage','The default is static fallback data.'),
('Can memo prevent context-driven updates when the consumed value changes?','No','Always','Only if the value is an object','Context consumers still receive changed context values.'),
('A search input affects one small panel. Is shared context automatically necessary?','No, local state may be clearer','Yes, all inputs need a provider','Only if it has a label','Choose scope based on ownership and actual consumers.')])
M('refs','Use refs for values and DOM access','/learn/referencing-values-with-refs /learn/manipulating-the-dom-with-refs /reference/react/useRef /reference/react/useImperativeHandle /reference/react/Fragment /reference/react-dom/components/common',
'Use refs without replacing reactive state or leaking imperative handles.',
'A ref preserves a mutable value across renders without triggering rendering. Store timer IDs or DOM handles there; use state for values displayed in UI. Do not read or write refs during render except permitted predictable initialization. Attach a ref to access a committed DOM node, such as to focus an input after an action. React 19 accepts ref as a prop for function components; useImperativeHandle can expose a narrow handle instead of the whole DOM node. Callback refs can return cleanup functions. React 19.3 Fragment refs expose grouped DOM operations without a wrapper; this is an advanced option, not a reason to manipulate React-owned markup.',
'''import { useRef } from 'react';
function FocusSearch() {
  const inputRef = useRef(null);
  return <>
    <label>Search <input ref={inputRef} /></label>
    <button onClick={() => inputRef.current?.focus()}>Focus search</button>
  </>;
}''',
'Decide whether a visible count and a timeout ID belong in state or refs. Add focus to a search field after a button click. Design a handle exposing only focus, rather than every node method.',
'''function SearchField({ ref }) {
  const input = useRef(null);
  useImperativeHandle(ref, () => ({ focus() { input.current?.focus(); } }), []);
  return <input ref={input} aria-label="Search lessons" />;
}
// Import useImperativeHandle from react.
// Visible count: state. Timeout ID: ref.
// Avoid changing children directly in DOM that React owns.''',
'Refs hold imperative handles and non-rendering values; state drives visible output.',[
('Does changing ref.current request a render?','No','Yes','Only if it holds a number','Refs are mutable storage outside the state update mechanism.'),
('Which value belongs in state rather than only in a ref?','A count displayed in JSX','A timeout handle','An input DOM handle','Visible values must participate in rendering.'),
('What can useImperativeHandle provide?','A deliberately limited imperative interface','Automatic shared context','A new component type each render','It restricts what a parent can do through a ref.'),
('A visible timer count changes internally but the page stays unchanged. What is likely wrong?','Only a ref was updated instead of state','The ref is too deeply nested','The button has a type','Ref writes do not notify React to render.')])
M('effects','Synchronize with external systems','/learn/synchronizing-with-effects /learn/lifecycle-of-reactive-effects /reference/react/useEffect /reference/react/StrictMode',
'Implement symmetric Effect setup and cleanup with correct dependencies.',
'An Effect synchronizes committed UI with an external system: a subscription, connection or browser API. Its lifecycle is start synchronization, then stop it when dependencies change or the component unmounts. React compares dependencies with Object.is. Every reactive value read by the Effect belongs in its dependencies unless the code is restructured to remove that reactivity. Cleanup stops the previous synchronization before the next setup. Development StrictMode exercises setup-cleanup-setup; correct cleanup prevents duplicate active subscriptions. An Effect cannot itself be async because its return must be cleanup, not a Promise. Effects run on the client, not during server rendering.',
'''import { useEffect, useState } from 'react';
function Clock() {
  const [seconds, setSeconds] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setSeconds(n => n + 1), 1000);
    return () => clearInterval(id);
  }, []);
  return <p>{seconds} seconds</p>;
}''',
'Explain why the updater permits an empty dependency list here. Remove cleanup and predict the StrictMode symptom. Sketch a subscription depending on lessonId and clean it up when the ID changes.',
'''function useLessonSubscription(lessonId, subscribe) {
  useEffect(() => {
    const unsubscribe = subscribe(lessonId);
    return () => unsubscribe();
  }, [lessonId, subscribe]);
}
// Both reactive values are dependencies. A stable subscribe supplied
// by the host avoids unnecessary reconnects; do not suppress the linter.''',
'Each Effect needs an external purpose, truthful dependencies and matching cleanup.',[
('When should an old subscription be cleaned up?','Before replacement setup and on unmount','Only when the browser closes','Never if state updates','Cleanup reverses the previous synchronization.'),
('Why is useEffect(async () => ...) incorrect?','The callback returns a Promise instead of cleanup','Effects cannot perform asynchronous work at all','Async always runs during render','Start async work inside a synchronous Effect callback.'),
('What compares Effect dependency values?','Object.is','A deep JSON comparison','Array sorting','Dependencies are compared by identity/value with Object.is.'),
('StrictMode reveals two running intervals. What should you inspect?','Whether cleanup clears the interval','Whether StrictMode needs production deployment','Whether seconds uses a string','Development checks expose incomplete cleanup.')])
M('effect-design','Remove unnecessary Effects and dependency bugs','/learn/you-might-not-need-an-effect /learn/removing-effect-dependencies /learn/separating-events-from-effects /reference/react/useEffectEvent',
'Distinguish derivation, user events and non-reactive Effect Events.',
'Derive filtered data and combined names while rendering instead of copying them through Effects. Put user-triggered mutations in their handlers. To change dependencies, change the code: move constants outside the component, create objects inside an Effect, split independent synchronization or use a functional updater. React 19.2 introduced useEffectEvent for non-reactive logic called from Effects. It sees latest committed values without resubscribing, but it is not a general dependency escape hatch. Call it only from Effects or other Effect Events, do not pass it elsewhere, and do not include it in dependency arrays. Its function identity is intentionally not stable.',
'''import { useEffect, useEffectEvent } from 'react';
function Connection({ roomId, theme, connect, notify }) {
  const onConnected = useEffectEvent(() => notify(theme));
  useEffect(() => {
    const connection = connect(roomId);
    connection.onConnected(onConnected);
    connection.start();
    return () => connection.stop();
  }, [roomId, connect]);
  return <p>Room: {roomId}</p>;
}''',
'Remove an Effect that sets fullName from firstName and lastName. For a connection, decide whether a room change should reconnect and whether a theme change should. Explain why an Effect Event cannot replace a click handler.',
'''function Name({ firstName, lastName }) {
  const fullName = firstName + ' ' + lastName;
  return <p>{fullName}</p>;
}
// roomId drives synchronization. Theme affects the notification only.
// Effect Events stay local to the Effect logic; ordinary user actions
// belong in ordinary event handlers. Use the current Hooks linter.''',
'Before adding an Effect, ask whether the work is derivation, an event or true synchronization.',[
('Where should fullName from two current props be calculated?','During render','In an Effect plus extra state','In a module global','Derived values need not create another state synchronization cycle.'),
('How should unnecessary dependencies be removed?','Restructure the code so it no longer reads them reactively','Delete dependency entries without changing code','Disable every Hooks lint','Dependencies describe the code rather than a preferred schedule.'),
('Can useEffectEvent be passed to a child as its click handler?','No','Yes, that is its purpose','Only if memoized','Effect Events belong to Effect logic, not arbitrary handlers.'),
('Changing a theme should update notifications but not reconnect a room. Which tool can separate those concerns?','An Effect Event for the non-reactive notification','An empty dependency list hiding roomId','A global mutable theme','Effect Events read latest committed values without making that notification reactive.')])
M('async','Handle asynchronous races and custom Hooks','/learn/reusing-logic-with-custom-hooks /learn/synchronizing-with-effects /reference/react/useDebugValue',
'Extract reusable synchronization and avoid stale request results.',
'Custom Hooks share stateful logic, not one shared state instance. Their names start with use, and they follow Hook ordering rules. Define a clear input/output contract rather than an artificial useMount lifecycle wrapper. For client requests in an Effect, represent loading, data and errors and ignore or abort outdated work; otherwise a slower older request can replace a newer selection. An ignore flag guards a result but does not cancel network work. AbortController can cancel a fetch, with abort treated separately from genuine failures. Framework loaders or documented Suspense integrations can solve caching and waterfall problems more comprehensively. useDebugValue labels custom Hooks for developer tools.',
'''import { useEffect, useState } from 'react';
export function useLesson(url) {
  const [result, setResult] = useState({ status: 'pending' });
  useEffect(() => {
    const controller = new AbortController();
    setResult({ status: 'pending' });
    async function load() {
      try {
        const response = await fetch(url, { signal: controller.signal });
        if (!response.ok) throw new Error('Request failed');
        const data = await response.json();
        if (!controller.signal.aborted) setResult({ status: 'success', data });
      } catch (error) {
        if (!controller.signal.aborted) setResult({ status: 'error', error });
      }
    }
    load();
    return () => controller.abort();
  }, [url]);
  return result;
}''',
'Change the URL rapidly and reason about old responses. Add UI for pending, error and success. Explain why two components calling useLesson each own their result and do not automatically share a cache.',
'''function LessonDetails({ url }) {
  const result = useLesson(url);
  if (result.status === 'pending') return <p role="status">Loading lesson…</p>;
  if (result.status === 'error') return <p role="alert">Could not load lesson.</p>;
  return <h2>{result.data.title}</h2>;
}
// Abort ends obsolete work; the guard prevents obsolete state updates.
// This teaching Hook is not a complete cache or framework data layer.''',
'Custom Hooks encapsulate behavior; cancellation, status and data ownership stay explicit.',[
('Do two calls to a custom Hook automatically share one state value?','No','Yes','Only if the name begins with use','Each call follows the owning component’s state identity.'),
('What prevents an old request from replacing a newer result?','Cancellation or an obsolete-result guard','A random component key on every render','Removing the URL dependency','Request lifetimes must agree with the current selection.'),
('What does an ignore flag alone do?','Reject obsolete results without necessarily cancelling work','Always cancel the network request','Cache every response','Ignoring completion is different from cancelling the underlying request.'),
('A fetched response is 404 but the catch branch does not run. What is missing?','A response.ok check before accepting the body','A longer dependency array','A memo wrapper','fetch can resolve normally for HTTP error statuses.')])
M('forms','Build controlled and native forms','/reference/react-dom/components/input /reference/react-dom/components/select /reference/react-dom/components/textarea /reference/react-dom/components/option /reference/react-dom/components/form /learn/reacting-to-input-with-state',
'Choose controlled inputs or native form data and keep input contracts consistent.',
'A controlled text input receives value plus an onChange update; a checkbox receives checked. Keep controlled values defined throughout the component lifetime rather than switching between undefined and a string. defaultValue supplies an uncontrolled initial value. FormData reads named successful controls, and unchecked checkboxes may be absent. Controlled select uses its value, not selected on each option. Labels, keyboard behavior and visible error feedback belong in the form design. In React 19 a form action can be a function, running as an Action; successful function actions reset uncontrolled fields. A traditional onSubmit with preventDefault remains valid.',
'''function LessonForm({ onSave }) {
  function submit(event) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    onSave({ title: String(data.get('title') || '').trim(),
      completed: data.get('completed') === 'on' });
  }
  return <form onSubmit={submit}>
    <label>Title <input name="title" required /></label>
    <label><input type="checkbox" name="completed" /> Completed</label>
    <button type="submit">Save lesson</button>
  </form>;
}''',
'Build a controlled title input initialized to an empty string. Build an uncontrolled equivalent using FormData. Validate whitespace-only titles and display a recovery message.',
'''function ControlledTitle() {
  const [title, setTitle] = useState('');
  const invalid = title.trim().length === 0;
  return <>
    <label>Title <input value={title} onChange={e => setTitle(e.currentTarget.value)} /></label>
    {invalid && <p>Enter a title before saving.</p>}
    <button disabled={invalid}>Save</button>
  </>;
}
// A native required input alone does not reject every whitespace-only value.''',
'Choose one input ownership model and validate the actual data, not just the markup.',[
('Which prop controls a checkbox’s state?','checked','value alone','selected','Checkbox selection is controlled with checked.'),
('What reads a native form control’s submitted value?','FormData and its name','The component function name','The key prop','Named controls contribute values to FormData.'),
('What can cause a controlled/uncontrolled warning?','Changing value from undefined to a string','Using a label','Setting type="submit"','Keep the input’s ownership model consistent.'),
('A controlled select ignores selected on its option. Where should selection be set?','The select value prop','The parent’s className','A random key on the option','React controls select through its value.')])
M('actions','Manage form Actions and pending status','/reference/react/useActionState /reference/react-dom/hooks/useFormStatus /reference/react-dom/components/form /reference/react/useTransition',
'Handle Action state, validation outcomes and parent form pending status.',
'useActionState combines an Action’s result state with dispatchAction and isPending. Its action function receives previous state before the submitted payload, so existing FormData handlers need the extra parameter. Function form actions supply the Action context automatically; manually dispatching async Actions needs an appropriate transition context. Expected validation failures can return structured state; thrown failures go to an Error Boundary and cancel queued actions. useFormStatus is imported from react-dom and reads the parent form’s submission status; placing it in the component that creates the form does not make it read that form. Server execution requires server/framework support, not merely a function action.',
'''import { useActionState } from 'react';
import { useFormStatus } from 'react-dom';
function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? 'Saving…' : 'Save'}</button>;
}
async function saveTitle(previous, data) {
  const title = String(data.get('title') || '').trim();
  return title ? { message: 'Saved: ' + title } : { message: 'Title required' };
}
function Editor() {
  const [state, action] = useActionState(saveTitle, { message: '' });
  return <form action={action}>
    <label>Title <input name="title" /></label>
    <SubmitButton /><p role="status">{state.message}</p>
  </form>;
}''',
'Rewrite a one-parameter FormData action for useActionState. Put the pending button inside the form. Decide whether invalid title is an expected state or an exception. The example validates locally and does not claim persistence.',
'Use (previousState, formData), with return values forming the next Action state. Keep SubmitButton as a descendant of the form. Return a validation message for expected input problems and reserve throws for exceptional failures. Add real persistence through a deliberate backend or framework integration; the local example only demonstrates Action state.',
'Action state describes outcomes; pending status depends on the form boundary and dispatch context.',[
('What is the first argument of a useActionState reducer action?','Previous state','FormData always','A DOM ref','useActionState adds previous state before the payload.'),
('Where must a component using useFormStatus be located?','Inside the form whose status it reads','Only alongside the form','Outside all forms','The Hook reads the parent form submission.'),
('Does a client form action automatically become server code?','No','Yes','Only if it is async','Server execution needs the supported server integration.'),
('A validation failure is expected and recoverable. What is a useful Action result?','Structured validation state displayed to the user','An unrelated render-time mutation','A silent console message only','Returning state supports visible, recoverable feedback.')])
M('optimistic','Show optimistic results with recovery','/reference/react/useOptimistic /reference/react/useActionState /reference/react/useTransition',
'Separate temporary optimistic feedback from confirmed canonical data.',
'useOptimistic lets UI temporarily project an update before an Action finishes. Its base value is confirmed data; a pure reducer combines that base with optimistic updates. Dispatch optimistic changes inside an Action or transition, and update canonical state when work succeeds. Pending UI must not masquerade as confirmed persistence. When an Action ends, optimistic state converges to the current base; failures need explicit feedback and recovery. Handle overlapping work and item IDs deliberately so a slow older result does not overwrite newer confirmed data. Optimism does not replace validation, authorization or durable storage.',
'''import { useOptimistic, useState, startTransition } from 'react';
function Favorite({ save }) {
  const [confirmed, setConfirmed] = useState(false);
  const [optimistic, setOptimistic] = useOptimistic(confirmed);
  const [error, setError] = useState('');
  function choose() {
    startTransition(async () => {
      setError('');
      setOptimistic(true);
      try {
        await save(true);
        startTransition(() => setConfirmed(true));
      } catch { setError('Could not save. Try again.'); }
    });
  }
  return <><button onClick={choose}>{optimistic ? 'Favorited' : 'Favorite'}</button>
    <p role="status">{error}</p></>;
}''',
'Use a fake save that rejects, then one that resolves. Predict the temporary and confirmed UI. Describe how you would distinguish a pending list item from a confirmed item and avoid duplicate temporary IDs.',
'On failure, confirmed remains false and the optimistic projection ends with the Action; display the error so the user can retry. On success, update confirmed state. For a list, tag temporary items as pending, generate IDs outside the reducer and reconcile the server’s canonical item. Test overlapping requests instead of assuming response order.',
'Optimistic UI is a temporary projection with confirmation and a failure path.',[
('What should optimistic state be based on?','Confirmed canonical state','A permanently mutated server response','A render-time network request','The projection converges to the current confirmed value.'),
('Where should optimistic updates be dispatched?','An Action or transition','An arbitrary render call','A module initializer on every import','Optimistic updates need an Action lifetime.'),
('What must a failed optimistic save provide?','Visible recovery and unchanged or restored confirmed data','A false success message','Permanent pending data','The UI must distinguish feedback from persistence.'),
('Two saves overlap and the older response arrives last. What needs explicit design?','Canonical reconciliation and request ordering','More random list keys','An omitted error state','Optimism does not remove asynchronous ordering problems.')])
M('transitions','Keep urgent interactions responsive','/reference/react/useTransition /reference/react/startTransition /reference/react/useDeferredValue',
'Separate urgent input updates from non-urgent rendering work.',
'useTransition provides isPending and startTransition to mark updates that can yield to urgent work. A controlled input’s own value update must remain urgent. useDeferredValue can let an expensive view lag behind a current value while keeping typing responsive; it does not automatically debounce network requests. startTransition marks state updates, not a generic background thread for arbitrary expensive JavaScript. Updates after an await currently need another startTransition to be marked as transitions. Consider request ordering for async Actions. Show pending or stale indicators where the delay matters; measure before introducing scheduling complexity.',
'''import { useDeferredValue, useState } from 'react';
function SearchResults({ lessons }) {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  const stale = query !== deferredQuery;
  return <>
    <label>Search <input value={query} onChange={e => setQuery(e.currentTarget.value)} /></label>
    <div style={{ opacity: stale ? 0.6 : 1 }}>
      <ul>{lessons.filter(x => x.title.includes(deferredQuery))
        .map(x => <li key={x.id}>{x.title}</li>)}</ul>
    </div>
  </>;
}''',
'Identify the urgent update in the example. Explain why deferring the query does not cancel existing fetches. Move only an expensive results update into a transition, leaving the input update immediate.',
'''function handleInput(nextQuery) {
  setQuery(nextQuery); // urgent controlled input
  startTransition(() => setResultsQuery(nextQuery));
}
// useTransition and useState are imported from react in a component.
// Scheduling lets React prioritize rendering; it does not move a costly
// synchronous function into a worker or implement request cancellation.''',
'Transitions prioritize rendering; cancellation, debouncing and CPU offloading are separate concerns.',[
('Which update should stay urgent?','The controlled input’s value','Every background result render','A hidden analytics label','An input must immediately reflect typing.'),
('Does useDeferredValue automatically reduce network requests?','No','Yes','Only for strings','Rendering deferral is not network debouncing.'),
('What does startTransition mark?','Eligible state updates as non-urgent','All JavaScript as a worker task','An automatic cache','It changes scheduling priority for updates.'),
('After an await, how can you mark a following update as a transition?','Wrap that update in another startTransition','Assume every later update inherits it','Use a random key','The documented async boundary currently requires another transition wrapper.')])
M('suspense','Load code and resources with Suspense','/reference/react/Suspense /reference/react/lazy /reference/react/use /reference/react/Component',
'Choose loading and error boundaries for supported suspended work.',
'Suspense shows a fallback when descendants suspend through a supported source, such as lazy code or a cached Promise read with use. It does not detect an ordinary fetch started in an Effect. lazy loads a component module; declare it outside components and ensure the loader resolves a default export. use can read a Promise or context during render and may be called conditionally, unlike ordinary Hooks; it still must be in a component or Hook and must not be wrapped in try/catch. Pending Promises suspend; rejected ones are handled by an Error Boundary. Do not create a fresh uncached Promise on every Client Component render. Let a framework or compatible data integration own caching.',
'''import { lazy, Suspense } from 'react';
const LessonDetails = lazy(() => import('./LessonDetails.jsx'));
function DetailsArea() {
  return <Suspense fallback={<p role="status">Loading details…</p>}>
    <LessonDetails />
  </Suspense>;
}
// LessonDetails.jsx must provide the expected default component export.''',
'Add two lazy regions with separate fallbacks and compare with one shared boundary. Describe what handles a rejected import. Explain why wrapping an Effect-fetching component in Suspense alone does not supply loading UI.',
'''function TwoRegions() {
  return <>
    <Suspense fallback={<p>Loading summary…</p>}><Summary /></Suspense>
    <Suspense fallback={<p>Loading details…</p>}><LessonDetails /></Suspense>
  </>;
}
// Summary and LessonDetails are lazy module-scope declarations.
// Use an Error Boundary for failures. Boundary placement controls reveal
// grouping; choose it to match the user's reading flow.''',
'Suspense coordinates supported loading; an Error Boundary handles rendering failures.',[
('Does Suspense automatically detect a fetch started in useEffect?','No','Yes','Only with an empty dependency list','Suspense requires a supported suspending source.'),
('Where should lazy component declarations live?','Outside component render functions','Inside every click handler','Inside another component on each render','A stable declaration preserves identity and loader behavior.'),
('What handles a rejected Promise read with use?','An Error Boundary','The Suspense fallback forever','A try/catch around use','Pending resources suspend; rejection is an error.'),
('Two independent panels should reveal separately. What design supports that?','Separate Suspense boundaries with appropriate fallbacks','One mandatory whole-page spinner','No boundaries anywhere','Boundary grouping should follow the intended reveal experience.')])
M('performance','Measure before memoizing','/reference/react/memo /reference/react/useMemo /reference/react/useCallback /reference/react/Profiler /reference/dev-tools/react-performance-tracks /learn/react-developer-tools',
'Identify expensive work and use memoization as an optimization, not correctness.',
'Use profiling to find costly renders in realistic interactions. memo can skip a component render when props compare equal, but its own state and consumed context still update it. useMemo caches a calculation and useCallback caches a function between matching dependencies. Neither makes impure logic safe nor guarantees permanent storage. A fresh object or function prop can defeat memoization. Custom comparisons need to compare behavior-affecting props, including callbacks, or they can preserve stale closures. React Compiler can automate eligible optimization; understand manual memoization when maintaining code, then measure rather than adding it everywhere.',
'''import { memo, useMemo } from 'react';
const Summary = memo(function Summary({ count }) {
  return <p>{count} matching lessons</p>;
});
function Results({ lessons, query }) {
  const visible = useMemo(() => lessons.filter(x => x.title.includes(query)), [lessons, query]);
  return <Summary count={visible.length} />;
}''',
'Profile a filter before and after useMemo with a large data set. Explain why small data may not benefit. Add a new object prop to a memoized child and identify why skipping stops. Do not use memoization to hold business state.',
'Keep the original straightforward calculation unless profiling shows a useful gain. A newly created object is unequal by reference to its previous counterpart; pass stable primitive props or memoize only where warranted. Store business values in state or another appropriate owner. Test behavior without relying on caches; their purpose is speed, not correctness.',
'Profile the interaction and optimize the measured bottleneck without changing semantics.',[
('Can memo skip updates caused by the component’s own state?','No','Always','Only with shallow props','memo is primarily a props-based optimization.'),
('What does useCallback cache?','A function identity','Its execution result','A durable database record','useMemo caches a calculated result; useCallback caches a function.'),
('What should determine whether optimization is worthwhile?','Measured interaction cost','The number of Hooks alone','A blanket rule to memoize everything','Optimization has overhead and should address a real bottleneck.'),
('A custom comparator ignores a callback prop and a child uses old values. What is likely wrong?','The comparator preserved a stale closure','The browser forgot event handlers','State must be replaced by refs','Behavior-affecting function props cannot be ignored safely.')])
M('compiler','Adopt the React Compiler and Rules of React','/learn/react-compiler /learn/react-compiler/introduction /learn/react-compiler/installation /learn/react-compiler/incremental-adoption /learn/react-compiler/debugging /reference/react-compiler/configuration /reference/react-compiler/directives /reference/eslint-plugin-react-hooks /reference/rules/rules-of-hooks',
'Plan compiler adoption with linting, scope and measured verification.',
'React Compiler is a build-time optimization tool that understands React’s programming model; it does not compile away the need for valid state ownership or pure rendering. Use the documented integration for the host build tool. Run the recommended Hooks lint configuration to reveal Rules of React and compiler diagnostics. Ordinary Hooks must stay at the top level of components or custom Hooks; components and Hooks must be pure. Adopt incrementally, investigate skipped components and verify the production build. Compiler settings include target, compilationMode, gating, logger and panicThreshold. The use memo and use no memo directives control specific compilation cases; do not scatter them without understanding their scope.',
'''// An adoption plan, not an application runtime API:
// 1. Identify the host's documented compiler integration.
// 2. Enable the recommended eslint-plugin-react-hooks rules.
// 3. Fix mutation, conditional Hooks and unstable component declarations.
// 4. Compile a representative slice; inspect diagnostics.
// 5. Test behavior and profile the production result.''',
'Write a compiler rollout plan for an existing app. Include target/version compatibility, a small pilot, lint fixes, a behavior check and a rollback path. Classify an impure render as a correctness problem rather than an optimization opportunity.',
'Pilot on a representative feature, use the host’s installation instructions and inspect diagnostics instead of assuming every component compiled. Fix semantic violations first. Keep existing memoization until the documented migration strategy and profiling justify changes. Review directive and configuration reference pages for the actual integration. Roll back the build configuration if the pilot exposes unsupported behavior.',
'The compiler optimizes valid React code; lint, adopt incrementally and test the built application.',[
('When does React Compiler operate?','At build time','Only after every user click','Inside the browser localStorage API','It is a build-time optimization tool.'),
('Does it make an impure render correct?','No','Yes','Only with use memo','Correct React semantics remain required.'),
('What is a safe rollout approach?','A documented integration with a measured pilot','Delete all tests and enable it everywhere','Ignore skipped component diagnostics','Incremental adoption allows validation and diagnosis.'),
('A compiler diagnostic flags mutation of props. What should you fix first?','The ownership and purity violation','Only the chart’s colors','The directive string everywhere','The diagnostic identifies a programming-model problem, not merely lost speed.')])
M('external-stores','Subscribe to external stores','/reference/react/useSyncExternalStore /reference/react/useDebugValue /reference/react/useInsertionEffect /reference/react/useLayoutEffect',
'Choose the right integration Hook and keep store snapshots stable.',
'useSyncExternalStore connects React to mutable data owned outside React. subscribe registers a listener and returns cleanup; getSnapshot supplies the current immutable snapshot. If the data has not changed, the snapshot must compare equal, or React can loop on freshly allocated objects. For server rendering, getServerSnapshot supplies an initial value compatible with hydration. Prefer ordinary state for data React owns. useLayoutEffect runs before paint for necessary DOM measurements and can block painting; do not substitute it for every Effect. useInsertionEffect primarily serves CSS-in-JS library insertion, not normal application data work. useDebugValue gives developer-tool labels to reusable Hooks.',
'''import { useSyncExternalStore } from 'react';
const subscribe = listener => {
  window.addEventListener('online', listener);
  window.addEventListener('offline', listener);
  return () => {
    window.removeEventListener('online', listener);
    window.removeEventListener('offline', listener);
  };
};
function OnlineStatus() {
  const online = useSyncExternalStore(subscribe, () => navigator.onLine, () => true);
  return <p>{online ? 'Online' : 'Offline'}</p>;
}''',
'Explain why the boolean snapshot stays equal when nothing changes. Replace it conceptually with a cached object snapshot. Decide whether an external editor store, a React-owned text field and tooltip measurement use the same Hook.',
'An external editor store may use useSyncExternalStore with stable snapshots and unsubscribe. The text field normally uses useState. A tooltip needing measurement before paint may use useLayoutEffect, while considering its server-rendering limitations. The server snapshot in this example deliberately yields true on both the server and initial hydration; the client then checks actual connectivity. navigator.onLine is a browser hint, not proof a particular server is reachable.',
'Use external-store contracts for external data; reserve layout/insertion timing for their specialized purposes.',[
('What must subscribe return?','An unsubscribe function','A JSX element','A Promise for all components','Cleanup removes the registered listener.'),
('What can cause a snapshot loop?','Returning a fresh object when data has not changed','Returning the same boolean','Using a semantic paragraph','Unchanged store data needs an equal snapshot.'),
('What is useInsertionEffect primarily intended for?','CSS-in-JS library style insertion','Fetching every page’s data','Replacing useState','It serves a specialized integration timing need.'),
('You own a simple input value entirely in React. Which choice is usually clearer?','useState','A new external store by default','useInsertionEffect','External-store integration is not needed merely because data changes.')])
M('activity-motion','Preserve hidden UI and coordinate motion','/reference/react/Activity /reference/react/ViewTransition /reference/react/addTransitionType /reference/react/Fragment /blog/2026/09/09/react-19-3',
'Distinguish hidden state preservation from unmounting and schedule accessible transitions.',
'Activity can hide UI while preserving its internal state. Hidden boundaries clean up Effects and render incoming props at lower priority; becoming visible restores state and recreates Effects. This differs from removing a subtree, which discards its identity. ViewTransition is stable in the pinned React 19.3 snapshot and coordinates supported DOM transitions with React’s transition scheduling. Ordinary urgent state updates do not trigger these animations. addTransitionType labels a transition’s cause for styling. React coordinates the browser transition API; do not independently start competing browser transitions. Respect prefers-reduced-motion: React does not automatically disable these animations. Fragment refs are also stable in 19.3 for group DOM interactions.',
'''import { Activity, ViewTransition, useState, startTransition } from 'react';
function Tabs() {
  const [visible, setVisible] = useState(true);
  return <>
    <button onClick={() => startTransition(() => setVisible(v => !v))}>Toggle notes</button>
    <ViewTransition><Activity mode={visible ? 'visible' : 'hidden'}>
      <textarea aria-label="Study notes" />
    </Activity></ViewTransition>
  </>;
}''',
'Type notes, hide and reveal them. Compare with conditional unmounting. Explain what happens to a subscription Effect while hidden. Add a reduced-motion rule to the host stylesheet.',
'''/* Host stylesheet: suppress view-transition animation for reduced motion. */
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) { animation: none !important; }
}
// Activity preserves notes but stops hidden Effects. Conditional removal
// creates a new textarea next time and does not preserve its local DOM value.''',
'Choose preservation deliberately and make motion respect user preferences and supported runtimes.',[
('What happens to Effects in a hidden Activity?','They are cleaned up and recreated when visible','They always keep every subscription active','They permanently delete state','Hidden Activity preserves state while deactivating Effects.'),
('What normally activates ViewTransition animation?','An eligible transition-driven update','Every urgent state update','Every key press automatically','React schedules supported transition changes for animation.'),
('Does React automatically disable ViewTransition animations for reduced motion?','No','Yes','Only if there are two children','The application must respect that preference.'),
('A draft should survive hiding a panel while subscriptions stop. Which boundary fits?','Activity','Conditional removal only','A random key per hide','Activity separates hidden preservation from active Effects.')])
M('boundaries','Handle errors and portaled UI','/reference/react/Component /reference/react-dom/createPortal /reference/react/captureOwnerStack',
'Place failure boundaries and preserve accessible behavior across portals.',
'An Error Boundary catches descendant rendering errors and provides fallback UI. The documented class form uses getDerivedStateFromError and may log through componentDidCatch. It does not automatically catch event-handler failures, ordinary asynchronous callbacks or server rendering failures; handle those at their own boundary. Choose failure scopes so one broken panel need not erase the whole app, and design a recovery path. createPortal moves a subtree’s DOM placement without changing its React parent relationships: context still follows React ancestry, and events propagate through the React tree. A portal alone does not implement an accessible modal; focus, dismissal, semantics and background interaction require design. captureOwnerStack is a development diagnostic, not a production guarantee.',
'''import { Component } from 'react';
class PanelBoundary extends Component {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  render() {
    return this.state.failed ? <p role="alert">This panel could not load.</p> : this.props.children;
  }
}''',
'Wrap a fragile preview while leaving navigation available. Explain why a rejected save in a click handler still needs explicit error handling. Sketch the requirements for a portaled dialog beyond its visual placement.',
'''function Page() {
  return <>
    <nav aria-label="Study navigation">Study studio</nav>
    <PanelBoundary><Preview /></PanelBoundary>
  </>;
}
// Preview is the host's potentially failing component.
// A dialog also needs a name, managed focus, dismissal and appropriate
// background behavior. Portal placement alone does not supply these.''',
'Scope failures and recovery intentionally; DOM placement does not change React ownership.',[
('Which failure does an Error Boundary normally catch?','A descendant’s rendering error','Every rejected event-handler request','Every server error','Event and async failures need their own handling.'),
('Does a portal change which context a child reads?','No','Yes, it reads DOM-parent context','It disables all context','Context follows the React tree.'),
('Does createPortal alone implement a complete accessible modal?','No','Yes','Only if its container is body','Modal semantics and interaction still need implementation.'),
('A preview failure should leave navigation working. What helps?','A boundary scoped around the preview','One unconditional page crash','A random key on the header','Failure scope should match the recoverable region.')])
M('roots','Mount, hydrate and integrate React DOM','/reference/react-dom/client /reference/react-dom/client/createRoot /reference/react-dom/client/hydrateRoot /reference/react-dom/flushSync /learn/add-react-to-an-existing-project',
'Choose mounting versus hydration and respect DOM ownership.',
'createRoot mounts client-rendered React in a DOM container. hydrateRoot attaches React behavior to HTML already rendered by React on the server. Initial client output must match server HTML; timestamps, random values and browser-only branching can produce hydration mismatches. Treat mismatches as bugs rather than routinely suppressing them. A root owns its subtree; avoid another script mutating the same children. Multiple roots can support independent widgets but do not automatically share context. root.unmount releases the component tree and its Effects. flushSync is a rare integration escape hatch that forces synchronous DOM updates, can hurt performance and can expose fallbacks; do not use it as a default state-update strategy.',
'''import { createRoot, hydrateRoot } from 'react-dom/client';
// Use one path, according to how the host produced this container:
const container = document.getElementById('root');
// Client-only region:
// const root = createRoot(container); root.render(<App />);
// Existing server-rendered React HTML:
// const root = hydrateRoot(container, <App />);''',
'Diagnose a hydration mismatch caused by Date.now() in render. Propose deterministic initial data and a later client update. Explain why a script removing React’s child nodes causes ownership problems.',
'Pass the same initial timestamp/data to the server and initial client tree, then update client-only values deliberately after hydration if needed. Use hydrateRoot only for server React markup, not arbitrary hand-written HTML. Keep outside scripts out of the owned subtree or integrate through explicit component APIs. Use root.unmount when the host removes a React widget so Effects can clean up.',
'Mount client UI, hydrate matching server UI and keep one owner for each DOM subtree.',[
('Which API attaches React to server-rendered React HTML?','hydrateRoot','createPortal','useRef','Hydration attaches behavior to existing server output.'),
('What must initial hydrated output do?','Match the server’s HTML','Generate fresh random text everywhere','Always remove all server nodes','Deterministic initial output avoids mismatches.'),
('What is flushSync?','A rare synchronous integration escape hatch','The normal way to update all input state','A server cache API','Forcing synchronous rendering has costs.'),
('An old host script rewrites children inside the React root. What should change?','Give React sole subtree ownership or create an explicit integration','Call flushSync after every script mutation','Disable keys','Competing DOM owners produce unreliable rendering.')])
M('server-rendering','Choose streaming and static server output','/reference/react-dom/server /reference/react-dom/server/renderToPipeableStream /reference/react-dom/server/renderToReadableStream /reference/react-dom/server/renderToString /reference/react-dom/server/renderToStaticMarkup /reference/react-dom/static /reference/react-dom/static/prerender /reference/react-dom/server/resume',
'Match server rendering APIs to the runtime and intended interactivity.',
'Server rendering produces HTML; it is different from Server Components’ separate module environment. Node hosts can stream with renderToPipeableStream; Web Stream hosts use renderToReadableStream. Streaming works with Suspense to send a shell and reveal later content. renderToString is non-streaming and does not wait for suspended work; renderToStaticMarkup produces non-interactive markup unsuitable for hydration. Static prerender APIs wait for data for planned output; prerenderToNodeStream is the Node variant. React’s resumable/prerender APIs can split precomputed output and later work, with postponed state managed by the host. These are server APIs, not code to paste into a static browser page. Use the framework’s supported rendering pipeline when available.',
'''// Conceptual Node host integration; not a browser runnable snippet.
import { renderToPipeableStream } from 'react-dom/server';
function respond(response, app) {
  const stream = renderToPipeableStream(app, {
    onShellReady() {
      response.setHeader('Content-Type', 'text/html');
      stream.pipe(response);
    },
    onShellError(error) { response.statusCode = 500; response.end('Render failed'); },
    onError(error) { console.error(error); }
  });
  return stream;
}''',
'Choose output for an interactive app, a static email and a Web Stream server. Explain why static markup cannot later be hydrated as if it were interactive output. Identify which bootstrap and error policy your actual host must supply.',
'Use a supported interactive SSR pipeline plus hydrateRoot for an app. Use renderToStaticMarkup for output intended to remain non-interactive, such as email. Use renderToReadableStream in a compatible Web Stream host. The Node sketch omits host routing, bootstrap scripts, status policy after streaming starts and cancellation; implement those in the server/framework layer. Static prerender/resume are advanced host integrations, not browser Hooks.',
'Server output strategy depends on runtime, loading behavior and whether the result will hydrate.',[
('Which API is intended for Node streaming?','renderToPipeableStream','createRoot','renderToStaticMarkup only','Node pipeable streams have a dedicated server API.'),
('Can renderToStaticMarkup output be used as interactive hydrated output?','No','Yes, automatically','Only with useState','It is designed for non-interactive static HTML.'),
('Does renderToString wait for every suspended resource?','No','Yes','Only for arrays','It is non-streaming and has Suspense limitations.'),
('A deployment uses Web Streams rather than Node pipeable streams. Which reference is relevant?','renderToReadableStream','useInsertionEffect','createRef','Choose the server API matching the host stream model.')])
M('server-components','Understand server and client module boundaries','/reference/rsc/server-components /reference/rsc/use-client /reference/rsc/directives /reference/react/use /reference/react/cache /reference/react/cacheSignal',
'Distinguish Server Components, Client Components, SSR and server-scoped caching.',
'Server Components run in a separate environment before the client bundle, at build time or per request depending on the host. They can read server resources without shipping that code to the browser, but cannot use interactive client Hooks. use client defines a client module boundary: its transitive imports participate in the client graph. A Client Component can still have initial HTML server-rendered, so client does not mean never rendered on the server. Pass supported serializable values across the boundary. cache memoizes server computations within React’s server rendering scope, not a universal persistent browser cache. cacheSignal supplies an abort signal for that cache/render lifetime and returns null outside supported scopes. RSC framework/bundler implementation APIs need version discipline.',
'''// Framework/RSC sketch: separate files, not a plain browser app.
// ServerLesson.jsx
async function ServerLesson({ id }) {
  const lesson = await readLessonFromDatabase(id);
  return <ClientFavorite lessonId={lesson.id} title={lesson.title} />;
}
// ClientFavorite.jsx begins with: 'use client';
// It may use client state and receives supported serializable data.''',
'Draw the module boundary for a server-read lesson and an interactive favorite button. Identify where database credentials belong. Explain why adding use client to the top of a large parent increases the client module graph.',
'Keep the database read and credentials in the server environment. Mark only the interactive client entry and its imported dependencies as client code. Pass a minimal supported data contract, not the database connection. Use the host’s RSC integration; the static LMS itself does not execute Server Components. Consider cached server reads and cache lifetime separately from client query caching.',
'Server/client boundaries describe module execution and data contracts; they are not the same as SSR.',[
('Can a Server Component use useState for an interactive button?','No','Yes','Only with cache','Interactive state belongs in a Client Component.'),
('Does use client guarantee a component never contributes server-rendered HTML?','No','Yes','Only for a form','Client Components can participate in initial server rendering.'),
('Is cache a permanent cross-user browser cache?','No','Yes','Only for string keys','Its React server scope is different from durable application caching.'),
('A client component imports a module containing database credentials. What boundary is wrong?','Server-only logic entered the client module graph','The component needs a random key','The provider default is null','Keep secrets and database work in the server environment.')])
M('server-functions','Use Server Functions with trust boundaries','/reference/rsc/server-functions /reference/rsc/use-server /reference/react/useActionState /reference/react/experimental_taintObjectReference /reference/react/experimental_taintUniqueValue',
'Build a server mutation contract without trusting client arguments.',
'use server marks supported async functions as callable Server Functions in an RSC-enabled integration. A function used in an Action becomes a Server Action; not every Server Function use is identical. Arguments arrive from a client-controlled boundary: authenticate the caller, authorize the specific operation and validate values on the server before mutation. Hiding a button or binding an ID is not authorization. Return supported serializable results and design error/refresh behavior through the host. Experimental taint APIs help catch accidental transfer of sensitive values, but do not replace access control or sanitize arbitrary data. This course treats taint as specialist experimental reference, not a required stable dependency.',
'''// RSC/framework server-only sketch. The host supplies these services.
async function renameLesson(lessonId, title) {
  'use server';
  const user = await requireUser();
  await requireLessonPermission(user, lessonId);
  if (typeof title !== 'string') return { error: 'Title must be text' };
  const clean = title.trim();
  if (!clean || clean.length > 120) return { error: 'Use 1–120 characters' };
  await database.rename(lessonId, clean);
  return { ok: true };
}''',
'List the checks required if someone invokes this function without using your UI. Explain why passing userId from the client does not establish identity. Separate expected validation results from unexpected exceptions.',
'Identity comes from the authenticated server session, not an untrusted client claim. Authorize lessonId against that identity, validate title and apply storage rules before writing. Return a recoverable validation message for normal mistakes; use the host’s error boundary/logging policy for failures. Keep experimental taint tools supplemental and version-specific.',
'A Server Function is a remote trust boundary; perform authentication, authorization and validation on the server.',[
('What should authorize a mutation?','Trusted server identity and resource permission','A hidden client button','The key prop','Clients can invoke operations independently of the UI.'),
('What does use server mark in a supported host?','Async Server Functions','Every component as interactive client code','CSS for a server theme','The directive participates in server-function integration.'),
('Do experimental taint APIs replace authorization?','No','Yes','Only for strings','They are supplemental data-transfer safeguards.'),
('A caller changes lessonId manually. What prevents unauthorized changes?','A server permission check for that resource','A disabled UI control','A transition wrapper','Trust cannot be delegated to the client interface.')])
M('dom-resources','Integrate DOM metadata, resources and browser-only content','/reference/react-dom/components/title /reference/react-dom/components/meta /reference/react-dom/components/link /reference/react-dom/components/style /reference/react-dom/components/script /reference/react-dom/components/img /reference/react-dom/components/progress /reference/react-dom/preconnect /reference/react-dom/preload /reference/react-dom/preinit /reference/react-dom/browser',
'Use documented resource behavior without duplicating requests or unsafe markup.',
'React DOM has special behavior for document metadata and resources, including title/meta and qualifying link, style and async script elements. Check each reference’s props and caveats rather than assuming every tag is hoisted or deduplicated the same way. preconnect warms a connection, preload starts fetching a resource, and preinit fetches and prepares resources such as styles or scripts; module variants exist for module resources. Hints can waste bandwidth if issued indiscriminately. Ordinary DOM semantics still matter: meaningful alt text, named progress and safe handling of HTML. Do not inject untrusted strings through dangerouslySetInnerHTML without a trusted sanitization policy. In React 19.3, use(browser()) marks a Client Component as browser-only inside a server Suspense boundary; calling browser() alone does nothing.',
'''import { use } from 'react';
import { browser } from 'react-dom';
function BrowserDraft() {
  use(browser('Draft storage requires this browser.'));
  // A server-rendering parent must provide a Suspense boundary.
  return <p>Browser draft editor</p>;
}
function LessonPage() {
  return <><title>React study studio</title>
    <meta name="description" content="Practice React skills" />
    <h1>React study studio</h1></>;
}''',
'Choose a resource hint for a known next stylesheet versus a speculative origin. Explain the boundary needed for BrowserDraft during SSR. Audit an image and a progress indicator for accessible labels.',
'Use documented preload/preinit behavior for a resource likely to be needed, with correct resource type and host support; preconnect alone does not download the stylesheet. Put browser-only content under an appropriate Suspense fallback on the server. Supply useful image alt text and a label for progress. Keep untrusted text as escaped content; resource hints and React metadata do not sanitize arbitrary HTML.',
'Resource APIs coordinate loading; validate each tag’s special behavior and keep DOM semantics intact.',[
('What does preconnect primarily prepare?','A connection to an origin','The full rendered page','A state reducer','It warms connection setup rather than rendering content.'),
('Does browser() alone mark a component browser-only?','No, pass it to use','Yes','Only if called in a handler','The documented API is use(browser()).'),
('What does a browser-only component need during server rendering?','An appropriate Suspense boundary','A random key','useInsertionEffect everywhere','The server leaves the boundary’s fallback for browser rendering.'),
('An API sends HTML containing scripts. What is the safe default rendering strategy?','Render it as text or use an explicitly trusted sanitization policy','Pass it directly to dangerouslySetInnerHTML','Put it in useMemo','Memoization and JSX ownership do not sanitize injected HTML.')])
M('typescript','Type component and Hook contracts','/learn/typescript /reference/react/useState /reference/react/useRef /reference/react/useContext',
'Use TypeScript to model props, events and valid state without confusing types with validation.',
'TypeScript checks code statically; it does not validate incoming JSON at runtime. Define props around domain inputs and callbacks. Use ReactNode for composable children and appropriate React event types for handlers. Inference handles many useState values; use unions for status models and explicit generics for empty arrays or nullable values. DOM refs need the element type and a null initial state. Context defaults can be nullable, with a custom Hook enforcing provider presence. Reducer action unions permit exhaustive handling. The course’s runnable project uses JavaScript for a lower setup barrier; a typed adaptation is an exercise rather than a false claim that the static LMS executes TypeScript.',
'''import type { ReactNode, ChangeEvent } from 'react';
type PanelProps = { title: string; children: ReactNode };
type Status = { kind: 'idle' } | { kind: 'success'; title: string };
function Panel({ title, children }: PanelProps) {
  return <section><h2>{title}</h2>{children}</section>;
}
function readInput(event: ChangeEvent<HTMLInputElement>) {
  return event.currentTarget.value;
}''',
'Type a Lesson with id, title and completed. Type an onRename callback and a nullable input ref. Model loading, success and error without allowing success to omit data. Explain how unknown JSON still needs runtime checks.',
'''type Lesson = { id: string; title: string; completed: boolean };
type RenameProps = { lesson: Lesson; onRename: (id: string, title: string) => void };
type LoadState =
  | { kind: 'loading' }
  | { kind: 'success'; data: Lesson[] }
  | { kind: 'error'; message: string };
// const inputRef = useRef<HTMLInputElement>(null);
// Validate unknown input before treating it as Lesson[].''',
'Types communicate static contracts; runtime validation and UI behavior still need tests.',[
('What type is suitable for composable children?','ReactNode','Only string','HTMLInputElement','ReactNode covers renderable children.'),
('What does an empty-array state sometimes require?','An explicit element type','A network request during render','A key on useState','Inference may otherwise produce an unhelpful empty array type.'),
('Does a Lesson type validate JSON at runtime?','No','Yes','Only in development','Type information is not a runtime parser.'),
('Success without data should be impossible statically. Which model helps?','A discriminated union','Three unrelated optional fields','A cast to any','The union links a state tag to the fields required in that state.')])
M('testing','Test behavior and diagnose failures','/reference/react/act /reference/react/StrictMode /learn/react-developer-tools /reference/react/Profiler /reference/react/captureOwnerStack',
'Verify user-visible transitions and cleanup rather than implementation details.',
'act helps flush React updates for tests before asserting, and async act is the recommended form for asynchronous update scenarios. User-facing testing helpers may wrap it, but verify their integration rather than ignoring warnings. Test render output, inputs, actions, empty/error/pending states, retries and cleanup. Pure reducers can be tested without rendering; integration tests verify that controls connect to those transitions. Avoid asserting private Hook order or mocking every interaction into a false success. StrictMode can expose missing cleanup, and developer tools/profiling help inspect actual ownership and timing. The included capstone tests use a DOM environment and real React rendering; manual keyboard and screen-reader review remains separate.',
'''// Integration test sketch; a DOM test environment and React are required.
import { act } from 'react';
import { createRoot } from 'react-dom/client';
const container = document.createElement('div');
const root = createRoot(container);
await act(async () => { root.render(<App />); });
// Assert the expected heading and controls, then drive actual events.
await act(async () => { root.unmount(); });''',
'Design tests for an add/complete/filter catalog. Include blank input, no results and a failed save. Explain which checks belong to pure reducer tests and which need rendered user interactions.',
'Pure tests cover immutable transitions, duplicate IDs and no-op updates. Rendered tests enter a title, submit, toggle completion and filter visible results. Async tests wait for the actual pending and error behavior instead of arbitrary timeouts. Unmount components and verify subscription cleanup where external work exists. Review keyboard access and labels in the browser as well.',
'Test observable behavior, model edge cases and resource cleanup at the right layer.',[
('What is act used for?','Flushing React updates before assertions','Replacing a server authorization check','Making every test synchronous','It coordinates pending React work in tests.'),
('Which test directly verifies wiring?','Typing into a rendered form and submitting it','Only calling a reducer','Only comparing file names','Reducer tests alone do not prove that UI events dispatch correctly.'),
('What is a useful error-path test?','A rejected save shows feedback and permits recovery','A mocked save that can only succeed','A screenshot without assertions','Recovery behavior matters alongside success.'),
('A test passes only with a fixed long sleep. What improves it?','Wait for the expected UI condition or controlled async completion','Increase the sleep forever','Disable all assertions','Condition-based waiting is more reliable and tests actual outcomes.')])
M('legacy','Maintain legacy React and specialist APIs','/reference/react/legacy /reference/react/Component /reference/react/PureComponent /reference/react/forwardRef /reference/react/createRef /reference/react/Children /reference/react/cloneElement /reference/react/isValidElement /reference/react/createElement',
'Recognize legacy patterns and migrate deliberately without rewriting working behavior blindly.',
'The current documentation retains legacy APIs for maintenance, not as the preferred foundation for new function-component code. Class components have state and lifecycle methods; Error Boundaries still have a documented class form. PureComponent provides shallow comparison for classes. createRef is commonly used in class code. React 19 can pass ref as a prop to function components, reducing the need for forwardRef in new code. Children transforms opaque children data, while cloneElement changes an element’s props and can obscure data flow; composition or render props can be clearer. isValidElement checks whether a value is a React element, not whether it is every kind of renderable node. createElement remains useful without JSX.',
'''import { Component, createRef } from 'react';
class LegacySearch extends Component {
  input = createRef();
  render() {
    return <><input ref={this.input} aria-label="Legacy search" />
      <button onClick={() => this.input.current?.focus()}>Focus</button></>;
  }
}''',
'Rewrite the class example with useRef while preserving accessible behavior. Explain why a rendering Error Boundary is not replaced by a try/catch around JSX. Review a cloneElement-based API and propose explicit props or children composition.',
'''function Search() {
  const input = useRef(null);
  return <><input ref={input} aria-label="Search" />
    <button onClick={() => input.current?.focus()}>Focus</button></>;
}
// Import useRef from react. Preserve behavior before changing architecture.
// JSX construction is not the same moment as descendant rendering.
// A string can be renderable without satisfying isValidElement.''',
'Maintain legacy behavior with targeted migration and explicit contracts, not automatic rewrites.',[
('What does isValidElement check?','Whether the value is a React element','Whether any value can be rendered','Whether a server user is authorized','Strings can render without being React elements.'),
('What ref pattern is available to new React 19 function components?','Accept ref as a prop','Only class createRef','A random key instead of a ref','React 19 supports function-component ref props.'),
('Does try/catch around returning JSX replace an Error Boundary?','No','Yes','Only if the JSX has a div','Descendant rendering happens through React after JSX construction.'),
('A legacy class feature works reliably. What should guide migration?','Behavioral tests and a targeted need','Replacing everything only because it is old','Deleting its error handling','Migration should preserve observable behavior and serve a concrete goal.')])
M('capstone','Build and evaluate a React study studio','/learn/thinking-in-react /learn/scaling-up-with-reducer-and-context /learn/you-might-not-need-an-effect /reference/react/act',
'Integrate ownership, immutable transitions and accessible UI in a tested project.',
'Build a local study catalog with add, complete and filter actions. Start with a static hierarchy, identify the minimal state, and assign owners. Keep filtering derived from canonical lessons and query. Use a pure reducer for domain transitions, stable IDs for rows and semantic form controls. Include empty, invalid and no-results states. The included examples project provides a runnable implementation and behavioral tests; compare your own attempt against it rather than copying before practicing. This browser-local capstone does not pretend to include authentication, a server, RSC or an AI tutor. Add persistence or async work only after the core model is correct, and document failure and cleanup behavior.',
'''// Core architecture:
// App owns lessons through a reducer and query through state.
// Add form emits an 'added' action with an event-generated ID.
// Each row emits a 'toggled' action with its stable lesson ID.
// Visible rows and completed counts are derived in render.
// Pure model tests and rendered interaction tests check different layers.''',
'Build your implementation before opening examples/App.jsx. Satisfy the rubric in examples/README.md. Demonstrate that whitespace is rejected, duplicate IDs are rejected, input remains usable, completion changes the summary and filtering does not mutate the catalog. Describe one tradeoff and one next feature.',
'The worked solution is examples/App.jsx plus examples/model.mjs. Run npm run dev:example for the project and npm test for model/rendered checks. Compare state ownership, reducer purity, stable keys and labels. Explain how you would add storage without writing during render, and how a remote save would expose pending/error states. Passing the quiz is conceptual evidence; the rubric evaluates practical work.',
'Practical mastery means explaining and testing a working model, not merely marking slides complete.',[
('Where should visible filtered lessons come from?','Derivation from lessons and query','A second independently mutated list','A ref with no rerenders','Derivation preserves one canonical model.'),
('Where should a new ID be generated?','The add event before reducer dispatch','Every reducer invocation','Inside each row render','Event-generated IDs keep the reducer deterministic.'),
('What demonstrates practical mastery beyond the quiz?','A working project meeting a behavioral rubric','Only opening all slides','A 100% screenshot without code','The capstone assesses application rather than recognition alone.'),
('Filtering works but editing after clearing the query loses rows. What architecture should you inspect?','Whether filtering overwrote canonical state','Whether the heading is bold','Whether useId was imported','A view filter must not destroy the underlying catalog.')])
