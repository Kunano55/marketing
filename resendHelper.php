<?php
// resendHelper.php - ส่งอีเมลผ่าน Resend HTTPS API (Port 443) สำหรับ Cloud & Render

if (file_exists(__DIR__ . '/config.local.php')) {
    include_once __DIR__ . '/config.local.php';
}

function sendViaResendAPI($toEmail, $subject, $htmlContent) {
    $apiKey = getenv('RESEND_API_KEY');
    if (empty($apiKey)) {
        return false;
    }

    $url = 'https://api.resend.com/emails';
    $primaryRecipient = trim($toEmail);
    $verifiedAccountEmail = 'kukongkaka@gmail.com';

    $postToResend = function($recipient, $subj, $body) use ($url, $apiKey) {
        $payload = [
            'from' => 'GrobGrob Seaweed <onboarding@resend.dev>',
            'to' => [$recipient],
            'subject' => $subj,
            'html' => $body
        ];

        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_USERAGENT, 'Resend-PHP/1.0');
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Authorization: Bearer ' . $apiKey,
            'Content-Type: application/json'
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
        curl_setopt($ch, CURLOPT_TIMEOUT, 6);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        return ['code' => $httpCode, 'body' => $response];
    };

    // 1. ลองส่งไปยังผู้รับปลายทาง
    $res = $postToResend($primaryRecipient, $subject, $htmlContent);

    if ($res['code'] >= 200 && $res['code'] < 300) {
        return true;
    }

    // 2. หากผู้รับปลายทางไม่ใช่ verified email บน Resend Free ให้ส่งสำเนาเข้าบัญชีหลัก (kukongkaka@gmail.com) ทันที
    if (strcasecmp($primaryRecipient, $verifiedAccountEmail) !== 0) {
        $forwardNotice = "<div style='background:#FFF3CD; padding:12px 16px; border-radius:8px; margin-bottom:16px; color:#856404; font-family:sans-serif;'>
            <strong>🔔 [GrobGrob Notification]</strong> อีเมลฉบับนี้ถูกส่งถึง: <code>{$primaryRecipient}</code> (ส่งต่อเข้ากล่องข้อความของคุณสำหรับการทดสอบระบบ)
        </div>";
        $fallbackRes = $postToResend($verifiedAccountEmail, "[ถึง: {$primaryRecipient}] {$subject}", $forwardNotice . $htmlContent);
        return ($fallbackRes['code'] >= 200 && $fallbackRes['code'] < 300);
    }

    return false;
}
