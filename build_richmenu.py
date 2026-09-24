import os
from PIL import Image, ImageDraw, ImageFont

def create_rich_menu():
    W, H = 1200, 810
    
    # Base Image
    base = Image.new("RGBA", (W, H), (252, 250, 246, 255))
    draw = ImageDraw.Draw(base)
    
    # Load fonts
    font_dir = "temp_fonts"
    f_title_xl = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 40)
    f_title_lg = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 30)
    f_title_md = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 26)
    f_title_sm = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 20)
    f_body_lg  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 20)
    f_body_md  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 17)
    f_body_sm  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 15)
    f_tag      = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 14)
    f_btn      = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 19)

    # Palette
    C_WHITE       = (255, 255, 255, 255)
    C_CREAM_LIGHT = (253, 250, 245, 255)
    C_DARK_OLIVE  = (46, 58, 31, 255)
    C_LEAF_GREEN  = (105, 136, 56, 255)
    C_LIGHT_GREEN = (169, 194, 90, 255)
    C_SOFT_GREEN  = (232, 242, 215, 255)
    C_AMBER       = (225, 115, 15, 255)
    C_AMBER_SOFT  = (254, 242, 220, 255)
    C_AMBER_BORDER= (245, 165, 55, 255)
    C_MUTED       = (115, 115, 105, 255)
    C_DIVIDER     = (224, 220, 212, 255)
    C_TEAL_SOFT   = (230, 242, 246, 255)
    C_TEAL_DARK   = (38, 92, 115, 255)

    # =============================================================
    # SECTION A: Top Banner (0, 0, 1200, 540)
    # =============================================================
    draw.rectangle([0, 0, W, 540], fill=C_CREAM_LIGHT)

    # Decorative background organic curves
    bg_decor = Image.new("RGBA", (W, 540), (0, 0, 0, 0))
    d_bg = ImageDraw.Draw(bg_decor)
    d_bg.ellipse([580, -90, 1360, 630], fill=(236, 244, 222, 150))
    d_bg.ellipse([700, -30, 1340, 560], fill=(225, 237, 206, 170))
    d_bg.ellipse([-50, -50, 300, 300], fill=(248, 240, 225, 120))

    # Dot pattern accents
    for x_d, y_d in [(570, 50), (595, 70), (575, 95), (1145, 430), (1170, 450), (1145, 475)]:
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
        target_lh = 92
        target_lw = int(lw * (target_lh / lh))
        logo_resized = logo_img.resize((target_lw, target_lh), Image.Resampling.LANCZOS)
        base.paste(logo_resized, (50, 35), logo_resized)

    # --- Top Subtitle Pill ---
    pill_x, pill_y = 50, 145
    draw.rounded_rectangle([pill_x, pill_y, pill_x + 380, pill_y + 32], radius=16, fill=C_SOFT_GREEN)
    draw.ellipse([pill_x + 12, pill_y + 9, pill_x + 23, pill_y + 20], fill=C_LEAF_GREEN)
    draw.text((pill_x + 30, pill_y + 5), "สาหร่ายแท้ 100% อบกรอบ ไม่ทอด ไม่อมน้ำมัน", font=f_body_sm, fill=C_DARK_OLIVE)

    # --- Main Headline & Tagline ---
    draw.text((50, 195), "ยินดีต้อนรับสู่ GrobGrob", font=f_title_xl, fill=C_DARK_OLIVE)
    draw.text((50, 255), "กรอบอร่อยเพลิน เคี้ยวสนุกทุกคำ!", font=f_title_lg, fill=C_LEAF_GREEN)
    draw.text((50, 310), "ช้อปออนไลน์ สั่งซื้อง่าย 24 ชม. ส่งตรงความสดใหม่ถึงบ้าน", font=f_body_md, fill=C_MUTED)

    # --- CTA Button (Website) ---
    btn_x, btn_y, btn_w, btn_h = 50, 370, 360, 68
    draw.rounded_rectangle([btn_x + 2, btn_y + 4, btn_x + btn_w + 2, btn_y + btn_h + 4], radius=34, fill=(46, 58, 31, 50))
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=34, fill=C_DARK_OLIVE)
    # Icon circle
    draw.ellipse([btn_x + 16, btn_y + 14, btn_x + 56, btn_y + 54], fill=C_LEAF_GREEN)
    draw.rectangle([btn_x + 28, btn_y + 30, btn_x + 46, btn_y + 42], fill=C_WHITE)
    draw.ellipse([btn_x + 30, btn_y + 43, btn_x + 35, btn_y + 48], fill=C_WHITE)
    draw.ellipse([btn_x + 40, btn_y + 43, btn_x + 45, btn_y + 48], fill=C_WHITE)
    draw.text((btn_x + 68, btn_y + 19), "เข้าสู่หน้าเว็บไซต์หลัก ›", font=f_title_md, fill=C_WHITE)

    # Free shipping note
    draw.ellipse([btn_x + 8, btn_y + 88, btn_x + 20, btn_y + 100], fill=C_AMBER)
    draw.text((btn_x + 26, btn_y + 82), "ส่งฟรีทั่วประเทศ เมื่อสั่งซื้อครบ 150 บาท", font=f_body_md, fill=C_DARK_OLIVE)

    # --- Right Side: 3 Clean Product Showcase Cards ---
    prod_cards = [
        {"file": "assets/seaweed-sheet.png", "title": "สาหร่ายแผ่น", "sub": "กรอบเต็มแผ่น", "pos": (595, 45),  "size": (175, 175)},
        {"file": "assets/seaweed-roll.png",  "title": "สาหร่ายม้วน",  "sub": "กรุบกรอบสะใจ", "pos": (790, 45),  "size": (175, 175)},
        {"file": "assets/seaweed-flakes.png","title": "ผงโรยข้าว",   "sub": "หอมคลุกเคล้า", "pos": (985, 45),  "size": (175, 175)}
    ]

    for p in prod_cards:
        px, py = p["pos"]
        pw, ph = p["size"]
        card_h = ph + 56
        
        # Shadow
        draw.rounded_rectangle([px + 3, py + 5, px + pw + 3, py + card_h + 5], radius=20, fill=(0, 0, 0, 24))
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
    trust_x, trust_y, trust_w, trust_h = 595, 310, 565, 130
    draw.rounded_rectangle([trust_x + 3, trust_y + 4, trust_x + trust_w + 3, trust_y + trust_h + 4], radius=20, fill=(0, 0, 0, 18))
    draw.rounded_rectangle([trust_x, trust_y, trust_x + trust_w, trust_y + trust_h], radius=20, fill=(255, 255, 255, 240), outline=(225, 235, 215, 255), width=2)
    
    # Trust banner content
    draw.text((trust_x + 22, trust_y + 16), "ความอร่อยการันตี 3 ซีรีส์ยอดนิยม 12 รสชาติ", font=f_title_sm, fill=C_DARK_OLIVE)
    draw.text((trust_x + 22, trust_y + 46), "คัดสรรสาหร่ายเกาหลีเกรดพรีเมียม สด สะอาด ปลอดภัย", font=f_body_sm, fill=C_MUTED)
    
    # 3 Trust Tags
    t_badges = ["อบไม่ทอด 100%", "มี อย. รับรอง", "ส่งไวใน 1-2 วัน"]
    tb_x = trust_x + 22
    for tb_text in t_badges:
        bbox = draw.textbbox((0, 0), tb_text, font=f_tag)
        bw = bbox[2] - bbox[0] + 24
        draw.rounded_rectangle([tb_x, trust_y + 78, tb_x + bw, trust_y + 110], radius=16, fill=C_SOFT_GREEN)
        draw.ellipse([tb_x + 8, trust_y + 90, tb_x + 16, trust_y + 98], fill=C_LEAF_GREEN)
        draw.text((tb_x + 20, trust_y + 84), tb_text, font=f_tag, fill=C_DARK_OLIVE)
        tb_x += bw + 14

    # =============================================================
    # GRID DIVIDERS
    # =============================================================
    draw.line([(0, 540), (W, 540)], fill=C_DIVIDER, width=3)
    draw.line([(400, 540), (400, H)], fill=C_DIVIDER, width=3)
    draw.line([(800, 540), (800, H)], fill=C_DIVIDER, width=3)

    # =============================================================
    # SECTION B: "สินค้า" (0, 540, 400, 810)
    # =============================================================
    draw.rectangle([0, 543, 398, H], fill=C_WHITE)
    draw.rectangle([0, 540, 398, 546], fill=C_LEAF_GREEN)

    # Category Pill
    draw.rounded_rectangle([25, 560, 130, 590], radius=15, fill=C_SOFT_GREEN)
    draw.text((38, 565), "12 รสชาติ", font=f_tag, fill=C_DARK_OLIVE)

    # Content
    draw.text((25, 600), "สินค้าทั้งหมด", font=f_title_lg, fill=C_DARK_OLIVE)
    draw.text((25, 646), "แผ่น • ม้วน • โรยข้าว", font=f_body_lg, fill=C_LEAF_GREEN)
    draw.text((25, 678), "เลือกดูรสชาติโปรด สดใหม่ทุกซอง", font=f_body_sm, fill=C_MUTED)

    # Action Button
    b_btn_y = 730
    draw.rounded_rectangle([25, b_btn_y, 220, b_btn_y + 50], radius=25, fill=C_DARK_OLIVE)
    draw.text((50, b_btn_y + 12), "ดูเมนูสินค้า ›", font=f_btn, fill=C_WHITE)

    # Product Thumbnail on the right
    if os.path.exists("assets/roll_bbq.png"):
        p_b = Image.open("assets/roll_bbq.png").convert("RGBA")
        p_b = p_b.resize((126, 126), Image.Resampling.LANCZOS)
        mask_b = Image.new("L", (126, 126), 0)
        ImageDraw.Draw(mask_b).rounded_rectangle([0, 0, 126, 126], radius=18, fill=255)
        # Background card
        draw.rounded_rectangle([248, 586, 378, 716], radius=20, fill=(248, 245, 238, 255), outline=(225, 230, 218, 255), width=2)
        base.paste(p_b, (250, 588), mask_b)

    # =============================================================
    # SECTION C: "ส่วนลด" (400, 540, 800, 810)
    # =============================================================
    draw.rectangle([402, 543, 798, H], fill=(255, 253, 248, 255))
    draw.rectangle([402, 540, 798, 546], fill=C_AMBER)

    # Promo Pill
    draw.rounded_rectangle([425, 560, 560, 590], radius=15, fill=C_AMBER_SOFT)
    draw.text((438, 565), "PROMO CODE", font=f_tag, fill=C_AMBER)

    # Title
    draw.text((425, 600), "คูปองส่วนลด", font=f_title_lg, fill=C_DARK_OLIVE)

    # Voucher Code Box
    c_box_x, c_box_y = 425, 646
    draw.rounded_rectangle([c_box_x, c_box_y, c_box_x + 190, c_box_y + 36], radius=8, fill=(255, 243, 226, 255), outline=C_AMBER_BORDER, width=2)
    draw.text((c_box_x + 14, c_box_y + 6), "โค้ด: GROB10", font=f_title_sm, fill=(205, 85, 10, 255))
    draw.text((425, 688), "ลดทันที 10% ทุกคำสั่งซื้อ", font=f_body_sm, fill=C_MUTED)

    # Action Button
    draw.rounded_rectangle([425, b_btn_y, 615, b_btn_y + 50], radius=25, fill=C_AMBER)
    draw.text((450, b_btn_y + 12), "กดรับคูปอง ›", font=f_btn, fill=C_WHITE)

    # Ticket graphic on right of C
    t_layer = Image.new("RGBA", (130, 130), (0, 0, 0, 0))
    td = ImageDraw.Draw(t_layer)
    td.rounded_rectangle([10, 12, 120, 118], radius=16, fill=(255, 246, 232, 255), outline=C_AMBER_BORDER, width=2)
    td.ellipse([4, 55, 18, 75], fill=(255, 253, 248, 255), outline=C_AMBER_BORDER, width=2)
    td.ellipse([112, 55, 126, 75], fill=(255, 253, 248, 255), outline=C_AMBER_BORDER, width=2)
    for dy in range(25, 105, 12):
        td.line([(65, dy), (65, dy + 6)], fill=(230, 170, 100, 255), width=2)
    td.text((22, 32), "10%", font=f_title_lg, fill=(215, 80, 10, 255))
    td.text((30, 78), "OFF", font=f_title_sm, fill=C_DARK_OLIVE)
    base.alpha_composite(t_layer, (650, 590))
    draw = ImageDraw.Draw(base)

    # =============================================================
    # SECTION D: "ติดต่อเรา / แอดมิน" (800, 540, 1200, 810)
    # =============================================================
    draw.rectangle([802, 543, W, H], fill=C_WHITE)
    draw.rectangle([802, 540, W, 546], fill=C_DARK_OLIVE)

    # Care Pill
    draw.rounded_rectangle([825, 560, 955, 590], radius=15, fill=C_TEAL_SOFT)
    draw.text((838, 565), "ONLINE CARE", font=f_tag, fill=C_TEAL_DARK)

    # Title & Sub
    draw.text((825, 600), "ติดต่อสอบถาม", font=f_title_lg, fill=C_DARK_OLIVE)
    draw.text((825, 646), "แชทกับแอดมิน GrobGrob", font=f_body_lg, fill=C_LEAF_GREEN)
    draw.text((825, 678), "แจ้งชำระเงิน • พัสดุ • สมาชิก", font=f_body_sm, fill=C_MUTED)

    # Action Button
    draw.rounded_rectangle([825, b_btn_y, 1015, b_btn_y + 50], radius=25, fill=C_DARK_OLIVE)
    draw.text((852, b_btn_y + 12), "คุยกับแอดมิน ›", font=f_btn, fill=C_WHITE)

    # Chat Support illustration on right of D
    cs_layer = Image.new("RGBA", (130, 130), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cs_layer)
    cd.ellipse([8, 8, 122, 122], fill=(240, 247, 238, 255), outline=C_SOFT_GREEN, width=2)
    cd.rounded_rectangle([20, 24, 98, 74], radius=16, fill=C_LEAF_GREEN)
    cd.polygon([(34, 74), (48, 74), (28, 92)], fill=C_LEAF_GREEN)
    cd.ellipse([38, 45, 46, 53], fill=C_WHITE)
    cd.ellipse([54, 45, 62, 53], fill=C_WHITE)
    cd.ellipse([70, 45, 78, 53], fill=C_WHITE)
    cd.rounded_rectangle([55, 58, 115, 98], radius=14, fill=C_DARK_OLIVE)
    cd.polygon([(95, 98), (82, 98), (102, 112)], fill=C_DARK_OLIVE)
    cd.text((68, 68), "LINE", font=f_tag, fill=C_WHITE)
    base.alpha_composite(cs_layer, (1045, 590))
    draw = ImageDraw.Draw(base)

    # =============================================================
    # Corner Badges A, B, C, D
    # =============================================================
    lbl_font = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 16)
    
    # A
    draw.rounded_rectangle([W - 48, 18, W - 18, 44], radius=13, fill=(0, 0, 0, 18))
    draw.text((W - 38, 20), "A", font=lbl_font, fill=C_MUTED)
    
    # B
    draw.rounded_rectangle([360, 555, 388, 580], radius=12, fill=(0, 0, 0, 15))
    draw.text((369, 557), "B", font=lbl_font, fill=C_MUTED)
    
    # C
    draw.rounded_rectangle([760, 555, 788, 580], radius=12, fill=(0, 0, 0, 15))
    draw.text((769, 557), "C", font=lbl_font, fill=C_MUTED)
    
    # D
    draw.rounded_rectangle([W - 45, 555, W - 17, 580], radius=12, fill=(0, 0, 0, 15))
    draw.text((W - 35, 557), "D", font=lbl_font, fill=C_MUTED)

    # Save output
    output_png = "richmenu_1200x810.png"
    output_jpg = "richmenu_1200x810.jpg"
    base.convert("RGB").save(output_png, quality=95)
    base.convert("RGB").save(output_jpg, quality=92, optimize=True)
    base.convert("RGB").save("assets/richmenu_1200x810.png", quality=95)
    base.convert("RGB").save("assets/richmenu_1200x810.jpg", quality=92, optimize=True)
    print("Done! Re-generated rich menu successfully.")

if __name__ == "__main__":
    create_rich_menu()
