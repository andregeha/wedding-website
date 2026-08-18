"""Table cards from the couple's hand-made scans: calligraphy name + ink drawing.
A5 (stand on table) + A7 (entrance), monochrome ink, matched by content."""
import os, sys
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from PIL import Image
from io import BytesIO
import fitz
from tables_extract import extract_name, extract_drawing, INK

HERE = os.path.dirname(os.path.abspath(__file__))
FDIR = "/mnt/skills/examples/canvas-design/canvas-fonts/"
BLUE_MODE = '--blue' in sys.argv
BLUE_INK = (60, 62, 138)          # ballpoint blue for the calligraphy (matches the drawings)
NAME_INK = BLUE_INK if BLUE_MODE else INK
DRAW_INK = None if BLUE_MODE else INK   # None = keep the drawings' original blue
TAG = "-blue" if BLUE_MODE else ""
INKC = colors.Color(*[v/255 for v in INK])
GREY = colors.Color(120/255, 120/255, 116/255)
HAIR = colors.Color(188/255, 188/255, 184/255)
SAGE = colors.Color(95/255, 125/255, 99/255)
W, H = 148, 210   # mm

# (num, label, name_page, name_idx, draw_page, rotate_deg)
TABLES = [
 (1, "Cèdre du Liban", 5, 2, 20, 0),
 (2, "Fleur d'Oranger", 1, 1, 10, -90),
 (3, "Rose de Mai", 1, 2, 11, -90),
 (4, "Pivoine Blanche", 2, 0, 12, -90),
 (5, "Magnolia de Méditerranée", 2, 1, 13, -90),
 (6, "Iris Poudré", 2, 2, 14, -90),
 (7, "Citron Vert", 3, 0, 15, -90),
 (8, "Bergamotte", 3, 1, 16, -90),
 (9, "Pamplemousse", 3, 2, 17, -90),
 (10, "Bois d'Oud", 4, 0, 22, 0),
 (11, "Cyprès de Montagne", 4, 1, 23, 0),
 (12, "Vanille Bourbon", 4, 2, 24, 0),
 (13, "Musc Blanc", 8, 0, 31, 0),
 (14, "Menthe Fraîche", 5, 1, 19, 0),
 (15, "Jasmin d'Orient", 1, 0, 9, -90),
 (16, "Santal Boisé", 5, 3, 21, 0),
 (17, "Fève Tonka", 6, 0, 25, 0),
 (18, "Miel de Fleurs", 6, 1, 26, 0),
 (19, "Cardamome", 6, 2, 27, 0),
 (20, "Patchouli Tropical", 7, 0, 28, 0),
 (21, "Cannelle", 7, 1, 29, 90),
 (22, "Chocolat des Îles", 7, 2, 30, -90),
 (23, "Verveine Sauvage", 5, 0, 18, 0),
]


def shrink(img, maxpx=1500):
    m = max(img.size)
    if m > maxpx:
        s = maxpx/m
        img = img.resize((max(1, int(img.size[0]*s)), max(1, int(img.size[1]*s))), Image.LANCZOS)
    return img


def to_reader(img):
    """Flatten onto white (card bg is white) and embed as JPEG to keep files small."""
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255)); bg.paste(img, mask=img.split()[3]); img = bg
    else:
        img = img.convert('RGB')
    b = BytesIO(); img.save(b, 'JPEG', quality=90); b.seek(0)
    return ImageReader(b)


def place(c, img, cx, top, bottom, maxw):
    iw, ih = img.size; ar = iw/ih
    boxh = bottom-top; w = maxw; h = w/ar
    if h > boxh: h = boxh; w = h*ar
    x = cx-w/2; ytop = top+(boxh-h)/2
    c.drawImage(to_reader(img), x*mm, (H-(ytop+h))*mm, width=w*mm, height=h*mm)


def draw_card(c, num, name_img, draw_img):
    cx = W/2
    c.setStrokeColor(HAIR); c.setLineWidth(1.1); c.rect(11*mm, 11*mm, (W-22)*mm, (H-22)*mm)
    c.setStrokeColor(colors.Color(224/255,227/255,220/255)); c.setLineWidth(0.5)
    c.rect(13.4*mm, 13.4*mm, (W-26.8)*mm, (H-26.8)*mm)
    # number
    num_s = "Nº %d" % num; s = 10.5; tr = s*0.32
    c.setFont("Plex", s); c.setFillColor(GREY)
    ws = [c.stringWidth(ch, "Plex", s) for ch in num_s]; tot = sum(ws)+tr*(len(num_s)-1)
    x = cx*mm - tot/2; y = (H-25)*mm
    for ch, wch in zip(num_s, ws):
        c.drawString(x, y, ch); x += wch+tr
    # name (calligraphy) centered in band 30..56 mm
    place(c, name_img, cx, 30, 56, 112)
    # short sage rule
    c.setStrokeColor(SAGE); c.setLineWidth(0.8)
    c.line((cx-11)*mm, (H-60)*mm, (cx+11)*mm, (H-60)*mm)
    # drawing hero
    place(c, draw_img, cx, 66, 191, 110)
    c.showPage()


def build():
    pdfmetrics.registerFont(TTFont("Plex", FDIR+"IBMPlexSerif-Regular.ttf"))
    names, draws = {}, {}
    for num, lab, npg, nidx, dpg, rot in TABLES:
        print("extract", num, lab)
        names[num] = shrink(extract_name(npg, nidx, ink=NAME_INK), 1200)
        draws[num] = shrink(extract_drawing(dpg, rotate=rot, ink=DRAW_INK), 1500)
    a5 = os.path.join(HERE, "tables%s-A5.pdf" % TAG)
    c = canvas.Canvas(a5, pagesize=(W*mm, H*mm))
    for num, lab, *_ in TABLES:
        draw_card(c, num, names[num], draws[num])
    c.save()
    # A7 = A5 at half scale
    a7 = os.path.join(HERE, "tables%s-A7.pdf" % TAG)
    src = fitz.open(a5); out = fitz.open()
    for p in range(src.page_count):
        pg = out.new_page(width=W*mm/2, height=H*mm/2)
        pg.show_pdf_page(pg.rect, src, p)
    out.save(a7); src.close(); out.close()
    print("wrote", a5, "and", a7)
    return names, draws


if __name__ == "__main__":
    build()
