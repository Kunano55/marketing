import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

def draw_vector_heart(draw, cx, cy, size, fill):
    # Draw smooth vector heart
    r = size // 2
    draw.ellipse([cx - size, cy - r, cx, cy + r], fill=fill)
    draw.ellipse([cx, cy - r, cx + size, cy + r], fill=fill)
    draw.polygon([(cx - size + 2, cy + 2), (cx + size - 2, cy + 2), (cx, cy + size + 2)], fill=fill)

def draw_vector_sparkle(draw, cx, cy, size, fill):
    # Draw 4-point sparkle star
    draw.polygon([
        (cx, cy - size), (cx + size//4, cy - size//4),
        (cx + size, cy), (cx + size//4, cy + size//4),
        (cx, cy + size), (cx - size//4, cy + size//4),
        (cx - size, cy), (cx - size//4, cy - size//4)
    ], fill=fill)

def draw_smooth_leaf(draw, cx, cy, size, fill):
    # Beautiful organic leaf
    draw.polygon([
        (cx - size, cy + size//2), (cx - size//2, cy - size),
        (cx + size, cy - size//2), (cx + size//2, cy + size)
    ], fill=fill)
    draw.ellipse([cx - size//2, cy - size//2, cx + size//2, cy + size//2], fill=fill)

def build_scratch_rich_menu():
    W, H = 1200, 810
    SPLIT_Y = 405
    
    # Palette (Warm Organic Seaweed Aesthetic)
    C_CREAM_BG     = (252, 249, 240, 255)  # #FCF9F0 Warm paper cream
    C_WHITE        = (255, 255, 255, 255)
    C_DARK_OLIVE   = (35, 54, 25, 255)     # #233619 Primary deep text
    C_DEEP_FOREST  = (28, 58, 30, 255)     # #1C3A1E Deep green for Box C
    C_LEAF_GREEN   = (90, 126, 48, 255)    # #5A7E30 Vibrant leaf green
    C_LIGHT_GREEN  = (164, 195, 94, 255)   # #A4C35E Accent green
    C_SOFT_GREEN   = (230, 242, 212, 255)  # #E6F2D4 Soft green fill
    C_AMBER        = (225, 115, 15, 255)   # #E1730F Promo orange
    C_AMBER_SOFT   = (255, 243, 222, 255)
    C_MUTED        = (115, 120, 105, 255)
    C_DIVIDER      = (220, 216, 204, 255)

    # Fonts
    font_dir = "temp_fonts"
    f_hero_title = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 48)
    f_hero_sub   = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 19)
    f_bubble     = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 22)
    
    f_card_title = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 30)
    f_card_sub   = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 16)
    f_btn        = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 20)
    f_badge      = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 16)
    f_tile_lbl   = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 17)
    
    f_ticket_big = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 68)
    f_ticket_md  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 22)

    # Base Canvas
    canvas = Image.new("RGBA", (W, H), C_CREAM_BG)
    draw = ImageDraw.Draw(canvas)

    # =============================================================
    # 1. SECTION A: Top Banner (1200 x 405)
    # =============================================================
    top_bg = Image.new("RGBA", (W, SPLIT_Y), (0, 0, 0, 0))
    d_top = ImageDraw.Draw(top_bg)

    # Rolling organic green hills at bottom of Section A
    d_top.ellipse([-100, 260, 1300, 520], fill=(132, 168, 76, 255))
    d_top.ellipse([-50, 300, 850, 510], fill=(105, 142, 58, 255))
    d_top.ellipse([500, 290, 1350, 510], fill=(80, 116, 44, 255))
    d_top.ellipse([-80, 330, 650, 480], fill=(68, 98, 36, 255))

    # Corner decorative leaves / foliage blobs
    d_top.ellipse([-70, -70, 160, 160], fill=(145, 180, 85, 160))
    d_top.ellipse([-30, -30, 90, 90], fill=(110, 150, 60, 180))
    d_top.ellipse([1100, -70, 1270, 160], fill=(145, 180, 85, 160))
    d_top.ellipse([1140, -30, 1240, 90], fill=(110, 150, 60, 180))

    canvas.alpha_composite(top_bg, (0, 0))
    draw = ImageDraw.Draw(canvas)

    # --- Official GrobGrob Logo on the Left ---
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        logo_im = Image.open(logo_path).convert("RGBA")
        bbox = logo_im.getbbox()
        if bbox:
            logo_im = logo_im.crop(bbox)
        lw, lh = logo_im.size
        target_lh = 135
        target_lw = int(lw * (target_lh / lh))
        logo_im = logo_im.resize((target_lw, target_lh), Image.Resampling.LANCZOS)
        canvas.paste(logo_im, (45, 50), logo_im)

    # --- Slogans in Center (Exact from Website) ---
    draw.text((435, 75), "กรอบอร่อยเพลิน", font=f_hero_title, fill=C_DARK_OLIVE)
    draw.text((435, 142), "เคี้ยวสนุกทุกคำ!", font=f_hero_title, fill=C_LEAF_GREEN)

    # Decorative brush underline under slogan
    draw.arc([430, 185, 790, 235], start=10, end=170, fill=C_DARK_OLIVE, width=4)

    # Website USP Tagline
    draw.text((385, 236), "สาหร่ายอบกรอบแท้ 100% • ไม่ใช้น้ำมันทอด • ไร้สารกันบูด", font=f_hero_sub, fill=C_DARK_OLIVE)
    draw.ellipse([365, 244, 375, 254], fill=C_LEAF_GREEN)
    draw.ellipse([845, 244, 855, 254], fill=C_LEAF_GREEN)

    # Feature Pill Badge
    badge_w, badge_h = 340, 38
    badge_x, badge_y = 430, 282
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=19, fill=C_WHITE, outline=C_LIGHT_GREEN, width=2)
    draw_vector_sparkle(draw, badge_x + 22, badge_y + 19, 8, C_AMBER)
    draw.text((badge_x + 38, badge_y + 7), "กรอบสนั่น รสเข้มข้น ดีต่อสุขภาพ", font=f_badge, fill=C_DARK_OLIVE)

    # --- Mascot on the Right ---
    mascot_path = "assets/mascot_transparent.png"
    if os.path.exists(mascot_path):
        m_im = Image.open(mascot_path).convert("RGBA")
        mw, mh = m_im.size
        target_mh = 275
        target_mw = int(mw * (target_mh / mh))
        m_im = m_im.resize((target_mw, target_mh), Image.Resampling.LANCZOS)
        canvas.paste(m_im, (880, 105), m_im)

    # --- Speech Bubble above Mascot ---
    b_cx, b_cy = 1000, 70
    bw, bh = 195, 72
    bubble_layer = Image.new("RGBA", (W, SPLIT_Y), (0, 0, 0, 0))
    d_b = ImageDraw.Draw(bubble_layer)
    # Oval body
    d_b.ellipse([b_cx - bw//2, b_cy - bh//2, b_cx + bw//2, b_cy + bh//2], fill=C_WHITE, outline=C_DARK_OLIVE, width=3)
    # Tail pointing down to mascot
    d_b.polygon([(965, 100), (985, 100), (960, 126)], fill=C_WHITE)
    d_b.line([(965, 100), (960, 126)], fill=C_DARK_OLIVE, width=3)
    d_b.line([(985, 100), (960, 126)], fill=C_DARK_OLIVE, width=3)
    # Speech bubble text + vector green heart
    d_b.text((922, 52), "อร่อยทุกคำ", font=f_bubble, fill=C_DARK_OLIVE)
    draw_vector_heart(d_b, 1052, 68, 8, C_LEAF_GREEN)
    
    # Sparkle lines around mascot
    for sx1, sy1, sx2, sy2 in [(860, 75, 845, 60), (885, 55, 885, 35), (910, 65, 925, 50)]:
        d_b.line([(sx1, sy1), (sx2, sy2)], fill=C_DARK_OLIVE, width=3)
        
    canvas.alpha_composite(bubble_layer, (0, 0))
    draw = ImageDraw.Draw(canvas)

    # =============================================================
    # 2. SECTION B: "สินค้าของเรา" (400 x 405, x: 0..400, y: 405..810)
    # =============================================================
    b_card_pad = 12
    bx1, by1 = b_card_pad, SPLIT_Y + b_card_pad
    bx2, by2 = 400 - b_card_pad, H - b_card_pad
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=24, fill=C_CREAM_BG, outline=(230, 226, 212, 255), width=2)

    # Header Row in B
    draw_smooth_leaf(draw, bx1 + 28, by1 + 26, 10, C_LEAF_GREEN)
    draw.text((bx1 + 48, by1 + 10), "สินค้าของเรา", font=f_card_title, fill=C_DARK_OLIVE)
    draw.text((bx1 + 48, by1 + 46), "Our Products", font=f_card_sub, fill=C_LEAF_GREEN)
    # Circular green arrow button
    arrow_bx, arrow_by = bx2 - 46, by1 + 18
    draw.ellipse([arrow_bx, arrow_by, arrow_bx + 32, arrow_by + 32], fill=C_LEAF_GREEN)
    draw.polygon([(arrow_bx + 13, arrow_by + 9), (arrow_bx + 21, arrow_by + 16), (arrow_bx + 13, arrow_by + 23)], fill=C_WHITE)

    # Visual in B: Seaweed dish
    dish_path = "assets/seaweed_dish.jpg"
    if os.path.exists(dish_path):
        dish_im = Image.open(dish_path).convert("RGBA")
        dish_w, dish_h = 336, 224
        dish_resized = ImageOps.fit(dish_im, (dish_w, dish_h), Image.Resampling.LANCZOS)
        mask_d = Image.new("L", (dish_w, dish_h), 0)
        ImageDraw.Draw(mask_d).rounded_rectangle([0, 0, dish_w, dish_h], radius=20, fill=255)
        
        dish_x = (400 - dish_w) // 2
        dish_y = by1 + 80
        draw.rounded_rectangle([dish_x + 2, dish_y + 3, dish_x + dish_w + 2, dish_y + dish_h + 3], radius=22, fill=(0, 0, 0, 20))
        canvas.paste(dish_resized, (dish_x, dish_y), mask_d)
        draw.rounded_rectangle([dish_x, dish_y, dish_x + dish_w, dish_y + dish_h], radius=20, outline=C_WHITE, width=3)

    # Bottom Tag in B
    tag_b_w = 320
    tag_b_x = (400 - tag_b_w) // 2
    tag_b_y = by2 - 46
    draw.rounded_rectangle([tag_b_x, tag_b_y, tag_b_x + tag_b_w, tag_b_y + 36], radius=18, fill=C_WHITE, outline=C_LIGHT_GREEN, width=2)
    draw.text((tag_b_x + 26, tag_b_y + 7), "สาหร่ายแผ่น • ม้วน • ผงโรยข้าว", font=f_badge, fill=C_DARK_OLIVE)

    # =============================================================
    # 3. SECTION C: "คูปองส่วนลด" (400 x 405, x: 400..800, y: 405..810)
    # =============================================================
    cx1, cy1 = 400 + b_card_pad, SPLIT_Y + b_card_pad
    cx2, cy2 = 800 - b_card_pad, H - b_card_pad
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=24, fill=C_DEEP_FOREST)

    # Header Row in C
    draw.polygon([(cx1 + 18, cy1 + 24), (cx1 + 28, cy1 + 14), (cx1 + 40, cy1 + 26), (cx1 + 30, cy1 + 36)], fill=C_WHITE)
    draw.ellipse([cx1 + 26, cy1 + 18, cx1 + 30, cy1 + 22], fill=C_DEEP_FOREST)
    draw.text((cx1 + 50, cy1 + 10), "คูปองส่วนลด", font=f_card_title, fill=C_WHITE)
    draw.text((cx1 + 50, cy1 + 46), "Special Offers", font=f_card_sub, fill=C_LIGHT_GREEN)
    # Circular white arrow button
    c_arrow_x, c_arrow_y = cx2 - 46, cy1 + 18
    draw.ellipse([c_arrow_x, c_arrow_y, c_arrow_x + 32, c_arrow_y + 32], fill=C_WHITE)
    draw.polygon([(c_arrow_x + 13, c_arrow_y + 9), (c_arrow_x + 21, c_arrow_y + 16), (c_arrow_x + 13, c_arrow_y + 23)], fill=C_DEEP_FOREST)

    # White Coupon Ticket (Center)
    t_w, t_h = 326, 185
    t_x = 400 + (400 - t_w) // 2
    t_y = cy1 + 80
    draw.rounded_rectangle([t_x, t_y, t_x + t_w, t_y + t_h], radius=18, fill=C_WHITE)
    # Semicircular cutouts
    draw.ellipse([t_x - 14, t_y + t_h//2 - 14, t_x + 14, t_y + t_h//2 + 14], fill=C_DEEP_FOREST)
    draw.ellipse([t_x + t_w - 14, t_y + t_h//2 - 14, t_x + t_w + 14, t_y + t_h//2 + 14], fill=C_DEEP_FOREST)
    # Dashed divider line
    dash_x = t_x + 234
    for dy in range(t_y + 15, t_y + t_h - 15, 12):
        draw.line([(dash_x, dy), (dash_x, dy + 6)], fill=(200, 205, 195, 255), width=2)

    # Ticket Content
    draw.text((t_x + 24, t_y + 14), "ลดทันที", font=f_ticket_md, fill=C_DARK_OLIVE)
    draw.text((t_x + 20, t_y + 40), "10%", font=f_ticket_big, fill=C_DEEP_FOREST)
    # Code Box inside ticket
    code_pill_w, code_pill_h = 168, 36
    draw.rounded_rectangle([t_x + 22, t_y + 132, t_x + 22 + code_pill_w, t_y + 132 + code_pill_h], radius=8, fill=C_AMBER_SOFT, outline=C_AMBER, width=2)
    draw.text((t_x + 36, t_y + 138), "โค้ด: GROB10", font=f_tile_lbl, fill=C_AMBER)
    # Right side of ticket
    draw.text((dash_x + 16, t_y + 40), "ช้อป", font=f_badge, fill=C_MUTED)
    draw.text((dash_x + 14, t_y + 65), "ครบ", font=f_badge, fill=C_MUTED)
    draw.text((dash_x + 10, t_y + 90), "150.-", font=f_card_sub, fill=C_DARK_OLIVE)
    draw.text((dash_x + 10, t_y + 115), "ส่งฟรี", font=f_card_sub, fill=C_LEAF_GREEN)

    # Bottom White Pill CTA Button in C
    c_btn_w = 326
    c_btn_h = 50
    c_btn_x = 400 + (400 - c_btn_w) // 2
    c_btn_y = by2 - 54
    draw.rounded_rectangle([c_btn_x, c_btn_y, c_btn_x + c_btn_w, c_btn_y + c_btn_h], radius=25, fill=C_WHITE)
    draw.text((c_btn_x + 68, c_btn_y + 13), "ดูโปรโมชั่นทั้งหมด ›", font=f_btn, fill=C_DEEP_FOREST)

    # =============================================================
    # 4. SECTION D: "อื่นๆ / More Info" (400 x 405, x: 800..1200, y: 405..810)
    # =============================================================
    dx1, dy1 = 800 + b_card_pad, SPLIT_Y + b_card_pad
    dx2, dy2 = 1200 - b_card_pad, H - b_card_pad
    draw.rounded_rectangle([dx1, dy1, dx2, dy2], radius=24, fill=C_CREAM_BG, outline=(230, 226, 212, 255), width=2)

    # Header Row in D
    grid_ix, grid_iy = dx1 + 18, dy1 + 18
    for gx in [grid_ix, grid_ix + 12]:
        for gy in [grid_iy, grid_iy + 12]:
            draw.rounded_rectangle([gx, gy, gx + 9, gy + 9], radius=2, outline=C_LEAF_GREEN, width=2)
    draw.text((dx1 + 48, dy1 + 10), "บริการ & ข้อมูล", font=f_card_title, fill=C_DARK_OLIVE)
    draw.text((dx1 + 48, dy1 + 46), "More Info", font=f_card_sub, fill=C_LEAF_GREEN)
    d_arrow_x, d_arrow_y = dx2 - 46, dy1 + 18
    draw.ellipse([d_arrow_x, d_arrow_y, d_arrow_x + 32, d_arrow_y + 32], fill=C_LEAF_GREEN)
    draw.polygon([(d_arrow_x + 13, d_arrow_y + 9), (d_arrow_x + 21, d_arrow_y + 16), (d_arrow_x + 13, d_arrow_y + 23)], fill=C_WHITE)

    # 4 White Rounded Tiles (2x2 Grid)
    tile_w, tile_h = 162, 126
    t_gap_x, t_gap_y = 12, 14
    start_tx = dx1 + 18
    start_ty = dy1 + 80

    tiles_data = [
        {"icon": "truck", "title": "วิธีการสั่งซื้อ", "col": 0, "row": 0},
        {"icon": "leaf",  "title": "เกี่ยวกับเรา",    "col": 1, "row": 0},
        {"icon": "headset","title": "ติดต่อเรา",     "col": 0, "row": 1},
        {"icon": "member", "title": "สมัครสมาชิก",   "col": 1, "row": 1}
    ]

    for item in tiles_data:
        ix = start_tx + item["col"] * (tile_w + t_gap_x)
        iy = start_ty + item["row"] * (tile_h + t_gap_y)
        
        # Shadow & white tile body
        draw.rounded_rectangle([ix + 2, iy + 3, ix + tile_w + 2, iy + tile_h + 3], radius=18, fill=(0, 0, 0, 12))
        draw.rounded_rectangle([ix, iy, ix + tile_w, iy + tile_h], radius=18, fill=C_WHITE, outline=(235, 238, 230, 255), width=2)
        
        icx, icy = ix + tile_w // 2, iy + 45
        
        if item["icon"] == "truck":
            draw.rounded_rectangle([icx - 22, icy - 14, icx + 6, icy + 10], radius=3, fill=C_LEAF_GREEN)
            draw.polygon([(icx + 6, icy - 6), (icx + 16, icy - 6), (icx + 22, icy + 10), (icx + 6, icy + 10)], fill=C_LEAF_GREEN)
            draw.ellipse([icx - 15, icy + 8, icx - 5, icy + 18], fill=C_DARK_OLIVE)
            draw.ellipse([icx + 9, icy + 8, icx + 19, icy + 18], fill=C_DARK_OLIVE)
        elif item["icon"] == "leaf":
            draw_smooth_leaf(draw, icx, icy, 12, C_LEAF_GREEN)
        elif item["icon"] == "headset":
            draw.arc([icx - 16, icy - 16, icx + 16, icy + 14], start=180, end=0, fill=C_LEAF_GREEN, width=4)
            draw.rounded_rectangle([icx - 20, icy - 2, icx - 12, icy + 14], radius=3, fill=C_DARK_OLIVE)
            draw.rounded_rectangle([icx + 12, icy - 2, icx + 20, icy + 14], radius=3, fill=C_DARK_OLIVE)
            draw.line([(icx + 16, icy + 10), (icx + 8, icy + 16)], fill=C_DARK_OLIVE, width=2)
            draw.ellipse([icx + 4, icy + 14, icx + 8, icy + 18], fill=C_LEAF_GREEN)
        elif item["icon"] == "member":
            draw.polygon([(icx - 18, icy + 12), (icx - 18, icy - 6), (icx - 9, icy + 2), (icx, icy - 12), (icx + 9, icy + 2), (icx + 18, icy - 6), (icx + 18, icy + 12)], fill=C_AMBER)
            draw.ellipse([icx - 2, icy - 16, icx + 2, icy - 12], fill=C_AMBER)
            draw.ellipse([icx - 20, icy - 10, icx - 16, icy - 6], fill=C_AMBER)
            draw.ellipse([icx + 16, icy - 10, icx + 20, icy - 6], fill=C_AMBER)
            draw.rectangle([icx - 18, icy + 10, icx + 18, icy + 14], fill=(190, 80, 10, 255))
            
        bbox = draw.textbbox((0, 0), item["title"], font=f_tile_lbl)
        tw = bbox[2] - bbox[0]
        draw.text((ix + (tile_w - tw) // 2, iy + 82), item["title"], font=f_tile_lbl, fill=C_DARK_OLIVE)

    # Dividers between the 4 Main Areas
    draw.line([(0, SPLIT_Y), (W, SPLIT_Y)], fill=C_DIVIDER, width=3)
    draw.line([(400, SPLIT_Y), (400, H)], fill=C_DIVIDER, width=3)
    draw.line([(800, SPLIT_Y), (800, H)], fill=C_DIVIDER, width=3)

    # Save output
    output_png = "richmenu_1200x810.png"
    output_jpg = "richmenu_1200x810.jpg"
    canvas.convert("RGB").save(output_png, quality=95)
    canvas.convert("RGB").save(output_jpg, quality=92, optimize=True)
    canvas.convert("RGB").save("assets/richmenu_1200x810.png", quality=95)
    canvas.convert("RGB").save("assets/richmenu_1200x810.jpg", quality=92, optimize=True)
    print("Done! Re-generated 100% fresh vector rich menu from scratch.")

if __name__ == "__main__":
    build_scratch_rich_menu()
