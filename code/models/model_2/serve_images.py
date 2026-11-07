import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = 8081
DATASET_DIR = Path(__file__).resolve().parent.parent / "datasets" / "model-2" / "nusaqc_extended_pseudo_dataset"

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

if __name__ == "__main__":
    if not DATASET_DIR.exists():
        print(f"[ERROR] Direktori dataset tidak ditemukan: {DATASET_DIR}")
        sys.exit(1)
        
    os.chdir(DATASET_DIR)
    print(f"[SERVER] Serving dataset images with CORS enabled from:\n   {DATASET_DIR}")
    print(f"[SERVER] Server running at: http://localhost:{PORT}/")
    
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")
