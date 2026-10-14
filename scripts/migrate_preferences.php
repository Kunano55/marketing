<?php
require_once __DIR__ . '/../api/db.php';

try {
    $cols = $pdo->query("SHOW COLUMNS FROM users LIKE 'preferred_category'")->fetchAll();
    if (empty($cols)) {
        $pdo->exec("ALTER TABLE users ADD COLUMN `preferred_category` VARCHAR(50) NULL DEFAULT 'sheet' COMMENT 'ประเภทสาหร่ายที่ชอบ'");
        echo "Added preferred_category column\n";
    }
    $cols2 = $pdo->query("SHOW COLUMNS FROM users LIKE 'preferred_flavor'")->fetchAll();
    if (empty($cols2)) {
        $pdo->exec("ALTER TABLE users ADD COLUMN `preferred_flavor` VARCHAR(50) NULL DEFAULT 'original' COMMENT 'รสชาติที่ชอบ'");
        echo "Added preferred_flavor column\n";
    }
    echo "Migration completed successfully!\n";
} catch (Exception $e) {
    echo "Migration error: " . $e->getMessage() . "\n";
}
