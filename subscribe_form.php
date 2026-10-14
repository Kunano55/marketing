<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>สมัครรับข่าวสาร (Subscribe) - GrobGrob</title>
  <link rel="stylesheet" href="style.css" />
  <link rel="icon" type="image/png" href="assets/logo.png" />
  <style>
    body {
      background-color: #FAF2E6;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .subscribe-wrapper {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 40px 20px;
    }
    .subscribe-card {
      background: #FFFFFF;
      border-radius: 24px;
      padding: 44px 36px;
      max-width: 460px;
      width: 100%;
      text-align: center;
      box-shadow: 0 16px 40px rgba(46, 58, 31, 0.08);
      border: 1px solid rgba(110, 139, 61, 0.15);
    }
    .subscribe-icon {
      font-size: 3rem;
      margin-bottom: 12px;
      display: inline-block;
    }
    .subscribe-title {
      font-size: 1.6rem;
      font-weight: 700;
      color: #2E3A1F;
      margin-bottom: 10px;
    }
    .subscribe-desc {
      font-size: 0.95rem;
      color: #5C5C54;
      line-height: 1.6;
      margin-bottom: 28px;
    }
    .subscribe-form-group {
      margin-bottom: 20px;
      text-align: left;
    }
    .subscribe-input {
      width: 100%;
      padding: 14px 18px;
      font-size: 1rem;
      border: 2px solid #E5E1D8;
      border-radius: 12px;
      outline: none;
      transition: all 0.2s ease;
      background: #FAF8F5;
      box-sizing: border-box;
    }
    .subscribe-input:focus {
      border-color: #6E8B3D;
      background: #FFFFFF;
      box-shadow: 0 0 0 4px rgba(110, 139, 61, 0.15);
    }
    .subscribe-submit-btn {
      width: 100%;
      padding: 14px;
      font-size: 1.05rem;
      font-weight: bold;
      color: #FFF8EC;
      background: #E86B43;
      border: none;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 6px 18px rgba(232, 107, 67, 0.25);
    }
    .subscribe-submit-btn:hover {
      background: #D45831;
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(232, 107, 67, 0.35);
    }
    .back-home-link {
      display: inline-block;
      margin-top: 20px;
      color: #6E8B3D;
      font-size: 0.9rem;
      text-decoration: none;
      font-weight: 600;
    }
    .back-home-link:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <!-- Navbar Simple -->
  <header class="navbar">
    <div class="container nav-container" style="justify-content: center;">
      <a href="index.html" class="logo-wrapper">
        <img src="assets/logo.png" alt="GrobGrob โลโก้" class="logo-img" />
      </a>
    </div>
  </header>

  <!-- Subscribe Form Section -->
  <main class="subscribe-wrapper">
    <div class="subscribe-card">
      <span class="subscribe-icon">✉️</span>
      <h1 class="subscribe-title">สมัครรับข่าวสาร</h1>
      <p class="subscribe-desc">
        รับข่าวสารและโปรโมชั่นพิเศษก่อนใคร ส่งตรงไปยังอีเมลของคุณ พร้อมรับโค้ดส่วนลดต้อนรับทันที!
      </p>

      <!-- แบบฟอร์มส่งข้อมูลแบบ POST ไปยัง sendMail.php -->
      <form action="sendMail.php" method="POST">
        <div class="subscribe-form-group">
          <input 
            type="email" 
            name="email" 
            class="subscribe-input" 
            placeholder="กรอกอีเมลของคุณ เช่น you@example.com" 
            required 
          />
        </div>
        <button type="submit" class="subscribe-submit-btn">
          สมัครเลย 🚀
        </button>
      </form>

      <a href="index.html" class="back-home-link">
        ← กลับสู่หน้าหลัก GrobGrob
      </a>
    </div>
  </main>

  <!-- Footer Simple -->
  <footer class="footer" style="padding: 20px 0;">
    <div class="container text-center">
      <p style="font-size: 0.85rem; color: #777;">&copy; 2026 GrobGrob Co., Ltd. All Rights Reserved.</p>
    </div>
  </footer>

</body>
</html>
