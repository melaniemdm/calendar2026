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
IMAGES_DIR = config["paths"]["images_dir"]
OUTPUT_DIR = config["paths"]["output_dir"]
BACKGROUND_IMAGE = config["paths"].get("background_image", None)

LAYOUT = config["layout"]
DPI = LAYOUT["dpi"]
WIDTH_IN = LAYOUT["paper"]["width_in"]
HEIGHT_IN = LAYOUT["paper"]["height_in"]
BG_COLOR = LAYOUT["background_color"]
TEXT_COLOR = LAYOUT["text_color"]
WEEKEND_BG = LAYOUT["weekend_bg"]
GRID_COLOR = LAYOUT["grid_color"]

HOLIDAYS = {(y, m, d): label for (y, m, d, label) in config["holidays"]}

MONTHS_FR = [
    "JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN",
    "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"
]
WEEKDAYS_FR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


# --- Fonctions principales ---
print(f"🔍 BACKGROUND_IMAGE = {BACKGROUND_IMAGE}")
print(f"📁 Chemin absolu = {os.path.abspath(BACKGROUND_IMAGE)}")
print(f"🧩 Existe ? {os.path.exists(BACKGROUND_IMAGE)}")

def draw_cover_page(year, outpath, image_path=None):
    """Crée la page de garde du calendrier"""
    fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN), dpi=DPI)
    ax = plt.axes([0, 0, 1, 1])
    ax.set_xlim(0, 210)
    ax.set_ylim(0, 297)
    ax.axis("off")

    # --- Lecture des effets depuis la config ---
    effects_cfg = config.get("effects", {})
    BLUR_RADIUS = effects_cfg.get("blur_radius", 0)
    VEIL_OPACITY = effects_cfg.get("white_veil_opacity", 0.25) # Valeur par default de l'opacité
    VEIL_COLOR = effects_cfg.get("white_veil_color", "#ffffff") # Couleur par default de l'opacité
    print(f"🎨 Effets : flou={BLUR_RADIUS}, voile={VEIL_OPACITY*100:.0f}% couleur={VEIL_COLOR}")

    # --- Fond d'image global (étendu sans déformation + flou + voile) ---
    if BACKGROUND_IMAGE and os.path.exists(BACKGROUND_IMAGE):
        try:
            pil_img = Image.open(BACKGROUND_IMAGE).convert("RGB")

            # Appliquer le flou
            if BLUR_RADIUS > 0:
                pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))
                print(f"Flou appliqué (radius={BLUR_RADIUS})")

            # Appliquer le voile de couleur
            if VEIL_OPACITY > 0:
                # Convertir la couleur hex en tuple RGB
                r = int(VEIL_COLOR[1:3], 16)
                g = int(VEIL_COLOR[3:5], 16)
                b = int(VEIL_COLOR[5:7], 16)
                overlay = Image.new("RGB", pil_img.size, (r, g, b))
                pil_img = Image.blend(pil_img, overlay, VEIL_OPACITY)
                print(f"Voile {VEIL_COLOR} appliqué (opacité={VEIL_OPACITY*100:.0f}%)")

            # Conversion vers numpy pour imshow
            bg_img = np.array(pil_img)

            img_h, img_w = bg_img.shape[:2]
            frame_w, frame_h = 210, 297
            img_ratio = img_w / img_h
            frame_ratio = frame_w / frame_h

            # Adapter sans déformation
            if img_ratio > frame_ratio:
                new_h = frame_h
                new_w = frame_h * img_ratio
            else:
                new_w = frame_w
                new_h = frame_w / img_ratio

            offset_x = (frame_w - new_w) / 2
            offset_y = (frame_h - new_h) / 2

            ax.imshow(
                bg_img,
                extent=[offset_x, offset_x + new_w, offset_y, offset_y + new_h],
                aspect="auto",
                zorder=0,
            )
            print("Fond ajusté sans déformation avec effets appliqués")

        except Exception as e:
            print(f"Erreur lors du chargement du fond : {e}")
            ax.add_patch(Rectangle((0, 0), 210, 297, facecolor=BG_COLOR, zorder=0))
    else:
        print(" Aucun fond trouvé — utilisation d’une couleur unie.")
        ax.add_patch(Rectangle((0, 0), 210, 297, facecolor=BG_COLOR, zorder=0))

    # --- Titre principal ---
    ax.text(105, 240, f"CALENDRIER {year}", fontsize=36, fontweight="bold",
            color=TEXT_COLOR, ha="center", va="center")
    ax.text(105, 220, ASSOCIATION, fontsize=16, fontweight="bold", color=TEXT_COLOR,
            ha="center", va="center")

    # --- Zone photo (sans déformation) ---
    photo_x, photo_y, photo_w, photo_h = 25, 60, 160, 120
    if image_path and os.path.exists(image_path):
        try:
            img = mpimg.imread(image_path)
            img_h, img_w = img.shape[:2]
            img_ratio = img_w / img_h
            frame_ratio = photo_w / photo_h

            if img_ratio > frame_ratio:
                new_w = photo_w
                new_h = photo_w / img_ratio
            else:
                new_h = photo_h
                new_w = photo_h * img_ratio

            offset_x = photo_x + (photo_w - new_w) / 2
            offset_y = photo_y + (photo_h - new_h) / 2

            ax.imshow(img, extent=[offset_x, offset_x + new_w, offset_y, offset_y + new_h],
                      aspect="auto", zorder=5)
            print(" Image de couverture insérée sans déformation")

        except Exception as e:
            print(f" Erreur lors de l’insertion de la photo : {e}")
    else:
        print(f" Image non trouvée : {image_path}")
        ax.add_patch(Rectangle((photo_x, photo_y), photo_w, photo_h,
                               facecolor="#e6e6e6", edgecolor="#dddddd", linewidth=1))
        ax.text(photo_x + photo_w / 2, photo_y + photo_h / 2,
                "ZONE PHOTO DE COUVERTURE", fontsize=14, color="#888888",
                ha="center", va="center")

    # --- Sauvegarde ---
    fig.savefig(outpath, dpi=DPI, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f" Page de garde enregistrée sous : {outpath}")






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
