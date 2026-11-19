#!/usr/bin/env python3
"""Rendus d'aperçu du pack (scène isométrique, galerie de blocs 3D, objets).

À lancer après generate.py :  python3 generator/render_screens.py
Produit : screenshots/scene.png, screenshots/blocs_3d.png, screenshots/objets.png
"""
import json
import os
import random

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "pack", "assets", "minecraft", "textures")
OUTDIR = os.path.join(ROOT, "screenshots")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
GRASS_TINT = (124, 189, 107)  # teinte de biome des plaines (appliquée par le jeu)

with open(os.path.join(ROOT, "pack", "assets", "minecraft", "lang", "fr_fr.json"), encoding="utf-8") as f:
    FR = json.load(f)


def font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_B if bold else FONT, size)
    except OSError:
        return ImageFont.load_default()


_cache = {}


def tex(name, kind="block"):
    key = (kind, name)
    if key not in _cache:
        _cache[key] = Image.open(os.path.join(TEX, kind, name + ".png")).convert("RGBA")
    return _cache[key]


def tint(img, color):
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            px[x, y] = (r * color[0] // 255, g * color[1] // 255, b * color[2] // 255, a)
    return out


def shade(img, f):
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            px[x, y] = (int(r * f), int(g * f), int(b * f), a)
    return out


def grass(face):
    if face == "top":
        return tint(tex("grass_block_top"), GRASS_TINT)
    side = tex("grass_block_side").copy()
    side.alpha_composite(tint(tex("grass_block_side_overlay"), GRASS_TINT))
    return side


# Définition des faces (dessus, gauche, droite) de chaque bloc
def faces(name):
    special = {
        "grass_block": (grass("top"), grass("side"), grass("side")),
        "crafting_table": (tex("crafting_table_top"), tex("crafting_table_front"), tex("crafting_table_side")),
        "furnace": (tex("furnace_top"), tex("furnace_front_on"), tex("furnace_side")),
        "furnace_off": (tex("furnace_top"), tex("furnace_front"), tex("furnace_side")),
        "tnt": (tex("tnt_top"), tex("tnt_side"), tex("tnt_side")),
    }
    if name in special:
        return special[name]
    t = tex(name)
    return (t, t, t)


def affine_face(texture, size, origin, eu, ev):
    """Plaque une texture 16x16 sur un parallélogramme (origin + u*eu + v*ev)."""
    a, b = eu[0], ev[0]
    c, d = eu[1], ev[1]
    det = a * d - b * c
    ia, ib, ic, id_ = d / det, -b / det, -c / det, a / det
    ox, oy = origin
    data = (ia, ib, -(ia * ox + ib * oy), ic, id_, -(ic * ox + id_ * oy))
    return texture.transform(size, Image.AFFINE, data, resample=Image.NEAREST)


def cube(name, a):
    """Cube isométrique : largeur 2a, hauteur 2a."""
    top, left, right = faces(name)
    size = (2 * a + 1, 2 * a + 1)
    s = a / 16
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    img.alpha_composite(affine_face(shade(left, 0.82), size, (0, a / 2), (s, s / 2), (0, s)))
    img.alpha_composite(affine_face(shade(right, 0.64), size, (a, a), (s, -s / 2), (0, s)))
    img.alpha_composite(affine_face(top, size, (0, a / 2), (s, -s / 2), (s, s / 2)))
    return img


def sky(w, h):
    img = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=(int(18 + 60 * t), int(20 + 50 * t), int(54 + 90 * t), 255))
    rng = random.Random(3)
    for _ in range(160):
        x, y = rng.randrange(w), rng.randrange(int(h * 0.6))
        c = rng.choice([(255, 255, 255), (150, 228, 255), (255, 230, 170)])
        d.point((x, y), fill=c)
        if rng.random() < 0.15:
            d.point([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)], fill=c)
    # planète à l'horizon
    d.ellipse([w - 260, 40, w - 80, 220], fill=(240, 146, 42, 255))
    d.ellipse([w - 230, 60, w - 120, 150], fill=(255, 190, 80, 255))
    d.ellipse([w - 300, 115, w - 40, 145], outline=(255, 226, 150, 255), width=3)
    d.ellipse([w - 120, 70, w - 90, 100], fill=(204, 104, 28, 255))
    return img


