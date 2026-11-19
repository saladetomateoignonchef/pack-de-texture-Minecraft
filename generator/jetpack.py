"""Élytres -> Jetpack (design original : deux réservoirs, tuyères et flammes).

Modèle 26.3 : deux plaques 10x20x2, texOffs (22, 0), texture 64x32.
Sur chaque plaque, h = distance à la charnière (épaule) : 0 = épaule, 9 = bout.
"""
from generate import CYAN, ORANGE, OUT, RED, STEEL, new, px, rect

FLAME = [(255, 252, 220), (255, 226, 120), (255, 170, 50), (240, 96, 30)]


def tank_column(h, y):
    """Couleur du jetpack à la position (h, y) d'une plaque, ou None (transparent)."""
    # sangle du harnais qui rejoint le centre du dos
    if y in (3, 4) and 6 <= h <= 9:
        return STEEL[1] if y == 3 else OUT
    # réservoir arrondi
    if 0 <= y <= 13 and 1 <= h <= 5:
        if y == 0 and h in (1, 5):
            return None
        shade = {1: ORANGE[4], 2: ORANGE[5], 3: ORANGE[3], 4: ORANGE[2], 5: ORANGE[1]}[h]
        if y in (4, 9):
            return STEEL[4] if h in (2, 3) else STEEL[2]
        if y == 6 and h == 3:
            return CYAN[4]  # jauge
        if y in (11, 12) and h in (2, 3, 4):
            return OUT if (h + y) % 2 else (250, 206, 40)  # bande de danger
        return shade
    # tuyère
    if y == 14 and 2 <= h <= 4:
        return STEEL[1]
    if y in (15, 16) and 1 <= h <= 5:
        return STEEL[3] if h in (2, 3) else STEEL[0]
    # flamme
    if y == 17 and 2 <= h <= 4:
        return FLAME[0] if h == 3 else FLAME[1]
    if y == 18 and 2 <= h <= 4:
        return FLAME[1] if h == 3 else FLAME[2]
    if y == 19 and h == 3:
        return FLAME[3]
    return None


def elytra_texture():
    t = new(64, 32)
    u, v, w, hh, d = 22, 0, 10, 20, 2
    # faces avant (24,2) : colonne 0 = bout, 9 = épaule ; arrière (36,2) : colonne 0 = épaule
    for y in range(hh):
        for col in range(w):
            c = tank_column(9 - col, y)
            if c:
                px(t, u + d + col, v + d + y, c)
            c = tank_column(col, y)
            if c:
                px(t, u + 2 * d + w + col, v + d + y, c)
    # tranche côté épaule (34,2) : flanc du réservoir ; côté bout (22,2) : sangle
    for y in range(hh):
        c = tank_column(3, y)
        for x in range(d):
            if c:
                px(t, u + d + w + x, v + d + y, ORANGE[2] if c in (ORANGE[3], ORANGE[5]) else c)
            if y in (3, 4):
                px(t, u + x, v + d + y, OUT)
    # dessus (24,0) et dessous (34,0) : colonne 0 = bout, 9 = épaule
    for col in range(w):
        h = 9 - col
        for x in range(d):
            if 1 <= h <= 5:
                px(t, u + d + col, v + x, ORANGE[3] if h != 3 else ORANGE[5])
                px(t, u + d + w + col, v + x, STEEL[0])
    return t


def item_icon(broken=False):
    """Icône 16x16 : jetpack vu de dos."""
    t = new()
    rect(t, 6, 3, 9, 4, STEEL[1])  # harnais
    rect(t, 7, 2, 8, 9, STEEL[2]); px(t, 7, 2, STEEL[4])
    for x0 in (2, 10):  # réservoirs
        rect(t, x0, 2, x0 + 3, 10, ORANGE[3])
        rect(t, x0 + 1, 2, x0 + 1, 10, ORANGE[5])
        rect(t, x0 + 3, 2, x0 + 3, 10, ORANGE[1])
        px(t, x0, 1, OUT); px(t, x0 + 3, 1, OUT); rect(t, x0 + 1, 1, x0 + 2, 1, ORANGE[4])
        rect(t, x0, 5, x0 + 3, 5, STEEL[4])
        rect(t, x0, 8, x0 + 3, 8, (250, 206, 40)); px(t, x0 + 1, 8, OUT); px(t, x0 + 3, 8, OUT)
        rect(t, x0, 11, x0 + 3, 11, STEEL[1])  # tuyère
        rect(t, x0 + 1, 12, x0 + 2, 12, STEEL[3])
        if broken:
            px(t, x0 + 1, 4, OUT); px(t, x0 + 2, 6, OUT); px(t, x0 + 1, 7, OUT)  # fissures
            px(t, x0 + 1, 14, (110, 110, 120)); px(t, x0 + 2, 15, (150, 150, 160))  # fumée
        else:
            px(t, x0 + 1, 13, FLAME[0]); px(t, x0 + 2, 13, FLAME[1])
            px(t, x0 + 1, 14, FLAME[2]); px(t, x0 + 2, 15, FLAME[3])
    if not broken:
        px(t, 7, 6, CYAN[4]); px(t, 8, 6, CYAN[3])
    else:
        px(t, 7, 6, RED[3])
    # contour sombre
    from generate import outline
    return outline(t)


TEXTURES_ENTITY = {
    "equipment/wings/elytra.png": elytra_texture,  # 1.21.2+ / 26.x
    "elytra.png": elytra_texture,  # 1.20.5 - 1.21.1
}
TEXTURES_ITEM = {
    "elytra.png": lambda: item_icon(False),
    "elytra_broken.png": lambda: item_icon(True),  # 26.x
    "broken_elytra.png": lambda: item_icon(True),  # anciennes versions
}
NAMES_FR = {"item.minecraft.elytra": "Jetpack"}
NAMES_EN = {"item.minecraft.elytra": "Jetpack"}
