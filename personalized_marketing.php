<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>แนะนำสินค้าเฉพาะคุณ (Personalized Marketing) - GrobGrob</title>
  <link rel="stylesheet" href="style.css?v=6" />
  <link rel="icon" type="image/png" href="assets/logo.png" />
  <style>
    body {
      background-color: #FAF2E6;
      min-height: 100vh;
    }
    .pers-container {
      max-width: 680px;
      margin: 40px auto;
      padding: 0 20px;
    }
    .pers-card {
      background: #FFFFFF;
      border-radius: 24px;
      padding: 40px;
      box-shadow: 0 16px 40px rgba(46, 58, 31, 0.08);
      border: 1px solid rgba(110, 139, 61, 0.15);
    }
    .flavor-option-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
      margin: 16px 0 24px 0;
    }
    .flavor-radio-card {
      border: 2px solid #E5E1D8;
      border-radius: 14px;
      padding: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .flavor-radio-card:hover {
      border-color: #6E8B3D;
      background: #FDFBF7;
    }
    .flavor-radio-card.active {
      border-color: #6E8B3D;
      background: #EBF2D5;
      font-weight: bold;
    }
    .flavor-radio-card input {
      display: none;
    }
    .cat-btn-group {
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
    }
    .cat-radio-label {
      flex: 1;
      text-align: center;
      padding: 12px;
      border-radius: 12px;
      border: 2px solid #E5E1D8;
      cursor: pointer;
      font-size: 0.95rem;
      transition: all 0.2s ease;
    }
    .cat-radio-label:hover {
      border-color: #6E8B3D;
    }
    .cat-radio-label.active {
      background: #2E3A1F;
      color: #FFF;
      border-color: #2E3A1F;
      font-weight: bold;
    }
    .cat-radio-label input {
      display: none;
    }
  </style>
</head>
<body>

  <!-- Navbar -->
  <header class="navbar">
    <div class="container nav-container">
      <a href="index.html" class="logo-wrapper">
        <img src="assets/logo.png" alt="GrobGrob โลโก้" class="logo-img" />
      </a>
      <a href="index.html" style="color: #6E8B3D; font-weight: 600; text-decoration: none;">← กลับหน้าแรก</a>
    </div>
  </header>

  <main class="pers-container">
    <div class="pers-card">
      <div style="text-align: center; margin-bottom: 28px;">
        <span style="font-size: 3rem;">🎯</span>
        <h1 style="font-size: 1.8rem; color: #2E3A1F; margin: 8px 0;">แนะนำสินค้าเฉพาะคุณ (Personalized Marketing)</h1>
        <p style="color: #666; font-size: 0.95rem; line-height: 1.6;">
          เลือกรสชาติที่คุณสนใจ ระบบจะจัดส่งข้อเสนอและโค้ดลดพิเศษ 15% ตรงไปยังอีเมลของคุณทันที!
        </p>
      </div>

      <!-- ฟอร์มเลือกความชอบ -->
      <form id="persForm" action="sendPersonalizedMail.php" method="POST">
        <!-- ส่งค่าชื่อและอีเมลของบัญชีที่ล็อกอินอยู่เบื้องหลังโดยอัตโนมัติ -->
        <input type="hidden" id="customerName" name="customerName" value="" />
        <input type="hidden" id="email" name="email" value="" />

        <!-- 1. เลือกหมวดหมู่ -->
        <label style="font-weight: bold; color: #2E3A1F; display: block; margin-bottom: 8px;">1. รูปแบบสาหร่ายที่คุณชอบ:</label>
        <div class="cat-btn-group">
          <label class="cat-radio-label active" style="cursor: pointer;">
            <input type="radio" name="category" value="sheet" checked /> 🍘 สาหร่ายแผ่น
          </label>
          <label class="cat-radio-label" style="cursor: pointer;">
            <input type="radio" name="category" value="roll" /> 🥢 สาหร่ายม้วน
          </label>
          <label class="cat-radio-label" style="cursor: pointer;">
            <input type="radio" name="category" value="flake" /> 🍚 ผงโรยข้าว
          </label>
        </div>

        <!-- 2. เลือกรสชาติ -->
        <label style="font-weight: bold; color: #2E3A1F; display: block; margin-bottom: 8px;">2. เลือกรสชาติที่คุณถูกใจที่สุด:</label>
        <div class="flavor-option-grid">
          <label class="flavor-radio-card active" style="cursor: pointer;">
            <input type="radio" name="flavor" value="spicy" checked />
            <span style="font-size: 1.8rem;">🔥</span>
            <div>
              <div style="color: #2E3A1F;">รสสไปซี่</div>
              <small style="color: #888;">เผ็ดซี้ดสะใจ</small>
            </div>
          </label>

          <label class="flavor-radio-card" style="cursor: pointer;">
            <input type="radio" name="flavor" value="original" />
            <span style="font-size: 1.8rem;">🌿</span>
            <div>
              <div style="color: #2E3A1F;">รสดั้งเดิม</div>
              <small style="color: #888;">หอมธรรมชาติ แคลต่ำ</small>
            </div>
          </label>

          <label class="flavor-radio-card" style="cursor: pointer;">
            <input type="radio" name="flavor" value="bbq" />
            <span style="font-size: 1.8rem;">🍖</span>
            <div>
              <div style="color: #2E3A1F;">รสบาร์บีคิว</div>
              <small style="color: #888;">หอมกลิ่นรมควัน</small>
            </div>
          </label>

          <label class="flavor-radio-card" style="cursor: pointer;">
            <input type="radio" name="flavor" value="wasabi" />
            <span style="font-size: 1.8rem;">🍣</span>
            <div>
              <div style="color: #2E3A1F;">รสวาซาบิ</div>
              <small style="color: #888;">ฉุนจี๊ดขึ้นจมูก</small>
            </div>
          </label>
        </div>

        <button type="submit" id="submitBtn" class="btn-primary" style="width: 100%; padding: 14px; font-size: 1.05rem; border-radius: 12px; justify-content: center; cursor: pointer;">
          <span>🎯 ส่งคำแนะนำสินค้า & โค้ดส่วนลดไปยังอีเมลของฉันทันที</span>
        </button>
      </form>
    </div>
  </main>

  <script src="app.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      // คลิกเลือกหมวดหมู่
      document.querySelectorAll('.cat-radio-label').forEach(label => {
        label.addEventListener('click', function(e) {
          document.querySelectorAll('.cat-radio-label').forEach(l => l.classList.remove('active'));
          this.classList.add('active');
          const radio = this.querySelector('input[type="radio"]');
          if (radio) radio.checked = true;
        });
      });

      // คลิกเลือกรสชาติ
      document.querySelectorAll('.flavor-radio-card').forEach(card => {
        card.addEventListener('click', function(e) {
          document.querySelectorAll('.flavor-radio-card').forEach(c => c.classList.remove('active'));
          this.classList.add('active');
          const radio = this.querySelector('input[type="radio"]');
          if (radio) radio.checked = true;
        });
      });

      // จัดการส่งอีเมลไปยังบัญชีที่ล็อกอินอยู่เบื้องหลัง
      const form = document.getElementById('persForm');
      const customerNameInput = document.getElementById('customerName');
      const emailInput = document.getElementById('email');

      function getCurrentUser() {
        try {
          const saved = localStorage.getItem('grobgrob_current_user');
          return saved ? JSON.parse(saved) : null;
        } catch (e) {
          return null;
        }
      }

      form.addEventListener('submit', (e) => {
        const currentUser = getCurrentUser();

        if (!currentUser || !currentUser.email) {
          e.preventDefault();
          alert('🔒 กรุณาเข้าสู่ระบบก่อน เพื่อให้ระบบส่งข้อเสนอพิเศษตรงไปยังอีเมลของคุณ');
          window.location.href = 'login.html';
          return;
        }

        // กำหนดชื่อและอีเมลของบัญชีที่ล็อกอินอยู่ ส่งไปยัง sendPersonalizedMail.php
        customerNameInput.value = currentUser.fullName || currentUser.username || 'สมาชิก GrobGrob';
        emailInput.value = currentUser.email;
      });
    });
  </script>
</body>
</html>
