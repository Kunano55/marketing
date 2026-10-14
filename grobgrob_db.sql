-- ==========================================================
-- GrobGrob E-Commerce Database Schema
-- ออกแบบสำหรับรองรับการย้ายข้อมูลจาก users.json สู่ MySQL / MariaDB (XAMPP)
-- Charset: utf8mb4 เพื่อรองรับภาษาไทยและ Emoji สมบูรณ์แบบ
-- ==========================================================

-- 1. สร้างฐานข้อมูล (หากยังไม่มี)
CREATE DATABASE IF NOT EXISTS `grobgrob_db` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `grobgrob_db`;

-- ----------------------------------------------------------
-- 2. สร้างตาราง users (ตารางสมาชิก แปลงมาจาก users.json)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT 'รหัส Primary Key อัตโนมัติ',
  `user_id` VARCHAR(50) NOT NULL UNIQUE COMMENT 'รหัสผู้ใช้ เช่น USER-2026-001',
  `username` VARCHAR(50) NOT NULL UNIQUE COMMENT 'ชื่อผู้ใช้สำหรับเข้าสู่ระบบ',
  `email` VARCHAR(100) NOT NULL UNIQUE COMMENT 'อีเมลผู้ใช้',
  `password` VARCHAR(255) NOT NULL COMMENT 'รหัสผ่าน (แนะนำให้ Hash เช่น password_hash / bcrypt)',
  `full_name` VARCHAR(100) NOT NULL COMMENT 'ชื่อ-นามสกุล',
  `phone` VARCHAR(20) NOT NULL COMMENT 'เบอร์โทรศัพท์',
  `birth_date` DATE NULL COMMENT 'วัน/เดือน/ปีเกิด (YYYY-MM-DD)',
  `gender` VARCHAR(20) DEFAULT 'ไม่ระบุ' COMMENT 'เพศ เช่น ชาย, หญิง, LGBTQ+, ไม่ระบุ',
  `address` VARCHAR(255) NULL COMMENT 'บ้านเลขที่ / อาคาร / ซอย / ถนน',
  `subdistrict` VARCHAR(100) NULL COMMENT 'ตำบล / แขวง',
  `district` VARCHAR(100) NULL COMMENT 'อำเภอ / เขต',
  `province` VARCHAR(100) NULL COMMENT 'จังหวัด',
  `zipcode` VARCHAR(10) NULL COMMENT 'รหัสไปรษณีย์',
  `terms_accepted` TINYINT(1) DEFAULT 1 COMMENT 'ยอมรับเงื่อนไขและ PDPA (1=ยินยอม, 0=ไม่ยินยอม)',
  `marketing_consent` TINYINT(1) DEFAULT 0 COMMENT 'ยินยอมรับข่าวสารโปรโมชั่น (1=ยินยอม, 0=ไม่ยินยอม)',
  `registered_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'เวลาที่ลงทะเบียน',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'เวลาที่สร้างเรคคอร์ดในฐานข้อมูล',
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'เวลาที่มีการแก้ไขล่าสุด',
  INDEX `idx_username` (`username`),
  INDEX `idx_email` (`email`),
  INDEX `idx_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ตารางข้อมูลสมาชิก GrobGrob';

