"""Textures des ennemis (mobs) du pack « Boulons & Galaxies ».

Designs originaux sur le thème « invasion robotique / soldats extraterrestres ».
Chaque texture respecte le patron UV (box UV) du modèle Minecraft Java remplacé.
"""
from PIL import Image, ImageOps

from generate import (BRASS, CYAN, DARKSTEEL, ORANGE, OUT, RED, STEEL, T, new, px, rect)
import random

ARMOR = [(40, 20, 62), (66, 34, 98), (98, 54, 140), (134, 84, 178), (176, 130, 218)]
VISOR = [(110, 10, 20), (200, 30, 40), (255, 84, 70), (255, 180, 160)]
SUIT = [(36, 36, 44), (52, 52, 62), (70, 70, 82)]
HAZ_Y, HAZ_K = (250, 206, 40), (30, 26, 30)


# --------------------------------------------------------------------------
# Outils
# --------------------------------------------------------------------------
def noisy(w, h, pal, seed, weights=None):
    rng = random.Random(seed)
    img = new(w, h)
    for y in range(h):
        for x in range(w):
            px(img, x, y, rng.choices(pal, weights=weights)[0])
    return img


def regions(u, v, w, h, d):
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}


def put(tex, u, v, w, h, d, **faces):
    reg = regions(u, v, w, h, d)
    for name, img in faces.items():
        x, y, rw, rh = reg[name]
        assert img.size == (rw, rh), (name, img.size, (rw, rh))
        tex.paste(img, (x, y))


