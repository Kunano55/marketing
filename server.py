import http.server
import socketserver
import json
import os

PORT = 8089
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/api/register':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                new_user = json.loads(post_data.decode('utf-8'))
                users_file = os.path.join(DIRECTORY, 'users.json')
                
                users = []
                if os.path.exists(users_file):
                    with open(users_file, 'r', encoding='utf-8') as f:
                        try:
                            users = json.load(f)
                        except Exception:
                            users = []

                # Duplicate check
                username_exists = any(u.get('username', '').lower() == new_user.get('username', '').lower() for u in users)
                email_exists = any(u.get('email', '').lower() == new_user.get('email', '').lower() for u in users)

                if username_exists or email_exists:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    response = {"success": False, "error": "ชื่อผู้ใช้หรืออีเมลนี้มีอยู่ในระบบแล้ว"}
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                    return

                users.append(new_user)

                with open(users_file, 'w', encoding='utf-8') as f:
                    json.dump(users, f, ensure_ascii=False, indent=2)

                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"success": True, "message": "ลงทะเบียนและบันทึกลง users.json สำเร็จ", "user": new_user}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"GrobGrob Server running on port {PORT} with users.json auto-save...")
        httpd.serve_forever()
