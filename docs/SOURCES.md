# Source scope and reading method

This is an independent React skills course adapted from the official `react.dev` documentation. Source repository: https://github.com/reactjs/react.dev . Pinned commit: `046f17d04295ba047bb5739026b4ac3110f17028`, inspected October 6, 2026. The snapshot documents React 19.3; the runnable capstone pins React and React DOM to 19.3.0.

The site’s source content inventory contains 225 Markdown files: 135 linked lesson-source pages, 45 reference-only pages, 44 site/community/historical pages and one internal source test page. Every file is inventoried with its source hash, route and coverage status. See `COVERAGE.md` for readable links and `source-inventory.json` for machine-readable provenance.

The authoring review inspected introductory summaries and structure across Learn and Reference, plus targeted API contracts, caveats and release details for the authored material. This is **not** a claim that every long page, embedded playground, historical post or external link was read in full. A lesson-source classification means the page supports an authored skill, not that every option and example on that page has been reproduced. Reference-only material includes API indexes, detailed compiler settings/lints, specialized resource hints and static/resume variants; use those pages for exact integration contracts. Historical/site material is not turned into redundant lessons. The old archived React documentation on other domains is outside this snapshot.

The course covers every current Learn chapter’s subject area and all documented built-in Hook families, modern React components, React DOM integration families, server/client boundaries, the Compiler, testing and legacy maintenance. Overview pages and specialist details can remain reference-only. Experimental taint APIs are labeled experimental, rather than required for stable projects. Current release features such as React 19.3 ViewTransition and Fragment refs are identified explicitly.

Lessons use original explanations, examples, exercises, solutions and scenario questions. Focused snippets may rely on imports or host helpers named in the text; server examples are architecture sketches requiring a compatible framework/runtime. The end-to-end runnable project is in `examples/`. Syntax parsing of every example is distinct from executing every integration sketch.

Content and study guides work from bundled LMS files. Source links require connectivity. The repository supplies neither a raw offline mirror of react.dev nor embeddings, RAG, an AI tutor or executable playground in the LMS. Those can be built later from a separately licensed and versioned corpus.

To regenerate the inventory, clone the source repository, check out the exact commit and run `python3 scripts/inventory-sources.py --source-root /path/to/react.dev`. To regenerate authored course JSON and HTML, run `npm run build:course`; this requires no source checkout or network.