def hstripes(img, y0, y1, a=HAZ_Y, b=HAZ_K):
    for y in range(y0, y1 + 1):
        for x in range(img.width):
            px(img, x, y, a if ((x + y) // 2) % 2 == 0 else b)


# --------------------------------------------------------------------------
# Zombie -> Soldat envahisseur (64x64, modèle humanoïde)
# --------------------------------------------------------------------------
def zombie():
    tex = new(64, 64)
    A = ARMOR

    def helmet_side(front_left, seed):
        s = noisy(8, 8, [A[2], A[2], A[3]], seed, [3, 1, 1])
        rect(s, 0, 0, 7, 0, A[3])
        fx = (0, 1) if front_left else (6, 7)
        for x in fx:
            px(s, x, 2, OUT); px(s, x, 3, VISOR[1]); px(s, x, 4, OUT)
        cx = 4 if front_left else 2
        rect(s, cx, 3, cx + 1, 4, STEEL[3]); px(s, cx, 3, STEEL[5]); px(s, cx + 1, 4, STEEL[1])
        rect(s, 0, 7, 7, 7, A[1])
        return s

    hf = noisy(8, 8, [A[2], A[2], A[3]], 1, [3, 1, 1])
    rect(hf, 0, 0, 7, 0, A[4])
    rect(hf, 0, 2, 7, 2, OUT); rect(hf, 0, 3, 7, 3, VISOR[1]); rect(hf, 0, 4, 7, 4, OUT)
    for x in (1, 2, 5, 6):
        px(hf, x, 3, VISOR[2])
    px(hf, 1, 3, VISOR[3]); px(hf, 5, 3, VISOR[3])
    rect(hf, 1, 5, 6, 7, STEEL[2]); rect(hf, 1, 5, 6, 5, STEEL[4])
    for x in (2, 4):
        rect(hf, x, 6, x, 7, STEEL[0])
    px(hf, 0, 7, A[1]); px(hf, 7, 7, A[1])

    hb = noisy(8, 8, [A[2], A[2], A[3]], 2, [3, 1, 1])
    rect(hb, 0, 0, 7, 0, A[3])
    for y in (4, 6):
        rect(hb, 2, y, 5, y, A[0])
    ht = noisy(8, 8, [A[2], A[3]], 3, [2, 1])
    rect(ht, 3, 0, 4, 7, A[4])
    put(tex, 0, 0, 8, 8, 8, top=ht, bottom=new(8, 8, A[0]), front=hf, back=hb,
        left=helmet_side(True, 4), right=helmet_side(False, 5))

    # couche « chapeau » : crête orange sur le casque
    crest_top = new(8, 8)
    rect(crest_top, 3, 1, 4, 7, ORANGE[3]); rect(crest_top, 3, 1, 3, 7, ORANGE[4])
    crest_back = new(8, 8)
    rect(crest_back, 3, 0, 4, 1, ORANGE[2])
    put(tex, 32, 0, 8, 8, 8, top=crest_top, back=crest_back)

    # torse
    def torso(w, front=False, back=False, seed=6):
        f = noisy(w, 12, [A[2], A[2], A[3]], seed, [3, 1, 1])
        rect(f, 0, 0, w - 1, 0, A[4])
        rect(f, 0, 6, w - 1, 6, A[1])
        rect(f, 0, 7, w - 1, 8, SUIT[0]); rect(f, 0, 7, w - 1, 7, SUIT[2])
        for y in range(9, 12):
            for x in range(w):
                px(f, x, y, SUIT[1] if (x + y) % 4 else SUIT[0])
        if front:
            rect(f, 2, 2, 5, 2, ORANGE[3]); rect(f, 3, 3, 4, 3, ORANGE[3]); px(f, 2, 2, ORANGE[4])
            px(f, 0, 1, A[4]); px(f, 7, 1, A[4])
            rect(f, 3, 7, 4, 8, BRASS[3]); px(f, 3, 7, BRASS[5])
        if back:
            rect(f, 1, 1, 6, 6, STEEL[2]); rect(f, 1, 1, 6, 1, STEEL[4]); rect(f, 1, 6, 6, 6, STEEL[0])
            px(f, 2, 3, ORANGE[4]); px(f, 3, 3, ORANGE[3]); rect(f, 2, 5, 5, 5, STEEL[1])
        return f

    put(tex, 16, 16, 8, 12, 4, top=new(8, 4, A[3]), bottom=new(8, 4, SUIT[0]),
        front=torso(8, front=True), back=torso(8, back=True, seed=7),
        left=torso(4, seed=8), right=torso(4, seed=9))

    # bras
    def arm(seed, front=False):
        f = noisy(4, 12, [SUIT[1], SUIT[2]], seed, [3, 1])
        rect(f, 0, 0, 3, 3, A[3]); rect(f, 0, 0, 3, 0, A[4]); rect(f, 0, 3, 3, 3, A[1])
        rect(f, 0, 9, 3, 11, A[2]); rect(f, 0, 9, 3, 9, OUT)
        if front:
            rect(f, 0, 10, 3, 10, STEEL[3])
        return f

    put(tex, 40, 16, 4, 12, 4, top=new(4, 4, A[4]), bottom=new(4, 4, A[1]),
        front=arm(10, True), back=arm(11), left=arm(12), right=arm(13))

    # jambes
    def leg(seed, front=False):
        f = noisy(4, 12, [SUIT[1], SUIT[2]], seed, [3, 1])
        rect(f, 0, 7, 3, 11, A[2]); rect(f, 0, 7, 3, 7, A[4])
        if front:
            rect(f, 0, 4, 3, 5, A[3]); px(f, 1, 4, A[4])
            rect(f, 0, 10, 3, 11, STEEL[3]); rect(f, 0, 11, 3, 11, STEEL[1])
        return f

    put(tex, 0, 16, 4, 12, 4, top=new(4, 4, SUIT[1]), bottom=new(4, 4, OUT),
        front=leg(14, True), back=leg(15), left=leg(16), right=leg(17))
    return tex


# --------------------------------------------------------------------------
# Squelette -> Droïde sentinelle (64x32)
# --------------------------------------------------------------------------
def skeleton():
    tex = new(64, 32)
    S = STEEL

    hf = noisy(8, 8, [S[3], S[3], S[4]], 20, [3, 1, 1])
    rect(hf, 0, 0, 7, 0, S[5]); rect(hf, 0, 7, 7, 7, S[1])
    for x, y in ((3, 1), (4, 1), (2, 2), (5, 2), (2, 3), (5, 3), (3, 4), (4, 4)):
        px(hf, x, y, OUT)
    rect(hf, 3, 2, 4, 3, RED[2]); px(hf, 3, 2, RED[5]); px(hf, 4, 2, RED[4])
    rect(hf, 2, 6, 5, 6, OUT); rect(hf, 2, 5, 5, 5, S[2])
    hs = noisy(8, 8, [S[3], S[3], S[4]], 21, [3, 1, 1])
    rect(hs, 0, 0, 7, 0, S[5]); rect(hs, 0, 7, 7, 7, S[1])
    rect(hs, 3, 3, 4, 4, S[1]); px(hs, 3, 3, S[5])
    hb = noisy(8, 8, [S[2], S[3]], 22)
    rect(hb, 1, 1, 6, 6, S[2]); rect(hb, 1, 1, 6, 1, S[4])
    for y in (3, 5):
        rect(hb, 2, y, 5, y, S[0])
    ht = noisy(8, 8, [S[3], S[4]], 23)
    rect(ht, 3, 3, 4, 4, OUT); px(ht, 3, 3, RED[4])
    put(tex, 0, 0, 8, 8, 8, top=ht, bottom=new(8, 8, S[1]), front=hf, back=hb, left=hs, right=hs)

    def frame(w, core=False):
        f = new(w, 12)
        rect(f, 0, 0, w - 1, 1, S[4]); rect(f, 0, 1, w - 1, 1, S[2])
        mid = w // 2
        rect(f, mid - 1, 0, mid, 11, S[3]) if w > 4 else rect(f, 1, 0, 2, 11, S[3])
        for y in (3, 5, 7):
            rect(f, 1 if w > 4 else 0, y, w - 2 if w > 4 else w - 1, y, S[2])
        rect(f, 0, 10, w - 1, 11, S[3]); rect(f, 0, 11, w - 1, 11, S[1])
        if core:
            rect(f, 3, 4, 4, 5, RED[2]); px(f, 3, 4, RED[5])
        return f

    put(tex, 16, 16, 8, 12, 4, top=new(8, 4, S[4]), bottom=new(8, 4, S[2]),
        front=frame(8, core=True), back=frame(8), left=frame(4), right=frame(4))

    def limb(seed, hand_color):
        f = noisy(2, 12, [S[3], S[4]], seed)
        rect(f, 0, 5, 1, 6, S[0]); px(f, 0, 5, RED[3])
        rect(f, 0, 10, 1, 11, hand_color)
        return f

    for (u, v, hand) in ((40, 16, S[1]), (0, 16, DARKSTEEL[2])):
        put(tex, u, v, 2, 12, 2, top=new(2, 2, S[4]), bottom=new(2, 2, S[1]),
            front=limb(u + 1, hand), back=limb(u + 2, hand), left=limb(u + 3, hand), right=limb(u + 4, hand))
    return tex


# --------------------------------------------------------------------------
# Creeper -> Bombe-robot (64x32)
# --------------------------------------------------------------------------
def creeper():
    tex = new(64, 32)
    D = DARKSTEEL

    hf = noisy(8, 8, [STEEL[1], STEEL[2]], 30)
    rect(hf, 1, 1, 6, 6, OUT)
    for x, y in ((1, 2), (2, 3), (2, 2), (6, 2), (5, 3), (5, 2)):  # yeux LED en colère
        px(hf, x, y, ORANGE[4])
    px(hf, 2, 3, ORANGE[5]); px(hf, 5, 3, ORANGE[5])
    for x, y in ((2, 5), (3, 4), (4, 5), (5, 4)):  # bouche en zigzag
        px(hf, x, y, ORANGE[3])
    rect(hf, 0, 0, 7, 0, STEEL[3])
    hs = noisy(8, 8, [STEEL[1], STEEL[2]], 31)
    rect(hs, 0, 0, 7, 0, STEEL[3])
    for y in (2, 4, 6):
        rect(hs, 2, y, 5, y, OUT)
    ht = noisy(8, 8, [STEEL[2], STEEL[3]], 32)
    rect(ht, 3, 3, 4, 4, RED[2]); px(ht, 3, 3, RED[5]); px(ht, 4, 4, RED[1])
    hb = hs.copy()
    hstripes(hb, 6, 7)
    put(tex, 0, 0, 8, 8, 8, top=ht, bottom=new(8, 8, STEEL[0]), front=hf, back=hb, left=hs, right=hs)

    def casing(w, seed, display=False, tanks=False):
        f = noisy(w, 12, [RED[2], RED[2], RED[3]], seed, [3, 1, 1])
        hstripes(f, 0, 1)
        hstripes(f, 10, 11)
        if display:
            rect(f, 1, 4, 6, 7, OUT)
            for x in (2, 4):
                rect(f, x, 5, x, 6, RED[4])
            px(f, 3, 5, RED[4]); px(f, 5, 6, RED[4]); px(f, 6, 5, RED[4])
            px(f, 1, 3, STEEL[5]); px(f, 6, 8, STEEL[5])
        if tanks:
            for x0 in (1, 5):
                rect(f, x0, 3, x0 + 1, 8, STEEL[3]); rect(f, x0, 3, x0, 8, STEEL[5])
                px(f, x0, 2, STEEL[1]); px(f, x0 + 1, 9, STEEL[1])
        return f

    put(tex, 16, 16, 8, 12, 4, top=new(8, 4, STEEL[2]), bottom=new(8, 4, STEEL[0]),
        front=casing(8, 33, display=True), back=casing(8, 34, tanks=True),
        left=casing(4, 35), right=casing(4, 36))

    def leg(seed):
        f = noisy(4, 6, [STEEL[2], STEEL[3]], seed)
        rect(f, 0, 2, 3, 2, STEEL[1])
        rect(f, 0, 4, 3, 5, ORANGE[3]); rect(f, 0, 5, 3, 5, ORANGE[1])
        return f

    put(tex, 0, 16, 4, 6, 4, top=new(4, 4, STEEL[3]), bottom=new(4, 4, D[0]),
        front=leg(37), back=leg(38), left=leg(39), right=leg(40))
    return tex


# --------------------------------------------------------------------------
# Araignée -> Araignée mécanique (64x32) + yeux lumineux
# --------------------------------------------------------------------------
EYE_PIXELS = [(1, 3), (2, 3), (5, 3), (6, 3), (3, 2), (4, 2), (2, 5), (5, 5)]


def spider(accent=ORANGE, body=STEEL, seed=50):
    tex = new(64, 32)

    hf = noisy(8, 8, [body[2], body[3]], seed)
    rect(hf, 0, 0, 7, 0, body[4])
    for x, y in EYE_PIXELS:
        px(hf, x, y, OUT)
    rect(hf, 1, 6, 1, 7, accent[3]); rect(hf, 6, 6, 6, 7, accent[3])
    rect(hf, 3, 7, 4, 7, body[0])
    hs = noisy(8, 8, [body[2], body[3]], seed + 1)
    rect(hs, 0, 0, 7, 0, body[4]); px(hs, 3, 4, body[5]); px(hs, 4, 5, body[1])
    put(tex, 32, 4, 8, 8, 8, top=noisy(8, 8, [body[3], body[4]], seed + 2), bottom=new(8, 8, body[1]),
        front=hf, back=hs, left=hs, right=hs)

    neck = noisy(6, 6, [DARKSTEEL[2], DARKSTEEL[3]], seed + 3)
    for y in (1, 4):
        rect(neck, 0, y, 5, y, accent[2])
    put(tex, 0, 0, 6, 6, 6, top=neck, bottom=neck, front=neck, back=neck, left=neck, right=neck)

    top = noisy(10, 12, [body[2], body[3]], seed + 4)
    for y in (0, 11):
        rect(top, 0, y, 9, y, body[1])
    rect(top, 4, 1, 5, 10, accent[3]); rect(top, 4, 1, 4, 10, accent[4])
    for y in (3, 7):
        rect(top, 1, y, 2, y, OUT); rect(top, 7, y, 8, y, OUT)
    px(top, 1, 1, body[5]); px(top, 8, 1, body[5]); px(top, 1, 10, body[5]); px(top, 8, 10, body[5])

    def flank(seed_):
        f = noisy(12, 8, [body[1], body[2]], seed_)
        rect(f, 0, 0, 11, 0, body[4])
        for x in (3, 7):
            rect(f, x, 1, x, 6, body[0])
        px(f, 1, 2, body[5]); px(f, 10, 2, body[5])
        rect(f, 1, 5, 10, 5, accent[2])
        return f

    rear = noisy(10, 8, [body[1], body[2]], seed + 7)
    rect(rear, 3, 2, 6, 5, OUT); rect(rear, 4, 3, 5, 4, accent[4])
    put(tex, 0, 12, 10, 8, 12, top=top, bottom=new(10, 12, body[0]), front=new(10, 8, DARKSTEEL[2]),
        back=rear, left=flank(seed + 5), right=flank(seed + 6))

    def leg_face(w, h, s):
        f = noisy(w, h, [body[2], body[3]], s)
        if w == 16:
            for x in (5, 10):
                rect(f, x, 0, x, h - 1, accent[3])
            rect(f, 0, 0, 1, h - 1, OUT)  # pointe de la patte (côté x0)
        return f

    put(tex, 18, 0, 16, 2, 2, top=leg_face(16, 2, seed + 8), bottom=leg_face(16, 2, seed + 9),
        front=leg_face(16, 2, seed + 10), back=leg_face(16, 2, seed + 11),
        left=leg_face(2, 2, seed + 12), right=new(2, 2, OUT))
    return tex


def spider_eyes(color=RED):
    eyes = new(64, 32)
    fx, fy = 40, 12  # face avant de la tête
    for i, (x, y) in enumerate(EYE_PIXELS):
        px(eyes, fx + x, fy + y, color[5] if i in (0, 5) else color[4] if i < 4 else color[3])
    return eyes


def textures():
    """Retourne {chemin relatif dans textures/entity: Image}."""
    return {
        "zombie/zombie.png": zombie(),
        "skeleton/skeleton.png": skeleton(),
        "creeper/creeper.png": creeper(),
        "spider/spider.png": spider(),
        "spider/cave_spider.png": spider(accent=CYAN, body=DARKSTEEL, seed=70),
        "spider/spider_eyes.png": spider_eyes(),  # 26.x
        "spider_eyes.png": spider_eyes(),  # 1.20.5 - 1.21.x
    }


NAMES_FR = {
    "entity.minecraft.zombie": "Soldat envahisseur",
    "entity.minecraft.skeleton": "Droïde sentinelle",
    "entity.minecraft.creeper": "Bombe-robot",
    "entity.minecraft.spider": "Araignée mécanique",
    "entity.minecraft.cave_spider": "Araignée-drone",
}
NAMES_EN = {
    "entity.minecraft.zombie": "Invader Trooper",
    "entity.minecraft.skeleton": "Sentry Droid",
    "entity.minecraft.creeper": "Bomb Bot",
    "entity.minecraft.spider": "Mech Spider",
    "entity.minecraft.cave_spider": "Spider Drone",
}
