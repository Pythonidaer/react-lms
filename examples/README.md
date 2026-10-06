# Capstone: React study studio

Try building the task in the final course section before consulting `App.jsx`.

Run `npm ci`, then `npm run dev:example`. The project uses React 19.3.0 and a Vite development host. It is independent of the static course; the LMS itself needs no npm installation. Run `npm run build:example` to build the capstone, and `npm test` for model and rendered interaction checks.

Rubric (demonstrate each behavior and explain the design):

- Add a named lesson; reject blank/whitespace input with recoverable feedback.
- Generate an ID in the event layer; reject duplicate IDs in the model.
- Complete and remove a lesson using immutable transitions.
- Filter titles and optionally completed items without overwriting canonical data.
- Derive the completed count and no-results state rather than storing duplicate state.
- Use stable row keys, labels, semantic buttons and keyboard-operable controls.
- Test original data preservation, duplicate rejection and rendered add/complete/filter/remove flows.
- Explain which data is local, how errors recover and what would change for remote persistence.

The worked implementation is intentionally local and resets on refresh. Persistence, remote saving, RSC and routing are extension tasks, not implied features. The examples in course slides are often focused fragments; this project is the runnable end-to-end example. Quiz success does not establish practical mastery.
