#!/usr/bin/env python3
"""Générateur du pack de textures « Boulons & Galaxies ».

Pack Minecraft (Java Edition) sur un thème sci-fi mécanique / aventure spatiale,
inspiré de l'ambiance Ratchet & Clank (boulons, clés, blasters, blindage riveté).
Toutes les textures sont dessinées par ce script, en pixel art 16x16.

Usage :  python3 generator/generate.py
Produit : pack/  (dossier du resource pack)
          dist/BoulonsEtGalaxies.zip
          preview.png
"""
import json
import math
import os
import random
import shutil
import zipfile

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, "pack")
BLOCK = os.path.join(PACK, "assets", "minecraft", "textures", "block")
ITEM = os.path.join(PACK, "assets", "minecraft", "textures", "item")
LANG = os.path.join(PACK, "assets", "minecraft", "lang")
PACK_NAME = "BoulonsEtGalaxies"

# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------
T = (0, 0, 0, 0)
OUT = (28, 24, 38, 255)
STEEL = [(44, 50, 64), (70, 80, 98), (104, 116, 136), (138, 152, 172), (178, 190, 208), (222, 230, 240)]
ORANGE = [(98, 40, 14), (150, 66, 18), (204, 104, 28), (240, 146, 42), (255, 190, 80), (255, 226, 150)]
BRASS = [(84, 56, 16), (138, 96, 26), (190, 142, 40), (226, 182, 62), (250, 216, 110), (255, 244, 190)]
CYAN = [(10, 40, 70), (20, 80, 130), (30, 140, 210), (70, 196, 255), (150, 228, 255), (230, 250, 255)]
PURPLE = [(36, 14, 60), (70, 28, 110), (116, 52, 170), (160, 90, 220), (200, 150, 250), (240, 220, 255)]
GREEN = [(10, 50, 30), (20, 100, 50), (40, 160, 70), (90, 220, 100), (170, 255, 160), (235, 255, 230)]
RED = [(60, 10, 14), (120, 20, 24), (190, 36, 36), (236, 70, 56), (255, 130, 100), (255, 210, 190)]
SOIL = [(70, 30, 20), (104, 46, 26), (138, 64, 34), (170, 88, 46), (198, 116, 62)]
SAND = [(196, 112, 50), (216, 134, 62), (232, 156, 78), (244, 178, 98), (252, 200, 124)]
WOODISH = [(70, 36, 18), (110, 58, 26), (150, 86, 38), (184, 116, 52), (214, 150, 72), (240, 190, 110)]
DARKSTEEL = [(20, 16, 30), (34, 28, 48), (48, 40, 66), (66, 56, 90), (96, 84, 124), (140, 128, 170)]


def rgba(c, a=255):
    return (c[0], c[1], c[2], a) if len(c) == 3 else c


def new(w=16, h=16, fill=T):
    return Image.new("RGBA", (w, h), rgba(fill) if fill != T else T)


def px(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), rgba(c))


