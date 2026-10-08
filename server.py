from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class VoiceHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/voice':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            user_text = data.get('message', '')
            print(f"\n[Voice Received]: {user_text}")
            
            # Reponse Headers
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    print("Server running on http://localhost:5000")
    print("Web app-la Mic button click panni pesungga...")
    server = HTTPServer(('localhost', 5000), VoiceHandler)
    server.serve_forever()

if __name__ == '__main__':
    run_server()
