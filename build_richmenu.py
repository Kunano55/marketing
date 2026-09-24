import os
from PIL import Image, ImageDraw, ImageFont

def create_rich_menu():
    W, H = 1200, 810
    SPLIT_Y = 405  # A is 1200x405, B, C, D are 400x405 each
    
    # Base Image
    base = Image.new("RGBA", (W, H), (252, 250, 246, 255))
    draw = ImageDraw.Draw(base)
    
    # Load fonts
    font_dir = "temp_fonts"
    f_title_xl = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 38)
    f_title_lg = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 30)
    f_title_md = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 25)
    f_title_sm = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 20)
    f_body_lg  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 20)
    f_body_md  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 17)
    f_body_sm  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 15)
    f_tag      = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 14)
    f_btn      = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 19)

    # Color Palette
    C_WHITE        = (255, 255, 255, 255)
    C_CREAM_LIGHT  = (253, 250, 245, 255)
    C_CREAM_WARM   = (248, 242, 230, 255)
    C_DARK_OLIVE   = (46, 58, 31, 255)
    C_LEAF_GREEN   = (105, 136, 56, 255)
    C_LIGHT_GREEN  = (169, 194, 90, 255)
    C_SOFT_GREEN   = (232, 242, 215, 255)
    C_AMBER        = (225, 115, 15, 255)
    C_AMBER_SOFT   = (254, 242, 220, 255)
    C_AMBER_BORDER = (245, 165, 55, 255)
    C_MUTED        = (115, 115, 105, 255)
    C_DIVIDER      = (224, 220, 212, 255)
    C_TEAL_SOFT    = (230, 242, 246, 255)
    C_TEAL_DARK    = (38, 92, 115, 255)

    # =============================================================
    # SECTION A: Top Banner (1200 x 405)
    # =============================================================
    draw.rectangle([0, 0, W, SPLIT_Y], fill=C_CREAM_LIGHT)

    # Decorative background organic curves
    bg_decor = Image.new("RGBA", (W, SPLIT_Y), (0, 0, 0, 0))
    d_bg = ImageDraw.Draw(bg_decor)
    d_bg.ellipse([580, -90, 1360, 520], fill=(236, 244, 222, 150))
    d_bg.ellipse([720, -40, 1340, 460], fill=(225, 237, 206, 170))
    d_bg.ellipse([-50, -50, 280, 280], fill=(248, 240, 225, 120))

    # Dot pattern accents
    for x_d, y_d in [(570, 30), (595, 50), (575, 75), (1145, 330), (1170, 350)]:
        d_bg.ellipse([x_d, y_d, x_d + 8, y_d + 8], fill=(169, 194, 90, 150))
    base.alpha_composite(bg_decor, (0, 0))
    draw = ImageDraw.Draw(base)

    # --- Logo ---
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path).convert("RGBA")
        bbox = logo_img.getbbox()
        if bbox:
            logo_img = logo_img.crop(bbox)
        lw, lh = logo_img.size
        target_lh = 78
        target_lw = int(lw * (target_lh / lh))
        logo_resized = logo_img.resize((target_lw, target_lh), Image.Resampling.LANCZOS)
        base.paste(logo_resized, (50, 25), logo_resized)

    # --- Welcome & Headline ---
    draw.text((50, 120), "ยินดีต้อนรับสู่ GrobGrob", font=f_title_xl, fill=C_DARK_OLIVE)
    draw.text((50, 172), "กรอบอร่อยเพลิน เคี้ยวสนุกทุกคำ!", font=f_title_lg, fill=C_LEAF_GREEN)
    draw.text((50, 218), "ช้อปออนไลน์ สั่งซื้อง่าย 24 ชม. ส่งตรงความสดใหม่ถึงบ้าน", font=f_body_md, fill=C_MUTED)

    # --- CTA Button (Website) ---
    btn_x, btn_y, btn_w, btn_h = 50, 265, 350, 62
    draw.rounded_rectangle([btn_x + 2, btn_y + 4, btn_x + btn_w + 2, btn_y + btn_h + 4], radius=31, fill=(46, 58, 31, 50))
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=31, fill=C_DARK_OLIVE)
    # Cart icon circle
    draw.ellipse([btn_x + 14, btn_y + 12, btn_x + 50, btn_y + 48], fill=C_LEAF_GREEN)
    draw.rectangle([btn_x + 24, btn_y + 26, btn_x + 40, btn_y + 36], fill=C_WHITE)
    draw.ellipse([btn_x + 26, btn_y + 37, btn_x + 30, btn_y + 41], fill=C_WHITE)
    draw.ellipse([btn_x + 34, btn_y + 37, btn_x + 38, btn_y + 41], fill=C_WHITE)
    draw.text((btn_x + 60, btn_y + 16), "เข้าสู่หน้าเว็บไซต์หลัก ›", font=f_btn, fill=C_WHITE)

    # Free shipping note
    draw.ellipse([btn_x + 6, btn_y + 78, btn_x + 18, btn_y + 90], fill=C_AMBER)
    draw.text((btn_x + 24, btn_y + 73), "ส่งฟรีทั่วประเทศ เมื่อสั่งซื้อครบ 150 บาท", font=f_body_sm, fill=C_DARK_OLIVE)

    # --- Right Side: 3 Product Cards ---
    prod_cards = [
        {"file": "assets/seaweed-sheet.png", "title": "สาหร่ายแผ่น", "sub": "กรอบเต็มแผ่น", "pos": (595, 25),  "size": (175, 175)},
        {"file": "assets/seaweed-roll.png",  "title": "สาหร่ายม้วน",  "sub": "กรุบกรอบสะใจ", "pos": (790, 25),  "size": (175, 175)},
        {"file": "assets/seaweed-flakes.png","title": "ผงโรยข้าว",   "sub": "หอมคลุกเคล้า", "pos": (985, 25),  "size": (175, 175)}
    ]

    for p in prod_cards:
        px, py = p["pos"]
        pw, ph = p["size"]
        card_h = ph + 54
        
        # Shadow
        draw.rounded_rectangle([px + 3, py + 4, px + pw + 3, py + card_h + 4], radius=20, fill=(0, 0, 0, 22))
        # Card Background
        draw.rounded_rectangle([px, py, px + pw, py + card_h], radius=20, fill=C_WHITE, outline=(225, 235, 215, 255), width=2)

        # Image
        if os.path.exists(p["file"]):
            img_p = Image.open(p["file"]).convert("RGBA")
            pad = 8
            img_w, img_h = pw - pad*2, ph - pad*2
            img_resized = img_p.resize((img_w, img_h), Image.Resampling.LANCZOS)
            mask_p = Image.new("L", (img_w, img_h), 0)
            ImageDraw.Draw(mask_p).rounded_rectangle([0, 0, img_w, img_h], radius=14, fill=255)
            base.paste(img_resized, (px + pad, py + pad), mask_p)

        # Text below image
        draw.text((px + 12, py + ph - 2), p["title"], font=f_title_sm, fill=C_DARK_OLIVE)
        draw.text((px + 12, py + ph + 24), p["sub"], font=f_body_sm, fill=C_LEAF_GREEN)

    # --- Right Side Bottom: Highlights / Trust Banner ---
    trust_x, trust_y, trust_w, trust_h = 595, 290, 565, 85
    draw.rounded_rectangle([trust_x + 2, trust_y + 3, trust_x + trust_w + 2, trust_y + trust_h + 3], radius=16, fill=(0, 0, 0, 16))
    draw.rounded_rectangle([trust_x, trust_y, trust_x + trust_w, trust_y + trust_h], radius=16, fill=(255, 255, 255, 240), outline=(225, 235, 215, 255), width=2)
    
    t_badges = ["อบไม่ทอด 100%", "มี อย. รับรอง", "12 รสชาติยอดนิยม", "ส่งไว 1-2 วัน"]
    tb_x = trust_x + 18
    for tb_text in t_badges:
        bbox = draw.textbbox((0, 0), tb_text, font=f_tag)
        bw = bbox[2] - bbox[0] + 20
        draw.rounded_rectangle([tb_x, trust_y + 26, tb_x + bw, trust_y + 58], radius=16, fill=C_SOFT_GREEN)
        draw.ellipse([tb_x + 8, trust_y + 38, tb_x + 14, trust_y + 44], fill=C_LEAF_GREEN)
        draw.text((tb_x + 18, trust_y + 32), tb_text, font=f_tag, fill=C_DARK_OLIVE)
        tb_x += bw + 10

    # =============================================================
    # GRID DIVIDERS
    # =============================================================
    # Horizontal Divider at y = 405 (exact 1200x405 split)
    draw.line([(0, SPLIT_Y), (W, SPLIT_Y)], fill=C_DIVIDER, width=3)
    # Vertical Dividers in bottom section (3x 400x405)
    draw.line([(400, SPLIT_Y), (400, H)], fill=C_DIVIDER, width=3)
    draw.line([(800, SPLIT_Y), (800, H)], fill=C_DIVIDER, width=3)

    # =============================================================
    # SECTION B: "สินค้า" (400 x 405, x: 0..400, y: 405..810)
    # =============================================================
    draw.rectangle([0, SPLIT_Y + 3, 398, H], fill=C_WHITE)
    draw.rectangle([0, SPLIT_Y, 398, SPLIT_Y + 6], fill=C_LEAF_GREEN)

    # Category Pill
    draw.rounded_rectangle([30, SPLIT_Y + 28, 135, SPLIT_Y + 58], radius=15, fill=C_SOFT_GREEN)
    draw.text((43, SPLIT_Y + 33), "12 รสชาติ", font=f_tag, fill=C_DARK_OLIVE)

    # Content
    draw.text((30, SPLIT_Y + 68), "สินค้าทั้งหมด", font=f_title_lg, fill=C_DARK_OLIVE)
    draw.text((30, SPLIT_Y + 114), "แผ่น • ม้วน • โรยข้าว", font=f_body_lg, fill=C_LEAF_GREEN)
    draw.text((30, SPLIT_Y + 146), "เลือกรสชาติที่ใช่ สดใหม่ทุกซอง", font=f_body_sm, fill=C_MUTED)

    # Product Visual Display Card
    if os.path.exists("assets/roll_bbq.png"):
        p_b = Image.open("assets/roll_bbq.png").convert("RGBA")
        p_b = p_b.resize((130, 130), Image.Resampling.LANCZOS)
        mask_b = Image.new("L", (130, 130), 0)
        ImageDraw.Draw(mask_b).rounded_rectangle([0, 0, 130, 130], radius=18, fill=255)
        # Background card
        draw.rounded_rectangle([240, SPLIT_Y + 38, 376, SPLIT_Y + 174], radius=20, fill=(248, 245, 238, 255), outline=(225, 230, 218, 255), width=2)
        base.paste(p_b, (243, SPLIT_Y + 41), mask_b)

    # Feature List in B
    b_pts = ["• แผ่นใหญ่ อบกรอบเต็มคำ", "• ม้วนกรุบกรอบ เคี้ยวเพลิน", "• ผงโรยข้าว คลุกอะไรก็อร่อย"]
    for i, pt in enumerate(b_pts):
        draw.text((30, SPLIT_Y + 182 + (i * 28)), pt, font=f_body_sm, fill=C_DARK_OLIVE)

    # Action Button
    b_btn_y = SPLIT_Y + 310
    draw.rounded_rectangle([30, b_btn_y, 370, b_btn_y + 54], radius=27, fill=C_DARK_OLIVE)
    draw.text((120, b_btn_y + 14), "ดูเมนูสินค้าทั้งหมด ›", font=f_btn, fill=C_WHITE)

    # =============================================================
    # SECTION C: "ส่วนลด" (400 x 405, x: 400..800, y: 405..810)
    # =============================================================
    draw.rectangle([402, SPLIT_Y + 3, 798, H], fill=(255, 253, 248, 255))
    draw.rectangle([402, SPLIT_Y, 798, SPLIT_Y + 6], fill=C_AMBER)

    # Promo Pill
    draw.rounded_rectangle([430, SPLIT_Y + 28, 565, SPLIT_Y + 58], radius=15, fill=C_AMBER_SOFT)
    draw.text((443, SPLIT_Y + 33), "PROMO CODE", font=f_tag, fill=C_AMBER)

    # Title & Sub
    draw.text((430, SPLIT_Y + 68), "คูปองส่วนลด", font=f_title_lg, fill=C_DARK_OLIVE)
    draw.text((430, SPLIT_Y + 114), "ลดทันที 10% ทุกคำสั่งซื้อ", font=f_body_lg, fill=(205, 85, 10, 255))
    draw.text((430, SPLIT_Y + 146), "เพียงกรอกโค้ดตอนสั่งซื้อหน้าเว็บ", font=f_body_sm, fill=C_MUTED)

    # Voucher Ticket Box Graphic (Centered)
    v_box_x, v_box_y, v_box_w, v_box_h = 430, SPLIT_Y + 185, 340, 95
    # Ticket shape
    draw.rounded_rectangle([v_box_x, v_box_y, v_box_x + v_box_w, v_box_y + v_box_h], radius=14, fill=(255, 246, 230, 255), outline=C_AMBER_BORDER, width=2)
    # Side notches
    draw.ellipse([v_box_x - 10, v_box_y + 35, v_box_x + 10, v_box_y + 55], fill=(255, 253, 248, 255), outline=C_AMBER_BORDER, width=2)
    draw.ellipse([v_box_x + v_box_w - 10, v_box_y + 35, v_box_x + v_box_w + 10, v_box_y + 55], fill=(255, 253, 248, 255), outline=C_AMBER_BORDER, width=2)
    # Dashed divider inside voucher
    for dy in range(v_box_y + 12, v_box_y + v_box_h - 10, 10):
        draw.line([(v_box_x + 115, dy), (v_box_x + 115, dy + 5)], fill=(235, 175, 110, 255), width=2)
    
    # Left voucher content
    draw.text((v_box_x + 22, v_box_y + 16), "10%", font=f_title_xl, fill=(215, 80, 10, 255))
    draw.text((v_box_x + 36, v_box_y + 58), "DISCOUNT", font=f_tag, fill=C_DARK_OLIVE)
    # Right voucher content
    draw.text((v_box_x + 135, v_box_y + 20), "โค้ด: GROB10", font=f_title_md, fill=(205, 85, 10, 255))
    draw.text((v_box_x + 135, v_box_y + 56), "ใช้ได้ไม่จำกัดจำนวนครั้ง", font=f_body_sm, fill=C_MUTED)

    # Action Button
    c_btn_y = SPLIT_Y + 310
    draw.rounded_rectangle([430, c_btn_y, 770, c_btn_y + 54], radius=27, fill=C_AMBER)
    draw.text((530, c_btn_y + 14), "กดรับคูปองส่วนลด ›", font=f_btn, fill=C_WHITE)

    # =============================================================
    # SECTION D: "ติดต่อเรา / แอดมิน" (400 x 405, x: 800..1200, y: 405..810)
    # =============================================================
    draw.rectangle([802, SPLIT_Y + 3, W, H], fill=C_WHITE)
    draw.rectangle([802, SPLIT_Y, W, SPLIT_Y + 6], fill=C_DARK_OLIVE)

    # Care Pill
    draw.rounded_rectangle([830, SPLIT_Y + 28, 960, SPLIT_Y + 58], radius=15, fill=C_TEAL_SOFT)
    draw.text((843, SPLIT_Y + 33), "ONLINE CARE", font=f_tag, fill=C_TEAL_DARK)

    # Title & Sub
    draw.text((830, SPLIT_Y + 68), "ติดต่อสอบถาม", font=f_title_lg, fill=C_DARK_OLIVE)
    draw.text((830, SPLIT_Y + 114), "แชทกับแอดมิน GrobGrob", font=f_body_lg, fill=C_LEAF_GREEN)
    draw.text((830, SPLIT_Y + 146), "บริการให้คำปรึกษาและดูแลลูกค้า", font=f_body_sm, fill=C_MUTED)

    # Clean bullet points in D
    d_pts = [
        "• สอบถามรายละเอียดสินค้า",
        "• ติดตามสถานะพัสดุ / จัดส่ง",
        "• สมัครสมาชิก & รับสิทธิ์พิเศษ"
    ]
    for i, pt in enumerate(d_pts):
        draw.text((830, SPLIT_Y + 182 + (i * 28)), pt, font=f_body_sm, fill=C_DARK_OLIVE)

    # Action Button
    d_btn_y = SPLIT_Y + 310
    draw.rounded_rectangle([830, d_btn_y, 1170, d_btn_y + 54], radius=27, fill=C_DARK_OLIVE)
    draw.text((930, d_btn_y + 14), "คุยกับแอดมินทันที ›", font=f_btn, fill=C_WHITE)

    # =============================================================
    # Corner Badges A, B, C, D
    # =============================================================
    lbl_font = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 16)
    
    # A
    draw.rounded_rectangle([W - 48, 16, W - 18, 42], radius=13, fill=(0, 0, 0, 18))
    draw.text((W - 38, 18), "A", font=lbl_font, fill=C_MUTED)
    
    # B
    draw.rounded_rectangle([360, SPLIT_Y + 15, 388, SPLIT_Y + 40], radius=12, fill=(0, 0, 0, 15))
    draw.text((369, SPLIT_Y + 17), "B", font=lbl_font, fill=C_MUTED)
    
    # C
    draw.rounded_rectangle([760, SPLIT_Y + 15, 788, SPLIT_Y + 40], radius=12, fill=(0, 0, 0, 15))
    draw.text((769, SPLIT_Y + 17), "C", font=lbl_font, fill=C_MUTED)
    
    # D
    draw.rounded_rectangle([W - 45, SPLIT_Y + 15, W - 17, SPLIT_Y + 40], radius=12, fill=(0, 0, 0, 15))
    draw.text((W - 35, SPLIT_Y + 17), "D", font=lbl_font, fill=C_MUTED)

    # Save output
    output_png = "richmenu_1200x810.png"
    output_jpg = "richmenu_1200x810.jpg"
    base.convert("RGB").save(output_png, quality=95)
    base.convert("RGB").save(output_jpg, quality=92, optimize=True)
    base.convert("RGB").save("assets/richmenu_1200x810.png", quality=95)
    base.convert("RGB").save("assets/richmenu_1200x810.jpg", quality=92, optimize=True)
    print("Done! Re-generated rich menu with clean typography.")

if __name__ == "__main__":
    create_rich_menu()
