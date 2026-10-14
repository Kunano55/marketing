# 🌿 Prompt: สร้างเว็บไซต์ Single Page ขายสาหร่ายอบกรอบ "GrobGrob"

ใช้ไฟล์นี้เป็น prompt/spec ป้อนให้ AI (Claude, Cursor, v0 ฯลฯ) สร้างเว็บไซต์ single page แบบ HTML/CSS (หรือ React) ให้ครบตาม requirement ด้านล่าง

---

## 1. ภาพรวมแบรนด์

- **ชื่อแบรนด์:** GrobGrob (กรอบกรอบ)
- **สโลแกน/แท็กไลน์:** กรอบอร่อยเพลิน เคี้ยวสนุกทุกคำ
- **บุคลิกแบรนด์:** สดใส ขี้เล่น อบอุ่น เป็นมิตร กินง่าย เด็กและผู้ใหญ่ชอบ
- **โลโก้:** ตัวอักษร "GrobGrob" ทรงกลมมน (rounded, bubbly font) สีเขียวสลับดำ มีภาพสาหร่ายฉีกครึ่งสีเขียวเข้มลายจุด อยู่ด้านบน วางบนพื้นวงกลมสีครีม/เบจอ่อน มีคำว่า "สาหร่ายอบกรอบ" อยู่ในแคปซูลสีเขียวด้านล่าง

## 2. Palette สี (ดึงจากโลโก้)

ใช้ **สีขาวเป็นพื้นหลักของเว็บ** แล้วแซมด้วยสีจากโลโก้ ดังนี้:

| ชื่อสี | Hex (โดยประมาณ) | ใช้ตรงไหน |
|---|---|---|
| White (พื้นหลักเว็บ) | `#FFFFFF` | Background หลักของทุก section |
| Cream / Sand | `#F6E7CE` | Background section สลับ, blob ตกแต่ง, badge |
| Dark Olive Green | `#2E3A1F` | สาหร่าย, ปุ่ม CTA หลัก, ตัวอักษรหัวข้อบางจุด |
| Medium Leaf Green | `#6E8B3D` | ปุ่มรอง, accent shape, ไอคอน, hover state |
| Light Green Dot | `#A9C25A` | จุดตกแต่ง (dot pattern), highlight เล็กๆ |
| Charcoal / Near Black | `#2B2B26` | ตัวอักษรเนื้อหา (body text), ตัว "rob" ในโลโก้ |
| Off-white text on green | `#FFF8EC` | ตัวอักษรบนพื้นเขียว (เช่นแคปซูล "สาหร่ายอบกรอบ") |

**กติกาใช้สี:** พื้นหลัง 70-80% เป็นสีขาว, สีครีมใช้เป็น section สลับหรือพื้นหลัง blob, สีเขียว 2 เฉดใช้เน้น CTA/ไอคอน/เส้นขอบ, ดำใช้กับ headline และ body text เพื่อความอ่านง่าย ห้ามใช้สีเขียวเข้มเป็นพื้นหลังเต็มหน้าจอ (จะหนักเกินไป)

## 3. Layout ของ Single Page (เรียงตามลำดับบนลงล่าง)

