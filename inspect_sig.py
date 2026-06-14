from PIL import Image
import os

base_dir = r"C:\Users\12tya\Desktop\Ohm\TRH\vision\static\vision\image"
ceo_path = os.path.join(base_dir, "ceo_signature.png")
hr_path = os.path.join(base_dir, "hr_signature.png")

for path in [ceo_path, hr_path]:
    if os.path.exists(path):
        img = Image.open(path).convert("RGBA")
        print(f"\nImage: {os.path.basename(path)}")
        print(f"Size: {img.size}")
        
        alpha = img.split()[-1]
        bbox_alpha = alpha.getbbox()
        print(f"Non-transparent bbox: {bbox_alpha}")
        
        from PIL import ImageChops
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        diff = ImageChops.difference(img, bg)
        bbox_color = diff.getbbox()
        print(f"Non-white bbox: {bbox_color}")
