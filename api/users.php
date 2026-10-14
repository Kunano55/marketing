<?php
// api/users.php - ดึงข้อมูลสมาชิกจาก MySQL
require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

try {
    $stmt = $pdo->query("
        SELECT id, user_id, username, email, full_name, phone, 
               birth_date, gender, address, subdistrict, district, 
               province, zipcode, terms_accepted, marketing_consent, registered_at
        FROM users 
        ORDER BY id ASC
    ");
    $users = $stmt->fetchAll();

    echo json_encode([
        'success' => true,
        'users' => $users
    ], JSON_UNESCAPED_UNICODE);
} catch (\PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Database error: ' . $e->getMessage()], JSON_UNESCAPED_UNICODE);
}
