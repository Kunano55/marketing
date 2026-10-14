<?php
// api/checkout.php - บันทึกคำสั่งซื้อลง MySQL และจัดส่งอีเมลยืนยันคำสั่งซื้อพร้อมประมาณการวันรับสินค้า
require_once __DIR__ . '/db.php';
require_once __DIR__ . '/../sendOrderConfirmationMail.php';

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

$userId         = trim($data['userId'] ?? $data['user_id'] ?? '');
$items          = $data['items'] ?? [];
$subtotal       = (float)($data['subtotal'] ?? 0);
$shippingFee    = (float)($data['shippingFee'] ?? 0);
$discountAmount = (float)($data['discountAmount'] ?? 0);
$netAmount      = (float)($data['netAmount'] ?? ($subtotal + $shippingFee - $discountAmount));
$customAddress  = trim($data['shippingAddress'] ?? '');
$customPhone    = trim($data['phone'] ?? '');
$customEmail    = trim($data['email'] ?? '');

if (empty($items)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'ไม่มีรายการสินค้าในคำสั่งซื้อ'], JSON_UNESCAPED_UNICODE);
    exit();
}

try {
    // 1. ดึงข้อมูลผู้ใช้จากฐานข้อมูล
    $user = null;
    if (!empty($userId)) {
        $stmtUser = $pdo->prepare("SELECT * FROM users WHERE user_id = ? OR username = ? OR email = ? LIMIT 1");
        $stmtUser->execute([$userId, $userId, $userId]);
        $user = $stmtUser->fetch();
    }

    if (!$user && !empty($customEmail)) {
        $stmtUser = $pdo->prepare("SELECT * FROM users WHERE email = ? LIMIT 1");
        $stmtUser->execute([$customEmail]);
        $user = $stmtUser->fetch();
    }

    // กำหนดข้อมูลลูกค้า
    $resolvedUserId   = $user['user_id'] ?? $userId ?? 'GUEST-ORDER';
    $customerName     = $user['full_name'] ?? ($data['customerName'] ?? 'ลูกค้า GrobGrob');
    $customerEmail    = $user['email'] ?? $customEmail;
    $customerPhone    = !empty($customPhone) ? $customPhone : ($user['phone'] ?? '-');

    if (empty($customerEmail)) {
        http_response_code(400);
        echo json_encode(['success' => false, 'error' => 'ไม่พบอีเมลของลูกค้าสำหรับจัดส่งข้อมูลคำสั่งซื้อ'], JSON_UNESCAPED_UNICODE);
        exit();
    }

    // ประกอบที่อยู่จัดส่ง
    $finalAddress = $customAddress;
    if (empty($finalAddress) && $user) {
        $addrParts = array_filter([
            $user['address'],
            $user['subdistrict'] ? 'ต./แขวง ' . $user['subdistrict'] : '',
            $user['district'] ? 'อ./เขต ' . $user['district'] : '',
            $user['province'] ? 'จ.' . $user['province'] : '',
            $user['zipcode']
        ]);
        $finalAddress = implode(' ', $addrParts);
    }
    if (empty($finalAddress)) {
        $finalAddress = 'จัดส่งตามที่อยู่โปรไฟล์สมาชิก';
    }

    // 2. สร้างเลขที่คำสั่งซื้อใหม่ (Unique Order Number)
    $orderNo = 'ORD-' . date('Ymd') . '-' . strtoupper(substr(uniqid(), -5));

    // เริ่ม Transaction
    $pdo->beginTransaction();

    // 3. บันทึกลงตาราง orders
    $stmtOrder = $pdo->prepare("
        INSERT INTO orders (
            order_no, user_id, total_amount, discount_amount, 
            shipping_fee, net_amount, shipping_address, 
            payment_status, order_status, order_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'paid', 'processing', NOW())
    ");
    $stmtOrder->execute([
        $orderNo,
        $resolvedUserId,
        $subtotal,
        $discountAmount,
        $shippingFee,
        $netAmount,
        $finalAddress
    ]);
    $orderId = (int)$pdo->lastInsertId();

    // 4. บันทึกแต่ละรายการลงตาราง order_items
    $stmtItem = $pdo->prepare("
        INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
        VALUES (?, ?, ?, ?, ?)
    ");

    // ดึง products ทั้งหมดเพื่อ Map หา product_id
    $productsStmt = $pdo->query("SELECT id, category, flavor FROM products");
    $dbProducts = $productsStmt->fetchAll();
    $productMap = [];
    foreach ($dbProducts as $dp) {
        $key = strtolower($dp['category']) . ':' . strtolower($dp['flavor']);
        $productMap[$key] = (int)$dp['id'];
    }

    foreach ($items as $item) {
        $cat = strtolower($item['productId'] ?? 'sheet');
        if ($cat === 'flakes') $cat = 'flake';
        $flv = strtolower($item['flavorId'] ?? 'original');
        $mapSearch = "{$cat}:{$flv}";

        $prodId = $productMap[$mapSearch] ?? 1; // Fallback ไปที่ ID 1
        $qty = max(1, (int)($item['qty'] ?? 1));
        $unitPrice = (float)($item['price'] ?? 0);
        $itemTotal = $unitPrice * $qty;

        $stmtItem->execute([
            $orderId,
            $prodId,
            $qty,
            $unitPrice,
            $itemTotal
        ]);
    }

    $pdo->commit();

    // 5. ส่งอีเมลยืนยันคำสั่งซื้อผ่าน PHPMailer
    $mailPayload = [
        'orderNo'         => $orderNo,
        'customerEmail'   => $customerEmail,
        'customerName'    => $customerName,
        'customerPhone'   => $customerPhone,
        'shippingAddress' => $finalAddress,
        'items'           => $items,
        'subtotal'        => $subtotal,
        'shippingFee'     => $shippingFee,
        'discountAmount'  => $discountAmount,
        'netAmount'       => $netAmount
    ];

    $emailResult = sendOrderConfirmationEmail($mailPayload);

    // ตอบกลับ JSON
    echo json_encode([
        'success'            => true,
        'message'            => 'สั่งซื้อสินค้าสำเร็จและบันทึกลงระบบเรียบร้อยแล้ว',
        'orderNo'            => $orderNo,
        'orderId'            => $orderId,
        'customerName'       => $customerName,
        'customerEmail'      => $customerEmail,
        'estimatedDays'      => $emailResult['estimatedDays'] ?? '2-3',
        'estimatedDateRange' => $emailResult['estimatedDateRange'] ?? '',
        'emailSent'          => $emailResult['success'] ?? false,
        'emailMessage'       => $emailResult['message'] ?? ($emailResult['error'] ?? '')
    ], JSON_UNESCAPED_UNICODE);

} catch (\Exception $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'error' => 'Database/Processing error: ' . $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}
