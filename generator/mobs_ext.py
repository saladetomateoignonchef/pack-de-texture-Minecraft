"""Mobs de l'End, du Nether et mobs passifs du pack « Boulons & Galaxies » (Minecraft Java 26.x).

Designs originaux (robots, drones et créatures mécaniques). Les zones UV suivent la
géométrie des modèles vanilla 26.3 (boîtes : texOffs u, v + dimensions w, h, d).
"""
import random

from generate import BRASS, CYAN, DARKSTEEL, GREEN, ORANGE, OUT, PURPLE, RED, STEEL, new, px, rect
import mobs as base

# --------------------------------------------------------------------------
# Palettes (6 nuances, du plus sombre au plus clair)
# --------------------------------------------------------------------------
VOID = [(10, 8, 16), (18, 14, 28), (28, 22, 42), (40, 32, 58), (58, 46, 82), (86, 70, 116)]
SHELL = [(50, 36, 70), (76, 58, 104), (106, 84, 140), (136, 112, 172), (170, 150, 204), (210, 196, 236)]
CERAMIC = [(110, 116, 130), (150, 156, 170), (190, 196, 208), (216, 220, 230), (236, 238, 244), (255, 255, 255)]
PLASMA = [(120, 40, 10), (200, 80, 20), (250, 140, 30), (255, 190, 60), (255, 230, 130), (255, 252, 220)]
MAGMA = [(26, 18, 18), (44, 30, 28), (64, 44, 38), (86, 60, 48), (110, 80, 60), (140, 104, 78)]
TEAL = [(30, 52, 50), (46, 74, 70), (62, 98, 90), (82, 124, 112), (108, 150, 134), (140, 178, 160)]
LEATHER = [(46, 26, 14), (70, 40, 22), (96, 58, 32), (124, 78, 44), (152, 102, 60), (184, 132, 84)]
RUST = [(70, 34, 20), (110, 54, 28), (150, 78, 40), (186, 104, 56), (214, 136, 80), (240, 176, 120)]
TOXIC = [(30, 20, 40), (52, 32, 66), (78, 50, 92), (104, 70, 118), (130, 94, 146), (160, 124, 176)]
HOT = [(40, 22, 20), (66, 34, 28), (92, 48, 36), (120, 64, 44), (150, 84, 56), (184, 110, 74)]
COOL = [(24, 32, 50), (38, 50, 74), (54, 70, 100), (74, 94, 128), (100, 122, 158), (136, 158, 192)]
PINKM = [(96, 56, 70), (136, 82, 98), (176, 112, 128), (206, 140, 154), (230, 172, 184), (250, 210, 218)]
SANDM = [(100, 70, 40), (140, 100, 58), (180, 134, 80), (210, 164, 104), (232, 192, 134), (250, 222, 172)]
ICEM = [(70, 90, 110), (100, 124, 146), (136, 160, 182), (170, 192, 210), (204, 222, 236), (236, 246, 252)]
INK = [(16, 16, 22), (28, 28, 36), (42, 42, 52), (58, 58, 70), (78, 78, 92), (104, 104, 120)]
REDP = [(80, 16, 18), (120, 26, 28), (166, 40, 40), (204, 60, 54), (232, 96, 84), (250, 150, 136)]
BROWNP = [(60, 36, 22), (88, 54, 32), (118, 74, 44), (146, 96, 58), (176, 124, 80), (206, 158, 112)]
NAVY = [(12, 22, 40), (20, 34, 60), (30, 50, 84), (42, 68, 110), (60, 92, 140), (90, 124, 172)]
NEON = [(6, 40, 50), (10, 70, 84), (16, 110, 124), (30, 160, 170), (90, 220, 220), (190, 255, 250)]
FOXO = [(110, 46, 14), (160, 70, 20), (206, 100, 30), (236, 132, 46), (250, 170, 84), (255, 210, 140)]
SNOWW = [(120, 130, 146), (160, 170, 184), (196, 204, 216), (220, 226, 236), (238, 242, 248), (255, 255, 255)]
GOLDM = [(110, 76, 20), (156, 112, 30), (200, 152, 44), (230, 186, 70), (248, 216, 120), (255, 240, 190)]
WOOL = [(150, 150, 156), (176, 176, 182), (200, 200, 206), (220, 220, 226), (236, 236, 240), (252, 252, 255)]


def shift(pal, k):
    return [pal[max(0, min(5, i + k))] for i in range(6)]


# --------------------------------------------------------------------------
# Peinture générique d'une boîte (patron box UV Minecraft)
# --------------------------------------------------------------------------
def regions(u, v, w, h, d):
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}


def plate(img, r, pal, rng, kind="side", seams=True, rivets=True):
    x0, y0, w, h = r
    if w <= 0 or h <= 0:
        return
    p = shift(pal, 1) if kind == "top" else shift(pal, -1) if kind == "bottom" else pal
    for y in range(h):
        for x in range(w):
            px(img, x0 + x, y0 + y, p[3] if rng.random() < 0.25 else p[2])
    if kind == "side" and h >= 3:
        for x in range(w):
            px(img, x0 + x, y0, p[4])
            px(img, x0 + x, y0 + h - 1, p[1])
    if seams and w >= 10 and h >= 4:
        for y in range(1, h - 1):
            px(img, x0 + w // 2, y0 + y, p[1])
    if rivets and w >= 6 and h >= 6:
        for x, y in ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)):
            px(img, x0 + x, y0 + y, p[5])


def box(img, u, v, w, h, d, pal, seed, **kw):
    rng = random.Random(seed)
    reg = regions(u, v, w, h, d)
    for name, r in reg.items():
        plate(img, r, pal, rng, "top" if name == "top" else "bottom" if name == "bottom" else "side", **kw)
    return reg


def fill(img, x0, y0, w, h, pal, seed):
    rng = random.Random(seed)
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            px(img, x, y, pal[3] if rng.random() < 0.3 else pal[2])


def at(img, r, x, y, c):
    if 0 <= x < r[2] and 0 <= y < r[3]:
        px(img, r[0] + x, r[1] + y, c)


