#!/usr/bin/env python3
"""Generate Sileo featured banner images from tweak icons."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 790, 444          # 3x of the {263, 148} itemSize declared in sileo-featured.json
SRC = "/Users/mafu/Documents/tweak/repo/web/images"
OUT = "/Users/mafu/Documents/tweak/repo/web/images/banners"

BANNERS = [
    ("MikkyyPro",  "#F59B3D", "Modern, lightweight\ninterface theming engine", "Mikkyy", "Mikkyy Pro"),
    ("K2gecamen",  "#16A4C5", "Capture moments anytime\nin the background"),
    ("Myrtle",     "#40BFB5", "Ultimate multitasking\nfrom one edge gesture"),
    ("K2geIsland", "#FF9B76", "Ultimate customization\nfor Dynamic Island"),
    ("K2ge3Air",   "#34C759", "Enhance LINE features"),
]

FONT = "/System/Library/Fonts/SFNS.ttf"   # SF Pro (variable)


def sf(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(weight)
    return f


title_font = sf(64, "Bold")
sub_font = sf(31, "Regular")


def rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def scale(color, factor):
    return tuple(min(255, int(c * factor)) for c in color)


def gradient(top, bottom):
    """Vertical gradient, drawn one row at a time."""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(
            round(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img


def rounded(icon, size, radius):
    icon = icon.convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius, fill=255)
    icon.putalpha(mask)
    return icon


def build(name, tint, subtitle, icon=None, title=None):
    base = rgb(tint)
    img = gradient(scale(base, 1.15), scale(base, 0.45))

    icon_size, pad = 230, 56
    icon = rounded(Image.open(f"{SRC}/{icon or name}.png"), icon_size, 48)
    icon_y = (H - icon_size) // 2

    # soft drop shadow under the icon
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [pad + 6, icon_y + 12, pad + icon_size + 6, icon_y + icon_size + 12],
        icon_size // 5, fill=(0, 0, 0, 70))
    img = Image.alpha_composite(img.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(14)))
    img.paste(icon, (pad, icon_y), icon)

    d = ImageDraw.Draw(img)
    tx = pad + icon_size + 44
    lines = subtitle.split("\n")
    block_h = 80 + len(lines) * 40
    ty = (H - block_h) // 2
    d.text((tx, ty), title or name, font=title_font, fill=(255, 255, 255, 255))
    for i, line in enumerate(lines):
        d.text((tx, ty + 86 + i * 40), line, font=sub_font, fill=(255, 255, 255, 215))

    img.convert("RGB").save(f"{OUT}/{name}.png", optimize=True)
    print(f"{OUT}/{name}.png")


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for b in BANNERS:
        build(*b)
