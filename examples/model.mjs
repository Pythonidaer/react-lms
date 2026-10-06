export function planReducer(state, action) {
  switch (action.type) {
    case 'added': {
      const { id, title } = action.lesson;
      if (typeof id !== 'string' || !id || state.some(item => item.id === id)) throw new Error('Unique ID required');
      if (typeof title !== 'string' || !title.trim()) throw new Error('Title required');
      return [...state, { id, title: title.trim(), completed: false }];
    }
    case 'toggled': return state.map(item => item.id === action.id ? { ...item, completed: !item.completed } : item);
    case 'removed': return state.filter(item => item.id !== action.id);
    default: throw new Error('Unknown action');
  }
}
export function selectLessons(lessons, query, onlyCompleted) {
  const term = query.trim().toLocaleLowerCase();
  return lessons.filter(item => item.title.toLocaleLowerCase().includes(term) && (!onlyCompleted || item.completed));
}
