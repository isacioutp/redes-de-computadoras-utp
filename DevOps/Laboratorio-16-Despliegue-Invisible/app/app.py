import http.server, pathlib
VERSION = pathlib.Path("/app/VERSION").read_text().strip()

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"ok\n" if self.path == "/health" else f"CitasYA api {VERSION}\n".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):
        pass

http.server.HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
