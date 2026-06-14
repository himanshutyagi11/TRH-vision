import os
import io
from PIL import Image, ImageDraw, ImageFont

base_dir = r"C:\Users\12tya\Desktop\Ohm\trh"
cert_img_path = os.path.join(base_dir, 'vision', 'static', 'vision', 'image', 'TRJcertificate.png')
cert = Image.open(cert_img_path).convert('RGBA')
W, H = cert.size
draw = ImageDraw.Draw(cert)
sig_y_line = 1220

def paste_sign_image(img_name, center_x, line_y):
    sig_path = os.path.join(base_dir, 'vision', 'static', 'vision', 'image', img_name)
    if os.path.exists(sig_path):
        sig_img = Image.open(sig_path).convert("RGBA")
        
        # Auto-crop transparent borders
        alpha = sig_img.split()[-1]
        bbox = alpha.getbbox()
        if bbox:
            sig_img = sig_img.crop(bbox)

        # Resize to fit above the signature line nicely
        sig_w, sig_h = sig_img.size
        new_w = 280
        new_h = int(sig_h * (new_w / sig_w))
        sig_img = sig_img.resize((new_w, new_h), Image.LANCZOS)
        
        paste_x = center_x - (new_w // 2)
        paste_y = line_y - new_h - 10
        cert.paste(sig_img, (paste_x, paste_y), sig_img)

sig1_x1 = int(W * 0.12)
sig1_x2 = int(W * 0.30)
sig1_center_x = (sig1_x1 + sig1_x2) // 2

draw.line([(sig1_x1, sig_y_line), (sig1_x2, sig_y_line)], fill='#1a3c6e', width=3)
paste_sign_image("ceo_signature.png", sig1_center_x, sig_y_line)

sig2_x1 = int(W * 0.70)
sig2_x2 = int(W * 0.88)
sig2_center_x = (sig2_x1 + sig2_x2) // 2

draw.line([(sig2_x1, sig_y_line), (sig2_x2, sig_y_line)], fill='#1a3c6e', width=3)
paste_sign_image("hr_signature.png", sig2_center_x, sig_y_line)

cert_rgb = cert.convert('RGB')

test_path = os.path.join(base_dir, 'test_cert.jpg')
cert_rgb.save(test_path)
print(f"Saved {test_path} successfully")
