@echo off
rem Nepali Rhyme Hub pre-video review: starts the local review server and opens it in the browser.
rem Comments and approvals are saved in each song's review\ folder. Close this window to stop the server.
cd /d D:\claude_project\subu-os
start "" http://127.0.0.1:8767/
python -m subu.musicvideo review serve --port 8767 --channel nepali-rhyme-hub
