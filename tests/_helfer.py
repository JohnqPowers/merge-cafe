"""Gemeinsame Hilfen für die Browser-Tests: kleiner HTTP-Server für www/ und Pfade.
Chrome wird über CHROME (Standard: /usr/bin/google-chrome) gestartet. Aufruf immer als: python3 -I tests/<datei>.py"""
import os, threading, http.server, functools
HIER = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(os.path.dirname(HIER), 'www')
CHROME = os.environ.get('CHROME', '/usr/bin/google-chrome')
STATE = os.path.join(HIER, 'state.json')

class _Still(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def server():
    """Startet einen lokalen Server für www/ und gibt die Adresse zurück (z. B. http://127.0.0.1:54321/index.html)."""
    h = functools.partial(_Still, directory=WWW)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), h)   # mehrere Verbindungen gleichzeitig: Chrome öffnet vorab Leerverbindungen
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f'http://127.0.0.1:{srv.server_address[1]}/index.html'
