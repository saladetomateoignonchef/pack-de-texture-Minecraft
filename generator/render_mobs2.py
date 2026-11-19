#!/usr/bin/env python3
"""Aperçus 3D des mobs de l'End, du Nether et des mobs passifs (géométrie Minecraft 26.x).

À lancer après generate.py :  python3 generator/render_mobs2.py
Produit : screenshots/mobs_end_nether.png, screenshots/mobs_passifs.png
"""
import math
import os

from PIL import Image, ImageDraw

import render_mobs as rm
import render_screens as rs
from render_mobs import Part

P2 = math.pi / 2


def ent(rel):
    return Image.open(os.path.join(rm.ENT, rel)).convert("RGBA")


def with_overlay(rel, overlay):
    t = ent(rel)
    t.alpha_composite(ent(overlay))
    return t


# ----------------------------------------------------------------- END ----
def enderman():
    return [Part((0, 0), (-4, -8, -4, 8, 8, 8), (0, -13, 0)), Part((32, 16), (-4, 0, -2, 8, 12, 4), (0, -14, 0)),
            Part((56, 0), (-1, -2, -1, 2, 30, 2), (-5, -12, 0), (-0.1, 0, 0)),
            Part((56, 0), (-1, -2, -1, 2, 30, 2), (5, -12, 0), (0.1, 0, 0), mirror=True),
            Part((56, 0), (-1, 0, -1, 2, 30, 2), (-2, -5, 0)), Part((56, 0), (-1, 0, -1, 2, 30, 2), (2, -5, 0), mirror=True)]


def endermite():
    sizes = [((0, 0), (4, 3, 2)), ((0, 5), (6, 4, 5)), ((0, 14), (3, 3, 1)), ((0, 18), (1, 2, 1))]
    parts, z = [], -3.5
    for uv, (w, h, d) in sizes:
        parts.append(Part(uv, (-w / 2, 0, -d / 2, w, h, d), (0, 24 - h, z + d / 2)))
        z += d
    return parts


def shulker():
    return [Part((0, 28), (-8, -8, -8, 16, 8, 16), (0, 24, 0)),
            Part((0, 0), (-8, -16, -8, 16, 12, 16), (0, 18, 0)),
            Part((0, 52), (-3, 0, -3, 6, 6, 6), (0, 10, 0))]


# --------------------------------------------------------------- NETHER ---
def blaze():
    parts = [Part((0, 0), (-4, -4, -4, 8, 8, 8), (0, -2, 0))]
    for ring, (r, y, n) in enumerate(((9, 0, 4), (7, 6, 4), (5, 12, 4))):
        for i in range(n):
            a = i * P2 + ring * 0.6
            parts.append(Part((0, 16), (0, 0, 0, 2, 8, 2), (math.cos(a) * r - 1, y, math.sin(a) * r - 1)))
    return parts


