import os
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import imageio_ffmpeg

def ease_out_back(t, s=1.70158):
    t -= 1.0
    return t * t * ((s + 1.0) * t + s) + 1.0

def ease_out_cubic(t):
    return 1.0 - (1.0 - t) ** 3

def ease_in_out_sine(t):
    return -(math.cos(math.pi * t) - 1.0) / 2.0

def draw_star(draw, cx, cy, r_out, r_in, fill):
    points = []
    for i in range(10):
        angle = i * math.pi / 5.0 - math.pi / 2.0
        r = r_out if i % 2 == 0 else r_in
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)

def draw_arrow_right(draw, cx, cy, size, fill):
    w, h = size, size * 0.7
    points = [
        (cx - w/2, cy - h/2),
        (cx + w/2, cy),
        (cx - w/2, cy + h/2)
    ]
    draw.polygon(points, fill=fill)

def draw_arrow_down(draw, cx, cy, size, fill):
    w, h = size * 0.7, size
    points = [
        (cx - w, cy - h/2),
        (cx + w, cy - h/2),
        (cx, cy + h/2)
    ]
    draw.polygon(points, fill=fill)

def main():
    W, H = 1080, 1080
    FPS = 30
    TOTAL_SECONDS = 8
    TOTAL_FRAMES = FPS * TOTAL_SECONDS

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    font_dir = "temp_fonts"

    # Fonts
    f_huge = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 54)
    f_title_xl = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 44)
    f_title_lg = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 34)
    f_title_md = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 26)
    f_body_lg  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 22)
    f_body_md  = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 18)
    f_btn      = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 32)

    # Assets
    logo_orig = Image.open("assets/logo.png").convert("RGBA")
    bbox = logo_orig.getbbox()
    if bbox: logo_orig = logo_orig.crop(bbox)

    mascot_orig = Image.open("assets/mascot_transparent.png").convert("RGBA")
    mbbox = mascot_orig.getbbox()
    if mbbox: mascot_orig = mascot_orig.crop(mbbox)

    promo_img = Image.open("assets/broadcast_promo.jpg").convert("RGBA")
    pouch_crop = promo_img.crop((280, 260, 740, 850))

    norisheet = Image.open("assets/seaweed-sheet.png").convert("RGBA")
    noriroll  = Image.open("assets/seaweed-roll.png").convert("RGBA")

    # Colors
    C_CREAM_TOP  = (254, 252, 246)
    C_CREAM_BOT  = (234, 246, 226)
    C_DARK_GREEN = (22, 53, 26)
    C_LEAF_GREEN = (85, 126, 42)
    C_AMBER      = (228, 110, 10)
    C_GOLD       = (245, 166, 35)
    C_WHITE      = (255, 255, 255)

    # Pre-render base background gradient
    base_bg = Image.new("RGBA", (W, H))
    bg_draw = ImageDraw.Draw(base_bg)
    for y in range(H):
        ratio = y / H
        r = int(C_CREAM_TOP[0] * (1 - ratio) + C_CREAM_BOT[0] * ratio)
        g = int(C_CREAM_TOP[1] * (1 - ratio) + C_CREAM_BOT[1] * ratio)
        b = int(C_CREAM_TOP[2] * (1 - ratio) + C_CREAM_BOT[2] * ratio)
        bg_draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    output_mp4 = "assets/richvideo_promo.mp4"
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "19",
        "-movflags", "+faststart",
        output_mp4
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for i in range(TOTAL_FRAMES):
        t = i / FPS
        frame = base_bg.copy()
        draw = ImageDraw.Draw(frame)

        # Ambient floating sparkles / golden particles
        for dot_idx in range(16):
            dx = (dot_idx * 73 + int(t * 25)) % W
            dy = (dot_idx * 117 + int(math.sin(t * 1.5 + dot_idx) * 40) + int(t * 15)) % H
            dsize = 5 + (dot_idx % 3) * 2
            alpha = int(100 + 60 * math.sin(t * 3 + dot_idx))
            draw.ellipse([dx, dy, dx + dsize, dy + dsize], fill=(245, 210, 110, alpha))

        # =========================================================================
        # SCENE 1: (0s - 2.5s, frames 0 - 75) - Crunchy Entrance & Mascot
        # =========================================================================
        if i <= 75:
            # 1. Top Logo drops in
            logo_t = min(1.0, i / 20.0)
            logo_y = -100 + ease_out_back(logo_t) * 140
            lw = 240
            lh = int(logo_orig.size[1] * (lw / logo_orig.size[0]))
            curr_logo = logo_orig.resize((lw, lh), Image.Resampling.LANCZOS)
            frame.paste(curr_logo, ((W - lw) // 2, int(logo_y)), curr_logo)

            # Subtitle
            if i > 12:
                sub_txt = "กรอบอร่อยเพลิน เคี้ยวสนุกทุกคำ!"
                bbox = draw.textbbox((0, 0), sub_txt, font=f_title_lg)
                tw = bbox[2] - bbox[0]
                draw.text(((W - tw) // 2, int(logo_y + lh + 10)), sub_txt, font=f_title_lg, fill=C_DARK_GREEN)

            # 2. Hero Pouch flies in & floats
            pouch_t = min(1.0, i / 25.0)
            p_scale = 0.5 + 0.5 * ease_out_back(pouch_t)
            float_y = math.sin(t * 4.0) * 12
            pw = int(380 * p_scale)
            ph = int(pouch_crop.size[1] * (pw / pouch_crop.size[0]))
            curr_pouch = pouch_crop.resize((pw, ph), Image.Resampling.LANCZOS)
            p_x = (W - pw) // 2
            p_y = int(320 + float_y - (1.0 - ease_out_cubic(pouch_t)) * 200)

            # Soft shadow
            sh_w = int(pw * 0.75)
            draw.ellipse([p_x + (pw - sh_w)//2, p_y + ph - 10, p_x + (pw + sh_w)//2, p_y + ph + 24], fill=(0, 0, 0, 35))
            frame.paste(curr_pouch, (p_x, p_y), curr_pouch)

            # 3. Flying Seaweed Elements
            s1_x = -150 + int(ease_out_cubic(min(1.0, i / 35.0)) * 260) + int(math.sin(t * 3) * 10)
            s1_y = 520 + int(math.cos(t * 2.5) * 15)
            s1 = norisheet.resize((150, 150), Image.Resampling.LANCZOS).rotate(int(t * 20), expand=True)
            frame.paste(s1, (s1_x, s1_y), s1)

            s2_x = W - int(ease_out_cubic(min(1.0, max(0.0, (i - 8) / 30.0))) * 250) + int(math.cos(t * 3) * 8)
            s2_y = 380 + int(math.sin(t * 2) * 15)
            s2 = noriroll.resize((140, 140), Image.Resampling.LANCZOS).rotate(int(-t * 25), expand=True)
            frame.paste(s2, (s2_x, s2_y), s2)

            # 4. Mascot peeks in from bottom left
            if i > 15:
                mascot_t = min(1.0, (i - 15) / 20.0)
                mw = 240
                mh = int(mascot_orig.size[1] * (mw / mascot_orig.size[0]))
                my = H - int(ease_out_back(mascot_t) * (mh * 0.9)) + int(math.sin(t * 6) * 8)
                curr_mascot = mascot_orig.resize((mw, mh), Image.Resampling.LANCZOS)
                frame.paste(curr_mascot, (40, my), curr_mascot)

            # Bottom Pill
            if i > 25:
                bp_t = min(1.0, (i - 25) / 18.0)
                bp_y = int(H - 120 + (1.0 - ease_out_back(bp_t)) * 100)
                bw, bh = 560, 64
                bx = (W - bw) // 2
                draw.rounded_rectangle([bx, bp_y, bx + bw, bp_y + bh], radius=32, fill=(255, 255, 255, 240), outline=C_LEAF_GREEN, width=2)
                txt = "สาหร่ายอบแท้ 100% ไร้น้ำมันทอด"
                bbox = draw.textbbox((0, 0), txt, font=f_title_md)
                tw = bbox[2] - bbox[0]
                draw.text((bx + (bw - tw) // 2, bp_y + 14), txt, font=f_title_md, fill=C_LEAF_GREEN)

        # =========================================================================
        # SCENE 2: (2.5s - 5.2s, frames 75 - 156) - Promotion Explosion & Coupon
        # =========================================================================
        elif i <= 156:
            scene2_frame = i - 75
            t2 = scene2_frame / 81.0

            # Golden halo background
            glow_r = int(340 + 20 * math.sin(t * 5))
            draw.ellipse([(W//2) - glow_r, 450 - glow_r, (W//2) + glow_r, 450 + glow_r], fill=(255, 246, 215, 170))

            # 1. Top Header Banner "โปรโมชันพิเศษเปิดตัว"
            top_t = min(1.0, scene2_frame / 15.0)
            ty = int(36 - (1.0 - ease_out_back(top_t)) * 80)
            tag_txt = "โปรโมชันพิเศษเปิดตัวร้านค้า"
            bbox = draw.textbbox((0, 0), tag_txt, font=f_title_md)
            tw = bbox[2] - bbox[0]
            tbw = tw + 80
            tbx = (W - tbw) // 2
            draw.rounded_rectangle([tbx, ty, tbx + tbw, ty + 50], radius=25, fill=C_DARK_GREEN)
            # Draw vector stars on sides
            draw_star(draw, tbx + 25, ty + 25, 11, 5, C_GOLD)
            draw_star(draw, tbx + tbw - 25, ty + 25, 11, 5, C_GOLD)
            draw.text((tbx + 42, ty + 9), tag_txt, font=f_title_md, fill=C_WHITE)

            # 2. Giant Discount Headline "ลดทันที 10%"
            disc_t = min(1.0, max(0.0, (scene2_frame - 6) / 18.0))
            disc_txt = "ลดทันที 10%"
            bbox = draw.textbbox((0, 0), disc_txt, font=f_huge)
            dw = bbox[2] - bbox[0]
            dy = int(ty + 65)
            draw.text(((W - dw) // 2, dy), disc_txt, font=f_huge, fill=C_AMBER)

            # 3. Glowing Golden Coupon Card
            card_t = min(1.0, max(0.0, (scene2_frame - 15) / 20.0))
            cw, ch = 880, 360
            cx = (W - cw) // 2
            cy = int(235 + (1.0 - ease_out_back(card_t)) * 180)

            # Card Shadow & Body
            draw.rounded_rectangle([cx + 6, cy + 10, cx + cw + 6, cy + ch + 10], radius=36, fill=(0, 0, 0, 30))
            draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=36, fill=(255, 255, 255, 252), outline=C_GOLD, width=4)

            # Coupon Ticket Box
            cp_w, cp_h = 760, 110
            cpx = cx + (cw - cp_w) // 2
            cpy = cy + 35
            draw.rounded_rectangle([cpx, cpy, cpx + cp_w, cpy + cp_h], radius=22, fill=(255, 247, 230), outline=C_AMBER, width=3)
            
            draw.text((cpx + 35, cpy + 32), "โค้ดส่วนลด:", font=f_title_lg, fill=C_DARK_GREEN)
            draw.text((cpx + 235, cpy + 22), "GROB10", font=f_huge, fill=C_AMBER)
            
            # Badge "ลด 10%"
            badge_x = cpx + cp_w - 180
            draw.rounded_rectangle([badge_x, cpy + 22, badge_x + 155, cpy + 88], radius=18, fill=C_LEAF_GREEN)
            draw.text((badge_x + 28, cpy + 36), "ลด 10%", font=f_title_md, fill=C_WHITE)

            # Subtext
            desc1 = "ไม่มีขั้นต่ำ • ใช้ได้ทุกรายการสินค้า"
            bbox = draw.textbbox((0, 0), desc1, font=f_title_md)
            draw.text((cx + (cw - (bbox[2] - bbox[0])) // 2, cy + 172), desc1, font=f_title_md, fill=C_DARK_GREEN)

            # Free shipping banner inside card
            fs_w, fs_h = 760, 72
            fs_x = cx + (cw - fs_w) // 2
            fs_y = cy + 245
            draw.rounded_rectangle([fs_x, fs_y, fs_x + fs_w, fs_y + fs_h], radius=20, fill=(240, 248, 232), outline=C_LEAF_GREEN, width=1)
            fs_txt = "ฟรีค่าจัดส่งทั่วประเทศ เมื่อช้อปครบ 150 บาท"
            bbox = draw.textbbox((0, 0), fs_txt, font=f_title_md)
            draw.text((fs_x + (fs_w - (bbox[2] - bbox[0])) // 2, fs_y + 17), fs_txt, font=f_title_md, fill=C_LEAF_GREEN)

            # Pouch & Mascot at bottom
            pw = 280
            ph = int(pouch_crop.size[1] * (pw / pouch_crop.size[0]))
            curr_pouch = pouch_crop.resize((pw, ph), Image.Resampling.LANCZOS)
            frame.paste(curr_pouch, (W - pw - 60, H - ph - 60), curr_pouch)

            mw = 240
            mh = int(mascot_orig.size[1] * (mw / mascot_orig.size[0]))
            curr_mascot = mascot_orig.resize((mw, mh), Image.Resampling.LANCZOS)
            frame.paste(curr_mascot, (60, H - mh - 50), curr_mascot)

        # =========================================================================
        # SCENE 3: (5.2s - 8.0s, frames 156 - 240) - High-Conversion CTA
        # =========================================================================
        else:
            scene3_frame = i - 156

            # 1. Top Logo + Brand
            lw = 240
            lh = int(logo_orig.size[1] * (lw / logo_orig.size[0]))
            curr_logo = logo_orig.resize((lw, lh), Image.Resampling.LANCZOS)
            frame.paste(curr_logo, ((W - lw) // 2, 40), curr_logo)

            slogan = "สาหร่ายอบกรอบ พรีเมียม 100%"
            bbox = draw.textbbox((0, 0), slogan, font=f_title_md)
            draw.text(((W - (bbox[2] - bbox[0])) // 2, 40 + lh + 8), slogan, font=f_title_md, fill=C_LEAF_GREEN)

            # 2. Center Stage: Pouch & Mascot together
            center_y = 215
            mw = 280
            mh = int(mascot_orig.size[1] * (mw / mascot_orig.size[0]))
            curr_mascot = mascot_orig.resize((mw, mh), Image.Resampling.LANCZOS)
            m_hop = int(math.sin(t * 8) * 8)
            frame.paste(curr_mascot, (140, center_y + 110 + m_hop), curr_mascot)

            pw = 370
            ph = int(pouch_crop.size[1] * (pw / pouch_crop.size[0]))
            curr_pouch = pouch_crop.resize((pw, ph), Image.Resampling.LANCZOS)
            p_hop = int(math.cos(t * 6) * 6)
            frame.paste(curr_pouch, (490, center_y + p_hop), curr_pouch)

            # 3. Value Badges (3 Clean Pills without missing emoji boxes)
            pills = [
                ("อบแท้ ไม่ใช้น้ำมัน", (235, 247, 230), C_DARK_GREEN),
                ("แคลต่ำ กรอบเพลิน", (255, 248, 230), C_AMBER),
                ("โค้ดลด 10% GROB10", (255, 235, 230), (200, 40, 20))
            ]
            pill_y = 745
            pill_total_w = 980
            px_start = (W - pill_total_w) // 2
            col_w = pill_total_w // 3
            for p_idx, (p_text, p_bg, p_fg) in enumerate(pills):
                px = px_start + p_idx * col_w + 10
                draw.rounded_rectangle([px, pill_y, px + col_w - 20, pill_y + 55], radius=24, fill=p_bg, outline=p_fg, width=2)
                bbox = draw.textbbox((0, 0), p_text, font=f_body_lg)
                tw = bbox[2] - bbox[0]
                draw.text((px + (col_w - 20 - tw) // 2, pill_y + 12), p_text, font=f_body_lg, fill=p_fg)

            # 4. Animated Giant Call-To-Action Button pointing to LINE OA's Action bar below!
            pulse_scale = 1.0 + 0.03 * math.sin(t * 10)
            btn_base_w, btn_base_h = 860, 110
            btn_w = int(btn_base_w * pulse_scale)
            btn_h = int(btn_base_h * pulse_scale)
            btn_x = (W - btn_w) // 2
            btn_y = int(865 - (btn_h - btn_base_h) // 2)

            # Button Shadow & Body
            draw.rounded_rectangle([btn_x + 4, btn_y + 8, btn_x + btn_w + 4, btn_y + btn_h + 8], radius=38, fill=(0, 0, 0, 35))
            draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=38, fill=C_AMBER)
            draw.rounded_rectangle([btn_x + 6, btn_y + 6, btn_x + btn_w - 6, btn_y + 35], radius=20, fill=(255, 255, 255, 60))

            # Button Text with animated arrows
            cta_txt = "แตะปุ่มด้านล่างเพื่อสั่งซื้อเลย"
            bbox = draw.textbbox((0, 0), cta_txt, font=f_btn)
            ctw = bbox[2] - bbox[0]
            mid_y = btn_y + 32
            draw.text((btn_x + (btn_w - ctw) // 2, mid_y), cta_txt, font=f_btn, fill=C_WHITE)

            # Animated downward indicator arrows on sides
            arr_y = btn_y + 55 + int(math.sin(t * 12) * 5)
            draw_arrow_down(draw, btn_x + 60, arr_y, 16, C_WHITE)
            draw_arrow_down(draw, btn_x + btn_w - 60, arr_y, 16, C_WHITE)

            # Small subtext at bottom
            foot_txt = "ส่งฟรีเมื่อช้อปครบ 150 บาท • ส่งตรงถึงบ้านทั่วประเทศ"
            bbox = draw.textbbox((0, 0), foot_txt, font=f_body_md)
            draw.text(((W - (bbox[2] - bbox[0])) // 2, H - 45), foot_txt, font=f_body_md, fill=C_DARK_GREEN)

        # Write frame to ffmpeg
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    print("Video generation completed successfully!")
    print("Saved to:", output_mp4, "File size:", os.path.getsize(output_mp4), "bytes")

if __name__ == "__main__":
    main()
