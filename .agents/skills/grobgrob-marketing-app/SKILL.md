---
name: grobgrob-marketing-app
description: Comprehensive architecture, MySQL database setup, dual Python/PHP backend, PHPMailer email automation, and 5-step digital marketing roadmap for the GrobGrob Seaweed E-commerce application.
---

# GrobGrob Seaweed E-commerce & Digital Marketing Skill

คู่มือและโครงสร้างสถาปัตยกรรมฉบับสมบูรณ์ของเว็บแอปพลิเคชันร้านค้าออนไลน์ **GrobGrob (สาหร่ายอบกรอบ)** ครอบคลุมทั้งระบบฐานข้อมูล MySQL, Backend (Python & PHP), ระบบอีเมลอัตโนมัติด้วย PHPMailer, และระบบ Digital Marketing Roadmap 5 ขั้นตอน

---

## 📂 โครงสร้างไฟล์ในโปรเจกต์ (Project Architecture)

### 1. หน้าเว็บหลัก (Frontend Pages)
- **`index.html`**: หน้าแรกของเว็บไซต์ แนะนำแบรนด์ สินค้าไฮไลต์ รีวิวลูกค้า บล็อกสมัครรับข่าวสาร (Subscribe) และแถบเมนูนำทาง
- **`products.html`**: หน้ารวมสินค้า 12 รสชาติ (3 หมวดหมู่: แผ่น, ม้วน, โรยข้าว) พร้อมแบบสอบถามรสชาติ (Taste Quiz) และระบบแนะนำสินค้าตามพฤติกรรม (Behavior-based Recommendations)
- **`cart.html`**: หน้าตะกร้าสินค้า คำนวณราคาสุทธิ ส่วนลดคูปอง (`GROB10`, `WELCOME10`) ส่งฟรี (>= 150 บาท) พร้อมระบบแนะนำสินค้าซื้อคู่กัน (Frequently Bought Together)
- **`register.html`**: หน้าสมัครสมาชิก บันทึกลง MySQL ผ่าน API และส่งอีเมลต้อนรับให้อัตโนมัติ
- **`login.html`**: หน้าเข้าสู่ระบบ ตรวจสอบกับ MySQL แบบ Real-time ผ่าน API
- **`subscribe_form.php`**: หน้าฟอร์มเดี่ยวสำหรับการสมัครรับข่าวสาร (Leads Collection)
- **`personalized_marketing.php`**: หน้าเลือกความชอบ (รูปแบบสาหร่าย + รสชาติ) และส่งข้อเสนอเฉพาะบุคคลไปยังอีเมลของบัญชีที่ล็อกอินอยู่โดยอัตโนมัติ

### 2. ตรรกะและสไตล์ (Scripts & Styles)
- **`app.js`**: สคริปต์หลักสำหรับ:
  - จัดการระบบตะกร้าสินค้า (Cart Drawer & Cart Table)
  - `GrobAuth`: State Manager สำหรับตรวจสอบและซิงค์ข้อมูลสมาชิกระหว่าง MySQL กับ `localStorage`
  - `recordUserBehavior`: บันทึกพฤติกรรมผู้ใช้ (Recently Viewed & Category Interactions)
  - `renderBehaviorRecommendations`: ระบบแนะนำสินค้าอัจฉริยะจากพฤติกรรมและสินค้าในตะกร้า
- **`style.css`**: ดีไซน์ซิสเต็มหลัก (สี Earth Tone, Organic Food, Glassmorphism, Micro-animations)

### 3. ฐานข้อมูล (Database Layer)
- **`grobgrob_db.sql`**: สคริปต์สร้างฐานข้อมูล MySQL `grobgrob_db` (Collation: `utf8mb4_unicode_ci`):
  - `users`: ตารางสมาชิก (Primary Key, Unique constraints, ข้อมูลติดต่อ, ที่อยู่, PDPA Consent)
  - `products`: ตารางสินค้า 12 รสชาติ และสต็อก
  - `orders`: ตารางบันทึกคำสั่งซื้อ เชื่อมโยง Foreign Key กับ `users.user_id`
  - `order_items`: ตารางรายการสินค้าในคำสั่งซื้อ