def frect(img, r, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            at(img, r, x, y, c)


def stripes(img, r, y0, y1, a=(250, 206, 40), b=(30, 26, 30)):
    for y in range(y0, y1 + 1):
        for x in range(r[2]):
            at(img, r, x, y, a if ((x + y) // 2) % 2 == 0 else b)


def eyes(img, r, pts, glow):
    for i, (x, y) in enumerate(pts):
        at(img, r, x, y, glow[5] if i % 2 == 0 else glow[4])


SIDES = ("right", "front", "left", "back")


# ==========================================================================
# END
# ==========================================================================
def enderman():
    t = new(64, 32)
    head = box(t, 0, 0, 8, 8, 8, VOID, 100)
    box(t, 0, 16, 8, 8, 8, VOID, 101)  # mâchoire
    body = box(t, 32, 16, 8, 12, 4, VOID, 102)
    limb = box(t, 56, 0, 2, 30, 2, VOID, 103, rivets=False)
    f = head["front"]
    frect(t, f, 0, 3, 7, 5, OUT)
    eyes(t, f, [(1, 4), (2, 4), (5, 4), (6, 4)], PURPLE)
    frect(t, f, 2, 6, 5, 6, VOID[0])
    for s in ("left", "right", "back"):
        frect(t, head[s], 0, 4, 7, 4, VOID[1])
    fb = body["front"]
    for y in range(1, 11, 3):  # circuits violets
        at(t, fb, 1, y, PURPLE[2]); at(t, fb, 6, y + 1, PURPLE[2])
    frect(t, fb, 3, 2, 4, 9, VOID[1]); at(t, fb, 3, 4, PURPLE[3]); at(t, fb, 4, 7, PURPLE[3])
    for s in SIDES:  # articulations des longs membres
        for y in (9, 19, 28):
            frect(t, limb[s], 0, y, 1, y, PURPLE[1])
    eyes_img = new(64, 32)
    eyes(eyes_img, f, [(1, 4), (2, 4), (5, 4), (6, 4)], PURPLE)
    return t, eyes_img


def endermite():
    t = new(64, 32)
    pal = SHELL
    segs = [(0, 0, 4, 3, 2), (0, 5, 6, 4, 5), (0, 14, 3, 3, 1), (0, 18, 1, 2, 1)]
    regs = [box(t, *s, pal, 110 + i, rivets=False) for i, s in enumerate(segs)]
    eyes(t, regs[0]["front"], [(0, 1), (3, 1)], CYAN)
    for s in SIDES:
        r = regs[1][s]
        frect(t, r, 0, r[3] - 1, r[2] - 1, r[3] - 1, PURPLE[3])
    return t


def shulker():
    t = new(64, 64)
    lid = box(t, 0, 0, 16, 12, 16, SHELL, 120)
    base_ = box(t, 0, 28, 16, 8, 16, SHELL, 121)
    head = box(t, 0, 52, 6, 6, 6, VOID, 122, rivets=False)
    for s in SIDES:
        frect(t, lid[s], 0, 10, 15, 10, CYAN[3])  # fente lumineuse sous le couvercle
        frect(t, lid[s], 0, 11, 15, 11, SHELL[0])
        frect(t, base_[s], 0, 0, 15, 0, CYAN[2])
        stripes(t, base_[s], 5, 6, SHELL[4], SHELL[1])
    r = lid["top"]
    frect(t, r, 5, 5, 10, 10, SHELL[1]); frect(t, r, 6, 6, 9, 9, PURPLE[3]); at(t, r, 6, 6, PURPLE[5])
    f = head["front"]
    frect(t, f, 1, 1, 4, 4, OUT); frect(t, f, 2, 2, 3, 3, CYAN[4]); at(t, f, 2, 2, CYAN[5])
    return t


# Géométrie 26.3 du dragon : (u, v, w, h, d)
DRAGON = {
    "upperlip": (176, 44, 12, 5, 16), "upperhead": (112, 30, 16, 16, 16), "hscale": (0, 0, 2, 4, 6),
    "nostril": (112, 0, 2, 2, 4), "jaw": (176, 65, 12, 4, 16), "neck": (192, 104, 10, 10, 10),
    "nscale": (48, 0, 2, 4, 6), "body": (0, 0, 24, 24, 64), "bscale": (220, 53, 2, 6, 12),
    "wbone": (112, 88, 56, 8, 8), "wtbone": (112, 136, 56, 4, 4), "fleg": (112, 104, 8, 24, 8),
    "ftip": (226, 138, 6, 24, 6), "ffoot": (144, 104, 8, 4, 16), "rleg": (0, 0, 16, 32, 16),
    "rtip": (196, 0, 12, 32, 12), "rfoot": (112, 0, 18, 6, 24),
}


def dragon(hot=False):
    """Dragon-mécha du Vide. Retourne (texture, couche lumineuse « yeux »)."""
    A = PLASMA if hot else PURPLE  # énergie principale
    B = RED if hot else CYAN  # énergie secondaire
    t = new(256, 256)
    g = new(256, 256)  # couche émissive (dragon_eyes.png)

    def glow(r, x, y, c, solid=True):
        if 0 <= x < r[2] and 0 <= y < r[3]:
            px(g, r[0] + x, r[1] + y, c)
            if solid:
                px(t, r[0] + x, r[1] + y, c)

    def gline(r, x0, y0, x1, y1, c):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                glow(r, x, y, c)

    R = {}
    for i, (name, (u, v, w, h, d)) in enumerate(DRAGON.items()):
        R[name] = box(t, u, v, w, h, d, VOID, 1400 + i, rivets=w * h > 60)

    # --- corps : plaques, conduits, réacteur ventral, tuyères ---
    body = R["body"]
    for x in (4, 19):
        gline(body["top"], x, 0, x, 63, A[3])
    for y in range(4, 64, 8):
        frect(t, body["top"], 0, y, 23, y, VOID[0])
        glow(body["top"], 4, y, A[5]); glow(body["top"], 19, y, A[5])
    for side in ("left", "right"):
        r = body[side]
        for x in range(0, 64, 8):
            frect(t, r, x, 1, x, 22, VOID[0])
        gline(r, 2, 9, 61, 9, A[3])
        for x in range(6, 60, 12):  # circuits qui descendent
            gline(r, x, 9, x, 15, A[2]); gline(r, x, 15, x + 4, 15, A[2]); glow(r, x + 4, 15, B[5])
        frect(t, r, 0, 18, 63, 23, STEEL[1])
        for x in range(1, 64, 4):
            at(t, r, x, 19, STEEL[4])
    belly = body["bottom"]
    for y in range(64):
        for x in range(24):
            if y % 6 == 0:
                at(t, belly, x, y, VOID[0])
    cx, cy = 11.5, 31.5
    for y in range(64):
        for x in range(24):
            dd = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if dd < 3.5:
                glow(belly, x, y, (255, 255, 255))
            elif dd < 6:
                glow(belly, x, y, B[5] if (x + y) % 2 else B[4])
            elif dd < 7:
                at(t, belly, x, y, VOID[0])
            elif dd < 8.6:
                glow(belly, x, y, A[5] if (x + y) % 3 == 0 else A[4])
            elif dd < 10.6:
                at(t, belly, x, y, STEEL[3] if (x * 7 + y * 3) % 5 else STEEL[5])
    for y in (8, 14, 49, 55):
        gline(belly, 5, y, 18, y, A[3])
    chest = body["front"]
    for i in range(8):
        glow(chest, 4 + i, 6 + i, A[4]); glow(chest, 19 - i, 6 + i, A[4])
    frect(t, chest, 0, 20, 23, 23, STEEL[2])
    back = body["back"]
    for x0 in (3, 16):
        for y in range(6, 18):
            for x in range(x0, x0 + 6):
                dd = ((x - x0 - 2.5) ** 2 + (y - 11.5) ** 2) ** 0.5
                if dd < 1.8:
                    glow(back, x, y, (255, 255, 255))
                elif dd < 3:
                    glow(back, x, y, B[4])
                elif dd < 3.8:
                    at(t, back, x, y, STEEL[4])

    # --- épines (corps, cou, cornes) : ailerons d'acier à pointe lumineuse ---
    for name in ("bscale", "nscale", "hscale"):
        for side, r in R[name].items():
            frect(t, r, 0, 0, r[2] - 1, r[3] - 1, STEEL[2])
            if side == "top":
                gline(r, 0, 0, r[2] - 1, r[3] - 1, A[5])
            elif side not in ("bottom",):
                gline(r, 0, 0, r[2] - 1, 0, A[5])
                gline(r, 0, 1, r[2] - 1, 1, A[3])
                frect(t, r, 0, r[3] - 1, r[2] - 1, r[3] - 1, STEEL[0])

    # --- cou et queue (même boîte) : anneaux d'énergie ---
    for side in SIDES:
        r = R["neck"][side]
        gline(r, 0, 4, 9, 4, A[3]); gline(r, 0, 5, 9, 5, A[4])
        frect(t, r, 0, 0, 9, 0, STEEL[2]); frect(t, r, 0, 9, 9, 9, STEEL[1])
    gline(R["neck"]["top"], 4, 0, 5, 9, A[2])

    # --- tête ---
    head = R["upperhead"]
    hf = head["front"]
    frect(t, hf, 0, 2, 15, 6, OUT)
    for x0 in (1, 11):
        for x in range(x0, x0 + 4):
            glow(hf, x, 4, (255, 255, 255) if x in (x0 + 1, x0 + 2) else A[5])
            glow(hf, x, 3, A[3]); glow(hf, x, 5, A[3])
    gline(hf, 7, 0, 8, 2, B[4])
    for side, front_left in (("left", True), ("right", False)):
        r = head[side]
        xs = range(0, 5) if front_left else range(11, 16)
        for x in xs:
            glow(r, x, 4, A[5]); glow(r, x, 5, A[4])
        a, b_ = (5, 15) if front_left else (0, 10)
        gline(r, a, 8, b_, 8, A[2])
        frect(t, r, 0, 12, 15, 15, STEEL[1])
    ht = head["top"]
    for i in range(8):
        glow(ht, 7 - i // 2, 15 - i, A[4]); glow(ht, 8 + i // 2, 15 - i, A[4])
    lip = R["upperlip"]
    gline(lip["top"], 2, 0, 2, 15, A[2]); gline(lip["top"], 9, 0, 9, 15, A[2])
    frect(t, lip["top"], 4, 0, 7, 15, STEEL[2])
    for side in ("left", "right", "front"):
        r = lip[side]
        for x in range(r[2]):
            at(t, r, x, 4, STEEL[5] if x % 2 == 0 else VOID[0])  # crocs d'acier
    for r in R["nostril"].values():
        frect(t, r, 0, 0, r[2] - 1, r[3] - 1, OUT)
    for x, y in ((0, 0), (1, 1)):
        glow(R["nostril"]["front"], x, y, B[5])
    jaw = R["jaw"]
    for y in range(16):  # gueule de plasma
        for x in range(12):
            glow(jaw["top"], x, y, A[5] if (x + y) % 3 == 0 else A[4] if 1 <= x <= 10 else STEEL[5])
    for side in ("left", "right", "front"):
        r = jaw[side]
        for x in range(r[2]):
            at(t, r, x, 0, STEEL[5] if x % 2 else VOID[0])
        gline(r, 0, 2, r[2] - 1, 2, A[2])

    # --- ailes : os + voiles d'énergie ---
    for name in ("wbone", "wtbone"):
        for side, r in R[name].items():
            if side in ("front", "top"):
                gline(r, 0, r[3] // 2, r[2] - 1, r[3] // 2, B[3])
                for x in range(4, r[2], 8):
                    glow(r, x, r[3] // 2, B[5])
            if side in ("front", "back"):
                for x in range(0, r[2], 14):
                    frect(t, r, x, 0, x + 1, r[3] - 1, STEEL[3])
    for vy in (88, 144):
        for y in range(vy, vy + 56):
            for x in range(0, 112):
                lx, ly = x % 56, y - vy
                edge = ly if x < 56 else 55 - ly
                if edge < 4 and (lx // 4 + edge) % 4 == 0:
                    t.putpixel((x, y), (0, 0, 0, 0))
                    continue
                c = VOID[1] if (lx + ly) % 7 else VOID[2]
                px(t, x, y, c)
                if lx % 8 == 0:
                    px(t, x, y, STEEL[2])  # nervures
                    if ly % 4 == 0:
                        px(g, x, y, B[4])
                elif (ly + (lx // 8) * 4) % 8 == 0:
                    px(t, x, y, A[2]); px(g, x, y, A[3])  # maillage lumineux
                elif edge < 6 and edge >= 4:
                    px(t, x, y, A[3]); px(g, x, y, A[4])  # bord de fuite incandescent

    # --- pattes : genoux lumineux, griffes d'acier ---
    for name in ("fleg", "rleg"):
        for side in SIDES:
            r = R[name][side]
            gline(r, 0, r[3] - 3, r[2] - 1, r[3] - 3, A[4])
            frect(t, r, 0, 0, r[2] - 1, 2, STEEL[1])
    for name in ("ftip", "rtip"):
        for side in SIDES:
            r = R[name][side]
            gline(r, 0, 2, r[2] - 1, 2, B[3])
            for y in range(6, r[3] - 2, 6):
                frect(t, r, 0, y, r[2] - 1, y, VOID[0])
    for name in ("ffoot", "rfoot"):
        r = R[name]["front"]
        for x in range(r[2]):
            at(t, r, x, r[3] - 1, STEEL[5] if x % 3 != 2 else VOID[0])
            at(t, r, x, r[3] - 2, STEEL[3] if x % 3 != 2 else VOID[0])
        gline(R[name]["top"], 0, R[name]["top"][3] // 2, R[name]["top"][2] - 1, R[name]["top"][3] // 2, A[3])
    return t, g


# ==========================================================================
# NETHER
# ==========================================================================
def blaze():
    t = new(64, 32)
    head = box(t, 0, 0, 8, 8, 8, STEEL, 200)
    f = head["front"]
    frect(t, f, 0, 2, 7, 4, OUT); frect(t, f, 1, 3, 6, 3, CYAN[2]); frect(t, f, 3, 3, 4, 3, CYAN[5])
    frect(t, f, 2, 6, 5, 6, ORANGE[3])
    for s in ("left", "right", "back"):
        stripes(t, head[s], 6, 7, ORANGE[3], DARKSTEEL[1])
    r = head["top"]
    frect(t, r, 2, 2, 5, 5, DARKSTEEL[1]); frect(t, r, 3, 3, 4, 4, ORANGE[4])
    rods = regions(0, 16, 2, 8, 2)
    for name, rr in rods.items():  # bâtons de plasma
        for y in range(rr[3]):
            for x in range(rr[2]):
                c = PLASMA[5] if (x + y) % 3 == 0 else PLASMA[3 + (y % 2)]
                if name in ("top", "bottom"):
                    c = STEEL[3]
                at(t, rr, x, y, c)
        if name not in ("top", "bottom"):
            frect(t, rr, 0, 0, 1, 0, STEEL[4]); frect(t, rr, 0, 7, 1, 7, STEEL[1])
    return t


def ghast(shooting=False):
    """Sonde-méduse (patron 64x32 dessiné en double résolution 128x64)."""
    t = new(64, 32)
    body = box(t, 0, 0, 16, 16, 16, CERAMIC, 210)
    f = body["front"]
    frect(t, f, 2, 3, 13, 12, OUT)
    frect(t, f, 2, 3, 13, 3, CERAMIC[1])
    if shooting:
        for x0 in (4, 9):
            frect(t, f, x0, 5, x0 + 2, 7, RED[3]); at(t, f, x0, 5, RED[5])
        frect(t, f, 5, 9, 10, 11, RED[2]); frect(t, f, 6, 10, 9, 10, RED[5])
    else:
        frect(t, f, 4, 6, 6, 6, CYAN[3]); frect(t, f, 9, 6, 11, 6, CYAN[3])
        frect(t, f, 6, 10, 9, 10, CYAN[2])
    for s in ("left", "right", "back"):
        r = body[s]
        stripes(t, r, 12, 13, CYAN[3], CERAMIC[1])
        frect(t, r, 6, 5, 9, 8, CERAMIC[1]); frect(t, r, 7, 6, 8, 7, CYAN[4])
    r = body["top"]
    frect(t, r, 6, 6, 9, 9, CERAMIC[1]); at(t, r, 7, 7, RED[4]); at(t, r, 8, 8, RED[2])
    # câbles (tentacules) : zone 0..8 x 0..16
    for y in range(0, 16):
        for x in range(0, 8):
            px(t, x, y, ORANGE[3] if y % 4 == 0 else STEEL[4] if x % 2 == 0 else STEEL[3])
    return t.resize((128, 64), resample=0)


def magma_cube():
    t = new(64, 64)
    for i in range(8):
        u, v = (0, 9 * i) if i < 4 else (32, 9 * (i - 4))
        reg = regions(u, v, 8, 1, 8)
        rng = random.Random(220 + i)
        top_pal = MAGMA if i == 0 else PLASMA
        for name, r in reg.items():
            if name in ("top", "bottom"):
                outer = (name == "top" and i == 0) or (name == "bottom" and i == 7)
                p = MAGMA if outer else PLASMA
                for y in range(8):
                    for x in range(8):
                        c = p[2] if rng.random() < 0.7 else p[3]
                        if outer and (x in (0, 7) or y in (0, 7)):
                            c = MAGMA[4]
                        if outer and (x + y) % 5 == 0 and 0 < x < 7 and 0 < y < 7:
                            c = PLASMA[3]
                        at(t, r, x, y, c)
            else:
                for x in range(8):
                    c = MAGMA[3] if rng.random() < 0.6 else MAGMA[2]
                    if x in (0, 7):
                        c = MAGMA[5]
                    if i in (1, 4, 6) and x % 3 == 1:
                        c = PLASMA[3]  # joints de fusion
                    at(t, r, x, 0, c)
                if name == "front" and i in (2, 3):
                    for x in (1, 2, 5, 6):
                        at(t, r, x, 0, PLASMA[5] if i == 2 else PLASMA[3])
        _ = top_pal
    core = regions(24, 40, 4, 4, 4)
    for r in core.values():
        frect(t, r, 0, 0, r[2] - 1, r[3] - 1, PLASMA[4])
        at(t, r, 1, 1, PLASMA[5])
    return t


def wither_skeleton():
    t = base.skeleton()
    # recoloration du droïde : acier -> métal noir du Néant, œil violet
    src = {c: i for i, c in enumerate(STEEL)}
    px_ = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px_[x, y]
            if a and (r, g, b) in src:
                px_[x, y] = VOID[min(5, src[(r, g, b)])] + (255,)
            elif a and (r, g, b) in [c for c in RED]:
                px_[x, y] = PURPLE[min(5, RED.index((r, g, b)) + 1)] + (255,)
    return t


def piglin_family(kind):
    t = new(64, 64)
    skin = {"piglin": TEAL, "brute": TEAL, "zombified": [(56, 66, 52), (74, 88, 68), (94, 110, 84), (116, 132, 102), (140, 156, 122), (170, 186, 150)]}[kind]
    head = box(t, 0, 0, 10, 8, 8, skin, 300, rivets=False)
    snout = box(t, 31, 1, 4, 4, 1, shift(skin, -1), 301, rivets=False)
    for (u, v) in ((2, 4), (2, 0)):
        reg = regions(u, v, 1, 2, 1)
        for r in reg.values():
            frect(t, r, 0, 0, r[2] - 1, r[3] - 1, STEEL[5] if kind != "zombified" else STEEL[3])
    ears = [box(t, 51, 6, 1, 5, 4, skin, 302, rivets=False), box(t, 39, 6, 1, 5, 4, skin, 303, rivets=False)]
    f = head["front"]
    sf = snout["front"]
    at(t, sf, 1, 2, OUT); at(t, sf, 2, 2, OUT)
    if kind == "piglin":
        frect(t, f, 0, 2, 9, 2, LEATHER[1])  # sangle de lunettes
        for x0 in (1, 6):
            frect(t, f, x0, 2, x0 + 2, 3, BRASS[3]); at(t, f, x0 + 1, 2, ORANGE[4]); at(t, f, x0 + 1, 3, ORANGE[2])
        for s in ("left", "right", "back"):
            frect(t, head[s], 0, 2, head[s][2] - 1, 2, LEATHER[1])
    elif kind == "brute":
        for s, r in head.items():
            if s != "bottom":
                frect(t, r, 0, 0, r[2] - 1, min(3, r[3] - 1), STEEL[3])
                frect(t, r, 0, 0, r[2] - 1, 0, STEEL[5])
        frect(t, f, 1, 3, 8, 3, RED[3]); at(t, f, 2, 3, RED[5]); at(t, f, 7, 3, RED[5])
    else:
        frect(t, f, 5, 0, 9, 7, STEEL[2]); frect(t, f, 5, 0, 5, 7, STEEL[0])  # demi-visage métallique
        at(t, f, 7, 3, GREEN[5]); at(t, f, 8, 3, GREEN[4]); at(t, f, 2, 3, OUT); at(t, f, 3, 3, (180, 60, 40))
        frect(t, head["left"], 0, 0, 7, 7, STEEL[2]); at(t, head["left"], 3, 3, STEEL[5])
    for e in ears:
        frect(t, e["front"], 0, 1, 0, 1, BRASS[3] if kind != "zombified" else STEEL[3])

    jacket = {"piglin": LEATHER, "brute": STEEL, "zombified": LEATHER}[kind]
    body = box(t, 16, 16, 8, 12, 4, jacket, 304)
    fb = body["front"]
    if kind == "brute":
        frect(t, fb, 1, 1, 6, 6, STEEL[4]); frect(t, fb, 3, 2, 4, 5, RED[2])
        stripes(t, fb, 8, 9)
    else:
        frect(t, fb, 3, 0, 4, 7, skin[2] if kind == "piglin" else STEEL[1])  # col ouvert / côtes
        frect(t, fb, 0, 8, 7, 8, OUT); frect(t, fb, 3, 8, 4, 8, BRASS[4])
        frect(t, fb, 0, 2, 0, 6, ORANGE[3]); frect(t, fb, 7, 2, 7, 6, ORANGE[3])
        if kind == "zombified":
            for y in (2, 4, 6):
                frect(t, fb, 3, y, 4, y, STEEL[4])
    frect(t, body["back"], 1, 1, 6, 6, BRASS[2] if kind == "piglin" else jacket[1])

    def arm(u, v, seed):
        reg = box(t, u, v, 4, 12, 4, jacket, seed)
        for s in SIDES:
            frect(t, reg[s], 0, 9, 3, 11, skin[2] if kind != "brute" else STEEL[1])
            frect(t, reg[s], 0, 8, 3, 8, ORANGE[3] if kind == "piglin" else STEEL[4])
        frect(t, reg["bottom"], 0, 0, 3, 3, skin[1])

    def leg(u, v, seed):
        reg = box(t, u, v, 4, 12, 4, INK if kind != "brute" else STEEL, seed)
        for s in SIDES:
            frect(t, reg[s], 0, 8, 3, 11, LEATHER[1] if kind != "brute" else STEEL[1])
            frect(t, reg[s], 0, 8, 3, 8, LEATHER[3] if kind != "brute" else STEEL[4])

    arm(40, 16, 305); arm(32, 48, 306); leg(0, 16, 307); leg(16, 48, 308)
    if kind == "brute":  # épaulières sur les couches externes
        for (u, v) in ((40, 32), (48, 48)):
            reg = regions(u, v, 4, 12, 4)
            for s in list(SIDES) + ["top"]:
                r = reg[s]
                frect(t, r, 0, 0, r[2] - 1, min(2, r[3] - 1), STEEL[4])
                if s != "top":
                    frect(t, r, 0, 2, r[2] - 1, 2, STEEL[1])
    return t


def hoglin(kind="hoglin"):
    t = new(128, 64)
    pal = RUST if kind == "hoglin" else TOXIC
    glow = RED if kind == "hoglin" else GREEN
    fill(t, 1, 1, 26, 26, pal, 400)  # coin libre (oreilles/cornes)
    body = box(t, 1, 1, 16, 14, 26, pal, 401)
    head = box(t, 61, 1, 14, 6, 19, pal, 402)
    box(t, 1, 1, 6, 1, 4, shift(pal, 1), 403, rivets=False)
    box(t, 1, 6, 6, 1, 4, shift(pal, 1), 404, rivets=False)
    for (u, v) in ((10, 13), (1, 13)):  # défenses / cornes
        reg = regions(u, v, 2, 11, 2)
        for name, r in reg.items():
            frect(t, r, 0, 0, r[2] - 1, r[3] - 1, STEEL[4])
            if name not in ("top", "bottom"):
                frect(t, r, 0, 0, 1, 2, glow[3] if kind == "zoglin" else ORANGE[3])
                frect(t, r, 0, 8, 1, 10, STEEL[2])
    for (u, v, w, h, d, s) in ((66, 42, 6, 14, 6, 405), (41, 42, 6, 14, 6, 406), (21, 45, 5, 11, 5, 407), (0, 45, 5, 11, 5, 408)):
        reg = box(t, u, v, w, h, d, STEEL if kind == "hoglin" else VOID, s)
        for side in SIDES:
            frect(t, reg[side], 0, h - 3, reg[side][2] - 1, h - 1, pal[1])
            frect(t, reg[side], 0, h // 2, reg[side][2] - 1, h // 2, glow[2] if kind == "zoglin" else ORANGE[2])
    # dos : bande de danger + plaques
    r = body["back"]
    stripes(t, body["top"], 10, 15)
    for s in ("left", "right"):
        rr = body[s]
        frect(t, rr, 0, 4, rr[2] - 1, 4, pal[1])
        for x in range(2, rr[2] - 1, 6):
            frect(t, rr, x, 6, x + 2, 8, STEEL[3]); at(t, rr, x, 6, STEEL[5])
    frect(t, r, 5, 4, 10, 9, OUT); frect(t, r, 6, 5, 9, 8, glow[2]); frect(t, r, 7, 6, 8, 7, glow[4])
    # tête : yeux sur le dessus (tête inclinée vers l'avant), groin = grille
    ht = head["top"]
    eyes(t, ht, [(1, 3), (2, 3), (11, 3), (12, 3)], glow)
    frect(t, ht, 4, 10, 9, 18, pal[1])
    for y in range(11, 18, 2):
        frect(t, ht, 5, y, 8, y, STEEL[3])
    hf = head["front"]
    frect(t, hf, 2, 1, 11, 4, OUT); at(t, hf, 4, 2, glow[3]); at(t, hf, 9, 2, glow[3])
    # crinière : pointes métalliques (plan découpé)
    for (x0, y0) in ((90, 52), (109, 52)):
        for x in range(19):
            hgt = 10 - (x % 3) * 3
            for y in range(10):
                if y >= 10 - hgt:
                    px(t, x0 + x, y0 + y, STEEL[4] if y == 10 - hgt else STEEL[2] if x % 3 else glow[3])
    return t


def strider(cold=False):
    t = new(64, 128)
    pal = COOL if cold else HOT
    glow = CYAN if cold else PLASMA
    body = box(t, 0, 0, 16, 14, 16, pal, 500)
    for (u, v) in ((0, 32), (0, 55)):
        reg = box(t, u, v, 4, 16, 4, STEEL, 501 + v)
        for s in SIDES:
            for y in (5, 10):
                frect(t, reg[s], 0, y, 3, y, glow[3])
            frect(t, reg[s], 0, 14, 3, 15, pal[1])
    f = body["front"]
    for x0 in (2, 10):  # gros yeux-projecteurs
        frect(t, f, x0, 3, x0 + 3, 6, OUT); frect(t, f, x0 + 1, 4, x0 + 2, 5, glow[4]); at(t, f, x0 + 1, 4, glow[5])
    frect(t, f, 4, 9, 11, 11, OUT)
    for x in range(5, 11, 2):
        frect(t, f, x, 9, x, 11, glow[2])
    for s in ("left", "right", "back"):
        r = body[s]
        for x in range(2, 14, 4):
            frect(t, r, x, 4, x + 1, 9, OUT); frect(t, r, x, 5, x + 1, 8, glow[2])
    stripes(t, body["top"], 6, 9, glow[3], pal[1])
    # « poils » : câbles (plans transparents découpés)
    for v in (33, 49, 65):
        for x0 in (32, 44):
            for x in range(12):
                for y in range(16):
                    if x % 3 == 1 and y < 16 - (x % 4) * 2:
                        px(t, x0 + x, v + y, glow[3] if y % 5 == 0 else STEEL[4])
    return t


# ==========================================================================
# MOBS PASSIFS
# ==========================================================================
def pig(variant="temperate"):
    pal = {"temperate": PINKM, "warm": SANDM, "cold": ICEM}[variant]
    t = new(64, 64)
    head = box(t, 0, 0, 8, 8, 8, pal, 600)
    snout = box(t, 16, 16, 4, 3, 1, STEEL, 601, rivets=False)
    body = box(t, 28, 8, 10, 16, 8, pal, 602)
    legs = box(t, 0, 16, 4, 6, 4, STEEL, 603, rivets=False)
    f = head["front"]
    for x0 in (1, 5):
        frect(t, f, x0, 2, x0 + 1, 3, OUT); at(t, f, x0, 2, CYAN[5]); at(t, f, x0 + 1, 3, CYAN[3])
    at(t, snout["front"], 1, 1, OUT); at(t, snout["front"], 2, 1, OUT)
    stripes(t, body["back"], 6, 9, ORANGE[3], pal[1])  # dos (face « back » une fois le corps couché)
    for s in ("left", "right"):
        r = body[s]
        frect(t, r, 1, 7, r[2] - 2, 8, pal[1]); at(t, r, 2, 3, STEEL[5]); at(t, r, r[2] - 3, 3, STEEL[5])
    for s in SIDES:
        frect(t, legs[s], 0, 4, 3, 5, ORANGE[2] if variant != "cold" else CYAN[2])
    if variant == "cold":  # matelassage isolant (couche externe)
        reg = regions(28, 32, 10, 16, 8)
        for name, r in reg.items():
            for y in range(r[3]):
                for x in range(r[2]):
                    at(t, r, x, y, ICEM[4] if (x // 2 + y // 2) % 2 else ICEM[3])
            frect(t, r, 0, 0, r[2] - 1, 0, ICEM[5])
        fill(t, 16, 24, 12, 8, ICEM, 604)
    return t


def cow(variant="temperate"):
    pal, spot = {"temperate": (CERAMIC, INK), "warm": (SANDM, RUST), "cold": (ICEM, COOL),
                 "mooshroom_red": (REDP, CERAMIC), "mooshroom_brown": (BROWNP, SANDM)}[variant]
    t = new(64, 64)
    head = box(t, 0, 0, 8, 8, 6, pal, 700)
    mx = 9 if variant == "cold" else 1
    muzzle = box(t, mx, 33, 6, 3, 1, STEEL, 701, rivets=False)
    body = box(t, 18, 4, 12, 18, 10, pal, 702)
    udder = box(t, 52, 0, 4, 6, 1, BRASS, 703, rivets=False)
    legs = box(t, 0, 16, 4, 12, 4, pal, 704, rivets=False)
    f = head["front"]
    for x0 in (1, 5):
        frect(t, f, x0, 3, x0 + 1, 4, OUT); at(t, f, x0, 3, CYAN[5]); at(t, f, x0 + 1, 4, CYAN[3])
    frect(t, f, 0, 0, 7, 0, spot[2])
    for x in range(1, 5, 2):
        at(t, muzzle["front"], x, 1, OUT)
    # taches = panneaux de blindage
    rng = random.Random(705)
    for s in ("left", "right", "back", "front", "top"):
        r = body[s]
        for _ in range(3 if r[2] * r[3] > 100 else 1):
            w, h = rng.randint(3, 5), rng.randint(3, 5)
            x0, y0 = rng.randrange(0, max(1, r[2] - w)), rng.randrange(0, max(1, r[3] - h))
            frect(t, r, x0, y0, x0 + w - 1, y0 + h - 1, spot[2])
            frect(t, r, x0, y0, x0 + w - 1, y0, spot[4])
    for s in SIDES:
        frect(t, legs[s], 0, 9, 3, 11, STEEL[1])
        frect(t, legs[s], 0, 9, 3, 9, STEEL[4])
    at(t, udder["front"], 1, 5, CYAN[4]); at(t, udder["front"], 2, 5, CYAN[4])
    if variant == "temperate" or variant.startswith("mooshroom"):
        box(t, 22, 0, 1, 3, 1, STEEL, 706, rivets=False)
    elif variant == "warm":
        box(t, 27, 0, 4, 2, 2, BRASS, 707, rivets=False)
        box(t, 39, 0, 2, 2, 2, BRASS, 708, rivets=False)
    else:  # froide : cornes + couche isolante
        box(t, 0, 40, 2, 6, 2, STEEL, 709, rivets=False)
        box(t, 0, 32, 2, 6, 2, STEEL, 710, rivets=False)
        reg = regions(20, 32, 12, 18, 10)
        for name, r in reg.items():
            for y in range(r[3]):
                for x in range(r[2]):
                    at(t, r, x, y, ICEM[4] if (x // 2 + y // 2) % 2 else ICEM[3])
    fill(t, 0, 32, 16, 5, pal, 711) if variant != "cold" else None
    return t


def chicken(variant="temperate"):
    pal = {"temperate": CERAMIC, "warm": SANDM, "cold": ICEM}[variant]
    t = new(64, 32)
    head = box(t, 0, 0, 4, 6, 3, pal, 800, rivets=False)
    box(t, 14, 0, 4, 2, 2, BRASS, 801, rivets=False)
    wattle = box(t, 14, 4, 2, 2, 2, RED, 802, rivets=False)
    body = box(t, 0, 9, 6, 8, 6, pal, 803)
    legs = box(t, 26, 0, 3, 5, 3, STEEL, 804, rivets=False)
    wings = box(t, 24, 13, 1, 4, 6, shift(pal, -1), 805, rivets=False)
    f = head["front"]
    at(t, f, 0, 2, CYAN[5]); at(t, f, 3, 2, CYAN[5])
    for r in wattle.values():
        at(t, r, 0, 0, RED[5])
    for s in ("left", "right"):
        r = wings[s]
        for x in range(0, r[2], 2):
            frect(t, r, x, 0, x, r[3] - 1, ORANGE[3])
    stripes(t, body["back"], 2, 3, ORANGE[3], pal[1])
    for s in SIDES:
        frect(t, legs[s], 0, 4, 2, 4, ORANGE[3])
    if variant == "cold":
        box(t, 44, 0, 6, 3, 4, ICEM, 806, rivets=False)
        box(t, 38, 9, 0, 3, 5, ICEM, 807, rivets=False)
        fill(t, 50, 25, 14, 7, ICEM, 808)
    return t


def sheep():
    t = new(64, 32)
    head = box(t, 0, 0, 6, 6, 8, INK, 900, rivets=False)
    box(t, 28, 8, 8, 16, 6, INK, 901)
    legs = box(t, 0, 16, 4, 12, 4, STEEL, 902, rivets=False)
    f = head["front"]
    for x0 in (1, 4):
        at(t, f, x0, 2, CYAN[5])
    frect(t, f, 2, 4, 3, 4, STEEL[3])
    for s in SIDES:  # ressorts dans les pattes
        for y in range(2, 10, 2):
            frect(t, legs[s], 0, y, 3, y, STEEL[1])
    return t


def wool(undercoat=False):
    """Fibre isolante (gris clair, teintée par la couleur du mouton)."""
    t = new(64, 32)
    pal = shift(WOOL, -1) if undercoat else WOOL
    for i, (u, v, w, h, d) in enumerate(((0, 0, 6, 6, 6), (28, 8, 8, 16, 6), (0, 16, 4, 6, 4))):
        reg = regions(u, v, w, h, d)
        for r in reg.values():
            for y in range(r[3]):
                for x in range(r[2]):
                    c = pal[4] if (x + 2 * y) % 4 == 0 else pal[3] if (x + y) % 2 else pal[2]
                    at(t, r, x, y, c)
    if undercoat:
        for (x0, y0, w, h) in ((0, 12, 9, 2), (13, 8, 15, 6), (18, 0, 2, 6)):
            fill(t, x0, y0, w, h, pal, 950)
    return t


RABBITS = {"brown": BROWNP, "white": SNOWW, "black": INK, "gold": GOLDM, "salt": STEEL,
           "toast": LEATHER, "white_splotched": SNOWW, "caerbannog": SNOWW}


def rabbit(variant):
    pal = RABBITS[variant]
    t = new(64, 64)
    body = box(t, 0, 0, 8, 6, 10, pal, 1000)
    box(t, 20, 16, 4, 4, 4, STEEL, 1001, rivets=False)
    head = box(t, 0, 16, 5, 5, 5, pal, 1002, rivets=False)
    ears = [box(t, 32, 0, 2, 5, 1, STEEL, 1003, rivets=False), box(t, 26, 0, 2, 5, 1, STEEL, 1004, rivets=False)]
    for (u, v) in ((36, 18), (44, 18)):
        box(t, u, v, 2, 4, 2, STEEL, 1005 + u, rivets=False)
    for (u, v) in ((20, 24), (36, 24)):
        box(t, u, v, 2, 1, 6, STEEL, 1007 + u, rivets=False)
    glow = RED if variant == "caerbannog" else CYAN
    f = head["front"]
    at(t, f, 1, 1, glow[5]); at(t, f, 3, 1, glow[5]); at(t, f, 2, 3, OUT)
    for e in ears:  # antennes
        for r in e.values():
            at(t, r, 0, 0, ORANGE[4] if variant != "caerbannog" else RED[4])
    if variant == "white_splotched":
        for s in ("left", "right", "top"):
            frect(t, body[s], 1, 1, 3, 3, INK[2])
    if variant == "toast":
        frect(t, body["top"], 2, 2, 5, 7, ORANGE[3])
    return t


def squid(glow=False):
    pal = NEON if glow else NAVY
    t = new(64, 32)
    body = box(t, 0, 0, 12, 16, 12, pal, 1100)
    tent = box(t, 48, 0, 2, 18, 2, shift(pal, 1), 1101, rivets=False)
    hi = CYAN if not glow else [(255, 255, 255)] * 6
    for s in SIDES:  # hublots
        r = body[s]
        frect(t, r, 4, 3, 7, 6, OUT); frect(t, r, 5, 4, 6, 5, hi[4] if not glow else NEON[5])
        stripes(t, r, 12, 13, ORANGE[3] if not glow else NEON[5], pal[1])
    f = body["front"]
    frect(t, f, 1, 8, 3, 9, OUT); frect(t, f, 8, 8, 10, 9, OUT)
    at(t, f, 2, 8, (255, 220, 120) if not glow else NEON[5]); at(t, f, 9, 8, (255, 220, 120) if not glow else NEON[5])
    for s in SIDES:
        for y in range(0, 18, 3):
            frect(t, tent[s], 0, y, 1, y, ORANGE[3] if not glow else NEON[5])
    return t


def bat():
    """Mini-drone de reconnaissance : pas d'ailes, caméra rouge, propulseurs, antennes."""
    t = new(32, 32)
    body = box(t, 0, 0, 3, 5, 2, STEEL, 1200, rivets=False)
    head = box(t, 0, 7, 4, 3, 2, DARKSTEEL, 1201, rivets=False)
    for s_ in SIDES:  # fuselage : bande cyan + batterie
        r = body[s_]
        frect(t, r, 0, 1, r[2] - 1, 1, CYAN[3])
        frect(t, r, 0, 4, r[2] - 1, 4, STEEL[1])
    frect(t, body["front"], 1, 2, 1, 3, GREEN[4])
    f = head["front"]  # objectif de caméra
    frect(t, f, 0, 0, 3, 2, OUT)
    frect(t, f, 1, 0, 2, 1, RED[3]); at(t, f, 1, 0, (255, 255, 255)); at(t, f, 2, 1, RED[1])
    at(t, f, 3, 2, ORANGE[4])
    for s_ in ("left", "right", "back"):
        frect(t, head[s_], 0, 1, head[s_][2] - 1, 1, CYAN[2])
    for (u, v, w, h) in ((1, 15, 3, 5), (8, 15, 3, 5)):  # oreilles -> antennes
        for side in (0, 1):
            x = u + side * w + 1
            for y in range(1, h):
                px(t, x, v + y, STEEL[4])
            px(t, x, v, RED[5])
    for (u, v) in ((12, 0), (12, 7)):  # base des ailes -> petits propulseurs
        for side in (0, 1):
            x0 = u + side * 2
            rect(t, x0, v + 2, x0 + 1, v + 3, STEEL[3])
            px(t, x0, v + 2, STEEL[5])
            rect(t, x0, v + 4, x0 + 1, v + 4, CYAN[4])
    for side in (0, 1):  # pattes -> patin d'atterrissage
        x0 = 16 + side * 3
        rect(t, x0, 17, x0 + 2, 17, STEEL[4])
        px(t, x0 + 1, 16, STEEL[2])
    # bouts d'ailes (16,0) et (16,8) : laissés transparents => plus d'ailes
    return t


def fox(snow=False, sleep=False):
    pal = SNOWW if snow else FOXO
    t = new(48, 32)
    head = box(t, 1, 5, 8, 6, 6, pal, 1300, rivets=False)
    box(t, 8, 1, 2, 2, 1, STEEL, 1301, rivets=False)
    box(t, 15, 1, 2, 2, 1, STEEL, 1302, rivets=False)
    nose = box(t, 6, 18, 4, 2, 3, CERAMIC if not snow else STEEL, 1303, rivets=False)
    body = box(t, 24, 15, 6, 11, 6, pal, 1304)
    for (u, v) in ((4, 24), (13, 24)):
        box(t, u, v, 2, 6, 2, INK, 1305 + u, rivets=False)
    tail = box(t, 30, 0, 4, 9, 5, pal, 1307, rivets=False)
    f = head["front"]
    if sleep:
        frect(t, f, 1, 2, 2, 2, OUT); frect(t, f, 5, 2, 6, 2, OUT)
    else:
        for x0 in (1, 5):
            at(t, f, x0, 2, OUT); at(t, f, x0 + 1, 2, (120, 255, 140)); at(t, f, x0 + 1, 3, OUT)
    at(t, nose["front"], 1, 0, OUT); at(t, nose["front"], 2, 0, OUT)
    stripes(t, body["back"], 3, 4, CERAMIC[4], pal[1])
    for s in SIDES:  # queue : segments + pointe lumineuse
        r = tail[s]
        for y in range(0, 9, 2):
            frect(t, r, 0, y, r[2] - 1, y, pal[1])
        frect(t, r, 0, 7, r[2] - 1, 8, CERAMIC[5] if not snow else CYAN[4])
    return t


# --------------------------------------------------------------------------
def textures():
    tex = {}
    em, em_eyes = enderman()
    tex["enderman/enderman.png"] = em
    tex["enderman/enderman_eyes.png"] = em_eyes
    tex["endermite/endermite.png"] = endermite()
    tex["shulker/shulker.png"] = shulker()
    tex["enderdragon/dragon.png"], tex["enderdragon/dragon_eyes.png"] = dragon()
    hot, hot_glow = dragon(hot=True)  # animation de mort : surchauffe
    hot.alpha_composite(hot_glow)
    tex["enderdragon/dragon_exploding.png"] = hot
    tex["blaze/blaze.png"] = blaze()
    tex["ghast/ghast.png"] = ghast()
    tex["ghast/ghast_shooting.png"] = ghast(shooting=True)
    tex["slime/magmacube.png"] = magma_cube()
    tex["skeleton/wither_skeleton.png"] = wither_skeleton()
    tex["piglin/piglin.png"] = piglin_family("piglin")
    tex["piglin/piglin_brute.png"] = piglin_family("brute")
    tex["piglin/zombified_piglin.png"] = piglin_family("zombified")
    tex["hoglin/hoglin.png"] = hoglin("hoglin")
    tex["hoglin/zoglin.png"] = hoglin("zoglin")
    tex["strider/strider.png"] = strider()
    tex["strider/strider_cold.png"] = strider(cold=True)
    for v in ("temperate", "warm", "cold"):
        tex[f"pig/pig_{v}.png"] = pig(v)
        tex[f"cow/cow_{v}.png"] = cow(v)
        tex[f"chicken/chicken_{v}.png"] = chicken(v)
    tex["cow/mooshroom_red.png"] = cow("mooshroom_red")
    tex["cow/mooshroom_brown.png"] = cow("mooshroom_brown")
    tex["sheep/sheep.png"] = sheep()
    tex["sheep/sheep_wool.png"] = wool()
    tex["sheep/sheep_wool_undercoat.png"] = wool(undercoat=True)
    for v in RABBITS:
        tex[f"rabbit/rabbit_{v}.png"] = rabbit(v)
    tex["squid/squid.png"] = squid()
    tex["squid/glow_squid.png"] = squid(glow=True)
    tex["bat/bat.png"] = bat()
    for snow in (False, True):
        for sleep in (False, True):
            name = "fox" + ("_snow" if snow else "") + ("_sleep" if sleep else "")
            tex[f"fox/{name}.png"] = fox(snow, sleep)
    # anciens chemins (versions 1.20.5 - 1.21.x), même format d'image
    tex["blaze.png"] = tex["blaze/blaze.png"]
    tex["endermite.png"] = tex["endermite/endermite.png"]
    return tex


NAMES_FR = {
    "entity.minecraft.enderman": "Spectre du Vide",
    "entity.minecraft.endermite": "Nanobot du Vide",
    "entity.minecraft.shulker": "Tourelle-coffre",
    "entity.minecraft.ender_dragon": "Dragon cuirassé du Vide",
    "entity.minecraft.blaze": "Drone à plasma",
    "entity.minecraft.ghast": "Sonde-méduse",
    "entity.minecraft.magma_cube": "Cube de fusion",
    "entity.minecraft.wither_skeleton": "Droïde du Néant",
    "entity.minecraft.piglin": "Contrebandier",
    "entity.minecraft.piglin_brute": "Garde blindé",
    "entity.minecraft.zombified_piglin": "Contrebandier cyborg",
    "entity.minecraft.hoglin": "Sanglier-tank",
    "entity.minecraft.zoglin": "Sanglier-tank corrompu",
    "entity.minecraft.strider": "Marcheur thermique",
    "entity.minecraft.pig": "Porcelet mécanique",
    "entity.minecraft.cow": "Vache-citerne",
    "entity.minecraft.mooshroom": "Vache bio-réacteur",
    "entity.minecraft.chicken": "Poule-drone",
    "entity.minecraft.sheep": "Mouton à ressorts",
    "entity.minecraft.rabbit": "Lapin sauteur",
    "entity.minecraft.squid": "Calamar-sonde",
    "entity.minecraft.glow_squid": "Calamar néon",
    "entity.minecraft.bat": "Chauve-souris drone",
    "entity.minecraft.fox": "Renard éclaireur",
}
NAMES_EN = {
    "entity.minecraft.enderman": "Void Wraith",
    "entity.minecraft.endermite": "Void Nanobot",
    "entity.minecraft.shulker": "Vault Turret",
    "entity.minecraft.ender_dragon": "Armored Void Dragon",
    "entity.minecraft.blaze": "Plasma Drone",
    "entity.minecraft.ghast": "Jellyfish Probe",
    "entity.minecraft.magma_cube": "Fusion Cube",
    "entity.minecraft.wither_skeleton": "Void Droid",
    "entity.minecraft.piglin": "Smuggler",
    "entity.minecraft.piglin_brute": "Armored Guard",
    "entity.minecraft.zombified_piglin": "Cyborg Smuggler",
    "entity.minecraft.hoglin": "Tank Boar",
    "entity.minecraft.zoglin": "Corrupted Tank Boar",
    "entity.minecraft.strider": "Thermal Walker",
    "entity.minecraft.pig": "Robo Pig",
    "entity.minecraft.cow": "Tank Cow",
    "entity.minecraft.mooshroom": "Bioreactor Cow",
    "entity.minecraft.chicken": "Drone Hen",
    "entity.minecraft.sheep": "Spring Sheep",
    "entity.minecraft.rabbit": "Hopper Bot",
    "entity.minecraft.squid": "Probe Squid",
    "entity.minecraft.glow_squid": "Neon Squid",
    "entity.minecraft.bat": "Bat Drone",
    "entity.minecraft.fox": "Scout Fox",
}
