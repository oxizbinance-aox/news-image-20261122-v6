#!/usr/bin/env python3
"""Draw the News Image 22 Nov 2026 v6 broadsheet: 46 dated stories, 8 regions.

One page, 1024x1024: masthead + title + 6-number data strip + region chips +
UTC timeline + 3 picture-led leads + 2 charts (drone bars, COP31 donut) +
12-story middle grid + dot-matrix world map with pins + 31-story numbered
list + region bars + date-check box. Everything drawn in code with PIL.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (16, 24, 64)
INK = (24, 24, 24)
RED = (178, 24, 32)
TEAL = (0, 128, 128)
GOLD = (184, 134, 11)
PAPER = (250, 246, 236)
PANEL = (255, 255, 255)
GREY = (90, 90, 90)
LIGHT = (232, 236, 240)
MAPBG = (220, 232, 240)
DOTC = (138, 122, 95)

REGION_COLORS = {
    "Europe": (30, 80, 160), "Middle East": (178, 24, 32),
    "North America": (0, 110, 90), "Latin America": (150, 90, 0),
    "Asia-Pacific": (120, 40, 140), "Africa": (90, 60, 20),
    "Oceania": (0, 120, 160), "World": (70, 70, 70),
}

def font(path, size):
    return ImageFont.truetype(path, int(size))

def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_font(d, text, path, size, max_w, floor=7):
    s = size
    while s > floor and d.textlength(text, font=font(path, s)) > max_w:
        s -= 0.5
    return font(path, s)

def text(d, x, y, s, fnt, fill, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

# ---------------------------------------------------------------- stories
LEADS = [
    dict(n=1, place="KYIV REGION, UKRAINE", topic="WAR", tag="REPORTED",
         tagc=TEAL, pic="night",
         head="Russia fires 186 drones at Ukraine overnight",
         body="Air defences downed or jammed 161 of 186 drones fired from eight "
              "directions. One hit a five-storey block in Dymer; seven feared "
              "trapped. (Ukrainian Air Force)"),
    dict(n=2, place="ANTALYA, TÜRKIYE", topic="CLIMATE", tag="ONGOING",
         tagc=NAVY, pic="cop",
         head="COP31 ends with no deal on fossil fuels",
         body="The final text “recalls” the Dubai pact whole, keeps the 35% "
              "clean-electricity goal for 2035, drops the $120bn adaptation "
              "target and admits 1.5°C will be overshot. (Reuters, BBC)"),
    dict(n=3, place="MANAMA, BAHRAIN", topic="GULF", tag="CLAIM",
         tagc=RED, pic="radar",
         head="Iran claims two US radars hit; Bahrain denies it",
         body="Tehran says it destroyed two US Patriot radars. Bahrain answered "
              "Sunday: the target was a civilian site — a fire, no injuries. "
              "(Al Jazeera, Reuters)"),
]

MIDDLE = [
    (4, "HONG KONG", "ELECTION", "Hong Kong elects its Election Committee",
     "856 candidates, 723 seats; polls 09:00–18:00. (SCMP)", "POLLS OPEN", RED),
    (5, "LAS VEGAS", "FORMULA 1", "Verstappen takes the Las Vegas GP",
     "Beats Norris and Piastri; Russell 5th. (Reuters, F1)", "POLE TO FLAG", NAVY),
    (6, "WELLINGTON", "CRICKET", "India declare 720/9 — a record in NZ",
     "Rahul 136, Pant 128, Gill 98; hosts 112/2. (ESPN)", "720/9 DECLARED", TEAL),
    (7, "MOSCOW", "DIPLOMACY", "US envoys to Moscow after Abu Dhabi talks",
     "Kushner and Witkoff brief Putin, then Dublin. (ANSA)", "ABU DHABI – MOSCOW", (120, 40, 140)),
    (8, "SAN ANTONIO", "NBA", "Wembanyama scores 50 as Spurs roll",
     "50 pts, 19 rebounds, 5 blocks; 114–91. (Reuters)", "50 POINTS", GOLD),
    (9, "BRASÍLIA", "HEALTH", "Bolsonaro in intensive care",
     "Bowel obstruction; stable, breathing on his own. (Reuters)", "IN INTENSIVE CARE", RED),
    (10, "WASHINGTON", "CYBER", "FBI probes hack of its crime database",
     "State pauses gun-dealer checks; breach assessed. (AP)", "FBI PROBE", NAVY),
    (11, "BRUSSELS", "TRAVEL", "Belgian controllers join Monday strike",
     "Most flights grounded 07:00–21:00. (VRT)", "FLIGHTS GROUNDED", TEAL),
    (12, "MANIPUR", "POISONING", "Toxic-liquor toll climbs to 19",
     "600 in hospital, six held. (Xinhua)", "TOLL AT 19", RED),
    (13, "GULF OF FINLAND", "SEA", "Russian cargo ship Sparta II still burning",
     "Hit by drones Saturday; Finland leads rescue. (Saturday)", "SHIP ABLAZE", (150, 90, 0)),
    (14, "TEHRAN", "ENERGY", "Iran begins rationing electricity",
     "Rolling cuts up to two hours a day. (RFE/RL)", "POWER CUTS", GOLD),
    (15, "JUNÍN", "QUAKE", "Peru quake toll: 1 dead, 16 hurt",
     "170 homes damaged in Junín; count completed. (Reuters)", "1 DEAD, 16 HURT", NAVY),
]

# (number, region, short one-line story, source)
LISTED = [
    (16, "Europe", "Estonia to shut 5 Russia crossings in 1 Dec", "Reuters"),
    (17, "Europe", "Denmark expels Russian attaché in spy row", "Guardian"),
    (18, "Asia-Pacific", "Nepal PM Shah resigns in Delhi", "IANS"),
    (19, "Asia-Pacific", "Chinese bomber turns back off Manila", "AP"),
    (20, "Asia-Pacific", "M5.9 quake, 898 km deep off Palawan", "EMSC"),
    (21, "Asia-Pacific", "Japan poll: record 52% warm to South Korea", "Yonhap"),
    (22, "Asia-Pacific", "Taiwan holds drill “resisting invasion”", "TMA"),
    (23, "Africa", "Somalia expels UAE ambassador, recalls envoy", "Wires"),
    (24, "Africa", "Sudan: RSF accused of killing civilians", "Wires"),
    (25, "Africa", "Kenya discharges its last Ebola patient", "Wires"),
    (26, "Africa", "DR Congo: candidate attack, 40 killed", "Local officials"),
    (27, "Europe", "Russia opens crypto trading", "Bank of Russia"),
    (28, "World", "Gold near $5,355; Bitcoin above $60,000", "Markets"),
    (29, "North America", "Nvidia faces SEC accounting probe", "Reports"),
    (30, "Middle East", "Trump seeks “permanent” Iran deal", "Al Jazeera"),
    (31, "Middle East", "Hamas seeks US role as Iran mediator", "Al Jazeera"),
    (32, "Africa", "Sudan army retakes 30 towns in Kordofan", "UPI"),
    (33, "World", "EU–Indonesia sign trade deal after ten years", "DW"),
    (34, "Asia-Pacific", "World court: Myanmar guilty of genocide", "Guardian"),
    (35, "Oceania", "Melbourne: 70 years since the 1956 Olympics", "ABC"),
    (36, "Oceania", "Cummins keeps Australia’s Test captaincy", "Wires"),
    (37, "Middle East", "Houthi missile over Riyadh", "Anadolu"),
    (38, "Asia-Pacific", "Cikande factory fire: 3 dead, 36 missing", "Reuters"),
    (39, "Middle East", "Israeli fire kills four in Gaza", "Al Jazeera"),
    (40, "Africa", "Drones strike homes near Khartoum", "AFP"),
    (41, "Africa", "Mourners: boat capsizes in Nigeria, 29 dead", "AP"),
    (42, "Europe", "Pope hosts 1,300 poor guests at Vatican", "Vatican News"),
    (43, "Oceania", "Ashes: Australia press on day two in Perth", "Wires"),
    (44, "Europe", "Pope leads Sunday Angelus in St Peter’s", "Vatican News"),
    (45, "World", "Oil steady as traders weigh COP31 outcome", "Markets"),
    (46, "North America", "NFL: Week 12 Sunday slate under way", "Wires"),
]

REGIONS = [("Europe", 10), ("Middle East", 6), ("North America", 5),
           ("Latin America", 2), ("Asia-Pacific", 9), ("Africa", 7),
           ("Oceania", 4), ("World", 3)]
assert sum(c for _, c in REGIONS) == 46
assert len(LEADS) + len(MIDDLE) + len(LISTED) == 46

# ---------------------------------------------------------------- map data
# land spans per row, 52 columns (lon -180..180), 30 rows (lat 80..-60)
LAND = [
    [(1, 5), (10, 16), (33, 50)],
    [(1, 6), (8, 18), (20, 23), (33, 51)],
    [(1, 6), (7, 18), (20, 23), (25, 29), (32, 51)],
    [(2, 6), (7, 18), (24, 25), (25, 28), (31, 51)],
    [(7, 18), (24, 25), (26, 28), (30, 50)],
    [(8, 17), (24, 31), (32, 50)],
    [(8, 17), (24, 32), (33, 51)],
    [(8, 17), (24, 32), (33, 45), (48, 50)],
    [(8, 16), (24, 31), (32, 36), (37, 48)],
    [(9, 16), (24, 29), (32, 37), (38, 47)],
    [(9, 16), (23, 31), (32, 36), (38, 46)],
    [(10, 14), (23, 32), (33, 36), (38, 41), (43, 46)],
    [(11, 14), (24, 33), (33, 35), (39, 41), (43, 47)],
    [(11, 14), (24, 33), (40, 41), (44, 47)],
    [(14, 19), (24, 33), (44, 46)],
    [(14, 20), (25, 32), (42, 47)],
    [(14, 20), (25, 31), (42, 46)],
    [(15, 20), (26, 31), (43, 45)],
    [(15, 20), (26, 30), (43, 45)],
    [(15, 19), (27, 29), (42, 48)],
    [(15, 19), (27, 29), (42, 48)],
    [(16, 19), (27, 29), (31, 32), (42, 48)],
    [(16, 18), (27, 29), (43, 47)],
    [(16, 18), (43, 47), (50, 51)],
    [(16, 18), (50, 51)],
    [(17, 18)],
    [(17, 18)],
    [(17, 18)],
    [(17, 17)],
    [],
]

# (story number, lon, lat, dx, dy) pins on the map
PINS = [
    (1, 30.5, 50.4, 0, -2), (2, 30.7, 36.9, 2, 3), (3, 50.6, 26.2, 6, 0),
    (4, 114.0, 22.3, 0, 0), (5, -115.0, 36.0, -4, 0), (6, 174.8, -41.3, 0, 0),
    (16, 24.7, 59.4, -3, -3), (19, 121.0, 14.6, 4, 2), (23, 45.3, 2.0, 5, 2),
    (35, 145.0, -37.8, 0, -2), (39, 34.5, 31.5, -7, 6), (41, 6.0, 9.0, -4, 0),
]

# ---------------------------------------------------------------- pictograms
def pic_night(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 48))
    for (px, py, r) in [(12, 12, 2), (40, 26, 1), (70, 10, 2), (120, 20, 1),
                        (170, 12, 2), (220, 28, 1), (260, 14, 2), (300, 24, 1)]:
        d.ellipse([x + px - r, y + py - r, x + px + r, y + py + r], fill=(255, 255, 220))
    for i in range(9):  # city lights
        bx = x + 14 + i * 34
        bh = 10 + (i * 7) % 22
        d.rectangle([bx, y + h - 8 - bh, bx + 18, y + h - 8], fill=(240, 190, 60))
        d.rectangle([bx + 4, y + h - 8 - bh + 4, bx + 8, y + h - 8 - bh + 8], fill=(255, 240, 170))
    d.polygon([(x + w - 70, y + h - 8), (x + w - 30, y + 8), (x + w - 6, y + h - 8)],
              fill=(250, 240, 180))  # searchlight beam
    for (dx, dy) in [(60, 34), (150, 46), (230, 30)]:  # drones
        d.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3], fill=(255, 80, 70))
        d.line([x + dx - 8, y + dy, x + dx + 8, y + dy], fill=(255, 180, 160), width=1)

def pic_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 60, 52))
    d.ellipse([x + 18, y + 10, x + 88, y + 80], fill=(40, 170, 150),
              outline=(220, 255, 240), width=2)
    d.arc([x + 30, y + 22, x + 76, y + 68], 200, 340, fill=(220, 255, 240), width=2)
    d.line([x + 24, y + 45, x + 82, y + 45], fill=(220, 255, 240), width=2)
    d.ellipse([x + w - 52, y + 14, x + w - 22, y + 44], fill=(250, 200, 80))  # sun
    for i, c in enumerate([(200, 60, 60), (60, 120, 200), (240, 200, 60),
                           (90, 180, 90), (230, 120, 40)]):
        bx = x + 120 + i * 38
        d.ellipse([bx, y + 46, bx + 16, y + 62], fill=(240, 220, 190))  # heads
        d.rectangle([bx - 2, y + 64, bx + 18, y + h - 10], fill=c)     # flags
    d.rectangle([x + 110, y + h - 10, x + w - 10, y + h - 6], fill=(120, 80, 40))

def pic_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 20, 52))
    cx, cy = x + w // 2, y + h - 6
    for r in (26, 52, 78):
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(140, 220, 255), width=2)
    d.line([cx, cy, cx + 66, cy - 66], fill=(255, 220, 100), width=2)
    d.ellipse([cx + 62, cy - 70, cx + 70, cy - 62], fill=(255, 220, 100))
    for (dx, dy) in [(-70, -18), (70, -30), (-40, -44)]:
        d.polygon([(cx + dx, cy - 6), (cx + dx + 16, cy - 6), (cx + dx + 8, cy + dy)],
                  fill=(150, 150, 170))
        d.ellipse([cx + dx + 5, cy + dy - 5, cx + dx + 11, cy + dy + 1], fill=(255, 120, 100))
    for (px, py, r) in [(30, 16, 2), (90, 10, 1), (250, 18, 2), (290, 30, 1)]:
        d.ellipse([x + px - r, y + py - r, x + px + r, y + py + r], fill=(255, 255, 255))

# ---------------------------------------------------------------- draw
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# top bar
d.rectangle([0, 0, W, 24], fill=NAVY)
text(d, 8, 5, "THE WORLD IN ONE DAY", font(SANSB, 11), (255, 255, 255))
text(d, W - 8, 5, "46 STORIES  ·  8 REGIONS  ·  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
     font(SANSB, 11), (255, 200, 60), anchor="ra")

# title + deck
text(d, W // 2, 28, "Sunday 22 November 2026", font(SERIF, 54), INK, anchor="ma")
text(d, W // 2, 88,
     "186 drones over Ukraine in the night  ·  COP31 ends with no fossil-fuel deal  ·  "
     "Iran’s radar claim meets Bahrain’s denial",
     font(SANS, 12), RED, anchor="ma")

# data strip: 6 big numbers
strip = [("186", "drones fired overnight"), ("161", "downed or jammed"),
         ("35%", "clean-power goal for 2035, kept"), ("$120bn", "adaptation target dropped"),
         ("720/9", "India’s record Test total"), ("50", "Wembanyama points")]
sx, sw = 8, (W - 16) // 6
for i, (num, lab) in enumerate(strip):
    cx = sx + i * sw
    d.line([cx, 108, cx, 148], fill=(200, 190, 170), width=1)
    text(d, cx + sw // 2, 106, num, font(SERIF, 26), RED, anchor="ma")
    text(d, cx + sw // 2, 136, lab, font(SANS, 9), GREY, anchor="ma")
d.line([8, 152, W - 8, 152], fill=INK, width=2)

# region chips
rx = 8
text(d, rx, 156, "REGIONS:", font(SANSB, 10), INK)
rx += 62
for name, cnt in REGIONS:
    label = f"{name.upper()} {cnt}"
    fnt = font(SANSB, 10)
    cw = int(d.textlength(label, font=fnt)) + 12
    d.rounded_rectangle([rx, 154, rx + cw, 170], radius=3, fill=REGION_COLORS[name])
    text(d, rx + 6, 156, label, fnt, (255, 255, 255))
    rx += cw + 5
d.line([8, 174, W - 8, 174], fill=INK, width=1)

# UTC timeline
d.rectangle([8, 178, W - 8, 194], fill=NAVY)
utc = ("THE DAY IN UTC   01:00 HK polls open  ·  03:00 COP31 objections close  ·  "
       "05:11 Hamas seeks talks  ·  05:30 Verstappen wins  ·  06:00 COP31 approval due  ·  "
       "07:30 Approval slips")
uf = fit_font(d, utc, SANSB, 11, W - 24)
text(d, 14, 181, utc, uf, (255, 255, 255))

# leads
lead_x = [8, 346, 684]
for li, lead in enumerate(LEADS):
    x0 = lead_x[li]
    w0 = 330
    d.rectangle([x0, 198, x0 + w0, 378], outline=(190, 180, 165), width=1, fill=PANEL)
    {"night": pic_night, "cop": pic_cop, "radar": pic_radar}[lead["pic"]](
        d, x0 + 1, 199, w0 - 2, 86)
    d.ellipse([x0 + 8, 272, x0 + 30, 294], fill=RED, outline=(255, 255, 255), width=2)
    text(d, x0 + 19, 275, str(lead["n"]), font(SANSB, 12), (255, 255, 255), anchor="ma")
    text(d, x0 + 36, 290, f"{lead['n']}  {lead['place']} · {lead['topic']}",
         font(SANSB, 10), RED)
    bw = x0 + w0 - 8
    d.rectangle([bw - 66, 288, bw, 302], fill=lead["tagc"])
    text(d, bw - 33, 290, lead["tag"], font(SANSB, 8), (255, 255, 255), anchor="ma")
    hl = wrap(d, lead["head"], font(SERIF, 16), w0 - 16)
    yy = 306
    for ln in hl[:2]:
        text(d, x0 + 8, yy, ln, font(SERIF, 16), INK)
        yy += 19
    bsize = 10
    bl = wrap(d, lead["body"], font(SANS, bsize), w0 - 16)
    while len(bl) > 3 and bsize > 8:
        bsize -= 0.5
        bl = wrap(d, lead["body"], font(SANS, bsize), w0 - 16)
    yy = 344
    for ln in bl[:3]:
        text(d, x0 + 8, yy, ln, font(SANS, bsize), (40, 40, 40))
        yy += 12

# charts row
d.rectangle([8, 382, 508, 466], outline=(190, 180, 165), width=1, fill=PANEL)
text(d, 16, 386, "THE NIGHT OVER UKRAINE — DRONES", font(SANSB, 10), INK)
for j, (lab, val, col) in enumerate([("Fired", 186, RED), ("Downed or jammed", 161, NAVY)]):
    yy = 406 + j * 26
    text(d, 16, yy, lab, font(SANS, 10), INK)
    bw = int(300 * val / 186)
    d.rectangle([150, yy + 1, 150 + bw, yy + 13], fill=col)
    text(d, 154 + bw, yy, str(val), font(SANSB, 11), col)
text(d, 16, 452, "161 of 186 — 87% stopped before impact.", font(SANS, 9), GREY)

d.rectangle([516, 382, 1016, 466], outline=(190, 180, 165), width=1, fill=PANEL)
text(d, 524, 386, "COP31 IN NUMBERS — NATIONS", font(SANSB, 10), INK)
cx, cy, R, r = 596, 428, 30, 19
d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(215, 220, 225))
d.pieslice([cx - R, cy - R, cx + R, cy + R], -90, -90 + int(360 * 130 / 195),
           fill=TEAL)
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PANEL)
text(d, cx, cy - 7, "130+", font(SANSB, 12), TEAL, anchor="ma")
text(d, 640, 406, "backed fossil-fuel language", font(SANS, 10), INK)
text(d, 640, 422, "of ~195 nations at COP31", font(SANS, 10), GREY)
text(d, 640, 438, "Signed electrification pledge  90+", font(SANS, 9), INK)
d.rectangle([640, 452, 640 + int(300 * 90 / 195), 460], fill=GOLD)

# middle grid: 12 stories, 6 columns x 2 rows
gx, gy, cw, chh = 8, 470, 163, 89
for i, (n, place, topic, head, body, tag, col) in enumerate(MIDDLE):
    col_i, row_i = i % 6, i // 6
    x0 = gx + col_i * (cw + 5)
    y0 = gy + row_i * (chh + 2)
    d.rectangle([x0, y0, x0 + cw, y0 + chh], outline=(190, 180, 165), width=1, fill=PANEL)
    d.rectangle([x0, y0, x0 + cw, y0 + 20], fill=col)
    text(d, x0 + 5, y0 + 4, tag, font(SANSB, 8), (255, 255, 255))
    text(d, x0 + cw - 5, y0 + 4, "REPORTED", font(SANSB, 7), (255, 255, 255), anchor="ra")
    text(d, x0 + 5, y0 + 24, f"{n} {place} · {topic}", font(SANSB, 8), RED)
    hl = wrap(d, head, font(SANSB, 11), cw - 10)
    yy = y0 + 36
    for ln in hl[:2]:
        text(d, x0 + 5, yy, ln, font(SANSB, 11), INK)
        yy += 12
    bl = wrap(d, body, font(SANS, 9), cw - 10)
    yy = y0 + 62
    for ln in bl[:2]:
        text(d, x0 + 5, yy, ln, font(SANS, 9), (60, 60, 60))
        yy += 11

# map + list section header
text(d, 8, 654, "WHERE IT HAPPENED", font(SANSB, 11), INK)
text(d, 168, 655, "pins match story numbers", font(SANS, 9), GREY)
text(d, 330, 654, "ALSO ON SUNDAY 22 NOVEMBER — 31 MORE STORIES",
     font(SANSB, 11), INK)
d.line([8, 668, W - 8, 668], fill=INK, width=1)

# map panel
d.rectangle([8, 672, 316, 950], outline=(190, 180, 165), width=1, fill=MAPBG)
mx0, my0, pitch = 16, 678, 5.5
for ri, spans in enumerate(LAND):
    for (c0, c1) in spans:
        for c in range(c0, c1 + 1):
            cx = mx0 + c * pitch + pitch / 2
            cy = my0 + ri * pitch + pitch / 2
            d.ellipse([cx - 1.7, cy - 1.7, cx + 1.7, cy + 1.7], fill=DOTC)
for (n, lon, lat, dx, dy) in PINS:
    px = mx0 + (lon + 180) / 360 * 52 * pitch + dx
    py = my0 + (80 - lat) / 140 * 30 * pitch + dy
    d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255), width=1)
    text(d, px, py - 5, str(n), font(SANSB, 7), (255, 255, 255), anchor="ma")
# region bars under the map
text(d, 16, 852, "STORIES BY REGION", font(SANSB, 10), INK)
for j, (name, cnt) in enumerate(REGIONS):
    yy = 870 + j * 9
    text(d, 16, yy, name, font(SANS, 8), INK)
    bw = int(150 * cnt / 10)
    d.rectangle([108, yy + 1, 108 + bw, yy + 7], fill=REGION_COLORS[name])
    text(d, 112 + bw, yy, str(cnt), font(SANSB, 8), INK)
text(d, 16, 942, "46 stories · 8 regions · 3 leads · 2 charts",
     font(SANS, 8), GREY)

# numbered list, two columns
for ci in range(2):
    col_items = LISTED[ci * 16:(ci + 1) * 16]
    lx = 330 + ci * 344
    yy = 676
    for (n, region, short, src) in col_items:
        rc = REGION_COLORS[region]
        d.rectangle([lx, yy, lx + 14, yy + 11], fill=rc)
        text(d, lx + 7, yy, str(n), font(SANSB, 7), (255, 255, 255), anchor="ma")
        s = f"{region}: {short} ({src})"
        fnt = fit_font(d, s, SANS, 10.5, 320, floor=8)
        text(d, lx + 18, yy, s, fnt, INK)
        yy += 17

# date-check box
d.rectangle([8, 954, 1016, 982], outline=RED, width=2, fill=(255, 240, 240))
d.rectangle([14, 959, 96, 973], fill=RED)
text(d, 16, 960, "DATE CHECK", font(SANSB, 9), (255, 255, 255))
dc = ("Left out as other days’ news: the 400-drone night (Thu) · the 148-drone night (Fri) · "
      "110-missile barrage (Thu–Fri) · “El Chapo Isidro” captured (Fri) · Gaza aid-van strike "
      "(Sat) · BepiColombo Mercury burn (Sat) · Peru quake itself Fri 20 Nov · "
      "Bitcoin $55,830 two-year low (Sat).")
dl = wrap(d, dc, font(SANS, 10), 900)
yy = 958
for ln in dl[:2]:
    text(d, 104, yy, ln, font(SANS, 10), INK)
    yy += 11

# sources + bottom bar
text(d, 8, 986,
     "Sources: Reuters, BBC, Al Jazeera, The Guardian, AP, SCMP, ESPN, Xinhua, RFE/RL, UPI, DW, "
     "AFP, Anadolu, Vatican News, EMSC, Yonhap, IANS, ABC, TMA, VRT, ANSA, F1, Wires. Pictures and "
     "map: original, drawn in code.",
     font(SANS, 8), GREY)
d.rectangle([0, 1000, W, H], fill=NAVY)
text(d, 8, 1006, "THE WORLD IN ONE DAY", font(SANSB, 10), (255, 255, 255))
text(d, W - 8, 1006, "SUNDAY 22 NOVEMBER 2026 · ONE PAGE", font(SANSB, 10),
     (255, 200, 60), anchor="ra")

img.save(OUT, "PNG")
print("saved", OUT, img.size, "stories:", len(LEADS) + len(MIDDLE) + len(LISTED))
