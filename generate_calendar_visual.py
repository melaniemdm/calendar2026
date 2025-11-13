#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import calendar
import yaml
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

# --- Lecture du fichier de configuration ---
CONFIG_PATH = "config.yaml"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

YEAR = config["year"]
ASSOCIATION = config["association"]

# --- Chemins ---
paths = config["paths"]
IMAGES_DIR = paths["images_dir"]
OUTPUT_DIR = paths["output_dir"]
BACKGROUND_IMAGE = paths.get("background_image")

# --- Layout / mise en page ---
layout = config["layout"]
DPI = layout["dpi"]
WIDTH_IN = layout["paper"]["width_in"]
HEIGHT_IN = layout["paper"]["height_in"]
BG_COLOR = layout["background_color"]
TEXT_COLOR = layout["text_color"]
WEEKEND_BG = layout["weekend_bg"]
GRID_COLOR = layout["grid_color"]

# --- Effets visuels ---
effects = config.get("effects", {})
BLUR_RADIUS = effects.get("blur_radius", 0)
VEIL_OPACITY = effects.get("veil_opacity", 0)
VEIL_COLOR = effects.get("veil_color", "#ffffff")

# --- Fêtes ---
HOLIDAYS = {(y, m, d): label for (y, m, d, label) in config["holidays"]}

MONTHS_FR = [
    "JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN",
    "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"
]
WEEKDAYS_FR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


# --- Fonctions principales ---
print(f" BACKGROUND_IMAGE = {BACKGROUND_IMAGE}")
print(f" Chemin absolu = {os.path.abspath(BACKGROUND_IMAGE)}")
print(f" Existe ? {os.path.exists(BACKGROUND_IMAGE)}")

def draw_cover_page(year, outpath, image_path=None):
    """Crée la page de garde du calendrier"""

    fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN), dpi=DPI)
    ax = plt.axes([0, 0, 1, 1])
    ax.set_xlim(0, 210)
    ax.set_ylim(0, 297)
    ax.axis("off")

    # ----- CONFIG -----
    title_cfg = layout.get("title", {})
    asso_cfg = config.get("association_style", {})
    photo_cfg = layout.get("cover_photo", {})
    effects_cfg = config.get("effects", {})

    # Effets
    BLUR_RADIUS = effects_cfg.get("blur_radius", 0)
    VEIL_OPACITY = effects_cfg.get("white_veil_opacity", 0)
    VEIL_COLOR = effects_cfg.get("white_veil_color", "#ffffff")

    # Photo params
    px = photo_cfg.get("x", 25)
    py = photo_cfg.get("y", 60)
    pw = photo_cfg.get("w", 160)
    ph = photo_cfg.get("h", 120)

    # ================================
    #  FOND DE PAGE : flou + voile + cover
    # ================================
    if BACKGROUND_IMAGE and os.path.exists(BACKGROUND_IMAGE):
        try:
            pil_img = Image.open(BACKGROUND_IMAGE).convert("RGB")

            # Flou
            if BLUR_RADIUS > 0:
                pil_img = pil_img.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))

            # Voile
            if VEIL_OPACITY > 0:
                veil_rgb = tuple(int(VEIL_COLOR[i:i+2], 16) for i in (1, 3, 5))
                overlay = Image.new("RGB", pil_img.size, veil_rgb)
                pil_img = Image.blend(pil_img, overlay, VEIL_OPACITY)

            bg_img = np.array(pil_img)

            # Ajustement COVER
            img_h, img_w = bg_img.shape[:2]
            frame_w, frame_h = 210, 297
            ratio_img = img_w / img_h
            ratio_frame = frame_w / frame_h

            if ratio_img > ratio_frame:
                new_h = frame_h
                new_w = frame_h * ratio_img
            else:
                new_w = frame_w
                new_h = frame_w / ratio_img

            offset_x = (frame_w - new_w) / 2
            offset_y = (frame_h - new_h) / 2

            ax.imshow(
                bg_img,
                extent=[offset_x, offset_x + new_w, offset_y, offset_y + new_h],
                aspect="auto", zorder=0
            )

        except Exception as e:
            print(f"⚠️ Erreur fond : {e}")
            ax.add_patch(Rectangle((0, 0), 210, 297, facecolor=BG_COLOR))
    else:
        ax.add_patch(Rectangle((0, 0), 210, 297, facecolor=BG_COLOR))

    # ================================
    #  TITRE
    # ================================
    ax.text(
        105,
        title_cfg.get("text_y", 240),
        f"CALENDRIER {year}",
        fontsize=title_cfg.get("fontsize", 40),
        fontweight=title_cfg.get("fontweight", "bold"),
        color=title_cfg.get("color", TEXT_COLOR),
        ha="center", va="center",
    )

    # ================================
    #  ASSOCIATION (multi-ligne auto)
    # ================================
    asso_text = ASSOCIATION
    if asso_cfg.get("auto_newline", False):
        token = asso_cfg.get("newline_token", " des ")
        asso_text = asso_text.replace(token, f"\n{token}")

    ax.text(
        105,
        asso_cfg.get("text_y", 220),
        asso_text,
        fontsize=asso_cfg.get("fontsize", 20),
        fontweight=asso_cfg.get("fontweight", "bold"),
        color=asso_cfg.get("color", TEXT_COLOR),
        ha="center", va="center",
    )

    # ================================
    #  PHOTO (ajustée sans déformation)
    # ================================
    if image_path and os.path.exists(image_path):
        try:
            img = mpimg.imread(image_path)
            ih, iw = img.shape[:2]
            ratio = iw / ih
            frame_ratio = pw / ph

            if ratio > frame_ratio:
                new_w = pw
                new_h = pw / ratio
            else:
                new_h = ph
                new_w = ph * ratio

            ox = px + (pw - new_w) / 2
            oy = py + (ph - new_h) / 2

            ax.imshow(img, extent=[ox, ox + new_w, oy, oy + new_h], zorder=5)

        except Exception as e:
            print(f"⚠️ Erreur insertion photo : {e}")
    else:
        ax.add_patch(Rectangle((px, py), pw, ph, facecolor="#cccccc"))
        ax.text(px + pw / 2, py + ph / 2, "ZONE PHOTO",
                ha="center", va="center")

    # ================================
    #  EXPORT
    # ================================
    fig.savefig(outpath, dpi=DPI, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f" Page de garde enregistrée → {outpath}")