1. **Navbar** — โลโก้ GrobGrob (ซ้าย) + เมนู (สินค้า, เกี่ยวกับเรา, รีวิว, ติดต่อ) + ปุ่ม CTA "สั่งซื้อเลย" (ขวา), พื้นหลังขาว/โปร่งใส
2. **Hero Section** — พื้นขาวมี blob สีครีม/เขียวอ่อนลอยด้านหลัง, หัวข้อใหญ่ + คำโปรย + ปุ่ม CTA 2 ปุ่ม (สั่งซื้อ / ดูสินค้า) + รูปสินค้าเด่น (สาหร่ายแผ่น) ลอยอยู่ขวา พร้อม decorative blob ล้อมรอบ
3. **จุดเด่นสินค้า (Feature strip)** — แถวไอคอน 3-4 อัน (เช่น กรอบทุกคำ, ไม่ใช้น้ำมันทอด, ไม่มี MSG, วัตถุดิบพรีเมียม) ใช้ basic shape icon สไตล์เดียวกับโลโก้
4. **สินค้าของเรา (Products Section)** — การ์ดสินค้า 3 ใบ เรียงแนวนอน (responsive เป็นแนวตั้งบนมือถือ): แต่ละใบมีรูปสินค้า (generate), ชื่อสินค้า, คำอธิบายสั้น, ราคา, ปุ่ม "หยิบใส่ตะกร้า"
5. **เกี่ยวกับเรา (Story Section)** — พื้นหลังครีม, ข้อความเล่าเรื่องแบรนด์สั้นๆ + รูป/ไอคอน blob ประกอบ
6. **รีวิวลูกค้า (Testimonials)** — การ์ด 3 ใบ พื้นขาวขอบมน มี blob สีเขียวอ่อนแซมมุม
7. **CTA Section ปิดท้าย** — พื้นเขียวเข้ม (`#2E3A1F`) ตัวหนังสือสีขาว/ครีม ชวนสั่งซื้อ/ติดตาม
8. **Footer** — โลโก้เล็ก, ลิงก์โซเชียล, ที่อยู่/ติดต่อ, ลิขสิทธิ์ พื้นสีขาวหรือครีม เส้นขอบบนสีเขียว

## 4. สินค้าที่ต้องมี (3 รายการ) + Prompt เจนรูปสินค้า

ให้ generate รูปสินค้าแบบสมจริง (product photography) พื้นหลังโปร่งใสหรือสีขาวสตูดิโอ แสงนุ่ม โทนสีเข้ากับแบรนด์ (เขียวเข้ม/ครีม/ขาว) มุมกล้อง 3/4 ท็อปดาวน์เล็กน้อย

### 4.1 สาหร่ายอบกรอบแผ่น (Seaweed Sheet)
- **ชื่อสินค้า:** สาหร่ายอบกรอบแผ่น รสออริจินัล
- **คำอธิบาย:** สาหร่ายแผ่นอบกรอบ กรอบทุกคำ ไม่ใช้น้ำมันทอด เหมาะทานเล่นหรือห่อข้าว
- **ราคา (ตัวอย่าง):** 39 บาท / ห่อ
- **Image prompt:**
  > "Product photography of crispy roasted seaweed sheets snack, dark green textured seaweed sheet stacked neatly, placed on a minimal cream-colored ceramic plate, soft studio lighting, white background, some sesame seeds scattered around, top-down 3/4 angle, clean minimalist food packaging photography style, high detail texture, no text, no logo"

### 4.2 สาหร่ายม้วนอบกรอบ รสเข้มข้น (Seaweed Roll)
- **ชื่อสินค้า:** สาหร่ายม้วนอบกรอบ รสเข้มข้น
- **คำอธิบาย:** สาหร่ายม้วนแท่งกรอบ หอมเข้มข้น พกพาสะดวก ทานเพลินได้ทุกที่ทุกเวลา
- **ราคา (ตัวอย่าง):** 35 บาท / ห่อ
- **Image prompt:**
  > "Product photography of crispy seaweed rolls (rolled tube-shaped seaweed snack sticks), arranged in a small cream bowl and scattered beside it, dark green glossy texture, soft natural lighting, white studio background, minimal styling, top-down angle, clean food snack photography, no text, no logo"

### 4.3 สาหร่ายผงโรยข้าว (Seaweed Flakes/Powder)
- **ชื่อสินค้า:** สาหร่ายอบกรอบผง โรยข้าว
- **คำอธิบาย:** สาหร่ายบดละเอียดกรอบ โรยข้าว โรยซุป เพิ่มรสชาติและคุณค่าทางโภชนาการ
- **ราคา (ตัวอย่าง):** 45 บาท / กระปุก
- **Image prompt:**
  > "Product photography of crispy seaweed flakes powder (furikake style) in a small glass jar with lid off, dark green fine flaky texture visible, a small wooden spoon scooping some flakes beside the jar, soft studio lighting, white background, minimal clean styling, top-down 3/4 angle, no text, no logo"

## 5. Decorative Graphics — Prompt สำหรับ Blob/Basic Shape ตกแต่งเว็บ (สไตล์เดียวกับโลโก้)