def rect(img, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(img, x, y, c)


def noise_fill(img, pal, rng, weights=None, box=None):
    x0, y0, x1, y1 = box or (0, 0, img.width - 1, img.height - 1)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(img, x, y, rng.choices(pal, weights=weights)[0])


def bevel(img, x0, y0, x1, y1, light, dark):
    for x in range(x0, x1 + 1):
        px(img, x, y0, light)
        px(img, x, y1, dark)
    for y in range(y0, y1 + 1):
        px(img, x0, y, light)
        px(img, x1, y, dark)
    px(img, x1, y0, light)
    px(img, x0, y1, dark)


def rivet(img, x, y, pal=STEEL):
    px(img, x, y, pal[5])
    px(img, x + 1, y, pal[3])
    px(img, x, y + 1, pal[3])
    px(img, x + 1, y + 1, pal[1])


def outline(img, color=OUT):
    """Ajoute un contour sombre (4-voisins) autour des pixels opaques."""
    src = img.copy()
    for y in range(img.height):
        for x in range(img.width):
            if src.getpixel((x, y))[3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < img.width and 0 <= ny < img.height and src.getpixel((nx, ny))[3] > 0:
                        img.putpixel((x, y), rgba(color))
                        break
    return img


def shape(mask, pal, w=16, h=16, base=2):
    """Remplit un masque avec ombrage auto : clair en haut-gauche, sombre en bas-droite."""
    img = new(w, h)
    inside = lambda x, y: 0 <= x < w and 0 <= y < h and mask(x, y)
    for y in range(h):
        for x in range(w):
            if not inside(x, y):
                continue
            c = base
            if not inside(x - 1, y - 1):
                c = base + 2
            elif not inside(x - 1, y) or not inside(x, y - 1):
                c = base + 1
            if not inside(x + 1, y + 1):
                c = base - 2
            elif not inside(x + 1, y) or not inside(x, y + 1):
                c = base - 1
            img.putpixel((x, y), rgba(pal[max(0, min(len(pal) - 1, c))]))
    return img


def seg_dist(px_, py_, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((px_ - ax) * vx + (py_ - ay) * vy) / (vx * vx + vy * vy)))
    cx, cy = ax + t * vx, ay + t * vy
    return math.hypot(px_ - cx, py_ - cy), t


def in_hex(x, y, cx, cy, r):
    dx, dy = abs(x - cx), abs(y - cy)
    return dy <= r * 0.866 and (0.866 * dx + 0.5 * dy) <= r * 0.866


def paste(dst, src, ox=0, oy=0):
    dst.alpha_composite(src, (ox, oy))
    return dst


# --------------------------------------------------------------------------
# Blocs
# --------------------------------------------------------------------------
def stone(seed=1):
    """Roche bleutée d'une planète métallique."""
    rng = random.Random(seed)
    pal = [(86, 94, 112), (100, 108, 128), (114, 122, 142), (128, 136, 156)]
    img = new()
    noise_fill(img, pal, rng, [2, 4, 4, 2])
    for _ in range(3):  # petites fissures
        x, y = rng.randrange(16), rng.randrange(16)
        for _ in range(rng.randint(2, 4)):
            px(img, x, y, (64, 70, 88))
            px(img, x + 1, y, (146, 154, 172))
            x += rng.choice((-1, 0, 1))
            y += 1
    return img


def iron_block():
    """Panneau de blindage riveté."""
    rng = random.Random(2)
    img = new()
    noise_fill(img, STEEL[2:4], rng, [3, 2])
    bevel(img, 0, 0, 15, 15, STEEL[4], STEEL[0])
    bevel(img, 3, 3, 12, 12, STEEL[1], STEEL[4])
    rect(img, 4, 4, 11, 11, STEEL[3])
    rect(img, 5, 7, 10, 8, STEEL[2])
    for x, y in ((1, 1), (13, 1), (1, 13), (13, 13)):
        rivet(img, x, y)
    return img


def gold_block():
    """Bloc de boulons : quatre gros boulons en laiton."""
    img = new(fill=BRASS[0])
    for oy in (0, 8):
        for ox in (0, 8):
            rect(img, ox, oy, ox + 7, oy + 7, BRASS[1])
            b = shape(lambda x, y: in_hex(x, y, 3.5, 3.5, 3.6), BRASS, 8, 8, base=3)
            px(b, 3, 3, BRASS[1]); px(b, 4, 4, BRASS[1]); px(b, 4, 3, BRASS[2]); px(b, 3, 4, BRASS[2])
            paste(img, b, ox, oy)
    bevel(img, 0, 0, 15, 15, BRASS[4], BRASS[0])
    return img


def cobblestone():
    """Tôles de ferraille assemblées."""
    rng = random.Random(3)
    img = new(fill=STEEL[0])
    plates = [(0, 0, 6, 5), (7, 0, 15, 3), (7, 4, 11, 9), (12, 4, 15, 10), (0, 6, 6, 11),
              (0, 12, 4, 15), (5, 12, 10, 15), (11, 11, 15, 15), (7, 10, 10, 11)]
    tints = [STEEL, STEEL, [(90, 60, 50), (120, 74, 54), (150, 92, 62), (176, 112, 76), (200, 140, 100), (230, 180, 140)]]
    for (x0, y0, x1, y1) in plates:
        p = rng.choice(tints)
        rect(img, x0, y0, x1, y1, p[2])
        noise_fill(img, [p[2], p[3]], rng, [3, 1], (x0 + 1, y0 + 1, x1 - 1, y1 - 1))
        bevel(img, x0, y0, x1, y1, p[4], p[0])
        if x1 - x0 >= 4 and y1 - y0 >= 3:
            px(img, x0 + 1, y0 + 1, p[5])
    return img


def dirt():
    """Terre rouge-orangé d'une planète désertique."""
    rng = random.Random(4)
    img = new()
    noise_fill(img, SOIL[1:4], rng, [2, 4, 3])
    for _ in range(7):
        x, y = rng.randrange(15), rng.randrange(15)
        px(img, x, y, SOIL[4]); px(img, x + 1, y + 1, SOIL[0])
    return img


def sand():
    rng = random.Random(5)
    img = new()
    noise_fill(img, SAND[1:5], rng, [1, 4, 4, 2])
    for y in (3, 9, 14):  # petites dunes
        for x in range(16):
            if (x + y) % 5 < 3:
                px(img, x, y, SAND[0] if x % 2 else SAND[1])
    return img


def grass_top():
    """Niveaux de gris : Minecraft teinte selon le biome."""
    rng = random.Random(6)
    img = new()
    noise_fill(img, [(120, 120, 120), (140, 140, 140), (156, 156, 156), (172, 172, 172)], rng, [1, 3, 3, 2])
    for _ in range(10):
        x, y = rng.randrange(16), rng.randrange(15)
        px(img, x, y, (196, 196, 196)); px(img, x, y + 1, (108, 108, 108))
    return img


def grass_side():
    img = dirt()
    over = grass_side_overlay()
    for y in range(16):
        for x in range(16):
            if over.getpixel((x, y))[3]:
                img.putpixel((x, y), over.getpixel((x, y)))
    return img


def grass_side_overlay():
    rng = random.Random(7)
    img = new()
    for x in range(16):
        depth = 3 + (1 if rng.random() < 0.5 else 0) + (2 if rng.random() < 0.2 else 0)
        for y in range(depth):
            g = rng.choice((130, 148, 160, 172))
            px(img, x, y, (g, g, g))
    return img


def oak_planks():
    """Plaques de blindage orange boulonnées."""
    rng = random.Random(8)
    img = new()
    for i, y0 in enumerate((0, 4, 8, 12)):
        noise_fill(img, ORANGE[2:4], rng, [2, 3], (0, y0, 15, y0 + 3))
        for x in range(16):
            px(img, x, y0, ORANGE[4])
            px(img, x, y0 + 3, ORANGE[1])
        cut = 5 if i % 2 == 0 else 11
        for y in range(y0, y0 + 4):
            px(img, cut, y, ORANGE[0])
        px(img, (cut + 3) % 16, y0 + 1, STEEL[5]); px(img, (cut + 3) % 16, y0 + 2, STEEL[1])
    return img


def crafting_top():
    img = new(fill=STEEL[2])
    noise_fill(img, STEEL[2:4], random.Random(9), [3, 1])
    bevel(img, 0, 0, 15, 15, STEEL[4], STEEL[0])
    for i in range(2, 14, 4):  # grille 3x3 du plan de travail
        for j in range(2, 14, 4):
            rect(img, i, j, i + 2, j + 2, STEEL[1])
            px(img, i + 2, j + 2, STEEL[3])
    for x, y in ((1, 1), (13, 1), (1, 13), (13, 13)):
        px(img, x, y, ORANGE[3])
    return img


def crafting_front():
    img = crafting_side(drawer=False)
    rect(img, 1, 1, 14, 9, DARKSTEEL[2])  # panneau à outils
    for x in range(2, 14, 2):
        for y in range(2, 9, 2):
            px(img, x, y, DARKSTEEL[1])
    # clé à molette accrochée
    for y in range(3, 9):
        px(img, 4, y, STEEL[4]); px(img, 5, y, STEEL[2])
    rect(img, 3, 2, 6, 3, STEEL[4]); px(img, 4, 2, DARKSTEEL[2]); px(img, 5, 2, DARKSTEEL[2])
    # marteau
    for y in range(4, 9):
        px(img, 10, y, ORANGE[3]); px(img, 11, y, ORANGE[1])
    rect(img, 8, 2, 13, 3, STEEL[3]); rect(img, 8, 3, 13, 3, STEEL[1])
    bevel(img, 1, 1, 14, 9, DARKSTEEL[0], DARKSTEEL[4])
    return img


def crafting_side(drawer=True):
    rng = random.Random(10)
    img = new()
    noise_fill(img, ORANGE[2:4], rng, [3, 2])
    bevel(img, 0, 0, 15, 15, ORANGE[4], ORANGE[0])
    rect(img, 0, 0, 15, 1, STEEL[3]); rect(img, 0, 1, 15, 1, STEEL[1])
    if drawer:
        bevel(img, 3, 10, 12, 14, ORANGE[1], ORANGE[4])
        rect(img, 6, 12, 9, 12, STEEL[4])
        bevel(img, 3, 4, 12, 8, ORANGE[1], ORANGE[4])
        rect(img, 6, 6, 9, 6, STEEL[4])
    else:
        bevel(img, 3, 11, 12, 14, ORANGE[1], ORANGE[4])
        rect(img, 6, 12, 9, 12, STEEL[4])
    return img


def glass():
    """Champ de force : uniquement pixels 100% opaques ou transparents (rendu cutout)."""
    img = new()
    for i in range(16):
        for c in ((i, 0), (i, 15), (0, i), (15, i)):
            px(img, *c, CYAN[3])
    for c in ((0, 0), (15, 0), (0, 15), (15, 15)):
        px(img, *c, CYAN[5])
    for x, y in ((3, 4), (4, 3), (5, 2), (3, 6), (4, 5), (11, 12), (12, 11)):
        px(img, x, y, CYAN[4])
    return img


def ore(base, pal, seed, kind="chunk"):
    rng = random.Random(seed)
    img = base.copy()
    spots = [(2, 3), (9, 2), (5, 8), (11, 9), (3, 12), (12, 13)]
    rng.shuffle(spots)
    for (x, y) in spots[:5]:
        if kind == "crystal":
            px(img, x, y + 1, pal[2]); px(img, x + 1, y, pal[4]); px(img, x + 1, y + 1, pal[3])
            px(img, x + 1, y - 1, pal[5]); px(img, x + 2, y + 1, pal[1]); px(img, x, y + 2, OUT)
        elif kind == "bolt":
            rect(img, x, y, x + 1, y + 1, pal[3]); px(img, x, y, pal[5]); px(img, x + 2, y + 1, pal[1])
            px(img, x + 1, y + 2, pal[1]); px(img, x + 1, y + 1, pal[2])
        else:
            rect(img, x, y, x + 1, y + 1, pal[3]); px(img, x, y, pal[4]); px(img, x + 1, y + 1, pal[1])
            if rng.random() < 0.5:
                px(img, x + 2, y, pal[2])
    return img


def tnt_side():
    """Caisse explosive avec bande de danger."""
    img = new(fill=RED[2])
    noise_fill(img, RED[2:4], random.Random(11), [3, 1])
    bevel(img, 0, 0, 15, 15, RED[4], RED[0])
    for y in range(5, 11):  # bande jaune/noire
        for x in range(1, 15):
            px(img, x, y, (250, 206, 40) if ((x + y) // 2) % 2 == 0 else (30, 26, 30))
    for x in range(1, 15):
        px(img, x, 4, STEEL[4]); px(img, x, 11, STEEL[1])
    for x, y in ((1, 1), (13, 1), (1, 13), (13, 13)):
        rivet(img, x, y)
    return img


def tnt_top(bottom=False):
    img = new(fill=RED[2])
    noise_fill(img, RED[2:4], random.Random(12), [3, 1])
    bevel(img, 0, 0, 15, 15, RED[4], RED[0])
    if not bottom:  # détonateur
        b = shape(lambda x, y: math.hypot(x - 7.5, y - 7.5) <= 4.2, STEEL, base=3)
        paste(img, b)
        b2 = shape(lambda x, y: math.hypot(x - 7.5, y - 7.5) <= 2.0, RED, base=4)
        paste(img, b2)
        px(img, 7, 6, RED[5])
    else:
        for x in range(2, 14):
            px(img, x, 7, RED[0]); px(img, x, 8, RED[4])
    for x, y in ((1, 1), (13, 1), (1, 13), (13, 13)):
        rivet(img, x, y)
    return img


def obsidian():
    """Panneau sombre parcouru de circuits violets."""
    rng = random.Random(13)
    img = new()
    noise_fill(img, DARKSTEEL[0:3], rng, [3, 3, 1])
    paths = [[(0, 3), (5, 3), (5, 8), (10, 8)], [(15, 12), (11, 12), (11, 15)],
             [(8, 0), (8, 4), (13, 4), (13, 8)], [(0, 12), (3, 12), (3, 15)]]
    for path in paths:
        for (ax, ay), (bx, by) in zip(path, path[1:]):
            for x in range(min(ax, bx), max(ax, bx) + 1):
                for y in range(min(ay, by), max(ay, by) + 1):
                    px(img, x, y, PURPLE[2])
        ex, ey = path[-1]
        px(img, ex, ey, PURPLE[4])
    for x, y in ((10, 8), (13, 8), (5, 3)):
        px(img, x, y, PURPLE[5])
    return img


def glowstone():
    """Panneau néon cyan."""
    img = new(fill=CYAN[2])
    for y in range(16):
        for x in range(16):
            if x % 5 == 0 or y % 5 == 0:
                px(img, x, y, CYAN[1])
            elif (x % 5 in (1, 2)) and (y % 5 in (1, 2)):
                px(img, x, y, CYAN[5] if (x % 5, y % 5) == (1, 1) else CYAN[4])
            else:
                px(img, x, y, CYAN[3])
    return img


def lamp(on):
    img = new(fill=STEEL[1])
    bevel(img, 0, 0, 15, 15, STEEL[3], STEEL[0])
    for x, y in ((1, 1), (13, 1), (1, 13), (13, 13)):
        rivet(img, x, y)
    pal = ORANGE if on else [(40, 30, 30), (60, 40, 34), (80, 54, 40), (100, 66, 46), (120, 80, 56), (140, 96, 66)]
    lens = shape(lambda x, y: math.hypot(x - 7.5, y - 7.5) <= 5.2, pal, base=3)
    paste(img, lens)
    px(img, 5, 5, pal[5]); px(img, 6, 5, pal[5]); px(img, 5, 6, pal[5])
    return img


def furnace_front(on):
    img = furnace_side()
    rect(img, 3, 3, 12, 12, DARKSTEEL[0])
    bevel(img, 3, 3, 12, 12, STEEL[0], STEEL[4])
    if on:
        for y in range(4, 12):
            for x in range(4, 12):
                d = math.hypot(x - 7.5, y - 9)
                px(img, x, y, CYAN[5] if d < 1.6 else CYAN[4] if d < 2.8 else CYAN[3] if d < 4 else CYAN[1])
    else:
        for x in range(4, 12, 2):
            px(img, x, 10, STEEL[1]); px(img, x + 1, 11, STEEL[1])
    return img


def furnace_side():
    rng = random.Random(14)
    img = new()
    noise_fill(img, STEEL[1:3], rng, [1, 3])
    bevel(img, 0, 0, 15, 15, STEEL[3], STEEL[0])
    for y in (13, 14):
        for x in range(1, 15):
            px(img, x, y, ORANGE[3] if (x // 2) % 2 == 0 else DARKSTEEL[1])
    return img


def furnace_top():
    img = furnace_side()
    for y in range(4, 12, 2):  # grille d'aération
        rect(img, 3, y, 12, y, DARKSTEEL[0])
        rect(img, 3, y + 1, 12, y + 1, STEEL[3])
    return img


# --------------------------------------------------------------------------
# Objets
# --------------------------------------------------------------------------
def bolt_item():
    """Boulon : la monnaie de l'univers (remplace la pépite d'or)."""
    img = shape(lambda x, y: in_hex(x, y, 7.5, 7.5, 6.2), BRASS, base=3)
    ring = shape(lambda x, y: math.hypot(x - 7.5, y - 7.5) <= 2.6, BRASS, base=2)
    paste(img, ring)
    rect(img, 6, 7, 9, 8, BRASS[0])  # fente du boulon
    px(img, 4, 4, BRASS[5])
    return outline(img)


def wrench(pal, grip, glow=None):
    """Clé à molette en diagonale (manche en bas à gauche, mâchoire en haut à droite)."""
    cx, cy = 11.3, 4.7

    def mask(x, y):
        d = math.hypot(x - cx, y - cy)
        ang = math.degrees(math.atan2(-(y - cy), x - cx))  # 45° = haut-droite
        head = 1.7 <= d <= 3.9 and abs(ang - 45) > 38
        dh, _ = seg_dist(x, y, 2.2, 13.8, 9.4, 6.6)
        return head or dh <= 1.05

    img = shape(mask, pal, base=3)
    for y in range(16):  # poignée
        for x in range(16):
            if img.getpixel((x, y))[3]:
                d, t = seg_dist(x, y, 2.2, 13.8, 9.4, 6.6)
                if t < 0.45 and d <= 1.05:
                    img.putpixel((x, y), rgba(grip[3] if (x + y) % 3 else grip[1]))
    px(img, 2, 13, pal[1])  # trou d'accroche
    if glow:
        for x, y in ((9, 2), (13, 7), (12, 1), (14, 4)):
            if img.getpixel((x, y))[3]:
                px(img, x, y, glow)
    return outline(img)


def blaster(charge=0):
    """Blaster (remplace l'arc). charge = 0..3 pour l'animation de tir."""
    def body(x, y):
        d, _ = seg_dist(x, y, 3.0, 12.0, 8.5, 6.5)
        return d <= 1.9

    def barrel(x, y):
        d, _ = seg_dist(x, y, 7.5, 7.5, 13.2, 1.8)
        return d <= 1.0

    def handle(x, y):
        d, _ = seg_dist(x, y, 6.0, 10.0, 8.6, 12.6)
        return d <= 1.1

    img = shape(barrel, STEEL, base=3)
    paste(img, shape(handle, DARKSTEEL, base=3))
    paste(img, shape(body, ORANGE, base=3))
    for x, y in ((5, 9), (6, 8), (4, 10)):  # cellule d'énergie
        px(img, x, y, CYAN[4] if charge == 0 else CYAN[5])
    px(img, 13, 2, CYAN[3])
    if charge:
        glow = [None, CYAN[3], CYAN[4], CYAN[5]][charge]
        pts = [(14, 1), (13, 1), (14, 2), (15, 0), (12, 1), (14, 3)][: 2 + charge]
        for x, y in pts:
            px(img, x, y, glow)
    return outline(img)


def ingot(pal, stamp):
    def mask(x, y):
        return 2 <= x <= 13 and 5 <= y <= 11 and not ((x, y) in ((2, 5), (13, 5), (2, 11), (13, 11)))

    img = shape(mask, pal, base=3)
    for x in range(4, 12):
        px(img, x, 7, pal[4])
    rect(img, 6, 8, 9, 9, stamp)
    return outline(img)


def crystal():
    def mask(x, y):
        d1, _ = seg_dist(x, y, 5, 12, 9, 3)
        d2, _ = seg_dist(x, y, 9, 13, 12, 6)
        return d1 <= 2.0 or d2 <= 1.4

    img = shape(mask, PURPLE, base=3)
    for x, y in ((8, 4), (7, 6), (11, 7)):
        px(img, x, y, CYAN[5])
    px(img, 6, 9, CYAN[3]); px(img, 10, 10, CYAN[3])
    return outline(img)


def energy_cell():
    def mask(x, y):
        return 5 <= x <= 10 and 2 <= y <= 13

    img = shape(mask, STEEL, base=3)
    core = shape(lambda x, y: 6 <= x <= 9 and 4 <= y <= 11, GREEN, base=3)
    paste(img, core)
    for y in range(5, 11, 2):
        px(img, 7, y, GREEN[5])
    rect(img, 7, 1, 8, 1, STEEL[4])
    return outline(img)


def health_capsule():
    img = shape(lambda x, y: math.hypot(x - 7.5, y - 8.5) <= 5.3, RED, base=3)
    rect(img, 7, 5, 8, 11, RED[5]); rect(img, 5, 7, 10, 8, RED[5])
    rect(img, 7, 1, 8, 3, STEEL[3]); px(img, 7, 1, STEEL[5])
    px(img, 4, 5, (255, 255, 255))
    return outline(img)


def mini_bomb():
    img = shape(lambda x, y: math.hypot(x - 7.5, y - 8.5) <= 4.8, STEEL, base=2)
    for x in range(3, 13):
        if img.getpixel((x, 8))[3]:
            px(img, x, 8, ORANGE[3]); px(img, x, 9, ORANGE[1])
    rect(img, 7, 2, 8, 3, STEEL[4]); px(img, 9, 2, CYAN[4])
    px(img, 5, 6, STEEL[5])
    return outline(img)


def teleport_orb():
    img = shape(lambda x, y: math.hypot(x - 7.5, y - 7.5) <= 5.5, CYAN, base=2)
    for t in range(0, 360, 40):  # spirale
        r = 1 + t / 90
        x = 7.5 + r * math.cos(math.radians(t))
        y = 7.5 + r * math.sin(math.radians(t))
        px(img, int(round(x)), int(round(y)), PURPLE[4])
    px(img, 7, 7, (255, 255, 255)); px(img, 5, 4, CYAN[5])
    return outline(img)


# --------------------------------------------------------------------------
# Icône du pack
# --------------------------------------------------------------------------
def pack_icon():
    rng = random.Random(42)
    img = new(32, 32)
    for y in range(32):
        for x in range(32):
            t = y / 31
            img.putpixel((x, y), (int(14 + 40 * t), int(16 + 10 * t), int(46 + 40 * t), 255))
    for _ in range(26):
        px(img, rng.randrange(32), rng.randrange(32), rng.choice([(255, 255, 255), CYAN[4], BRASS[5]]))
    planet = shape(lambda x, y: math.hypot(x - 30, y - 32) <= 13, ORANGE, 32, 32, base=3)
    paste(img, planet)
    for x in range(14, 32):
        px(img, x, 24 + (x % 3 == 0), ORANGE[1])
    bolt = shape(lambda x, y: in_hex(x, y, 13.5, 13.5, 9.5), BRASS, 32, 32, base=3)
    ring = shape(lambda x, y: math.hypot(x - 13.5, y - 13.5) <= 4.2, BRASS, 32, 32, base=2)
    paste(bolt, ring)
    rect(bolt, 10, 13, 17, 14, BRASS[0])
    px(bolt, 8, 7, BRASS[5]); px(bolt, 9, 7, BRASS[5]); px(bolt, 8, 8, BRASS[5])
    outline(bolt)
    paste(img, bolt)
    return img.resize((128, 128), Image.NEAREST)


# --------------------------------------------------------------------------
# Assemblage
# --------------------------------------------------------------------------
def build():
    base_stone = stone()
    blocks = {
        "stone": base_stone,
        "iron_block": iron_block(),
        "gold_block": gold_block(),
        "cobblestone": cobblestone(),
        "dirt": dirt(),
        "sand": sand(),
        "grass_block_top": grass_top(),
        "grass_block_side": grass_side(),
        "grass_block_side_overlay": grass_side_overlay(),
        "oak_planks": oak_planks(),
        "crafting_table_top": crafting_top(),
        "crafting_table_front": crafting_front(),
        "crafting_table_side": crafting_side(),
        "glass": glass(),
        "coal_ore": ore(base_stone, DARKSTEEL, 20),
        "iron_ore": ore(base_stone, STEEL, 21),
        "gold_ore": ore(base_stone, BRASS, 22, "bolt"),
        "diamond_ore": ore(base_stone, PURPLE, 23, "crystal"),
        "emerald_ore": ore(base_stone, GREEN, 24, "crystal"),
        "redstone_ore": ore(base_stone, RED, 25),
        "tnt_side": tnt_side(),
        "tnt_top": tnt_top(),
        "tnt_bottom": tnt_top(bottom=True),
        "obsidian": obsidian(),
        "glowstone": glowstone(),
        "redstone_lamp": lamp(False),
        "redstone_lamp_on": lamp(True),
        "furnace_front": furnace_front(False),
        "furnace_front_on": furnace_front(True),
        "furnace_side": furnace_side(),
        "furnace_top": furnace_top(),
    }
    items = {
        "gold_nugget": bolt_item(),
        "wooden_sword": wrench(WOODISH, STEEL),
        "stone_sword": wrench(STEEL[:1] + STEEL[:5], ORANGE),
        "iron_sword": wrench(STEEL, ORANGE),
        "golden_sword": wrench(BRASS, DARKSTEEL),
        "diamond_sword": wrench(CYAN, ORANGE, glow=CYAN[5]),
        "netherite_sword": wrench(DARKSTEEL, PURPLE, glow=PURPLE[4]),
        "bow": blaster(0),
        "bow_pulling_0": blaster(1),
        "bow_pulling_1": blaster(2),
        "bow_pulling_2": blaster(3),
        "iron_ingot": ingot(STEEL, STEEL[1]),
        "gold_ingot": ingot(BRASS, BRASS[1]),
        "diamond": crystal(),
        "emerald": energy_cell(),
        "apple": health_capsule(),
        "snowball": mini_bomb(),
        "ender_pearl": teleport_orb(),
    }

    if os.path.isdir(PACK):
        shutil.rmtree(PACK)
    for d in (BLOCK, ITEM, LANG):
        os.makedirs(d)
    for name, img in blocks.items():
        img.save(os.path.join(BLOCK, name + ".png"))
    for name, img in items.items():
        img.save(os.path.join(ITEM, name + ".png"))
    pack_icon().save(os.path.join(PACK, "pack.png"))

    import mobs  # textures des ennemis
    entity_dir = os.path.join(PACK, "assets", "minecraft", "textures", "entity")
    for rel, img in mobs.textures().items():
        path = os.path.join(entity_dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path)

    mcmeta = {
        "pack": {
            "pack_format": 46,
            "supported_formats": [34, 99],
            "min_format": 34,
            "max_format": 99,
            "description": "§6Boulons §f& §bGalaxies§r\n§7Pack sci-fi mécanique (fan-made)",
        }
    }
    with open(os.path.join(PACK, "pack.mcmeta"), "w", encoding="utf-8") as f:
        json.dump(mcmeta, f, ensure_ascii=False, indent=2)

    names_fr = {
        "item.minecraft.gold_nugget": "Boulon",
        "item.minecraft.wooden_sword": "Clé de fortune",
        "item.minecraft.stone_sword": "Clé rouillée",
        "item.minecraft.iron_sword": "Clé à molette en acier",
        "item.minecraft.golden_sword": "Clé en laiton",
        "item.minecraft.diamond_sword": "Clé à énergie",
        "item.minecraft.netherite_sword": "Clé du néant",
        "item.minecraft.bow": "Blaster",
        "item.minecraft.iron_ingot": "Barre d'acier",
        "item.minecraft.gold_ingot": "Barre de laiton",
        "item.minecraft.diamond": "Cristal rare",
        "item.minecraft.emerald": "Cellule d'énergie",
        "item.minecraft.apple": "Capsule de soin",
        "item.minecraft.snowball": "Mini-bombe",
        "item.minecraft.ender_pearl": "Orbe de téléportation",
        "block.minecraft.gold_block": "Bloc de boulons",
        "block.minecraft.iron_block": "Bloc de blindage",
        "block.minecraft.crafting_table": "Établi mécanique",
        "block.minecraft.tnt": "Caisse explosive",
        "block.minecraft.glass": "Champ de force",
        "block.minecraft.glowstone": "Panneau néon",
        "block.minecraft.obsidian": "Panneau de circuits",
        "block.minecraft.furnace": "Forge à plasma",
        "block.minecraft.oak_planks": "Plaques de blindage",
        "block.minecraft.cobblestone": "Ferraille",
    }
    names_en = {
        "item.minecraft.gold_nugget": "Bolt",
        "item.minecraft.wooden_sword": "Makeshift Wrench",
        "item.minecraft.stone_sword": "Rusty Wrench",
        "item.minecraft.iron_sword": "Steel Wrench",
        "item.minecraft.golden_sword": "Brass Wrench",
        "item.minecraft.diamond_sword": "Energy Wrench",
        "item.minecraft.netherite_sword": "Void Wrench",
        "item.minecraft.bow": "Blaster",
        "item.minecraft.iron_ingot": "Steel Bar",
        "item.minecraft.gold_ingot": "Brass Bar",
        "item.minecraft.diamond": "Rare Crystal",
        "item.minecraft.emerald": "Energy Cell",
        "item.minecraft.apple": "Health Capsule",
        "item.minecraft.snowball": "Mini Bomb",
        "item.minecraft.ender_pearl": "Teleport Orb",
        "block.minecraft.gold_block": "Block of Bolts",
        "block.minecraft.iron_block": "Armor Plating Block",
        "block.minecraft.crafting_table": "Mechanic Workbench",
        "block.minecraft.tnt": "Explosive Crate",
        "block.minecraft.glass": "Force Field",
        "block.minecraft.glowstone": "Neon Panel",
        "block.minecraft.obsidian": "Circuit Panel",
        "block.minecraft.furnace": "Plasma Forge",
        "block.minecraft.oak_planks": "Armor Plates",
        "block.minecraft.cobblestone": "Scrap Metal",
    }
    names_fr.update(mobs.NAMES_FR)
    names_en.update(mobs.NAMES_EN)
    for fname, data in (("fr_fr.json", names_fr), ("en_us.json", names_en)):
        with open(os.path.join(LANG, fname), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # Archive prête à glisser dans .minecraft/resourcepacks
    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)
    zpath = os.path.join(dist, PACK_NAME + ".zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, _, files in os.walk(PACK):
            for fn in sorted(files):
                full = os.path.join(folder, fn)
                z.write(full, os.path.relpath(full, PACK))

    make_preview(blocks, items)
    print(f"{len(blocks)} blocs, {len(items)} objets -> {zpath}")


def make_preview(blocks, items):
    scale, pad, cols = 6, 10, 8
    cell = 16 * scale + pad
    entries = list(blocks.items()) + list(items.items())
    rows = math.ceil(len(entries) / cols)
    W, H = cols * cell + pad, rows * (cell + 14) + pad + 40
    img = Image.new("RGBA", (W, H), (24, 22, 36, 255))
    d = ImageDraw.Draw(img)
    d.text((pad, 12), "Boulons & Galaxies - apercu des textures", fill=(255, 200, 90, 255))
    for i, (name, tex) in enumerate(entries):
        cx = pad + (i % cols) * cell
        cy = 40 + (i // cols) * (cell + 14)
        bg = Image.new("RGBA", (16 * scale, 16 * scale), (52, 50, 70, 255))
        bg.alpha_composite(tex.resize((16 * scale, 16 * scale), Image.NEAREST))
        img.paste(bg, (cx, cy))
        d.text((cx, cy + 16 * scale + 2), name[:17], fill=(200, 200, 220, 255))
    img.save(os.path.join(ROOT, "preview.png"))


if __name__ == "__main__":
    build()
