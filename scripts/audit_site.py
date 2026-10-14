import os
import re

html_files = ['index.html', 'products.html', 'cart.html', 'login.html', 'register.html']
print("=== CHECKING HTML ASSETS AND LINKS ===")

for filename in html_files:
    if not os.path.exists(filename):
        print(f"File missing: {filename}")
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Images
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
    for img in imgs:
        if not img.startswith('http') and not img.startswith('data:'):
            clean_img = img.split('?')[0]
            if not os.path.exists(clean_img):
                print(f"[{filename}] BROKEN IMAGE: {img}")

    # CSS links
    css_files = re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', content, re.IGNORECASE)
    for css in css_files:
        clean_css = css.split('?')[0]
        if not os.path.exists(clean_css):
            print(f"[{filename}] BROKEN CSS: {css}")

    # Script files
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+\.js[^"\']*)["\']', content, re.IGNORECASE)
    for js in scripts:
        clean_js = js.split('?')[0]
        if not os.path.exists(clean_js):
            print(f"[{filename}] BROKEN JS: {js}")

    # Anchor links
    links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    for href in links:
        if not href.startswith('http') and not href.startswith('#') and not href.startswith('javascript:'):
            clean_href = href.split('?')[0].split('#')[0]
            if clean_href and not os.path.exists(clean_href):
                print(f"[{filename}] BROKEN LINK: {href}")

print("=== CHECKING APP.JS PRODUCT IMAGES ===")
if os.path.exists('app.js'):
    with open('app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    js_imgs = re.findall(r"image:\s*['\"]([^'\"]+)['\"]", js_content)
    print(f"Found {len(js_imgs)} images in app.js")
    for img in js_imgs:
        clean_img = img.split('?')[0]
        if not os.path.exists(clean_img):
            print(f"[app.js] BROKEN IMAGE: {img}")

print("All checks completed successfully.")
