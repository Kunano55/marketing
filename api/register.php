<?php
// api/register.php - สมัครสมาชิกและบันทึกลง MySQL
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

$username = trim($data['username'] ?? '');
$email = trim($data['email'] ?? '');
$password = $data['password'] ?? '';
$full_name = trim($data['fullName'] ?? $data['full_name'] ?? '');
$phone = trim($data['phone'] ?? '');
$birth_date = !empty($data['birthDate']) ? $data['birthDate'] : (!empty($data['birth_date']) ? $data['birth_date'] : null);
$gender = $data['gender'] ?? 'ไม่ระบุ';
$address = trim($data['address'] ?? '');
$subdistrict = trim($data['subdistrict'] ?? '');
$district = trim($data['district'] ?? '');
$province = trim($data['province'] ?? '');
$zipcode = trim($data['zipcode'] ?? '');
$preferred_category = !empty($data['preferredCategory']) ? trim($data['preferredCategory']) : (!empty($data['preferred_category']) ? trim($data['preferred_category']) : null);
$preferred_flavor = !empty($data['preferredFlavor']) ? trim($data['preferredFlavor']) : (!empty($data['preferred_flavor']) ? trim($data['preferred_flavor']) : null);
$terms_accepted = !empty($data['termsAccepted']) || !empty($data['terms_accepted']) ? 1 : 0;
$marketing_consent = !empty($data['marketingConsent']) || !empty($data['marketing_consent']) ? 1 : 0;

if (empty($username) || empty($email) || empty($password) || empty($full_name)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'กรุณากรอกข้อมูลที่จำเป็นให้ครบถ้วน'], JSON_UNESCAPED_UNICODE);
    exit();
}

try {
    // Duplicate check
    $stmt = $pdo->prepare("SELECT id FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)");
    $stmt->execute([$username, $email]);
    if ($stmt->fetch()) {
        http_response_code(400);
        echo json_encode(['success' => false, 'error' => 'ชื่อผู้ใช้หรืออีเมลนี้มีอยู่ในระบบแล้ว'], JSON_UNESCAPED_UNICODE);
        exit();
    }

    // Auto generate unique user_id
    $idStmt = $pdo->query("SELECT user_id FROM users");
    $existingIds = $idStmt->fetchAll(PDO::FETCH_COLUMN);
    $idx = 1;
    while (in_array(sprintf('USER-2026-%03d', $idx), $existingIds)) {
        $idx++;
    }
    $user_id = !empty($data['userId']) && !in_array($data['userId'], $existingIds) 
        ? $data['userId'] 
        : sprintf('USER-2026-%03d', $idx);

    $insertSql = "
        INSERT INTO users (
            user_id, username, email, password, full_name, phone,
            birth_date, gender, address, subdistrict, district,
            province, zipcode, preferred_category, preferred_flavor,
            terms_accepted, marketing_consent, registered_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
    ";
    $insertStmt = $pdo->prepare($insertSql);
    $insertStmt->execute([
        $user_id, $username, $email, $password, $full_name, $phone,
        $birth_date, $gender, $address, $subdistrict, $district,
        $province, $zipcode, $preferred_category, $preferred_flavor,
        $terms_accepted, $marketing_consent
    ]);

    $newId = $pdo->lastInsertId();
    $userStmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
    $userStmt->execute([$newId]);
    $createdUser = $userStmt->fetch();

    // ส่งอีเมลต้อนรับสมาชิกใหม่พร้อมสินค้าแนะนำตามความชอบผ่าน PHPMailer
    $emailSent = false;
    $welcomeMailFile = dirname(__DIR__) . '/sendMemberWelcomeMail.php';
    if (file_exists($welcomeMailFile)) {
        require_once $welcomeMailFile;
        if (function_exists('sendMemberWelcomeEmail')) {
            $emailSent = sendMemberWelcomeEmail($email, $full_name, $user_id, $preferred_category, $preferred_flavor);
        }
    }

    echo json_encode([
        'success' => true,
        'message' => 'ลงทะเบียนและบันทึกลง MySQL (grobgrob_db) สำเร็จ',
        'welcome_email_sent' => $emailSent,
        'user' => $createdUser
    ], JSON_UNESCAPED_UNICODE);

} catch (\PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Database error: ' . $e->getMessage()], JSON_UNESCAPED_UNICODE);
}
