from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, random

W, H = 960, 540

def _font(size):
    for name in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()

def create_scene_image(description: str, output_path: Path, seed: int = 1):
    """Create a cheerful original cartoon illustration locally, without external image APIs."""
    random.seed(seed)
    im = Image.new("RGB", (W, H), (155, 220, 255))
    d = ImageDraw.Draw(im)
    # sky and sun
    d.rectangle((0, 0, W, 365), fill=(153, 218, 255))
    d.ellipse((770, 40, 875, 145), fill=(255, 220, 83))
    # clouds
    for x, y in [(100, 75), (380, 105), (620, 65)]:
        d.ellipse((x, y, x+90, y+45), fill="white")
        d.ellipse((x+25, y-18, x+78, y+40), fill="white")
        d.ellipse((x+55, y, x+120, y+45), fill="white")
    # rolling hills
    d.ellipse((-120, 280, 530, 650), fill=(103, 202, 113))
    d.ellipse((300, 290, 1120, 690), fill=(70, 184, 104))
    # flowers
    for _ in range(26):
        x = random.randint(15, W-15); y = random.randint(355, 510)
        d.line((x, y, x, y+15), fill=(32, 135, 64), width=3)
        color = random.choice([(255, 111, 157), (255, 235, 95), (255,255,255), (174,126,255)])
        for a in range(5):
            px = x + int(math.cos(a*math.pi*2/5)*7)
            py = y + int(math.sin(a*math.pi*2/5)*7)
            d.ellipse((px-5, py-5, px+5, py+5), fill=color)
        d.ellipse((x-4,y-4,x+4,y+4), fill=(255,180,50))
    # cute round animal character
    cx, cy = 475, 330
    d.ellipse((cx-82, cy-68, cx+82, cy+94), fill=(255, 218, 170), outline=(135, 91, 70), width=4)
    d.ellipse((cx-68, cy-155, cx-18, cy-55), fill=(255, 218, 170), outline=(135,91,70), width=4)
    d.ellipse((cx+18, cy-155, cx+68, cy-55), fill=(255, 218, 170), outline=(135,91,70), width=4)
    d.ellipse((cx-38, cy-18, cx-20, cy+5), fill=(45, 55, 70))
    d.ellipse((cx+20, cy-18, cx+38, cy+5), fill=(45, 55, 70))
    d.ellipse((cx-7, cy+8, cx+7, cy+20), fill=(230, 115, 135))
    d.arc((cx-27,cy+9,cx+27,cy+48), 5, 175, fill=(120,65,65), width=4)
    d.ellipse((cx-61, cy+4, cx-35, cy+20), fill=(255, 160, 160))
    d.ellipse((cx+35, cy+4, cx+61, cy+20), fill=(255, 160, 160))
    # little companion bird
    d.ellipse((640, 355, 705, 415), fill=(255, 220, 80), outline=(150,110,30), width=3)
    d.ellipse((660, 372, 668, 382), fill=(45,55,70))
    d.polygon([(702,380),(722,388),(702,394)], fill=(255,130,60))
    d.ellipse((642, 375, 664, 399), fill=(255,240,145))
    # title card
    d.rounded_rectangle((35, 25, 610, 100), radius=22, fill=(255,255,255), outline=(255,255,255), width=2)
    text = description[:42].title()
    d.text((55, 43), text, font=_font(25), fill=(55, 85, 115), stroke_width=0)
    d.rounded_rectangle((35, 465, 925, 520), radius=18, fill=(255,255,255), outline=(255,255,255))
    d.text((55, 479), "TOONSTORY AI  •  IMAGINE KINDNESS", font=_font(21), fill=(56, 102, 80))
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    im.save(output_path, format="PNG")
    return output_path
