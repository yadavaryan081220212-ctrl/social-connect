SOCIAL STUDIO — LOCAL TERMINAL DEMO

WHAT IT DOES
- Keeps the Social Studio visual theme.
- Lets you type a sample message in the clearly labelled Test Message field.
- When you click Send to Terminal, the submitted message appears in the terminal window.
- Runs only on this computer at 127.0.0.1. No database or external service is used.
- It does not collect login passwords or hidden form input.

HOW TO RUN
1. Extract this ZIP file.
2. Keep index.html, logger.js, server.py, START_TERMINAL.bat, and this README.txt together in the same folder.
3. Double-click START_TERMINAL.bat.
4. Open http://127.0.0.1:5000 in your browser.
5. Type a test message such as chvsdsb in the Test Message field.
6. Click Send to Terminal. The message should appear in the terminal window.
7. Press Ctrl+C in the terminal to stop the server.

REQUIREMENT
Python 3 must be installed. If the py command is unavailable, edit START_TERMINAL.bat to use python server.py.

PRIVACY
Use this for clearly disclosed test messages only. Do not enter passwords, private information, or other people's sensitive data. The server binds to 127.0.0.1 and does not transmit messages to an external service.
