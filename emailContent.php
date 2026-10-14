<?php
// emailContent.php - เทมเพลตเนื้อหาอีเมลส่งถึงลูกค้าที่ Subscribe
// ออกแบบสำหรับแบรนด์ GrobGrob (สาหร่ายอบกรอบแท้ 100%)
// มีการแสดงรูปภาพแบบ Embedded Image ผ่าน CID: <img src="cid:promo_poster">

$bodyContent = '
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ขอบคุณที่สมัครรับข่าวสาร GrobGrob</title>
</head>
<body style="margin: 0; padding: 0; background-color: #FAF2E6; font-family: \'Prompt\', Tahoma, Arial, sans-serif; color: #2B2B26;">
  <center style="width: 100%; table-layout: fixed; background-color: #FAF2E6; padding: 30px 0;">
    <table align="center" style="width: 600px; max-width: 600px; background-color: #FFFFFF; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(46, 58, 31, 0.1); border-spacing: 0;">
      
      <!-- 1. รูปภาพโปสเตอร์โปรโมชั่น / สินค้าแนะนำ -->
      <tr>
        <td align="center" style="background-color: #FFFFFF; padding: 0;">
          <img src="https://kunano55.github.io/marketing/email_design/subscribe_newsletter.jpg" alt="GrobGrob โปสเตอร์สินค้าแนะนำ" style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />
        </td>
      </tr>

      <!-- 2. ส่วนข้อความต้อนรับ -->
      <tr>
        <td style="padding: 36px 32px; text-align: center;">
          <span style="background-color: #EBF2D5; color: #445926; font-weight: bold; font-size: 13px; padding: 6px 14px; border-radius: 20px; display: inline-block; margin-bottom: 12px;">
            🌱 HEALTHY & CRISPY SNACK
          </span>
          <h1 style="color: #2E3A1F; font-size: 24px; margin: 0 0 12px 0;">ยินดีต้อนรับสู่ครอบครัว GrobGrob! 🎉</h1>
          <p style="color: #5C5C54; font-size: 15px; line-height: 1.6; margin: 0 0 24px 0;">
            ขอบคุณที่สมัครรับข่าวสารกับ <strong>GrobGrob (กรอบกรอบ)</strong> สาหร่ายอบกรอบแท้ 100% ไม่ใช้น้ำมันทอด ไร้สารกันเสีย ไร้ MSG!<br/>
            คุณจะได้รับอัปเดตสินค้าใหม่ รสชาติพิเศษ และสิทธิประโยชน์ก่อนใครส่งตรงถึงอีเมลนี้
          </p>

          <!-- กล่องคูปองส่วนลดพิเศษ -->
          <div style="background-color: #FFF8EC; border: 2px dashed #6E8B3D; border-radius: 16px; padding: 20px; margin: 0 auto 28px auto; max-width: 440px;">
            <p style="color: #6E8B3D; font-size: 13px; font-weight: bold; margin: 0 0 4px 0; text-transform: uppercase; letter-spacing: 1px;">
              🎁 โค้ดส่วนลดต้อนรับสมาชิกใหม่
            </p>
            <div style="font-size: 28px; font-weight: bold; color: #2E3A1F; letter-spacing: 3px; margin: 6px 0;">
              WELCOME10
            </div>
            <p style="color: #666; font-size: 13px; margin: 0;">
              ใช้เป็นส่วนลด 10% สำหรับทุกคำสั่งซื้อที่หน้าชำระเงิน
            </p>
          </div>

          <!-- สินค้าแนะนำไฮไลต์ 3 หมวดหมู่ -->
          <h3 style="color: #2E3A1F; font-size: 18px; margin: 0 0 16px 0; text-align: left; border-bottom: 2px solid #EBF2D5; padding-bottom: 8px;">
            ✨ สินค้าไฮไลต์ที่คุณไม่ควรพลาด:
          </h3>
          <table width="100%" style="border-spacing: 10px; margin-bottom: 24px;">
            <tr>
              <td width="33%" style="background-color: #FAF2E6; padding: 14px; border-radius: 12px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 6px;">🍘</div>
                <strong style="font-size: 14px; color: #2E3A1F;">สาหร่ายแผ่น</strong>
                <p style="font-size: 12px; color: #666; margin: 4px 0 0 0;">กรอบ บางสะใจ 4 รสชาติ</p>
              </td>
              <td width="33%" style="background-color: #FAF2E6; padding: 14px; border-radius: 12px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 6px;">🥢</div>
                <strong style="font-size: 14px; color: #2E3A1F;">สาหร่ายม้วน</strong>
                <p style="font-size: 12px; color: #666; margin: 4px 0 0 0;">เคี้ยวเพลิน เต็มคำ ไม่เลอะมือ</p>
              </td>
              <td width="33%" style="background-color: #FAF2E6; padding: 14px; border-radius: 12px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 6px;">🍚</div>
                <strong style="font-size: 14px; color: #2E3A1F;">สาหร่ายโรยข้าว</strong>
                <p style="font-size: 12px; color: #666; margin: 4px 0 0 0;">ผสมงาหอม เพิ่มรสชาติทุกมื้อ</p>
              </td>
            </tr>
          </table>

          <!-- ปุ่ม CTA เลือกซื้อสินค้า -->
          <a href="https://grobgrob.com/products" target="_blank" style="background-color: #2E3A1F; color: #FFF8EC; text-decoration: none; padding: 14px 36px; font-size: 16px; font-weight: bold; border-radius: 999px; display: inline-block; box-shadow: 0 4px 15px rgba(46, 58, 31, 0.2);">
            🛒 ไปเลือกซื้อสินค้า GrobGrob เลย
          </a>
        </td>
      </tr>

      <!-- 3. ส่วนท้าย Footer -->
      <tr>
        <td style="background-color: #2E3A1F; color: #FFF8EC; padding: 24px 32px; text-align: center; font-size: 12px; line-height: 1.6;">
          <p style="margin: 0 0 6px 0; font-size: 14px; font-weight: bold;">GrobGrob Co., Ltd. (บริษัท กรอบกรอบ จำกัด)</p>
          <p style="margin: 0 0 10px 0; color: #D6E3B8;">กรอบอร่อยเพลิน เคี้ยวสนุกทุกคำ สาหร่ายอบกรอบแท้ 100%</p>
          <p style="margin: 0; color: #9AB273; font-size: 11px;">
            คุณได้รับอีเมลนี้เนื่องจากสมัครรับข่าวสารผ่านเว็บไซต์ GrobGrob<br/>
            หากต้องการยกเลิกการรับข่าวสาร สามารถคลิก <a href="#" style="color: #FFF8EC; text-decoration: underline;">ยกเลิกการติดตาม</a> ได้ทุกเมื่อ
          </p>
        </td>
      </tr>

    </table>
  </center>
</body>
</html>
';
?>
