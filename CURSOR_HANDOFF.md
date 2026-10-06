# React skills course handoff

Replaced the Design Lab starter content with `react-skills-complete-v1`: 35 sections, 35 five-slide lessons, 175 slides, 105 section quiz questions and 35 fresh applied final questions. Authoring lives in `scripts/curriculum.py`; `scripts/build-course.py` regenerates course.json and embedded JSON. Do not manually edit one output without regeneration.

Official source snapshot: reactjs/react.dev `046f17d04295ba047bb5739026b4ac3110f17028` (React 19.3, October 6 2026). docs/COVERAGE.md and source-inventory.json inventory 225 content files with taught/reference/history/test statuses. Source inventory does not imply full page reproduction or a raw offline mirror.

Preserved the repository's newest Design Lab layout and settings: desktop/mobile collapsible sidebar, independent scroll areas, icon navigation and compact charts. Added safe fenced code display, HTTPS source links, metadata preservation, completion guards and section Markdown guide downloads with React attribution and learner notes. Guides require lesson completion plus quiz pass regardless of freely accessible lesson/quiz settings. Actual report data is the default; samples are labeled.

The runnable capstone lives in examples/. It uses a pure immutable reducer and derived search/completion UI with accessible controls. npm test verifies model and rendered behavior, course/source structure, all example syntax and exports. npm run build:example verifies the production app. npm run test:browser exercises full course flow and layout, requiring Playwright/Chromium.

No RAG, executable LMS code editor, authenticated grading, server persistence or framework/RSC runtime is implemented. Server examples are labeled integration sketches. The new course ID preserves starter-course progress separately. Review and merge the course PR to publish via the existing Pages workflow; this work does not deploy independently.
