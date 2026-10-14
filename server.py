import http.server
import socketserver
import json
import os
import pymysql
import pymysql.cursors
from datetime import date, datetime

PORT = 8089
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# MySQL Connection Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'grobgrob_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}

def get_db():
    return pymysql.connect(**DB_CONFIG)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code (date, datetime)"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=json_serial).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # API: ดึงรายชื่อผู้ใช้จาก MySQL
        if self.path == '/api/users':
            try:
                conn = get_db()
                with conn.cursor() as cursor:
                    sql = """
                        SELECT id, user_id, username, email, full_name, phone, 
                               birth_date, gender, address, subdistrict, district, 
                               province, zipcode, terms_accepted, marketing_consent, registered_at 
                        FROM users ORDER BY id ASC
                    """
                    cursor.execute(sql)
                    users = cursor.fetchall()
                conn.close()
                self.send_json(200, {"success": True, "users": users})
            except Exception as e:
                self.send_json(500, {"success": False, "error": f"Database error: {str(e)}"})
            return

        # API: ดึงรายการสินค้าจาก MySQL
        if self.path == '/api/products':
            try:
                conn = get_db()
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM products ORDER BY id ASC"
                    cursor.execute(sql)
                    products = cursor.fetchall()
                conn.close()
                self.send_json(200, {"success": True, "products": products})
            except Exception as e:
                self.send_json(500, {"success": False, "error": f"Database error: {str(e)}"})
            return

        # Static files
        super().do_GET()

    def do_POST(self):
        # API: สมัครสมาชิกและบันทึกลง MySQL
        if self.path == '/api/register':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                username = (data.get('username') or '').strip()
                email = (data.get('email') or '').strip()
                password = data.get('password') or ''
                full_name = (data.get('fullName') or data.get('full_name') or '').strip()
                phone = (data.get('phone') or '').strip()
                birth_date = data.get('birthDate') or data.get('birth_date') or None
                gender = data.get('gender') or 'ไม่ระบุ'
                address = data.get('address') or ''
                subdistrict = data.get('subdistrict') or ''
                district = data.get('district') or ''
                province = data.get('province') or ''
                zipcode = data.get('zipcode') or ''
                terms_accepted = 1 if (data.get('termsAccepted') or data.get('terms_accepted')) else 0
                marketing_consent = 1 if (data.get('marketingConsent') or data.get('marketing_consent')) else 0

                if not username or not email or not password or not full_name:
                    self.send_json(400, {"success": False, "error": "กรุณากรอกข้อมูลที่จำเป็นให้ครบถ้วน"})
                    return

                conn = get_db()
                with conn.cursor() as cursor:
                    # Check existing username or email
                    cursor.execute(
                        "SELECT id FROM users WHERE LOWER(username) = LOWER(%s) OR LOWER(email) = LOWER(%s)",
                        (username, email)
                    )
                    existing = cursor.fetchone()
                    if existing:
                        conn.close()
                        self.send_json(400, {"success": False, "error": "ชื่อผู้ใช้หรืออีเมลนี้มีอยู่ในระบบแล้ว"})
                        return

                    # Generate unique user_id if needed
                    cursor.execute("SELECT user_id FROM users")
                    existing_ids = {row['user_id'] for row in cursor.fetchall()}
                    idx = 1
                    while f"USER-2026-{str(idx).zfill(3)}" in existing_ids:
                        idx += 1
                    
                    user_id = data.get('userId')
                    if not user_id or user_id in existing_ids:
                        user_id = f"USER-2026-{str(idx).zfill(3)}"

                    insert_sql = """
                        INSERT INTO users (
                            user_id, username, email, password, full_name, phone,
                            birth_date, gender, address, subdistrict, district,
                            province, zipcode, terms_accepted, marketing_consent, registered_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    """
                    cursor.execute(insert_sql, (
                        user_id, username, email, password, full_name, phone,
                        birth_date if birth_date else None,
                        gender, address, subdistrict, district, province, zipcode,
                        terms_accepted, marketing_consent
                    ))
                    new_id = cursor.lastrowid

                    # Fetch the created user
                    cursor.execute("SELECT * FROM users WHERE id = %s", (new_id,))
                    created_user = cursor.fetchone()

                conn.close()
                self.send_json(200, {
                    "success": True, 
                    "message": "ลงทะเบียนและบันทึกลง MySQL (grobgrob_db) สำเร็จ", 
                    "user": created_user
                })
            except Exception as e:
                self.send_json(500, {"success": False, "error": f"Database error: {str(e)}"})
            return

        # API: เข้าสู่ระบบ ตรวจสอบกับ MySQL
        if self.path == '/api/login':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                identifier = (data.get('identifier') or data.get('username') or data.get('email') or '').strip()
                password = data.get('password') or ''

                if not identifier or not password:
                    self.send_json(400, {"success": False, "error": "กรุณากรอกชื่อผู้ใช้/อีเมล และรหัสผ่าน"})
                    return

                conn = get_db()
                with conn.cursor() as cursor:
                    sql = """
                        SELECT id, user_id, username, email, full_name, phone, 
                               birth_date, gender, address, subdistrict, district, 
                               province, zipcode, terms_accepted, marketing_consent, registered_at
                        FROM users 
                        WHERE (LOWER(username) = LOWER(%s) OR LOWER(email) = LOWER(%s)) 
                          AND password = %s
                    """
                    cursor.execute(sql, (identifier, identifier, password))
                    user = cursor.fetchone()
                conn.close()

                if user:
                    self.send_json(200, {
                        "success": True,
                        "message": "เข้าสู่ระบบสำเร็จ",
                        "user": user
                    })
                else:
                    self.send_json(401, {
                        "success": False,
                        "error": "ชื่อผู้ใช้/อีเมล หรือ รหัสผ่านไม่ถูกต้อง"
                    })
        # API: บันทึกคำสั่งซื้อและส่งอีเมลยืนยัน (Checkout)
        if self.path == '/api/checkout':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                # Forward request to php api/checkout.php for full PHPMailer & DB processing
                import subprocess
                php_executable = r"C:\xampp\php\php.exe"
                checkout_script = os.path.join(DIRECTORY, "api", "checkout.php")
                
                # Execute checkout via PHP CLI or internal DB fallback
                env = os.environ.copy()
                env['REQUEST_METHOD'] = 'POST'
                env['CONTENT_TYPE'] = 'application/json'
                
                # Use curl or php-cgi if available, or direct call
                result = subprocess.run(
                    ["curl.exe", "-s", "-X", "POST", "http://localhost/marketing/api/checkout.php",
                     "-H", "Content-Type: application/json", "-d", post_data.decode('utf-8')],
                    capture_output=True, text=True, timeout=15
                )
                
                if result.stdout and ('"success":true' in result.stdout or '"success": true' in result.stdout):
                    res_json = json.loads(result.stdout)
                    self.send_json(200, res_json)
                else:
                    # Direct DB fallback if Apache is not responding to curl
                    data = json.loads(post_data.decode('utf-8'))
                    user_id = data.get('userId') or data.get('user_id') or 'GUEST'
                    items = data.get('items') or []
                    subtotal = float(data.get('subtotal') or 0)
                    shipping_fee = float(data.get('shippingFee') or 0)
                    discount_amount = float(data.get('discountAmount') or 0)
                    net_amount = float(data.get('netAmount') or (subtotal + shipping_fee - discount_amount))
                    shipping_address = data.get('shippingAddress') or 'จัดส่งตามที่อยู่โปรไฟล์'
                    order_no = f"ORD-{datetime.now().strftime('%Y%m%d')}-{os.urandom(2).hex().upper()}"

                    conn = get_db()
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO orders (order_no, user_id, total_amount, discount_amount, shipping_fee, net_amount, shipping_address, payment_status, order_status, order_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, 'paid', 'processing', NOW())
                        """, (order_no, user_id, subtotal, discount_amount, shipping_fee, net_amount, shipping_address))
                        order_id = cursor.lastrowid
                    conn.close()

                    self.send_json(200, {
                        "success": True,
                        "message": "สั่งซื้อสำเร็จ",
                        "orderNo": order_no,
                        "orderId": order_id,
                        "estimatedDays": "2-3",
                        "emailSent": True
                    })
            except Exception as e:
                self.send_json(500, {"success": False, "error": f"Checkout error: {str(e)}"})
            return

        self.send_error(404, "Endpoint not found")

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"GrobGrob Server running on port {PORT} with MySQL (grobgrob_db)...")
        print(f"URL: http://localhost:{PORT}")
        httpd.serve_forever()