# --------------------------------------------------------------------------
def build_world():
    W = {}
    N = 10
    for x in range(N):
        for z in range(N):
            for y in range(3):
                W[(x, y, z)] = "stone"
            W[(x, 3, z)] = "dirt"
            W[(x, 4, z)] = "grass_block"
    # minerais visibles sur la tranche
    for pos, ore in {(0, 1, 7): "gold_ore", (0, 0, 3): "diamond_ore", (0, 2, 5): "iron_ore",
                     (4, 1, 9): "emerald_ore", (7, 0, 9): "redstone_ore", (2, 2, 9): "coal_ore",
                     (0, 1, 1): "coal_ore"}.items():
        W[pos] = ore
    # zone de sable
    for x in range(0, 3):
        for z in range(0, 3):
            W[(x, 4, z)] = "sand"
    W[(0, 4, 2)] = "grass_block"
    # garage blindé
    for x in range(5, 9):
        for z in range(1, 5):
            for y in (5, 6):
                if x in (5, 8) or z in (1, 4):
                    W[(x, y, z)] = "iron_block"
            W[(x, 7, z)] = "oak_planks"
    W[(5, 6, 2)] = "glass"; W[(5, 6, 3)] = "glass"
    W[(6, 6, 4)] = "glass"; W[(7, 6, 4)] = "glass"
    W[(5, 7, 4)] = "glowstone"; W[(8, 7, 1)] = "glowstone"
    W[(7, 8, 2)] = "obsidian"; W[(7, 9, 2)] = "redstone_lamp_on"
    # atelier en extérieur
    W[(2, 5, 4)] = "crafting_table"
    W[(2, 5, 3)] = "furnace"
    W[(3, 5, 7)] = "gold_block"
    W[(1, 5, 8)] = "tnt"; W[(1, 6, 8)] = "tnt"; W[(2, 5, 8)] = "tnt"
    W[(7, 5, 7)] = "cobblestone"; W[(8, 5, 7)] = "cobblestone"; W[(8, 6, 7)] = "cobblestone"
    W[(8, 5, 8)] = "glass"
    return W


def screen_pos(x, y, z, a, ox, oy):
    return int(ox + x * a + z * a), int(oy - x * a / 2 + z * a / 2 - y * a)


def render_scene(a=44):
    W = build_world()
    w, h = 1280, 1000
    img = sky(w, h)
    ox, oy = 200, 560
    cubes = {}
    for (x, y, z) in sorted(W, key=lambda p: (p[2] - p[0] + p[1], p[1])):
        name = W[(x, y, z)]
        if name not in cubes:
            cubes[name] = cube(name, a)
        sx, sy = screen_pos(x, y, z, a, ox, oy)
        img.alpha_composite(cubes[name], (sx, sy - a // 2 - 0))
    # objets lâchés au sol (boulons près du bloc de boulons)
    bolt = tex("gold_nugget", "item").resize((28, 28), Image.NEAREST)
    for (x, z, dx, dy) in ((4, 7, 10, 0), (4, 8, -6, 6), (3, 9, 8, -4), (5, 8, 0, 0)):
        sx, sy = screen_pos(x, 5, z, a, ox, oy)
        img.alpha_composite(bolt, (sx + a - 14 + dx, sy - 26 + dy))
    pearl = tex("ender_pearl", "item").resize((28, 28), Image.NEAREST)
    sx, sy = screen_pos(3, 5, 5, a, ox, oy)
    img.alpha_composite(pearl, (sx + a - 14, sy - 26))

    hotbar(img)
    d = ImageDraw.Draw(img)
    title = "Boulons & Galaxies"
    d.text((32, 26), title, font=font(40, True), fill=(255, 190, 80))
    d.text((34, 76), "rendu isométrique avec les textures du pack", font=font(18), fill=(200, 210, 235))
    return img


def hotbar(img):
    items = ["iron_sword", "diamond_sword", "bow_pulling_2", "gold_nugget", "apple",
             "snowball", "ender_pearl", "emerald", "diamond"]
    slot = 72
    w = slot * len(items)
    x0 = (img.width - w) // 2
    y0 = img.height - slot - 30
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0 - 8, y0 - 8, x0 + w + 8, y0 + slot + 8], radius=10,
                        fill=(28, 24, 38, 230), outline=(104, 116, 136), width=3)
    sel = 1
    for i, it in enumerate(items):
        sx = x0 + i * slot
        col = (240, 146, 42) if i == sel else (70, 80, 98)
        d.rectangle([sx + 4, y0 + 4, sx + slot - 4, y0 + slot - 4], fill=(44, 50, 64), outline=col, width=4 if i == sel else 2)
        icon = tex(it, "item").resize((48, 48), Image.NEAREST)
        img.alpha_composite(icon, (sx + 12, y0 + 12))
        if it == "gold_nugget":
            d.text((sx + slot - 30, y0 + slot - 28), "64", font=font(18, True), fill=(255, 255, 255))
    # info-bulle de l'objet sélectionné
    name = FR["item.minecraft." + items[sel]]
    f = font(22, True)
    tw = d.textlength(name, font=f)
    cx = x0 + sel * slot + slot // 2
    d.rounded_rectangle([cx - tw / 2 - 12, y0 - 58, cx + tw / 2 + 12, y0 - 20], radius=6,
                        fill=(20, 16, 30, 240), outline=(116, 52, 170), width=2)
    d.text((cx - tw / 2, y0 - 52), name, font=f, fill=(150, 228, 255))


