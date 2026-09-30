import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

def build_thai_broadcast_image():
    base_path = r"C:\Users\noobz\.gemini\antigravity-ide\brain\afa6fe71-4bfc-426f-acff-7b1e4c3b699b\broadcast_clean_base_1790792623270.jpg"
    if not os.path.exists(base_path):
        print("Base photo not found")
        return

    base_img = Image.open(base_path).convert("RGBA")
    W, H = 1024, 1024
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    canvas.paste(base_img, (0, 0))
    draw = ImageDraw.Draw(canvas)

    # Fonts
    font_dir = "temp_fonts"
    f_title_xl = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 46)
    f_title_lg = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 34)
    f_body_lg  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 20)
    f_btn      = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 21)
    f_badge    = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 16)

    # Palette
    C_DARK_OLIVE = (35, 54, 25, 255)
    C_LEAF_GREEN = (90, 126, 48, 255)
    C_WHITE      = (255, 255, 255, 255)
    C_AMBER      = (225, 115, 15, 255)
    C_AMBER_SOFT = (255, 243, 222, 255)
    C_DEEP_GREEN = (24, 52, 26, 255)

    # 1. Place GrobGrob logo on the snack pouch in center
    logo_pouch = Image.open("assets/logo.png").convert("RGBA")
    bbox = logo_pouch.getbbox()
    if bbox:
        logo_pouch = logo_pouch.crop(bbox)
    lw, lh = logo_pouch.size
    pouch_lh = 110
    pouch_lw = int(lw * (pouch_lh / lh))
    logo_pouch = logo_pouch.resize((pouch_lw, pouch_lh), Image.Resampling.LANCZOS)
    logo_pouch = logo_pouch.rotate(-3, expand=True, resample=Image.Resampling.BICUBIC)
    canvas.paste(logo_pouch, (430, 430), logo_pouch)

    # 2. Top Header Banner
    top_w, top_h = 960, 140
    tx, ty = (W - top_w) // 2, 32
    draw.rounded_rectangle([tx + 3, ty + 5, tx + top_w + 3, ty + top_h + 5], radius=26, fill=(0, 0, 0, 28))
    draw.rounded_rectangle([tx, ty, tx + top_w, ty + top_h], radius=26, fill=(255, 255, 255, 248), outline=(220, 230, 210, 255), width=2)

    # Logo inside top header
    logo_im = Image.open("assets/logo.png").convert("RGBA")
    if bbox:
        logo_im = logo_im.crop(bbox)
    top_logo_lh = 100
    top_logo_lw = int(lw * (top_logo_lh / lh))
    logo_im = logo_im.resize((top_logo_lw, top_logo_lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_im, (tx + 28, ty + 20), logo_im)

    # Headline and subtext
    draw.text((tx + top_logo_lw + 50, ty + 26), "กรอบอร่อยเพลิน เคี้ยวสนุกทุกคำ!", font=f_title_lg, fill=C_DARK_OLIVE)
    draw.text((tx + top_logo_lw + 50, ty + 78), "สาหร่ายอบกรอบแท้ 100% • ไม่ใช้น้ำมันทอด • ไร้สารกันบูด", font=f_body_lg, fill=C_LEAF_GREEN)

    # 3. Cute Mascot on Bottom Left
    mascot_im = Image.open("assets/mascot_transparent.png").convert("RGBA")
    mw, mh = mascot_im.size
    target_mh = 275
    target_mw = int(mw * (target_mh / mh))
    mascot_im = mascot_im.resize((target_mw, target_mh), Image.Resampling.LANCZOS)
    canvas.paste(mascot_im, (35, 690), mascot_im)

    # Mascot Speech Bubble
    bw, bh = 175, 62
    bx, by = 140, 635
    draw.ellipse([bx, by, bx + bw, by + bh], fill=C_WHITE, outline=C_DARK_OLIVE, width=3)
    draw.polygon([(185, by + bh - 2), (205, by + bh - 2), (185, by + bh + 18)], fill=C_WHITE)
    draw.line([(185, by + bh - 2), (185, by + bh + 18)], fill=C_DARK_OLIVE, width=3)
    draw.line([(205, by + bh - 2), (185, by + bh + 18)], fill=C_DARK_OLIVE, width=3)
    draw.text((bx + 26, by + 16), "อร่อยทุกคำ", font=f_badge, fill=C_DARK_OLIVE)

    # Vector green heart
    hx, hy = bx + 125, by + 30
    hr = 6
    draw.ellipse([hx - hr, hy - hr//2, hx, hy + hr//2], fill=C_LEAF_GREEN)
    draw.ellipse([hx, hy - hr//2, hx + hr, hy + hr//2], fill=C_LEAF_GREEN)
    draw.polygon([(hx - hr + 1, hy + 1), (hx + hr - 1, hy + 1), (hx, hy + hr + 1)], fill=C_LEAF_GREEN)

    # 4. Floating 3D Golden Promo Card on Bottom Right
    px, py = 615, 550
    pw, ph = 375, 240
    draw.rounded_rectangle([px + 4, py + 6, px + pw + 4, py + ph + 6], radius=24, fill=(0, 0, 0, 35))
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=C_DEEP_GREEN, outline=(245, 175, 65, 255), width=3)

    # White inner coupon ticket
    it_w, it_h = 335, 138
    it_x, it_y = px + 20, py + 20
    draw.rounded_rectangle([it_x, it_y, it_x + it_w, it_y + it_h], radius=16, fill=C_WHITE)
    draw.ellipse([it_x - 12, it_y + it_h//2 - 12, it_x + 12, it_y + it_h//2 + 12], fill=C_DEEP_GREEN)
    draw.ellipse([it_x + it_w - 12, it_y + it_h//2 - 12, it_x + it_w + 12, it_y + it_h//2 + 12], fill=C_DEEP_GREEN)

    # Ticket content
    draw.text((it_x + 22, it_y + 12), "ส่วนลดพิเศษเปิดร้าน", font=f_badge, fill=C_DARK_OLIVE)
    draw.text((it_x + 20, it_y + 36), "ลดทันที 10%", font=f_title_xl, fill=C_DEEP_GREEN)

    # Promo code pill
    draw.rounded_rectangle([it_x + 185, it_y + 12, it_x + 318, it_y + 44], radius=8, fill=C_AMBER_SOFT, outline=C_AMBER, width=2)
    draw.text((it_x + 195, it_y + 16), "โค้ด: GROB10", font=f_badge, fill=C_AMBER)

    # Star icon & Free shipping note
    draw.polygon([(it_x + 24, it_y + 98), (it_x + 27, it_y + 104), (it_x + 34, it_y + 105), (it_x + 29, it_y + 110), (it_x + 30, it_y + 116), (it_x + 24, it_y + 113), (it_x + 18, it_y + 116), (it_x + 19, it_y + 110), (it_x + 14, it_y + 105), (it_x + 21, it_y + 104)], fill=C_AMBER)
    draw.text((it_x + 38, it_y + 96), "ช้อปครบ 150 บาท ส่งฟรีทั่วประเทศ", font=f_badge, fill=C_LEAF_GREEN)

    # CTA Button
    btn_y = py + 172
    draw.rounded_rectangle([it_x, btn_y, it_x + it_w, btn_y + 48], radius=24, fill=C_AMBER)
    draw.text((it_x + 60, btn_y + 12), "สั่งซื้อออนไลน์ได้แล้ววันนี้ ›", font=f_btn, fill=C_WHITE)

    # Save outputs
    canvas.convert("RGB").save("assets/broadcast_promo.jpg", quality=95)
    canvas.convert("RGB").save("assets/broadcast_promo.png", quality=95)
    canvas.convert("RGB").save("broadcast_promo.jpg", quality=95)
    canvas.convert("RGB").save("broadcast_promo.png", quality=95)
    print("Generated 100% Thai Broadcast Poster successfully!")

if __name__ == "__main__":
    build_thai_broadcast_image()
