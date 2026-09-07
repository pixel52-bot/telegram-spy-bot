import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


class KeepAliveHandler(BaseHTTPRequestHandler):
    """Обрабатывает входящие HTTP-запросы от сервисов мониторинга (cron-job.org)."""

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


def _run_server():
    """Слушает порт Render и держит соединение открытым."""
    port = int(os.getenv("PORT", 8080))
    http_server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    http_server.serve_forever()


def start_server():
    """Запускает мини-сервер в отдельном фоновом потоке."""
    server_thread = threading.Thread(target=_run_server, daemon=True)
    server_thread.start()