# Design foundations

Run `python3 -m http.server 8000` in this folder and open http://localhost:8000. You can deploy this directory to any static host. No install/build step is needed. Direct remote media URLs require connectivity and permission to load. Uploaded media is packaged in assets/.

Edit course.json and copy its JSON into the lms-course-data script in index.html, or re-export from Design Lab. The embedded JSON lets the course load without a data API. Keep IDs stable to preserve progress; changing a lesson’s content changes its fingerprint and starts that lesson’s saved progress over.

Progress is stored in this browser’s localStorage, one key per course. A refresh on the same browser keeps lesson completion, quiz attempts, scores, and pass or fail, lesson notes, and the last opened lesson. It also keeps the learner name, outline state, and learner settings. Nothing is sent to a server, so another browser or device starts fresh. Clearing this site’s data removes it. There is no authentication, cloud dashboard, SCORM/xAPI integration, or verified grading. Correct answers are in the client, and quiz attempts are not exam-secure.