# --------------------------------------------------------------------------
GALLERY = [
    ("iron_block", "block.minecraft.iron_block"), ("gold_block", "block.minecraft.gold_block"),
    ("cobblestone", "block.minecraft.cobblestone"), ("oak_planks", "block.minecraft.oak_planks"),
    ("crafting_table", "block.minecraft.crafting_table"), ("furnace", "block.minecraft.furnace"),
    ("tnt", "block.minecraft.tnt"), ("glass", "block.minecraft.glass"),
    ("glowstone", "block.minecraft.glowstone"), ("obsidian", "block.minecraft.obsidian"),
    ("redstone_lamp_on", "Lampe (allumée)"), ("redstone_lamp", "Lampe (éteinte)"),
    ("stone", "Roche métallique"), ("grass_block", "Herbe (teintée par le biome)"),
    ("dirt", "Terre martienne"), ("sand", "Sable orange"),
    ("gold_ore", "Minerai de boulons"), ("diamond_ore", "Minerai de cristal"),
    ("emerald_ore", "Minerai d'énergie"), ("iron_ore", "Minerai d'acier"),
]


def label(key):
    return FR.get(key, key)


def render_blocks(a=72, cols=5):
    cw, ch = 2 * a + 90, 2 * a + 70
    rows = (len(GALLERY) + cols - 1) // cols
    w, h = cols * cw + 40, rows * ch + 110
    img = Image.new("RGBA", (w, h), (24, 22, 36, 255))
    d = ImageDraw.Draw(img)
    d.text((24, 22), "Les blocs en 3D", font=font(34, True), fill=(255, 190, 80))
    for i, (name, key) in enumerate(GALLERY):
        cx = 20 + (i % cols) * cw
        cy = 90 + (i // cols) * ch
        d.rounded_rectangle([cx + 4, cy, cx + cw - 4, cy + ch - 10], radius=10, fill=(40, 38, 56))
        img.alpha_composite(cube(name, a), (cx + (cw - 2 * a) // 2, cy + 10))
        t = label(key)
        f = font(17)
        tw = d.textlength(t, font=f)
        d.text((cx + (cw - tw) / 2, cy + 2 * a + 22), t, font=f, fill=(220, 225, 240))
    return img


ITEMS = ["gold_nugget", "wooden_sword", "stone_sword", "iron_sword", "golden_sword", "diamond_sword",
         "netherite_sword", "bow", "bow_pulling_2", "iron_ingot", "gold_ingot", "diamond", "emerald",
         "apple", "snowball", "ender_pearl"]


def render_items(cols=4):
    cw, ch = 300, 210
    rows = (len(ITEMS) + cols - 1) // cols
    img = Image.new("RGBA", (cols * cw + 40, rows * ch + 110), (24, 22, 36, 255))
    d = ImageDraw.Draw(img)
    d.text((24, 22), "Les objets (noms en jeu)", font=font(34, True), fill=(255, 190, 80))
    for i, it in enumerate(ITEMS):
        cx = 20 + (i % cols) * cw
        cy = 90 + (i // cols) * ch
        d.rounded_rectangle([cx + 6, cy, cx + cw - 6, cy + ch - 12], radius=10, fill=(40, 38, 56))
        img.alpha_composite(tex(it, "item").resize((128, 128), Image.NEAREST), (cx + (cw - 128) // 2, cy + 12))
        t = FR.get("item.minecraft." + it, "Blaster (chargé)" if it == "bow_pulling_2" else it)
        f = font(19, True)
        tw = d.textlength(t, font=f)
        d.text((cx + (cw - tw) / 2, cy + 152), t, font=f, fill=(150, 228, 255))
    return img


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    render_scene().convert("RGB").save(os.path.join(OUTDIR, "scene.png"))
    render_blocks().convert("RGB").save(os.path.join(OUTDIR, "blocs_3d.png"))
    render_items().convert("RGB").save(os.path.join(OUTDIR, "objets.png"))
    print("OK ->", OUTDIR)
