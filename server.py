from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parent
ALLOWED_EVENTS = {"PAGE_VIEW", "LEARN_MORE_CLICKED"}
MAX_MESSAGE_LENGTH = 200

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/index.html": ("index.html", "text/html; charset=utf-8"),
            "/logger.js": ("logger.js", "application/javascript; charset=utf-8"),
        }
        item = routes.get(self.path)
        if not item:
            self.send_error(404)
            return
        filename, content_type = item
        data = (ROOT / filename).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/events":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 4096:
                self.send_error(413, "Invalid request size")
                return
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(body, dict):
                raise ValueError("JSON body must be an object")
            event = body.get("event")
            if event == "DEMO_MESSAGE_SUBMITTED":
                message = body.get("message")
                if not isinstance(message, str):
                    self.send_error(400, "Message must be text")
                    return
                message = message.strip()
                if not message or len(message) > MAX_MESSAGE_LENGTH:
                    self.send_error(400, "Message must be 1-200 characters")
                    return
                # Explicitly submitted demo text only; never log credentials or other form fields.
                printable = message.replace("\r", " ").replace("\n", " ")
                self._print_terminal(f"DEMO MESSAGE: {printable}")
            elif event in ALLOWED_EVENTS:
                self._print_terminal(event)
            else:
                self.send_error(400, "Unknown event")
                return
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            self.send_error(400, "Invalid JSON")
            return

        response = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    @staticmethod
    def _print_terminal(message):
        timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        print(f"[{timestamp}] {message}", flush=True)

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 5000), Handler)
    print("Social Studio local terminal demo is running.", flush=True)
    print("Open http://127.0.0.1:5000 in your browser.", flush=True)
    print("Only messages explicitly submitted in the Test Message field are displayed.", flush=True)
    print("Nothing is sent to an external service. Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.", flush=True)
    finally:
        server.server_close()
