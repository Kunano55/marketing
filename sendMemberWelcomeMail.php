<?php
// sendMemberWelcomeMail.php - ข้อ 4: ส่งอีเมลต้อนรับสมาชิกใหม่พร้อมสินค้าแนะนำตามความชอบ (Personalized EDM)
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require_once __DIR__ . '/PHPMailer/src/PHPMailer.php';
require_once __DIR__ . '/PHPMailer/src/SMTP.php';
require_once __DIR__ . '/PHPMailer/src/Exception.php';

function sendMemberWelcomeEmail($toEmail, $fullName, $userId, $preferredCategory = null, $preferredFlavor = null) {
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

        $mail->setFrom($senderEmail, '🌿 GrobGrob Member Services (กรอบกรอบ)');
        $mail->addAddress($toEmail);

        // 1. หมวดหมู่สินค้า
        $categories = [
            'sheet' => ['name' => 'สาหร่ายอบกรอบแผ่น', 'icon' => '🍘'],
            'roll'  => ['name' => 'สาหร่ายม้วนอบกรอบ', 'icon' => '🥢'],
            'flake' => ['name' => 'สาหร่ายอบกรอบผงโรยข้าว', 'icon' => '🍚']
        ];
        $selectedCat = (!empty($preferredCategory) && isset($categories[$preferredCategory])) 
            ? $categories[$preferredCategory] 
            : $categories['sheet'];

        // 2. รสชาติที่เลือก (ถ้ามี)
        $flavorMap = [
            'spicy' => [
                'title' => 'รสสไปซี่ พริกคั่วเข้มข้น',
                'desc' => 'เผ็ดร้อนจัดจ้าน กลมกล่อมพริกคั่วเข้มข้น รสเด็ดสะใจคนชอบรสจัดจ้าน',
                'coupon' => 'SPICY15',
                'discount' => '15%',
                'badge' => '🔥 SPICY KICK'
            ],
            'original' => [
                'title' => 'รสออริจินัล เกลือทะเลธรรมชาติ',
                'desc' => 'รสชาติต้นตำรับ หอมกลิ่นสาหร่ายแท้ๆ โรยเกลือทะเลเบาๆ สัมผัสความกรอบสดชื่น',
                'coupon' => 'ORIGINAL15',
                'discount' => '15%',
                'badge' => '🌿 100% NATURAL'
            ],
            'bbq' => [
                'title' => 'รสสโมคกี้บาร์บีคิว',
                'desc' => 'หอมกลิ่นรมควันบาร์บีคิวแท้ รสชาติเข้มข้น กลมกล่อม ทานเพลินทุกช่วงเวลา',
                'coupon' => 'BBQ15',
                'discount' => '15%',
                'badge' => '🍢 SMOKY BBQ'
            ],
            'wasabi' => [
                'title' => 'รสวาซาบิ ซี้ดขึ้นจมูก สไตล์ญี่ปุ่นแท้',
                'desc' => 'สัมผัสความจี๊ดจ๊าดสไตล์ญี่ปุ่นแท้ๆ วาซาบิสดฉุนกำลังดี ช่วยเพิ่มความสดชื่นและตื่นตัวในทุกคำ',
                'coupon' => 'WASABI15',
                'discount' => '15%',
                'badge' => '🍣 JAPANESE WASABI'
            ],
            'corncheese' => [
                'title' => 'รสคอร์นชีส หอมหวานละมุน',
                'desc' => 'หอมหวานข้าวโพดผสานชีสเนียนนุ่ม รสละมุนกลมกล่อม ทานง่าย ถูกใจทั้งครอบครัว',
                'coupon' => 'CORN15',
                'discount' => '15%',
                'badge' => '🧀 SWEET CORN CHEESE'
            ],
            'tomyum' => [
                'title' => 'รสต้มยำกุ้ง แซ่บจี๊ดจ๊าด',
                'desc' => 'รสชาติแบบไทยแท้ เปรี้ยว เผ็ด เค็ม ครบรสกลิ่นสมุนไพร ตะไคร้ใบมะกรูดสดชื่น',
                'coupon' => 'TOMYUM15',
                'discount' => '15%',
                'badge' => '🌶️ TOM YUM SPICE'
            ]
        ];

        $hasPersonalized = !empty($preferredFlavor) && isset($flavorMap[$preferredFlavor]);
        $selectedFlavor = $hasPersonalized ? $flavorMap[$preferredFlavor] : null;

        // แนบรูปภาพโปสเตอร์หลักของ GrobGrob
        $bannerPath = __DIR__ . '/email_design/member_welcome.jpg';
        if (file_exists($bannerPath)) {
            $mail->addEmbeddedImage($bannerPath, 'member_welcome_banner', 'member_welcome.jpg', 'base64', 'image/jpeg', 'inline');
        }

        // แนบรูปสินค้าเฉพาะกรณีระบุรสชาติ
        if ($hasPersonalized) {
            $imageRelPath = 'assets/seaweed-sheet.png';
            if ($preferredCategory === 'sheet') {
                if ($preferredFlavor === 'spicy' || $preferredFlavor === 'tomyum') $imageRelPath = 'assets/sheet_spicy.png';
                elseif ($preferredFlavor === 'bbq') $imageRelPath = 'assets/sheet_bbq.png';
                elseif ($preferredFlavor === 'corncheese') $imageRelPath = 'assets/sheet_cheese.png';
                else $imageRelPath = 'assets/seaweed-sheet.png';
            } elseif ($preferredCategory === 'roll') {
                if ($preferredFlavor === 'wasabi') $imageRelPath = 'assets/roll_wasabi.png';
                elseif ($preferredFlavor === 'bbq') $imageRelPath = 'assets/roll_bbq.png';
                elseif ($preferredFlavor === 'spicy' || $preferredFlavor === 'tomyum') $imageRelPath = 'assets/roll_spicy.png';
                else $imageRelPath = 'assets/seaweed-roll.png';
            } else {
                if ($preferredFlavor === 'spicy' || $preferredFlavor === 'tomyum') $imageRelPath = 'assets/flakes_spicy.png';
                elseif ($preferredFlavor === 'bbq' || $preferredFlavor === 'original') $imageRelPath = 'assets/flakes_garlic.png';
                elseif ($preferredFlavor === 'corncheese') $imageRelPath = 'assets/flakes_saltedegg.png';
                else $imageRelPath = 'assets/seaweed-flakes.png';
            }

            $prodFullPath = __DIR__ . '/' . $imageRelPath;
            if (file_exists($prodFullPath)) {
                $mimeType = mime_content_type($prodFullPath) ?: 'image/png';
                $mail->addEmbeddedImage($prodFullPath, 'fav_product', basename($imageRelPath), 'base64', $mimeType, 'inline');
            }
        }

        // ป้องกันไม่ให้ตก Spam
        $mail->addCustomHeader('X-Mailer', 'GrobGrob Member Mailer');
        $mail->addCustomHeader('Precedence', 'bulk');

        $mail->isHTML(true);
        if ($hasPersonalized) {
            $mail->Subject = "ยินดีต้อนรับคุณ {$fullName} สู่ GrobGrob! รับส่วนลด 15% สำหรับ {$selectedCat['name']} {$selectedFlavor['title']}";
            $mail->AltBody = "ยินดีต้อนรับคุณ {$fullName} เข้าสู่ครอบครัว GrobGrob!\nสินค้าแนะนำสำหรับคุณ: {$selectedCat['name']} {$selectedFlavor['title']}\nโค้ดส่วนลดต้อนรับสมาชิก: {$selectedFlavor['coupon']} (ลด 15%)\nโค้ดลดทั่วไป: WELCOME10\nเข้าสู่ระบบ: https://grobgrob.com/products";
        } else {
            $mail->Subject = "ยินดีต้อนรับคุณ {$fullName} เข้าสู่ครอบครัว GrobGrob Family!";
            $mail->AltBody = "ยินดีต้อนรับคุณ {$fullName} เข้าสู่ครอบครัว GrobGrob!\nโค้ดส่วนลดต้อนรับสมาชิก: WELCOME10 (ลด 10% ทุกออเดอร์)\nเข้าสู่ระบบ: https://grobgrob.com/products";
        }

        $personalizedBlock = '';
        if ($hasPersonalized) {
            $personalizedBlock = "
          <!-- 3. ส่วนสินค้าแนะนำตามความชอบเฉพาะบุคคล (Personalized Match) -->
          <table align='center' style='width: 100%; background: #FDFBF7; border: 2px solid #EBF2D5; border-radius: 20px; margin-bottom: 28px; border-collapse: separate;'>
            <tr>
              <td align='center' style='padding: 24px 20px;'>
                <div style='display: inline-block; background-color: #E86B43; color: #FFFFFF; font-size: 12px; font-weight: bold; padding: 4px 14px; border-radius: 999px; margin-bottom: 12px;'>
                  🎯 สินค้าแนะนำตรงใจคุณ (Personalized Pick)
                </div>
                
                <h3 style='font-size: 20px; color: #2E3A1F; margin: 4px 0 8px 0;'>
                  {$selectedCat['icon']} {$selectedCat['name']} - {$selectedFlavor['title']}
                </h3>
                
                <p style='font-size: 14px; color: #666; margin: 0 0 16px 0; line-height: 1.5;'>
                  {$selectedFlavor['desc']}
                </p>

                <!-- Product Showcase Image -->
                <table align='center' style='margin-bottom: 18px;'>
                  <tr>
                    <td align='center' style='background: #FFFFFF; border-radius: 16px; padding: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.06);'>
                      <img src='cid:fav_product' alt='{$selectedFlavor['title']}' width='220' style='max-width: 220px; width: 100%; height: auto; display: block; border-radius: 10px;' />
                    </td>
                  </tr>
                </table>

                <!-- Personalized Coupon Ticket -->
                <table align='center' style='width: 100%; max-width: 440px; background-color: #FFF8EC; border: 2px dashed #E86B43; border-radius: 16px;'>
                  <tr>
                    <td align='center' style='padding: 16px 20px;'>
                      <span style='font-size: 13px; color: #E86B43; font-weight: bold; letter-spacing: 1px;'>
                        🎁 คูปองส่วนลด 15% เฉพาะรสชาติที่คุณชอบ
                      </span>
                      <div style='font-size: 28px; font-weight: bold; color: #2E3A1F; letter-spacing: 3px; margin: 6px 0;'>
                        {$selectedFlavor['coupon']}
                      </div>
                      <span style='font-size: 13px; color: #555;'>
                        รับส่วนลดทันที <strong>15%</strong> เมื่อสั่งซื้อสินค้ารสชาตินี้ในตะกร้าสินค้า
                      </span>
                    </td>
                  </tr>
                </table>

              </td>
            </tr>
          </table>
            ";
        }

        // โค้ดเทมเพลตอีเมล HTML ตามดีไซน์พรีเมียม (อิงตาม member_welcome.jpg และ subscribe_newsletter.jpg)
        $mail->Body = "
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' lang='th'>
<head>
  <meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1.0'/>
  <title>ยินดีต้อนรับสมาชิกใหม่ GrobGrob Family!</title>
  <style type='text/css'>
    body {
      margin: 0;
      padding: 0;
      background-color: #FAF2E6;
      font-family: 'Prompt', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      color: #2B2B26;
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }
    table {
      border-spacing: 0;
      mso-table-lspace: 0pt;
      mso-table-rspace: 0pt;
    }
    td {
      padding: 0;
    }
    img {
      border: 0;
      display: block;
      line-height: 100%;
      outline: none;
      text-decoration: none;
      max-width: 100%;
      height: auto;
    }
    .wrapper {
      width: 100%;
      table-layout: fixed;
      background-color: #FAF2E6;
      padding-top: 30px;
      padding-bottom: 50px;
    }
    .main-table {
      background-color: #FFFFFF;
      margin: 0 auto;
      width: 600px;
      max-width: 600px;
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 14px 40px rgba(46, 58, 31, 0.12);
    }
    .content-padding {
      padding: 32px 36px;
    }
    .cta-btn {
      background-color: #2E3A1F;
      color: #FFF8EC !important;
      font-weight: bold;
      text-decoration: none;
      padding: 16px 36px;
      border-radius: 999px;
      display: inline-block;
      font-size: 16px;
      box-shadow: 0 6px 20px rgba(46, 58, 31, 0.25);
    }
    @media screen and (max-width: 620px) {
      .main-table {
        width: 94% !important;
        border-radius: 16px !important;
      }
      .content-padding {
        padding: 20px !important;
      }
    }
  </style>
</head>
<body>
  <center class='wrapper'>
    <table class='main-table' align='center'>
      
      <!-- 1. Header Banner Image (member_welcome.jpg) -->
      <tr>
        <td align='center' style='background-color: #FFFFFF;'>
          <a href='https://grobgrob.com/products' target='_blank' style='text-decoration: none; display: block;'>
            <img src='cid:member_welcome_banner' alt='ยินดีต้อนรับสมาชิกใหม่! GrobGrob Family' width='600' style='width: 100%; max-width: 600px; height: auto; display: block; border: 0; outline: none;' />
          </a>
        </td>
      </tr>

      <!-- 2. Main Content & Member Greeting -->
      <tr>
        <td class='content-padding' align='center' style='background-color: #FFFFFF; text-align: center;'>
          
          <div style='display: inline-block; background-color: #F6E7CE; color: #2E3A1F; font-size: 12px; font-weight: bold; padding: 5px 16px; border-radius: 999px; margin-bottom: 12px;'>
            ✨ GROBGROB MEMBER EXCLUSIVE
          </div>
          
          <h1 style='font-size: 26px; color: #2E3A1F; margin: 0 0 16px 0; font-weight: bold;'>
            ยินดีต้อนรับ คุณ{$fullName}
          </h1>

          <p style='font-size: 15px; color: #5C5C54; line-height: 1.6; margin: 0 0 28px 0;'>
            บัญชีสมาชิก GrobGrob ของคุณเปิดใช้งานเรียบร้อยแล้วในระบบฐานข้อมูล!<br/>
            เราได้เตรียมข้อเสนอและสิทธิประโยชน์สุดพิเศษไว้ให้คุณเรียบร้อยแล้ว:
          </p>

          {$personalizedBlock}

          <!-- 4. Member Welcome Coupon (GROB10) -->
          <table align='center' style='width: 100%; max-width: 440px; background-color: #F6E7CE; border: 2px dashed #6E8B3D; border-radius: 16px; margin: 0 auto 28px auto;'>
            <tr>
              <td align='center' style='padding: 16px 20px;'>
                <span style='font-size: 13px; color: #6E8B3D; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;'>
                  🏷️ โค้ดส่วนลดต้อนรับสมาชิกใหม่ (ใช้ได้กับทุกสินค้า)
                </span>
                <div style='font-size: 28px; font-weight: bold; color: #2E3A1F; letter-spacing: 3px; margin: 6px 0;'>
                  GROB10
                </div>
                <span style='font-size: 14px; color: #2B2B26;'>
                  ลดทันที 10% ทุกคำสั่งซื้อ | <strong>ส่งฟรี</strong> เมื่อช้อปครบ 150 บาทขึ้นไป
                </span>
              </td>
            </tr>
          </table>

          <!-- 5. Member Benefits Grid (2x2) -->
          <table align='center' style='width: 100%; margin-bottom: 28px; border-collapse: separate; border-spacing: 8px;'>
            <tr>
              <td style='background-color: #FAF2E6; padding: 14px; border-radius: 14px; text-align: left; width: 50%;'>
                <div style='font-size: 18px; margin-bottom: 4px;'>🏷️ <strong>คูปองต้อนรับ 10%</strong></div>
                <div style='font-size: 13px; color: #5C5C54;'>ใช้โค้ด <strong>GROB10</strong> ในตะกร้าสินค้า</div>
              </td>
              <td style='background-color: #FAF2E6; padding: 14px; border-radius: 14px; text-align: left; width: 50%;'>
                <div style='font-size: 18px; margin-bottom: 4px;'>🚚 <strong>ส่งฟรีทั่วไทย</strong></div>
                <div style='font-size: 13px; color: #5C5C54;'>เมื่อมียอดสั่งซื้อครบ 150 บาทขึ้นไป</div>
              </td>
            </tr>
            <tr>
              <td style='background-color: #FAF2E6; padding: 14px; border-radius: 14px; text-align: left; width: 50%;'>
                <div style='font-size: 18px; margin-bottom: 4px;'>⭐ <strong>สะสมแต้มความกรอบ</strong></div>
                <div style='font-size: 13px; color: #5C5C54;'>ทุก 25 บาท รับ 1 พอยต์ แลกของรางวัล</div>
              </td>
              <td style='background-color: #FAF2E6; padding: 14px; border-radius: 14px; text-align: left; width: 50%;'>
                <div style='font-size: 18px; margin-bottom: 4px;'>🎁 <strong>ของขวัญวันเกิด</strong></div>
                <div style='font-size: 13px; color: #5C5C54;'>เซอร์ไพรส์พิเศษส่งตรงในเดือนเกิดของคุณ</div>
              </td>
            </tr>
          </table>

          <!-- 6. สินค้าไฮไลต์ 3 สไตล์ -->
          <h3 style='color: #2E3A1F; font-size: 18px; margin: 0 0 14px 0; text-align: left; border-bottom: 2px solid #EBF2D5; padding-bottom: 8px;'>
            ✨ สินค้าไฮไลต์ที่คุณไม่ควรพลาด:
          </h3>
          <table width='100%' style='border-spacing: 8px; margin-bottom: 28px;'>
            <tr>
              <td width='33%' style='background-color: #FAF2E6; padding: 14px 10px; border-radius: 12px; text-align: center;'>
                <div style='font-size: 26px; margin-bottom: 6px;'>🍘</div>
                <strong style='font-size: 14px; color: #2E3A1F;'>สาหร่ายแผ่น</strong>
                <p style='font-size: 12px; color: #666; margin: 4px 0 0 0;'>กรอบ บางสะใจ 4 รสชาติ</p>
              </td>
              <td width='33%' style='background-color: #FAF2E6; padding: 14px 10px; border-radius: 12px; text-align: center;'>
                <div style='font-size: 26px; margin-bottom: 6px;'>🥢</div>
                <strong style='font-size: 14px; color: #2E3A1F;'>สาหร่ายม้วน</strong>
                <p style='font-size: 12px; color: #666; margin: 4px 0 0 0;'>เคี้ยวเพลิน เต็มคำ ไม่เลอะมือ</p>
              </td>
              <td width='33%' style='background-color: #FAF2E6; padding: 14px 10px; border-radius: 12px; text-align: center;'>
                <div style='font-size: 26px; margin-bottom: 6px;'>🍚</div>
                <strong style='font-size: 14px; color: #2E3A1F;'>สาหร่ายโรยข้าว</strong>
                <p style='font-size: 12px; color: #666; margin: 4px 0 0 0;'>ผสมงาหอม เพิ่มรสชาติทุกมื้อ</p>
              </td>
            </tr>
          </table>

          <!-- 7. Action Button -->
          <table align='center'>
            <tr>
              <td align='center'>
                <a href='https://grobgrob.com/products' target='_blank' class='cta-btn'>
                  🛒 ไปเลือกซื้อสินค้า GrobGrob เลย
                </a>
              </td>
            </tr>
          </table>

        </td>
      </tr>

      <!-- 8. Footer -->
      <tr>
        <td align='center' style='background-color: #2E3A1F; padding: 26px 32px; color: #FFF8EC; font-size: 13px; text-align: center;'>
          <p style='margin: 0 0 8px 0; font-size: 15px; font-weight: bold;'>GrobGrob Co., Ltd. (บริษัท กรอบกรอบ จำกัด)</p>
          <p style='margin: 0 0 10px 0; color: #EBF2D5; font-size: 12px;'>กรอบอร่อยเพลิน เคี้ยวสนุกทุกคำ สาหร่ายอบกรอบแท้ 100% ไร้น้ำมันทอด ไร้ MSG</p>
          <p style='margin: 0; color: #A9C25A; font-size: 11px; line-height: 1.6;'>
            คุณได้รับอีเมลนี้เนื่องจากสมัครสมาชิกบนเว็บไซต์ GrobGrob ด้วยอีเมลนี้<br/>
            หากต้องการความช่วยเหลือติดต่อ: LINE @GrobGrob หรือ โทร 081-234-5678
          </p>
        </td>
      </tr>

    </table>
  </center>
</body>
</html>
";

        $mail->send();
        file_put_contents(__DIR__ . "/member_emails_log.txt", date('Y-m-d H:i:s') . " | Welcome email sent to: $toEmail ($fullName - $userId - Cat: $preferredCategory, Flav: $preferredFlavor)\n", FILE_APPEND);
        return true;
    } catch (Exception $e) {
        file_put_contents(__DIR__ . "/member_emails_log.txt", date('Y-m-d H:i:s') . " | Error sending to $toEmail: " . $mail->ErrorInfo . "\n", FILE_APPEND);
        return false;
    }
}

// หากเรียกไฟล์นี้โดยตรงผ่าน POST สำหรับทดสอบส่ง
if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['email'])) {
    $email = filter_var($_POST['email'], FILTER_VALIDATE_EMAIL);
    $name = trim($_POST['fullName'] ?? 'สมาชิกใหม่');
    $uid = trim($_POST['userId'] ?? 'USER-2026-DEMO');
    $cat = trim($_POST['category'] ?? 'sheet');
    $flav = trim($_POST['flavor'] ?? 'wasabi');

    if ($email) {
        $result = sendMemberWelcomeEmail($email, $name, $uid, $cat, $flav);
        if ($result) {
            echo "✔ ส่งอีเมลต้อนรับสมาชิกพร้อมสินค้าแนะนำไปยัง $email สำเร็จเรียบร้อยแล้ว!";
        } else {
            echo "❌ ไม่สามารถส่งอีเมลต้อนรับได้ กรุณาตรวจสอบการตั้งค่า Gmail";
        }
    } else {
        echo "อีเมลไม่ถูกต้อง";
    }
}
