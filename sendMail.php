<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

// โหลดไฟล์ PHPMailer class
require 'PHPMailer/src/PHPMailer.php';
require 'PHPMailer/src/SMTP.php';
require 'PHPMailer/src/Exception.php';

// ตรวจสอบการส่งข้อมูลผ่าน POST ที่ส่งจากฟอร์ม subscribe
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
    if ($email) {
        $mail = new PHPMailer(true);
        try {
            // ตั้งค่าการเข้ารหัสภาษาไทย
            $mail->CharSet = 'UTF-8';
            $mail->Encoding = 'base64';

            // ตั้งค่า SMTP ของ Gmail
            $mail->isSMTP();
            $mail->Host = 'smtp.gmail.com';
            $mail->SMTPAuth = true;

            // ==========================================================
            // ⚠️ กำหนดค่าบัญชี Gmail ของผู้ส่ง (ให้นักศึกษากรอกข้อมูลส่วนนี้)
            // ==========================================================
            $senderEmail = 'noobzaza77@gmail.com';         // ระบุอีเมล Gmail ผู้ส่ง
            $appPassword = 'qucg hixg pgui crnu';    // ใช้ App Password 16 หลักจาก Google Account

            $mail->Username = $senderEmail;
            $mail->Password = $appPassword;
            $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
            $mail->Port = 587;

            // กำหนดชื่อผู้ส่งแสดงใน inbox ผู้รับ เป็น ชื่อร้านค้า
            $mail->setFrom($senderEmail, '🌿 GrobGrob Shop (สาหร่ายอบกรอบ)');

            // อีเมลผู้รับ (รับตัวแปรจากฟอร์ม subscribe)
            $mail->addAddress($email);

            // แนบรูปภาพสินค้าแนะนำสำหรับลูกค้าใหม่ (Embedded Image ด้วย CID)
            $posterPath = __DIR__ . '/email_design/subscribe_newsletter.jpg';
            if (file_exists($posterPath)) {
                $mail->addEmbeddedImage($posterPath, 'promo_poster', 'subscribe_newsletter.jpg', 'base64', 'image/jpeg', 'inline');
            } elseif (file_exists(__DIR__ . '/assets/seaweed-sheet.png')) {
                $mail->addEmbeddedImage(__DIR__ . '/assets/seaweed-sheet.png', 'promo_poster', 'seaweed-sheet.png', 'base64', 'image/png', 'inline');
            }

            // บรรทัดที่ 25: ดึงเนื้อหา HTML จากไฟล์ emailContent.php
            include "emailContent.php";

            $mail->isHTML(true);

            // กำหนดหัวข้อหลักแสดงใน inbox ผู้รับ
            $mail->Subject = 'ยินดีต้อนรับสู่ GrobGrob! รับโค้ดส่วนลดพิเศษ 10% ทันที';
            $mail->AltBody = "ยินดีต้อนรับสู่ GrobGrob สาหร่ายอบกรอบแท้ 100%!\nขอบคุณที่สมัครรับข่าวสารกับเรา\nโค้ดส่วนลดของคุณ: WELCOME10 (รับส่วนลด 10%)\nเลือกซื้อสินค้า: https://grobgrob.com/products";
            $mail->Body    = $bodyContent;
            $mail->addCustomHeader('X-Mailer', 'GrobGrob Newsletter');
            $mail->addCustomHeader('Precedence', 'bulk');

            // ส่งอีเมล
            $mail->send();

            // บันทึกอีเมลผู้ติดตามลงไฟล์ subscribers.txt
            file_put_contents("subscribers.txt", date('Y-m-d H:i:s') . " - " . $email . "\n", FILE_APPEND);

            // แสดงผลตอบกลับ
            echo "
            <!DOCTYPE html>
            <html lang='th'>
            <head>
              <meta charset='UTF-8'>
              <meta name='viewport' content='width=device-width, initial-scale=1.0'>
              <title>Subscription สำเร็จ - GrobGrob</title>
              <link rel='stylesheet' href='style.css'>
            </head>
            <body style='background-color: #FAF2E6; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; font-family: sans-serif;'>
              <div style='background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); text-align: center; max-width: 480px; width: 90%;'>
                <div style='font-size: 3.5rem; margin-bottom: 12px;'>🎉</div>
                <h2 style='color: #2E3A1F; margin-bottom: 10px;'>✔ Subscription สำเร็จ!</h2>
                <p style='color: #555; line-height: 1.6; margin-bottom: 24px;'>
                  คุณจะได้รับข้อเสนอพิเศษและโค้ดส่วนลดทางอีเมล: <br/><strong style='color: #445926;'>$email</strong>
                </p>
                <div style='display: flex; gap: 10px; justify-content: center;'>
                  <a href='index.html' class='btn-primary' style='display: inline-block; padding: 12px 24px; background: #2E3A1F; color: white; text-decoration: none; border-radius: 999px;'>
                    🏠 กลับสู่หน้าหลัก
                  </a>
                  <a href='subscribe_form.php' style='display: inline-block; padding: 12px 24px; background: #EBF2D5; color: #2E3A1F; text-decoration: none; border-radius: 999px; font-weight: bold;'>
                    ✉️ ฟอร์ม Subscribe
                  </a>
                </div>
              </div>
            </body>
            </html>
            ";

        } catch (Exception $e) {
            echo "
            <!DOCTYPE html>
            <html lang='th'>
            <head>
              <meta charset='UTF-8'>
              <title>เกิดข้อผิดพลาด</title>
            </head>
            <body style='padding: 40px; font-family: sans-serif;'>
              <h2 style='color: #c0392b;'>❌ เกิดข้อผิดพลาด : ไม่สามารถส่งอีเมลถึงคุณได้</h2>
              <p>สาเหตุ: {$mail->ErrorInfo}</p>
              <p>คำแนะนำ: ตรวจสอบว่าได้กรอก Gmail และ App Password 16 หลักถูกต้องใน <code>sendMail.php</code> หรือยัง</p>
              <br/>
              <a href='javascript:history.back()'>⬅ ย้อนกลับไปแก้ไข</a>
            </body>
            </html>
            ";
        }
    } else {
        echo "⚠ ไม่มีอีเมลล์นี้หรือไม่ถูกต้อง";
    }
} else {
    echo "Access Denied.";
}
?>