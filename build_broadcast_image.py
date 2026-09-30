import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

def draw_vector_heart(draw, cx, cy, size, fill):
    r = size // 2
    draw.ellipse([cx - size, cy - r, cx, cy + r], fill=fill)
    draw.ellipse([cx, cy - r, cx + size, cy + r], fill=fill)
    draw.polygon([(cx - size + 2, cy + 2), (cx + size - 2, cy + 2), (cx, cy + size + 2)], fill=fill)

def draw_vector_sparkle(draw, cx, cy, size, fill):
    draw.polygon([
        (cx, cy - size), (cx + size//4, cy - size//4),
        (cx + size, cy), (cx + size//4, cy + size//4),
        (cx, cy + size), (cx - size//4, cy + size//4),
        (cx - size, cy), (cx - size//4, cy - size//4)
    ], fill=fill)

def draw_vector_cart(draw, cx, cy, size, fill):
    # Shopping cart icon
    draw.rectangle([cx - size, cy - size//2, cx + size//2, cy + size//3], fill=fill)
    draw.polygon([(cx + size//2, cy - size//2), (cx + size, cy - size//2), (cx + size//2, cy + size//3)], fill=fill)
    draw.ellipse([cx - size//2, cy + size//2, cx - size//4, cy + size//2 + size//3], fill=fill)
    draw.ellipse([cx + size//4, cy + size//2, cx + size//2, cy + size//2 + size//3], fill=fill)

def draw_vector_truck(draw, cx, cy, size, fill):
    # Delivery truck icon
    draw.rounded_rectangle([cx - size, cy - size//2, cx + size//3, cy + size//2], radius=2, fill=fill)
    draw.polygon([(cx + size//3, cy - size//4), (cx + size, cy - size//4), (cx + size, cy + size//2), (cx + size//3, cy + size//2)], fill=fill)
    draw.ellipse([cx - size//2 - 2, cy + size//2, cx - size//4, cy + size//2 + size//2], fill=fill)
    draw.ellipse([cx + size//2, cy + size//2, cx + size//2 + size//3, cy + size//2 + size//2], fill=fill)

def build_broadcast_image():
    W, H = 1080, 1080
    
    # Palette
    C_CREAM_BG     = (252, 249, 240, 255)  # #FCF9F0
    C_WHITE        = (255, 255, 255, 255)
    C_DARK_OLIVE   = (35, 54, 25, 255)     # #233619
    C_DEEP_FOREST  = (28, 58, 30, 255)     # #1C3A1E
    C_LEAF_GREEN   = (90, 126, 48, 255)    # #5A7E30
    C_LIGHT_GREEN  = (164, 195, 94, 255)   # #A4C35E
    C_SOFT_GREEN   = (230, 242, 212, 255)  # #E6F2D4
    C_AMBER        = (225, 115, 15, 255)   # #E1730F
    C_AMBER_SOFT   = (255, 243, 222, 255)
    C_MUTED        = (115, 120, 105, 255)
    C_DIVIDER      = (220, 216, 204, 255)

    # Fonts
    font_dir = "temp_fonts"
    f_title_xl   = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 48)
    f_title_lg   = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 34)
    f_title_md   = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 27)
    f_body_lg    = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 20)
    f_body_md    = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 18)
    f_btn        = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 24)
    f_badge      = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 17)
    f_ticket_big = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 64)

    # Canvas
    canvas = Image.new("RGBA", (W, H), C_CREAM_BG)
    draw = ImageDraw.Draw(canvas)

    # 1. Background Organic Shapes
    bg_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_bg = ImageDraw.Draw(bg_layer)
    # Top corner leaves
    d_bg.ellipse([-80, -80, 180, 180], fill=(145, 180, 85, 150))
    d_bg.ellipse([980, -80, 1160, 180], fill=(145, 180, 85, 150))
    # Bottom green hills
    d_bg.ellipse([-100, 840, 1180, 1220], fill=(132, 168, 76, 255))
    d_bg.ellipse([100, 880, 1200, 1240], fill=(90, 126, 48, 255))
    canvas.alpha_composite(bg_layer, (0, 0))
    draw = ImageDraw.Draw(canvas)

    # 2. Header: Logo & Special Friend Tag
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        logo_im = Image.open(logo_path).convert("RGBA")
        bbox = logo_im.getbbox()
        if bbox:
            logo_im = logo_im.crop(bbox)
        lw, lh = logo_im.size
        target_lh = 88
        target_lw = int(lw * (target_lh / lh))
        logo_im = logo_im.resize((target_lw, target_lh), Image.Resampling.LANCZOS)
        canvas.paste(logo_im, (50, 40), logo_im)

    # Tag: พิเศษเฉพาะเพื่อนใน LINE
    tag_w, tag_h = 280, 42
    tag_x, tag_y = W - tag_w - 50, 62
    draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=21, fill=C_SOFT_GREEN, outline=C_LIGHT_GREEN, width=2)
    draw_vector_sparkle(draw, tag_x + 22, tag_y + 21, 8, C_AMBER)
    draw.text((tag_x + 40, tag_y + 8), "พิเศษเฉพาะเพื่อนใน LINE", font=f_badge, fill=C_DARK_OLIVE)

    # 3. Main Headlines (Centered)
    def draw_centered_text(text, font, fill, center_x, y):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = center_x - tw // 2
        draw.text((x, y), text, font=font, fill=fill)

    draw_centered_text("กรอบอร่อยเพลิน เคี้ยวสนุกทุกคำ!", f_title_xl, C_DARK_OLIVE, W // 2, 145)
    draw_centered_text("สาหร่ายอบกรอบแท้ 100% • ไม่ใช้น้ำมันทอด • ไร้สารกันบูด", f_body_lg, C_LEAF_GREEN, W // 2, 205)

    # 4. Hero Visual: Snack Dish (Left) + Seaweed Mascot (Right)
    # Left: Appetizing Dish
    dish_path = "assets/seaweed_dish.jpg"
    if os.path.exists(dish_path):
        dish_im = Image.open(dish_path).convert("RGBA")
        dw, dh = 480, 370
        dish_resized = ImageOps.fit(dish_im, (dw, dh), Image.Resampling.LANCZOS)
        mask_d = Image.new("L", (dw, dh), 0)
        ImageDraw.Draw(mask_d).rounded_rectangle([0, 0, dw, dh], radius=28, fill=255)
        
        dx, dy = 50, 260
        draw.rounded_rectangle([dx + 3, dy + 5, dx + dw + 3, dy + dh + 5], radius=30, fill=(0, 0, 0, 22))
        canvas.paste(dish_resized, (dx, dy), mask_d)
        draw.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=28, outline=C_WHITE, width=4)

        # Flavor tag over dish
        draw.rounded_rectangle([dx + 20, dy + dh - 48, dx + 260, dy + dh - 12], radius=18, fill=C_DARK_OLIVE)
        draw.text((dx + 38, dy + dh - 42), "3 สไตล์ • 12 รสชาติเด็ด", font=f_badge, fill=C_WHITE)

    # Right: Cute Mascot with Speech Bubble
    mascot_path = "assets/mascot_transparent.png"
    if os.path.exists(mascot_path):
        m_im = Image.open(mascot_path).convert("RGBA")
        mw, mh = m_im.size
        target_mh = 330
        target_mw = int(mw * (target_mh / mh))
        m_im = m_im.resize((target_mw, target_mh), Image.Resampling.LANCZOS)
        canvas.paste(m_im, (630, 290), m_im)

    # Speech Bubble for Mascot
    b_cx, b_cy = 780, 270
    bw, bh = 220, 78
    bubble_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_b = ImageDraw.Draw(bubble_layer)
    d_b.ellipse([b_cx - bw//2, b_cy - bh//2, b_cx + bw//2, b_cy + bh//2], fill=C_WHITE, outline=C_DARK_OLIVE, width=3)
    d_b.polygon([(750, 305), (770, 305), (740, 335)], fill=C_WHITE)
    d_b.line([(750, 305), (740, 335)], fill=C_DARK_OLIVE, width=3)
    d_b.line([(770, 305), (740, 335)], fill=C_DARK_OLIVE, width=3)
    d_b.text((700, 248), "อร่อยทุกคำ", font=f_title_md, fill=C_DARK_OLIVE)
    draw_vector_heart(d_b, 848, 268, 9, C_LEAF_GREEN)
    canvas.alpha_composite(bubble_layer, (0, 0))
    draw = ImageDraw.Draw(canvas)

    # 5. Promo Coupon Card (Full Width in Center-Bottom)
    promo_box_w = 980
    promo_box_h = 220
    px = (W - promo_box_w) // 2
    py = 665

    # Deep green container card
    draw.rounded_rectangle([px + 3, py + 5, px + promo_box_w + 3, py + promo_box_h + 5], radius=28, fill=(0, 0, 0, 24))
    draw.rounded_rectangle([px, py, px + promo_box_w, py + promo_box_h], radius=28, fill=C_DEEP_FOREST)

    # Left: White Ticket
    tw, th = 430, 160
    tx, ty = px + 30, py + 30
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=18, fill=C_WHITE)
    draw.ellipse([tx - 12, ty + th//2 - 12, tx + 12, ty + th//2 + 12], fill=C_DEEP_FOREST)
    draw.ellipse([tx + tw - 12, ty + th//2 - 12, tx + tw + 12, ty + th//2 + 12], fill=C_DEEP_FOREST)
    dash_x = tx + 160
    for dy in range(ty + 14, ty + th - 14, 12):
        draw.line([(dash_x, dy), (dash_x, dy + 6)], fill=(200, 205, 195, 255), width=2)
    # Ticket content
    draw.text((tx + 26, ty + 20), "ลดทันที", font=f_body_lg, fill=C_DARK_OLIVE)
    draw.text((tx + 22, ty + 50), "10%", font=f_ticket_big, fill=C_DEEP_FOREST)
    # Promo code pill
    draw.rounded_rectangle([tx + 180, ty + 24, tx + 400, ty + 70], radius=10, fill=C_AMBER_SOFT, outline=C_AMBER, width=2)
    draw.text((tx + 195, ty + 30), "โค้ด: GROB10", font=f_btn, fill=C_AMBER)
    draw.text((tx + 185, ty + 86), "ใช้ได้กับทุกคำสั่งซื้อ", font=f_body_md, fill=C_MUTED)
    draw.text((tx + 185, ty + 114), "ไม่จำกัดจำนวนครั้ง", font=f_body_md, fill=C_LEAF_GREEN)
    draw_vector_sparkle(draw, tx + 345, ty + 124, 6, C_AMBER)

    # Right: Free Shipping & Benefits
    rx = px + 500
    draw_vector_truck(draw, rx + 16, py + 52, 14, C_LIGHT_GREEN)
    draw.text((rx + 42, py + 36), "จัดส่งฟรีทั่วประเทศ", font=f_title_md, fill=C_WHITE)
    draw.text((rx + 42, py + 78), "เมื่อช้อปสินค้าครบ 150 บาทขึ้นไป", font=f_body_lg, fill=C_LIGHT_GREEN)
    
    # Bullet points
    draw.ellipse([rx + 42, py + 128, rx + 50, py + 136], fill=C_LIGHT_GREEN)
    draw.text((rx + 60, py + 120), "อบด้วยลมร้อน ไร้น้ำมัน 100%", font=f_body_md, fill=C_WHITE)
    draw.ellipse([rx + 42, py + 162, rx + 50, py + 170], fill=C_LIGHT_GREEN)
    draw.text((rx + 60, py + 154), "ไร้ผงชูรสและสารกันบูด สด สะอาด", font=f_body_md, fill=C_WHITE)

    # 6. Bottom CTA Button Bar
    btn_w = 980
    btn_h = 74
    bx = (W - btn_w) // 2
    by = 930
    draw.rounded_rectangle([bx + 3, by + 4, bx + btn_w + 3, by + btn_h + 4], radius=37, fill=(0, 0, 0, 30))
    draw.rounded_rectangle([bx, by, bx + btn_w, by + btn_h], radius=37, fill=C_DARK_OLIVE, outline=C_LIGHT_GREEN, width=2)
    draw_vector_cart(draw, bx + 160, by + 37, 14, C_LIGHT_GREEN)
    draw_centered_text("สั่งซื้อออนไลน์ได้แล้ววันนี้ คลิกเข้าสู่เว็บไซต์ ›", f_btn, C_WHITE, W // 2 + 15, by + 19)

    # Save output
    output_png = "broadcast_promo.png"
    output_jpg = "broadcast_promo.jpg"
    canvas.convert("RGB").save(output_png, quality=95)
    canvas.convert("RGB").save(output_jpg, quality=92, optimize=True)
    canvas.convert("RGB").save("assets/broadcast_promo.png")
    canvas.convert("RGB").save("assets/broadcast_promo.jpg", quality=92, optimize=True)
    print(f"Generated {output_png} and {output_jpg} for broadcast!")

if __name__ == "__main__":
    build_broadcast_image()
