import os
from PIL import Image, ImageDraw, ImageFont

def create_rich_menu():
    W, H = 1200, 810
    SPLIT_Y = 405  # A is 1200x405, B/C/D are 400x405 each
    
    base = Image.new("RGBA", (W, H), (253, 251, 247, 255))
    draw = ImageDraw.Draw(base)
    
    # Load fonts (BIG & BOLD for LINE Mobile App)
    font_dir = "temp_fonts"
    f_hero_xl   = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 52)
    f_hero_sub  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 30)
    f_card_main = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 40)
    f_card_sub  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 24)
    f_btn_big   = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 26)
    f_btn_hero  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 28)
    f_badge     = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 19)
    f_prod_name = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 22)
    f_prod_tag  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 16)

    # Color Palette
    C_WHITE        = (255, 255, 255, 255)
    C_CREAM_LIGHT  = (254, 251, 246, 255)
    C_DARK_OLIVE   = (44, 56, 30, 255)
    C_LEAF_GREEN   = (102, 134, 52, 255)
    C_SOFT_GREEN   = (230, 242, 212, 255)
    C_AMBER        = (225, 115, 15, 255)
    C_AMBER_SOFT   = (255, 242, 218, 255)
    C_MUTED        = (120, 120, 110, 255)
    C_DIVIDER      = (220, 216, 208, 255)

    # =============================================================
    # SECTION A: Top Banner (1200 x 405)
    # =============================================================
    draw.rectangle([0, 0, W, SPLIT_Y], fill=C_CREAM_LIGHT)

    # Organic soft green background curves
    bg_decor = Image.new("RGBA", (W, SPLIT_Y), (0, 0, 0, 0))
    d_bg = ImageDraw.Draw(bg_decor)
    d_bg.ellipse([540, -100, 1380, 520], fill=(235, 244, 220, 160))
    d_bg.ellipse([680, -40, 1360, 470], fill=(224, 237, 204, 190))
    d_bg.ellipse([-60, -60, 300, 300], fill=(248, 240, 225, 130))
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
        target_lh = 84
        target_lw = int(lw * (target_lh / lh))
        logo_resized = logo_img.resize((target_lw, target_lh), Image.Resampling.LANCZOS)
        base.paste(logo_resized, (50, 25), logo_resized)

    # --- Headline ---
    draw.text((50, 122), "ช้อปออนไลน์ สั่งเลย!", font=f_hero_xl, fill=C_DARK_OLIVE)
    draw.text((50, 188), "กรอบอร่อยเพลิน เคี้ยวสนุกทุกคำ", font=f_hero_sub, fill=C_LEAF_GREEN)

    # --- Big CTA Button ---
    btn_x, btn_y, btn_w, btn_h = 50, 252, 340, 72
    draw.rounded_rectangle([btn_x + 3, btn_y + 4, btn_x + btn_w + 3, btn_y + btn_h + 4], radius=36, fill=(44, 56, 30, 40))
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=36, fill=C_DARK_OLIVE)
    # Cart Icon inside button
    draw.ellipse([btn_x + 18, btn_y + 15, btn_x + 60, btn_y + 57], fill=C_LEAF_GREEN)
    draw.rectangle([btn_x + 30, btn_y + 32, btn_x + 48, btn_y + 44], fill=C_WHITE)
    draw.ellipse([btn_x + 32, btn_y + 45, btn_x + 37, btn_y + 50], fill=C_WHITE)
    draw.ellipse([btn_x + 42, btn_y + 45, btn_x + 47, btn_y + 50], fill=C_WHITE)
    draw.text((btn_x + 74, btn_y + 16), "เข้าสู่เว็บไซต์ ›", font=f_btn_hero, fill=C_WHITE)

    # Shipping badge pill
    badge_x, badge_y, badge_w, badge_h = 50, 338, 340, 44
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=22, fill=C_SOFT_GREEN)
    draw.ellipse([badge_x + 14, badge_y + 16, badge_x + 26, badge_y + 28], fill=C_AMBER)
    draw.text((badge_x + 34, badge_y + 8), "ส่งฟรีทั่วประเทศ เมื่อสั่งครบ 150.-", font=f_badge, fill=C_DARK_OLIVE)

    # --- Right Side: 3 Product Cards ---
    prod_cards = [
        {"file": "assets/seaweed-sheet.png", "title": "สาหร่ายแผ่น", "sub": "กรอบเต็มแผ่น", "pos": (585, 25),  "size": (185, 235)},
        {"file": "assets/seaweed-roll.png",  "title": "สาหร่ายม้วน",  "sub": "กรุบกรอบสะใจ", "pos": (785, 25),  "size": (185, 235)},
        {"file": "assets/seaweed-flakes.png","title": "ผงโรยข้าว",   "sub": "หอมคลุกข้าว", "pos": (985, 25),  "size": (185, 235)}
    ]

    for p in prod_cards:
        px, py = p["pos"]
        pw, ph = p["size"]
        
        # Soft shadow
        draw.rounded_rectangle([px + 2, py + 4, px + pw + 2, py + ph + 4], radius=22, fill=(0, 0, 0, 16))
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=22, fill=C_WHITE, outline=(225, 235, 215, 255), width=2)

        # Image
        if os.path.exists(p["file"]):
            img_p = Image.open(p["file"]).convert("RGBA")
            pad = 8
            img_w, img_h = pw - pad*2, ph - 68
            img_resized = img_p.resize((img_w, img_h), Image.Resampling.LANCZOS)
            mask_p = Image.new("L", (img_w, img_h), 0)
            ImageDraw.Draw(mask_p).rounded_rectangle([0, 0, img_w, img_h], radius=16, fill=255)
            base.paste(img_resized, (px + pad, py + pad), mask_p)

        # Large Product Name
        draw.text((px + 14, py + ph - 58), p["title"], font=f_prod_name, fill=C_DARK_OLIVE)
        draw.text((px + 14, py + ph - 28), p["sub"], font=f_prod_tag, fill=C_LEAF_GREEN)

    # Trust Pill Bar at the bottom of Right Side
    bar_x, bar_y, bar_w, bar_h = 585, 280, 585, 102
    draw.rounded_rectangle([bar_x + 2, bar_y + 4, bar_x + bar_w + 2, bar_y + bar_h + 4], radius=22, fill=(0, 0, 0, 14))
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=22, fill=(255, 255, 255, 245), outline=(225, 235, 215, 255), width=2)
    draw.text((bar_x + 26, bar_y + 18), "สาหร่ายเกาหลีแท้ 100% • 12 รสชาติสุดฮิต", font=f_card_sub, fill=C_DARK_OLIVE)
    draw.text((bar_x + 26, bar_y + 56), "อบไม่ทอด • ไม่ใช้วัตถุกันเสีย • มี อย. รับรอง", font=f_card_sub, fill=C_LEAF_GREEN)

    # =============================================================
    # GRID DIVIDERS
    # =============================================================
    draw.line([(0, SPLIT_Y), (W, SPLIT_Y)], fill=C_DIVIDER, width=4)
    draw.line([(400, SPLIT_Y), (400, H)], fill=C_DIVIDER, width=4)
    draw.line([(800, SPLIT_Y), (800, H)], fill=C_DIVIDER, width=4)

    # Helper function to paste centered 3D icon with clean rounded container
    def paste_centered_icon(icon_path, center_x, center_y, icon_size=155):
        if os.path.exists(icon_path):
            im = Image.open(icon_path).convert("RGBA")
            im = im.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
            
            mask = Image.new("L", (icon_size, icon_size), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, icon_size, icon_size], radius=30, fill=255)
            
            card_pad = 5
            bx = center_x - icon_size // 2
            by = center_y - icon_size // 2
            
            # Subtle card border & shadow
            draw.rounded_rectangle([bx - card_pad + 2, by - card_pad + 3, bx + icon_size + card_pad + 2, by + icon_size + card_pad + 3], radius=32, fill=(0, 0, 0, 12))
            draw.rounded_rectangle([bx - card_pad, by - card_pad, bx + icon_size + card_pad, by + icon_size + card_pad], radius=32, fill=C_WHITE, outline=(225, 230, 220, 255), width=2)
            
            base.paste(im, (bx, by), mask)

    # Helper to draw centered text
    def draw_centered_text(text, font, fill, center_x, y):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        x = center_x - text_w // 2
        draw.text((x, y), text, font=font, fill=fill)

    # Button coordinates
    btn_w_bottom = 330
    btn_h_bottom = 64
    btn_y_bottom = SPLIT_Y + 306

    # =============================================================
    # SECTION B: "สินค้าทั้งหมด" (400 x 405, x: 0..400, y: 405..810)
    # =============================================================
    draw.rectangle([0, SPLIT_Y + 4, 398, H], fill=C_WHITE)
    draw.rectangle([0, SPLIT_Y, 398, SPLIT_Y + 8], fill=C_LEAF_GREEN)

    # Centered 3D Snack Icon
    paste_centered_icon("assets/icon_3d_snack.jpg", 200, SPLIT_Y + 105, 150)

    # BIG BOLD Title & Subtitle
    draw_centered_text("สินค้าทั้งหมด", f_card_main, C_DARK_OLIVE, 200, SPLIT_Y + 192)
    draw_centered_text("12 รสชาติยอดนิยม", f_card_sub, C_LEAF_GREEN, 200, SPLIT_Y + 244)

    # Prominent Tap Button
    b_bx = 200 - btn_w_bottom // 2
    draw.rounded_rectangle([b_bx + 2, btn_y_bottom + 3, b_bx + btn_w_bottom + 2, btn_y_bottom + btn_h_bottom + 3], radius=32, fill=(44, 56, 30, 35))
    draw.rounded_rectangle([b_bx, btn_y_bottom, b_bx + btn_w_bottom, btn_y_bottom + btn_h_bottom], radius=32, fill=C_DARK_OLIVE)
    draw_centered_text("ดูสินค้าทั้งหมด ›", f_btn_big, C_WHITE, 200, btn_y_bottom + 15)

    # =============================================================
    # SECTION C: "คูปองส่วนลด" (400 x 405, x: 400..800, y: 405..810)
    # =============================================================
    draw.rectangle([402, SPLIT_Y + 4, 798, H], fill=(255, 253, 248, 255))
    draw.rectangle([402, SPLIT_Y, 798, SPLIT_Y + 8], fill=C_AMBER)

    # Centered 3D Coupon Icon
    paste_centered_icon("assets/icon_3d_coupon.jpg", 600, SPLIT_Y + 105, 150)

    # BIG BOLD Title & Subtitle
    draw_centered_text("คูปองส่วนลด", f_card_main, C_DARK_OLIVE, 600, SPLIT_Y + 192)
    draw_centered_text("ลด 10% โค้ด: GROB10", f_card_sub, C_AMBER, 600, SPLIT_Y + 244)

    # Prominent Tap Button
    c_bx = 600 - btn_w_bottom // 2
    draw.rounded_rectangle([c_bx + 2, btn_y_bottom + 3, c_bx + btn_w_bottom + 2, btn_y_bottom + btn_h_bottom + 3], radius=32, fill=(225, 115, 15, 35))
    draw.rounded_rectangle([c_bx, btn_y_bottom, c_bx + btn_w_bottom, btn_y_bottom + btn_h_bottom], radius=32, fill=C_AMBER)
    draw_centered_text("กดรับคูปอง ›", f_btn_big, C_WHITE, 600, btn_y_bottom + 15)

    # =============================================================
    # SECTION D: "ติดต่อสอบถาม" (400 x 405, x: 800..1200, y: 405..810)
    # =============================================================
    draw.rectangle([802, SPLIT_Y + 4, W, H], fill=C_WHITE)
    draw.rectangle([802, SPLIT_Y, W, SPLIT_Y + 8], fill=C_DARK_OLIVE)

    # Centered 3D Support Headset Icon
    paste_centered_icon("assets/icon_3d_support.jpg", 1000, SPLIT_Y + 105, 150)

    # BIG BOLD Title & Subtitle
    draw_centered_text("ติดต่อสอบถาม", f_card_main, C_DARK_OLIVE, 1000, SPLIT_Y + 192)
    draw_centered_text("แชทกับแอดมิน GrobGrob", f_card_sub, C_LEAF_GREEN, 1000, SPLIT_Y + 244)

    # Prominent Tap Button
    d_bx = 1000 - btn_w_bottom // 2
    draw.rounded_rectangle([d_bx + 2, btn_y_bottom + 3, d_bx + btn_w_bottom + 2, btn_y_bottom + btn_h_bottom + 3], radius=32, fill=(44, 56, 30, 35))
    draw.rounded_rectangle([d_bx, btn_y_bottom, d_bx + btn_w_bottom, btn_y_bottom + btn_h_bottom], radius=32, fill=C_DARK_OLIVE)
    draw_centered_text("คุยกับแอดมิน ›", f_btn_big, C_WHITE, 1000, btn_y_bottom + 15)

    # Subtle Section Label Badges in corner
    lbl_font = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 16)
    draw.rounded_rectangle([W - 48, 16, W - 18, 42], radius=13, fill=(0, 0, 0, 18))
    draw.text((W - 38, 18), "A", font=lbl_font, fill=C_MUTED)

    draw.rounded_rectangle([360, SPLIT_Y + 16, 388, SPLIT_Y + 41], radius=12, fill=(0, 0, 0, 15))
    draw.text((369, SPLIT_Y + 18), "B", font=lbl_font, fill=C_MUTED)

    draw.rounded_rectangle([760, SPLIT_Y + 16, 788, SPLIT_Y + 41], radius=12, fill=(0, 0, 0, 15))
    draw.text((769, SPLIT_Y + 18), "C", font=lbl_font, fill=C_MUTED)

    draw.rounded_rectangle([W - 45, SPLIT_Y + 16, W - 17, SPLIT_Y + 41], radius=12, fill=(0, 0, 0, 15))
    draw.text((W - 35, SPLIT_Y + 18), "D", font=lbl_font, fill=C_MUTED)

    # Save output
    output_png = "richmenu_1200x810.png"
    output_jpg = "richmenu_1200x810.jpg"
    base.convert("RGB").save(output_png, quality=95)
    base.convert("RGB").save(output_jpg, quality=92, optimize=True)
    base.convert("RGB").save("assets/richmenu_1200x810.png", quality=95)
    base.convert("RGB").save("assets/richmenu_1200x810.jpg", quality=92, optimize=True)
    print("Done! Generated refined mobile LINE rich menu.")

if __name__ == "__main__":
    create_rich_menu()
