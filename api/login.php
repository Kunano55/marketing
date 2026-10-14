<?php
// api/login.php - ตรวจสอบการเข้าสู่ระบบกับ MySQL
require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed'], JSON_UNESCAPED_UNICODE);
    exit();
}

$raw_input = file_get_contents('php://input');
$data = json_decode($raw_input, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid JSON input'], JSON_UNESCAPED_UNICODE);
    exit();
}

$identifier = trim($data['identifier'] ?? $data['username'] ?? $data['email'] ?? '');
$password   = $data['password'] ?? '';

if (empty($identifier) || empty($password)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'กรุณากรอกชื่อผู้ใช้/อีเมล และรหัสผ่าน'], JSON_UNESCAPED_UNICODE);
    exit();
}

try {
    $stmt = $pdo->prepare("
        SELECT id, user_id, username, email, full_name, phone, 
               birth_date, gender, address, subdistrict, district, 
               province, zipcode, preferred_category, preferred_flavor,
               terms_accepted, marketing_consent, registered_at
        FROM users 
        WHERE (LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)) 
          AND password = ?
    ");
    $stmt->execute([$identifier, $identifier, $password]);
    $user = $stmt->fetch();

    if ($user) {
        echo json_encode([
            'success' => true,
            'message' => 'เข้าสู่ระบบสำเร็จ',
            'user' => $user
        ], JSON_UNESCAPED_UNICODE);
    } else {
        http_response_code(401);
        echo json_encode([
            'success' => false,
            'error' => 'ชื่อผู้ใช้/อีเมล หรือ รหัสผ่านไม่ถูกต้อง'
        ], JSON_UNESCAPED_UNICODE);
    }
} catch (\PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Database error: ' . $e->getMessage()], JSON_UNESCAPED_UNICODE);
}
