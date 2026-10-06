import { useId, useReducer, useState } from 'react';
import { planReducer, selectLessons } from './model.mjs';
export default function App() {
  const [lessons, dispatch] = useReducer(planReducer, []);
  const [query, setQuery] = useState('');
  const [onlyCompleted, setOnlyCompleted] = useState(false);
  const [error, setError] = useState('');
  const searchId = useId();
  const visible = selectLessons(lessons, query, onlyCompleted);
  function add(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const title = String(new FormData(form).get('title') || '').trim();
    if (!title) { setError('Enter a lesson title.'); return; }
    dispatch({ type: 'added', lesson: { id: crypto.randomUUID(), title } });
    setError('');
    form.reset();
  }
  return <main>
    <h1>React study studio</h1>
    <form onSubmit={add}>
      <label>Lesson title <input name="title" aria-describedby={error ? 'add-error' : undefined} /></label>
      <button type="submit">Add lesson</button>
      {error && <p id="add-error" role="alert">{error}</p>}
    </form>
    <label htmlFor={searchId}>Search lessons</label>
    <input id={searchId} value={query} onChange={e => setQuery(e.currentTarget.value)} />
    <label><input type="checkbox" checked={onlyCompleted} onChange={e => setOnlyCompleted(e.currentTarget.checked)} /> Completed only</label>
    <p role="status">{lessons.filter(item => item.completed).length} of {lessons.length} completed</p>
    {!lessons.length ? <p>Add your first lesson.</p> : !visible.length ? <p>No matching lessons.</p> : <ul>
      {visible.map(item => <li key={item.id}>
        <label><input type="checkbox" checked={item.completed} onChange={() => dispatch({ type: 'toggled', id: item.id })} /> {item.title}</label>
        <button aria-label={'Remove ' + item.title} onClick={() => dispatch({ type: 'removed', id: item.id })}>Remove</button>
      </li>)}
    </ul>}
  </main>;
}
