#!/usr/bin/env python3
"""Rendu 3D isométrique des ennemis, à partir des vraies géométries de modèles Minecraft.

À lancer après generate.py :  python3 generator/render_mobs.py
Produit : screenshots/ennemis.png, screenshots/textures_ennemis.png
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageOps

import render_screens as rs

ROOT = rs.ROOT
ENT = os.path.join(ROOT, "pack", "assets", "minecraft", "textures", "entity")
VIEW = (-1.0, 1.0, 1.0)
LIGHT = (-0.6, 1.0, 0.2)


# --------------------------------------------------------------------------
# Mini moteur : pavés texturés (box UV Minecraft), rotations ZYX, projection 2:1
# --------------------------------------------------------------------------
def rot(xr, yr, zr):
    cx, sx, cy, sy, cz, sz = math.cos(xr), math.sin(xr), math.cos(yr), math.sin(yr), math.cos(zr), math.sin(zr)
    Rx = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]]
    Ry = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]
    Rz = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]
    mm = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mm(mm(Rz, Ry), Rx)


def apply(M, v):
    return tuple(sum(M[i][k] * v[k] for k in range(3)) for i in range(3))


def to_world(p):  # espace modèle MC (y vers le bas, avant = -z) -> monde (avant = -X, haut = +Y)
    return (p[2], 24 - p[1], p[0])


def vec_world(v):
    return (v[2], -v[1], v[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


class Part:
    def __init__(self, uv, box, pivot=(0, 0, 0), r=(0, 0, 0), mirror=False, inflate=0.0):
        self.u, self.v = uv
        self.x0, self.y0, self.z0, self.w, self.h, self.d = box
        self.pivot, self.M, self.mirror, self.inf = pivot, rot(*r), mirror, inflate

    def faces(self, tex):
        u, v, w, h, d, i = self.u, self.v, self.w, self.h, self.d, self.inf
        x0, y0, z0 = self.x0 - i, self.y0 - i, self.z0 - i
        x1, y1, z1 = self.x0 + w + i, self.y0 + h + i, self.z0 + d + i
        X, Y, Z = x1 - x0, y1 - y0, z1 - z0
        reg = {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
               "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}
        if self.mirror:
            reg["left"], reg["right"] = reg["right"], reg["left"]
        geo = {  # coin haut-gauche de l'image, axe x de l'image, axe y de l'image
            "front": ((x0, y0, z0), (X, 0, 0), (0, Y, 0)),
            "back": ((x1, y0, z1), (-X, 0, 0), (0, Y, 0)),
            "left": ((x1, y0, z0), (0, 0, Z), (0, Y, 0)),
            "right": ((x0, y0, z1), (0, 0, -Z), (0, Y, 0)),
            "top": ((x0, y0, z1), (X, 0, 0), (0, 0, -Z)),
            "bottom": ((x0, y1, z0), (X, 0, 0), (0, 0, Z)),
        }
        c_local = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
        center = to_world(tuple(p + q for p, q in zip(self.pivot, apply(self.M, c_local))))
        out = []
        for name, (o, ex, ey) in geo.items():
            rx, ry, rw, rh = reg[name]
            img = tex.crop((rx, ry, rx + rw, ry + rh))
            if self.mirror:
                img = ImageOps.mirror(img)
            if img.getbbox() is None:
                continue
            ow = to_world(tuple(p + q for p, q in zip(self.pivot, apply(self.M, o))))
            exw, eyw = vec_world(apply(self.M, ex)), vec_world(apply(self.M, ey))
            fc = tuple(ow[k] + exw[k] / 2 + eyw[k] / 2 for k in range(3))
            n = tuple(fc[k] - center[k] for k in range(3))
            if dot(n, VIEW) <= 1e-6:
                continue
            nl = math.sqrt(dot(n, n)) or 1
            ll = math.sqrt(dot(LIGHT, LIGHT))
            b = 0.62 + 0.38 * max(0.0, dot(n, LIGHT) / nl / ll)
            out.append((dot(fc, VIEW), img, ow, exw, eyw, rw, rh, b))
        return out


def project(p, k, ox, oy):
    X, Y, Z = p
    return ox + (X + Z) * k, oy + (-X + Z) * k / 2 - Y * k


def render_model(parts, tex, k, size, origin=(0, 0, 0)):
    """origin : décalage monde (en texels) du modèle."""
    W, H = size
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    ox, oy = W / 2, H - 20
    faces = []
    for p in parts:
        faces += p.faces(tex)
    faces.sort(key=lambda f: f[0])
    for _, img, o, ex, ey, rw, rh, b in faces:
        o = tuple(o[i] + origin[i] for i in range(3))
        sx, sy = project(o, k, ox, oy)
        eu = ((ex[0] + ex[2]) * k / rw, (-ex[0] + ex[2]) * k / 2 / rw - ex[1] * k / rw)
        ev = ((ey[0] + ey[2]) * k / rh, (-ey[0] + ey[2]) * k / 2 / rh - ey[1] * k / rh)
        det = eu[0] * ev[1] - ev[0] * eu[1]
        if abs(det) < 1e-6:
            continue
        canvas.alpha_composite(rs.affine_face(rs.shade(img, b), size, (sx, sy), eu, ev))
    return canvas


# --------------------------------------------------------------------------
# Géométries des modèles vanilla (Java 1.21)
# --------------------------------------------------------------------------
P2 = math.pi / 2


def humanoid(arm_w, leg_w, arms_rot=(0, 0), hat=True):
    a, l = arm_w, leg_w
    parts = [Part((0, 0), (-4, -8, -4, 8, 8, 8)), Part((16, 16), (-4, 0, -2, 8, 12, 4))]
    if hat:
        parts.append(Part((32, 0), (-4, -8, -4, 8, 8, 8), inflate=0.5))
    ax = -3 if a == 4 else -1
    parts += [
        Part((40, 16), (ax, -2, -a / 2, a, 12, a), (-5, 2, 0), (arms_rot[0], 0, 0)),
        Part((40, 16), (-1, -2, -a / 2, a, 12, a), (5, 2, 0), (arms_rot[1], 0, 0), mirror=True),
        Part((0, 16), (-l / 2, 0, -l / 2, l, 12, l), (-1.9 if l == 4 else -2, 12, 0)),
        Part((0, 16), (-l / 2, 0, -l / 2, l, 12, l), (1.9 if l == 4 else 2, 12, 0), mirror=True),
    ]
    return parts


def zombie_model():
    return humanoid(4, 4, arms_rot=(-P2 + 0.05, -P2 - 0.05))


def skeleton_model():
    return humanoid(2, 2, arms_rot=(-1.35, -0.25))


def creeper_model():
    parts = [Part((0, 0), (-4, -8, -4, 8, 8, 8), (0, 6, 0)), Part((16, 16), (-4, 0, -2, 8, 12, 4), (0, 6, 0))]
    for x, z in ((-2, 4), (2, 4), (-2, -4), (2, -4)):
        parts.append(Part((0, 16), (-2, 0, -2, 4, 6, 4), (x, 18, z)))
    return parts


def spider_model():
    parts = [
        Part((32, 4), (-4, -4, -8, 8, 8, 8), (0, 15, -3)),
        Part((0, 0), (-3, -3, -3, 6, 6, 6), (0, 15, 0)),
        Part((0, 12), (-5, -4, -6, 10, 8, 12), (0, 15, 9)),
    ]
    q, e, m = math.pi / 4, math.pi / 8, 0.58119
    for z, zr, yr in ((2, q, q), (1, m, e), (0, m, -e), (-1, q, -q)):
        parts.append(Part((18, 0), (-15, -1, -1, 16, 2, 2), (-4, 15, z), (0, yr, -zr)))
        parts.append(Part((18, 0), (-1, -1, -1, 16, 2, 2), (4, 15, z), (0, -yr, zr)))
    return parts


def load(rel, eyes=False):
    t = Image.open(os.path.join(ENT, rel)).convert("RGBA")
    if eyes:
        t.alpha_composite(Image.open(os.path.join(ENT, "spider_eyes.png")).convert("RGBA"))
    return t


MOBS = [
    ("zombie/zombie.png", zombie_model, False, "entity.minecraft.zombie", "Zombie", 1.0),
    ("skeleton/skeleton.png", skeleton_model, False, "entity.minecraft.skeleton", "Squelette", 1.0),
    ("creeper/creeper.png", creeper_model, False, "entity.minecraft.creeper", "Creeper", 1.0),
    ("spider/spider.png", spider_model, True, "entity.minecraft.spider", "Araignée", 1.0),
    ("spider/cave_spider.png", spider_model, True, "entity.minecraft.cave_spider", "Araignée venimeuse", 0.7),
]


def render_gallery():
    cw, ch, k = 420, 470, 7.5
    W, H = cw * 3 + 40, ch * 2 + 110
    img = rs.sky(W, H)
    d = ImageDraw.Draw(img)
    d.text((26, 22), "Les ennemis", font=rs.font(38, True), fill=(255, 190, 80))
    d.text((28, 70), "modèles Minecraft avec les textures du pack", font=rs.font(18), fill=(200, 210, 235))
    for i, (rel, model, eyes, key, vanilla, scale) in enumerate(MOBS):
        cx, cy = 20 + (i % 3) * cw, 100 + (i // 3) * ch
        d.rounded_rectangle([cx + 6, cy, cx + cw - 6, cy + ch - 12], radius=14, fill=(30, 26, 48, 220),
                            outline=(70, 80, 98), width=2)
        sk = k * scale
        cell = render_model(model(), load(rel, eyes), sk, (cw - 20, ch - 110))
        # ombre au sol
        sh = Image.new("RGBA", cell.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([cell.width / 2 - 70 * scale, cell.height - 40, cell.width / 2 + 90 * scale, cell.height - 5],
                                   fill=(0, 0, 0, 90))
        img.alpha_composite(sh, (cx + 10, cy + 10))
        img.alpha_composite(cell, (cx + 10, cy + 10))
        name = rs.FR[key]
        f = rs.font(24, True)
        tw = d.textlength(name, font=f)
        d.text((cx + (cw - tw) / 2, cy + ch - 92), name, font=f, fill=(150, 228, 255))
        sub = "remplace : " + vanilla
        f2 = rs.font(17)
        tw = d.textlength(sub, font=f2)
        d.text((cx + (cw - tw) / 2, cy + ch - 56), sub, font=f2, fill=(200, 200, 220))
    # dernière case : planche des textures à plat
    cx, cy = 20 + 2 * cw, 100 + ch
    d.rounded_rectangle([cx + 6, cy, cx + cw - 6, cy + ch - 12], radius=14, fill=(30, 26, 48, 220),
                        outline=(70, 80, 98), width=2)
    d.text((cx + 24, cy + 16), "Textures à plat (patrons UV)", font=rs.font(18, True), fill=(255, 190, 80))
    y = cy + 50
    for rel in ("zombie/zombie.png", "skeleton/skeleton.png", "creeper/creeper.png", "spider/spider.png"):
        t = load(rel)
        s = 5 if t.height == 32 else 2.5
        t2 = t.resize((int(t.width * s), int(t.height * s)), Image.NEAREST)
        if y + t2.height > cy + ch - 20:
            break
        bg = Image.new("RGBA", t2.size, (52, 50, 70, 255))
        bg.alpha_composite(t2)
        img.paste(bg, (cx + (cw - t2.width) // 2, y))
        y += t2.height + 8
    return img


def render_ambush():
    """Les ennemis sur l'île du pack."""
    a = 44
    k = a / 16
    W = rs.build_world()
    w, h = 1280, 900
    img = rs.sky(w, h)
    ox, oy = 200, 520
    placements = [  # (mob, case x, case z) sur des zones dégagées
        (MOBS[1], 0.9, 1.4), (MOBS[0], 3.8, 2.4), (MOBS[0], 3.4, 5.6), (MOBS[3], 5.6, 6.0),
        (MOBS[4], 0.9, 5.2), (MOBS[2], 6.4, 8.6),
    ]
    draw = [((z - x + y, y), "block", (x, y, z)) for (x, y, z) in W]
    draw += [((bz - bx + 5, 5), "mob", (m, bx, bz)) for m, bx, bz in placements]
    draw.sort(key=lambda e: e[0])
    cubes = {}
    for _, kind, data in draw:
        if kind == "block":
            x, y, z = data
            name = W[data]
            cubes.setdefault(name, rs.cube(name, a))
            sx, sy = rs.screen_pos(x, y, z, a, ox, oy)
            img.alpha_composite(cubes[name], (sx, sy - a // 2))
        else:
            (rel, model, eyes, *_rest), bx, bz = data
            size = (400, 400)
            layer = render_model(model(), load(rel, eyes), k * _rest[-1], size)
            sx, sy = rs.screen_pos(bx, 4, bz, a, ox, oy)  # centre du dessus de la case
            img.alpha_composite(layer, (int(sx + a - size[0] / 2), int(sy - size[1] + 20)))
    d = ImageDraw.Draw(img)
    d.text((32, 26), "Invasion !", font=rs.font(40, True), fill=(255, 190, 80))
    d.text((34, 76), "les ennemis du pack sur l'île", font=rs.font(18), fill=(200, 210, 235))
    return img


if __name__ == "__main__":
    os.makedirs(rs.OUTDIR, exist_ok=True)
    render_gallery().convert("RGB").save(os.path.join(rs.OUTDIR, "ennemis.png"))
    render_ambush().convert("RGB").save(os.path.join(rs.OUTDIR, "invasion.png"))
    print("OK")
