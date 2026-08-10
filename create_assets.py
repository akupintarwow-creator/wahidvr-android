from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([10, 10, size-10, size-10], fill=(10, 10, 26, 255))
    draw.ellipse([20, 20, size-20, size-20], fill=(0, 136, 204, 255))
    draw.ellipse([40, 40, size-40, size-40], fill=(0, 212, 255, 255))
    draw.ellipse([80, 80, size-80, size-80], fill=(10, 10, 26, 255))
    
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    text = "VR"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), text, fill=(0, 212, 255, 255), font=font)
    
    img.save('icon.png')
    print("Icon created!")

def create_presplash():
    width, height = 800, 480
    img = Image.new('RGB', (width, height), (0, 136, 204))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([width//2-100, height//2-100, width//2+100, height//2+100], fill=(0, 212, 255))
    draw.ellipse([width//2-60, height//2-60, width//2+60, height//2+60], fill=(10, 10, 26))
    
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    text = "WAHIDVR KAMERA"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width-text_width)//2, height//2+120), text, fill=(255, 255, 255), font=font)
    
    img.save('presplash.png')
    print("Presplash created!")

if __name__ == '__main__':
    create_icon()
    create_presplash()
