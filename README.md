# React skills

35 sections · 35 five-slide lessons · 175 slides · 35 section quizzes (105 questions) · 35-question applied final assessment.

An independent skills course based on the official React documentation, from components/JSX through state ownership, immutable transitions, Effects, custom Hooks, forms, Actions, Suspense, scheduling, performance, the Compiler, React DOM, server integration, TypeScript, testing, legacy maintenance and a working capstone. See `docs/COVERAGE.md` for the full 225-file source inventory and explicit taught/reference/history distinctions.

Prerequisites: JavaScript functions, closures, modules, arrays, Promises and basic HTML/CSS. Suggested practice time is about 30 minutes per skill section plus capstone work; this is an estimate, not tracked active learning time. Start with foundations and state before attempting escape hatches or server integration. Advanced server and specialist sections can be revisited when the host project needs them.

## Study

Run `python3 -m http.server 8000` here and open http://localhost:8000, or open `index.html` directly subject to browser storage/download rules. The LMS needs no install, backend or external font. Its intended GitHub Pages address is https://pythonidaer.github.io/react-lms/ ; branch changes appear there only after merge/deployment.

Each skill has a goal, explanation, worked example, task, solution and takeaway. Review all five slides to enable lesson completion. Finish the lesson and pass its quiz at 80% to unlock a Markdown study guide containing examples, exercises, solutions, notes and attribution. Each three-question section quiz requires all three correct to meet 80%; retakes are allowed. The 35-question final requires at least 28 correct.

Lessons and quizzes are accessible by default. In learner settings, turn off “Unlock all lessons and quizzes” to use sequential gates, including a final gate requiring all 70 section lesson/quiz items. Freely opening a quiz never bypasses study-guide completion requirements. Practical coding work is self-assessed; use `examples/README.md` for the capstone rubric.

The existing Design Lab theme, collapsible sidebar at all device sizes, independent main/sidebar scrolling, compact report bars and interactive pie are preserved. Section quizzes map to section skills. Grades average each submitted quiz’s best score, including failed grades; unattempted quizzes are excluded. A skill at the passing threshold is marked learned as a quiz indicator, not certified practical mastery. Reports show actual data by default, with a clearly labeled optional sample preview.

## Develop and verify

```sh
npm ci
npm test
npm run build:example
npm run dev:example
```

The capstone is an actual React application, separate from the static LMS. Dependencies are pinned in `package-lock.json`; React and React DOM use 19.3.0. Checks validate course completeness, source routes, offline data agreement, safe formatting/guide attribution, syntax of all 35 examples, immutable reducer behavior and rendered capstone add/complete/filter/remove/error behavior. Focused lesson snippets and framework/server sketches are not all standalone executable applications.

`npm run test:browser` requires Playwright plus Chromium and a local server (or `LMS_TEST_URL` pointing to the offline index). It checks the full course flow, failures/retakes, final assessment, notes/guide downloads, stale-content invalidation, sidebar persistence, independent scrolling, reports and 390/768/1440px layouts.

Author content in `scripts/curriculum.py`, then run `npm run build:course`. Stable IDs preserve progress; changed lesson content invalidates its completion. The new course ID separates this course from sample-course progress. Source provenance is pinned separately from course regeneration.

## Limits

Progress, notes and grades are saved in this browser’s localStorage. No authentication, shared server progress, SCORM/xAPI, exam-secure answers, certified grading, RAG or raw offline React documentation mirror is included. Clearing site data clears progress. Examples and source links are labeled for their actual execution environment. Read `docs/SOURCES.md` and `docs/ATTRIBUTION.md` before extending or redistributing the course.
