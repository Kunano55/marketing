<?php
// sendOrderConfirmationMail.php - ส่งอีเมลยืนยันคำสั่งซื้อพร้อมสรุปรายการสินค้าและกำหนดเวลาส่งถึงลูกค้า
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require_once __DIR__ . '/PHPMailer/src/PHPMailer.php';
require_once __DIR__ . '/PHPMailer/src/SMTP.php';
require_once __DIR__ . '/PHPMailer/src/Exception.php';

function thaiDate($timestamp) {
    $thai_months = [
        1 => 'มกราคม', 2 => 'กุมภาพันธ์', 3 => 'มีนาคม', 4 => 'เมษายน',
        5 => 'พฤษภาคม', 6 => 'มิถุนายน', 7 => 'กรกฎาคม', 8 => 'สิงหาคม',
        9 => 'กันยายน', 10 => 'ตุลาคม', 11 => 'พฤศจิกายน', 12 => 'ธันวาคม'
    ];
    $day = date('j', $timestamp);
    $month = $thai_months[(int)date('n', $timestamp)];
    $year = (int)date('Y', $timestamp) + 543;
    return "$day $month $year";
}

function sendOrderConfirmationEmail($orderData) {
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
        $mail->Timeout = 3;

        $mail->setFrom($senderEmail, '🌿 GrobGrob Shop (คำสั่งซื้อ)');
        
        $customerEmail = $orderData['customerEmail'];
        $customerName  = $orderData['customerName'] ?? 'ลูกค้าคนพิเศษ';
        $mail->addAddress($customerEmail, $customerName);

        // วันที่สั่งซื้อ และวันที่คาดว่าจะได้รับสินค้า (2 - 3 วัน)
        $now = time();
        $orderDateStr = thaiDate($now);
        $minDays = 2;
        $maxDays = 3;
        $estMinDate = thaiDate(strtotime("+$minDays days", $now));
        $estMaxDate = thaiDate(strtotime("+$maxDays days", $now));

        $orderNo = $orderData['orderNo'] ?? ('ORD-' . date('Ymd-His'));
        $items = $orderData['items'] ?? [];
        $subtotal = number_format((float)($orderData['subtotal'] ?? 0), 2);
        $shippingFee = (float)($orderData['shippingFee'] ?? 0);
        $shippingStr = $shippingFee <= 0 ? '<span style="color:#2E7D32;font-weight:700;">ฟรี (โปรโมชั่นส่งฟรี)</span>' : number_format($shippingFee, 2) . ' ฿';
        $discountAmount = (float)($orderData['discountAmount'] ?? 0);
        $discountStr = $discountAmount > 0 ? '-' . number_format($discountAmount, 2) . ' ฿' : '0.00 ฿';
        $netAmount = number_format((float)($orderData['netAmount'] ?? 0), 2);
        $shippingAddress = htmlspecialchars($orderData['shippingAddress'] ?? 'จัดส่งตามที่อยู่ที่ระบุไว้ในระบบ');
        $customerPhone = htmlspecialchars($orderData['customerPhone'] ?? '-');

        // รูปภาพแบรนด์/โลโก้ GrobGrob สำหรับแสดงผลในอีเมล
        $logoUrl = 'https://kunano55.github.io/marketing/assets/logo.png';
        $logoPath = __DIR__ . '/assets/logo.png';
        if (file_exists($logoPath)) {
            $mail->addEmbeddedImage($logoPath, 'grob_logo', 'logo.png', 'base64', 'image/png', 'inline');
        }
        $logoHtml = '<img src="' . $logoUrl . '" alt="🌿 GrobGrob" style="max-height: 52px; display: inline-block; border: 0;" />';

        // สร้างตารางรายการสินค้า
        $itemsHtml = '';
        foreach ($items as $idx => $it) {
            $name = htmlspecialchars($it['name'] ?? 'สาหร่ายอบกรอบ GrobGrob');
            $qty = (int)($it['qty'] ?? 1);
            $price = number_format((float)($it['price'] ?? 0), 2);
            $itemSubtotal = number_format((float)(($it['price'] ?? 0) * $qty), 2);
            
            $bgColor = ($idx % 2 === 0) ? '#FFFFFF' : '#F9FBF7';

            $itemsHtml .= "
                <tr style='background-color: {$bgColor}; border-bottom: 1px solid #E5E7EB;'>
                    <td style='padding: 14px 12px; font-size: 14px; color: #222;'>
                        <strong>{$name}</strong>
                        <div style='font-size: 12px; color: #666; margin-top: 3px;'>สาหร่ายอบกรอบแท้ 100% ปราศจากน้ำมันทอด</div>
                    </td>
                    <td style='padding: 14px 12px; text-align: center; font-size: 14px; color: #444;'>{$qty}</td>
                    <td style='padding: 14px 12px; text-align: right; font-size: 14px; color: #444;'>{$price} ฿</td>
                    <td style='padding: 14px 12px; text-align: right; font-size: 14px; font-weight: 700; color: #2D5A27;'>{$itemSubtotal} ฿</td>
                </tr>
            ";
        }

        // หัวข้ออีเมล
        $mail->Subject = "📦 ยืนยันคำสั่งซื้อ #{$orderNo} - สินค้าจะถึงคุณในอีก {$minDays}-{$maxDays} วัน | GrobGrob";

        // HTML Body
        $body = "
<!DOCTYPE html>
<html lang='th'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>ยืนยันคำสั่งซื้อ GrobGrob</title>
</head>
<body style='margin: 0; padding: 0; background-color: #F4F6F0; font-family: -apple-system, BlinkMacSystemFont, \"Sarabun\", \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif; color: #333333;'>
  <div style='max-width: 650px; margin: 30px auto; background-color: #FFFFFF; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #E5EAD7;'>
    
    <!-- Header -->
    <div style='background: linear-gradient(135deg, #2D5A27 0%, #466D38 100%); padding: 32px 24px; text-align: center; color: #FFFFFF;'>
      <div style='margin-bottom: 12px;'>{$logoHtml}</div>
      <h1 style='margin: 0 0 8px 0; font-size: 24px; font-weight: 800; color: #FFFFFF;'>🎉 ขอบคุณสำหรับคำสั่งซื้อของคุณ!</h1>
      <p style='margin: 0; font-size: 15px; color: #E0EED4; line-height: 1.5;'>
        เราได้รับคำสั่งซื้อเรียบร้อยแล้วและกำลังเตรียมจัดส่งสาหร่ายอบกรอบสดใหม่ให้คุณ
      </p>
    </div>

    <!-- ETA Alert Box (Highlight: อีกกี่วันถึงจะได้สินค้า) -->
    <div style='margin: 24px; padding: 20px; background: #FFF9ED; border-radius: 12px; border: 2px dashed #E86B43;'>
      <div style='display: flex; align-items: center; margin-bottom: 10px;'>
        <span style='font-size: 26px; margin-right: 10px;'>🚚</span>
        <div>
          <div style='font-size: 13px; font-weight: 700; color: #C2410C; text-transform: uppercase; letter-spacing: 0.5px;'>
            ประมาณการระยะเวลาจัดส่งถึงคุณ
          </div>
          <div style='font-size: 20px; font-weight: 800; color: #9A3412; margin-top: 2px;'>
            จะได้รับสินค้าในอีก <span style='background: #FFEDD5; padding: 2px 8px; border-radius: 6px;'>{$minDays} - {$maxDays} วันทำการ</span>
          </div>
        </div>
      </div>
      <div style='font-size: 14px; color: #7C2D12; background: #FFFFFF; padding: 12px 14px; border-radius: 8px; margin-top: 8px; border: 1px solid #FED7AA;'>
        📅 <strong>คาดว่าจะถึงมือคุณภายในวันที่:</strong> <span style='font-weight: 700; color: #C2410C;'>{$estMinDate} - {$estMaxDate}</span><br>
        📍 จัดส่งโดยบริการขนส่งด่วนพิเศษ (Express Delivery พร้อมระบบควบคุมความกรอบ)
      </div>
    </div>

    <!-- Order Info Grid -->
    <div style='padding: 0 24px;'>
      <div style='background-color: #F8FAF5; border-radius: 12px; padding: 18px 20px; border: 1px solid #E8EDE2; margin-bottom: 24px;'>
        <table style='width: 100%; border-collapse: collapse; font-size: 14px;'>
          <tr>
            <td style='padding: 6px 0; color: #666; width: 40%;'>เลขที่คำสั่งซื้อ:</td>
            <td style='padding: 6px 0; font-weight: 700; color: #2D5A27;'>#{$orderNo}</td>
          </tr>
          <tr>
            <td style='padding: 6px 0; color: #666;'>วันที่สั่งซื้อ:</td>
            <td style='padding: 6px 0; font-weight: 600; color: #333;'>{$orderDateStr}</td>
          </tr>
          <tr>
            <td style='padding: 6px 0; color: #666;'>ชื่อผู้รับ:</td>
            <td style='padding: 6px 0; font-weight: 600; color: #333;'>{$customerName}</td>
          </tr>
          <tr>
            <td style='padding: 6px 0; color: #666;'>เบอร์โทรศัพท์ติดต่อ:</td>
            <td style='padding: 6px 0; font-weight: 600; color: #333;'>{$customerPhone}</td>
          </tr>
          <tr>
            <td style='padding: 6px 0; color: #666; vertical-align: top;'>ที่อยู่สำหรับจัดส่ง:</td>
            <td style='padding: 6px 0; font-weight: 600; color: #333; line-height: 1.4;'>{$shippingAddress}</td>
          </tr>
        </table>
      </div>
    </div>

    <!-- Items Table (Highlight: สั่งซื้ออะไรไปบ้าง) -->
    <div style='padding: 0 24px 24px 24px;'>
      <h3 style='margin: 0 0 14px 0; font-size: 16px; font-weight: 700; color: #2D5A27; border-bottom: 2px solid #E5EAD7; padding-bottom: 8px;'>
        📋 สรุปรายการสินค้าที่คุณสั่งซื้อ
      </h3>
      
      <table style='width: 100%; border-collapse: collapse; margin-bottom: 20px;'>
        <thead>
          <tr style='background-color: #EEF3E6; color: #2D5A27; font-size: 13px; text-transform: uppercase;'>
            <th style='padding: 10px 12px; text-align: left; border-top-left-radius: 8px;'>สินค้า</th>
            <th style='padding: 10px 12px; text-align: center;'>จำนวน</th>
            <th style='padding: 10px 12px; text-align: right;'>ราคา/ชิ้น</th>
            <th style='padding: 10px 12px; text-align: right; border-top-right-radius: 8px;'>รวม</th>
          </tr>
        </thead>
        <tbody>
          {$itemsHtml}
        </tbody>
      </table>

      <!-- Price Breakdown -->
      <div style='background-color: #FAFBF9; border-radius: 12px; padding: 16px 20px; border: 1px solid #E5EAD7;'>
        <table style='width: 100%; border-collapse: collapse; font-size: 14px;'>
          <tr>
            <td style='padding: 6px 0; color: #666;'>ราคารวมสินค้า:</td>
            <td style='padding: 6px 0; text-align: right; font-weight: 600;'>{$subtotal} ฿</td>
          </tr>
          <tr>
            <td style='padding: 6px 0; color: #666;'>ค่าจัดส่ง:</td>
            <td style='padding: 6px 0; text-align: right; font-weight: 600;'>{$shippingStr}</td>
          </tr>
          <tr>
            <td style='padding: 6px 0; color: #666;'>ส่วนลดพิเศษ:</td>
            <td style='padding: 6px 0; text-align: right; font-weight: 600; color: #2E7D32;'>{$discountStr}</td>
          </tr>
          <tr style='border-top: 2px dashed #D5DDD0;'>
            <td style='padding: 12px 0 4px 0; font-size: 17px; font-weight: 800; color: #2D5A27;'>ยอดชำระสุทธิ:</td>
            <td style='padding: 12px 0 4px 0; text-align: right; font-size: 20px; font-weight: 800; color: #2D5A27;'>{$netAmount} ฿</td>
          </tr>
        </table>
      </div>
    </div>

    <!-- Delivery Process Steps -->
    <div style='padding: 0 24px 24px 24px;'>
      <div style='background: #F4F7EE; border-radius: 12px; padding: 18px; text-align: center;'>
        <div style='font-size: 13px; font-weight: 700; color: #466D38; margin-bottom: 12px;'>ขั้นตอนต่อไปของพัสดุของคุณ:</div>
        <table style='width: 100%; border-collapse: collapse; font-size: 12px; color: #444;'>
          <tr>
            <td style='width: 33.33%; text-align: center; padding: 6px;'>
              <div style='font-size: 22px; margin-bottom: 4px;'>📦</div>
              <strong>1. เตรียมแพ็กสินค้า</strong><br>
              <span style='color: #888;'>กำลังดำเนินการ</span>
            </td>
            <td style='width: 33.33%; text-align: center; padding: 6px;'>
              <div style='font-size: 22px; margin-bottom: 4px;'>🚛</div>
              <strong>2. ขนส่งรับพัสดุ</strong><br>
              <span style='color: #888;'>ภายใน 24 ชม.</span>
            </td>
            <td style='width: 33.33%; text-align: center; padding: 6px;'>
              <div style='font-size: 22px; margin-bottom: 4px;'>🏠</div>
              <strong>3. ส่งถึงบ้านคุณ</strong><br>
              <span style='color: #2D5A27; font-weight:700;'>ภายใน {$minDays}-{$maxDays} วัน</span>
            </td>
          </tr>
        </table>
      </div>
    </div>

    <!-- Footer -->
    <div style='background-color: #273724; padding: 24px; text-align: center; color: #B9C7B6; font-size: 13px;'>
      <p style='margin: 0 0 8px 0; color: #FFFFFF; font-weight: 700;'>🌿 GrobGrob Co., Ltd. - สาหร่ายอบกรอบแท้ 100%</p>
      <p style='margin: 0 0 12px 0; line-height: 1.5;'>
        หากมีข้อสงสัยหรือต้องการเปลี่ยนแปลงข้อมูลจัดส่ง สามารถติดต่อทีมงานได้ที่<br>
        อีเมล: support@grobgrob.com หรือโทร: 02-123-4567 (จันทร์-ศุกร์ 09:00 - 18:00 น.)
      </p>
      <p style='margin: 0; font-size: 11px; color: #7B8C78;'>
        &copy; 2026 GrobGrob Seaweed E-commerce. All Rights Reserved.
      </p>
    </div>

  </div>
</body>
</html>
";

        $mail->isHTML(true);
        $mail->Body    = $body;
        $mail->AltBody = "ขอบคุณสำหรับคำสั่งซื้อ #{$orderNo} จาก GrobGrob!\nสินค้าของคุณจะถูกจัดส่งถึงคุณในอีก {$minDays}-{$maxDays} วันทำการ (ภายใน {$estMinDate} - {$estMaxDate})\nยอดชำระสุทธิ: {$netAmount} บาท\nดูรายละเอียดเพิ่มเติมได้ที่เว็บไซต์ GrobGrob";

        // ลองส่งผ่าน Resend HTTPS API (พอร์ต 443 สำหรับ Cloud / Render)
        require_once __DIR__ . '/resendHelper.php';
        if (function_exists('sendViaResendAPI')) {
            $orderSubject = "📦 ยืนยันคำสั่งซื้อ #{$orderNo} จาก GrobGrob (คาดว่าจะถึงใน {$minDays}-{$maxDays} วันทำการ)";
            if (sendViaResendAPI($customerEmail, $orderSubject, $body)) {
                $logEntry = "[" . date('Y-m-d H:i:s') . "] SENT ORDER EMAIL VIA RESEND API: Order #{$orderNo} to {$customerEmail} ({$customerName}) | Net: {$netAmount} THB\n";
                @file_put_contents(__DIR__ . '/order_emails_log.txt', $logEntry, FILE_APPEND);
                return [
                    'success' => true,
                    'message' => 'ส่งอีเมลยืนยันคำสั่งซื้อสำเร็จ',
                    'orderNo' => $orderNo,
                    'estimatedDays' => "{$minDays}-{$maxDays}",
                    'estimatedDateRange' => "{$estMinDate} - {$estMaxDate}"
                ];
            }
        }

        $mail->send();

        // บันทึก log
        $logEntry = "[" . date('Y-m-d H:i:s') . "] SENT ORDER EMAIL: Order #{$orderNo} to {$customerEmail} ({$customerName}) | Net: {$netAmount} THB | ETA: {$minDays}-{$maxDays} days\n";
        @file_put_contents(__DIR__ . '/order_emails_log.txt', $logEntry, FILE_APPEND);

        return [
            'success' => true,
            'message' => 'ส่งอีเมลยืนยันคำสั่งซื้อสำเร็จ',
            'orderNo' => $orderNo,
            'estimatedDays' => "{$minDays}-{$maxDays}",
            'estimatedDateRange' => "{$estMinDate} - {$estMaxDate}"
        ];
    } catch (Exception $e) {
        $errorMsg = $mail->ErrorInfo;
        $logEntry = "[" . date('Y-m-d H:i:s') . "] FAILED ORDER EMAIL: Order #{$orderNo} to {$customerEmail} | Error: {$errorMsg}\n";
        @file_put_contents(__DIR__ . '/order_emails_log.txt', $logEntry, FILE_APPEND);

        return [
            'success' => false,
            'error' => 'ไม่สามารถส่งอีเมลได้: ' . $errorMsg
        ];
    }
}
