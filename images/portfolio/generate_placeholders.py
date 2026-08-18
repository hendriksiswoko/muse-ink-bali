import math
import random
from PIL import Image, ImageDraw, ImageFilter

SIZE = 800
SS = 4  # supersample factor
CANVAS = SIZE * SS
PAPER = (243, 240, 232, 255)
INK = (30, 28, 26, 255)
INK_SOFT = (60, 56, 52, 180)


def new_canvas():
    im = Image.new("RGBA", (CANVAS, CANVAS), PAPER)
    # subtle paper grain
    draw = ImageDraw.Draw(im)
    rnd = random.Random(42)
    for _ in range(2200):
        x = rnd.randint(0, CANVAS - 1)
        y = rnd.randint(0, CANVAS - 1)
        shade = rnd.randint(-10, 10)
        c = tuple(max(0, min(255, PAPER[i] + shade)) for i in range(3)) + (60,)
        draw.point((x, y), fill=c)
    return im, draw


def finish(im, path):
    im = im.resize((SIZE, SIZE), Image.LANCZOS)
    im = im.convert("RGB")
    im.save(path, quality=87, optimize=True)
    print("saved", path)


def blackwork():
    im, d = new_canvas()
    cx, cy = CANVAS / 2, CANVAS / 2
    r0 = CANVAS * 0.34
    # solid mandala core
    d.ellipse([cx - r0, cy - r0, cx + r0, cy + r0], fill=INK)
    d.ellipse([cx - r0 * 0.62, cy - r0 * 0.62, cx + r0 * 0.62, cy + r0 * 0.62], fill=PAPER)
    d.ellipse([cx - r0 * 0.46, cy - r0 * 0.46, cx + r0 * 0.46, cy + r0 * 0.46], fill=INK)
    # radiating triangles
    n = 16
    r1, r2 = r0 * 1.05, r0 * 155 / 1000 * CANVAS / CANVAS * 1.55
    r2 = r0 * 1.55
    for i in range(n):
        a = 2 * math.pi * i / n
        bx = cx + math.cos(a) * r1
        by = cy + math.sin(a) * r1
        tip_a = a + (math.pi / n) * 0.9
        tip_b = a - (math.pi / n) * 0.9
        p1 = (cx + math.cos(tip_a) * r1, cy + math.sin(tip_a) * r1)
        p2 = (cx + math.cos(tip_b) * r1, cy + math.sin(tip_b) * r1)
        p3 = (cx + math.cos(a) * r2, cy + math.sin(a) * r2)
        d.polygon([p1, p2, p3], fill=INK)
    # dotwork ring
    for i in range(60):
        a = 2 * math.pi * i / 60
        rr = r0 * 1.78
        x = cx + math.cos(a) * rr
        y = cy + math.sin(a) * rr
        rad = CANVAS * 0.012
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=INK)
    finish(im, "blackwork/sample.jpg")


def fineline():
    im, d = new_canvas()
    stroke = max(2, int(CANVAS * 0.0035))
    cx, cy = CANVAS * 0.5, CANVAS * 0.56
    # single continuous stem, curved
    pts = []
    for i in range(200):
        t = i / 199
        x = cx + math.sin(t * math.pi * 1.6) * CANVAS * 0.16
        y = CANVAS * 0.82 - t * CANVAS * 0.62
        pts.append((x, y))
    d.line(pts, fill=INK, width=stroke, joint="curve")
    # leaves & small blooms along the stem
    rnd = random.Random(7)
    for i in range(6, len(pts) - 10, 22):
        x, y = pts[i]
        side = 1 if i % 44 == 0 else -1
        ang = math.atan2(pts[i + 8][1] - y, pts[i + 8][0] - x) + side * math.pi / 2.4
        lx = x + math.cos(ang) * CANVAS * 0.11
        ly = y + math.sin(ang) * CANVAS * 0.11
        leaf = [
            (x, y),
            (x + math.cos(ang - 0.4) * CANVAS * 0.05, y + math.sin(ang - 0.4) * CANVAS * 0.05),
            (lx, ly),
            (x + math.cos(ang + 0.4) * CANVAS * 0.05, y + math.sin(ang + 0.4) * CANVAS * 0.05),
        ]
        d.line(leaf + [leaf[0]], fill=INK, width=stroke, joint="curve")
    # small flower at top
    tx, ty = pts[-1]
    for i in range(6):
        a = 2 * math.pi * i / 6
        r = CANVAS * 0.055
        px = tx + math.cos(a) * r
        py = ty + math.sin(a) * r
        d.ellipse([px - r * 0.55, py - r * 0.55, px + r * 0.55, py + r * 0.55], outline=INK, width=stroke)
    d.ellipse([tx - CANVAS * 0.02, ty - CANVAS * 0.02, tx + CANVAS * 0.02, ty + CANVAS * 0.02], fill=INK)
    finish(im, "fineline/sample.jpg")


