// GrobGrob Interactive, Auth & Multi-Page Cart Logic
document.addEventListener('DOMContentLoaded', () => {
  // --- Auth State Management ---
  function getUsers() {
    try {
      const saved = localStorage.getItem('grobgrob_users');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
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

  // Pre-load default users from users.json into localStorage if empty
  if (getUsers().length === 0) {
    fetch('users.json')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data) && data.length > 0) {
          saveUsers(data);
          updateNavbarAuthUI();
        }
      })
      .catch(err => console.log('Notice: Loaded empty local user storage'));
  }

  window.logoutUser = function() {
    setCurrentUser(null);
    showToast('👋 ออกจากระบบเรียบร้อยแล้ว');
    updateNavbarAuthUI();
    setTimeout(() => {
      window.location.href = 'index.html';
    }, 1000);
  };

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

    // Clean up any legacy auth items in nav-links
    if (navLinks) {
      const existingAuthItems = navLinks.querySelectorAll('.nav-auth-item');
      existingAuthItems.forEach(el => el.remove());
    }

    if (navActions) {
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
      } else {
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
  };

  // --- Quick View Modal Controls ---
  window.openProductModal = function(productId, initialFlavorId = null) {
    const product = productsData[productId];
    if (!product || !quickViewModal || !modalBoxContent) return;

    const activeFlavorId = initialFlavorId || selectedFlavors[productId] || product.flavors[0].id;
    renderModalContent(productId, activeFlavorId);

    quickViewModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  function renderModalContent(productId, flavorId) {
    const product = productsData[productId];
    const flavor = product.flavors.find(f => f.id === flavorId) || product.flavors[0];

    const flavorButtonsHTML = product.flavors.map(f => `
      <button class="flavor-pill ${f.id === flavor.id ? 'active' : ''}" 
              onclick="window.switchModalFlavor('${productId}', '${f.id}')">
        <span>${f.icon}</span> <span>${f.name}</span>
      </button>
    `).join('');

    modalBoxContent.innerHTML = `
      <div class="modal-grid-layout">
        <div class="modal-img-container">
          <img id="modalProductImg" src="${flavor.image}" alt="${product.name} ${flavor.name}" class="modal-img" />
        </div>
        <div>
          <span class="badge badge-green" style="margin-bottom: 12px;">${flavor.icon} ${flavor.tag}</span>
          <h3 style="font-size: 1.5rem; margin-bottom: 4px; font-weight: 700;">${product.name}</h3>
          <h4 style="font-size: 1.1rem; color: var(--color-leaf-medium); margin-bottom: 12px;">${flavor.name}</h4>
          
          <div style="color: #F59E0B; margin-bottom: 16px; font-weight: 600; font-size: 0.95rem;">
            ★ ${product.rating} <span style="color: var(--color-charcoal-muted); font-size: 0.85rem;">(${product.reviewsCount} รีวิวจากผู้ทานจริง)</span>
          </div>

          <div style="margin-bottom: 16px;">
            <label style="font-size: 0.85rem; font-weight: 700; color: var(--color-charcoal-muted); display: block; margin-bottom: 8px;">เลือกรสชาติที่ต้องการ:</label>
            <div class="flavor-pills-wrapper">
              ${flavorButtonsHTML}
            </div>
          </div>

          <p style="color: var(--color-charcoal-muted); margin-bottom: 16px; font-size: 0.95rem;">${flavor.desc}</p>
          
          <div style="font-size: 0.85rem; background: var(--bg-cream); padding: 12px; border-radius: var(--radius-sm); margin-bottom: 20px; white-space: pre-line; line-height: 1.6;">
            ${flavor.details}
          </div>

          <div style="display: flex; align-items: center; justify-content: space-between;">
            <span style="font-size: 1.7rem; font-weight: 700; color: var(--color-olive-dark);">${product.price} บาท <small style="font-size: 0.85rem; font-weight: 400;">/${product.unit}</small></span>
            <button class="add-cart-btn" onclick="window.addToCart('${product.id}', '${flavor.id}')">
              <span>🛒 หยิบใส่ตะกร้า</span>
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
  window.addToCart = function(productId, flavorId = null) {
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

    const existingIndex = cart.findIndex(item => item.uniqueId === itemUniqueId);
    if (existingIndex > -1) {
      cart[existingIndex].qty += 1;
    } else {
      cart.push({
        uniqueId: itemUniqueId,
        productId: product.id,
        flavorId: flavor.id,
        name: `${product.name} (${flavor.name})`,
        price: product.price,
        unit: product.unit,
        image: flavor.image,
        qty: 1
      });
    }

    saveCart(cart);
    updateCartUI();
    showToast(`เพิ่ม "${product.name} (${flavor.name})" ลงในตะกร้าเรียบร้อยแล้ว!`);

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

  // --- Checkout Action with Auth Check ---
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
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
      showToast(`🎉 ขอบคุณคุณ ${currentUser.fullName || currentUser.username}! ระบบบันทึกคำสั่งซื้อเรียบร้อยแล้ว`);
      setTimeout(() => {
        cart = [];
        saveCart(cart);
        updateCartUI();
        if (cartDrawer) closeCart();
      }, 2000);
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

  // Initialize recommendations on page load
  renderRecommendationsUI();

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

  animatedElements.forEach(el => observer.observe(el));
});