def draw_month_visual(year, month, outpath, image_path=None):
    """Crée une page mensuelle du calendrier"""
    fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN), dpi=DPI)
    ax = plt.axes([0, 0, 1, 1])
    ax.set_xlim(0, 210)
    ax.set_ylim(0, 297)
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), 210, 297, facecolor=BG_COLOR, edgecolor="none"))

    # Titre
    ax.text(10, 282, f"{MONTHS_FR[month-1]} {year}", fontsize=22,
            color=TEXT_COLOR, va="top", ha="left", fontweight="bold")

    # --- Zone photo ---
    photo_x, photo_y, photo_w, photo_h = 10, 160, 190, 110

    if image_path and os.path.exists(image_path):
        try:
            img = mpimg.imread(image_path)
            print(f"   ✅ Image chargée : {image_path} | type={type(img)}, shape={getattr(img, 'shape', 'inconnu')}")
            if img is None or (hasattr(img, "size") and img.size == 0):
                print(f"   ⚠️ Image vide ou non lisible pour {MONTHS_FR[month-1]}")
                ax.add_patch(Rectangle((photo_x, photo_y), photo_w, photo_h,
                                       facecolor="#e6e6e6", edgecolor="#dddddd", linewidth=1))
                ax.text(photo_x + photo_w/2, photo_y + photo_h/2, "ZONE PHOTO",
                        fontsize=18, color="#888888", ha="center", va="center")
            else:
                ax.imshow(img, extent=[photo_x, photo_x + photo_w, photo_y, photo_y + photo_h],
                          aspect='auto', zorder=5)
                print(f"✅ Image insérée pour {MONTHS_FR[month-1]} : {image_path}")
        except Exception as e:
            print(f"⚠️ Erreur lors de l’insertion de {MONTHS_FR[month-1]} : {e}")
    else:
        print(f"❌ Image non trouvée pour {MONTHS_FR[month-1]} : {image_path}")
        ax.add_patch(Rectangle((photo_x, photo_y), photo_w, photo_h,
                               facecolor="#e6e6e6", edgecolor="#dddddd", linewidth=1))
        ax.text(photo_x + photo_w/2, photo_y + photo_h/2, "ZONE PHOTO",
                fontsize=18, color="#888888", ha="center", va="center")

    # --- Grille du calendrier ---
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)
    left, bottom, right, top = 10, 22, 200, 150
    cols = 7
    rows = 1 + len(month_days)
    cell_w = (right - left) / cols
    cell_h = (top - bottom) / rows

    # Entêtes
    for c in range(cols):
        x = left + c * cell_w
        y = top - cell_h
        ax.add_patch(Rectangle((x, y), cell_w, cell_h,
                               facecolor="white", edgecolor=GRID_COLOR, linewidth=0.8))
        ax.text(x + cell_w/2, y + cell_h/2, WEEKDAYS_FR[c],
                ha="center", va="center", fontsize=12, color=TEXT_COLOR)

    # Jours
    for r, week in enumerate(month_days):
        for c, day in enumerate(week):
            x = left + c * cell_w
            y = top - (r + 2) * cell_h
            is_weekend = (c >= 5)
            face = WEEKEND_BG if is_weekend else "white"
            ax.add_patch(Rectangle((x, y), cell_w, cell_h,
                                   facecolor=face, edgecolor=GRID_COLOR, linewidth=0.8))
            if day != 0:
                color = "red" if (year, month, day) in HOLIDAYS else TEXT_COLOR
                ax.text(x + cell_w * 0.08, y + cell_h * 0.78, str(day),
                        ha="left", va="top", fontsize=11, color=color)

    fig.savefig(outpath, dpi=DPI, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f"💾 Mois {MONTHS_FR[month-1]} enregistré sous : {outpath}")


def generate_full_calendar():
    """Crée la couverture + les 12 mois avec images"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("🖨 Création de la page de garde...")

    cover_path = os.path.join(IMAGES_DIR, "cover.png")
    draw_cover_page(YEAR, os.path.join(OUTPUT_DIR, f"ASMAA_Couverture_{YEAR}.png"), cover_path)

    print("🗓 Génération des 12 mois...")
    for month in range(1, 13):
        month_name = MONTHS_FR[month - 1].lower()
        image_path = os.path.join(IMAGES_DIR, f"{month:02d}_{month_name}.png")

        print(f"\n🔍 Recherche d’image pour {MONTHS_FR[month - 1]} : {image_path}")
        out = os.path.join(OUTPUT_DIR, f"ASMAA_Calendrier_{YEAR}_{month:02d}_A4.png")
        draw_month_visual(YEAR, month, out, image_path)
        print(f"  → {MONTHS_FR[month - 1]} créé ✅")

    print(f"\n🎉 Génération complète terminée ! Les fichiers sont dans '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    generate_full_calendar()