สร้างเป็นภาพ **flat vector, basic organic blob shapes, minimal, ไม่มีเงา 3D**, ใช้สี palette ด้านบน สำหรับใช้เป็น background decoration/section divider ของเว็บ (ไม่ใช่รูปสินค้า)

1. **Blob พื้นหลัง Hero:**
   > "Flat vector illustration, single organic blob shape (irregular rounded circle), cream/sand color (#F6E7CE), minimal flat design, no gradient, no shadow, no outline, simple background decoration shape, transparent background"

2. **Blob เขียวอ่อนแซมมุม (การ์ด/testimonial):**
   > "Flat vector illustration, small organic blob shape, light leaf green color (#A9C25A), minimal flat design, no shadow, no texture, simple decorative accent shape, transparent background"

3. **Dot pattern ตกแต่ง (ล้อลายจุดบนสาหร่ายในโลโก้):**
   > "Flat vector illustration, scattered small circular dots pattern, light green color (#A9C25A) dots on transparent background, minimal, evenly random placement, no shadow, no gradient, simple decorative texture element"

4. **เส้นขีด/sparkle แบบในโลโก้ (สองข้างโลโก้):**
   > "Flat vector illustration, two simple curved sparkle/motion lines (comma-like shapes), medium olive green color (#6E8B3D), minimal flat icon, no shadow, no gradient, decorative accent element, transparent background"

5. **Divider shape คั่น section (คลื่นมนๆ):**
   > "Flat vector illustration, wide organic wavy blob shape used as a section divider, dark olive green color (#2E3A1F), minimal flat design, smooth rounded wave edges, no texture, no shadow, transparent background, horizontal orientation"

6. **ไอคอนจุดเด่นสินค้า (feature icons) 3-4 แบบ:** (กรอบ, ไม่ทอด, ไม่มี MSG, วัตถุดิบพรีเมียม)
   > "Flat vector icon set, minimal line-and-shape style, rounded simple shapes, dark olive green (#2E3A1F) and medium leaf green (#6E8B3D) two-tone color, icons representing: crispy texture, no-frying/healthy, no MSG, premium ingredients, consistent minimal icon style, transparent background, no shadow, no gradient"

## 6. Typography

- **หัวข้อ (Heading):** ฟอนต์กลมมน หนา (rounded bold, bubbly) ให้ฟีลเดียวกับโลโก้ เช่น "Baloo 2", "Fredoka", หรือฟอนต์ไทยกลมมนเช่น "Prompt" (weight หนา), "Mali Bold"
- **เนื้อหา (Body):** ฟอนต์อ่านง่าย เช่น "Noto Sans Thai", "Sarabun", "Prompt" (weight ปกติ)
- **สีตัวอักษร:** headline ใช้ `#2B2B26` หรือสลับเขียวเข้มบางจุด, body ใช้ `#2B2B26` ที่ opacity ~85%

## 7. เทคนิค/ข้อกำหนดเว็บ

- ทำเป็น **single page** (ไม่มีหลาย route) เลื่อนอ่านตาม section ด้านบนทั้งหมด
- Responsive: Desktop / Tablet / Mobile (การ์ดสินค้าเรียงจาก 3 คอลัมน์ → 1 คอลัมน์บนมือถือ)
- ปุ่ม CTA ทุกปุ่มเป็นทรงมน (rounded-full หรือ border-radius สูง) ให้เข้ากับสไตล์โลโก้กลมมน
- การ์ดสินค้า/รีวิว ใช้ขอบมน (border-radius ~16-24px) เงาอ่อนๆ (soft shadow) ไม่ใช้เงาหนัก
- ใส่ animation เล็กน้อยตอน scroll เข้า section (fade-up) และ hover เด้งเบาๆ ที่การ์ดสินค้า/ปุ่ม
- แนบโลโก้ที่ผู้ใช้ให้มาไว้ใน Navbar และ Footer

---

**สรุป:** เว็บพื้นขาวสะอาดตา แซมด้วยครีม/เขียวจากโลโก้ มี 3 สินค้า (แผ่น/ม้วน/ผง) พร้อม prompt เจนรูปสินค้าและ blob ตกแต่งให้ครบ พร้อมนำไปสร้างเว็บ single page ได้ทันที
