<?php
// resendHelper.php - ระบบส่งอีเมลผ่าน Cloud HTTPS API (Brevo API + Resend API)

if (file_exists(__DIR__ . '/config.local.php')) {
    include_once __DIR__ . '/config.local.php';
}

function sendViaResendAPI($toEmail, $subject, $htmlContent) {
    // 1. ลองส่งผ่าน Brevo API ก่อน (ส่งได้ทุกอีเมลทั่วโลก ไม่จำกัดโดเมน)
    $brevoKey = getenv('BREVO_API_KEY');
    if (!empty($brevoKey)) {
        $ch = curl_init('https://api.brevo.com/v3/smtp/email');
        $payload = [
            'sender' => ['name' => '🌿 GrobGrob Seaweed (กรอบกรอบ)', 'email' => 'kukongkaka@gmail.com'],
            'to' => [['email' => trim($toEmail)]],
            'subject' => $subject,
            'htmlContent' => $htmlContent
        ];
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_USERAGENT, 'Brevo-PHP/1.0');
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'api-key: ' . $brevoKey,
            'Content-Type: application/json'
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
        curl_setopt($ch, CURLOPT_TIMEOUT, 6);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($httpCode >= 200 && $httpCode < 300) {
            return true;
        }
    }

    // 2. สำรองด้วย Resend API
    $resendKey = getenv('RESEND_API_KEY');
    if (!empty($resendKey)) {
        $url = 'https://api.resend.com/emails';
        $primaryRecipient = trim($toEmail);
        $verifiedAccountEmail = 'kukongkaka@gmail.com';

        $postToResend = function($recipient, $subj, $body) use ($url, $resendKey) {
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
                'Authorization: Bearer ' . $resendKey,
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

        $res = $postToResend($primaryRecipient, $subject, $htmlContent);
        if ($res['code'] >= 200 && $res['code'] < 300) {
            return true;
        }

        if (strcasecmp($primaryRecipient, $verifiedAccountEmail) !== 0) {
            $forwardNotice = "<div style='background:#FFF3CD; padding:12px 16px; border-radius:8px; margin-bottom:16px; color:#856404; font-family:sans-serif;'>
                <strong>🔔 [GrobGrob Notification]</strong> อีเมลฉบับนี้ถูกส่งถึง: <code>{$primaryRecipient}</code> (ส่งต่อเข้ากล่องข้อความของคุณสำหรับการทดสอบระบบ)
            </div>";
            $fallbackRes = $postToResend($verifiedAccountEmail, "[ถึง: {$primaryRecipient}] {$subject}", $forwardNotice . $htmlContent);
            return ($fallbackRes['code'] >= 200 && $fallbackRes['code'] < 300);
        }
    }

    return false;
}
