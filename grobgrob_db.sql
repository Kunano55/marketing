-- ==========================================================
-- GrobGrob Complete Database Schema & Data Dump
-- Charset: utf8mb4
-- ==========================================================
CREATE DATABASE IF NOT EXISTS `grobgrob_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `grobgrob_db`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_code` varchar(50) NOT NULL COMMENT 'รหัสสินค้า เช่น GROB-SH-ORIGINAL',
  `category` enum('sheet','roll','flake') NOT NULL COMMENT 'หมวดหมู่สินค้า (แผ่น, ม้วน, โรยข้าว)',
  `flavor` varchar(50) NOT NULL COMMENT 'รสชาติ เช่น รสดั้งเดิม, สไปซี่, วาซาบิ, บาร์บีคิว',
  `name_th` varchar(150) NOT NULL COMMENT 'ชื่อสินค้าภาษาไทย',
  `name_en` varchar(150) DEFAULT NULL COMMENT 'ชื่อสินค้าภาษาอังกฤษ',
  `price` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT 'ราคาขาย (บาท)',
  `stock_quantity` int(11) NOT NULL DEFAULT 100 COMMENT 'จำนวนคงเหลือในสต็อก',
  `image_url` varchar(255) DEFAULT NULL COMMENT 'พาธรูปภาพสินค้า',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_code` (`product_code`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `products` (`id`, `product_code`, `category`, `flavor`, `name_th`, `name_en`, `price`, `stock_quantity`, `image_url`, `created_at`) VALUES
  (1, 'GROB-SH-ORIGINAL', 'sheet', 'original', 'สาหร่ายอบกรอบแผ่น รสออริจินัล', 'Crispy Seaweed Sheet - Original', '39.00', 100, 'assets/seaweed-sheet.png', '2026-10-08 09:45:47'),
  (2, 'GROB-SH-SPICY', 'sheet', 'spicy', 'สาหร่ายอบกรอบแผ่น รสเผ็ดสไปซี่พริกคั่ว', 'Crispy Seaweed Sheet - Spicy', '39.00', 100, 'assets/sheet_spicy.png', '2026-10-08 09:45:47'),
  (3, 'GROB-SH-BBQ', 'sheet', 'bbq', 'สาหร่ายอบกรอบแผ่น รสบาร์บีคิวรมควัน', 'Crispy Seaweed Sheet - BBQ', '39.00', 100, 'assets/sheet_bbq.png', '2026-10-08 09:45:47'),
  (4, 'GROB-SH-CHEESE', 'sheet', 'cheese', 'สาหร่ายอบกรอบแผ่น รสฮอกไกโดชีส', 'Crispy Seaweed Sheet - Hokkaido Cheese', '39.00', 100, 'assets/sheet_cheese.png', '2026-10-08 09:45:47'),
  (5, 'GROB-RL-ORIGINAL', 'roll', 'original', 'สาหร่ายม้วนอบกรอบ รสดั้งเดิม', 'Crispy Seaweed Roll - Original', '49.00', 100, 'assets/seaweed-roll.png', '2026-10-08 09:45:47'),
  (6, 'GROB-RL-SPICY', 'roll', 'spicy', 'สาหร่ายม้วนอบกรอบ รสสไปซี่ฮอต', 'Crispy Seaweed Roll - Spicy Hot', '49.00', 100, 'assets/roll_spicy.png', '2026-10-08 09:45:47'),
  (7, 'GROB-RL-WASABI', 'roll', 'wasabi', 'สาหร่ายม้วนอบกรอบ รสวาซาบิญี่ปุ่น', 'Crispy Seaweed Roll - Wasabi', '49.00', 100, 'assets/roll_wasabi.png', '2026-10-08 09:45:47'),
  (8, 'GROB-RL-BBQ', 'roll', 'bbq', 'สาหร่ายม้วนอบกรอบ รสสโมคบาร์บีคิว', 'Crispy Seaweed Roll - Smoky BBQ', '49.00', 100, 'assets/roll_bbq.png', '2026-10-08 09:45:47'),
  (9, 'GROB-FK-ORIGINAL', 'flake', 'original', 'สาหร่ายโรยข้าว รสคลาสสิกงาหอม', 'Seaweed Rice Flakes - Classic Sesame', '59.00', 100, 'assets/seaweed-flake.png', '2026-10-08 09:45:47'),
  (10, 'GROB-FK-SPICY', 'flake', 'spicy', 'สาหร่ายโรยข้าว รสชิลลี่การ์ลิค', 'Seaweed Rice Flakes - Chili Garlic', '59.00', 100, 'assets/flakes_spicy.png', '2026-10-08 09:45:47'),
  (11, 'GROB-FK-SALTEDEGG', 'flake', 'saltedegg', 'สาหร่ายโรยข้าว รสไข่เค็มลาวา', 'Seaweed Rice Flakes - Salted Egg', '59.00', 100, 'assets/flakes_saltedegg.png', '2026-10-08 09:45:47'),
  (12, 'GROB-FK-GARLIC', 'flake', 'garlic', 'สาหร่ายโรยข้าว รสเนยกระเทียม', 'Seaweed Rice Flakes - Butter Garlic', '59.00', 100, 'assets/flakes_garlic.png', '2026-10-08 09:45:47');

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'รหัส Primary Key อัตโนมัติ',
  `user_id` varchar(50) NOT NULL COMMENT 'รหัสผู้ใช้ เช่น USER-2026-001',
  `username` varchar(50) NOT NULL COMMENT 'ชื่อผู้ใช้สำหรับเข้าสู่ระบบ',
  `email` varchar(100) NOT NULL COMMENT 'อีเมลผู้ใช้',
  `password` varchar(255) NOT NULL COMMENT 'รหัสผ่าน (แนะนำให้ Hash เช่น password_hash / bcrypt)',
  `full_name` varchar(100) NOT NULL COMMENT 'ชื่อ-นามสกุล',
  `phone` varchar(20) NOT NULL COMMENT 'เบอร์โทรศัพท์',
  `birth_date` date DEFAULT NULL COMMENT 'วัน/เดือน/ปีเกิด (YYYY-MM-DD)',
  `gender` varchar(20) DEFAULT 'ไม่ระบุ' COMMENT 'เพศ เช่น ชาย, หญิง, LGBTQ+, ไม่ระบุ',
  `address` varchar(255) DEFAULT NULL COMMENT 'บ้านเลขที่ / อาคาร / ซอย / ถนน',
  `subdistrict` varchar(100) DEFAULT NULL COMMENT 'ตำบล / แขวง',
  `district` varchar(100) DEFAULT NULL COMMENT 'อำเภอ / เขต',
  `province` varchar(100) DEFAULT NULL COMMENT 'จังหวัด',
  `zipcode` varchar(10) DEFAULT NULL COMMENT 'รหัสไปรษณีย์',
  `terms_accepted` tinyint(1) DEFAULT 1 COMMENT 'ยอมรับเงื่อนไขและ PDPA (1=ยินยอม, 0=ไม่ยินยอม)',
  `marketing_consent` tinyint(1) DEFAULT 0 COMMENT 'ยินยอมรับข่าวสารโปรโมชั่น (1=ยินยอม, 0=ไม่ยินยอม)',
  `registered_at` datetime DEFAULT current_timestamp() COMMENT 'เวลาที่ลงทะเบียน',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'เวลาที่สร้างเรคคอร์ดในฐานข้อมูล',
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'เวลาที่มีการแก้ไขล่าสุด',
  `preferred_category` varchar(50) DEFAULT 'sheet' COMMENT 'ประเภทสาหร่ายที่ชอบ',
  `preferred_flavor` varchar(50) DEFAULT 'original' COMMENT 'รสชาติที่ชอบ',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_username` (`username`),
  KEY `idx_email` (`email`),
  KEY `idx_phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ตารางข้อมูลสมาชิก GrobGrob';

INSERT INTO `users` (`id`, `user_id`, `username`, `email`, `password`, `full_name`, `phone`, `birth_date`, `gender`, `address`, `subdistrict`, `district`, `province`, `zipcode`, `terms_accepted`, `marketing_consent`, `registered_at`, `created_at`, `updated_at`, `preferred_category`, `preferred_flavor`) VALUES
  (1, 'USER-2026-001', 'somchai_grob', 'somchai@example.com', 'Password123!', 'นายสมชาย ใจดี', '081-234-5678', '1995-05-15', 'ชาย', '99/1 หมู่บ้านสุขสันต์ ถนนพัฒนาการ', 'สวนหลวง', 'สวนหลวง', 'กรุงเทพมหานคร', '10250', 1, 1, '2026-09-01 10:00:00', '2026-09-16 23:56:22', '2026-09-16 23:56:22', 'sheet', 'original'),
  (2, 'USER-2026-002', 'may_healthy', 'may.n@example.com', 'Password123!', 'นางสาวนภาวรรณ มีสุข', '089-876-5432', '1998-11-20', 'หญิง', '45/12 คอนโดลุมพินี ซอยสุขุมวิท 55', 'คลองตันเหนือ', 'วัฒนา', 'กรุงเทพมหานคร', '10110', 1, 1, '2026-09-01 14:30:00', '2026-09-16 23:56:22', '2026-09-16 23:56:22', 'sheet', 'original'),
  (3, 'USER-2026-004', 'kong', 'noobzaza77@gmail.com', '123456', 'นายก้อง สารี', '0812345678', '2003-02-13', 'ชาย', '200', 'หนองบัว', 'เมือง', 'อุดร', '41000', 1, 0, '2026-09-01 17:50:07', '2026-09-16 23:56:22', '2026-09-17 12:06:04', 'sheet', 'original'),
  (7, 'USER-2026-003', 'konggong', 'kukongkaka@gmail.com', '558947', 'นายจิม', '0812345678', '2026-09-03', 'LGBTQ+', '300', 'ฟหก', 'ฟหก', 'ฟหก', 'ฟหก', 1, 1, '2026-09-17 12:09:58', '2026-09-17 12:09:58', '2026-09-17 12:09:58', 'roll', 'bbq');

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(50) NOT NULL COMMENT 'เลขที่คำสั่งซื้อ เช่น ORD-20260901-0001',
  `user_id` varchar(50) NOT NULL COMMENT 'รหัสลูกค้า อ้างอิงจาก users.user_id',
  `total_amount` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT 'ราคารวมสินค้า',
  `discount_amount` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT 'ส่วนลดจากคูปอง (เช่น GROB10)',
  `shipping_fee` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT 'ค่าจัดส่ง',
  `net_amount` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT 'ยอดสุทธิที่ต้องชำระ',
  `shipping_address` text NOT NULL COMMENT 'ที่อยู่สำหรับจัดส่งในออเดอร์นี้',
  `payment_status` enum('pending','paid','failed') DEFAULT 'pending' COMMENT 'สถานะชำระเงิน',
  `order_status` enum('pending','processing','shipped','completed','cancelled') DEFAULT 'pending' COMMENT 'สถานะออเดอร์',
  `order_date` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `orders` (`id`, `order_no`, `user_id`, `total_amount`, `discount_amount`, `shipping_fee`, `net_amount`, `shipping_address`, `payment_status`, `order_status`, `order_date`) VALUES
  (1, 'ORD-20261008-91E9A', 'USER-2026-004', '127.00', '0.00', '35.00', '162.00', '200 ต./แขวง หนองบัว อ./เขต เมือง จ.อุดร 41000', 'paid', 'processing', '2026-10-08 09:48:03'),
  (2, 'ORD-20261008-11DF2', 'USER-2026-004', '160.00', '0.00', '0.00', '160.00', '200 ต./แขวง หนองบัว อ./เขต เมือง จ.อุดร 41000', 'paid', 'processing', '2026-10-08 09:51:13');

DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `unit_price` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `quantity`, `unit_price`, `subtotal`) VALUES
  (1, 1, 1, 2, '39.00', '78.00'),
  (2, 1, 6, 1, '49.00', '49.00'),
  (3, 2, 10, 1, '45.00', '45.00'),
  (4, 2, 7, 1, '35.00', '35.00'),
  (5, 2, 8, 1, '35.00', '35.00'),
  (6, 2, 12, 1, '45.00', '45.00');

SET FOREIGN_KEY_CHECKS = 1;