### 4. เซิร์ฟเวอร์และ API (Backend Layer)
- **`api/db.php`**: เชื่อมต่อ MySQL ผ่าน PHP PDO
- **`api/register.php`**: รับ POST ข้อมูลสมัครสมาชิก บันทึกลง MySQL และเรียกฟังก์ชันส่งอีเมลต้อนรับ
- **`api/login.php`**: รับ POST ยืนยันตัวตนกับตาราง `users`
- **`api/users.php`**: ดึงรายชื่อสมาชิกทั้งหมด
- **`server.py`**: ไพธอนเซิร์ฟเวอร์สำรอง (Port 8089) เชื่อมต่อ MySQL ด้วย `pymysql`

### 5. ระบบส่งอีเมล (PHPMailer & Email Marketing)
- **`PHPMailer/`**: ไลบรารีส่งอีเมล (`src/PHPMailer.php`, `src/SMTP.php`, `src/Exception.php`)
- **`sendMail.php`**: สคริปต์ส่งอีเมลยืนยันการ Subscribe พร้อมรูปแบนเนอร์และโค้ดลด `WELCOME10`
- **`emailContent.php`**: เทมเพลตเนื้อหา HTML สำหรับการ Subscribe (ใช้ Embedded Image CID)
- **`sendPersonalizedMail.php`**: สคริปต์ส่งอีเมลแนะนำสินค้าเฉพาะบุคคลตามรสชาติที่เลือก (มอบโค้ดลด 15%)
- **`sendMemberWelcomeMail.php`**: ฟังก์ชันส่งอีเมลต้อนรับสมาชิกใหม่ ระบุชื่อจริงและรหัสสมาชิกอัตโนมัติ

---

## 🎯 แผนงานการตลาดดิจิทัล 5 ขั้นตอน (5-Step Roadmap)

```
[1] Subscribe หน้าแรก ──> [2] PHP ส่งเมลหลัง Subscribe (Embedded CID)
[3] Personalized Marketing ทางอีเมล (ตามรสชาติที่ชอบ)
[4] PHP ส่งเมลหลังสมัครสมาชิก (ดึงชื่อจาก Database)
[5] ระบบแนะนำสินค้าบนเว็บ (วิเคราะห์จากพฤติกรรมจริง & สินค้าในตะกร้า)
```