def ornamen_bali():
    im, d = new_canvas()
    cx, cy = CANVAS / 2, CANVAS / 2
    stroke = max(2, int(CANVAS * 0.004))

    def spiral(center, r_start, r_end, turns, width):
        pts = []
        steps = 240
        for i in range(steps):
            t = i / (steps - 1)
            a = t * turns * 2 * math.pi
            r = r_start + (r_end - r_start) * t
            pts.append((center[0] + math.cos(a) * r, center[1] + math.sin(a) * r))
        d.line(pts, fill=INK, width=width, joint="curve")

    # central sun / karang boma motif
    r0 = CANVAS * 0.09
    d.ellipse([cx - r0, cy - r0, cx + r0, cy + r0], outline=INK, width=stroke)
    d.ellipse([cx - r0 * 0.5, cy - r0 * 0.5, cx + r0 * 0.5, cy + r0 * 0.5], fill=INK)
    n = 12
    for i in range(n):
        a = 2 * math.pi * i / n
        x1 = cx + math.cos(a) * r0
        y1 = cy + math.sin(a) * r0
        x2 = cx + math.cos(a) * r0 * 1.7
        y2 = cy + math.sin(a) * r0 * 1.7
        d.line([(x1, y1), (x2, y2)], fill=INK, width=stroke)
        d.ellipse([x2 - stroke * 1.4, y2 - stroke * 1.4, x2 + stroke * 1.4, y2 + stroke * 1.4], fill=INK)

    # four interlocking corner spirals (patra-style)
    offset = CANVAS * 0.30
    corners = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for sx, sy in corners:
        center = (cx + sx * offset, cy + sy * offset)
        spiral(center, CANVAS * 0.01, CANVAS * 0.085, 2.4, stroke)

    # connecting scrollwork ring
    r_ring = CANVAS * 0.33
    pts = []
    steps = 400
    for i in range(steps):
        t = i / (steps - 1)
        a = t * 2 * math.pi
        wobble = math.sin(a * 8) * CANVAS * 0.012
        r = r_ring + wobble
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    pts.append(pts[0])
    d.line(pts, fill=INK, width=stroke, joint="curve")

    finish(im, "ornamen-bali/sample.jpg")


def realism():
    im, d = new_canvas()
    cx, cy = CANVAS * 0.5, CANVAS * 0.46
    r = CANVAS * 0.30

    # base radial shading (soft grayscale blob) to fake pencil-shaded realism
    shade = Image.new("L", (CANVAS, CANVAS), 0)
    sd = ImageDraw.Draw(shade)
    for i in range(160, 0, -1):
        t = i / 160
        rad = r * t
        val = int(235 * (1 - t) ** 1.6)
        sd.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=val)
    shade = shade.filter(ImageFilter.GaussianBlur(CANVAS * 0.012))

    dark = Image.new("RGBA", (CANVAS, CANVAS), (20, 18, 16, 255))
    im = Image.composite(dark, im, shade.point(lambda v: int(v * 0.72)))
    d = ImageDraw.Draw(im)

    # eye almond outline (realism motif)
    aw, ah = r * 1.35, r * 0.62
    d.ellipse([cx - aw, cy - ah, cx + aw, cy + ah], outline=INK, width=max(2, int(CANVAS * 0.006)))
    # iris with radial lines
    iris_r = ah * 0.92
    d.ellipse([cx - iris_r, cy - iris_r, cx + iris_r, cy + iris_r], outline=INK, width=max(2, int(CANVAS * 0.004)))
    rnd = random.Random(3)
    for i in range(40):
        a = 2 * math.pi * i / 40
        r1 = iris_r * 0.25
        r2 = iris_r * (0.85 + rnd.uniform(-0.08, 0.08))
        x1, y1 = cx + math.cos(a) * r1, cy + math.sin(a) * r1
        x2, y2 = cx + math.cos(a) * r2, cy + math.sin(a) * r2
        d.line([(x1, y1), (x2, y2)], fill=INK_SOFT, width=max(1, int(CANVAS * 0.0015)))
    pupil_r = iris_r * 0.34
    d.ellipse([cx - pupil_r, cy - pupil_r, cx + pupil_r, cy + pupil_r], fill=INK)
    # highlight
    hl_r = pupil_r * 0.4
    hx, hy = cx - pupil_r * 0.4, cy - pupil_r * 0.5
    d.ellipse([hx - hl_r, hy - hl_r, hx + hl_r, hy + hl_r], fill=(245, 242, 236, 255))
    # lower lash suggestion
    lash_pts = []
    for i in range(60):
        t = i / 59
        x = cx - aw + t * aw * 2
        y = cy + ah * math.sin(t * math.pi) * 0.55
        lash_pts.append((x, y))
    d.line(lash_pts, fill=INK, width=max(2, int(CANVAS * 0.006)), joint="curve")

    finish(im, "realism/sample.jpg")


blackwork()
fineline()
ornamen_bali()
realism()
