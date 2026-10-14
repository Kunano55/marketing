<?php
// sendPersonalizedMail.php - ข้อ 3: Personalized Marketing แนะนำสินค้าตามความสนใจส่งไปทางอีเมล
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require_once __DIR__ . '/PHPMailer/src/PHPMailer.php';
require_once __DIR__ . '/PHPMailer/src/SMTP.php';
require_once __DIR__ . '/PHPMailer/src/Exception.php';

header('Content-Type: text/html; charset=utf-8');

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
    $category = $_POST['category'] ?? 'sheet';   // sheet, roll, flake
    $flavor = $_POST['flavor'] ?? 'spicy';       // spicy, original, bbq, wasabi
    $customerName = trim($_POST['customerName'] ?? 'คุณลูกค้าคนพิเศษ');

    if (!$email) {
        echo "<script>alert('กรุณากรอกอีเมลให้ถูกต้อง'); history.back();</script>";
        exit();
    }

    // Mapping ข้อมูลตามความสนใจของลูกค้า
    $flavorData = [
        'original' => [
            'title' => 'รสดั้งเดิม กรอบ หอมสาหร่ายแท้จากธรรมชาติ',
            'desc' => 'คัดสรรสาหร่ายเกรดพรีเมียม อบกรอบด้วยความร้อนพอเหมาะ ไม่ปรุงแต่งเกินจำเป็น แคลอรี่ต่ำ เหมาะกับสายเฮลตี้',
            'badge' => '🌿 NATURAL & HEALTHY',
            'coupon' => 'ORIGINAL15',
            'discount' => '15%',
            'image' => 'assets/seaweed-sheet.png'
        ],
        'spicy' => [
            'title' => 'รสสไปซี่ จัดจ้าน เผ็ดซี๊ดสะใจ!',
            'desc' => 'คลุกเคล้าพริกคั่วสูตรลับเฉพาะ เผ็ดร้อนกำลังดี เคี้ยวเพลิน ยิ่งกินยิ่งตื่นตัว เหมาะสำหรับคนชอบความเผ็ดร้อน',
            'badge' => '🔥 HOT & SPICY',
            'coupon' => 'SPICY15',
            'discount' => '15%',
            'image' => 'assets/sheet_spicy.png'
        ],
        'bbq' => [
            'title' => 'รสบาร์บีคิว เข้มข้น กลิ่นรมควันหอมกรุ่น',
            'desc' => 'รสชาติเข้มข้นกลมกล่อม หอมกลิ่นสโมคกี้บาร์บีคิวสไตล์อเมริกัน เคี้ยวกรุบกรอบ หยุดไม่อยู่',
            'badge' => '🍖 SMOKY BBQ',
            'coupon' => 'BBQ15',
            'discount' => '15%',
            'image' => 'assets/sheet_bbq.png'
        ],
        'wasabi' => [
            'title' => 'รสวาซาบิ ซี้ดขึ้นจมูก สไตล์ญี่ปุ่นแท้',
            'desc' => 'สัมผัสความจี๊ดจ๊าดสไตล์ญี่ปุ่นแท้ๆ วาซาบิสดฉุนกำลังดี ช่วยเพิ่มความสดชื่นและตื่นตัวในทุกคำ',
            'badge' => '🍣 JAPANESE WASABI',
            'coupon' => 'WASABI15',
            'discount' => '15%',
            'image' => 'assets/roll_wasabi.png'
        ]
    ];

    $categoryNames = [
        'sheet' => 'สาหร่ายแผ่นอบกรอบ',
        'roll' => 'สาหร่ายม้วนอบกรอบ',
        'flake' => 'สาหร่ายผงโรยข้าว'
    ];

    $selectedFlavor = $flavorData[$flavor] ?? $flavorData['spicy'];
    $selectedCatName = $categoryNames[$category] ?? 'สาหร่ายอบกรอบ';

    $mail = new PHPMailer(true);

    try {
        $mail->CharSet = 'UTF-8';
        $mail->Encoding = 'base64';

        // ตั้งค่า SMTP ของ Gmail
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com';
        $mail->SMTPAuth = true;

        $senderEmail = 'noobzaza77@gmail.com';
        $appPassword = 'qucg hixg pgui crnu';

        $mail->Username = $senderEmail;
        $mail->Password = $appPassword;
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
        $mail->Port = 587;

        $mail->setFrom($senderEmail, '🌿 GrobGrob Recommendations');
        $mail->addAddress($email);

        // แนบรูปสินค้าเฉพาะบุคคลแบบ Embedded Image (CID)
        $imagePath = __DIR__ . '/' . $selectedFlavor['image'];
        if (!file_exists($imagePath)) {
            $imagePath = __DIR__ . '/assets/seaweed-sheet.png';
        }
        $mimeType = mime_content_type($imagePath) ?: 'image/png';
        $mail->addEmbeddedImage($imagePath, 'recommended_product', basename($imagePath), 'base64', $mimeType, 'inline');

        // ป้องกันไม่ให้ตก Spam: กำหนด Header และ Plain Text Version
        $mail->addCustomHeader('X-Mailer', 'GrobGrob Marketing Mailer');
        $mail->addCustomHeader('Precedence', 'bulk');

        // สร้างเนื้อหาอีเมลแบบ Personalized
        $mail->isHTML(true);
        $mail->Subject = "แนะนำพิเศษสำหรับคุณ: {$selectedCatName} {$selectedFlavor['title']} พร้อมส่วนลด {$selectedFlavor['discount']}";

        // AltBody สำหรับโปรแกรมอ่านเมลและระบบกรองสแปม
        $mail->AltBody = "สินค้าคัดสรรเฉพาะคุณ: {$customerName}\n{$selectedCatName} - {$selectedFlavor['title']}\n{$selectedFlavor['desc']}\nคูปองส่วนลด: {$selectedFlavor['coupon']} (ลด {$selectedFlavor['discount']})\nเข้าชมสินค้า: https://grobgrob.com/products";

        $mail->Body = "
        <!DOCTYPE html>
        <html lang='th'>
        <head>
          <meta charset='UTF-8'>
          <title>สินค้าแนะนำพิเศษสำหรับคุณ</title>
        </head>
        <body style='margin: 0; padding: 0; background-color: #FAF2E6; font-family: Tahoma, Arial, sans-serif; color: #2B2B26;'>
          <center style='padding: 30px 0;'>
            <table align='center' style='width: 600px; max-width: 600px; background-color: #FFFFFF; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border-spacing: 0;'>
              
              <!-- Header -->
              <tr>
                <td align='center' style='background: linear-gradient(135deg, #2E3A1F, #445926); padding: 32px 20px; color: #FFF8EC;'>
                  <span style='background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 999px; font-size: 13px; font-weight: bold;'>
                    {$selectedFlavor['badge']}
                  </span>
                  <h1 style='font-size: 24px; margin: 12px 0 6px 0;'>สินค้าคัดสรรเฉพาะคุณ: {$customerName}</h1>
                  <p style='font-size: 14px; margin: 0; color: #D6E3B8;'>อิงตามความสนใจที่คุณชื่นชอบในหมวดหมู่ {$selectedCatName}</p>
                </td>
              </tr>

              <!-- Product Image Showcase -->
              <tr>
                <td align='center' style='padding: 30px 20px; background-color: #FFFDF9;'>
                  <div style='background: #FFFFFF; border-radius: 16px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); display: inline-block;'>
                    <img src='cid:recommended_product' alt='{$selectedFlavor['title']}' width='280' style='max-width: 280px; width: 100%; height: auto; display: block; border-radius: 12px; border: 0; outline: none;' />
                  </div>
                </td>
              </tr>

              <!-- Details & Coupon -->
              <tr>
                <td style='padding: 0 36px 36px 36px; text-align: center;'>
                  <h2 style='color: #2E3A1F; font-size: 20px; margin: 0 0 10px 0;'>{$selectedCatName} - {$selectedFlavor['title']}</h2>
                  <p style='color: #555; line-height: 1.6; font-size: 14px; margin: 0 0 24px 0;'>
                    {$selectedFlavor['desc']}
                  </p>

                  <!-- Exclusive Personalized Coupon -->
                  <div style='background-color: #FFF8EC; border: 2px dashed #E86B43; border-radius: 16px; padding: 18px; margin: 0 auto 24px auto; max-width: 420px;'>
                    <span style='color: #E86B43; font-size: 12px; font-weight: bold; letter-spacing: 1px;'>🎁 คูปองส่วนลดพิเศษเฉพาะความสนใจของคุณ</span>
                    <div style='font-size: 28px; font-weight: bold; color: #2E3A1F; margin: 6px 0; letter-spacing: 2px;'>
                      {$selectedFlavor['coupon']}
                    </div>
                    <span style='color: #555; font-size: 13px;'>รับส่วนลดทันที <strong>{$selectedFlavor['discount']}</strong> เมื่อสั่งซื้อสินค้ารสชาตินี้</span>
                  </div>

                  <a href='https://grobgrob.com/products' style='background: #E86B43; color: #FFF; text-decoration: none; padding: 14px 36px; font-size: 16px; font-weight: bold; border-radius: 999px; display: inline-block; box-shadow: 0 4px 14px rgba(232,107,67,0.3);'>
                    🛒 สั่งซื้อรสชาตินี้ทันที
                  </a>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style='background-color: #2E3A1F; color: #D6E3B8; padding: 20px; text-align: center; font-size: 12px;'>
                  <p style='margin: 0 0 6px 0; color: #FFF; font-weight: bold;'>GrobGrob - Personalized Marketing System</p>
                  <p style='margin: 0;'>อีเมลนี้ส่งถึงคุณเพื่อแนะนำสินค้าที่ตรงกับความสนใจของคุณ</p>
                </td>
              </tr>

            </table>
          </center>
        </body>
        </html>
        ";

        $mail->send();

        // บันทึกลง personalized_leads.txt
        file_put_contents("personalized_leads.txt", date('Y-m-d H:i:s') . " | $email | $customerName | $category | $flavor\n", FILE_APPEND);

        echo "
        <!DOCTYPE html>
        <html lang='th'>
        <head>
          <meta charset='UTF-8'>
          <title>ส่งคำแนะนำสินค้าสำเร็จ</title>
          <link rel='stylesheet' href='style.css'>
        </head>
        <body style='background-color: #FAF2E6; display: flex; align-items: center; justify-content: center; min-height: 100vh; font-family: sans-serif;'>
          <div style='background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); text-align: center; max-width: 480px;'>
            <div style='font-size: 3.5rem; margin-bottom: 12px;'>🎯</div>
            <h2 style='color: #2E3A1F;'>✔ ส่งคำแนะนำสินค้าเฉพาะบุคคลเรียบร้อย!</h2>
            <p style='color: #555; line-height: 1.6;'>
              ระบบได้ส่งคำแนะนำสินค้า <strong>{$selectedCatName} ({$selectedFlavor['title']})</strong> พร้อมโค้ดส่วนลด <strong>{$selectedFlavor['coupon']}</strong> ไปยังอีเมล <strong>$email</strong> เรียบร้อยแล้ว
            </p>
            <br/>
            <a href='personalized_marketing.php' class='btn-primary' style='padding: 12px 24px; text-decoration: none; border-radius: 999px;'>
              ← ลองเลือกความสนใจใหม่
            </a>
          </div>
        </body>
        </html>
        ";

    } catch (Exception $e) {
        echo "<script>alert('เกิดข้อผิดพลาดในการส่งอีเมล: {$mail->ErrorInfo}'); history.back();</script>";
    }
} else {
    header('Location: personalized_marketing.php');
    exit();
}
