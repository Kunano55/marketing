import os
from PIL import Image

def build_theme_rich_menu():
    W, H = 1200, 810
    SPLIT_Y = 405
    
    ref_path = r"C:\Users\noobz\.gemini\antigravity-ide\brain\afa6fe71-4bfc-426f-acff-7b1e4c3b699b\.user_uploaded\media_1790221043604.jpg"
    if not os.path.exists(ref_path):
        print(f"Reference image not found at {ref_path}")
        return
        
    ref = Image.open(ref_path)
    
    # Base canvas (1200 x 810 px)
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    
    # 1. TOP BANNER A (1200 x 405)
    # Full top area with logo, curved title, seaweed mascot and speech bubble
    top = ref.crop((0, 0, 1024, 296))
    top_resized = top.resize((1200, SPLIT_Y), Image.Resampling.LANCZOS)
    canvas.paste(top_resized, (0, 0))
    
    # 2. BOTTOM ROW CARDS: B, C, D (400 x 405 each)
    # B: สินค้า / Our Products (0 to 400, 405 to 810)
    b = ref.crop((2, 298, 342, 689)).resize((400, 405), Image.Resampling.LANCZOS)
    canvas.paste(b, (0, SPLIT_Y))
    
    # C: ส่วนลด / Special Offers (400 to 800, 405 to 810)
    c = ref.crop((342, 298, 682, 689)).resize((400, 405), Image.Resampling.LANCZOS)
    canvas.paste(c, (400, SPLIT_Y))
    
    # D: อื่นๆ / More Info (800 to 1200, 405 to 810)
    d = ref.crop((682, 298, 1022, 689)).resize((400, 405), Image.Resampling.LANCZOS)
    canvas.paste(d, (800, SPLIT_Y))
    
    # Save output files
    output_png = "richmenu_1200x810.png"
    output_jpg = "richmenu_1200x810.jpg"
    
    canvas.save(output_png, quality=95)
    canvas.save(output_jpg, quality=92, optimize=True)
    canvas.save("assets/richmenu_1200x810.png", quality=95)
    canvas.save("assets/richmenu_1200x810.jpg", quality=92, optimize=True)
    
    print(f"Generated {output_png} ({os.path.getsize(output_png)/1024:.1f} KB)")
    print(f"Generated {output_jpg} ({os.path.getsize(output_jpg)/1024:.1f} KB)")

if __name__ == "__main__":
    build_theme_rich_menu()