def ghast():
    parts = [Part((0, 0), (-8, -8, -8, 16, 16, 16), (0, 0, 0), ts=2)]
    lengths = [10, 13, 9, 12, 11, 14, 8, 12, 10]
    for i in range(9):
        f = ((i % 3) - (i // 3 % 2) * 0.5 + 0.25) / 2 * 2 - 1
        f1 = (i // 3) / 2 * 2 - 1
        parts.append(Part((0, 0), (-1, 0, -1, 2, lengths[i], 2), (f * 5, 7, f1 * 5), ts=2))
    return parts


def magma():
    parts = []
    for i in range(8):
        uv = (0, 9 * i) if i < 4 else (32, 9 * (i - 4))
        parts.append(Part(uv, (-4, 16 + i, -4, 8, 1, 8)))
    return parts


def skeleton():
    return rm.skeleton_model()


def piglin(arms=(0.0, 0.0)):
    head = Part((0, 0), (-5, -8, -4, 10, 8, 8))
    parts = [head, Part((31, 1), (-2, -4, -5, 4, 4, 1)), Part((2, 4), (2, -2, -5, 1, 2, 1)), Part((2, 0), (-3, -2, -5, 1, 2, 1)),
             Part((51, 6), (0, 0, -2, 1, 5, 4), (4.5, -6, 0), (0, 0, -math.pi / 6), parent=head),
             Part((39, 6), (-1, 0, -2, 1, 5, 4), (-4.5, -6, 0), (0, 0, math.pi / 6), parent=head),
             Part((16, 16), (-4, 0, -2, 8, 12, 4)), Part((16, 32), (-4, 0, -2, 8, 12, 4), inflate=0.25),
             Part((40, 16), (-3, -2, -2, 4, 12, 4), (-5, 2, 0), (arms[0], 0, 0)),
             Part((40, 32), (-3, -2, -2, 4, 12, 4), (-5, 2, 0), (arms[0], 0, 0), inflate=0.25),
             Part((32, 48), (-1, -2, -2, 4, 12, 4), (5, 2, 0), (arms[1], 0, 0)),
             Part((48, 48), (-1, -2, -2, 4, 12, 4), (5, 2, 0), (arms[1], 0, 0), inflate=0.25),
             Part((0, 16), (-2, 0, -2, 4, 12, 4), (-1.9, 12, 0)), Part((0, 32), (-2, 0, -2, 4, 12, 4), (-1.9, 12, 0), inflate=0.25),
             Part((16, 48), (-2, 0, -2, 4, 12, 4), (1.9, 12, 0)), Part((0, 48), (-2, 0, -2, 4, 12, 4), (1.9, 12, 0), inflate=0.25)]
    return parts


def hoglin():
    body = Part((1, 1), (-8, -7, -13, 16, 14, 26), (0, 7, 0))
    head = Part((61, 1), (-7, -3, -19, 14, 6, 19), (0, 2, -12), (0.8727, 0, 0))
    return [body, Part((90, 33), (0, 0, -9, 0, 10, 19), (0, -14, -5), parent=body), head,
            Part((1, 1), (-6, -1, -2, 6, 1, 4), (-6, -2, -3), (0, 0, -0.698), parent=head),
            Part((1, 6), (0, -1, -2, 6, 1, 4), (6, -2, -3), (0, 0, 0.698), parent=head),
            Part((10, 13), (-1, -11, -1, 2, 11, 2), (-7, 2, -12), parent=head),
            Part((1, 13), (-1, -11, -1, 2, 11, 2), (7, 2, -12), parent=head),
            Part((66, 42), (-3, 0, -3, 6, 14, 6), (-4, 10, -8.5)), Part((41, 42), (-3, 0, -3, 6, 14, 6), (4, 10, -8.5)),
            Part((21, 45), (-2.5, 0, -2.5, 5, 11, 5), (-5, 13, 10)), Part((0, 45), (-2.5, 0, -2.5, 5, 11, 5), (5, 13, 10))]


def strider():
    body = Part((0, 0), (-8, -6, -8, 16, 14, 16), (0, 1, 0))
    parts = [body, Part((0, 32), (-2, 0, -2, 4, 16, 4), (-4, 8, 0)), Part((0, 55), (-2, 0, -2, 4, 16, 4), (4, 8, 0))]
    for v, y, a in ((65, 4, 1.22), (49, -1, 1.13), (33, -5, 0.87)):
        parts.append(Part((16, v), (-12, 0, 0, 12, 0, 16), (-8, y, -8), (0, 0, -a), parent=body))
        parts.append(Part((16, v), (0, 0, 0, 12, 0, 16), (8, y, -8), (0, 0, a), parent=body))
    return parts


# -------------------------------------------------------------- PASSIFS ---
def pig(cold=False):
    parts = [Part((0, 0), (-4, -4, -8, 8, 8, 8), (0, 12, -6)), Part((16, 16), (-2, 0, -9, 4, 3, 1), (0, 12, -6)),
             Part((28, 8), (-5, -10, -7, 10, 16, 8), (0, 11, 2), (P2, 0, 0))]
    if cold:
        parts.append(Part((28, 32), (-5, -10, -7, 10, 16, 8), (0, 11, 2), (P2, 0, 0), inflate=0.5))
    for x, z in ((-3, 7), (3, 7), (-3, -5), (3, -5)):
        parts.append(Part((0, 16), (-2, 0, -2, 4, 6, 4), (x, 18, z)))
    return parts


def cow(variant="temperate"):
    head = Part((0, 0), (-4, -4, -6, 8, 8, 6), (0, 4, -8))
    parts = [head, Part((9 if variant == "cold" else 1, 33), (-3, 1, -7, 6, 3, 1), (0, 4, -8)),
             Part((18, 4), (-6, -10, -7, 12, 18, 10), (0, 5, 2), (P2, 0, 0)),
             Part((52, 0), (-2, 2, -8, 4, 6, 1), (0, 5, 2), (P2, 0, 0))]
    if variant == "warm":
        parts += [Part((27, 0), (-8, -3, -5, 4, 2, 2), (0, 4, -8)), Part((39, 0), (-8, -5, -5, 2, 2, 2), (0, 4, -8)),
                  Part((27, 0), (4, -3, -5, 4, 2, 2), (0, 4, -8)), Part((39, 0), (6, -5, -5, 2, 2, 2), (0, 4, -8))]
    elif variant == "cold":
        parts += [Part((20, 32), (-6, -10, -7, 12, 18, 10), (0, 5, 2), (P2, 0, 0), inflate=0.5),
                  Part((0, 40), (-1.5, -4.5, -0.5, 2, 6, 2), (-4.5, -2.5, -3.5), (P2, 0, 0), parent=head),
                  Part((0, 32), (-1.5, -3, -0.5, 2, 6, 2), (5.5, -2.5, -5), (P2, 0, 0), parent=head)]
    else:
        parts += [Part((22, 0), (-5, -5, -5, 1, 3, 1), (0, 4, -8)), Part((22, 0), (4, -5, -5, 1, 3, 1), (0, 4, -8))]
    for x, z in ((-4, 7), (4, 7), (-4, -5), (4, -5)):
        parts.append(Part((0, 16), (-2, 0, -2, 4, 12, 4), (x, 12, z)))
    return parts


def chicken(cold=False):
    parts = [Part((0, 0), (-2, -6, -2, 4, 6, 3), (0, 15, -4)), Part((14, 0), (-2, -4, -4, 4, 2, 2), (0, 15, -4)),
             Part((14, 4), (-1, -2, -3, 2, 2, 2), (0, 15, -4)), Part((0, 9), (-3, -4, -3, 6, 8, 6), (0, 16, 0), (P2, 0, 0)),
             Part((26, 0), (-1, 0, -3, 3, 5, 3), (-2, 19, 1)), Part((26, 0), (-1, 0, -3, 3, 5, 3), (1, 19, 1)),
             Part((24, 13), (0, 0, -3, 1, 4, 6), (-4, 13, 0)), Part((24, 13), (-1, 0, -3, 1, 4, 6), (4, 13, 0))]
    if cold:
        parts.append(Part((44, 0), (-3, -7, -2.015, 6, 3, 4), (0, 15, -4)))
    return parts


def sheep(wool=False):
    if wool:
        parts = [Part((0, 0), (-3, -4, -4, 6, 6, 6), (0, 6, -8), inflate=0.6),
                 Part((28, 8), (-4, -10, -7, 8, 16, 6), (0, 5, 2), (P2, 0, 0), inflate=1.75)]
        legs = [((0, 16), (-2, 0, -2, 4, 6, 4), 0.5)]
    else:
        parts = [Part((0, 0), (-3, -4, -6, 6, 6, 8), (0, 6, -8)), Part((28, 8), (-4, -10, -7, 8, 16, 6), (0, 5, 2), (P2, 0, 0))]
        legs = [((0, 16), (-2, 0, -2, 4, 12, 4), 0)]
    for uv, b, inf in legs:
        for x, z in ((-3, 7), (3, 7), (-3, -5), (3, -5)):
            parts.append(Part(uv, b, (x, 12, z), inflate=inf))
    return parts


def rabbit():
    body = Part((0, 0), (-4, -6, -9, 8, 6, 10), (0, 23, 4), (-0.393, 0, 0))
    head = Part((0, 16), (-2.5, -3, -4, 5, 5, 5), (0, -5.293, -8.121), (0.393, 0, 0), parent=body)
    front = Part((0, 0), (0, 0, 0, 0, 0, 0), (0, -1.535, -6.311), parent=body)
    back = Part((0, 0), (0, 0, 0, 0, 0, 0), (0, 23, 4))
    return [body, head, Part((20, 16), (-2, -3, -1, 4, 4, 4), (0, -5, 0), parent=body),
            Part((32, 0), (-1, -4.293, -0.121, 2, 5, 1), (1.5, -3.707, -0.879), parent=head),
            Part((26, 0), (-1, -4.293, -0.121, 2, 5, 1), (-1.5, -3.707, -0.879), parent=head),
            Part((36, 18), (-0.9, -1, -0.9, 2, 4, 2), (-2, 1.924, 0.383), (0.393, 0, 0), parent=front),
            Part((44, 18), (-1, -1, -1, 2, 4, 2), (2, 1.924, 0.483), (0.393, 0, 0), parent=front),
            Part((20, 24), (-1, 0, -5, 2, 1, 6), (-3, 0, 0), (0, 0.393, 0), parent=back),
            Part((36, 24), (-1, 0, -5, 2, 1, 6), (3, 0, 0), (0, -0.393, 0), parent=back)]


def squid():
    parts = [Part((0, 0), (-6, -8, -6, 12, 16, 12), (0, 0, 0))]
    for i in range(8):
        a = i * math.pi / 4
        parts.append(Part((48, 0), (-1, 0, -1, 2, 18, 2), (math.cos(a) * 5, 7, math.sin(a) * 5), (0, -a + P2, 0)))
    return parts


def bat():
    body = Part((0, 0), (-1.5, 0, -1, 3, 5, 2), (0, 17, 0))
    head = Part((0, 7), (-2, -3, -1, 4, 3, 2), (0, 17, 0))
    rw = Part((12, 0), (-2, -2, 0, 2, 7, 0), (-1.5, 0, 0), (0, 0.5, 0), parent=body)
    lw = Part((12, 7), (0, -2, 0, 2, 7, 0), (1.5, 0, 0), (0, -0.5, 0), parent=body)
    return [body, head, Part((1, 15), (-2.5, -4, 0, 3, 5, 0), (-1.5, -2, 0), parent=head),
            Part((8, 15), (-0.1, -3, 0, 3, 5, 0), (1.1, -3, 0), parent=head), rw, lw,
            Part((16, 0), (-6, -2, 0, 6, 8, 0), (-2, 0, 0), (0, 0.3, 0), parent=rw),
            Part((16, 8), (0, -2, 0, 6, 8, 0), (2, 0, 0), (0, -0.3, 0), parent=lw),
            Part((16, 16), (-1.5, 0, 0, 3, 2, 0), (0, 5, 0), parent=body)]


def fox():
    head = Part((1, 5), (-3, -2, -5, 8, 6, 6), (-1, 16.5, -3))
    body = Part((24, 15), (-3, 3.999, -3.5, 6, 11, 6), (0, 16, -6), (P2, 0, 0))
    parts = [head, Part((8, 1), (-3, -4, -4, 2, 2, 1), parent=head), Part((15, 1), (3, -4, -4, 2, 2, 1), parent=head),
             Part((6, 18), (-1, 2.01, -8, 4, 2, 3), parent=head), body,
             Part((30, 0), (2, 0, -1, 4, 9, 5), (-4, 15, -1), (-0.052, 0, 0), parent=body)]
    for uv, x, z in (((4, 24), -5, 7), ((13, 24), -1, 7), ((4, 24), -5, 0), ((13, 24), -1, 0)):
        parts.append(Part(uv, (2, 0.5, -1, 2, 6, 2), (x, 17.5, z)))
    return parts


def dragon_model_lazy():
    return dragon_model()


# --------------------------------------------------------------------------
END_NETHER = [
    ("Spectre du Vide", "Enderman", enderman, lambda: with_overlay("enderman/enderman.png", "enderman/enderman_eyes.png")),
    ("Nanobot du Vide", "Endermite", endermite, lambda: ent("endermite/endermite.png")),
    ("Tourelle-coffre", "Shulker", shulker, lambda: ent("shulker/shulker.png")),
    ("Dragon cuirassé du Vide", "Ender Dragon", dragon_model_lazy, lambda: with_overlay("enderdragon/dragon.png", "enderdragon/dragon_eyes.png")),
    ("Drone à plasma", "Blaze", blaze, lambda: ent("blaze/blaze.png")),
    ("Sonde-méduse", "Ghast", ghast, lambda: ent("ghast/ghast.png")),
    ("Sonde-méduse (attaque)", "Ghast qui tire", ghast, lambda: ent("ghast/ghast_shooting.png")),
    ("Cube de fusion", "Cube de magma", magma, lambda: ent("slime/magmacube.png")),
    ("Droïde du Néant", "Wither squelette", skeleton, lambda: ent("skeleton/wither_skeleton.png")),
    ("Contrebandier", "Piglin", piglin, lambda: ent("piglin/piglin.png")),
    ("Garde blindé", "Piglin barbare", piglin, lambda: ent("piglin/piglin_brute.png")),
    ("Contrebandier cyborg", "Piglin zombifié", lambda: piglin((-P2, -P2)), lambda: ent("piglin/zombified_piglin.png")),
    ("Sanglier-tank", "Hoglin", hoglin, lambda: ent("hoglin/hoglin.png")),
    ("Sanglier-tank corrompu", "Zoglin", hoglin, lambda: ent("hoglin/zoglin.png")),
    ("Marcheur thermique", "Arpenteur", strider, lambda: ent("strider/strider.png")),
    ("Marcheur thermique (froid)", "Arpenteur gelé", strider, lambda: ent("strider/strider_cold.png")),
]

PASSIFS = [
    ("Porcelet mécanique", "Cochon", pig, lambda: ent("pig/pig_temperate.png")),
    ("… version désert", "Cochon (chaud)", pig, lambda: ent("pig/pig_warm.png")),
    ("… version glace", "Cochon (froid)", lambda: pig(True), lambda: ent("pig/pig_cold.png")),
    ("Vache-citerne", "Vache", cow, lambda: ent("cow/cow_temperate.png")),
    ("… version désert", "Vache (chaude)", lambda: cow("warm"), lambda: ent("cow/cow_warm.png")),
    ("… version glace", "Vache (froide)", lambda: cow("cold"), lambda: ent("cow/cow_cold.png")),
    ("Vache bio-réacteur", "Champimeuh rouge", cow, lambda: ent("cow/mooshroom_red.png")),
    ("Vache bio-réacteur", "Champimeuh brune", cow, lambda: ent("cow/mooshroom_brown.png")),
    ("Poule-drone", "Poule", chicken, lambda: ent("chicken/chicken_temperate.png")),
    ("… version glace", "Poule (froide)", lambda: chicken(True), lambda: ent("chicken/chicken_cold.png")),
    ("Mouton à ressorts", "Mouton tondu", sheep, lambda: ent("sheep/sheep.png")),
    ("Mouton à ressorts", "Mouton (laine)", None, None),
    ("Lapin sauteur", "Lapin", rabbit, lambda: ent("rabbit/rabbit_brown.png")),
    ("Lapin sauteur (or)", "Lapin doré", rabbit, lambda: ent("rabbit/rabbit_gold.png")),
    ("Calamar-sonde", "Calamar", squid, lambda: ent("squid/squid.png")),
    ("Calamar néon", "Calamar luisant", squid, lambda: ent("squid/glow_squid.png")),
    ("Chauve-souris drone", "Chauve-souris", bat, lambda: ent("bat/bat.png")),
    ("Renard éclaireur", "Renard", fox, lambda: ent("fox/fox.png")),
    ("Renard éclaireur (neige)", "Renard arctique", fox, lambda: ent("fox/fox_snow.png")),
]


def sheep_with_wool(size):
    base = ent("sheep/sheep.png")
    wool = ent("sheep/sheep_wool.png")
    k, ox, oy = rm.fit(sheep(True), wool, size)
    img = rm.render_model(sheep(), base, k, size, center=(ox, oy))
    img.alpha_composite(rm.render_model(sheep(True), wool, k, size, center=(ox, oy)))
    return img


def card_sheet(title, subtitle, entries, cols=4, cw=300, ch=320):
    rows = (len(entries) + cols - 1) // cols
    W, H = cols * cw + 40, rows * ch + 120
    img = rs.sky(W, H)
    d = ImageDraw.Draw(img)
    d.text((26, 22), title, font=rs.font(36, True), fill=(255, 190, 80))
    d.text((28, 70), subtitle, font=rs.font(17), fill=(200, 210, 235))
    for i, (name, vanilla, model, texf) in enumerate(entries):
        cx, cy = 20 + (i % cols) * cw, 106 + (i // cols) * ch
        d.rounded_rectangle([cx + 5, cy, cx + cw - 5, cy + ch - 10], radius=12, fill=(30, 26, 48, 225),
                            outline=(70, 80, 98), width=2)
        size = (cw - 24, ch - 92)
        if model is None and texf is None:
            cell = sheep_with_wool(size)
        elif model is None:  # dragon : texture à plat
            t = texf().crop((0, 0, 256, 200))
            s = min(size[0] / t.width, size[1] / t.height)
            cell = Image.new("RGBA", size, (0, 0, 0, 0))
            tt = t.resize((int(t.width * s), int(t.height * s)), Image.NEAREST)
            cell.alpha_composite(tt, ((size[0] - tt.width) // 2, (size[1] - tt.height) // 2))
        else:
            parts, tex = model(), texf()
            k, ox, oy = rm.fit(parts, tex, size)
            cell = rm.render_model(parts, tex, k, size, center=(ox, oy))
        img.alpha_composite(cell, (cx + 12, cy + 8))
        f = rs.font(19, True)
        tw = d.textlength(name, font=f)
        d.text((cx + (cw - tw) / 2, cy + ch - 80), name, font=f, fill=(150, 228, 255))
        sub = ("remplace : " + vanilla) if model is not None or texf is None else "texture (dragon)"
        f2 = rs.font(15)
        tw = d.textlength(sub, font=f2)
        d.text((cx + (cw - tw) / 2, cy + ch - 50), sub, font=f2, fill=(200, 200, 220))
    return img




# ------------------------------------------------------------ DRAGON 3D ---
def dragon_model(jaw_open=0.3, root_rot=(0, 0, 0)):
    root = Part((0, 0), (0, 0, 0, 0, 0, 0), (0, 0, 0), root_rot)
    head = Part((0, 0), (0, 0, 0, 0, 0, 0), (0, 21, -64), parent=root)
    parts = [Part((176, 44), (-6, -1, -24, 12, 5, 16), parent=head), Part((112, 30), (-8, -8, -10, 16, 16, 16), parent=head),
             Part((0, 0), (-5, -12, -4, 2, 4, 6), parent=head, mirror=True), Part((0, 0), (3, -12, -4, 2, 4, 6), parent=head),
             Part((112, 0), (-5, -3, -22, 2, 2, 4), parent=head, mirror=True), Part((112, 0), (3, -3, -22, 2, 2, 4), parent=head),
             Part((176, 65), (-6, 0, -16, 12, 4, 16), (0, 4, -8), (jaw_open, 0, 0), parent=head)]
    for i, (y, z) in enumerate(((20, -52), (18, -42), (16, -32), (15, -22), (15, -12))):
        parts += [Part((192, 104), (-5, -5, -5, 10, 10, 10), (0, y, z), parent=root),
                  Part((48, 0), (-1, -9, -3, 2, 4, 6), (0, y, z), parent=root)]
    body = Part((0, 0), (0, 0, 0, 0, 0, 0), (0, 20, 8), parent=root)
    parts.append(Part((0, 0), (-12, -16, -16, 24, 24, 64), parent=body))
    for z in (-10, 10, 30):
        parts.append(Part((220, 53), (-1, -22, z, 2, 6, 12), parent=body))
    for i in range(12):
        x, y, z = 6 * math.sin(i * 0.45), 14 + 3 * math.sin(i * 0.6), 61 + 10 * i
        parts += [Part((192, 104), (-5, -5, -5, 10, 10, 10), (x, y, z), parent=root),
                  Part((48, 0), (-1, -9, -3, 2, 4, 6), (x, y, z), parent=root)]
    for sgn in (1, -1):
        m = sgn > 0
        x0 = 0 if m else -56
        wing = Part((0, 0), (0, 0, 0, 0, 0, 0), (12 * sgn, -15, -6), (0, 0, -0.38 * sgn), parent=body)
        tip = Part((0, 0), (0, 0, 0, 0, 0, 0), (56 * sgn, 0, 0), (0, 0, 0.55 * sgn), parent=wing)
        parts += [Part((112, 88), (x0, -4, -4, 56, 8, 8), parent=wing, mirror=m),
                  Part((-56, 88), (x0, 0, 2, 56, 0, 56), parent=wing, mirror=m),
                  Part((112, 136), (x0, -2, -2, 56, 4, 4), parent=tip, mirror=m),
                  Part((-56, 144), (x0, 0, 2, 56, 0, 56), parent=tip, mirror=m)]
        fl = Part((112, 104), (-4, -4, -4, 8, 24, 8), (12 * sgn, 0, -6), (1.3, 0, 0), parent=body)
        ft = Part((226, 138), (-3, -1, -3, 6, 24, 6), (0, 20, -1), (-0.5, 0, 0), parent=fl)
        ff = Part((144, 104), (-4, 0, -12, 8, 4, 16), (0, 23, 0), (0.75, 0, 0), parent=ft)
        rl = Part((0, 0), (-8, -4, -8, 16, 32, 16), (16 * sgn, -4, 34), (1.0, 0, 0), parent=body)
        rt = Part((196, 0), (-6, -2, 0, 12, 32, 12), (0, 32, -4), (0.5, 0, 0), parent=rl)
        rf = Part((112, 0), (-9, 0, -20, 18, 6, 24), (0, 31, 4), (0.75, 0, 0), parent=rt)
        parts += [fl, ft, ff, rl, rt, rf]
    return parts


def render_dragon():
    from PIL import ImageChops, ImageFilter
    W, H = 1400, 860
    img = rs.sky(W, H)
    d = ImageDraw.Draw(img)
    for y in range(H):  # ambiance de l'End : brume violette
        a = int(70 * max(0, (y - H * 0.4) / (H * 0.6)))
        d.line([(0, y), (W, y)], fill=(60, 20, 90, a))
    img = Image.alpha_composite(rs.sky(W, H), img)
    base, glow = ent("enderdragon/dragon.png"), ent("enderdragon/dragon_eyes.png")
    hl = Image.new("RGB", (W, H), (0, 0, 0))
    views = [(dragon_model(0.45, (-1.15, -0.5, 0)), (W * 0.62, H - 120), (20, 110)),
             (dragon_model(0.3), (W * 0.4, H * 0.5), (W * 0.6, 120))]
    for parts, size, pos in views:
        size = (int(size[0]), int(size[1]))
        k, ox, oy = rm.fit(parts, base, size, margin=10)
        body = rm.render_model(parts, base, k, size, center=(ox, oy))
        lights = rm.render_model(parts, glow, k, size, center=(ox, oy))
        img.alpha_composite(body, (int(pos[0]), int(pos[1])))
        for radius in (6, 16):
            halo = lights.filter(ImageFilter.GaussianBlur(radius))
            tmp = Image.new("RGB", (W, H), (0, 0, 0))
            tmp.paste(halo.convert("RGB"), (int(pos[0]), int(pos[1])), halo)
            hl = ImageChops.add(hl, tmp)
    img = Image.merge("RGBA", (*ImageChops.add(img.convert("RGB"), hl).split(), Image.new("L", (W, H), 255)))
    d0 = ImageDraw.Draw(img)
    d0.text((W * 0.62, H * 0.58), "vue de dessus, en vol", font=rs.font(16), fill=(190, 180, 220))
    d0.text((30, H - 40), "cabré : réacteur ventral et gueule de plasma", font=rs.font(16), fill=(190, 180, 220))
    d = ImageDraw.Draw(img)
    d.text((32, 24), "Dragon cuirassé du Vide", font=rs.font(42, True), fill=(220, 160, 255))
    d.text((34, 78), "remplace l'Ender Dragon · réacteur ventral, anneaux d'énergie, voiles lumineuses, gueule de plasma",
           font=rs.font(18), fill=(200, 210, 235))
    return img


if __name__ == "__main__":
    os.makedirs(rs.OUTDIR, exist_ok=True)
    card_sheet("L'End et le Nether", "modèles Minecraft 26.x avec les textures du pack", END_NETHER).convert("RGB").save(
        os.path.join(rs.OUTDIR, "mobs_end_nether.png"))
    card_sheet("Les mobs passifs", "modèles Minecraft 26.x avec les textures du pack", PASSIFS).convert("RGB").save(
        os.path.join(rs.OUTDIR, "mobs_passifs.png"))
    render_dragon().convert("RGB").save(os.path.join(rs.OUTDIR, "dragon.png"))
    print("dragon OK")