-- ----------------------------------------------------------
-- 3. นำเข้าข้อมูลเริ่มต้นจากไฟล์ users.json
-- ----------------------------------------------------------
INSERT INTO `users` (
  `user_id`, `username`, `email`, `password`, `full_name`, 
  `phone`, `birth_date`, `gender`, `address`, `subdistrict`, 
  `district`, `province`, `zipcode`, `terms_accepted`, `marketing_consent`, `registered_at`
) VALUES
(
  'USER-2026-001', 
  'somchai_grob', 
  'somchai@example.com', 
  'Password123!', 
  'นายสมชาย ใจดี', 
  '081-234-5678', 
  '1995-05-15', 
  'ชาย', 
  '99/1 หมู่บ้านสุขสันต์ ถนนพัฒนาการ', 
  'สวนหลวง', 
  'สวนหลวง', 
  'กรุงเทพมหานคร', 
  '10250', 
  1, 
  1, 
  '2026-09-01 10:00:00'
),
(
  'USER-2026-002', 
  'may_healthy', 
  'may.n@example.com', 
  'Password123!', 
  'นางสาวนภาวรรณ มีสุข', 
  '089-876-5432', 
  '1998-11-20', 
  'หญิง', 
  '45/12 คอนโดลุมพินี ซอยสุขุมวิท 55', 
  'คลองตันเหนือ', 
  'วัฒนา', 
  'กรุงเทพมหานคร', 
  '10110', 
  1, 
  1, 
  '2026-09-01 14:30:00'
),
(
  'USER-2026-004', 
  'kong', 
  'kong@gmail.com', 
  '123456', 
  'นายก้อง สารี', 
  '0812345678', 
  '2003-02-13', 
  'ชาย', 
  '200', 
  'หนองบัว', 
  'เมือง', 
  'อุดร', 
  '41000', 
  1, 
  0, 
  '2026-09-01 17:50:07'
);

-- ==========================================================
-- 4. (ส่วนเสริมแนะนำ) ตารางสินค้าและคำสั่งซื้อสำหรับระบบ E-Commerce
-- ==========================================================

-- 4.1 ตารางสินค้า (products)
CREATE TABLE IF NOT EXISTS `products` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `product_code` VARCHAR(50) NOT NULL UNIQUE COMMENT 'รหัสสินค้า เช่น GROB-SH-ORIGINAL',
  `category` ENUM('sheet', 'roll', 'flake') NOT NULL COMMENT 'หมวดหมู่สินค้า (แผ่น, ม้วน, โรยข้าว)',
  `flavor` VARCHAR(50) NOT NULL COMMENT 'รสชาติ เช่น รสดั้งเดิม, สไปซี่, วาซาบิ, บาร์บีคิว',
  `name_th` VARCHAR(150) NOT NULL COMMENT 'ชื่อสินค้าภาษาไทย',
  `name_en` VARCHAR(150) NULL COMMENT 'ชื่อสินค้าภาษาอังกฤษ',
  `price` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'ราคาขาย (บาท)',
  `stock_quantity` INT NOT NULL DEFAULT 100 COMMENT 'จำนวนคงเหลือในสต็อก',
  `image_url` VARCHAR(255) NULL COMMENT 'พาธรูปภาพสินค้า',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4.2 ตารางคำสั่งซื้อ (orders)
CREATE TABLE IF NOT EXISTS `orders` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_no` VARCHAR(50) NOT NULL UNIQUE COMMENT 'เลขที่คำสั่งซื้อ เช่น ORD-20260901-0001',
  `user_id` VARCHAR(50) NOT NULL COMMENT 'รหัสลูกค้า อ้างอิงจาก users.user_id',
  `total_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'ราคารวมสินค้า',
  `discount_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'ส่วนลดจากคูปอง (เช่น GROB10)',
  `shipping_fee` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'ค่าจัดส่ง',
  `net_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'ยอดสุทธิที่ต้องชำระ',
  `shipping_address` TEXT NOT NULL COMMENT 'ที่อยู่สำหรับจัดส่งในออเดอร์นี้',
  `payment_status` ENUM('pending', 'paid', 'failed') DEFAULT 'pending' COMMENT 'สถานะชำระเงิน',
  `order_status` ENUM('pending', 'processing', 'shipped', 'completed', 'cancelled') DEFAULT 'pending' COMMENT 'สถานะออเดอร์',
  `order_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4.3 ตารางรายการสินค้าในคำสั่งซื้อ (order_items)
CREATE TABLE IF NOT EXISTS `order_items` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `quantity` INT NOT NULL DEFAULT 1,
  `unit_price` DECIMAL(10, 2) NOT NULL,
  `subtotal` DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
