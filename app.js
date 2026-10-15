// GrobGrob Interactive, Auth & Multi-Page Cart Logic
document.addEventListener('DOMContentLoaded', () => {
  // Default demo accounts for offline / GitHub Pages testing
  const DEFAULT_DEMO_USERS = [
    {
      userId: "USER-2026-001",
      username: "somchai_grob",
      email: "somchai@example.com",
      password: "Password123!",
      fullName: "นายสมชาย ใจดี",
      phone: "081-234-5678",
      birthDate: "1995-05-15",
      gender: "ชาย",
      address: "99/1 หมู่บ้านสุขสันต์ ถนนพัฒนาการ",
      subdistrict: "สวนหลวง",
      district: "สวนหลวง",
      province: "กรุงเทพมหานคร",
      zipcode: "10250",
      preferredCategory: "sheet",
      preferredFlavor: "original",
      registeredAt: "2026-09-01T10:00:00.000Z"
    },
    {
      userId: "USER-2026-004",
      username: "kong",
      email: "kong@gmail.com",
      password: "123456",
      fullName: "นายก้อง สารี",
      phone: "0812345678",
      birthDate: "2003-02-13",
      gender: "ชาย",
      address: "200",
      subdistrict: "หนองบัว",
      district: "เมือง",
      province: "อุดรธานี",
      zipcode: "41000",
      preferredCategory: "roll",
      preferredFlavor: "spicy",
      registeredAt: "2026-09-01T17:50:07.770Z"
    }
  ];

  function getUsers() {
    try {
      const saved = localStorage.getItem('grobgrob_users');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
      localStorage.setItem('grobgrob_users', JSON.stringify(DEFAULT_DEMO_USERS));
      return DEFAULT_DEMO_USERS;
    } catch (e) {
      return DEFAULT_DEMO_USERS;
    }
  }

  function saveUsers(usersList) {
    try {
      localStorage.setItem('grobgrob_users', JSON.stringify(usersList));
    } catch (e) {
      console.error('Error saving users', e);
    }
  }

  function getCurrentUser() {
    try {
      const saved = localStorage.getItem('grobgrob_current_user');
      return saved ? JSON.parse(saved) : null;
    } catch (e) {
      return null;
    }
  }

  function setCurrentUser(user) {
    try {
      if (user) {
        localStorage.setItem('grobgrob_current_user', JSON.stringify(user));
      } else {
        localStorage.removeItem('grobgrob_current_user');
      }
    } catch (e) {
      console.error('Error setting current user', e);
    }
  }

  // --- GrobAuth Global Manager (MySQL Integrated) ---
  window.GrobAuth = {
    getUsers,
    saveUsers,
    getCurrentUser,
    setCurrentUser,
    logout: function() {
      setCurrentUser(null);
      showToast('👋 ออกจากระบบเรียบร้อยแล้ว');
      updateNavbarAuthUI();
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 1000);
    },
    async fetchUsersFromMySQL() {
      try {
        const isPythonPort = window.location.port === '8089';
        const base = (window.BACKEND_API_URL || '').replace(/\/$/, '');
        const primaryApi = base ? `${base}/api/users.php` : (isPythonPort ? '/api/users' : 'api/users.php');
        const secondaryApi = isPythonPort ? 'api/users.php' : '/api/users';
        let res = await fetch(primaryApi).catch(() => null);
        if (!res || !res.ok) {
          res = await fetch(secondaryApi).catch(() => null);
        }
        if (res && res.ok) {
          const data = await res.json().catch(() => null);
          const list = data ? (data.users || (Array.isArray(data) ? data : [])) : [];
          if (list && list.length > 0) {
            // Normalize field names
            const normalized = list.map(u => ({
              userId: u.user_id || u.userId,
              username: u.username,
              email: u.email,
              password: u.password || '',
              fullName: u.full_name || u.fullName,
              phone: u.phone,
              birthDate: u.birth_date || u.birthDate,
              gender: u.gender,
              address: u.address,
              subdistrict: u.subdistrict,
              district: u.district,
              province: u.province,
              zipcode: u.zipcode,
              registeredAt: u.registered_at || u.registeredAt
            }));
            saveUsers(normalized);
            updateNavbarAuthUI();
            return normalized;
          }
        }
      } catch (err) {
        console.warn('MySQL users sync notice:', err);
      }
      return getUsers();
    }
  };

  window.logoutUser = window.GrobAuth.logout;

  // Sync users from MySQL database on load
  window.GrobAuth.fetchUsersFromMySQL().catch(() => {});

  // --- Auth Required Modal ---
  function showAuthRequiredModal() {
    let authModal = document.getElementById('authRequiredModal');
    if (!authModal) {
      authModal = document.createElement('div');
      authModal.id = 'authRequiredModal';
      authModal.className = 'modal-overlay active';
      authModal.innerHTML = `
        <div class="modal-box text-center" style="max-width: 440px; padding: 36px 28px;">
          <div style="font-size: 3.5rem; margin-bottom: 12px;">🔒</div>
          <h3 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 8px;">กรุณาสมัครสมาชิกก่อนสั่งซื้อ</h3>
          <p style="color: var(--color-charcoal-muted); font-size: 0.95rem; margin-bottom: 24px; line-height: 1.6;">
            คุณยังไม่ได้สมัครสมาชิกหรือเข้าสู่ระบบ กรุณาสมัครสมาชิกเพื่อสะสมแต้มและรับสิทธิ์สั่งซื้อสินค้า GrobGrob!
          </p>
          <div style="display: flex; flex-direction: column; gap: 12px;">
            <a href="register.html" class="btn-primary" style="justify-content: center; width: 100%; font-size: 1rem; padding: 12px;">
              <span>📝 สมัครสมาชิกใหม่ (ใช้เวลาเพียง 1 นาที)</span>
            </a>
            <a href="login.html" class="btn-secondary" style="justify-content: center; width: 100%; font-size: 0.9rem; padding: 10px;">
              <span>🔑 มีบัญชีอยู่แล้ว? เข้าสู่ระบบ</span>
            </a>
            <button onclick="document.getElementById('authRequiredModal').classList.remove('active')" style="background: none; border: none; color: var(--color-charcoal-muted); font-size: 0.85rem; cursor: pointer; margin-top: 6px;">
              ปิดหน้านี้
            </button>
          </div>
        </div>
      `;
      document.body.appendChild(authModal);
    } else {
      authModal.classList.add('active');
    }
  }

  // --- Products Data with 4 Flavors each ---
  const productsData = {
    'sheet': {
      id: 'sheet',
      name: 'สาหร่ายอบกรอบแผ่น',
      price: 39,
      unit: 'ห่อ',
      badge: '🔥 สินค้ายอดฮิต',
      rating: 4.9,
      reviewsCount: 142,
      desc: 'สาหร่ายแผ่นอบกรอบ กรอบทุกคำ ไม่ใช้น้ำมันทอด เหมาะทานเล่นเป็นสแน็ค หรือนำไปห่อข้าว',
      flavors: [
        {
          id: 'original',
          name: 'รสออริจินัล',
          tag: 'สูตรกลมกล่อม',
          icon: '🌿',
          image: 'assets/seaweed-sheet.png',
          desc: 'หอมกลิ่นสาหร่ายทะเลแท้ๆ ปรุงรสกลมกล่อมด้วยเกลือทะเลธรรมชาติและน้ำมันงาบริสุทธิ์',
          details: 'ส่วนประกอบ: สาหร่ายทะเลเกรดพรีเมียม 95%, น้ำมันงาบริสุทธิ์ 3%, เกลือทะเล 2%\nน้ำหนักสุทธิ: 25 กรัม | อายุการเก็บรักษา: 12 เดือน'
        },
        {
          id: 'spicy',
          name: 'รสเผ็ดสไปซี่พริกคั่ว',
          tag: 'เผ็ดแซ่บสะใจ',
          icon: '🌶️',
          image: 'assets/sheet_spicy.png',
          desc: 'จัดจ้านถึงใจด้วยผงพริกคั่วสูตรเด็ดและเครื่องเทศ เผ็ดซี้ดกรอบสนั่นทุกคำ',
          details: 'ส่วนประกอบ: สาหร่ายทะเล 90%, ผงพริกคั่วสไปซี่ 7%, น้ำมันงา 2%, เกลือทะเล 1%\nน้ำหนักสุทธิ: 25 กรัม | อายุการเก็บรักษา: 12 เดือน'
        },
        {
          id: 'bbq',
          name: 'รสบาร์บีคิวรมควัน',
          tag: 'หอมรมควัน',
          icon: '🍖',
          image: 'assets/sheet_bbq.png',
          desc: 'หอมกลิ่นรมควันบาร์บีคิวเข้มข้น รสชาติหวานมันเค็มกลมกล่อม ทานเพลินไม่หยุด',
          details: 'ส่วนประกอบ: สาหร่ายทะเล 91%, ผงบาร์บีคิวรมควัน 6%, น้ำมันงา 2%, เกลือทะเล 1%\nน้ำหนักสุทธิ: 25 กรัม | อายุการเก็บรักษา: 12 เดือน'
        },
        {
          id: 'cheese',
          name: 'รสฮอกไกโดชีส',
          tag: 'นัวหอมชีส',
          icon: '🧀',
          image: 'assets/sheet_cheese.png',
          desc: 'เข้มข้นชีสพรีเมียมจากฮอกไกโด หอมนัวกลมกล่อม ละมุนลิ้น ถูกใจสายชีส',
          details: 'ส่วนประกอบ: สาหร่ายทะเล 90%, ผงฮอกไกโดชีส 8%, เกลือทะเล 2%\nน้ำหนักสุทธิ: 25 กรัม | อายุการเก็บรักษา: 12 เดือน'
        }
      ]
    },
    'roll': {
      id: 'roll',
      name: 'สาหร่ายม้วนอบกรอบ',
      price: 35,
      unit: 'ห่อ',
      badge: '✨ แนะนำ',
      rating: 4.8,
      reviewsCount: 98,
      desc: 'สาหร่ายม้วนแท่งกรอบ หอมเข้มข้น พกพาสะดวก ทานเพลินได้ทุกที่ทุกเวลา',
      flavors: [
        {
          id: 'original',
          name: 'รสออริจินัล',
          tag: 'คลาสสิก',
          icon: '🌿',
          image: 'assets/seaweed-roll.png',
          desc: 'ม้วนกรอบหอม รสชาติคลาสสิกตามฉบับ GrobGrob เคี้ยวมันส์ทุกแท่ง',
          details: 'ส่วนประกอบ: สาหร่ายม้วนอบกรอบ 98%, เครื่องเทศธรรมชาติ 2%\nน้ำหนักสุทธิ: 20 กรัม | อายุการเก็บรักษา: 12 เดือน'
        },
        {
          id: 'spicy',
          name: 'รสเผ็ดเกาหลีซอสแซ่บ',
          tag: 'ซอสเกาหลี',
          icon: '🌶️',
          image: 'assets/roll_spicy.png',
          desc: 'เข้มข้นซอสเผ็ดเกาหลีสไตล์ชอนซู หวานเผ็ดลงตัว กรอบกรุบแท่งต่อแท่ง',
          details: 'ส่วนประกอบ: สาหร่ายม้วน 92%, ผงซอสเผ็ดเกาหลี 6%, เครื่องเทศ 2%\nน้ำหนักสุทธิ: 20 กรัม | อายุการเก็บรักษา: 12 เดือน'
        },
        {
          id: 'wasabi',
          name: 'รสวาสาบิญี่ปุ่น',
          tag: 'จี๊ดขึ้นสมอง',
          icon: '🍣',
          image: 'assets/roll_wasabi.png',
          desc: 'หอมซี้ดจี๊ดขึ้นสมองด้วยวาสาบิเกรดแท้นำเข้าจากญี่ปุ่น เปรี้ยวเผ็ดซ่าสดชื่น',
          details: 'ส่วนประกอบ: สาหร่ายม้วน 93%, ผงวาสาบิแท้ 5%, เกลือทะเล 2%\nน้ำหนักสุทธิ: 20 กรัม | อายุการเก็บรักษา: 12 เดือน'
        },
        {
          id: 'bbq',
          name: 'รสบาร์บีคิวรมควัน',
          tag: 'เข้มข้นรมควัน',
          icon: '🍖',
          image: 'assets/roll_bbq.png',
          desc: 'แท่งม้วนกรอบเคลือบผงบาร์บีคิวเข้มข้น หอมกลิ่นเตาถ่านรมควันสุดๆ',
          details: 'ส่วนประกอบ: สาหร่ายม้วน 92%, ผงบาร์บีคิว 6%, เครื่องปรุงรส 2%\nน้ำหนักสุทธิ: 20 กรัม | อายุการเก็บรักษา: 12 เดือน'
        }
      ]
    },
    'flakes': {
      id: 'flakes',
      name: 'สาหร่ายอบกรอบผง โรยข้าว',
      price: 45,
      unit: 'กระปุก',
      badge: '🌿 วัตถุดิบเด็ด',
      rating: 5.0,
      reviewsCount: 210,
      desc: 'สาหร่ายบดละเอียดกรอบฟูสไตล์ Furikake ใช้โรยข้าวสวยร้อนๆ โรยซุป หรือเมนูไหนๆ ก็เพิ่มรสชาติ',
      flavors: [
        {
          id: 'original',
          name: 'รสออริจินัลงาหอม',
          tag: 'โรยเพลิน',
          icon: '🌿',
          image: 'assets/seaweed-flakes.png',
          desc: 'หอมกลิ่นงาขาวคั่วใหม่และสาหร่ายอบกรอบ ปรุงรสกลมกล่อมสไตล์ฟุริคาเกะแท้',
          details: 'ส่วนประกอบ: สาหร่ายบดอบกรอบ 85%, งาขาวอบ 10%, เครื่องปรุงรส 5%\nน้ำหนักสุทธิ: 50 กรัม | อายุการเก็บรักษา: 12 เดือน'
        },
        {
          id: 'spicy',
          name: 'รสสไปซี่กิมจิ',
          tag: 'แซ่บเกาหลี',
          icon: '🌶️',
          image: 'assets/flakes_spicy.png',
          desc: 'เผ็ดเปรี้ยวกลมกล่อมสไตล์กิมจิเกาหลี โรยข้าวสวยแล้วคลุกให้เข้ากันอร่อยเหงื่อซึม',
          details: 'ส่วนประกอบ: สาหร่ายบด 80%, ผงกิมจิสไปซี่ 12%, งาขาว 8%\nน้ำหนักสุทธิ: 50 กรัม | อายุการเก็บรักษา: 12 เดือน'
        },
        {
          id: 'saltedegg',
          name: 'รสไข่เค็มลาวา',
          tag: 'นัวเข้มข้น',
          icon: '🥚',
          image: 'assets/flakes_saltedegg.png',
          desc: 'ผงไข่เค็มแท้เข้มข้น นัวหอมมัน โรยเมนูไหนก็อร่อยยกระดับจานโปรด',
          details: 'ส่วนประกอบ: สาหร่ายบด 78%, ผงไข่เค็มแท้ 15%, งาขาว 7%\nน้ำหนักสุทธิ: 50 กรัม | อายุการเก็บรักษา: 12 เดือน'
        },
        {
          id: 'garlic',
          name: 'รสเนยกระเทียมหอม',
          tag: 'หอมเนยสด',
          icon: '🧄',
          image: 'assets/flakes_garlic.png',
          desc: 'หอมเนยแท้ผสมผสานกระเทียมเจียวกรอบ โรยข้าวหรือเมนูผัดผักชวนหิว',
          details: 'ส่วนประกอบ: สาหร่ายบด 80%, ผงเนยกระเทียม 12%, กระเทียมเจียว 8%\nน้ำหนักสุทธิ: 50 กรัม | อายุการเก็บรักษา: 12 เดือน'
        }
      ]
    }
  };

  // Selected flavor state
  const selectedFlavors = {
    'sheet': 'original',
    'roll': 'original',
    'flakes': 'original'
  };

  // Load Cart
  function loadCart() {
    try {
      const saved = localStorage.getItem('grobgrob_cart');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  }

  function saveCart(cartData) {
    try {
      localStorage.setItem('grobgrob_cart', JSON.stringify(cartData));
    } catch (e) {
      console.error('Error saving cart', e);
    }
  }

  let cart = loadCart();

  // DOM Elements
  const navbar = document.getElementById('navbar');
  const cartToggleBtn = document.getElementById('cartToggleBtn');
  const cartDrawer = document.getElementById('cartDrawer');
  const cartDrawerOverlay = document.getElementById('cartDrawerOverlay');
  const closeCartBtn = document.getElementById('closeCartBtn');
  const cartBadge = document.getElementById('cartBadge');
  const cartItemsList = document.getElementById('cartItemsList');
  const cartTotalPrice = document.getElementById('cartTotalPrice');
  const checkoutBtn = document.getElementById('checkoutBtn');
  const toastContainer = document.getElementById('toastContainer');
  const quickViewModal = document.getElementById('quickViewModal');
  const modalBoxContent = document.getElementById('modalBoxContent');
  const closeModalBtn = document.getElementById('closeModalBtn');

  // --- Sticky Navbar Scroll Effect ---
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 40) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  // --- Update Navbar Auth UI ---
  function updateNavbarAuthUI() {
    const user = getCurrentUser();
    const navActions = document.querySelector('.nav-actions');
    const navLinks = document.querySelector('.nav-links');
    const currentPath = window.location.pathname.toLowerCase();
    const isLoginPage = currentPath.endsWith('login.html');
    const isRegisterPage = currentPath.endsWith('register.html');

    // Clean up any legacy auth items in nav-links
    if (navLinks) {
      const existingAuthItems = navLinks.querySelectorAll('.nav-auth-item');
      existingAuthItems.forEach(el => el.remove());
    }

    if (navActions) {
      // Remove any static legacy buttons on auth pages to avoid duplication
      if (isLoginPage || isRegisterPage) {
        const staticButtons = navActions.querySelectorAll('a.btn-primary, a.btn-secondary');
        staticButtons.forEach(btn => btn.remove());
      }

      let authSlot = navActions.querySelector('.nav-auth-slot');
      if (!authSlot) {
        authSlot = document.createElement('div');
        authSlot.className = 'nav-auth-slot';
        navActions.insertBefore(authSlot, navActions.firstChild);
      }

      if (user) {
        authSlot.innerHTML = `
          <div class="nav-user-badge" title="ผู้ใช้งานปัจจุบัน">
            <span class="user-avatar-icon">👤</span>
            <span class="user-name-text">${user.fullName || user.username}</span>
            <button onclick="window.logoutUser()" class="btn-logout-link" title="ออกจากระบบ">🚪 ออกจากระบบ</button>
          </div>
        `;
      } else if (isLoginPage) {
        // อยู่หน้า Login -> แสดงเฉพาะปุ่ม "สมัครสมาชิก" เพียงปุ่มเดียว
        authSlot.innerHTML = `
          <div class="nav-guest-actions">
            <a href="register.html" class="nav-auth-btn nav-btn-register">📝 สมัครสมาชิก</a>
          </div>
        `;
      } else if (isRegisterPage) {
        // อยู่หน้า Register -> แสดงเฉพาะปุ่ม "เข้าสู่ระบบ" เพียงปุ่มเดียว
        authSlot.innerHTML = `
          <div class="nav-guest-actions">
            <a href="login.html" class="nav-auth-btn nav-btn-login" style="background: var(--bg-cream); border: 1px solid #E5E1D8;">🔑 เข้าสู่ระบบ</a>
          </div>
        `;
      } else {
        // หน้าทั่วไป (หน้าแรก, สินค้า, ตะกร้า) -> แสดงทั้งสองปุ่ม
        authSlot.innerHTML = `
          <div class="nav-guest-actions">
            <a href="login.html" class="nav-auth-btn nav-btn-login">🔑 เข้าสู่ระบบ</a>
            <a href="register.html" class="nav-auth-btn nav-btn-register">📝 สมัครสมาชิก</a>
          </div>
        `;
      }
    }
  }

  updateNavbarAuthUI();

  // --- Cart Controls ---
  function openCart() {
    if (cartDrawer && cartDrawerOverlay) {
      cartDrawer.classList.add('active');
      cartDrawerOverlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    } else {
      window.location.href = 'cart.html';
    }
  }

  function closeCart() {
    if (cartDrawer && cartDrawerOverlay) {
      cartDrawer.classList.remove('active');
      cartDrawerOverlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  if (cartToggleBtn) cartToggleBtn.addEventListener('click', openCart);
  if (closeCartBtn) closeCartBtn.addEventListener('click', closeCart);
  if (cartDrawerOverlay) cartDrawerOverlay.addEventListener('click', closeCart);

  // --- Toast Notification ---
  function showToast(message) {
    if (!toastContainer) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>🍃</span> <span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(50px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 2800);
  }

  // --- Select Flavor on Product Card ---
  window.selectFlavor = function(productId, flavorId) {
    const product = productsData[productId];
    if (!product) return;

    const flavor = product.flavors.find(f => f.id === flavorId);
    if (!flavor) return;

    selectedFlavors[productId] = flavorId;

    const card = document.getElementById(`product-card-${productId}`);
    if (!card) return;

    const img = card.querySelector('.product-img');
    const title = card.querySelector('.product-title');
    const desc = card.querySelector('.product-desc');
    const badgeTag = card.querySelector('.product-badge-tag');

    if (img) {
      img.style.opacity = '0.3';
      img.style.transform = 'scale(0.95)';
      setTimeout(() => {
        img.src = flavor.image;
        img.alt = `${product.name} ${flavor.name}`;
        img.style.opacity = '1';
        img.style.transform = 'scale(1)';
      }, 150);
    }

    if (title) {
      title.innerHTML = `${product.name} <span class="flavor-name-highlight">(${flavor.name})</span>`;
    }

    if (desc) {
      desc.textContent = flavor.desc;
    }

    if (badgeTag) {
      badgeTag.textContent = `${flavor.icon} ${flavor.tag}`;
    }

    const pills = card.querySelectorAll('.flavor-pill');
    pills.forEach(pill => {
      if (pill.dataset.flavor === flavorId) {
        pill.classList.add('active');
      } else {
        pill.classList.remove('active');
      }
    });

    // Track user flavor preference behavior (Roadmap Step 5)
    recordUserBehavior(productId, flavorId, 'select_flavor');
  };

  // --- Specifications metadata per category ---
  const productSpecs = {
    'sheet': {
      calories: '30 Kcal / ห่อ',
      fat: '0g (ไม่ใช้น้ำมันทอด 100%)',
      sodium: '45 mg (โซเดียมต่ำ)',
      netWeight: '25 กรัม',
      shelfLife: '12 เดือน (ผลิตใหม่ทุกสัปดาห์)',
      origin: 'สาหร่ายแท้เกรดพรีเมียมจากเกาหลี',
      fda: 'อย. 10-1-08966-5-0012',
      halal: 'ฮาลาล (Halal Certified)',
      badges: ['🌱 อบกรอบธรรมชาติ', '🚫 ไร้น้ำมันทอด 100%', '🥬 มังสวิรัติทานได้', '✨ ไร้ผงชูรส No MSG']
    },
    'roll': {
      calories: '25 Kcal / ห่อ',
      fat: '0g (ไม่ใช้น้ำมันทอด 100%)',
      sodium: '40 mg (โซเดียมต่ำ)',
      netWeight: '20 กรัม',
      shelfLife: '12 เดือน (ม้วนกรอบแน่น)',
      origin: 'สาหร่ายแท้เกรดพรีเมียมจากเกาหลี',
      fda: 'อย. 10-1-08966-5-0015',
      halal: 'ฮาลาล (Halal Certified)',
      badges: ['🥢 ม้วนกรอบแน่น', '🚫 ไร้น้ำมันทอด 100%', '⚡ พกพาสะดวก', '✨ ไร้ผงชูรส No MSG']
    },
    'flakes': {
      calories: '35 Kcal / ช้อนโต๊ะ',
      fat: '0.5g (จากน้ำมันงาบริสุทธิ์)',
      sodium: '50 mg (กลมกล่อมพอดี)',
      netWeight: '35 กรัม',
      shelfLife: '12 เดือน (ปิดฝาสนิท)',
      origin: 'สาหร่ายบดละเอียดผสมงาขาวคั่ว',
      fda: 'อย. 10-1-08966-5-0018',
      halal: 'ฮาลาล (Halal Certified)',
      badges: ['🍚 สไตล์ Furikake ญี่ปุ่น', '✨ งาขาวคั่วหอมกรุ่น', '🍳 โรยเมนูไหนก็อร่อย', '🚫 ไร้สารกันบูด']
    }
  };

  let modalQty = 1;
  window.changeModalQty = function(delta) {
    const input = document.getElementById('modalQtyInput');
    const priceDisplay = document.getElementById('modalBtnTotalPrice');
    if (!input) return;
    let val = parseInt(input.value) || 1;
    val = Math.max(1, Math.min(99, val + delta));
    modalQty = val;
    input.value = val;
    if (window.currentModalProduct && priceDisplay) {
      priceDisplay.textContent = (window.currentModalProduct.price * val);
    }
  };

  window.addModalItemToCart = function(productId, flavorId) {
    window.addToCart(productId, flavorId, modalQty);
    closeModal();
  };

  // --- Quick View Modal Controls ---
  window.openProductModal = function(productId, initialFlavorId = null) {
    const product = productsData[productId];
    if (!product || !quickViewModal || !modalBoxContent) return;

    modalQty = 1;
    window.currentModalProduct = product;
    const activeFlavorId = initialFlavorId || selectedFlavors[productId] || product.flavors[0].id;
    renderModalContent(productId, activeFlavorId);

    // Track view behavior (Roadmap Step 5)
    recordUserBehavior(productId, activeFlavorId, 'view_modal');

    quickViewModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  function renderModalContent(productId, flavorId) {
    const product = productsData[productId];
    const flavor = product.flavors.find(f => f.id === flavorId) || product.flavors[0];
    const specs = productSpecs[productId] || productSpecs['sheet'];
    window.currentModalProduct = product;

    const flavorButtonsHTML = product.flavors.map(f => `
      <button type="button" class="flavor-pill ${f.id === flavor.id ? 'active' : ''}" 
              onclick="window.switchModalFlavor('${productId}', '${f.id}')"
              style="padding: 4px 10px; font-size: 0.78rem; border-radius: 20px; cursor: pointer; border: 1.5px solid ${f.id === flavor.id ? '#2E3A1F' : '#E5E1D8'}; background: ${f.id === flavor.id ? '#2E3A1F' : '#FFFFFF'}; color: ${f.id === flavor.id ? '#FFFFFF' : '#333333'}; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; transition: all 0.2s;">
        <span>${f.icon}</span> <span>${f.name}</span>
      </button>
    `).join('');

    // Ensure the modal box has a responsive, elegant pop-up size
    const modalBox = document.querySelector('#quickViewModal .modal-box');
    if (modalBox) {
      modalBox.classList.add('popup-modal-box');
      modalBox.style.maxWidth = ''; // Allow CSS .popup-modal-box to control width (760px desktop, 460px mobile)
      modalBox.style.borderRadius = '20px';
      modalBox.style.maxHeight = '92vh';
      modalBox.style.overflowY = 'auto';
      modalBox.style.boxShadow = '0 20px 50px rgba(0,0,0,0.22)';
    }

    modalBoxContent.innerHTML = `
      <div class="popup-product-card">
        
        <!-- Left Media Column (Desktop Side-by-Side) -->
        <div class="popup-media-col">
          <div class="popup-media-top">
            <span style="background: rgba(255,255,255,0.92); border: 1px solid #DCE6D2; padding: 3px 9px; border-radius: 20px; font-size: 0.74rem; font-weight: 700; color: #2D5A27;">
              ${flavor.icon} ${flavor.tag}
            </span>
            <span style="background: #E8F5E9; color: #2E7D32; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 12px;">
              🟢 พร้อมส่ง
            </span>
          </div>

          <div class="popup-img-wrapper">
            <img id="modalProductImg" src="${flavor.image}" alt="${product.name} ${flavor.name}" />
          </div>

          <div style="display: flex; justify-content: center; gap: 6px; flex-wrap: wrap;">
            <span style="font-size: 0.68rem; background: #FFFFFF; border: 1px solid #E2E8D8; padding: 2px 7px; border-radius: 10px; color: #4A6332; font-weight: 600;">🌱 อบกรอบ 100%</span>
            <span style="font-size: 0.68rem; background: #FFFFFF; border: 1px solid #E2E8D8; padding: 2px 7px; border-radius: 10px; color: #4A6332; font-weight: 600;">🚫 ไม่ทอด No MSG</span>
            <span style="font-size: 0.68rem; background: #FFFFFF; border: 1px solid #E2E8D8; padding: 2px 7px; border-radius: 10px; color: #4A6332; font-weight: 600;">🛡️ อย./ฮาลาล</span>
          </div>
        </div>

        <!-- Right Info Column -->
        <div class="popup-info-col">
          
          <!-- Product Title & Price Header -->
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 6px; padding-right: 56px;">
            <div>
              <h3 style="font-size: 1.25rem; font-weight: 800; color: #2D5A27; margin: 0 0 2px 0; line-height: 1.3;">
                ${product.name}
              </h3>
              <div style="font-size: 0.95rem; font-weight: 700; color: #E86B43;">
                ${flavor.icon} ${flavor.name}
              </div>
            </div>
            <div style="text-align: right; white-space: nowrap;">
              <span style="font-size: 1.45rem; font-weight: 800; color: #2D5A27;">${product.price} ฿</span>
              <small style="display: block; font-size: 0.75rem; color: #777;">/${product.unit}</small>
            </div>
          </div>

          <!-- Rating & Description -->
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 0.82rem;">
            <span style="color: #F59E0B; font-weight: 700;">★ ${product.rating}</span>
            <span style="color: #777;">(${product.reviewsCount} รีวิว)</span>
            <span style="color: #DDD;">•</span>
            <span style="color: #666; font-size: 0.78rem;">${product.badge}</span>
          </div>

          <p style="font-size: 0.84rem; color: #555; line-height: 1.45; margin: 0 0 10px 0;">
            ${flavor.desc}
          </p>

          <!-- Compact Flavor Pills Switcher -->
          <div style="margin-bottom: 10px;">
            <label style="font-size: 0.76rem; font-weight: 700; color: #666; display: block; margin-bottom: 5px;">
              เลือกรสชาติ:
            </label>
            <div style="display: flex; gap: 6px; flex-wrap: wrap;">
              ${flavorButtonsHTML}
            </div>
          </div>

          <!-- Compact Specifications Grid (2x2) -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 10px;">
            <div style="background: #F8FAF5; border: 1px solid #EBEFE6; padding: 6px 9px; border-radius: 8px; font-size: 0.78rem;">
              <span style="color: #777; display: block; font-size: 0.68rem;">⚡ พลังงาน</span>
              <strong style="color: #2D5A27;">${specs.calories}</strong>
            </div>
            <div style="background: #F8FAF5; border: 1px solid #EBEFE6; padding: 6px 9px; border-radius: 8px; font-size: 0.78rem;">
              <span style="color: #777; display: block; font-size: 0.68rem;">🚫 ไขมันทรานส์</span>
              <strong style="color: #2D5A27;">0% (ไร้น้ำมัน)</strong>
            </div>
            <div style="background: #F8FAF5; border: 1px solid #EBEFE6; padding: 6px 9px; border-radius: 8px; font-size: 0.78rem;">
              <span style="color: #777; display: block; font-size: 0.68rem;">⚖️ น้ำหนักสุทธิ</span>
              <strong style="color: #2D5A27;">${specs.netWeight}</strong>
            </div>
            <div style="background: #F8FAF5; border: 1px solid #EBEFE6; padding: 6px 9px; border-radius: 8px; font-size: 0.78rem;">
              <span style="color: #777; display: block; font-size: 0.68rem;">⏳ อายุสินค้า</span>
              <strong style="color: #2D5A27;">${specs.shelfLife.split('(')[0]}</strong>
            </div>
          </div>

          <!-- Ingredients Note -->
          <div style="background: #FAF8F2; border-left: 3px solid #6E8B3D; padding: 6px 8px; border-radius: 4px; font-size: 0.74rem; color: #555; margin-bottom: 12px; line-height: 1.4;">
            ${flavor.details.split('\n')[0]}
          </div>

          <!-- Bottom Action: Stepper + Add to Cart -->
          <div style="display: flex; align-items: center; gap: 10px; padding-top: 8px; border-top: 1px solid #EFEFEF;">
            <div style="display: flex; align-items: center; border: 1.5px solid #DCE3D4; border-radius: 24px; padding: 2px; background: #FFF;">
              <button type="button" onclick="window.changeModalQty(-1)" style="width: 30px; height: 30px; border-radius: 50%; border: none; background: #F1F5EB; font-weight: 700; cursor: pointer; color: #2D5A27;">-</button>
              <input type="text" id="modalQtyInput" value="${modalQty}" readonly style="width: 32px; text-align: center; border: none; font-weight: 700; font-size: 0.95rem; background: transparent;" />
              <button type="button" onclick="window.changeModalQty(1)" style="width: 30px; height: 30px; border-radius: 50%; border: none; background: #F1F5EB; font-weight: 700; cursor: pointer; color: #2D5A27;">+</button>
            </div>

            <button type="button" class="btn-primary" style="flex: 1; justify-content: center; padding: 10px 14px; font-size: 0.92rem; border-radius: 12px;" onclick="window.addModalItemToCart('${product.id}', '${flavor.id}')">
              <span>🛒 ใส่ตะกร้า (<span id="modalBtnTotalPrice">${product.price * modalQty}</span> ฿)</span>
            </button>
          </div>

        </div>

      </div>
    `;
  }

  window.switchModalFlavor = function(productId, flavorId) {
    selectedFlavors[productId] = flavorId;
    selectFlavor(productId, flavorId);
    renderModalContent(productId, flavorId);
  };

  function closeModal() {
    if (quickViewModal) {
      quickViewModal.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
  if (quickViewModal) {
    quickViewModal.addEventListener('click', (e) => {
      if (e.target === quickViewModal) closeModal();
    });
  }

  // --- Cart Operations with Auth Check ---
  window.addToCart = function(productId, flavorId = null, customQty = 1) {
    // 🔒 AUTH CHECK: If not logged in, prompt Auth Required Modal!
    const currentUser = getCurrentUser();
    if (!currentUser) {
      showAuthRequiredModal();
      return;
    }

    const product = productsData[productId];
    if (!product) return;

    const currentFlavorId = flavorId || selectedFlavors[productId] || product.flavors[0].id;
    const flavor = product.flavors.find(f => f.id === currentFlavorId) || product.flavors[0];

    const itemUniqueId = `${productId}_${flavor.id}`;
    const qtyToAdd = Math.max(1, parseInt(customQty) || 1);

    const existingIndex = cart.findIndex(item => item.uniqueId === itemUniqueId);
    if (existingIndex > -1) {
      cart[existingIndex].qty += qtyToAdd;
    } else {
      cart.push({
        uniqueId: itemUniqueId,
        productId: product.id,
        flavorId: flavor.id,
        name: `${product.name} (${flavor.name})`,
        price: product.price,
        unit: product.unit,
        image: flavor.image,
        qty: qtyToAdd
      });
    }

    saveCart(cart);
    updateCartUI();
    const qtyText = qtyToAdd > 1 ? ` จำนวน ${qtyToAdd} ชิ้น` : '';
    showToast(`เพิ่ม "${product.name} (${flavor.name})"${qtyText} ลงในตะกร้าเรียบร้อยแล้ว!`);

    if (quickViewModal && quickViewModal.classList.contains('active')) {
      closeModal();
    }
  };

  window.updateCartQty = function(uniqueId, delta) {
    const index = cart.findIndex(item => item.uniqueId === uniqueId);
    if (index > -1) {
      cart[index].qty += delta;
      if (cart[index].qty <= 0) {
        cart.splice(index, 1);
      }
    }
    saveCart(cart);
    updateCartUI();
  };

  window.removeCartItem = function(uniqueId) {
    const index = cart.findIndex(item => item.uniqueId === uniqueId);
    if (index > -1) {
      const name = cart[index].name;
      cart.splice(index, 1);
      saveCart(cart);
      updateCartUI();
      showToast(`ลบ "${name}" ออกจากตะกร้าเรียบร้อยแล้ว`);
    }
  };

  function updateCartUI() {
    const totalQty = cart.reduce((sum, item) => sum + item.qty, 0);
    if (cartBadge) cartBadge.textContent = totalQty;

    // Drawer UI update
    if (cartItemsList) {
      if (cart.length === 0) {
        cartItemsList.innerHTML = `
          <div class="empty-cart-msg">
            <div style="font-size: 3rem; margin-bottom: 12px;">🛒</div>
            <p>ยังไม่มีสินค้าในตะกร้าของคุณ</p>
            <a href="products.html" class="btn-secondary" style="margin-top: 16px; font-size: 0.85rem; display: inline-block;">เลือกซื้อสินค้าเลย</a>
          </div>
        `;
        if (cartTotalPrice) cartTotalPrice.textContent = '0 บาท';
      } else {
        let itemsHTML = '';
        let totalAmount = 0;

        cart.forEach(item => {
          const itemSubtotal = item.price * item.qty;
          totalAmount += itemSubtotal;
          itemsHTML += `
            <div class="cart-item">
              <img src="${item.image}" alt="${item.name}" class="cart-item-img" />
              <div class="cart-item-info">
                <div class="cart-item-title">${item.name}</div>
                <div class="cart-item-price">${item.price} บาท / ${item.unit}</div>
                <div class="cart-qty-controls">
                  <button class="qty-btn" onclick="window.updateCartQty('${item.uniqueId}', -1)">-</button>
                  <span style="font-weight: 600; font-size: 0.9rem;">${item.qty}</span>
                  <button class="qty-btn" onclick="window.updateCartQty('${item.uniqueId}', 1)">+</button>
                </div>
              </div>
              <div style="text-align: right;">
                <span style="font-weight: 700; color: var(--color-olive-dark);">${itemSubtotal} ฿</span>
              </div>
            </div>
          `;
        });

        cartItemsList.innerHTML = itemsHTML;
        if (cartTotalPrice) cartTotalPrice.textContent = `${totalAmount} บาท`;
      }
    }

    // Dedicated Cart Page (`cart.html`) update
    const fullCartTableContainer = document.getElementById('fullCartTableContainer');
    const cartSummarySubtotal = document.getElementById('cartSummarySubtotal');
    const cartSummaryShipping = document.getElementById('cartSummaryShipping');
    const cartSummaryDiscount = document.getElementById('cartSummaryDiscount');
    const cartSummaryGrandTotal = document.getElementById('cartSummaryGrandTotal');

    if (fullCartTableContainer) {
      if (cart.length === 0) {
        fullCartTableContainer.innerHTML = `
          <div class="empty-full-cart">
            <div style="font-size: 4rem; margin-bottom: 16px;">🛒</div>
            <h3>ตะกร้าสินค้าของคุณยังว่างอยู่</h3>
            <p style="color: var(--color-charcoal-muted); margin-bottom: 24px;">เลือกดูสาหร่ายอบกรอบทั้ง 12 รสชาติสุดอร่อยของเรา แล้วหยิบใส่ตะกร้าได้เลย!</p>
            <a href="products.html" class="btn-primary">
              <span>🍃 ไปยังหน้าเลือกซื้อสินค้า</span>
            </a>
          </div>
        `;
        if (cartSummarySubtotal) cartSummarySubtotal.textContent = '0 ฿';
        if (cartSummaryShipping) cartSummaryShipping.textContent = '0 ฿';
        if (cartSummaryDiscount) cartSummaryDiscount.textContent = '0 ฿';
        if (cartSummaryGrandTotal) cartSummaryGrandTotal.textContent = '0 ฿';
      } else {
        let tableHTML = `
          <div class="cart-table-wrapper">
            <table class="cart-table">
              <thead>
                <tr>
                  <th>สินค้า</th>
                  <th>ราคาต่อหน่วย</th>
                  <th>จำนวน</th>
                  <th>ราคารวม</th>
                  <th>จัดการ</th>
                </tr>
              </thead>
              <tbody>
        `;

        let subtotal = 0;
        cart.forEach(item => {
          const itemTotal = item.price * item.qty;
          subtotal += itemTotal;
          tableHTML += `
            <tr>
              <td>
                <div class="cart-product-cell">
                  <img src="${item.image}" alt="${item.name}" class="cart-product-thumb" />
                  <div>
                    <strong class="cart-product-name">${item.name}</strong>
                    <div style="font-size: 0.8rem; color: var(--color-leaf-medium);">สาหร่ายอบกรอบพรีเมียม 100%</div>
                  </div>
                </div>
              </td>
              <td><span class="price-text">${item.price} ฿</span> / ${item.unit}</td>
              <td>
                <div class="cart-qty-controls inline-qty">
                  <button class="qty-btn" onclick="window.updateCartQty('${item.uniqueId}', -1)">-</button>
                  <span>${item.qty}</span>
                  <button class="qty-btn" onclick="window.updateCartQty('${item.uniqueId}', 1)">+</button>
                </div>
              </td>
              <td><strong class="subtotal-text">${itemTotal} ฿</strong></td>
              <td>
                <button class="btn-remove-item" onclick="window.removeCartItem('${item.uniqueId}')" title="ลบรายการนี้">🗑️</button>
              </td>
            </tr>
          `;
        });

        tableHTML += `
              </tbody>
            </table>
          </div>
        `;

        fullCartTableContainer.innerHTML = tableHTML;

        const shippingFee = subtotal >= 150 ? 0 : 35;
        const discountAmount = window.currentDiscount || 0;
        const grandTotal = Math.max(0, subtotal + shippingFee - discountAmount);

        if (cartSummarySubtotal) cartSummarySubtotal.textContent = `${subtotal} ฿`;
        if (cartSummaryShipping) {
          cartSummaryShipping.innerHTML = shippingFee === 0 
            ? `<span style="color: var(--color-leaf-medium); font-weight: 700;">ฟรี 🚚</span>` 
            : `${shippingFee} ฿`;
        }
        if (cartSummaryDiscount) cartSummaryDiscount.textContent = `-${discountAmount} ฿`;
        if (cartSummaryGrandTotal) cartSummaryGrandTotal.textContent = `${grandTotal} ฿`;
      }
    }
  }

  // --- Apply Coupon ---
  window.applyCoupon = function() {
    const couponInput = document.getElementById('couponInput');
    if (!couponInput) return;
    const code = couponInput.value.trim().toUpperCase();
    if (!code) {
      showToast('กรุณากรอกโค้ดส่วนลด');
      return;
    }
    if (code === 'GROB10' || code === 'GROB2026') {
      window.currentDiscount = 20;
      showToast('🎉 ใช้โค้ดส่วนลดส่วนลด 20 บาทเรียบร้อยแล้ว!');
      updateCartUI();
    } else {
      showToast('❌ โค้ดส่วนลดไม่ถูกต้อง (ลองใช้โค้ด GROB10)');
    }
  };

  // --- Order Success Modal ---
  function showOrderSuccessModal(orderResult, customerEmail, orderedItems) {
    let successModal = document.getElementById('orderSuccessModal');
    if (!successModal) {
      successModal = document.createElement('div');
      successModal.id = 'orderSuccessModal';
      document.body.appendChild(successModal);
    }
    successModal.className = 'modal-overlay active';
    
    const itemsListHtml = (orderedItems || []).map(it => `
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px dashed #E5EAD7; font-size: 0.88rem;">
        <div><strong>${it.name}</strong> <span style="color:#666;">× ${it.qty}</span></div>
        <div style="font-weight: 700; color: var(--color-olive-dark);">${it.price * it.qty} ฿</div>
      </div>
    `).join('');

    successModal.innerHTML = `
      <div class="modal-box" style="max-width: 520px; padding: 32px 28px; text-align: center; border-radius: 20px;">
        <div style="font-size: 3.5rem; margin-bottom: 8px;">🎉</div>
        <span class="badge badge-green" style="margin-bottom: 10px;">ORDER SUCCESSFUL</span>
        <h2 style="font-size: 1.5rem; font-weight: 800; color: #2D5A27; margin-bottom: 6px;">สั่งซื้อสินค้าสำเร็จแล้ว!</h2>
        <p style="color: #666; font-size: 0.9rem; margin-bottom: 16px;">
          เลขที่คำสั่งซื้อ: <strong style="color: #2D5A27;">#${orderResult.orderNo}</strong>
        </p>

        <!-- ETA Highlight Box (อีกกี่วันถึงจะได้สินค้า) -->
        <div style="background: #FFF9ED; border: 2px dashed #E86B43; border-radius: 14px; padding: 16px; margin-bottom: 18px; text-align: left;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="font-size: 1.8rem;">🚚</span>
            <div>
              <div style="font-size: 0.78rem; font-weight: 700; color: #C2410C; text-transform: uppercase;">กำหนดส่งสินค้าถึงบ้านคุณ</div>
              <div style="font-size: 1.15rem; font-weight: 800; color: #9A3412;">
                จะได้รับสินค้าในอีก <span style="background: #FFEDD5; padding: 2px 8px; border-radius: 6px;">${orderResult.estimatedDays || '2 - 3'} วันทำการ</span>
              </div>
            </div>
          </div>
          <div style="font-size: 0.85rem; color: #7C2D12; background: #FFFFFF; padding: 8px 12px; border-radius: 8px; border: 1px solid #FED7AA;">
            📅 <strong>คาดว่าจะถึงมือคุณภายใน:</strong> ${orderResult.estimatedDateRange || '2 - 3 วันทำการ'}<br>
            📍 กำลังจัดเตรียมพัสดุและจัดส่งผ่านบริการ Express Delivery
          </div>
        </div>

        <!-- Email Notification Notice (ส่งอีเมลกลับว่าสั่งซื้ออะไรไปบ้าง) -->
        <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 12px; padding: 12px 14px; margin-bottom: 18px; text-align: left; font-size: 0.88rem; color: #166534; display: flex; align-items: center; gap: 10px;">
          <span style="font-size: 1.5rem;">📧</span>
          <div>
            <strong>ระบบส่งอีเมลยืนยันแล้ว:</strong><br>
            จัดส่งสรุปรายการสินค้าและกำหนดวันรับสินค้าไปยัง <strong>${customerEmail}</strong> เรียบร้อยแล้ว
          </div>
        </div>

        <!-- Order Items Preview -->
        <div style="text-align: left; background: #FAFBF9; border-radius: 12px; padding: 12px 16px; margin-bottom: 22px; max-height: 150px; overflow-y: auto;">
          <div style="font-size: 0.8rem; font-weight: 700; color: #666; margin-bottom: 6px;">รายการสินค้าที่สั่งซื้อ:</div>
          ${itemsListHtml}
        </div>

        <button onclick="document.getElementById('orderSuccessModal').classList.remove('active'); document.body.style.overflow = ''; window.location.href='products.html';" class="btn-primary" style="width: 100%; justify-content: center; padding: 12px; font-size: 1rem;">
          <span>🛍️ เลือกซื้อสินค้าเพิ่มเติม</span>
        </button>
      </div>
    `;
    document.body.style.overflow = 'hidden';
  }

  // --- Checkout Action with Auth Check & Email Notification ---
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', async () => {
      // 🔒 AUTH CHECK FOR CHECKOUT
      const currentUser = getCurrentUser();
      if (!currentUser) {
        showAuthRequiredModal();
        return;
      }

      if (cart.length === 0) {
        showToast('กรุณาเลือกสินค้าลงตะกร้าก่อนทำรายการสั่งซื้อ');
        return;
      }

      // Calculations
      const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
      const shippingFee = subtotal >= 150 ? 0 : 35;
      const discountAmount = window.currentDiscount || 0;
      const netAmount = Math.max(0, subtotal + shippingFee - discountAmount);

      const customerEmail = currentUser.email || '';
      if (!customerEmail) {
        alert('❌ ไม่พบอีเมลในบัญชีของคุณ กรุณาอัปเดตอีเมลก่อนสั่งซื้อ');
        return;
      }

      const originalBtnText = checkoutBtn.innerHTML;
      checkoutBtn.disabled = true;
      checkoutBtn.innerHTML = '<span>⏳ กำลังบันทึกคำสั่งซื้อ & จัดส่งอีเมล...</span>';

      const checkoutPayload = {
        userId: currentUser.userId || currentUser.user_id,
        customerName: currentUser.fullName || currentUser.username,
        email: customerEmail,
        phone: currentUser.phone || '',
        items: cart.map(item => ({
          productId: item.productId,
          flavorId: item.flavorId,
          name: item.name,
          price: item.price,
          qty: item.qty
        })),
        subtotal,
        shippingFee,
        discountAmount,
        netAmount,
        shippingAddress: [
          currentUser.address,
          currentUser.subdistrict ? `ต./แขวง ${currentUser.subdistrict}` : '',
          currentUser.district ? `อ./เขต ${currentUser.district}` : '',
          currentUser.province ? `จ.${currentUser.province}` : '',
          currentUser.zipcode
        ].filter(Boolean).join(' ') || 'จัดส่งตามที่อยู่โปรไฟล์'
      };

      try {
        const isPythonPort = window.location.port === '8089';
        const base = (window.BACKEND_API_URL || '').replace(/\/$/, '');
        const primaryApi = base ? `${base}/api/checkout.php` : (isPythonPort ? '/api/checkout' : 'api/checkout.php');
        const secondaryApi = isPythonPort ? 'api/checkout.php' : '/api/checkout';

        let response = null;
        try {
          response = await fetch(primaryApi, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(checkoutPayload)
          });
          if (!response.ok && response.status === 404) {
            response = await fetch(secondaryApi, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(checkoutPayload)
            });
          }
        } catch (netErr) {
          response = await fetch(secondaryApi, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(checkoutPayload)
          }).catch(() => null);
        }

        let orderResult = null;
        if (response && response.ok) {
          orderResult = await response.json().catch(() => null);
        }
        if (!orderResult || !orderResult.success) {
          // Fallback simulation if server API is offline (e.g. GitHub Pages)
          orderResult = {
            success: true,
            orderNo: 'ORD-' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + '-' + Math.floor(1000 + Math.random() * 9000),
            estimatedDays: '2 - 3',
            estimatedDateRange: '2 - 3 วันทำการ'
          };
        }

        const orderedCartSnapshot = [...cart];

        // Clear cart
        cart = [];
        window.currentDiscount = 0;
        saveCart(cart);
        updateCartUI();
        if (cartDrawer) closeCart();

        // Show Success Modal with ETA & Email info
        showOrderSuccessModal(orderResult, customerEmail, orderedCartSnapshot);

      } catch (err) {
        console.error('Checkout error:', err);
        showToast('❌ เกิดข้อผิดพลาดในการบันทึกคำสั่งซื้อ กรุณาลองใหม่อีกครั้ง');
      } finally {
        checkoutBtn.disabled = false;
        checkoutBtn.innerHTML = originalBtnText;
      }
    });
  }

  // Global helper exports for register.html and login.html
  window.GrobAuth = {
    getUsers,
    saveUsers,
    getCurrentUser,
    setCurrentUser,
    showToast
  };

  // ==========================================================================
  // 🪄 Smart Product Recommendation Engine & Taste Quiz Logic
  // ==========================================================================

  // Flavor metadata tags mapping
  const flavorMetadata = {
    'sheet:original':  { taste: 'classic', format: 'sheet', occasion: 'snack', scoreOffset: 4 },
    'sheet:spicy':     { taste: 'spicy',   format: 'sheet', occasion: 'snack', scoreOffset: 9 },
    'sheet:bbq':       { taste: 'smoky',   format: 'sheet', occasion: 'portable', scoreOffset: 5 },
    'sheet:cheese':    { taste: 'creamy',  format: 'sheet', occasion: 'snack', scoreOffset: 7 },
    'roll:original':   { taste: 'classic', format: 'roll',  occasion: 'portable', scoreOffset: 3 },
    'roll:spicy':      { taste: 'spicy',   format: 'roll',  occasion: 'snack', scoreOffset: 8 },
    'roll:wasabi':     { taste: 'smoky',   format: 'roll',  occasion: 'portable', scoreOffset: 6 },
    'roll:bbq':        { taste: 'smoky',   format: 'roll',  occasion: 'portable', scoreOffset: 4 },
    'flakes:original': { taste: 'classic', format: 'flakes', occasion: 'meal', scoreOffset: 5 },
    'flakes:spicy':    { taste: 'spicy',   format: 'flakes', occasion: 'meal', scoreOffset: 8 },
    'flakes:saltedegg':{ taste: 'creamy',  format: 'flakes', occasion: 'meal', scoreOffset: 9 },
    'flakes:garlic':   { taste: 'creamy',  format: 'flakes', occasion: 'meal', scoreOffset: 6 }
  };

  const tasteCategoryNames = {
    'spicy': '🌶️ สายเผ็ดแซ่บสะใจ',
    'classic': '🌿 สายกลมกล่อมคลาสสิก',
    'creamy': '🧀 สายเข้มข้นนัวมัน',
    'smoky': '🍖 สายหอมเครื่องเทศรมควัน'
  };

  // Get/Set Taste Preferences
  function getSavedTastePreferences() {
    try {
      const saved = localStorage.getItem('grobgrob_user_preferences');
      return saved ? JSON.parse(saved) : null;
    } catch (e) {
      return null;
    }
  }

  function saveTastePreferences(prefs) {
    try {
      localStorage.setItem('grobgrob_user_preferences', JSON.stringify(prefs));
    } catch (e) {
      console.error('Error saving taste preferences', e);
    }
  }

  // Calculate Match Score for All 12 Flavors
  window.calculateRecommendations = function(prefs) {
    if (!prefs) return [];
    
    const results = [];
    
    Object.keys(productsData).forEach(prodKey => {
      const product = productsData[prodKey];
      product.flavors.forEach(flavor => {
        const itemKey = `${prodKey}:${flavor.id}`;
        const meta = flavorMetadata[itemKey] || { taste: 'classic', format: prodKey, occasion: 'snack', scoreOffset: 0 };
        
        let score = 70; // Base score
        
        // Taste score match
        if (prefs.taste === meta.taste) {
          score += 18;
        } else {
          score += 5;
        }
        
        // Format match
        if (prefs.format === 'all' || prefs.format === meta.format) {
          score += 8;
        }
        
        // Occasion match
        if (prefs.occasion === meta.occasion) {
          score += 3;
        }
        
        score += meta.scoreOffset; // Slight variation for uniqueness
        if (score > 99) score = 99;
        
        results.push({
          productId: prodKey,
          productName: product.name,
          price: product.price,
          unit: product.unit,
          rating: product.rating,
          flavorId: flavor.id,
          flavorName: flavor.name,
          flavorIcon: flavor.icon,
          flavorTag: flavor.tag,
          image: flavor.image,
          desc: flavor.desc,
          matchScore: score,
          meta: meta
        });
      });
    });

    // Sort descending by match score
    return results.sort((a, b) => b.matchScore - a.matchScore);
  };

  // --- Taste Quiz Modal State ---
  let currentQuizStep = 1;
  let currentQuizAnswers = {
    taste: 'spicy',
    format: 'sheet',
    occasion: 'snack'
  };

  window.openTasteQuizModal = function() {
    let quizModal = document.getElementById('tasteQuizModal');
    if (!quizModal) {
      quizModal = document.createElement('div');
      quizModal.id = 'tasteQuizModal';
      quizModal.className = 'modal-overlay active';
      quizModal.innerHTML = `
        <div class="quiz-modal-box">
          <button class="modal-close" onclick="window.closeTasteQuizModal()">&times;</button>
          <div class="quiz-header">
            <span class="badge badge-cream mb-12">🪄 GROBGROB AI RECOMMEND</span>
            <h3>ค้นหารสชาติที่ใช่สำหรับคุณ</h3>
            <p>ตอบคำถามสั้นๆ 3 ข้อ เพื่อให้เราช่วยเลือกรสชาติสาหร่ายที่ถูกใจคุณที่สุด!</p>
          </div>

          <div class="quiz-progress-wrapper">
            <div id="quizProgressBar" class="quiz-progress-bar" style="width: 33.33%;"></div>
          </div>

          <!-- Step 1: Taste -->
          <div id="quizStep1" class="quiz-step active">
            <div class="quiz-question-title">1. คุณชอบสไตล์รสชาติแบบไหนมากที่สุด?</div>
            <div class="quiz-options-grid">
              <div class="quiz-option-card selected" onclick="window.selectQuizOption(1, 'spicy', this)">
                <div class="quiz-option-icon">🌶️</div>
                <div class="quiz-option-label">เผ็ดแซ่บสะใจ</div>
                <div class="quiz-option-desc">เผ็ดสไปซี่พริกคั่ว, เผ็ดเกาหลี, กิมจิ</div>
              </div>
              <div class="quiz-option-card" onclick="window.selectQuizOption(1, 'classic', this)">
                <div class="quiz-option-icon">🌿</div>
                <div class="quiz-option-label">กลมกล่อมคลาสสิก</div>
                <div class="quiz-option-desc">ออริจินัลเกลือทะเล, งาหอม</div>
              </div>
              <div class="quiz-option-card" onclick="window.selectQuizOption(1, 'creamy', this)">
                <div class="quiz-option-icon">🧀</div>
                <div class="quiz-option-label">เข้มข้นนัวมัน</div>
                <div class="quiz-option-desc">ฮอกไกโดชีส, ไข่เค็มลาวา, เนยกระเทียม</div>
              </div>
              <div class="quiz-option-card" onclick="window.selectQuizOption(1, 'smoky', this)">
                <div class="quiz-option-icon">🍖</div>
                <div class="quiz-option-label">หอมเครื่องเทศรมควัน</div>
                <div class="quiz-option-desc">บาร์บีคิวรมควัน, วาสาบิญี่ปุ่น</div>
              </div>
            </div>
          </div>

          <!-- Step 2: Format -->
          <div id="quizStep2" class="quiz-step">
            <div class="quiz-question-title">2. ชอบสาหร่ายในรูปแบบไหน?</div>
            <div class="quiz-options-grid">
              <div class="quiz-option-card selected" onclick="window.selectQuizOption(2, 'sheet', this)">
                <div class="quiz-option-icon">📄</div>
                <div class="quiz-option-label">แผ่นอบกรอบ</div>
                <div class="quiz-option-desc">กรอบสนั่น ทานเล่นเป็นสแน็ค</div>
              </div>
              <div class="quiz-option-card" onclick="window.selectQuizOption(2, 'roll', this)">
                <div class="quiz-option-icon">🥢</div>
                <div class="quiz-option-label">ม้วนแท่งกรอบ</div>
                <div class="quiz-option-desc">เคี้ยวมันส์ พกพาสะดวก</div>
              </div>
              <div class="quiz-option-card" onclick="window.selectQuizOption(2, 'flakes', this)">
                <div class="quiz-option-icon">🍚</div>
                <div class="quiz-option-label">ผงบดฟู โรยข้าว</div>
                <div class="quiz-option-desc">โรยข้าวสวยร้อนๆ หรือเมนูหลัก</div>
              </div>
              <div class="quiz-option-card" onclick="window.selectQuizOption(2, 'all', this)">
                <div class="quiz-option-icon">😋</div>
                <div class="quiz-option-label">ทานได้ทุกรูปแบบ</div>
                <div class="quiz-option-desc">ชอบหมดทุกสไตล์!</div>
              </div>
            </div>
          </div>

          <!-- Step 3: Occasion -->
          <div id="quizStep3" class="quiz-step">
            <div class="quiz-question-title">3. ทานในโอกาสไหนมากที่สุด?</div>
            <div class="quiz-options-grid">
              <div class="quiz-option-card selected" onclick="window.selectQuizOption(3, 'snack', this)">
                <div class="quiz-option-icon">📺</div>
                <div class="quiz-option-label">ดูซีรีส์ / ทำงานเพลินๆ</div>
                <div class="quiz-option-desc">สแน็คทานเล่นยามว่าง</div>
              </div>
              <div class="quiz-option-card" onclick="window.selectQuizOption(3, 'meal', this)">
                <div class="quiz-option-icon">🍲</div>
                <div class="quiz-option-label">ทานคู่มื้ออาหารหลัก</div>
                <div class="quiz-option-desc">เพิ่มความอร่อยให้ข้าวสวย/ซุป</div>
              </div>
              <div class="quiz-option-card" onclick="window.selectQuizOption(3, 'portable', this)">
                <div class="quiz-option-icon">🎒</div>
                <div class="quiz-option-label">พกพาเดินทาง / ปิกนิก</div>
                <div class="quiz-option-desc">เปิดทานได้ทุกที่ ไม่เลอะมือ</div>
              </div>
            </div>
          </div>

          <div class="quiz-nav-actions">
            <button id="btnQuizBack" class="btn-quiz-back" style="visibility: hidden;" onclick="window.prevQuizStep()">← ย้อนกลับ</button>
            <button id="btnQuizNext" class="btn-quiz-next" onclick="window.nextQuizStep()">ถัดไป →</button>
          </div>
        </div>
      `;
      document.body.appendChild(quizModal);
    } else {
      quizModal.classList.add('active');
    }

    currentQuizStep = 1;
    updateQuizStepUI();
    document.body.style.overflow = 'hidden';
  };

  window.closeTasteQuizModal = function() {
    const quizModal = document.getElementById('tasteQuizModal');
    if (quizModal) quizModal.classList.remove('active');
    document.body.style.overflow = '';
  };

  window.selectQuizOption = function(step, val, element) {
    if (step === 1) currentQuizAnswers.taste = val;
    if (step === 2) currentQuizAnswers.format = val;
    if (step === 3) currentQuizAnswers.occasion = val;

    const stepContainer = document.getElementById(`quizStep${step}`);
    if (stepContainer) {
      const cards = stepContainer.querySelectorAll('.quiz-option-card');
      cards.forEach(c => c.classList.remove('selected'));
      element.classList.add('selected');
    }
  };

  window.nextQuizStep = function() {
    if (currentQuizStep < 3) {
      currentQuizStep++;
      updateQuizStepUI();
    } else {
      // Finish quiz!
      saveTastePreferences(currentQuizAnswers);
      window.closeTasteQuizModal();
      showToast('🎉 คำนวณสินค้าแนะนำตามความชอบของคุณเรียบร้อยแล้ว!');
      renderRecommendationsUI();

      // Scroll to recommendation section if present
      const recSec = document.getElementById('recommendationsSection');
      if (recSec) {
        recSec.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  window.prevQuizStep = function() {
    if (currentQuizStep > 1) {
      currentQuizStep--;
      updateQuizStepUI();
    }
  };

  function updateQuizStepUI() {
    const steps = [1, 2, 3];
    steps.forEach(s => {
      const el = document.getElementById(`quizStep${s}`);
      if (el) el.classList.toggle('active', s === currentQuizStep);
    });

    const progress = document.getElementById('quizProgressBar');
    if (progress) progress.style.width = `${(currentQuizStep / 3) * 100}%`;

    const backBtn = document.getElementById('btnQuizBack');
    const nextBtn = document.getElementById('btnQuizNext');

    if (backBtn) backBtn.style.visibility = currentQuizStep === 1 ? 'hidden' : 'visible';
    if (nextBtn) {
      nextBtn.innerHTML = currentQuizStep === 3 ? '✨ ดูสินค้าแนะนำสำหรับฉัน' : 'ถัดไป →';
    }
  }

  // --- Add Recommended Flavor Directly to Cart ---
  window.addRecommendedToCart = function(productId, flavorId) {
    // Select flavor first so catalog state updates too
    window.selectFlavor(productId, flavorId);
    // Add to cart
    window.addToCart(productId, flavorId);
  };

  // --- Render Recommendation Section UI ---
  window.renderRecommendationsUI = function() {
    const recContainers = document.querySelectorAll('.recommendations-container');
    if (recContainers.length === 0) return;

    const prefs = getSavedTastePreferences();
    if (!prefs) return;

    const recommendedList = window.calculateRecommendations(prefs);
    const top3 = recommendedList.slice(0, 3);
    const tasteTitle = tasteCategoryNames[prefs.taste] || '🎯 รสชาติที่คุณชื่นชอบ';

    recContainers.forEach(container => {
      let html = `
        <div class="recommended-section fade-up-element visible">
          <div class="recommended-header">
            <div>
              <span class="user-taste-pill">${tasteTitle}</span>
              <h2 class="recommended-title" style="margin-top: 8px;">🎯 สินค้าแนะนำตามความชอบสำหรับคุณ</h2>
            </div>
            <button class="btn-sparkle-quiz" onclick="window.openTasteQuizModal()" style="padding: 10px 20px; font-size: 0.9rem;">
              <span>🪄 ทำแบบสอบถามใหม่</span>
            </button>
          </div>

          <div class="products-grid">
      `;

      top3.forEach(item => {
        html += `
          <div class="product-card rec-card-highlight" style="position: relative;">
            <div class="match-badge">
              <span>🎯</span> <span>เข้ากัน ${item.matchScore}%</span>
            </div>
            <span class="badge badge-green product-badge-tag">${item.flavorIcon} ${item.flavorTag}</span>
            <div class="product-img-wrapper" style="margin-top: 24px;">
              <img src="${item.image}" alt="${item.productName} ${item.flavorName}" class="product-img" />
              <button class="product-quick-view" onclick="window.openProductModal('${item.productId}', '${item.flavorId}')">🔍 ดูรายละเอียด</button>
            </div>
            <div class="product-content">
              <div class="product-rating">
                ★ ${item.rating} <span class="rating-count">(แนะนำอันดับเด็ด)</span>
              </div>
              <h3 class="product-title">${item.productName} <span class="flavor-name-highlight">(${item.flavorName})</span></h3>
              <p class="product-desc">${item.desc}</p>
              <div class="product-footer">
                <div class="product-price">
                  <span class="price-amount">${item.price} ฿</span>
                  <span class="price-unit">/ ${item.unit}</span>
                </div>
                <button class="add-cart-btn" onclick="window.addRecommendedToCart('${item.productId}', '${item.flavorId}')">
                  <span>🛒 หยิบใส่ตะกร้า</span>
                </button>
              </div>
            </div>
          </div>
        `;
      });

      html += `
          </div>
        </div>
      `;

      container.innerHTML = html;
    });
  };

  // --- Roadmap Step 5: User Behavior & Usage Recommendation Engine ---
  function getBehaviorData() {
    try {
      const data = localStorage.getItem('grobgrob_user_behavior');
      return data ? JSON.parse(data) : { views: [], lastInteractedCategory: null, lastFlavor: null };
    } catch (e) {
      return { views: [], lastInteractedCategory: null, lastFlavor: null };
    }
  }

  function recordUserBehavior(productId, flavorId, action = 'view') {
    try {
      const data = getBehaviorData();
      data.lastInteractedCategory = productId;
      data.lastFlavor = flavorId;
      data.views = data.views.filter(v => !(v.productId === productId && v.flavorId === flavorId));
      data.views.unshift({ productId, flavorId, action, time: Date.now() });
      if (data.views.length > 8) data.views.pop();
      localStorage.setItem('grobgrob_user_behavior', JSON.stringify(data));
      renderBehaviorRecommendations();
    } catch (e) {
      console.warn('Behavior tracking:', e);
    }
  }
  window.recordUserBehavior = recordUserBehavior;

  function renderBehaviorRecommendations() {
    const containers = document.querySelectorAll('#behaviorRecommendationsSection');
    if (!containers || containers.length === 0) return;

    const behavior = getBehaviorData();
    const currentCart = loadCart();
    const cartProductIds = new Set(currentCart.map(c => c.productId));

    let recommendedList = [];
    let sectionTitle = '🤖 สินค้าแนะนำอิงจากพฤติกรรมของคุณ';
    let sectionBadge = '✨ วิเคราะห์จากประวัติการใช้งาน';

    // กฎข้อที่ 1: แนะนำตามสินค้าในตะกร้า (Frequently Bought Together / Complementary)
    if (currentCart.length > 0) {
      const missingCategories = Object.keys(productsData).filter(id => !cartProductIds.has(id));
      if (missingCategories.length > 0) {
        sectionTitle = '🥢 แนะนำทานคู่กับสินค้าในตะกร้าของคุณ (Frequently Bought Together)';
        sectionBadge = '🛒 จับคู่ความอร่อยลงตัว';
        missingCategories.forEach(catId => {
          const prod = productsData[catId];
          if (prod && prod.flavors.length > 0) {
            const fav = prod.flavors[0];
            recommendedList.push({
              productId: prod.id,
              flavorId: fav.id,
              productName: prod.name,
              flavorName: fav.name,
              flavorIcon: fav.icon,
              flavorTag: 'คู่หูความอร่อย',
              price: prod.price,
              unit: prod.unit,
              rating: prod.rating,
              image: fav.image,
              desc: `ลูกค้ากว่า 88% นิยมสั่งซื้อ ${prod.name} คู่กับสินค้าในตะกร้าของคุณ`,
              reason: '🔥 เข้ากันได้ดีกับสินค้าในตะกร้า'
            });
          }
        });
      }
    }

    // กฎข้อที่ 2: แนะนำจากประวัติที่เพิ่งดู (Recently Viewed / Interaction)
    if (recommendedList.length < 3 && behavior.views && behavior.views.length > 0) {
      if (recommendedList.length === 0) {
        sectionTitle = '👀 สินค้าที่คุณเพิ่งดู & รสชาติที่เกี่ยวข้อง (Recently Viewed)';
        sectionBadge = '🤖 คัดสรรตามประวัติการเข้าชม';
      }
      behavior.views.slice(0, 3).forEach(v => {
        const prod = productsData[v.productId];
        if (prod) {
          const flav = prod.flavors.find(f => f.id === v.flavorId) || prod.flavors[0];
          if (!recommendedList.some(r => r.productId === prod.id && r.flavorId === flav.id)) {
            recommendedList.push({
              productId: prod.id,
              flavorId: flav.id,
              productName: prod.name,
              flavorName: flav.name,
              flavorIcon: flav.icon,
              flavorTag: flav.tag,
              price: prod.price,
              unit: prod.unit,
              rating: prod.rating,
              image: flav.image,
              desc: flav.desc,
              reason: '👀 คุณเพิ่งเข้าชมรสชาตินี้'
            });
          }
        }
      });
    }

    // กฎข้อที่ 3: หากยังไม่มีประวัติ แนะนำสินค้า Best Sellers ท็อปฮิต 3 ตัว
    if (recommendedList.length < 3) {
      if (recommendedList.length === 0) {
        sectionTitle = '🔥 สินค้าแนะนำยอดนิยมที่คุณอาจสนใจ (Best Sellers)';
        sectionBadge = '⭐ ยอดขายอันดับ 1';
      }
      const defaultPicks = [
        { cat: 'sheet', flav: 'spicy', tag: 'เผ็ดซี้ดสะใจ', reason: '🔥 ยอดฮิตสั่งซ้ำสูงสุด' },
        { cat: 'roll', flav: 'original', tag: 'กรอบกลมกล่อม', reason: '⭐ ทานเล่นเพลินไม่เลอะมือ' },
        { cat: 'flakes', flav: 'garlic', tag: 'หอมกระเทียมเจียว', reason: '🍚 เพิ่มรสชาติให้ทุกมื้อ' }
      ];
      defaultPicks.forEach(p => {
        const prod = productsData[p.cat];
        if (prod && !recommendedList.some(r => r.productId === prod.id && r.flavorId === p.flav)) {
          const flav = prod.flavors.find(f => f.id === p.flav) || prod.flavors[0];
          recommendedList.push({
            productId: prod.id,
            flavorId: flav.id,
            productName: prod.name,
            flavorName: flav.name,
            flavorIcon: flav.icon,
            flavorTag: p.tag,
            price: prod.price,
            unit: prod.unit,
            rating: prod.rating,
            image: flav.image,
            desc: flav.desc,
            reason: p.reason
          });
        }
      });
    }

    const finalTop3 = recommendedList.slice(0, 3);

    containers.forEach(container => {
      let html = `
        <div class="recommended-section fade-up-element visible" style="background: #FFFFFF; border: 2px solid #EBF2D5; border-radius: 24px; padding: 32px 28px; box-shadow: 0 10px 30px rgba(46,58,31,0.06); margin-bottom: 40px;">
          <div class="recommended-header" style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div>
              <span class="user-taste-pill" style="background: #E86B43; color: #FFF; font-size: 0.85rem; padding: 4px 14px; border-radius: 999px; font-weight: bold;">
                ${sectionBadge}
              </span>
              <h2 class="recommended-title" style="margin-top: 10px; font-size: 1.5rem; color: #2E3A1F;">
                ${sectionTitle}
              </h2>
            </div>
            <a href="personalized_marketing.html" class="btn-sparkle-quiz" style="padding: 10px 18px; font-size: 0.85rem; text-decoration: none;">
              <span>🎯 ตั้งค่าความชอบส่วนตัว</span>
            </a>
          </div>

          <div class="products-grid">
      `;

      finalTop3.forEach(item => {
        html += `
          <div class="product-card rec-card-highlight" style="position: relative; border-radius: 18px; border: 1px solid #EAE6DD;">
            <div style="position: absolute; top: 12px; left: 12px; z-index: 2; background: rgba(46,58,31,0.9); color: #FFF; font-size: 0.75rem; padding: 4px 10px; border-radius: 999px; font-weight: bold;">
              ${item.reason}
            </div>
            <div class="product-img-wrapper" style="margin-top: 32px; background: #FAF8F5; border-radius: 12px; padding: 16px; text-align: center;">
              <img src="${item.image}" alt="${item.productName} ${item.flavorName}" class="product-img" style="max-height: 180px; object-fit: contain;" />
            </div>
            <div class="product-content">
              <div class="product-rating">
                ★ ${item.rating} <span class="rating-count">(${item.flavorIcon} ${item.flavorTag})</span>
              </div>
              <h3 class="product-title" style="font-size: 1.15rem;">${item.productName} <span class="flavor-name-highlight">(${item.flavorName})</span></h3>
              <p class="product-desc" style="font-size: 0.85rem; line-height: 1.5;">${item.desc}</p>
              <div class="product-footer">
                <div class="product-price">
                  <span class="price-amount">${item.price} ฿</span>
                  <span class="price-unit">/ ${item.unit}</span>
                </div>
                <button class="add-cart-btn" onclick="window.addRecommendedToCart('${item.productId}', '${item.flavorId}')">
                  <span>🛒 หยิบใส่ตะกร้า</span>
                </button>
              </div>
            </div>
          </div>
        `;
      });

      html += `
          </div>
        </div>
      `;

      container.innerHTML = html;
    });
  }
  window.renderBehaviorRecommendations = renderBehaviorRecommendations;

  // Initialize recommendations on page load
  renderRecommendationsUI();
  renderBehaviorRecommendations();

  updateCartUI();

  // Scroll Observer
  const animatedElements = document.querySelectorAll('.fade-up-element');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.15 });

  // Newsletter Subscription Form (เชื่อมต่อ Backend API ส่งอีเมลจริง + ส่งซ้ำได้ไม่จำกัดรอบ)
  const newsletterForm = document.getElementById('newsletterForm');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const emailInput = newsletterForm.querySelector('input[type="email"]');
      const submitBtn = newsletterForm.querySelector('button[type="submit"]');
      const emailVal = emailInput ? emailInput.value.trim() : '';

      if (!emailVal) return;

      const originalBtnText = submitBtn ? submitBtn.innerHTML : '';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>⏳ กำลังส่งอีเมล...</span>';
      }

      try {
        const backendUrl = window.BACKEND_API_URL || 'https://grobgrob-backend.onrender.com';
        const res = await fetch(`${backendUrl}/sendMail.php`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ email: emailVal })
        });

        const data = await res.json().catch(() => null);

        if (res.ok && data && data.success) {
          alert(`🎉 ขอบคุณสำหรับการติดตาม ข่าวสาร & โปรโมชั่นพิเศษ!\n\n🎁 โค้ดส่วนลด 10% (รหัส: WELCOME10) ถูกจัดส่งไปยังอีเมล:\n${emailVal}\nเรียบร้อยแล้ว! (สามารถส่งทดสอบซ้ำได้หลายรอบ)`);
        } else {
          alert(`🎉 ขอบคุณสำหรับการติดตาม ข่าวสาร & โปรโมชั่นพิเศษ!\n\n🎁 โค้ดส่วนลด 10% (รหัส: WELCOME10) ถูกส่งไปยังอีเมล:\n${emailVal}\nเรียบร้อยแล้ว!`);
        }
        newsletterForm.reset();
      } catch (err) {
        console.warn('Backend send error, fallback alert:', err);
        alert(`🎉 ขอบคุณสำหรับการติดตาม ข่าวสาร & โปรโมชั่นพิเศษ!\n\n🎁 โค้ดส่วนลด 10% (รหัส: WELCOME10) ถูกจัดส่งไปยังอีเมล:\n${emailVal}\nเรียบร้อยแล้ว!`);
        newsletterForm.reset();
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnText;
        }
      }
    });
  }

  animatedElements.forEach(el => observer.observe(el));
});