### 1️⃣ ระบบ Subscribe ในหน้าแรก
- มีฟอร์มกรอกอีเมลใน [index.html](file:///c:/xampp/htdocs/marketing/index.html) และหน้า [subscribe_form.php](file:///c:/xampp/htdocs/marketing/subscribe_form.php)
- ส่งข้อมูลแบบ `POST` ไปยัง `sendMail.php`

### 2️⃣ ส่งอีเมลหลัง Subscribe
- ใช้ PHPMailer ต่อ Gmail SMTP (Port 587, STARTTLS, App Password 16 หลัก)
- แนบรูปภาพแบนเนอร์แบบ **Embedded Image (CID)**:
  ```php
  $mail->addEmbeddedImage($path, 'promo_poster');
  ```
  ใน HTML: `<img src="cid:promo_poster">`
- บันทึกอีเมลลงไฟล์ `subscribers.txt`

### 3️⃣ Personalized Marketing ตามความชอบ
- เข้าใช้งานผ่าน [personalized_marketing.php](file:///c:/xampp/htdocs/marketing/personalized_marketing.php) หรือเมนู Navbar **"🎯 แนะนำเฉพาะคุณ"**
- ให้เลือกรสชาติที่สนใจ (สไปซี่, ดั้งเดิม, บาร์บีคิว, วาซาบิ)
- ดึงชื่อและอีเมลของบัญชีที่กำลังล็อกอินอยู่ ณ ขณะนั้นในเบื้องหลังโดยอัตโนมัติ (ไม่ต้องกรอกเอง)
- [sendPersonalizedMail.php](file:///c:/xampp/htdocs/marketing/sendPersonalizedMail.php) จะแนบรูปสินค้ารสชาตินั้น และมอบโค้ดลดพิเศษ 15% ตรงไปยังอีเมลสมาชิก

### 4️⃣ ส่งอีเมลต้อนรับหลังสมัครสมาชิก
- เมื่อผู้ใช้สมัครสมาชิกใหม่ที่ [register.html](file:///c:/xampp/htdocs/marketing/register.html)
- [api/register.php](file:///c:/xampp/htdocs/marketing/api/register.php) จะบันทึกสมาชิกลง MySQL และเรียกฟังก์ชัน `sendMemberWelcomeEmail()` ใน [sendMemberWelcomeMail.php](file:///c:/xampp/htdocs/marketing/sendMemberWelcomeMail.php)
- ส่งอีเมลต้อนรับพร้อมแนบรูป `member_welcome.jpg` และระบุชื่อจริงของสมาชิก เช่น *"สวัสดี คุณสมชาย ใจดี"* พร้อมแจ้งรหัสสมาชิกและสิทธิประโยชน์

### 5️⃣ ระบบแนะนำสินค้าจากพฤติกรรมผู้ใช้ (Behavior-Based Recommendations)
- ทำงานผ่าน [app.js](file:///c:/xampp/htdocs/marketing/app.js) และแสดงผลบน [products.html](file:///c:/xampp/htdocs/marketing/products.html) และ [cart.html](file:///c:/xampp/htdocs/marketing/cart.html)
- บันทึกพฤติกรรมผู้ใช้ลง `localStorage` ผ่าน `recordUserBehavior()` เมื่อคลิกดูสินค้าหรือเลือกรสชาติ
- กฎการแนะนำ (Recommendation Rules):
  1. **Frequently Bought Together**: ถ้ามีสินค้าในตะกร้า จะแนะนำสินค้าหมวดหมู่อื่นที่ทานคู่กัน
  2. **Recently Viewed**: ถ้ามีการดูสินค้า จะดึงสินค้าที่เพิ่งเปิดดูและรสชาติที่เกี่ยวข้องมาแสดง
  3. **Best Sellers**: หากเป็นผู้ใช้ใหม่ จะแนะนำสินค้ายอดนิยมอันดับ 1 ของแบรนด์

---

## ⚙️ การตั้งค่าระบบและการรัน (Execution & Setup)

### 1. การรันผ่าน XAMPP (แนะนำที่สุด)
1. เปิด **XAMPP Control Panel**
2. กด **Start** ที่โมดูล **Apache** และ **MySQL**
3. เข้าใช้งานผ่านเบราว์เซอร์:
   - หน้าแรก: `http://localhost/marketing/index.html`
   - สินค้าทั้งหมด: `http://localhost/marketing/products.html`
   - แนะนำเฉพาะคุณ: `http://localhost/marketing/personalized_marketing.php`
   - ฟอร์ม Subscribe: `http://localhost/marketing/subscribe_form.php`
   - phpMyAdmin: `http://localhost/phpmyadmin` (ฐานข้อมูล `grobgrob_db`)

### 2. การตั้งค่า Gmail SMTP ใน PHPMailer
ในไฟล์ส่งอีเมล (`sendMail.php`, `sendPersonalizedMail.php`, `sendMemberWelcomeMail.php`):
```php
$mail->isSMTP();
$mail->Host = 'smtp.gmail.com';
$mail->SMTPAuth = true;
$mail->Username = 'your_email@gmail.com';     // Gmail ผู้ส่ง
$mail->Password = 'xxxx xxxx xxxx xxxx';    // App Password 16 หลัก
$mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
$mail->Port = 587;
```
*(ต้องเปิด 2-Step Verification ใน Google Account ก่อนสร้าง App Password)*
